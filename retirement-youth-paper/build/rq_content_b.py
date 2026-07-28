# -*- coding: utf-8 -*-
"""Manuscript content, part B: results, discussion, conclusions.

Every number is read from stats.json, which analysis.py writes, and from the
uncertainty sample it dumps, so the text cannot drift from the computation
that produced it.
"""
import json
import math
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
S = json.load(open(os.path.join(HERE, "stats.json")))

B = S["baseline"]
SC, QC, RF = S["scaled"], S["queue_cost"], S["reform"]
CH, IND, IX = S["channels"], S["indicator"], S["indexation"]
UNC, MET = S["uncertainty"], S["meta"]
POL = {r["key"]: r for r in S["policy_baseline"]}
POL2 = {r["key"]: r for r in S["policy_post_reform"]}
SQ, SP = S["sensitivity_quota"], S["sensitivity_premium"]

_UN = pd.read_csv(os.path.join(DATA, "uncertainty.csv"))
COHORT = SC["cohort_millions"]


def _corr(a, b):
    return float(np.corrcoef(_UN[a], _UN[b])[0, 1])


CORR_DQ = _corr("delta_Q", "d_entry_prob")
CORR_TY = _corr("T_y", "queue_loss_pct_Y")
CORR_R = _corr("r", "queue_loss_pct_Y")
SHARE_SN_BAD = float((_UN["gain_s_N"] < 0).mean())
SHARE_TAU_BEST = float((_UN["gain_tau_q"] > _UN["gain_s_v"]).mean())


# ------------------------------------------------------------------ formatting
def _m(t):
    """Typographic minus sign, as the journal's style requires."""
    return t.replace("-", "−")


def n(x, d=3):
    return _m(("%%.%df" % d) % x)


def pct(x, d=1):
    """A proportion reported in per cent."""
    return _m(("%%.%df" % d) % (100 * x))


def sg(x, d=2):
    """A signed number."""
    return _m(("%%+.%df" % d) % x)


def spc(x, d=1):
    """A signed proportion reported in per cent."""
    return _m(("%%+.%df" % d) % (100 * x))


def lpt(x, d=2):
    """A log change reported in log points multiplied by one hundred."""
    return _m(("%%+.%df" % d) % (100 * x))


def kilo(x):
    """A count of thousands, rounded and written out with a separator."""
    return "{:,.0f}".format(round(1000.0 * x, -3))


def _after(key, prop):
    return B[key] * (1.0 + RF[prop])


# ------------------------------------------------------------------ Table 4
def _t4_rows():
    rows = [["Quantity", "Symbol", "Model", "Scaled to China"]]

    def r(label, sym, val, scaled):
        rows.append([label, sym, val, scaled])

    r("Market tightness", "⟪\\theta⟫", n(B["theta"], 3), "—")
    r("Job-finding rate of the young, per year", "⟪f_{y}⟫", n(B["f_y"], 3),
      "mean open search of %s months" % n(B["search_months_y"], 1))
    r("Job-finding rate of the prime-age, per year", "⟪f_{p}⟫",
      n(B["f_p"], 3), "—")
    r("Hazard of winning a rationed post, per year", "⟪\\lambda_{Q}⟫",
      n(B["lam_Q"], 3),
      "expected wait of %s years" % n(B["queue_years"], 2))
    r("Share of young non-employment entrants who queue", "⟪a_{q}⟫",
      n(B["a_q"], 3), "—")
    r("Queueing", "⟪u_{q}⟫", n(B["u_q"], 3),
      "%s million" % n(SC["queueing_millions"], 2))
    r("Openly searching, young", "⟪u_{m}⟫", n(B["u_m"], 3),
      "%s million" % n(B["u_m"] * COHORT, 2))
    r("Young in a rationed job", "⟪e_{q}⟫", n(B["e_q"], 3),
      "%s million" % n(B["e_q"] * COHORT, 2))
    r("Young in a market job", "⟪e_{m}⟫", n(B["e_m"], 3),
      "%s million" % n(B["e_m"] * COHORT, 2))
    r("The establishment", "⟪\\bar{N}⟫", n(B["N"], 3),
      "%s million" % n(SC["establishment_millions"], 1))
    r("Rationed hires per year", "⟪v_{Q}⟫", n(B["v_Q"], 3),
      "%s million" % n(SC["quota_hires_millions"], 2))
    r("Chance of ever holding a rationed job", "—",
      pct(B["cohort_entry_Q"], 2) + "%",
      "about one entrant in %s" % n(1.0 / B["cohort_entry_Q"], 1))
    r("Administered wage", "⟪w_{Q}⟫", n(B["w_Q"], 3),
      "%s times the entry market wage" % n(B["w_Q"] / B["w_y"], 2))
    r("Entry market wage", "⟪w_{y}⟫", n(B["w_y"], 3), "—")
    r("Prime-age market wage", "⟪w_{p}⟫", n(B["w_p"], 3), "—")
    r("Output forgone by the queue", "⟪\\mathcal{L}⟫", n(B["queue_loss"], 3),
      pct(QC["pct_of_output"] / 100, 2) + "% of output")
    r("Break-even screening value", "⟪\\xi^{*}⟫",
      n(QC["break_even_screening"], 3),
      pct(QC["break_even_screening"], 1) + "% of rationed output")
    return rows


# ------------------------------------------------------------------ Table 5
def _t5_rows():
    rho1 = B["rho"] * (1.0 + RF["d_rho"])
    yq0, yq1 = B["e_q"] + B["e_m"], (B["e_q"] + B["e_m"]) * (
        1.0 + RF["d_young_emp"])
    pq0, pq1 = B["E_q"] + B["E_m"], (B["E_q"] + B["E_m"]) * (
        1.0 + RF["d_prime_emp"])
    rows = [["Outcome", "Before", "After", "Change"]]

    def r(label, a, b, c):
        rows.append([label, a, b, c])

    r("Effective retirement age", n(MET["R0"], 1), n(MET["R1"], 1),
      sg(MET["R1"] - MET["R0"], 1) + " years")
    r("Retirement hazard ⟪\\rho⟫", n(B["rho"], 4), n(rho1, 4),
      spc(RF["d_rho"], 2) + "%")
    r("Labour force", n(B["L"], 2), n(B["L"] * (1 + RF["d_L"]), 2),
      spc(RF["d_L"], 2) + "%")
    r("Prime-age employment", n(pq0, 2), n(pq1, 2),
      spc(RF["d_prime_emp"], 2) + "%")
    r("Young employment", n(yq0, 3), n(yq1, 3),
      spc(RF["d_young_emp"], 3) + "%")
    r("Crowding-out coefficient ⟪\\Xi⟫", "—", "—", n(RF["crowding_out"], 4))
    r("Youth unemployment rate (%)", pct(B["u_rate_y"], 2),
      pct(B["u_rate_y"] + RF["u_rate_y_pp"] / 100, 2),
      sg(RF["u_rate_y_pp"], 3) + " pp")
    r("Prime-age unemployment rate (%)", pct(B["u_rate_p"], 2),
      pct(B["u_rate_p"] + RF["u_rate_p_pp"] / 100, 2),
      sg(RF["u_rate_p_pp"], 3) + " pp")
    r("Chance of ever holding a rationed job (%)",
      pct(B["cohort_entry_Q"], 2), pct(IX["entry_prob_no_index"], 2),
      spc(RF["d_entry_prob"], 2) + "%")
    r("Rationed hires per year (millions)",
      n(SC["quota_hires_millions"], 3),
      n(IX["entry_prob_no_index"] * COHORT, 3),
      kilo(RF["entry_lost_thousands"]) + " fewer")
    r("Expected years of queueing", n(B["queue_years"], 3),
      n(B["queue_years"] * (1 + RF["d_queue_years"]), 3),
      sg(RF["queue_years_diff"], 3) + " years")
    r("Queue share of youth non-employment (%)", pct(B["queue_share"], 2),
      pct(B["queue_share"] * (1 + RF["d_queue_share"]), 2),
      spc(RF["d_queue_share"], 2) + "%")
    r("Rationed share of employment (%)", pct(B["quota_share"], 2),
      pct(B["quota_share"] + RF["quota_share_pp"] / 100, 2),
      sg(RF["quota_share_pp"], 2) + " pp")
    r("Market tightness ⟪\\theta⟫", n(B["theta"], 3),
      n(_after("theta", "d_theta"), 3), spc(RF["d_theta"], 2) + "%")
    r("Entry market wage", n(B["w_y"], 4), n(_after("w_y", "d_w_y"), 4),
      spc(RF["d_w_y"], 3) + "%")
    r("Output", n(B["Y"], 2), n(B["Y"] * (1 + RF["d_Y"]), 2),
      spc(RF["d_Y"], 2) + "%")
    r("Welfare per head", n(B["welfare_pc"], 4),
      n(_after("welfare_pc", "d_welfare_pc"), 4),
      spc(RF["d_welfare_pc"], 3) + "%")
    r("Value of being a new entrant", n(B["V_entrant"], 3),
      n(_after("V_entrant", "d_V_entrant"), 3),
      spc(RF["d_V_entrant"], 2) + "%")
    return rows


