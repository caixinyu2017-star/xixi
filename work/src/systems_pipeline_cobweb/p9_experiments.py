# -*- coding: utf-8 -*-
"""Paper 9 — experiments.

Runs the calibrated model through the technology shock, the belief regimes, the
stability frontier, the information and capacity instruments, and a global sensitivity
sweep, and writes every number the manuscript reports to p9_results.json.
"""
import json
import os

import numpy as np

import p9_model as M
import p9_calibrate as C

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20260731

# the shock: a permanent fall in the exposed field's relative productivity, switched on
# after a settled period, calibrated below to the observed rise in new-graduate
# unemployment in computing
SHOCK_T = 10
HORIZON = 90

# baseline belief parameters
PHI = 1.5     # trend extrapolation
PSI = 20.0    # intensity of choice over forecasting rules
COST = 0.02   # cost of the anchored rule, per period
MEM = 0.5     # memory in the fitness measure


def shock_fn(z, t0=SHOCK_T):
    return lambda t: 1.0 if t < t0 else z


def run(p, st, z, periods=HORIZON, **kw):
    q = p.copy()
    for k, v in kw.items():
        setattr(q, k, v)
    return M.simulate(q, st, periods, shock=shock_fn(z)), q


def path_stats(out, s0, t0=SHOCK_T):
    """Overshoot, timing and settling of the enrolment response."""
    s = out['s']
    post = s[t0:]
    final = float(np.mean(s[-10:]))
    trough = float(post.min())
    k = int(np.argmin(post))
    long_run = final / s0 - 1.0
    peak = trough / s0 - 1.0
    amp = float(peak / long_run) if abs(long_run) > 1e-12 else float('nan')
    # settling: first date after the trough at which the share stays within 10% of the
    # remaining gap to its long-run value
    tol = 0.1 * abs(final - trough)
    settle = None
    for i in range(k, len(post)):
        if np.all(np.abs(post[i:] - final) <= tol + 1e-15):
            settle = i
            break
    return dict(pre_shock_share=float(s0),
                long_run_share=final,
                trough_share=trough,
                long_run_change_pct=100.0 * long_run,
                trough_change_pct=100.0 * peak,
                amplification=amp,
                years_to_trough=int(k),
                years_to_settle=(int(settle) if settle is not None else None),
                first_year_change_pct=float(100.0 * (s[t0] / s0 - 1.0)))


def output_loss(out, p, st, z, t0=SHOCK_T):
    """Discounted output forgone relative to instantaneous adjustment.

    The benchmark is the economy that jumps to the post-shock stationary share the
    moment the shock lands.  The difference is what the adjustment itself costs: output
    lost because too many graduates hold the skills the economy has stopped wanting and
    too few hold the ones it now wants.
    """
    q = p.copy(); q.A = p.A.copy(); q.A[0] = p.A[0] * z
    s_new, st_new, _ = M.steady_state(q)
    Y_star = M.market(q, st_new.E)['Y']
    disc = np.array([(1.0 / (1.0 + p.r)) ** i for i in range(len(out['Y']) - t0)])
    gap = (Y_star - out['Y'][t0:]) / Y_star
    return dict(post_shock_share=float(s_new),
                discounted_loss_pct=float(100.0 * np.sum(disc * gap) / np.sum(disc)),
                peak_gap_pct=float(100.0 * gap.max()),
                undiscounted_10y_loss_pct=float(100.0 * np.mean(gap[:10])))


