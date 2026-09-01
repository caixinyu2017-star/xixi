# -*- coding: utf-8 -*-
"""A compact reverse-mode automatic differentiation engine on numpy.

The deployment environment provides no deep-learning framework, so the
neural components of this study are built on this engine. It supports
the operations required by the proposed architecture and by every
baseline: dense algebra, gated recurrences, attention with masked
softmax, and the loss terms. Correctness is verified against central
finite differences in ``gradcheck.py``.
"""
from __future__ import annotations

import numpy as np


def _unbroadcast(grad, shape):
    """Reduce a gradient to the shape it was broadcast from."""
    while grad.ndim > len(shape):
        grad = grad.sum(axis=0)
    for i, s in enumerate(shape):
        if s == 1 and grad.shape[i] != 1:
            grad = grad.sum(axis=i, keepdims=True)
    return grad.reshape(shape)


class Tensor:
    __slots__ = ("data", "grad", "_parents", "_backward", "requires_grad")

    def __init__(self, data, requires_grad=False, _parents=(),
                 _backward=None):
        self.data = np.asarray(data, dtype=np.float64)
        self.requires_grad = requires_grad or any(
            p.requires_grad for p in _parents)
        self.grad = None
        self._parents = _parents
        self._backward = _backward

    # -- construction ----------------------------------------------------
    @property
    def shape(self):
        return self.data.shape

    def __repr__(self):
        return "Tensor(shape=%s)" % (self.data.shape,)

    def _make(self, out_data, parents, backward):
        return Tensor(out_data, _parents=parents, _backward=backward)

    # -- elementwise -----------------------------------------------------
    def __add__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = self._make(self.data + other.data, (self, other), None)

        def bw(g):
            return (_unbroadcast(g, self.shape),
                    _unbroadcast(g, other.shape))
        out._backward = bw
        return out

    __radd__ = __add__

    def __mul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = self._make(self.data * other.data, (self, other), None)

        def bw(g):
            return (_unbroadcast(g * other.data, self.shape),
                    _unbroadcast(g * self.data, other.shape))
        out._backward = bw
        return out

    __rmul__ = __mul__

    def __neg__(self):
        return self * -1.0

    def __sub__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __truediv__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = self._make(self.data / other.data, (self, other), None)

        def bw(g):
            return (_unbroadcast(g / other.data, self.shape),
                    _unbroadcast(-g * self.data / other.data ** 2,
                                 other.shape))
        out._backward = bw
        return out

    def __rtruediv__(self, other):
        return Tensor(other) / self

    def __pow__(self, p):
        out = self._make(self.data ** p, (self,), None)
        out._backward = lambda g: (g * p * self.data ** (p - 1),)
        return out

    # -- linear algebra --------------------------------------------------
    def matmul(self, other):
        out = self._make(self.data @ other.data, (self, other), None)

        def bw(g):
            ga = g @ np.swapaxes(other.data, -1, -2)
            gb = np.swapaxes(self.data, -1, -2) @ g
            return (_unbroadcast(ga, self.shape),
                    _unbroadcast(gb, other.shape))
        out._backward = bw
        return out

    __matmul__ = matmul

    def transpose(self, *axes):
        ax = axes if axes else None
        out = self._make(np.transpose(self.data, ax), (self,), None)
        inv = None if ax is None else np.argsort(ax)
        out._backward = lambda g: (np.transpose(g, inv),)
        return out

    @property
    def T(self):
        return self.transpose()

    def reshape(self, *shape):
        out = self._make(self.data.reshape(*shape), (self,), None)
        out._backward = lambda g: (g.reshape(self.shape),)
        return out

    # -- reductions ------------------------------------------------------
    def sum(self, axis=None, keepdims=False):
        out = self._make(self.data.sum(axis=axis, keepdims=keepdims),
                         (self,), None)

        def bw(g):
            gg = np.asarray(g)
            if axis is not None and not keepdims:
                gg = np.expand_dims(gg, axis)
            return (np.broadcast_to(gg, self.shape).copy(),)
        out._backward = bw
        return out

    def mean(self, axis=None, keepdims=False):
        n = (self.data.size if axis is None
             else self.data.shape[axis])
        return self.sum(axis=axis, keepdims=keepdims) * (1.0 / n)

    def max(self, axis=None, keepdims=False):
        idx = np.argmax(self.data, axis=axis)
        out_data = np.max(self.data, axis=axis, keepdims=keepdims)
        out = self._make(out_data, (self,), None)

        def bw(g):
            mask = np.zeros_like(self.data)
            if axis is None:
                mask.flat[np.argmax(self.data)] = 1.0
                return (mask * g,)
            np.put_along_axis(mask, np.expand_dims(idx, axis), 1.0,
                              axis=axis)
            gg = g if keepdims else np.expand_dims(g, axis)
            return (mask * gg,)
        out._backward = bw
        return out

    # -- nonlinearities --------------------------------------------------
    def exp(self):
        e = np.exp(self.data)
        out = self._make(e, (self,), None)
        out._backward = lambda g: (g * e,)
        return out

    def log(self):
        out = self._make(np.log(self.data), (self,), None)
        out._backward = lambda g: (g / self.data,)
        return out

    def tanh(self):
        t = np.tanh(self.data)
        out = self._make(t, (self,), None)
        out._backward = lambda g: (g * (1.0 - t ** 2),)
        return out

    def sigmoid(self):
        s = 1.0 / (1.0 + np.exp(-self.data))
        out = self._make(s, (self,), None)
        out._backward = lambda g: (g * s * (1.0 - s),)
        return out

    def relu(self):
        out = self._make(np.maximum(self.data, 0.0), (self,), None)
        out._backward = lambda g: (g * (self.data > 0),)
        return out

    def leaky_relu(self, slope=0.2):
        d = np.where(self.data > 0, 1.0, slope)
        out = self._make(np.where(self.data > 0, self.data,
                                  slope * self.data), (self,), None)
        out._backward = lambda g: (g * d,)
        return out

    def softmax(self, axis=-1, mask=None):
        z = self.data
        if mask is not None:
            z = np.where(mask, z, -1e30)
        z = z - z.max(axis=axis, keepdims=True)
        e = np.exp(z)
        if mask is not None:
            e = e * mask
        s = e / (e.sum(axis=axis, keepdims=True) + 1e-30)
        out = self._make(s, (self,), None)

        def bw(g):
            dot = (g * s).sum(axis=axis, keepdims=True)
            gi = s * (g - dot)
            if mask is not None:
                gi = gi * mask
            return (gi,)
        out._backward = bw
        return out

    # -- structural ------------------------------------------------------
    def gather_rows(self, idx):
        """Select rows (axis 0) by an integer index array."""
        idx = np.asarray(idx, dtype=int)
        out = self._make(self.data[idx], (self,), None)

        def bw(g):
            gg = np.zeros_like(self.data)
            np.add.at(gg, idx, g)
            return (gg,)
        out._backward = bw
        return out

    def __getitem__(self, item):
        out = self._make(self.data[item], (self,), None)

        def bw(g):
            gg = np.zeros_like(self.data)
            np.add.at(gg, item, g)
            return (gg,)
        out._backward = bw
        return out

    def masked_scale(self, mask):
        """Multiply by a constant 0/1 mask (no gradient to the mask)."""
        m = np.asarray(mask, dtype=np.float64)
        out = self._make(self.data * m, (self,), None)
        out._backward = lambda g: (g * m,)
        return out

    # -- backward --------------------------------------------------------
    def backward(self):
        topo, seen = [], set()

        def build(t):
            if id(t) in seen:
                return
            seen.add(id(t))
            for p in t._parents:
                build(p)
            topo.append(t)

        build(self)
        for t in topo:
            t.grad = None
        self.grad = np.ones_like(self.data)
        for t in reversed(topo):
            if t._backward is None or t.grad is None:
                continue
            grads = t._backward(t.grad)
            for p, g in zip(t._parents, grads):
                if not p.requires_grad and not p._parents:
                    continue
                g = np.asarray(g, dtype=np.float64)
                p.grad = g if p.grad is None else p.grad + g