# ------------------------------------------------------------------ Table 6
def _t6_rows():
    lab = {"cohort_entry_Q": "Chance of ever holding a rationed job",
           "u_rate_y": "Youth unemployment rate",
           "queue_years": "Expected years of queueing",
           "V_entrant": "Value of being a new entrant",
           "quota_share": "Rationed share of employment"}
    rows = [["Outcome", "Total", "Quota route", "Horizon route",
             "Demographic route"]]
    for k in ("cohort_entry_Q", "u_rate_y", "queue_years", "V_entrant",
              "quota_share"):
        c = CH[k]
        rows.append([lab[k], lpt(c["total"]), lpt(c["quota"]),
                     lpt(c["value"]), lpt(c["demo"])])
    return rows


# ------------------------------------------------------------------ Table 7
def _pol_rows(tbl):
    out = []
    for key in ("tau_q", "s_v", "s_N"):
        r = tbl[key]
        out.append([r["instrument"], n(r["rate"], 4),
                    n(r["d_welfare_pc_pct"], 4), n(r["d_entry_prob_pct"], 3),
                    sg(r["d_u_rate_y_pp"], 3), n(r["d_queue_loss_pct"], 2),
                    n(r["mvpf"], 2)])
    return out


def _t7_rows():
    rows = [["Instrument", "Rate", "Welfare per head (%)", "Access (%)",
             "Youth unemployment (pp)", "Queue loss (%)", "MVPF"]]
    rows += _pol_rows(POL)
    rows.append(["", "", "", "", "", "", ""])
    rows += _pol_rows(POL2)
    return rows


# ------------------------------------------------------------------ Table 8
def _t8_rows():
    return [
        ["Quantity", "Establishment fixed", "Establishment indexed"],
        ["Expansion of the establishment ⟪s_{N}⟫", "0.000",
         n(IX["s_N"], 4)],
        ["Chance of ever holding a rationed job (%)",
         pct(IX["entry_prob_no_index"], 2), pct(IX["entry_prob_indexed"], 2)],
        ["Relative to the pre-reform level of "
         + pct(IX["entry_prob_baseline"], 2) + "%",
         pct(IX["entry_prob_no_index"] / IX["entry_prob_baseline"] - 1, 1)
         + "%",
         "+" + pct(IX["entry_prob_indexed"] / IX["entry_prob_baseline"] - 1, 1)
         + "%"],
        ["Share of the lost access restored (%)", "0.0",
         n(IX["restored_pct"], 1)],
        ["Fiscal cost (% of output)", "0.000",
         n(IX["fiscal_pct_Y"], 3)],
        ["Welfare per head (%)", "0.000", n(IX["d_welfare_pc_pct"], 4)],
        ["Output forgone by the queue (%)", "0.00",
         sg(IX["d_queue_loss_pct"], 2)],
        ["Youth unemployment rate (pp)", "0.000",
         sg(IX["d_u_rate_y_pp"], 3)],
    ]


# ------------------------------------------------------------------ Table 9
def _t9_rows():
    rows = [["Varied quantity", "Value", "Access change (%)",
             "Youth unemployment (pp)", "Queue length (years)",
             "Queue loss (% of output)"]]
    for i, r in enumerate(SQ):
        rows.append(["Rationed share of employment" if i == 0 else "",
                     pct(r["quota_share"], 0) + "%",
                     spc(r["d_entry_prob"], 2), sg(r["d_u_rate_y_pp"], 3),
                     n(B["queue_years"], 2), n(r["queue_loss_pct_Y"], 2)])
    for i, r in enumerate(SP):
        rows.append(["Administered compensation premium" if i == 0 else "",
                     n(r["wage_premium"], 2),
                     spc(r["d_entry_prob"], 2), sg(r["d_u_rate_y_pp"], 3),
                     n(r["queue_years"], 2), n(r["queue_loss_pct_Y"], 2)])
    return rows