def main():
    R = {}

    # ------------------------------------------------------------- calibration
    p, m, s0, st, mkt, err = C.calibrate(verbose=False)
    d = C.diagnostics(p, s0, st, mkt)
    R['calibration'] = dict(
        targets=C.TARGETS, external=C.EXTERNAL, moments=m,
        max_abs_log_deviation=err,
        estimated=dict(mu=float(p.mu), A0=float(p.A[0]), beta=float(p.beta),
                       amen=float(p.amen), kappa=float(p.kappa)),
        diagnostics=d,
        belief=dict(phi=PHI, psi=PSI, cost=COST, mem=MEM,
                    n_extrapolative=M.steady_weights(
                        p.copy(psi=PSI, cost=COST))))
    print('calibration err %.2e | share %.4f | gain %.4f' % (err, s0, d['loop_gain']))

    # ------------------------------------------- shock size from the observed data
    # choose z so that the exposed field's new-graduate unemployment rate at the
    # trough of the transition matches the 7.0 per cent observed for computing
    target_u = 0.070
    lo, hi = 0.30, 0.999
    for _ in range(60):
        z = 0.5 * (lo + hi)
        out, q = run(p, st, z, phi=PHI, psi=PSI, cost=COST, mem=MEM)
        peak_u = float(out['u0'][SHOCK_T:].max())
        if peak_u < target_u:
            hi = z
        else:
            lo = z
    z_star = 0.5 * (lo + hi)
    out, q = run(p, st, z_star, phi=PHI, psi=PSI, cost=COST, mem=MEM)
    R['shock'] = dict(relative_productivity_factor=float(z_star),
                      productivity_fall_pct=float(100.0 * (1.0 - z_star)),
                      matched_peak_unemployment=float(out['u0'][SHOCK_T:].max()),
                      target_peak_unemployment=target_u)
    print('shock: A0 x %.4f (%.1f%% fall)' % (z_star, 100 * (1 - z_star)))

    # --------------------------------------------------- baseline transition path
    ps = path_stats(out, s0)
    ol = output_loss(out, p, st, z_star)
    R['transition'] = dict(**ps, **ol,
                           peak_premium_compression_pct=float(
                               100.0 * (out['prem'][SHOCK_T:].min() / out['prem'][0] - 1.0)),
                           peak_unemployment_gap_pp=float(
                               100.0 * (out['u0'][SHOCK_T:] - out['u1'][SHOCK_T:]).max()))
    R['paths'] = {k: [float(v) for v in out[k]]
                  for k in ('s', 'u0', 'u1', 'prem', 'E0', 'Y', 'x', 'n_extrap', 'A0')}
    print('transition: trough %.2f%%  long run %.2f%%  amplification %.2f'
          % (ps['trough_change_pct'], ps['long_run_change_pct'], ps['amplification']))

    # ------------------------------------------------------------ belief regimes
    regimes = [('anchored', dict(phi=0.0, psi=0.0, cost=0.0)),
               ('mixed', dict(phi=PHI, psi=0.0, cost=COST, mem=MEM)),
               ('baseline', dict(phi=PHI, psi=PSI, cost=COST, mem=MEM)),
               ('imitative', dict(phi=PHI, psi=5.0 * PSI, cost=COST, mem=MEM))]
    R['belief_regimes'] = {}
    for name, kw in regimes:
        o, qq = run(p, st, z_star, **kw)
        st_ = path_stats(o, s0)
        lo_ = output_loss(o, p, st, z_star)
        R['belief_regimes'][name] = dict(
            **kw, n_extrapolative=M.steady_weights(qq),
            **{k: st_[k] for k in ('trough_change_pct', 'long_run_change_pct',
                                   'amplification', 'years_to_trough',
                                   'years_to_settle')},
            discounted_loss_pct=lo_['discounted_loss_pct'])
        print('  %-10s n_e=%.2f trough %.1f%% amp %.2f loss %.3f%%'
              % (name, M.steady_weights(qq), st_['trough_change_pct'],
                 st_['amplification'], lo_['discounted_loss_pct']))

    # ------------------------------------------------------- stability frontier
    psis = np.linspace(0.0, 60.0, 31)
    mods = []
    for v in psis:
        q2 = p.copy(phi=PHI, psi=float(v), cost=COST, mem=MEM)
        mods.append(float(M.dominant_mode(q2, st)['modulus']))
    mods = np.array(mods)
    cross = None
    for i in range(len(psis) - 1):
        if mods[i] < 1.0 <= mods[i + 1]:
            w = (1.0 - mods[i]) / (mods[i + 1] - mods[i])
            cross = float(psis[i] + w * (psis[i + 1] - psis[i]))
            break
    R['stability'] = dict(psi_grid=[float(v) for v in psis],
                          modulus=[float(v) for v in mods],
                          psi_critical=cross,
                          psi_baseline=PSI,
                          modulus_baseline=float(
                              M.dominant_mode(p.copy(phi=PHI, psi=PSI, cost=COST, mem=MEM),
                                              st)['modulus']))
    print('stability: critical psi %s' % cross, flush=True)

    # frontier in the two elasticities the literature disputes
    grid = []
    for es in (0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4):
        for sg in (1.5, 2.0, 3.0, 4.0):
            try:
                tg = dict(C.TARGETS); tg['supply_elast'] = es
                ex = dict(C.EXTERNAL); ex['sigma'] = sg
                pp, mm, ss, stt, mk, ee = C.calibrate(tg, ex, verbose=False)
                if ee > 1e-5:
                    continue
                g = float(M.loop_gain(pp, ss))
                md = float(M.dominant_mode(pp.copy(phi=PHI, psi=PSI, cost=COST, mem=MEM),
                                           stt)['modulus'])
                grid.append(dict(supply_elast=es, sigma=sg, loop_gain=g, modulus=md))
            except Exception:
                continue
    R['frontier'] = grid
    print('frontier points: %d' % len(grid), flush=True)

    # ------------------------------------------------------------- instruments
    R['instruments'] = {}
    base_amp = R['transition']['amplification']
    base_loss = R['transition']['discounted_loss_pct']
    for name, kw in [('baseline', {}),
                     ('sharper_wage_signal', dict(omega=1.0)),
                     ('noisier_wage_signal', dict(omega=0.6)),
                     ('pipeline_published_half', dict(pipe=0.5)),
                     ('pipeline_published_full', dict(pipe=1.0))]:
        o, _ = run(p, st, z_star, phi=PHI, psi=PSI, cost=COST, mem=MEM, **kw)
        s_ = path_stats(o, s0); l_ = output_loss(o, p, st, z_star)
        # how far the entering share sits from the share that would have been chosen
        # with full knowledge of the post-shock fundamental
        mis = float(np.mean(np.abs(o['s'][SHOCK_T:] - l_['post_shock_share']))
                    / l_['post_shock_share'] * 100.0)
        R['instruments'][name] = dict(
            mean_misallocation_pct=mis,
            **kw, trough_change_pct=s_['trough_change_pct'],
            amplification=s_['amplification'],
            years_to_settle=s_['years_to_settle'],
            discounted_loss_pct=l_['discounted_loss_pct'],
            loss_reduction_pct=float(100.0 * (1.0 - l_['discounted_loss_pct'] / base_loss)),
            amplification_change_pct=float(100.0 * (s_['amplification'] / base_amp - 1.0)))
        print('  %-24s amp %.2f  loss %.3f%%' % (name, s_['amplification'],
                                                 l_['discounted_loss_pct']))

    # ----------------------------------------------------- global sensitivity
    rng = np.random.default_rng(SEED)
    names = ['D', 'sigma', 'gam', 'delta', 'alpha', 'b']
    lows = np.array([3.0, 1.5, 1.0 / 9, 0.06, 0.4, 0.25])
    highs = np.array([5.0, 4.0, 1.0 / 5, 0.14, 0.6, 0.55])
    n = 192
    cut = (np.arange(n)[:, None] + rng.random((n, len(names)))) / n
    for j in range(len(names)):
        rng.shuffle(cut[:, j])
    draws = lows + cut * (highs - lows)
    amps, loss, mods2, ok = [], [], [], 0
    for row in draws:
        ex = dict(C.EXTERNAL)
        for k, v in zip(names, row):
            ex[k] = int(round(v)) if k == 'D' else float(v)
        try:
            pp, mm, ss, stt, mk, ee = C.calibrate(external=ex, verbose=False)
            if ee > 1e-5:
                continue
            o, _ = run(pp, stt, z_star, phi=PHI, psi=PSI, cost=COST, mem=MEM)
            s_ = path_stats(o, ss); l_ = output_loss(o, pp, stt, z_star)
            if not np.isfinite(s_['amplification']):
                continue
            amps.append(s_['amplification'])
            loss.append(l_['discounted_loss_pct'])
            mods2.append(float(M.dominant_mode(
                pp.copy(phi=PHI, psi=PSI, cost=COST, mem=MEM), stt)['modulus']))
            ok += 1
        except Exception:
            continue
        if ok % 8 == 0:
            print('   sensitivity %d/%d solved' % (ok, n), flush=True)
    amps, loss, mods2 = np.array(amps), np.array(loss), np.array(mods2)
    R['sensitivity'] = dict(
        n_draws=n, n_solved=ok, parameters=names,
        low=[float(v) for v in lows], high=[float(v) for v in highs],
        amplification=dict(mean=float(amps.mean()), p5=float(np.percentile(amps, 5)),
                           p95=float(np.percentile(amps, 95)),
                           share_above_one=float(np.mean(amps > 1.0))),
        loss=dict(mean=float(loss.mean()), p5=float(np.percentile(loss, 5)),
                  p95=float(np.percentile(loss, 95))),
        modulus=dict(mean=float(mods2.mean()), p5=float(np.percentile(mods2, 5)),
                     p95=float(np.percentile(mods2, 95)),
                     share_unstable=float(np.mean(mods2 >= 1.0))),
        draws=dict(amplification=[float(v) for v in amps],
                   loss=[float(v) for v in loss],
                   modulus=[float(v) for v in mods2]))
    print('sensitivity: %d/%d solved, amplification %.2f [%.2f, %.2f]'
          % (ok, n, amps.mean(), np.percentile(amps, 5), np.percentile(amps, 95)))

    with open(os.path.join(HERE, 'p9_results.json'), 'w') as fh:
        json.dump(R, fh, indent=1)
    print('written p9_results.json')
    return R


if __name__ == '__main__':
    main()
