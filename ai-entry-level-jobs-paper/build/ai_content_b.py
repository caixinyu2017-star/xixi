# -*- coding: utf-8 -*-
"""Manuscript content, part B: results, discussion, conclusions.

Every number is read from stats.json, which analysis.py writes, so the text
cannot drift from the computation that produced it.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "stats.json")))

B, P_, W = S["baseline"], S["planner"], S["wedge"]
WS, SH, CH, EX = S["wedge_sources"], S["shock"], S["channels"], S["exposure"]
IMP, IMP2, UNC = (S["implementation_baseline"], S["implementation_post_ai"],
                  S["uncertainty"])
POL = {r["key"]: r for r in S["policy_baseline"]}
POL2 = {r["key"]: r for r in S["policy_post_ai"]}
RIG, SIG, MET = S["rigidity"], S["sigma"], S["meta"]


def _m(t):
    """Typographic minus sign, as the journal's style requires."""
    return t.replace("-", "\u2212")


def pc(x, d=1):
    return _m(("%%.%df" % d) % (100 * x))


def n(x, d=3):
    return _m(("%%.%df" % d) % x)


def lp(x, d=1):
    """A log change reported in per cent."""
    return _m(("%%.%df" % d) % (100 * (math.exp(x) - 1.0)))


def alp(x, d=1):
    return ("%%.%df" % d) % abs(100 * (math.exp(x) - 1.0))


LAB = {"s_m": "mentoring credit", "s_v": "entry-level vacancy subsidy",
       "s_w": "entry-level wage subsidy", "t_a": "tax on artificial intelligence"}
RANK = [r["key"] for r in S["policy_baseline"]
        if r.get("d_welfare_pct") is not None]
BEST = RANK[0]
FEAS = [k for k in RANK if POL[k].get("rate") is not None
        and not (isinstance(POL[k].get("rate"), float)
                 and math.isnan(POL[k]["rate"]))]
WORST = FEAS[-1]
TA_FEASIBLE = "t_a" in FEAS
BEST_SHARE = UNC["best_instrument_shares"].get("gain_" + BEST, 0.0)
RIG0 = RIG[0]
RIG1 = [r for r in RIG if r["gamma_w"] == 1.0][0]
RIGB = [r for r in RIG if abs(r["gamma_w"] - MET["gamma_w"]) < 1e-9][0]
FOLD = 1.0 + W["mentoring"]