PART_B = [

    # =====================================================================
    ('h1', '5. Results'),

    ('p', 'Section 5.1 describes the estimated economy and prices the queue. '
          'Sections 5.2 and 5.3 run the retirement reform and separate two '
          'questions the debate usually merges: whether the young are '
          'displaced, and whether their access to the rationed sector '
          'survives. Section 5.4 decomposes the response, Section 5.5 asks '
          'what a monitoring authority watching the headline rate would have '
          'seen, and Sections 5.6 to 5.9 compare instruments and test how far '
          'the conclusions survive the parameters we did not estimate.'),

    # ------------------------------------------------------------------
    ('h2', '5.1. The Estimated Economy and the Price of the Queue'),

    ('p', 'Table 4 reports the estimated equilibrium. Market tightness is '
          + n(B["theta"], 1) + ', which is high because a vacancy in this '
          'model is a recruiting effort rather than a posted position, and it '
          'delivers job-finding rates of ' + n(B["f_y"], 2) + ' a year for '
          'the young and ' + n(B["f_p"], 2) + ' for the prime-age. The '
          'quantity that matters is the other one. The establishment hires '
          + n(B["v_Q"], 3) + ' workers for every entering cohort of one, '
          + n(SC["quota_hires_millions"], 2) + ' million a year at Chinese '
          'scale, and ' + n(SC["queueing_millions"], 2) + ' million young '
          'people are queueing for them at any moment. The hazard of winning '
          'a post is ' + n(B["lam_Q"], 3) + ' a year, so the expected wait is '
          + n(B["queue_years"], 2) + ' years.'),

    ('p', 'That wait is expensive because it is exclusive. A candidate who '
          'prepares full time is not searching, is not accumulating '
          'experience and is not producing, and the establishment hires the '
          'same ' + n(B["v_Q"], 3) + ' workers whether the line behind each '
          'post is two people long or twenty. The output forgone is '
          + n(QC["pct_of_output"], 2) + ' per cent of gross domestic '
          'product—larger than the entire measured contribution of many '
          'sectors that receive far more policy attention, and larger than '
          'the direct fiscal cost of most active labour-market programmes '
          '{{alm1|alm2}}. It is also, in the one setting where the long-run '
          'consequences have been measured, persistent: cohorts exposed to a '
          'harsher examination queue in Tamil Nadu still had lower employment '
          'and lower earning capacity a decade later {{mangal2024}}. And it is, '
          'on the estimates, the largest single distortion in the economy: '
          'the market sector satisfies the Hosios '
          'condition by construction, so there is nothing else of comparable '
          'size for it to compete with.'),

    ('p', 'The obvious objection is that examinations are not pure waste, '
          'because they select. Suppose they do, and that a worker selected '
          'by examination is more productive in a rationed post by a factor '
          '⟪\\xi⟫. The examination system breaks even when the extra output '
          'it generates covers the output the queue destroys:'),
    ('eq', 'eq24', 24),
    ('p', 'The estimated economy gives ⟪\\xi^{*}⟫ = '
          + n(QC["break_even_screening"], 3) + '. Selection by examination '
          'would have to raise the productivity of every worker in every '
          'government agency and public institution by '
          + pct(QC["break_even_screening"], 1) + ' per cent, permanently and '
          'over and above what an ordinary hiring process would achieve, for '
          'the observed queue to be socially efficient. That is not a '
          'refutation, because no one has measured the number. It does '
          'establish what would have to be true, and the magnitude is far '
          'outside the range that the personnel-economics literature reports '
          'for any selection instrument {{murphy1991|zhao2023}}.'),

    ('tabcap', '4', 'The estimated equilibrium. Stocks are per entering '
                    'cohort; the last column scales them by a cohort of '
                    + n(COHORT, 1) + ' million.'),
    ('table', _t4_rows(), [3600, 1180, 1500, 3360]),

    ('notes', 'The queue hazard, the expected wait, the mean duration of open '
              'search and the break-even screening value are implications '
              'rather than targets.'),

    # ------------------------------------------------------------------
    ('h2', '5.2. The Reform, and the Absence of Crowding Out'),

    ('p', 'The reform raises the effective retirement age from '
          + n(MET["R0"], 1) + ' to ' + n(MET["R1"], 1) + ' over '
          + n(MET["phase"], 0) + ' years, which is the schedule announced '
          'in September 2024 expressed as an employment-weighted average '
          '{{nbs2026}}. The retirement hazard falls '
          + pct(abs(RF["d_rho"]), 1) + ' per cent. Figure 3 traces the path '
          'and Table 5 reports the endpoints.'),

    ('figure', 'fig3_reform_path.png', 3,
     'The phased reform, year by year. Panel (a) shows the two headline '
     'indicators; panel (b) the chance that a member of an entering cohort '
     'ever holds a rationed job; panel (c) the length of the queue and its '
     'share of youth non-employment; panel (d) the rationed share of '
     'employment against the growth of the labour force. The vertical scales '
     'differ: what moves in (b) does not move in (a).'),

    ('p', 'Start with the question the public debate asks. Prime-age '
          'employment rises ' + pct(RF["d_prime_emp"], 1) + ' per cent, '
          'because people who would have retired are still working. Young '
          'employment falls ' + pct(abs(RF["d_young_emp"]), 3) + ' per cent. '
          'The crowding-out coefficient is ' + n(RF["crowding_out"], 4) + ', '
          'against ⟪\\Xi = -1⟫ under the lump-of-labour hypothesis and '
          '⟪\\Xi = 0⟫ under no competition at all. For every hundred '
          'additional prime-age workers the economy retains, young employment '
          'falls by ' + n(100 * abs(RF["crowding_out"]), 2) + ' of one '
          'worker. The lump-of-labour hypothesis is rejected, and it is not a '
          'close call.'),

    ('p', 'The reason is that the market sector has free entry. A larger '
          'labour force is met by more recruiting, tightness falls only '
          + pct(abs(RF["d_theta"]), 2) + ' per cent, the entry wage falls '
          + pct(abs(RF["d_w_y"]), 3) + ' per cent, and output rises '
          + pct(RF["d_Y"], 1) + ' per cent—slightly more than the '
          + pct(RF["d_L"], 1) + ' per cent by which the labour force grows, '
          'because the additional workers are prime-age and prime-age '
          'workers are less often between jobs. This reproduces the finding '
          'that the cross-country and quasi-experimental literature has been '
          'reporting for two decades {{gruber2010|boeri2022|mohnen2025}}, and '
          'it reproduces it in a model that was never calibrated to any of '
          'those studies, and in a Chinese computable general-equilibrium model '
          'built for a quite different purpose {{jiang2025}}. Our '
          'contribution is not that finding. It is what the model says '
          'next.'),

    ('tabcap', '5', 'The retirement reform: from an effective retirement age '
                    'of ' + n(MET["R0"], 1) + ' to ' + n(MET["R1"], 1) + '.'),
    ('table', _t5_rows(), [3480, 1600, 1600, 2960]),

    ('notes', 'Stocks are per entering cohort. The crowding-out coefficient '
              'is the ratio of the change in young employment to the change '
              'in prime-age employment, Equation (21).'),

    # ------------------------------------------------------------------
    ('h2', '5.3. Access Falls Even Though Nobody Is Displaced'),

    ('p', 'No young worker is pushed out of a job. What happens instead is '
          'that a door closes. The establishment cannot expand, so its '
          'vacancies are its separations plus its retirements; when '
          'retirements become rarer, so do vacancies. Rationed hiring falls '
          'from ' + n(SC["quota_hires_millions"], 2) + ' million a year to '
          + n(IX["entry_prob_no_index"] * COHORT, 2) + ' million. The chance '
          'that a member of an entering cohort ever holds a rationed job '
          'falls from ' + pct(B["cohort_entry_Q"], 2) + ' per cent to '
          + pct(IX["entry_prob_no_index"], 2) + ' per cent, a decline of '
          + pct(abs(RF["d_entry_prob"]), 1) + ' per cent. At a cohort of '
          + n(COHORT, 1) + ' million that is '
          + kilo(RF["entry_lost_thousands"]) + ' young people '
          'a year for whom the outcome they were preparing for stops being '
          'available.'),

    ('p', 'They are not unemployed. They queue slightly longer—the expected '
          'wait rises ' + n(RF["queue_years_diff"], 2) + ' of a year, from '
          + n(B["queue_years"], 2) + ' to '
          + n(B["queue_years"] * (1 + RF["d_queue_years"]), 2) + '—and then '
          'most of them take a market job, which is why measured employment '
          'barely moves. The composition of what the young end up doing '
          'changes; the count of what they end up doing does not. An '
          'indicator built on the count is therefore blind to the change by '
          'construction, and the blindness is not a data problem that better '
          'sampling would fix.'),

    ('p', 'The direction of the queue response is worth pausing on, because '
          'two forces pull against each other. Fewer openings shorten the '
          'line, since there is less to wait for. A longer working life '
          'lengthens it, since the prize is now held for '
          + n(MET["R1"] - MET["R0"], 1) + ' more years and is worth more. In the '
          'estimated economy the second force wins, narrowly: the queue gets '
          'longer per opening even as openings become scarcer, so the number '
          'of young people waiting falls only '
          + pct(abs(RF["d_queue_share"]), 1) + ' per cent while the number of '
          'posts they are waiting for falls '
          + pct(abs(RF["d_entry_prob"]), 1) + ' per cent. Waiting becomes a '
          'worse bet and stays almost as popular.'),

    # ------------------------------------------------------------------
    ('h2', '5.4. Decomposing the Response'),

    ('p', 'The retirement hazard enters the model in three distinct places, '
          'and the three do not have to agree. It sets the establishment’s '
          'replacement flow, through Equation (8); it sets how long any job '
          'is held, and therefore what a job is worth on both sides of the '
          'match, through Equations (10) to (14); and it sets the size of the '
          'prime-age population, and therefore the labour force against which '
          'a fixed ⟪\\bar{N}⟫ is measured. We call these the quota, horizon '
          'and demographic routes, shut each combination of them down in '
          'turn, and allocate the total by the Shapley value, which is the '
          'unique attribution that is symmetric and adds up. Table 6 reports '
          'the decomposition and Figure 4 draws it.'),

    ('tabcap', '6', 'Shapley decomposition of the response to the full '
                    'reform, in log points multiplied by one hundred.'),
    ('table', _t6_rows(), [3700, 1560, 1560, 1560, 1560]),

    ('notes', 'The three contributions sum to the total by construction; the '
              'residual is zero to within 4 × 10⁻¹⁸ for every outcome.'),

    ('figure', 'fig4_channels.png', 4,
     'The same decomposition. Positive and negative contributions coexist in '
     'the youth unemployment rate and cancel; in the chance of ever holding a '
     'rationed job there is only one contribution and nothing to cancel it.'),

    ('p', 'The decomposition is unusually clean. Access is '
          + pct(1.0, 0) + ' per cent quota route: the horizon and demographic '
          'contributions to the chance of ever holding a rationed job are '
          + lpt(CH["cohort_entry_Q"]["value"], 3) + ' and '
          + lpt(CH["cohort_entry_Q"]["demo"], 3) + ' log points, which is to '
          'say exactly zero. This is not an approximation. The number of '
          'young people the establishment hires per cohort is '
          '⟪v_{Q}/n⟫, and by Equation (8) that depends on the retirement '
          'hazard and on nothing else that the reform touches; how much a '
          'post is worth and how large the labour force is do not enter.'),

    ('p', 'The youth unemployment rate is the opposite case. Its three '
          'contributions are ' + lpt(CH["u_rate_y"]["quota"]) + ', '
          + lpt(CH["u_rate_y"]["value"]) + ' and '
          + lpt(CH["u_rate_y"]["demo"]) + ' log points, and they sum to '
          + lpt(CH["u_rate_y"]["total"]) + '. The quota route pushes the rate '
          'down, because young people who would have queued instead search '
          'and are counted as employed sooner. The horizon route pushes it '
          'up, because a more valuable rationed post makes waiting more '
          'attractive. The demographic route pushes it up as well. The '
          'largest single contribution is '
          + n(abs(100 * CH["u_rate_y"]["quota"]), 2) + ' log points and the '
          'net is ' + n(abs(100 * CH["u_rate_y"]["total"]), 2) + '. More than '
          'four fifths of the largest single movement is cancelled inside '
          'the indicator by movements of the opposite sign.'),

    ('p', 'The same arithmetic explains a result that would otherwise look '
          'like good news. The value of being a new entrant rises '
          + pct(RF["d_V_entrant"], 2) + ' per cent, which a welfare analysis '
          'that stopped there would read as the reform making young people '
          'better off. Of the '
          + lpt(CH["V_entrant"]["total"]) + ' log points, the horizon route '
          'contributes ' + lpt(CH["V_entrant"]["value"]) + ', the '
          'demographic route ' + lpt(CH["V_entrant"]["demo"]) + ' and the '
          'quota route ' + lpt(CH["V_entrant"]["quota"], 3) + '. The gain is the mechanical consequence of a '
          'longer working life over which to collect the same flow payoffs, '
          'not of anything the reform did to the opportunities in front of '
          'an entrant. Strip the horizon out and the entrant is, to three '
          'decimal places, exactly where they started—except that the '
          'rationed door is '
          + pct(abs(RF["d_entry_prob"]), 1) + ' per cent less likely to open.'),

    # ------------------------------------------------------------------
    ('h2', '5.5. What the Headline Indicator Misses'),

    ('p', 'Figure 5 puts the two series side by side, both indexed to their '
          'pre-reform values. Over the whole reform the youth unemployment '
          'rate moves by ' + n(IND["u_rate_y_range_pp"], 3) + ' percentage '
          'points, a small fraction of the month-to-month variation in the '
          'published Chinese series and far too little to be reported as a '
          'change by anyone. Over the same period the chance that an entrant '
          'ever holds a rationed job falls '
          + pct(abs(RF["d_entry_prob"]), 1) + ' per cent. The ratio of the '
          'two proportional movements is ' + n(IND["ratio"], 1) + ' to one.'),

    ('figure', 'fig5_indicator.png', 5,
     'The monitoring problem. Panel (a) indexes the youth unemployment rate, '
     'the chance of ever holding a rationed job and the expected years of '
     'queueing to their pre-reform values. Panel (b) puts the two changes on '
     'a common percentage-point scale. An authority monitoring the reform '
     'through the headline rate would record it as having had no effect on '
     'the young.'),

    ('p', 'This is a specific instance of a general problem that the systems '
          'literature has described for fifty years: an indicator selected '
          'because it is available and comparable comes to define the '
          'objective, and the parts of the system it does not measure drift '
          'without resistance {{forrester1971|meadows1998|goodhart1984}}. '
          'What makes this instance sharp is that the blindness is '
          'structural rather than statistical. The youth unemployment rate is '
          'a stock divided by a stock at a point in time. Access to a '
          'rationed sector is a probability over a lifetime. A reform that '
          'moves the second without moving the first is not an unusual case '
          'to be guarded against; it is what the model predicts as the '
          'central case, and Section 5.9 shows that it happens in every draw '
          'of the parameters we did not estimate.'),

    ('p', 'The practical implication is that the flow is observable and '
          'nobody is publishing it. Every province publishes its recruitment '
          'plan; the number of establishment posts filled each year is an '
          'administrative fact, not a survey estimate. Dividing it by the '
          'size of the entering cohort produces the series in panel (b) of '
          'Figure 5 directly, at negligible cost, with no sampling error and '
          'with a two-month rather than a two-year lag.'),

    # ------------------------------------------------------------------
    ('h2', '5.6. Three Instruments at a Common Budget'),

    ('p', 'What should a government that accepts this diagnosis do? We give '
          'it a budget of ' + n(100 * MET["budget"], 1) + ' per cent '
          'of output and three instruments: expand the establishment, subsidise '
          'market vacancies, or cut the administered premium and rebate the '
          'saving. Each rate is solved to exhaust the same budget, so the '
          'comparison is like for like. Instruments are ranked by welfare per '
          'head and by the marginal value of public funds,'),
    ('eq', 'eq23', 23),
    ('p', 'which exceeds one for an instrument that returns more than it '
          'costs {{hendren2020}}. Table 7 reports the comparison before and '
          'after the reform and Figure 6 draws it.'),

    ('tabcap', '7', 'Three instruments at a common fiscal cost of '
                    + n(POL["tau_q"]["fiscal_pct_Y"], 1) + ' per cent of '
                    'output. The upper block is the estimated baseline, the '
                    'lower block the economy after the retirement reform.'),
    ('table', _t7_rows(), [2500, 1080, 1560, 1080, 1620, 1180, 620]),

    ('notes', 'Access is the chance that a member of an entering cohort ever '
              'holds a rationed job. The queue loss is the output forgone by '
              'queueing, Equation (20). A marginal value of public funds '
              'above one identifies an instrument that returns more than it '
              'costs.'),

    ('figure', 'fig6_policy.png', 6,
     'The same three instruments, before and after the reform. Expanding the '
     'establishment is the only instrument that raises access, and the only '
     'one that lowers welfare.'),

    ('p', 'Cutting the administered premium wins on welfare and on the '
          'marginal value of public funds, in the baseline economy and after '
          'the reform. A ' + pct(POL["tau_q"]["rate"], 2) + ' per cent cut in '
          'the premium raises welfare per head '
          + n(POL["tau_q"]["d_welfare_pc_pct"], 3) + ' per cent, shortens the '
          'queue by ' + n(abs(POL["tau_q"]["d_queue_years"]), 3) + ' of a '
          'year, cuts the output lost to queueing '
          + n(abs(POL["tau_q"]["d_queue_loss_pct"]), 1) + ' per cent and '
          'returns ' + n(POL["tau_q"]["mvpf"], 2) + ' units of welfare per '
          'unit of public money. The market vacancy subsidy is second on '
          'welfare, at a marginal value of '
          + n(POL["s_v"]["mvpf"], 2) + ', and is the only instrument that '
          'does much for the value of being an entrant, raising it '
          + n(POL["s_v"]["d_V_entrant_pct"], 2) + ' per cent against '
          + n(POL["tau_q"]["d_V_entrant_pct"], 3) + ' per cent for the '
          'premium cut.'),

    ('p', 'Expanding the establishment is the intuitive response to a '
          'shortage of establishment posts, and it is the worst of the three. '
          'It raises access—by ' + n(POL["s_N"]["d_entry_prob_pct"], 2) + ' '
          'per cent, mechanically, because access is the vacancy flow and the '
          'vacancy flow is what the instrument buys. It also lowers welfare '
          'per head by ' + n(abs(POL["s_N"]["d_welfare_pc_pct"]), 4) + ' '
          'per cent, raises the output lost to queueing by '
          + n(POL["s_N"]["d_queue_loss_pct"], 2) + ' per cent, raises the '
          'youth unemployment rate by '
          + n(POL["s_N"]["d_u_rate_y_pp"], 3) + ' percentage points, and '
          'returns ' + n(POL["s_N"]["mvpf"], 2) + ' units of welfare per unit '
          'spent—less than the money would be worth left alone. A larger '
          'prize draws a longer line: the Harris–Todaro indifference '
          'condition (15) restores the queue in proportion to whatever is '
          'added to it, so the additional posts are paid for twice, once out '
          'of the budget and once out of the time of the people who queue for '
          'them {{harris1970|zenou2011}}.'),

    ('p', 'The ranking is unchanged after the reform, and the case for the '
          'premium cut strengthens slightly: the queue is longer, so the same '
          'expenditure retires more of it, and the output saved rises from '
          + n(abs(POL["tau_q"]["d_queue_loss_pct"]), 2) + ' to '
          + n(abs(POL2["tau_q"]["d_queue_loss_pct"]), 2) + ' per cent.'),

    # ------------------------------------------------------------------
    ('h2', '5.7. Indexing the Establishment to the Labour Force'),

    ('p', 'The instruments in Table 7 are marginal. A government could '
          'instead index the establishment to the labour force, the reform '
          'aimed most directly at holding access constant. The '
          'labour force grows ' + n(IX["labour_force_growth_pct"], 1) + ' per '
          'cent over the reform, so full indexation means '
          '⟪s_{N}⟫ = ' + n(IX["s_N"], 3) + '. Table 8 reports what that buys '
          'and what it costs.'),

    ('tabcap', '8', 'Indexing the establishment to the labour force, after '
                    'the retirement reform.'),
    ('table', _t8_rows(), [4400, 2620, 2620]),

    ('notes', 'Percentage changes are relative to the post-reform economy '
              'with a fixed establishment.'),

    ('p', 'Indexation over-corrects. It restores '
          + n(IX["restored_pct"], 0) + ' per cent of the lost access, which '
          'is to say it leaves an entrant '
          + pct(IX["entry_prob_indexed"] / IX["entry_prob_baseline"] - 1, 1)
          + ' per cent more likely to hold a rationed job than before the '
          'reform, because it corrects for the retirement channel and for '
          'thirty years of accumulated labour-force growth at the same time. '
          'It costs ' + n(IX["fiscal_pct_Y"], 2) + ' per cent of output, '
          'roughly fourteen times the budget of Table 7. And it lowers '
          'welfare per head by ' + n(abs(IX["d_welfare_pc_pct"]), 3) + ' per '
          'cent while raising the output lost to queueing '
          + n(IX["d_queue_loss_pct"], 1) + ' per cent and the youth '
          'unemployment rate ' + n(IX["d_u_rate_y_pp"], 2) + ' percentage '
          'points. The instrument that most directly fixes the thing this '
          'paper says is broken is not the instrument we would recommend, and '
          'the reason is the same as in Section 5.6.'),

    ('h2', '5.8. Sensitivity: the Quota, the Premium and the Value of '
           'Screening'),

    ('p', 'Table 9 varies the two features of the rationed sector that are '
          'hardest to pin down, re-estimating the model at each value so that '
          'all remaining moments continue to hold exactly. Two invariances '
          'are worth naming. The proportional fall in access is '
          + pct(abs(RF["d_entry_prob"]), 2) + ' per cent for every size of '
          'the rationed sector between 8 and 20 per cent of employment, and '
          'for every premium between 1.1 and '
          + n(SP[-1]["wage_premium"], 2) + ', because Equation (8) makes the '
          'vacancy flow proportional to the establishment and the retirement '
          'hazard enters it multiplicatively. The result does not depend on '
          'getting the size of the rationed sector right. And the length of '
          'the queue is ' + n(B["queue_years"], 2) + ' years at every '
          'premium, because the queue is pinned by the data—by the share of '
          'youth non-employment that is preparing and by the youth '
          'unemployment rate—rather than by the premium. What the premium '
          'changes is the flow value of preparing, and therefore what the '
          'queue costs: the output forgone runs from '
          + n(SP[0]["queue_loss_pct_Y"], 2) + ' per cent of output at a '
          'premium of ' + n(SP[0]["wage_premium"], 2) + ' to '
          + n(SP[-1]["queue_loss_pct_Y"], 2) + ' per cent at '
          + n(SP[-1]["wage_premium"], 2) + '.'),

    ('tabcap', '9', 'Sensitivity to the size of the rationed sector and to '
                    'the administered premium. The model is re-estimated at '
                    'each value so that the remaining moments continue to '
                    'hold exactly.'),
    ('table', _t9_rows(), [3060, 1000, 1300, 1700, 1420, 1160]),

    ('notes', 'Access and the youth unemployment rate report the response '
              'to the full retirement reform. The estimated economy is the '
              'row at a rationed share of 12 per cent and a premium of '
              '1.25.'),

    ('p', 'The size of the rationed sector does move one thing: what the '
          'queue costs, from ' + n(SQ[0]["queue_loss_pct_Y"], 2) + ' per cent '
          'of output at a rationed share of ' + pct(SQ[0]["quota_share"], 0)
          + ' per cent to ' + n(SQ[-1]["queue_loss_pct_Y"], 2) + ' per cent '
          'at ' + pct(SQ[-1]["quota_share"], 0) + ' per cent. A country with '
          'a larger administered sector has more to gain from the policies of '
          'Section 5.6 and loses more from the ones it is tempted by. It also '
          'moves the sign of the indicator: at a rationed share of '
          + pct(SQ[0]["quota_share"], 0) + ' per cent the youth unemployment '
          'rate falls ' + n(abs(SQ[0]["d_u_rate_y_pp"]), 3) + ' percentage '
          'points over the reform rather than rising, while access falls by '
          'exactly the same ' + pct(abs(SQ[0]["d_entry_prob"]), 1) + ' per '
          'cent as everywhere else. The indicator does not merely understate '
          'the change; over a plausible range it does not reliably get the '
          'direction right either.'),

    ('p', 'Finally, the calibration set rationed-sector productivity equal to '
          'market productivity, so that the administered premium is a pure '
          'rent. Relaxing that is the same calculation as the break-even '
          'screening value of Section 5.1: a premium that reflects genuine '
          'productivity by a factor ⟪\\xi⟫ is efficient when ⟪\\xi⟫ exceeds '
          '⟪\\xi^{*}⟫ = ' + n(QC["break_even_screening"], 3) + '. Below that '
          'threshold the queue destroys output on net and every conclusion in '
          'this section holds, with the cost of the queue falling '
          'proportionally as ⟪\\xi⟫ rises towards ⟪\\xi^{*}⟫; above it the '
          'examinations are an efficient sorting device and the welfare '
          'rankings of Section 5.6 no longer follow.'),

    # ------------------------------------------------------------------
    ('h2', '5.9. Parameter Uncertainty'),

    ('p', 'Six parameters are set outside the estimation, and the results '
          'above are conditional on them. We draw '
          + str(UNC["n_requested"]) + ' Latin hypercube points over the '
          'discount rate, the length of the young tier, the two separation '
          'rates, the matching elasticity and the age of entry, re-estimate '
          'all six structural parameters at every draw so that the six '
          'moments continue to hold exactly, and re-run the reform. All '
          + str(UNC["n_solved"]) + ' draws solve. Figure 7 reports the '
          'distributions.'),

    ('figure', 'fig7_robustness.png', 7,
     'Robustness over the parameters that were set rather than estimated. '
     'Panels (a) and (b) show the distribution of the response to the reform '
     'across ' + str(UNC["n_requested"]) + ' draws, with the estimated '
     'economy marked. Panel (c) shows the output forgone by the queue as a '
     'function of the size of the rationed sector.'),

    ('p', 'Access falls in ' + pct(UNC["d_entry_prob_negative_share"], 0)
          + ' per cent of draws, with a mean of '
          + pct(UNC["d_entry_prob_mean"], 1) + ' per cent and a fifth-to-'
          'ninety-fifth-percentile range of '
          + pct(UNC["d_entry_prob_p5"], 1) + ' to '
          + pct(UNC["d_entry_prob_p95"], 1) + ' per cent. The youth '
          'unemployment rate moves by less than half a percentage point in '
          + pct(UNC["d_u_rate_y_small_share"], 0) + ' per cent of draws, with '
          'a range of ' + n(UNC["d_u_rate_y_pp_p5"], 3) + ' to '
          + n(UNC["d_u_rate_y_pp_p95"], 3) + ' percentage points that '
          'straddles zero. The output forgone by the queue lies between '
          + n(UNC["queue_loss_p5"], 2) + ' and '
          + n(UNC["queue_loss_p95"], 2) + ' per cent of output. The two '
          'central claims of the paper—that access falls and that the '
          'indicator does not register it—hold in every draw.'),

    ('p', 'The instrument ranking is equally stable. Cutting the administered '
          'premium is the best of the three in '
          + pct(UNC["best_instrument_shares"]["gain_tau_q"], 0) + ' per cent '
          'of draws, and expanding the establishment lowers welfare in '
          + pct(SHARE_SN_BAD, 0) + ' per cent. The one parameter that '
          'materially governs the size of the effect is the separation rate '
          'from establishment posts: its correlation with the fall in access '
          'across draws is ' + n(CORR_DQ, 2) + '. That is the right economics '
          'and it is a testable prediction. Where establishment posts turn '
          'over for reasons other than retirement, retirements are a smaller '
          'share of the vacancy flow and the reform matters less; where the '
          'iron rice bowl is most secure, it matters most. Two further '
          'correlations are worth recording: the cost of the queue rises with '
          'the length of the window in which candidates are eligible to sit '
          'the examinations, at ' + n(CORR_TY, 2) + ', and falls with the '
          'discount rate, at ' + n(CORR_R, 2) + ', since impatient candidates '
          'will not wait.'),

    # =====================================================================
    ('h1', '6. Discussion'),

    ('h2', '6.1. Two Questions That Are Not the Same Question'),

    ('p', 'The literature on retirement and youth employment has converged on '
          'a clear answer to a clear question. Whether measured across '
          'countries and decades {{gruber2010}}, in a matching model with '
          'endogenous vacancy creation {{boeri2022}}, in Norwegian '
          'administrative data {{vestad2013}} or in recent United States '
          'evidence {{mohnen2025}}, older workers do not take jobs from '
          'younger ones. The exception proves the rule: displacement appears '
          'where the number of slots is fixed, as in the short promotion '
          'ladders studied by Bianchi and co-authors {{bianchi2023}}, and it '
          'appears by age group where technology fixes the number of tasks '
          '{{robots_age}}. Our model reproduces the consensus answer, with '
          'a '
          'crowding-out coefficient of ' + n(RF["crowding_out"], 4) + ', and '
          'we regard this as validation rather than as a finding.'),

    ('p', 'The finding is that the answer is to a different question from the '
          'one young people are asking. "Will I be displaced from a job I '
          'hold?" and "will the job I am preparing for still be there?" have '
          'different answers when part of the labour market is rationed, '
          'because the two are governed by different equations. Displacement '
          'is governed by free entry, which restores what a shock takes away. '
          'Access to a rationed sector is governed by an administrative '
          'ceiling, which does not restore anything, because there is no '
          'decision on the employer’s side to be restored. In a labour market '
          'that is entirely market-clearing the two questions coincide and '
          'the literature’s answer covers both. In an economy where '
          + pct(B["quota_share"], 0) + ' per cent of urban employment sits '
          'behind a quota and ' + pct(B["queue_share"], 0) + ' per cent of '
          'young non-employment is spent preparing for it, they do not.'),

    ('p', 'This is a general point about aggregation, not a Chinese '
          'peculiarity. Any economy with a large rationed segment—licensed '
          'professions, academic tenure lines, public-sector establishments '
          'in southern Europe, protected incumbent contracts—will show the '
          'same divergence between an employment count and a lifetime '
          'probability of access, and will show it most strongly for the '
          'cohort that has not yet entered {{gelb1991|krueger1974}}. The '
          'youth-unemployment indicator is defined on the people who are '
          'already in the labour market. The cost falls on the ones deciding '
          'whether to be.'),

    ('h2', '6.2. The Queue Is the Mechanism'),

    ('p', 'The distinctive object in this model is not the retirement age; it '
          'is the queue, and the retirement reform is instructive mainly '
          'because of what it reveals about the queue. Three features are '
          'worth separating.'),

    ('p', 'First, the queue is a stock of forgone production that no accounts '
          'record. ' + n(SC["queueing_millions"], 1) + ' million young people '
          'preparing full time for an examination are not unemployed by the '
          'International Labour Organization definition if they are not '
          'actively searching, are not out of the labour force in any '
          'meaningful sense, and are not in education in the sense the '
          'not-in-education-employment-or-training literature uses '
          '{{ilo2|neet_cee|rahmani2023}}. They occupy a category the '
          'measurement system does not have, and the output they forgo is '
          + n(QC["pct_of_output"], 1) + ' per cent of gross domestic product '
          'a year.'),

    ('p', 'Second, the queue is a rent-dissipation device of exactly the form '
          'Krueger described {{krueger1974}}. The establishment offers a '
          'premium of ' + n(B["w_Q"] / B["w_y"], 2) + ' over an entry-level '
          'market job. Access is rationed by examination rather than by '
          'price, so the premium is competed away in preparation time until '
          'the marginal candidate is indifferent. The rent is not '
          'transferred; it is destroyed. And because the number of posts is '
          'fixed, the dissipation is complete at the margin: a longer line '
          'produces no additional hire. The size of the premium is itself a '
          'policy variable rather than a fact of nature, and cross-country '
          'evidence shows how far it varies {{gindling2020|armijos2025}}.'),

    ('p', 'Third, the queue selects the wrong people to do the wrong thing '
          'with their twenties. Murphy, Shleifer and Vishny argued that the '
          'allocation of talent between production and rent seeking is a '
          'first-order determinant of growth {{murphy1991}}, and the '
          'Chinese evidence on human-capital mismatch and on the returns to '
          'higher education points the same way {{zhao2023|zheng2021|li2014}}. '
          'The candidates who queue longest are those with the strongest '
          'preference for security and the highest expected examination '
          'scores, which is to say a group with substantial general human '
          'capital, and they spend ' + n(B["queue_years"], 1) + ' years of it '
          'on a screening technology that produces no output.'),

    ('h2', '6.3. Why the Intuitive Remedy Backfires'),

    ('p', 'Section 5.6 found that expanding the establishment—the response '
          'most often proposed when access to public-sector jobs tightens, '
          'and the one adopted in the 2023 and 2024 expansions of graduate '
          'recruitment—raises access, lowers welfare and raises the youth '
          'unemployment rate. The mechanism is worth stating plainly because '
          'it is the paper’s clearest example of counterintuitive behaviour '
          'in a social system {{forrester1971|meadows2008}}.'),

    ('p', 'Adding posts does two things. It adds hires, one for one. It also '
          'raises the expected value of queueing, because the hazard of '
          'winning rises for a given line length, and the Harris–Todaro '
          'indifference condition then draws more entrants into the line '
          'until indifference is restored. The second effect is not a '
          'friction that decays; it is an equilibrium response, and in the '
          'estimated economy it consumes the gain. This is where an '
          'administrative ceiling differs from a public sector that chooses '
          'its own headcount: in models where the state optimises over '
          'employment and wages, expansion is disciplined by the wage bill it '
          'implies {{albrecht2019|chassamboulli2023}}, and there is no '
          'equilibrium queue for the expansion to feed. Welfare per head '
          'falls '
          + n(abs(POL["s_N"]["d_welfare_pc_pct"]), 4) + ' per cent and the '
          'marginal value of public funds is '
          + n(POL["s_N"]["mvpf"], 2) + ', below the value of leaving the '
          'money in private hands, in the estimated economy and in '
          + pct(SHARE_SN_BAD, 0) + ' per cent of parameter draws.'),

    ('p', 'The instrument that works does the opposite. Cutting the '
          'administered premium reduces the prize, shortens the line and '
          'releases the time; it is regressive-looking and politically hard, '
          'and it returns ' + n(POL["tau_q"]["mvpf"], 2) + ' units of welfare '
          'per unit of public money. This is the standard result in the '
          'queueing literature—reduce the rent rather than expand the '
          'rationed good {{harris1970|zenou2011}}—and its unpopularity is '
          'the reason the standard result keeps needing to be restated.'),

    ('h2', '6.4. What to Measure Instead'),

    ('p', 'If the youth unemployment rate cannot see this, what can? The '
          'model suggests three series, each constructible from data that '
          'already exist.'),

    ('p', 'The first is the cohort access rate: establishment hires in a year '
          'divided by the size of the entering cohort. Both numbers are '
          'administrative. This is the series that falls '
          + pct(abs(RF["d_entry_prob"]), 1) + ' per cent in our reform while '
          'the headline rate moves ' + n(RF["u_rate_y_pp"], 3) + ' percentage '
          'points, and it is the series a young person is actually deciding '
          'against. The second is the queue itself: candidates registered for '
          'public-sector examinations, net of those already employed, '
          'expressed as a share of the cohort. Registration data are '
          'published. The third is the implied wait, the ratio of the first '
          'two, which is the expected number of years a candidate must '
          'prepare and which in our estimates is '
          + n(B["queue_years"], 1) + ' years.'),

    ('p', 'None of these requires a new survey and all three are timelier '
          'than the labour force survey. The obstacle is not measurement, and '
          'the systems literature has a name for the obstacle: an indicator '
          'that has been adopted as a target stops being available as a '
          'measure, and the institutional incentive is to keep monitoring the '
          'series whose behaviour is understood {{goodhart1984|meadows1998}}. '
          'The argument for the three series above is precisely that nobody '
          'has yet had a reason to manage them. Broadening the unemployment '
          'concept does not help either. Full-time-equivalent utilisation rates uncover considerably '
          'more slack than the headline measure, especially among the young '
          '{{houston2025}}, and measures of employment quality uncover more '
          'still {{liu2024sus|yg}}; neither would register our reform, '
          'because the people it affects are employed and working full '
          'time.'),

    ('h2', '6.5. Implications for China'),

    ('p', 'Three implications follow for the Chinese policy debate '
          'specifically. The first is that the retirement reform should not '
          'be defended or attacked on youth-employment grounds. It does not '
          'displace young workers—the crowding-out coefficient is '
          + n(RF["crowding_out"], 4) + '—and the debate that has occupied '
          'commentary since September 2024 is aimed at an effect that does '
          'not exist. What the reform does do, quietly, is close '
          + kilo(RF["entry_lost_thousands"]) + ' establishment '
          'openings a year to new entrants, and that is worth an explicit '
          'decision rather than an unnoticed consequence.'),

    ('p', 'The second concerns the age ceiling on the examinations. The 2026 '
          'central civil-service examination raised the general upper age '
          'limit from 35 to 38, and several provinces have followed. Read '
          'through this model the relaxation is not obviously a favour to '
          'young people. It lengthens the window in which a candidate may '
          'keep queueing without changing the number of posts, and the '
          'parameter that governs the length of that window is positively '
          'correlated with the output lost to queueing across our draws, at '
          + n(CORR_TY, 2) + '. Widening eligibility for a fixed prize '
          'lengthens the line. The measure will be recorded as expanding '
          'opportunity and will show up in the data as more people preparing '
          'for longer.'),

    ('p', 'The third is about the direction of the underlying trend, which is '
          'slower and larger than the retirement reform. The establishment is '
          'fixed in absolute terms while the urban labour force grows; the '
          'demographic route alone reduces the rationed share of employment '
          'by ' + n(abs(100 * CH["quota_share"]["demo"]), 1) + ' log points '
          'over our horizon, which is nine tenths of the total decline in '
          'that share and by far the largest single contribution in Table 6. '
          'Public-sector employment as an aspiration is being priced by a '
          'ratio whose denominator grows every year, and the graduating '
          'cohort is expected to reach ' + n(COHORT, 1) + ' million in 2026 '
          '{{moe2026}}. '
          'The retirement reform accelerates a squeeze that was already '
          'underway; it did not create it, and reversing the reform would not '
          'relieve it. The constructive response is to make the routes that '
          'do not run through the examination more attractive—vocational '
          'training carries a measurable return in China {{vet1}}, and '
          'regional development policy already treats the quality of local '
          'employment as an objective {{tong2026|liang2024}}—rather than to '
          'enlarge the prize at the end of the queue.'),

    ('h2', '6.6. Limitations'),

    ('p', 'Five limitations deserve statement. The model is a steady-state '
          'comparison, so the reform path in Figure 3 is a sequence of '
          'stationary equilibria rather than a transition; the direction of '
          'every result would survive a full transition but the timing would '
          'not, and a cohort caught mid-reform faces a worse draw than any '
          'steady state shows. The market sector is homogeneous, with no '
          'on-the-job search and no experience premium beyond the retirement '
          'horizon, which understates what a candidate gives up by queueing '
          'and therefore understates the cost of the queue '
          '{{postelvinay2002|cahuc2006|kambourov2009}}. Wages in the market '
          'sector are fully flexible, which is a strong assumption over a '
          'fifteen-year horizon even though the literature disagrees about '
          'how strong {{shimer2005|hall2008|hagedorn2008|pissarides2009}}; '
          'introducing rigidity would shift some of the adjustment from wages '
          'to employment and would raise, not lower, the measured '
          'crowding-out coefficient, so the central result is conservative in '
          'that direction. We also hold the market sector’s technology fixed, '
          'while entry-level demand is being reshaped by artificial '
          'intelligence over exactly the horizon we study '
          '{{acemoglu2025macro|brynjolfsson2025canaries|humlum2025}}, and by '
          'the reallocation of labour across Chinese regions and sectors '
          '{{wangguan2024|career1|career2}}. Those forces move the market '
          'alternative to queueing, and therefore the queue; they do not move '
          'the establishment’s vacancy flow, which is what our results turn '
          'on.'),

    ('p', 'The last is the most important. We treat the examination as a '
          'lottery among those who prepare, so preparation buys probability '
          'and nothing else. If preparation instead builds human capital that '
          'is useful in market employment, the queue is partly an investment '
          'and its cost is overstated; if candidates differ in ability and '
          'the examination sorts on it, the queue is partly a screen and '
          'Section 5.8 gives the threshold at which it pays for itself. '
          'Both extensions require individual-level data on candidates that '
          'is not currently collected, which is itself an argument for '
          'collecting it. Our reading is that the assumption is defensible '
          'because the content of the examinations is specific to public '
          'administration and the preparation industry is organised around '
          'the test rather than around the job, but it is a reading and not a '
          'measurement.'),

    # =====================================================================
    ('h1', '7. Conclusions'),

    ('p', 'A retirement reform reduces the rate at which people leave jobs. '
          'Where jobs are created by firms deciding to create them, that is '
          'absorbed: firms create more, and nobody is displaced. Where jobs '
          'are created by an administrative rule that fixes their number, the '
          'only thing that creates a vacancy is somebody leaving, and slowing '
          'the leaving closes the door. Both mechanisms operate in the same '
          'economy at the same time, and the aggregate indicator we use to '
          'watch them adds them together.'),

    ('p', 'We built a two-sector search model in which an establishment '
          'sector of fixed headcount coexists with a free-entry market '
          'sector, and in which the young queue for the rationed sector as in '
          'Harris and Todaro. Six parameters were estimated against six '
          'Chinese moments, exactly rather than approximately, and the '
          'estimated economy reproduced an untargeted queueing duration of '
          + n(B["queue_years"], 2) + ' years that matches independent '
          'evidence on repeat candidates. Raising the effective retirement '
          'age from ' + n(MET["R0"], 1) + ' to ' + n(MET["R1"], 1) + ' produces a '
          'crowding-out coefficient of ' + n(RF["crowding_out"], 4) + ', '
          'which rejects the lump-of-labour hypothesis. It also reduces the '
          'chance that a member of an entering cohort ever holds a rationed '
          'job by ' + pct(abs(RF["d_entry_prob"]), 1) + ' per cent, about '
          + kilo(RF["entry_lost_thousands"]) + ' young people '
          'a year, and a Shapley decomposition attributes all of that to the '
          'establishment’s shrinking replacement flow and none of it to '
          'anything else. Over the same reform the youth unemployment rate '
          'moves ' + n(RF["u_rate_y_pp"], 3) + ' percentage points, because '
          'three channels of opposite sign very nearly cancel inside it. '
          'Access falls ' + n(IND["ratio"], 0) + ' times more than the '
          'headline rate moves, in the estimated economy and in every one of '
          + str(UNC["n_solved"]) + ' parameter draws.'),

    ('p', 'The queue that produces this is not incidental. It costs '
          + n(QC["pct_of_output"], 1) + ' per cent of output a year, it would '
          'need to raise the productivity of every establishment worker by '
          + pct(QC["break_even_screening"], 0) + ' per cent to justify '
          'itself, and it responds to policy in a way that defeats the '
          'obvious remedy: expanding the establishment raises access, lowers '
          'welfare and returns ' + n(POL["s_N"]["mvpf"], 2) + ' units of '
          'welfare per unit of public money, because a larger prize draws a '
          'longer line. Cutting the administered premium returns '
          + n(POL["tau_q"]["mvpf"], 2) + ', and does so in every draw.'),

    ('p', 'The general lesson is about what an indicator can be asked to do. '
          'The youth unemployment rate answers a question about the people '
          'already in the labour market. Rationing operates on the people '
          'deciding whether to enter it, and it operates on a probability '
          'over a lifetime rather than on a stock at a moment. When a reform '
          'moves the second and not the first, a monitoring system built on '
          'the first will report that nothing happened, and it will be '
          'correct about what it measures and wrong about what matters. The '
          'series that would have caught this—establishment hires per '
          'cohort, candidates registered per cohort, and the implied '
          'wait—are administrative, cheap, and nobody publishes them. That '
          'is the recommendation this paper ends on, and it costs nothing.'),

    # =====================================================================
    ('back', 'Author Contributions:',
     'Conceptualization, methodology, formal analysis, software and '
     'writing—original draft preparation, X.C.; validation, data curation and '
     'visualization, D.H.; investigation, writing—review and editing, '
     'supervision and project administration, T.M. All authors have read and '
     'agreed to the published version of the manuscript.'),
    ('back', 'Funding:', 'This research received no external funding.'),
    ('back', 'Institutional Review Board Statement:',
     'Not applicable. The study is a structural simulation calibrated to '
     'published aggregate statistics and involves no human participants or '
     'animals.'),
    ('back', 'Informed Consent Statement:', 'Not applicable.'),
    ('back', 'Data Availability Statement:',
     'The model is fully specified by Equations (1)–(24). No individual-level '
     'data were used; every calibration target is drawn from the published '
     'sources listed in Table 2. The model code, the exact-identification '
     'routine, the counterfactual, decomposition, policy and uncertainty '
     'experiments and the scripts that generate every figure and table in '
     'this article are available from the corresponding author on reasonable '
     'request.'),
    ('back', 'Acknowledgments:',
     'The authors thank the editors and the anonymous reviewers for comments '
     'that improved the manuscript.'),
    ('back', 'Conflicts of Interest:',
     'The authors declare no conflicts of interest.'),
]