# ---------------------------------------------------------------------------
def cat(tensors, axis=-1):
    """Concatenate tensors along an existing axis."""
    parts = [t.data for t in tensors]
    out = Tensor(np.concatenate(parts, axis=axis), _parents=tuple(tensors))
    sizes = [p.shape[axis] for p in parts]
    bounds = np.cumsum([0] + sizes)

    def bw(g):
        outs = []
        for k in range(len(tensors)):
            sl = [slice(None)] * g.ndim
            sl[axis] = slice(bounds[k], bounds[k + 1])
            outs.append(g[tuple(sl)])
        return tuple(outs)
    out._backward = bw
    return out


def stack(tensors, axis=0):
    out = Tensor(np.stack([t.data for t in tensors], axis=axis),
                 _parents=tuple(tensors))

    def bw(g):
        return tuple(np.take(g, k, axis=axis) for k in range(len(tensors)))
    out._backward = bw
    return out


def bce(pred, target, eps=1e-7):
    """Mean binary cross-entropy over all entries."""
    t = Tensor(np.asarray(target, dtype=np.float64))
    p = Tensor(np.clip(pred.data, eps, 1 - eps))   # value clip only

    def safe_log(x):
        out = Tensor(np.log(np.clip(x.data, eps, None)), _parents=(x,))
        out._backward = lambda g: (g / np.clip(x.data, eps, None),)
        return out

    one = Tensor(np.ones_like(t.data))
    loss = -(t * safe_log(pred) + (one - t) * safe_log(one - pred))
    del p
    return loss.mean()


# ---------------------------------------------------------------------------
class Adam:
    """Adam optimiser with decoupled gradient clipping."""

    def __init__(self, params, lr=3e-3, b1=0.9, b2=0.999, eps=1e-8,
                 clip=5.0):
        self.p = list(params)
        self.lr, self.b1, self.b2, self.eps, self.clip = lr, b1, b2, eps, clip
        self.m = [np.zeros_like(t.data) for t in self.p]
        self.v = [np.zeros_like(t.data) for t in self.p]
        self.t = 0

    def zero_grad(self):
        for t in self.p:
            t.grad = None

    def step(self):
        self.t += 1
        gs = [np.zeros_like(t.data) if t.grad is None else t.grad
              for t in self.p]
        norm = np.sqrt(sum(float((g ** 2).sum()) for g in gs))
        scale = min(1.0, self.clip / (norm + 1e-12))
        for k, t in enumerate(self.p):
            g = gs[k] * scale
            self.m[k] = self.b1 * self.m[k] + (1 - self.b1) * g
            self.v[k] = self.b2 * self.v[k] + (1 - self.b2) * g * g
            mh = self.m[k] / (1 - self.b1 ** self.t)
            vh = self.v[k] / (1 - self.b2 ** self.t)
            t.data -= self.lr * mh / (np.sqrt(vh) + self.eps)


def param(shape, scale=None, rng=None, zeros=False):
    rng = rng or np.random.default_rng(0)
    if zeros:
        return Tensor(np.zeros(shape), requires_grad=True)
    fan_in = shape[0] if len(shape) > 1 else shape[0]
    s = scale if scale is not None else np.sqrt(2.0 / fan_in)
    return Tensor(rng.normal(0.0, s, shape), requires_grad=True)