def _nan(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


def _t4_rows():
    rows = [["Quantity", "Market", "Constrained optimum", "Gap"]]
    spec = [("Entry-level market tightness", "theta_j", 3, "pct"),
            ("Experienced market tightness", "theta_s", 3, "pct"),
            ("Mentoring per entrant", "m", 4, "pct"),
            ("Aggregate mentoring time", "mentoring", 5, "pct"),
            ("Promotion hazard", "pi", 3, "pct"),
            ("Years to first promotion", "promo_years", 2, "diff"),
            ("Promotion flow", "throughput", 5, "pct"),
            ("Entry-level employed", "e_j", 4, "pct"),
            ("Experienced employed", "e_s", 4, "pct"),
            ("Total unemployment", "U_total", 4, "pct"),
            ("Output", "Y", 4, "pct"),
            ("Welfare", "welfare", 4, "pct")]
    for label, k, d, kind in spec:
        mv, pv = B[k], P_[k]
        gap = (_m("%+.1f%%" % (100 * (pv / mv - 1))) if kind == "pct"
               else _m("%+.2f" % (pv - mv)))
        rows.append([label, n(mv, d), n(pv, d), gap])
    return rows


def _t5_rows():
    rows = [["Outcome", "Baseline", "After the shock", "Change"]]
    ai = SH["target_ai_share"]
    spec = [("AI share of the entry-level task bundle", B["ai_share"], ai,
             _m("%+.2f" % (ai - B["ai_share"]))),
            ("Entry-level employment rate", B["emp_rate_j"],
             B["emp_rate_j"] * math.exp(SH["d_ln_emp_rate_j"]),
             lp(SH["d_ln_emp_rate_j"]) + "%"),
            ("Entry wage", B["w_j"], B["w_j"] * math.exp(SH["d_ln_w_j"]),
             lp(SH["d_ln_w_j"]) + "%"),
            ("Experienced wage", B["w_s"], B["w_s"] * math.exp(SH["d_ln_w_s"]),
             lp(SH["d_ln_w_s"]) + "%"),
            ("Mentoring per entrant", B["m"], B["m"] * math.exp(SH["d_ln_m"]),
             lp(SH["d_ln_m"], 0) + "%"),
            ("Aggregate mentoring time", B["mentoring"],
             B["mentoring"] * math.exp(SH["d_ln_mentoring"]),
             lp(SH["d_ln_mentoring"], 0) + "%"),
            ("Years to first promotion", B["promo_years"],
             B["promo_years"] + SH["d_promo_years"],
             _m("%+.2f yr" % SH["d_promo_years"])),
            ("Promotion flow", B["throughput"],
             B["throughput"] * math.exp(SH["d_ln_throughput"]),
             lp(SH["d_ln_throughput"], 1) + "%"),
            ("Experienced employed", B["e_s"],
             B["e_s"] * math.exp(SH["d_ln_e_s"]), lp(SH["d_ln_e_s"], 1) + "%"),
            ("Output", B["Y"], B["Y"] * (1 + SH["d_Y_pct"] / 100),
             _m("%+.2f%%" % SH["d_Y_pct"])),
            ("Welfare", B["welfare"],
             B["welfare"] * (1 + SH["d_welfare_pct"] / 100),
             _m("%+.2f%%" % SH["d_welfare_pct"])),
            ("Value of being a new entrant", B["U_j"],
             B["U_j"] * (1 + SH["d_U_j_pct"] / 100),
             _m("%+.2f%%" % SH["d_U_j_pct"])),
            ("Efficient / market mentoring", 1 + SH["wedge_mentoring_before"],
             1 + SH["wedge_mentoring_after"],
             _m("%+.2f" % (SH["wedge_mentoring_after"] -
                           SH["wedge_mentoring_before"]))),
            ("Welfare gap to the optimum (%)", SH["welfare_gap_before"],
             SH["welfare_gap_after"],
             _m("%+.2f pp" % (SH["welfare_gap_after"] - SH["welfare_gap_before"])))]
    for label, a, b_, c in spec:
        rows.append([label, n(a, 4), n(b_, 4), c])
    return rows


def _t6_rows():
    rows = [["⟪\\gamma_{w}⟫", "Entry wage (%)",
             "Entry-level employment rate (%)", "Ratio",
             "Aggregate mentoring (%)"]]
    for r in RIG:
        ratio = ("—" if _nan(r["incidence_ratio"]) else n(r["incidence_ratio"], 2))
        rows.append([n(r["gamma_w"], 1), lp(r["d_ln_w_j"], 2),
                     lp(r["d_ln_emp_rate_j"], 2), ratio,
                     lp(r["d_ln_mentoring"], 1)])
    return rows


def _t7_rows():
    rows = [["Instrument", "Baseline", "After the shock"]]
    spec = [("Entry-level vacancy subsidy (% of the vacancy cost)", "s_v", "pc"),
            ("Mentoring credit (% of the mentoring cost)", "s_m", "pc"),
            ("Experienced vacancy subsidy (% of the vacancy cost)", "s_vs", "pc"),
            ("Tax on artificial intelligence", None, "zero"),
            ("Fiscal cost (% of output)", "fiscal_pct_Y", "num"),
            ("Welfare gain (%)", "welfare_gain_pct", "num"),
            ("Aggregate mentoring (%)", "d_mentoring_pct", "num0"),
            ("Years to first promotion", "promo_years", "num")]
    for label, k, kind in spec:
        if kind == "zero":
            rows.append([label, n(S["ai_tax"]["argmax_t_a"], 3),
                         n(S["ai_tax"]["argmax_t_a"], 3)])
        elif kind == "pc":
            rows.append([label, pc(IMP[k], 1), pc(IMP2[k], 1)])
        elif kind == "num0":
            rows.append([label, n(IMP[k], 0), n(IMP2[k], 0)])
        else:
            rows.append([label, n(IMP[k], 2), n(IMP2[k], 2)])
    return rows


def _pol_rows(tbl):
    rows = [["Instrument", "Rate", "Welfare (%)", "Entrant value (%)",
             "Mentoring (%)", "Promotion flow (%)", "MVPF"]]
    for r in tbl:
        if _nan(r.get("rate")):
            rows.append([r["instrument"], "infeasible", "—", "—", "—", "—", "—"])
            continue
        rows.append([r["instrument"], n(r["rate"], 3),
                     n(r["d_welfare_pct"], 3), n(r["d_U_j_pct"], 2),
                     n(r["d_mentoring_pct"], 1), n(r["d_throughput_pct"], 2),
                     n(r["mvpf"], 2)])
    return rows


def _t8_rows():
    rows = _pol_rows(S["policy_baseline"])
    rows.append(["", "", "", "", "", "", ""])
    for r in _pol_rows(S["policy_post_ai"])[1:]:
        rows.append(r)
    return rows


def _t9_rows():
    rows = [["⟪\\sigma⟫", "Entry-level employment rate (%)",
             "Aggregate mentoring (%)", "Efficient / market mentoring",
             "Welfare gap (%)"]]
    for r in SIG:
        rows.append([n(r["sigma"], 1), lp(r["d_ln_emp_rate_j"], 2),
                     lp(r["d_ln_mentoring"], 1),
                     n(1 + r["wedge_mentoring"], 2),
                     n(r["welfare_gap_pct"], 2)])
    return rows


PART_B = [

    # =====================================================================
    ('h1', '5. Results'),

    ('h2', '5.1. The Baseline Allocation and the Training Wedge'),

    ('p', 'Table 4 sets the estimated equilibrium beside the constrained optimum. The '
          'difference is not marginal. The market provides '
          '' + n(1.0 / FOLD, 2) + ' of the socially efficient amount of mentoring—'
          'about one ' + ("seventh" if 6.5 < FOLD < 7.8 else n(FOLD, 1) + "th") + ' of '
          'it—so the promotion hazard is '
          '' + pc(W["pi"], 0) + ' per cent below its efficient level and first '
          'promotion takes ' + n(B["promo_years"], 2) + ' years instead of '
          '' + n(P_["promo_years"], 2) + '. The stock of experienced workers is '
          '' + pc(W["e_s"], 1) + ' per cent below the optimum, output '
          '' + pc(W["Y"], 1) + ' per cent below it, and welfare '
          '' + n(W["welfare_pct"], 2) + ' per cent below it.'),

    ('p', 'What generates that gap matters more than its size. Worker bargaining power '
          'is set exactly equal to the matching elasticity, so the classical search '
          'externality is switched off by construction and none of this is a Hosios '
          'violation. Consistently with Proposition 1, entry-level tightness is close '
          'to efficient—the planner would raise it by only '
          '' + pc(W["theta_j"], 1) + ' per cent—while the training margin is not. '
          'Removing both contracting frictions raises mentoring by '
          '' + n(WS["removed_both_pct"], 0) + ' per cent, and a Shapley '
          'decomposition of that log gap attributes '
          '' + pc(WS["holdup_share"], 0) + ' per cent of it to hold-up and '
          '' + pc(WS["poaching_share"], 0) + ' per cent to poaching. Neither '
          'friction is exotic: hold-up follows from the impossibility of writing an '
          'enforceable contract on how much attention a supervisor gives a recruit, '
          'and poaching from the fact that trained workers can quit. The numerical '
          'check behind Proposition 1 is reported alongside: with the Hosios '
          'condition, no poaching, contractible training and flexible wages, market '
          'and planner agree on every reported quantity to a relative error of '
          '' + ("%.0e" % S["efficiency_check"]["max_rel_gap"]) + '.'),

    ('tabcap', '4', 'The estimated equilibrium and the constrained optimum.'),
    ('table', _t4_rows(), [3600, 1900, 2240, 1900]),

    ('p', 'One aggregate deserves comment because it recurs below. Entry-level '
          'employment measured as a stock is a poor welfare indicator in this economy. '
          'The planner holds ' + pc(abs(W["e_j"]), 0) + ' per cent '
          + ("fewer" if W["e_j"] < 0 else "more") + ' entry-level workers than the '
          'market does, not because it wants fewer people to have first jobs but '
          'because it moves them out of the entry tier '
          '' + n(B["promo_years"] / P_["promo_years"], 1) + ' times faster. With an '
          'exogenous flow of entrants, the entry-level stock confounds inflow with '
          'duration. We therefore report entry-level access as the entry-level '
          'employment rate and the ladder’s output as the promotion flow.'),

    ('h2', '5.2. The Artificial-Intelligence Shock'),

    ('p', 'We now lower the price of one efficiency unit of artificial intelligence '
          'and trace the equilibrium and the optimum along the path. Figure 3 shows '
          'the whole trajectory; Table 5 reports the point at which artificial '
          'intelligence performs ' + pc(SH["target_ai_share"], 0) + ' per cent of '
          'the entry-level task bundle, twice its estimated share, which requires the '
          'price to fall by ' + n(abs(SH["p_a_fall_pct"]), 1) + ' per cent.'),

    ('figure', 'fig3_ai_path.png', 3,
     'The economy as artificial intelligence becomes cheaper. Panel (a): the '
     'entry-level employment rate and the entry wage, indexed to the estimated '
     'baseline. Panel (b): mentoring per entrant and the expected time to promotion. '
     'Panel (c): the ladder’s output—the promotion flow and the stock of experienced '
     'workers. Panel (d): the training wedge, measured as the excess of efficient '
     'over market mentoring, and the welfare gap. The horizontal axis is the share of '
     'the entry-level task bundle performed by artificial intelligence; the estimated '
     'economy sits at ' + pc(B["ai_share"], 0) + ' per cent.'),

    ('tabcap', '5', 'The artificial-intelligence shock: the entry-level task share doubles.'),
    ('table', _t5_rows(), [3800, 1800, 2140, 1900]),

    ('p', 'The first finding is that the burden falls on access rather than on pay. '
          'The entry-level employment rate falls by '
          '' + alp(SH["d_ln_emp_rate_j"]) + ' per cent while the entry wage falls by '
          'only ' + alp(SH["d_ln_w_j"]) + ' per cent, a ratio of '
          '' + n(SH["incidence_ratio"], 1) + ' to one, and the entry-level '
          'unemployment rate rises by '
          '' + n(SH["d_u_rate_j_pp"], 1) + ' percentage points against '
          '' + n(SH["d_u_rate_s_pp"], 2) + ' for experienced workers. This matches '
          'what the payroll evidence reports for the United States, where adjustment '
          'appears in headcount rather than in compensation '
          '{{brynjolfsson2025canaries}}, and it explains why studies that look for '
          'wage effects find little {{humlum2025}}. Section 5.4 shows that this '
          'pattern is not a property of the technology.'),

    ('p', 'The second finding is the one we did not expect, and it is the paper’s main '
          'substantive result. The ladder does not break. Mentoring per entrant rises '
          'by ' + lp(SH["d_ln_m"], 0) + ' per cent, aggregate mentoring by '
          '' + lp(SH["d_ln_mentoring"], 0) + ' per cent, the expected time to first '
          'promotion falls from ' + n(B["promo_years"], 2) + ' to '
          '' + n(B["promo_years"] + SH["d_promo_years"], 2) + ' years, the flow of '
          'promotions '
          + ("rises" if SH["d_ln_throughput"] > 0 else "falls") + ' by '
          '' + alp(SH["d_ln_throughput"], 1) + ' per cent and the stock of '
          'experienced workers '
          + ("rises" if SH["d_ln_e_s"] > 0 else "falls") + ' by '
          '' + alp(SH["d_ln_e_s"], 1) + ' per cent. Firms respond to a smaller '
          'intake by training it far more intensively. The mechanism is a '
          'general-equilibrium one that a partial-equilibrium account would miss: '
          'fewer entrants means more experienced time available per entrant and a '
          'lower opportunity cost of the mentor’s hour, while the promotion option '
          'itself is unaffected by a technology that cannot mentor. What artificial '
          'intelligence does to the career ladder is narrow the gate, not dismantle '
          'the staircase behind it.'),

    ('p', 'The third finding follows from the second and reverses a natural prior. '
          'Panel (d) shows that the training wedge does not widen as artificial '
          'intelligence spreads; it narrows, from '
          '' + n(1 + SH["wedge_mentoring_before"], 1) + ' to '
          '' + n(1 + SH["wedge_mentoring_after"], 1) + ' times the market level, '
          'and the welfare gap falls from '
          '' + n(SH["welfare_gap_before"], 2) + ' to '
          '' + n(SH["welfare_gap_after"], 2) + ' per cent. Because scarcer entrants '
          'are individually more worth training, the private return to mentoring moves '
          'towards the social return. The training externality is large, but it is a '
          'pre-existing feature of the contracting environment, not something the '
          'technology creates or aggravates. Aggregate output rises by '
          '' + n(SH["d_Y_pct"], 1) + ' per cent and aggregate welfare by '
          '' + n(SH["d_welfare_pct"], 2) + ' per cent, while the value of being a '
          'new entrant '
          + ("rises" if SH["d_U_j_pct"] > 0 else "falls") + ' by '
          '' + n(abs(SH["d_U_j_pct"]), 2) + ' per cent. What the shock produces is a '
          'distributional problem sitting on top of an efficiency problem that was '
          'already there, and the two require different instruments.'),

    ('h2', '5.3. Decomposing the Response'),

    ('p', 'To identify what the employment response is made of we deactivate '
          'individual channels by holding the relevant object at its baseline value '
          'and re-solving, attributing the total by the Shapley value over all '
          'deactivation orders, which makes the decomposition exact and '
          'order-independent. Three channels are considered beyond direct '
          'substitution: the training margin, meaning the response of mentoring '
          'intensity; the promotion-value margin, meaning the revaluation of the '
          'experienced job that the entry-level match delivers on promotion; and the '
          'senior-scarcity margin, meaning the general-equilibrium response of the '
          'price of experienced time.'),

    ('figure', 'fig4_channels.png', 4,
     'Shapley decomposition of the change in the entry-level employment rate when '
     'artificial intelligence doubles its share of the entry-level task bundle. '
     'Contributions are in log points multiplied by one hundred and sum exactly to '
     'the total; shares in parentheses are of the total response.'),

    ('p', 'Direct task substitution accounts for '
          '' + pc(CH["direct"] / CH["total"], 0) + ' per cent of the fall in the '
          'entry-level employment rate and the training margin for '
          '' + pc(CH["training"] / CH["total"], 0) + ' per cent, while the '
          'promotion-value and senior-scarcity margins together account for under '
          '' + pc((CH["promotion_value"] + CH["senior_scarcity"]) / CH["total"], 0) +
          ' per cent. The decomposition is exact to '
          '' + ("%.0e" % abs(CH["check"])) + ' log points. The training margin '
          'therefore does double duty: it is what saves the ladder, and it is also '
          'what deepens the fall in entry-level access, because a firm that intends to '
          'mentor an entrant intensively is more selective about opening the position '
          'in the first place. A reduced-form estimate of the displacement elasticity, '
          'however well identified, recovers only the first of these terms.'),

    ('h2', '5.4. Who Bears the Shock: Wage Rigidity and Incidence'),

    ('p', 'Proposition 2 says that the split of the shock between pay and employment '
          'is governed by the wage rule rather than by the technology. Table 6 and '
          'panel (a) of Figure 7 quantify it. In the flexible-wage economy '
          '⟪(\\gamma_{w} = 0)⟫ the same shock lowers the entry wage by '
          '' + alp(RIG0["d_ln_w_j"]) + ' per cent and the entry-level employment '
          'rate by only ' + alp(RIG0["d_ln_emp_rate_j"], 2) + ' per cent. With a '
          'fixed entry wage ⟪(\\gamma_{w} = 1)⟫ the wage does not move at all and the '
          'employment rate falls by ' + alp(RIG1["d_ln_emp_rate_j"]) + ' per cent. '
          'The ratio of the employment response to the wage response rises '
          'monotonically from ' + n(RIG0["incidence_ratio"], 2) + ' to infinity '
          'across that range, passing through '
          '' + n(RIGB["incidence_ratio"], 1) + ' at our baseline value of '
          '' + n(MET["gamma_w"], 1) + '.'),

    ('tabcap', '6', 'Incidence of the same shock as a function of the real rigidity of the entry wage.'),
    ('table', _t6_rows(), [1100, 2100, 2800, 1340, 2300]),

    ('p', 'This has an empirical payoff. The stylised fact that motivates the '
          'literature—large employment effects for young workers, negligible effects '
          'on their pay—is not evidence about artificial intelligence at all. It is '
          'evidence that entry wages are rigid. A flexible-wage economy hit by exactly '
          'the same technology shock would show the opposite pattern, and would '
          'generate the precise nulls on employment that the Danish evidence reports '
          '{{humlum2025}}. The apparent conflict between studies finding large '
          'employment effects and studies finding none is therefore not necessarily a '
          'conflict about the technology; it is consistent with a difference in '
          'wage-setting institutions between the settings studied. In China, where '
          'provincial minimum wages bind for entry-level urban positions '
          '{{mayneris2018}} and graduate pay scales are compressed, the model places '
          'the economy towards the rigid end of that range.'),

    ('h2', '5.5. Held-Out Validation: The Exposure Gradient'),

    ('p', 'No information about employment by exposure entered the calibration, so we '
          'can ask the model a question it was not fitted to answer. Consider '
          'occupation groups differing only in how much of their entry-level task '
          'content artificial intelligence can perform, spanning shares from '
          '' + pc(EX["share_lo"], 0) + ' to ' + pc(EX["share_hi"], 0) + ' per '
          'cent, and compute for each the change in entry-level and experienced '
          'employment relative to a pre-artificial-intelligence benchmark. The '
          'difference between the most and the least exposed group, of entry-level '
          'relative to experienced employment, is the model analogue of a '
          'difference-in-differences estimate.'),

    ('figure', 'fig5_exposure.png', 5,
     'Held-out validation. Panel (a): the predicted change in entry-level and '
     'experienced employment, relative to a pre-artificial-intelligence benchmark, '
     'across occupation groups differing in the share of entry-level task content '
     'that artificial intelligence performs. Panel (b): the implied difference '
     'between the most and least exposed groups against the payroll-data estimate for '
     'United States workers aged 22 to 25 reported by Brynjolfsson, Chandar and Chen. '
     'Neither that estimate nor any employment-by-exposure information was used in '
     'the calibration.'),

    ('p', 'The model predicts ' + n(EX["did_pct"], 1) + ' per cent against a payroll '
          'estimate of ' + n(EX["target_pct"], 1) + ' per cent '
          '{{brynjolfsson2025canaries}}. It also reproduces two features of that study '
          'that were not targeted: the gradient is monotone in exposure, and the '
          'corresponding difference in entry wages is only '
          '' + n(EX["wage_did_pct"], 1) + ' per cent, so the model delivers the '
          'employment-not-pay pattern at roughly the observed relative magnitude. We '
          'read this as corroboration rather than confirmation, for two reasons. The '
          'calibration targets are Chinese and the validation estimate American, so '
          'the comparison presumes that technology and contracting, rather than '
          'national institutions, dominate this margin—a presumption that Section 5.4 '
          'shows to be only partly warranted, since the wage rule matters a great '
          'deal. And the model compares steady states whereas the estimate is a '
          'medium-run difference, so the two objects coincide only if adjustment is '
          'substantially complete.'),

    ('h2', '5.6. Implementing the Optimum, and the Tax That Should Not Be Levied'),

    ('p', 'Because the wedges are known they can be priced. Table 7 reports the '
          'combination of an entry-level vacancy subsidy, a mentoring credit and an '
          'experienced-tier vacancy subsidy that reproduces the planner’s allocation '
          'exactly. At the baseline the required rates are '
          '' + pc(IMP["s_v"], 1) + ' per cent of the entry-level vacancy cost, '
          '' + pc(IMP["s_m"], 1) + ' per cent of the mentoring cost and '
          '' + pc(IMP["s_vs"], 1) + ' per cent of the experienced vacancy cost, at a '
          'fiscal cost of ' + n(IMP["fiscal_pct_Y"], 2) + ' per cent of output. They '
          'raise welfare by ' + n(IMP["welfare_gain_pct"], 2) + ' per cent, raise '
          'aggregate mentoring by ' + n(IMP["d_mentoring_pct"], 0) + ' per cent and '
          'cut time to first promotion to ' + n(IMP["promo_years"], 2) + ' years. '
          'After the shock the required mentoring credit is '
          '' + pc(IMP2["s_m"], 1) + ' per cent, '
          + ("higher" if IMP2["s_m"] > IMP["s_m"] else "lower") + ' than before, which '
          'is the policy counterpart of the narrowing wedge documented in Section 5.2.'),

    ('tabcap', '7', 'Subsidies that decentralise the constrained optimum.'),
    ('table', _t7_rows(), [4700, 2470, 2470]),

    ('p', 'One entry in that table is a zero, and it is the most interesting number in '
          'the paper. The welfare-maximising tax on artificial intelligence, once the '
          'ladder subsidies are in place, is ' + n(S["ai_tax"]["argmax_t_a"], 3) + '. '
          'Conditional on the allocation of labour, firms hire artificial intelligence '
          'until its marginal product equals its price, and the planner’s condition '
          'for the input is identical, so the input is efficiently priced. The '
          'distortion in this economy is not in the market for artificial '
          'intelligence; it is in the market for training. Taxing the technology to '
          'protect entry-level jobs treats a symptom at the cost of output, and once '
          'the ladder is correctly subsidised there is nothing left for the tax to '
          'correct.'),

    ('h2', '5.7. Instruments at a Common Budget'),

    ('p', 'Governments do not implement first-best packages; they choose an instrument '
          'and a budget. We therefore fix a common fiscal cost of '
          '' + n(100 * MET["budget"], 2) + ' per cent of output—of the order of a '
          'national youth-employment programme—and ask what each of four instruments '
          'buys. Welfare is output net of recruiting and technology costs plus the '
          'flow value of non-employment, so transfers net out and only efficiency '
          'gains appear. The marginal value of public funds is aggregate willingness '
          'to pay over net government cost, which in this accounting is'),
    ('eq', 'eq24', 24),
    ('p', 'so that a value above one identifies an instrument that returns more than '
          'it costs. Figure 6 and Table 8 report the comparison at the baseline and '
          'after the shock.'),

    ('figure', 'fig6_policy.png', 6,
     'Four instruments at a common fiscal cost, evaluated at the estimated baseline '
     'and after artificial intelligence doubles its share of the entry-level task '
     'bundle. Panel (a): welfare gain. Panel (b): change in the value of being a new '
     'entrant. Panel (c): marginal value of public funds; the dotted line marks '
     'unity. The tax on artificial intelligence is absent from the baseline panels '
     'because its base is too elastic to raise the required revenue at any rate.'),

    ('p', 'The ranking is unambiguous and the spread is large. The ' + LAB[BEST] +
          ' delivers a welfare gain of '
          '' + n(POL[BEST]["d_welfare_pct"], 3) + ' per cent, raises aggregate '
          'mentoring by ' + n(POL[BEST]["d_mentoring_pct"], 0) + ' per cent, raises '
          'the value of being a new entrant by '
          '' + n(POL[BEST]["d_U_j_pct"], 2) + ' per cent and shortens time to '
          'promotion by ' + n(abs(POL[BEST]["d_promo_years"]), 2) + ' years, with a '
          'marginal value of public funds of '
          '' + n(POL[BEST]["mvpf"], 1) + '. The entry-level vacancy subsidy is a '
          'distant second at ' + n(POL["s_v"]["d_welfare_pct"], 3) + ' per cent and '
          'a marginal value of ' + n(POL["s_v"]["mvpf"], 2) + '. The entry-level '
          'wage subsidy is worse than doing nothing: it lowers welfare by '
          '' + n(abs(POL["s_w"]["d_welfare_pct"]), 3) + ' per cent and has a '
          'marginal value of ' + n(POL["s_w"]["mvpf"], 2) + ', because by raising '
          'the entry wage it raises the cost of the very matches whose training '
          'content is under-provided and crowds mentoring out by '
          '' + n(abs(POL["s_w"]["d_mentoring_pct"]), 0) + ' per cent.'),

    ('p', 'The tax on artificial intelligence cannot be assessed at the common budget '
          'in the baseline economy for an instructive reason: its base is too elastic. '
          'The largest revenue any rate can raise is '
          '' + n(S.get("ai_tax_laffer", {}).get("peak_revenue_pct_Y", 0.0), 3) + ' '
          'per cent of output, below the envelope we set, so the instrument is '
          'infeasible at that scale before its welfare properties are even considered. '
          'After the shock the base is larger and the tax becomes feasible, at which '
          'point it lowers welfare by '
          '' + n(abs(POL2["t_a"]["d_welfare_pct"]), 3) + ' per cent with a marginal '
          'value of public funds of ' + n(POL2["t_a"]["mvpf"], 2) + '—the worst of '
          'the four. The ordering after the shock is otherwise preserved, with the '
          + LAB[BEST] + ' delivering ' + n(POL2[BEST]["d_welfare_pct"], 3) + ' per '
          'cent at a marginal value of ' + n(POL2[BEST]["mvpf"], 1) + '.'),

    ('tabcap', '8', 'Four instruments at a common fiscal cost. The upper block is the estimated baseline, the lower block the economy after the artificial-intelligence shock.'),
    ('table', _t8_rows(), [2560, 1080, 1300, 1400, 1300, 1400, 600]),
    ('notes', 'A marginal value of public funds above one identifies an instrument that returns more than it costs. The tax on artificial intelligence is infeasible at this budget in the baseline economy because its base is too elastic; the maximum revenue any rate can raise is reported in Section 5.7.'),

    ('p', 'The economics behind the ordering is transparent. The mentoring credit is '
          'the only instrument that pays for the activity whose private return falls '
          'short of its social return. The vacancy subsidy pays for entry-level '
          'matches without paying for what those matches are supposed to produce, so '
          'it buys quantity where the distortion is smallest. The wage subsidy is '
          'actively counter-productive because it raises the price of the input whose '
          'complementary investment is under-supplied. And the technology tax raises '
          'the cost of an efficiently priced input in order to shift demand back '
          'towards labour that remains under-trained. The policy conclusion is not '
          'that more should be spent on youth employment but that the same money '
          'should be spent on a different margin.'),

    ('h2', '5.8. Robustness'),

    ('p', 'Two dimensions of robustness matter here. The first is the elasticity of '
          'substitution between the entry-level and the experienced task bundle, which '
          'is set outside the estimation. Table 9 reports the baseline, the shock '
          'response and the training wedge across values of ⟪\\sigma⟫ from '
          '' + n(SIG[0]["sigma"], 1) + ' to ' + n(SIG[-1]["sigma"], 1) + ', with '
          'the price of artificial intelligence re-targeted in each economy so that '
          'all of them start from the same estimated task share. The employment '
          'response to the shock is monotone in ⟪\\sigma⟫, as one would expect, while '
          'the wedge is generated by the contracting structure and moves far less.'),

    ('tabcap', '9', 'Sensitivity to the elasticity of substitution between the two task bundles.'),
    ('table', _t9_rows(), [1100, 2700, 2200, 2340, 1300]),
    ('notes', 'The price of artificial intelligence is re-targeted in each economy so that all of them start from the same estimated task share, and the same proportional price fall is then applied.'),

    ('p', 'The second is the eight parameters set outside the estimation, which are the '
          'ones most open to dispute. We draw ' + str(UNC["n_requested"]) + ' '
          'Latin-hypercube samples over plausible ranges for the discount rate, the '
          'exit rate, both separation rates, the poaching rate, the matching '
          'elasticity, the elasticity of substitution and the elasticity of promotion '
          'to mentoring, imposing the Hosios condition on every draw. Crucially, the '
          'model is re-estimated on every draw, so each economy in the sample '
          'reproduces the eight targeted moments exactly and differs only in what was '
          'not estimated. Of the draws, ' + str(UNC["n_solved"]) + ' re-estimated '
          'and solved and ' + str(UNC["n_ranked"]) + ' permitted the full policy '
          'comparison.'),

    ('figure', 'fig7_uncertainty.png', 7,
     'Robustness. Panel (a): the incidence of the shock between the entry wage and '
     'the entry-level employment rate as a function of the real rigidity of the entry '
     'wage. Panel (b): the distribution of the training wedge across Latin-hypercube '
     'draws over the externally set parameters, with the estimated value marked. '
     'Panel (c): the welfare gain of each instrument at a common budget across the '
     'same draws.'),

    ('p', 'The wedge is not an artefact of a particular parameterisation. Its mean '
          'across draws is ' + n(1 + UNC["wedge_mentoring_mean"], 1) + ' times the '
          'market level, with a fifth-to-ninety-fifth-percentile range of '
          '' + n(1 + UNC["wedge_mentoring_p5"], 1) + ' to '
          '' + n(1 + UNC["wedge_mentoring_p95"], 1) + ', and it is positive in '
          '' + pc(UNC["wedge_positive_share"], 0) + ' per cent of draws. Welfare at '
          'the optimum exceeds welfare at the market allocation by a mean of '
          '' + n(UNC["welfare_gap_mean"], 2) + ' per cent, with a range of '
          '' + n(UNC["welfare_gap_p5"], 2) + ' to '
          '' + n(UNC["welfare_gap_p95"], 2) + ' per cent. The instrument ranking is '
          'equally stable: the ' + LAB[BEST] + ' is the best of the four in '
          '' + pc(BEST_SHARE, 0) + ' per cent of draws, and the tax on '
          'artificial intelligence is infeasible at this budget in '
          '' + pc(1 - UNC['instrument_feasible_share']['gain_t_a'], 0) + ' per cent of them. What survives the sampling '
          'is not a point estimate of the wedge but its sign, its order of magnitude '
          'and the identity of the instrument that addresses it.'),

    # =====================================================================
    ('h1', '6. Discussion'),

    ('h2', '6.1. Why the Ladder Does Not Break'),

    ('p', 'The intuition that automating entry-level work must eventually starve the '
          'economy of experienced workers is a partial-equilibrium intuition. It '
          'treats training intensity per entrant as fixed and therefore reads a fall '
          'in entry-level hiring straight through into a fall in promotions. In '
          'general equilibrium training intensity is a choice, and it is a choice that '
          'moves in the opposite direction to hiring. When entrants become scarce, '
          'experienced time per entrant becomes abundant, the opportunity cost of '
          'mentoring falls, and the promotion option—untouched by a technology that '
          'cannot mentor—becomes a larger share of what an entry-level match is worth. '
          'The two effects nearly cancel at the aggregate level: in our estimated '
          'economy a doubling of the artificial-intelligence task share leaves the '
          'flow of promotions and the stock of experienced workers within '
          '' + alp(SH["d_ln_e_s"], 1) + ' per cent of where they started.'),

    ('p', 'This is a testable implication, and it is the sharpest one the paper '
          'offers. It predicts that firms in the most exposed occupations should '
          'shorten time to promotion and raise supervision intensity per junior hire '
          'even as they cut the number of junior hires. Linked employer–employee data '
          'with promotion records would settle it. If the prediction fails—if exposed '
          'firms cut hiring and mentoring together—then the joint product is more '
          'complementary than we have modelled it, and the pessimistic reading of the '
          'evidence would be the right one.'),

    ('h2', '6.2. Incidence Is Institutional, Not Technological'),

    ('p', 'The result that the pay-versus-employment split is governed by the wage '
          'rule rather than by the technology reframes a live empirical debate. '
          'Studies that find sizeable employment effects for young workers and studies '
          'that find precise nulls are often read as contradicting one another about '
          'what artificial intelligence does. Our model says they can both be right '
          'about their own settings and that the difference between them is '
          'informative in its own right: it is a measurement of how much of a shock '
          'entry wages are permitted to absorb. That reading suggests a research '
          'design—comparing the incidence of the same exposure measure across labour '
          'markets that differ in minimum-wage bite or in the compression of graduate '
          'pay—which would identify the wage rule from cross-country variation '
          'rather than assuming it, in the spirit of the cross-country work linking '
          'digitalisation to youth unemployment {{basol|ogbonna}}.'),

    ('p', 'It also carries an uncomfortable policy corollary. The institutions that '
          'protect the pay of young workers who are employed are the same institutions '
          'that concentrate the burden of a technology shock on those who are not yet '
          'employed. We do not read this as an argument for lower entry wages: the '
          'flexible-wage economy delivers the shock as a large pay cut to a cohort '
          'that is already at the bottom of the distribution, and our welfare '
          'accounting is not equipped to rank those two outcomes. We read it as a '
          'reason to attach the compensating instrument to the margin that the '
          'rigidity displaces, which is entry.'),

    ('h2', '6.3. Why the Standard Instruments Misfire'),

    ('p', 'Youth employment policy is built on the premise that the problem is the '
          'price or the availability of a young worker. In a model without a ladder '
          'that premise would be right and a wage or hiring subsidy would be the '
          'appropriate answer. The analysis here says that the binding problem is '
          'different in kind. An entry-level job is a production process with two '
          'outputs, and the market has a mechanism for pricing one of them and no '
          'mechanism for pricing the other. Subsidising the wage lowers the cost of an '
          'input to a process whose output is mispriced; it buys more of the process '
          'without correcting the mispricing, and in our estimates it does active harm '
          'by crowding out the under-provided investment. Paying directly for '
          'mentoring corrects the mispricing, which is why at equal cost it does an '
          'order of magnitude more work. The point generalises beyond artificial '
          'intelligence: any shock that shifts the balance between the two outputs of '
          'an entry-level job—offshoring of routine junior work, outsourcing of junior '
          'functions, the flattening of hierarchies—has the same implication for which '
          'instrument to reach for. It also cautions against reading improvements '
          'in the measured quality of the jobs that survive as evidence that the '
          'transition is benign {{gig1|broadband|wangguan2024}}, since the '
          'workers the model identifies as bearing the cost are those who never '
          'enter.'),

    ('h2', '6.4. Should Artificial Intelligence Be Taxed?'),

    ('p', 'Proposals to tax automation have intuitive appeal and a weak analytical '
          'foundation, and this model shows why. Artificial intelligence is hired '
          'until its marginal product equals its price, and the planner’s condition '
          'for the input is the same, so at any given allocation of labour there is no '
          'wedge in this market to correct. A tax reduces output and reduces the '
          'resources available for everything else, including for training the workers '
          'it is meant to protect. In our comparison it is the worst-performing '
          'instrument wherever it is feasible at all, and once the ladder subsidies '
          'are in place its optimal rate is zero to three decimal places. The correct '
          'reading of the shock is not that the technology should be slowed but that '
          'the institution it stresses—the mechanism by which an economy produces its '
          'next generation of experienced workers—was under-funded before the '
          'technology arrived and is more visibly under-funded now.'),

    ('p', 'This conclusion is conditional on the model’s scope, and the condition is '
          'worth stating. We assume artificial intelligence cannot mentor. If a future '
          'technology genuinely substitutes for the transmission of tacit know-how, '
          'the second component of the joint product is automatable too, the '
          'reproduction loop no longer requires entry-level jobs, and the case for '
          'subsidising them weakens rather than strengthens. Nothing in the current '
          'evidence suggests that point has been reached, but the model is explicit '
          'about where the argument would break.'),

    ('h2', '6.5. Implications for China'),

    ('p', 'Three features of the Chinese setting make the mechanism more acute rather '
          'than less. The cohort is large: 12.22 million graduates entered the labour '
          'market in 2025 and 12.7 million are expected in 2026, so the flow through '
          'the entry-level gate is enormous relative to the stock of experienced '
          'workers who must mentor them {{moe2026}}. Adoption is fast, which '
          'compresses into months an adjustment that elsewhere is spread over years '
          '{{nbs2026|digital_emp2}}. And entry wages are rigid, because provincial minimum wages '
          'bind for entry-level urban positions {{mayneris2018}}, which by Section 5.4 '
          'places China at the end of the range where the shock is borne almost '
          'entirely by access.'),

    ('p', 'The instruments in use are the ones this analysis ranks last: expanded '
          'public-sector and state-owned-enterprise recruitment quotas, one-off hiring '
          'and wage subsidies, and enlarged postgraduate places, all of which act on '
          'the quantity of entry-level positions or postpone entry, and none of which '
          'pays for mentoring. The model’s recommendation is specific and implementable '
          'within existing administrative machinery: convert part of the hiring '
          'subsidy into a credit conditional on documented supervision and on '
          'promotion outcomes, and make the existing employee-education deduction '
          'contingent on training entrants rather than on training in general. The '
          'general lesson is that youth employment policy should be evaluated by what '
          'it does to the flow of promotions, not by what it does to the stock of '
          'entry-level hires—a criterion that sits naturally alongside the '
          'common-prosperity agenda’s emphasis on the quality rather than the '
          'quantity of employment {{tong2026}}.'),

    ('h2', '6.6. Limitations'),

    ('p', 'Six limitations bound the claims. First, the analysis compares steady '
          'states. It is silent on transition dynamics, which matter here because the '
          'stock of experienced workers adjusts with a lag of several times the '
          'average time to promotion; the comparisons we report are the destination, '
          'not the path, and a cohort passing through the transition can be much worse '
          'off than either steady state. Second, the labour force and the flow of '
          'entrants are exogenous, so the model cannot represent discouragement, '
          'delayed entry into postgraduate study or withdrawal from the labour force, '
          'all of which are prominent in the Chinese data; the entry-level employment '
          'rate is the right outcome variable in this model but it maps only '
          'imperfectly on to measured youth employment. Third, the economy is '
          'representative-agent within each tier, so it cannot address heterogeneity '
          'by field of study, institution, gender or region {{mismatch2|pan2025}}. '
          'Fourth, poaching is a reduced-form flow: the poaching firm pays no '
          'recruiting cost, which is why the flow is a pure private loss; an explicit '
          'raiding market would attenuate the poaching wedge, though the hold-up '
          'wedge, the larger of the two, would remain. Fifth, the '
          'artificial-intelligence task share is the least well measured of the eight '
          'targets, which is why Section 5.2 reports a path rather than a point. '
          'Sixth, the model under-predicts observed enterprise training expenditure by '
          'an order of magnitude, as Section 4.3 records; if part of that gap reflects '
          'training margins the model omits rather than definitional differences, the '
          'estimated wedge is an upper bound.'),

    ('p', 'Three extensions follow naturally. Endogenous participation would let the '
          'model speak to discouragement and to the measured youth employment rate '
          'directly. Allowing artificial intelligence to substitute partially for '
          'mentoring, with an estimated rather than assumed degree of '
          'substitutability, would let the data speak to the condition under which the '
          'paper’s central conclusion reverses. And embedding the ladder in a '
          'multi-sector economy would allow entry-level tasks automated in one sector '
          'to reappear in another, which is the reinstatement margin the task-based '
          'literature has shown to be decisive over long horizons {{acemoglu2019}}.'),

    # =====================================================================
    ('h1', '7. Conclusions'),

    ('p', 'An entry-level job produces two things: output today and an experienced '
          'worker tomorrow. Artificial intelligence is good at the first and useless '
          'at the second, and the natural inference is that the career ladder is in '
          'danger. This paper formalised that inference in a two-tier search economy '
          'with endogenous mentoring, estimated it to reproduce eight Chinese '
          'labour-market moments exactly, validated it against an employment gradient '
          'it was never shown, and found the inference to be wrong in an instructive '
          'way.'),

    ('p', 'Four findings stand. The market provides about one '
          + ("seventh" if 6.5 < FOLD < 7.8 else n(FOLD, 1) + "th") + ' of the '
          'efficient amount of on-the-job training, so first promotion takes '
          '' + n(B["promo_years"], 1) + ' years rather than '
          '' + n(P_["promo_years"], 1) + ', even though the Hosios condition holds '
          'exactly; hold-up accounts for '
          '' + pc(WS["holdup_share"], 0) + ' per cent of the gap and poaching for '
          'the rest. Cheaper artificial intelligence is borne by entry-level access '
          'rather than entry-level pay, in a ratio of '
          '' + n(SH["incidence_ratio"], 1) + ' to one—but only because entry wages '
          'are rigid, and a flexible-wage economy would show the opposite. The ladder '
          'itself does not break: firms mentor a smaller intake '
          '' + lp(SH["d_ln_m"], 0) + ' per cent more intensively, promotions and the '
          'stock of experienced workers barely move, and the training wedge narrows '
          'rather than widens. And at a common budget the mentoring credit dominates '
          'the vacancy subsidy, the wage subsidy and the technology tax, on welfare, '
          'on the value of being a new entrant and on the marginal value of public '
          'funds, in the estimated economy and in '
          '' + pc(BEST_SHARE, 0) + ' per cent of draws over the parameters we did '
          'not estimate.'),

    ('p', 'The policy implication is uncomfortable for both sides of the current '
          'debate. It does not support slowing the technology: the optimal tax on '
          'artificial intelligence is zero once the ladder is priced correctly, and '
          'where the tax is feasible at all it is the worst instrument we examine. Nor '
          'does it support the reassurance that markets will handle the transition, '
          'because the margin under pressure is one the market has never priced '
          'properly and the burden falls on a cohort with no standing in the '
          'transaction. What it supports is paying explicitly for the thing that '
          'entry-level jobs were quietly producing all along. Economies have been '
          'getting their supply of experienced workers as a by-product of a '
          'transaction undertaken for other reasons. The by-product turns out to be '
          'more robust than we feared, and more under-supplied than we assumed.'),
]
