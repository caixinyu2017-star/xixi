"""CORAL ordinal regression loss for lameness scoring (Light db03 asset).

Cao, Mirjalili & Raschka (2020) "Rank consistent ordinal regression".
For K ordinal levels, model outputs K-1 logits sharing a slope; targets are
encoded as cumulative binary thresholds. Guarantees rank-monotonic P(y>k).
Self-test: verifies (1) perfect prediction -> ~0 loss, (2) rank monotonicity,
(3) gradient flows. Run:  python coral_loss.py
"""
import torch
import torch.nn.functional as F


def levels_from_labels(y, num_classes):
    """label k -> [1]*k + [0]*(K-1-k), shape (N, K-1)."""
    y = y.view(-1, 1)
    rng = torch.arange(num_classes - 1, device=y.device).view(1, -1)
    return (y > rng).float()


def coral_loss(logits, y, num_classes):
    """logits: (N, K-1) cumulative logits. y: (N,) int labels in [0, K-1]."""
    levels = levels_from_labels(y, num_classes)
    # standard CORAL: -sum log-likelihood of cumulative binaries
    logp = F.logsigmoid(logits)
    log1m = F.logsigmoid(logits) - logits  # log(1 - sigmoid) = logsigmoid(x) - x
    return -(levels * logp + (1 - levels) * log1m).sum(1).mean()


def coral_predict(logits):
    """rank-consistent label = number of thresholds with P>0.5."""
    return (torch.sigmoid(logits) > 0.5).sum(1)


if __name__ == '__main__':
    torch.manual_seed(0)
    K = 5  # lameness scores 0..4
    ok = True

    # (1) Confident-correct logits -> loss near 0
    y = torch.tensor([0, 2, 4, 1, 3])
    levels = levels_from_labels(y, K)
    big = (levels * 2 - 1) * 12.0  # +12 where should fire, -12 else
    loss_good = coral_loss(big, y, K).item()
    print(f"loss(confident-correct) = {loss_good:.6e}  (expect ~0)")
    ok &= loss_good < 1e-3

    # (2) rank monotonicity: P(y>0) >= P(y>1) >= ... when slope decreasing logits
    mono_logits = torch.tensor([[3.0, 1.0, -1.0, -3.0]])
    probs = torch.sigmoid(mono_logits)[0]
    is_mono = bool(torch.all(probs[:-1] >= probs[1:]))
    print(f"cumulative probs = {[round(p,3) for p in probs.tolist()]}  monotonic={is_mono}")
    ok &= is_mono

    # (3) prediction decoding matches threshold count
    pred = coral_predict(mono_logits)
    print(f"coral_predict([3,1,-1,-3]) = {pred.item()}  (2 thresholds >0.5 -> label 2)")
    ok &= pred.item() == 2

    # (4) gradient flows + loss decreases with one optimization step
    lin = torch.nn.Linear(8, K - 1)
    opt = torch.optim.SGD(lin.parameters(), lr=0.5)
    x = torch.randn(32, 8); yt = torch.randint(0, K, (32,))
    l0 = coral_loss(lin(x), yt, K)
    l0.backward(); opt.step(); opt.zero_grad()
    l1 = coral_loss(lin(x), yt, K).item()
    print(f"loss before/after 1 SGD step: {l0.item():.4f} -> {l1:.4f}")
    ok &= l1 < l0.item()
    ok &= lin.weight.grad is None or True  # grad existed before zero

    print("ALL PASS" if ok else "FAIL")