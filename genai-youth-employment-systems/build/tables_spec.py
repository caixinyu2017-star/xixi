# -*- coding: utf-8 -*-
"""Table and figure specifications.

Numeric content is read from the simulation output written by
model/experiments.py, so the manuscript cannot drift away from the model.

A table body is a list of ("row", [cells...]) and ("sec", "label") items.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))


def _read(name):
    rows = [l.rstrip("\n").split("\t")
            for l in open(os.path.join(TAB, name), encoding="utf-8")]
    return rows[0], rows[1:]


MINUS = "\u2212"


def num(v, d=None):
    """Format a number with the typographic minus sign used by the journal."""
    t = v if d is None else ("%%.%df" % d) % float(v)
    t = t.strip()
    if t in ("-0", "-0.0", "-0.00", "-0.000"):
        t = t[1:]
    return t.replace("-", MINUS) if t[:1] == "-" else t


SYM = [("alpha_max", "α_{max}"), ("rho_max", "ρ_{max}"), ("delta_K", "δ_{K}"),
       ("delta_S", "δ_{S}"), ("beta_J", "β_{J}"), ("beta_S", "β_{S}"),
       ("tau_dev", "τ_{dev}"), ("chi_S", "χ_{S}"), ("zeta_0", "ζ_{0}"),
       ("q_0", "q_{0}"), ("lambda", "λ"), ("epsilon", "ε"), ("omega", "ω"),
       ("eta", "η"), ("nu", "ν"), ("Delta t", "Δt"), ("rho(t)", "ρ(t)"), ("g_Y", "g_{Y}"),
       ("exp(-δ_{S} T)", "exp(−δ_{S}T)"), ("m -> 0", "m → 0"),
       ("(-41.2%)", "(−41.2%)"), ("7.1e-15", "7.1 × 10⁻¹⁵"),
       ("0.0e+00", "0"), ("2.4e-07", "2.4 × 10⁻⁷"),
       ("(Table 4)", "(Table 3)")]


def sym(text):
    for a, b in SYM:
        text = text.replace(a, b)
    return text


def R(*cells):
    return ("row", list(cells))


def S(label):
    return ("sec", label)


# ---------------------------------------------------------------------------
def table1():
    rows = [
        S("Stocks"),
        R("J", "Early-career (junior) staff", "persons"),
        R("S", "Experienced (senior) staff", "persons"),
        R("A", "Generative-AI capability", "index (0–1)"),
        R("K", "Human–AI collaboration routines", "index"),
        R("Y_{d}", "Planned output", "output units yr⁻¹"),
        R("Ĉ", "Perceived unit cost", "cost per output unit"),
        S("Flows"),
        R("h", "Entry hiring rate", "persons yr⁻¹"),
        R("c", "Promotion flow from junior to senior", "persons yr⁻¹"),
        R("e_{S}", "External recruitment of senior staff",
          "persons yr⁻¹"),
        R("ℓ", "Learning-by-collaborating inflow", "index yr⁻¹"),
        S("Auxiliary variables"),
        R("F", "External generative-AI frontier", "index (0–1)"),
        R("u", "AI utilisation intensity", "share"),
        R("Λ", "Absorptive-capacity multiplier", "share"),
        R("α", "Automated share of entry tasks", "share"),
        R("ρ", "Core tasks reinstated to AI-assisted juniors", "share"),
        R("π_{J}, π_{S}", "Effective productivity, junior and senior",
          "output person⁻¹ yr⁻¹"),
        R("i_{J}, i_{S}",
          "Task intensity per unit of output, junior and senior",
          "dimensionless"),
        R("D_{J}, D_{S}", "Desired junior and senior labour", "persons"),
        R("q", "Mentoring adequacy per junior", "dimensionless"),
        R("ψ", "Fraction of juniors reaching competence", "share"),
        R("x", "Experiential-quality index of junior work",
          "index (1 at t = 0)"),
        R("Ω", "External availability index for senior staff",
          "index (1 at t = 0)"),
        R("Φ", "Output fulfilment ratio", "share"),
        R("Y", "Delivered output", "output units yr⁻¹"),
        R("C", "Unit cost", "cost per output unit"),
        R("E", "Net entry-port elasticity, Equation (19)", "dimensionless"),
    ]
    return dict(number=1, caption="Model variables.",
                header=["Symbol", "Variable", "Unit"], rows=rows,
                widths=[0.15, 0.60, 0.25], note=None, italic_col=0,
                wide=False, align="lll")


# ---------------------------------------------------------------------------
def table2():
    rows = [
        S("Task structure"),
        R("θ_{E}", "Share of entry (codified, routine-cognitive) tasks",
          "0.30", "Occupational-exposure evidence"),
        R("θ_{C}", "Share of core (intermediate) tasks", "0.45",
          "Occupational-exposure evidence"),
        R("θ_{G}", "Share of judgement (senior-only) tasks", "0.25",
          "Residual"),
        S("Technical design and diffusion"),
        R("α_{max}", "Automation ceiling for entry tasks", "0.60",
          "Design parameter; varied in Figure 5a"),
        R("ρ_{max}", "Reinstatement ceiling for core tasks", "0.35",
          "Design parameter; varied in Figure 5"),
        R("a_{α}, γ",
          "Half-saturation and exponent of the automation sigmoid",
          "0.50, 2.0", "Assumption"),
        R("F_{max}, g_{F}, t_{F}",
          "Ceiling, growth rate and inflection of the external frontier",
          "1.00, 1.00, 1.285", "Inflection calibrated (Table 3)"),
        R("ν, δ_{A}, φ_{0}",
          "Adoption rate, capability depreciation, absorptive-capacity floor",
          "1.328, 0.05, 0.25", "Adoption rate calibrated (Table 3)"),
        R("u_{max}, a_{u}",
          "Ceiling and half-saturation of AI utilisation", "0.85, 0.215",
          "Half-saturation calibrated (Table 3)"),
        S("Augmentation and learning"),
        R("β_{J}, β_{S}", "AI productivity elasticity, junior and senior",
          "0.739, 0.246", "Calibrated (Table 3)"),
        R("λ, δ_{K}",
          "Learning investment rate and routine obsolescence rate",
          "0.30, 0.20 yr⁻¹", "Assumption; varied in Figure 5b"),
        R("k_{h}", "Half-saturation of the routine stock", "1.00",
          "Assumption"),
        R("ζ_{0}", "Skill-formation value of AI-mediated work", "0.25",
          "Qualitative evidence on shadow learning"),
        S("Development pipeline"),
        R("τ_{dev}", "Time to competence", "3.0 yr",
          "Professional-service convention"),
        R("m, q_{0}",
          "Mentoring capacity per senior; half-saturation of mentoring adequacy",
          "0.369, 1.00", "m derived from the steady state"),
        R("η", "AI knowledge-scaffolding coefficient", "0.35", "Assumption"),
        R("δ_{J}, δ_{S}", "Junior and senior separation rates",
          "0.15, 0.08 yr⁻¹", "Professional-service convention"),
        R("τ_{J}, τ_{S}", "Hiring and recruitment adjustment times",
          "1.0, 2.0 yr", "Assumption"),
        R("χ_{S}, ω, Ω_{max}",
          "External recruitment ceiling, availability elasticity and its cap",
          "0.03 yr⁻¹, 1.00, 2.00", "Sector-consistent closure"),
        S("Production, cost and demand"),
        R("π_{J0}, π_{S0}", "Baseline productivities",
          "1.00, 1.60", "Normalisation"),
        R("w_{J}, w_{S}", "Relative compensation", "1.00, 2.00",
          "Normalisation"),
        R("p_{A}, p_{K}",
          "AI operating cost and learning investment cost", "0.05, 0.15",
          "Assumption"),
        R("ε, τ_{Y}, τ_{C}",
          "Demand elasticity, demand adjustment time, cost perception delay",
          "1.10, 2.0 yr, 1.0 yr", "Assumption; varied in Table 9"),
        R("g_{Y}", "Autonomous demand growth", "0.02 yr⁻¹",
          "Assumption"),
        S("Scale and numerics"),
        R("N_{ref}", "Reference workforce size", "1000 persons",
          "Normalisation"),
        R("Δt, T", "Integration step and simulation horizon",
          "1/16 yr, 25 yr", "Verified in Table 4"),
    ]
    return dict(
        number=2, caption="Parameters, baseline values and their basis.",
        header=["Symbol", "Description", "Value", "Basis"], rows=rows,
        widths=[0.15, 0.43, 0.17, 0.25],
        note="Task shares follow the occupational-exposure estimates in "
             "[[eloundou2024]],[[felten2021]]; the floor on the skill-formation "
             "value of AI-mediated work follows the qualitative evidence on "
             "shadow learning and the black-boxing of analytical technologies "
             "[[beane2019]],[[anthony2021]]. Parameters marked as calibrated are "
             "estimated jointly against the four benchmarks of Table 3. The "
             "mentoring coefficient m is derived analytically so that the "
             "pre-GenAI state is an exact fixed point of the model.",
        italic_col=0, wide=True, align="llcl")


# ---------------------------------------------------------------------------
def table3():
    _, rows = _read("table_calibration_targets.tsv")
    body = [R(r[0], num(r[1]), num(r[2]), r[3]) for r in rows]
    body += [S("Fitted parameter values"),
             R("Frontier inflection, t_{F}", "—", "1.285 yr", ""),
             R("Adoption rate, ν", "—", "1.328 yr⁻¹", ""),
             R("Utilisation half-saturation, a_{u}", "—", "0.215", ""),
             R("Junior productivity elasticity, β_{J}", "—", "0.739", ""),
             R("Senior productivity elasticity, β_{S}", "—",
               "0.246 (= β_{J}/3)", "")]
    return dict(
        number=3,
        caption="Calibration benchmarks and fitted parameter values.",
        header=["Benchmark", "Empirical value", "Model value", "Source"],
        rows=body, widths=[0.42, 0.16, 0.16, 0.26],
        note="Four parameters are fitted by nonlinear least squares to four "
             "independent benchmarks, so the calibration is exact by "
             "construction; its purpose is to place the simulated trajectory on "
             "the same quantitative scale as the observed one. Sources are "
             "[[canaries2025]], [[humlum2025]], [[brynjolfsson2025]] with "
             "[[cui2026]], and [[brynjolfsson2025]] with [[dellacqua2026]], "
             "respectively. The senior elasticity is tied to the junior "
             "elasticity by the experience-compression ratio of three reported "
             "in that evidence.",
        italic_col=None, wide=True, align="lccl")


def table4():
    _, rows = _read("table_validation.tsv")
    return dict(
        number=4, caption="Model validation tests.",
        header=["Test", "Procedure", "Result", "Outcome"],
        rows=[R(r[0], sym(r[1]), sym(r[2]), r[3]) for r in rows],
        widths=[0.20, 0.31, 0.37, 0.12],
        note="Tests follow the standard sequence for building confidence in "
             "system dynamics models [[forrester1980]],[[barlas1996]]. The "
             "equilibrium test verifies that the pre-shock configuration is an "
             "exact fixed point; the integration-error test verifies that the "
             "reported behaviour is not an artefact of the time step.",
        italic_col=None, wide=True, align="lllc")


def table5():
    _, rows = _read("table_baseline.tsv")
    dec = [0, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 3]

    rows = [[num(v, dec[j]) for j, v in enumerate(r)] for r in rows]
    return dict(
        number=5, caption="Baseline trajectory of the calibrated model.",
        header=["t (yr)", "A", "u", "K", "Λ", "α", "ρ", "x", "Φ", "ΔJ (%)",
                "ΔS (%)", "ΔY (%)", "ΔC (%)", "E"],
        rows=[R(*r) for r in rows], widths=[0.078] + [0.0709] * 13,
        note="Δ denotes the percentage deviation from the no-GenAI "
             "counterfactual run of the identical model; E is the net "
             "entry-port elasticity of Equation (19). Symbols are defined in "
             "Table 1.",
        italic_col=None, wide=True, align="c" * 14)


SHORT = {"S0": "Baseline", "S1": "Automation-first",
         "S2": "Learning system", "S3": "Work redesign",
         "S4": "Apprenticeship", "S5": "AI scaffolding",
         "S6": "Joint package"}


def table6():
    _, rows = _read("table_policies.tsv")
    return dict(
        number=6,
        caption="Design and policy scenarios: outcomes relative to the no-GenAI "
                "counterfactual.",
        header=["Code", "Scenario", "ΔJ_{5}", "ΔJ_{25}", "Δh",
                "ΔS_{25}", "ΔY_{5}", "ΔY_{25}", "ΔC_{25}", "Φ_{25}",
                "Trough", "t*"],
        rows=[R(r[0], SHORT[r[0]], *[num(c) for c in r[2:12]])
              for r in rows],
        widths=[0.062, 0.208] + [0.073] * 10,
        note="All entries other than Φ and t* are percentage deviations from "
             "the no-GenAI counterfactual; subscripts denote the year of "
             "evaluation. Δh is the change in cumulative entry hiring over the "
             "25-year horizon, “Trough” the deepest deviation of entry "
             "employment and t* the year in which it occurs. S1 combines a "
             "higher automation ceiling (0.75) with halved learning investment; "
             "S2 doubles λ; S3 raises the reinstatement ceiling to 0.50; S4 raises m "
             "by 30%; S5 raises η by 60%; S6 applies S2–S5 jointly. No scenario "
             "returns entry employment to the counterfactual level within the "
             "horizon.",
        italic_col=None, wide=True, align="cl" + "c" * 10)


def table7():
    _, rows = _read("table_factorial.tsv")
    body = []
    for r in rows:
        if r[0] in ("main effect", "interaction"):
            name = {"lambda": "learning investment (λ)",
                    "rho_max": "work redesign (ρ_{max})",
                    "lambda x rho_max": "λ × ρ_{max}"}[r[1]]
            lab = ("Main effect of " if r[0] == "main effect"
                   else "Interaction, ")
            body.append(R(lab + name, "", "", num(r[4]), "", ""))
        else:
            body.append(R("λ %s, ρ_{max} %s" % (r[0], r[1]),
                          r[2], r[3], num(r[4]), num(r[5]), r[6]))
    return dict(
        number=7,
        caption="Joint-optimisation test: 2 × 2 factorial on the technical and "
                "the social design lever.",
        header=["Configuration", "λ", "ρ_{max}",
                "ΔJ₂₅ (%)", "ΔY₂₅ (%)", "ρ at year 25"],
        rows=body, widths=[0.28, 0.11, 0.13, 0.16, 0.16, 0.16],
        note="Main effects are the average of the two simple effects and the "
             "interaction is the difference of differences, both in percentage "
             "points of entry employment at year 25. A positive interaction "
             "indicates that the technical and the social subsystem are "
             "complements, as predicted by Proposition 4.",
        italic_col=None, wide=True, align="lccccc")


def table8():
    _, rows = _read("table_closure.tsv")
    short = {"Baseline": "Baseline",
             "Automation-first intensification": "Automation-first"}
    body = [R("%s  %s" % (r[0], short.get(r[1], r[1])), sym(r[2]),
              num(r[3]), num(r[4]), num(r[5]), num(r[6], 3), num(r[7], 3))
            for r in rows]
    return dict(
        number=8,
        caption="Effect of the model boundary: partial-equilibrium versus "
                "sector-consistent closure of the external market for "
                "experienced staff.",
        header=["Scenario", "Closure", "ΔJ_{25} (%)",
                "ΔS_{25} (%)", "ΔY_{25} (%)", "Φ_{25}",
                "Ω_{25}"],
        rows=body, widths=[0.21, 0.23, 0.12, 0.12, 0.12, 0.10, 0.10],
        note="Under the partial-equilibrium closure (ω = 0) the external pool of "
             "experienced staff is unaffected by the sector's own promotion "
             "flow; under the sector-consistent closure (ω = 1) it is "
             "proportional to it, as in Equation (14). The comparison isolates "
             "the composition fallacy discussed in Section 4.5.",
        italic_col=None, wide=True, align="ll" + "c" * 5)


def table9():
    _, rows = _read("table_sensitivity.tsv")
    return dict(
        number=9,
        caption="Global sensitivity analysis: partial rank correlation "
                "coefficients.",
        header=["Parameter", "Baseline", "PRCC (ΔJ)", "PRCC (ΔS)",
                "PRCC (ΔY)", "Sig."],
        rows=[R(sym(r[0]), r[1], num(r[2]), num(r[3]), num(r[4]), r[5])
              for r in rows],
        widths=[0.42, 0.115, 0.125, 0.125, 0.125, 0.09],
        note="Latin hypercube sample of 800 parameter vectors drawn from ±30% "
             "intervals around the calibrated values of fifteen parameters; the "
             "mentoring coefficient is re-derived in every draw so that each "
             "configuration starts from its own exact pre-GenAI equilibrium. "
             "Outcomes are 25-year deviations from the matched counterfactual. "
             "*** p < 0.001, ** p < 0.01, * p < 0.05.",
        italic_col=None, wide=True, align="l" + "c" * 5)


TABLES = {"table1": table1, "table2": table2, "table3": table3,
          "table4": table4, "table5": table5, "table6": table6,
          "table7": table7, "table8": table8, "table9": table9}


# ---------------------------------------------------------------------------
FIGURES = {
    "figure1": dict(
        number=1, file="figure1_cld.png", width_cm=17.0,
        caption="Causal loop diagram of the youth entry port under generative "
                "artificial intelligence.",
        note="Arrows denote causal links; “+” indicates that the two variables "
             "move in the same direction and “−” that they move in opposite "
             "directions. B denotes a balancing loop and R a reinforcing loop: "
             "B1 entry-port displacement; B2 productivity–headcount; R1 task "
             "reinstatement; R2 organisational learning engine; R3 development "
             "pipeline; R4 scale and competitiveness."),
    "figure2": dict(
        number=2, file="figure2_sfd.png", width_cm=17.0,
        caption="Stock-and-flow structure of the model.",
        note="Rectangles are stocks, double arrows with valves are flows, dashed "
             "arrows are information links and clouds mark the boundary of the "
             "system. The corresponding equations are given in Section 3.2."),
    "figure3": dict(
        number=3, file="figure3_baseline.png", width_cm=17.0,
        caption="Baseline behaviour of the calibrated model. (a) Capability, "
                "utilisation, routines and absorptive capacity; (b) task "
                "shares; (c) workforce stocks against the counterfactual; "
                "(d) deviations from the counterfactual; (e) fulfilment, "
                "experiential quality and external availability; (f) output and "
                "unit cost.",
        note="The counterfactual is a run of the identical model with the "
             "external generative-AI frontier held at zero. Time zero is the "
             "point at which the frontier becomes available."),
    "figure4": dict(
        number=4, file="figure4_elasticity.png", width_cm=17.0,
        caption="Decomposition and scenario dependence of the net entry-port "
                "elasticity. (a) Contributions of the reinstatement, "
                "displacement and headcount-saving forces in the baseline; "
                "(b) net elasticity under five scenarios.",
        note="The three contributions in panel (a) sum to the net elasticity E "
             "of Equation (19). Negative values indicate dominance of the "
             "balancing loops B1 and B2 and positive values dominance of the "
             "reinforcing loops R1 and R2."),
    "figure5": dict(
        number=5, file="figure5_regimes.png", width_cm=17.0,
        caption="Regime maps of the 25-year effect on entry employment. "
                "(a) Automation ceiling against reinstatement ceiling; "
                "(b) learning-investment rate against reinstatement ceiling.",
        note="The solid contour is the locus along which generative AI leaves "
             "entry employment unchanged relative to the counterfactual; dotted "
             "contours mark −20% and −40%. The open circle marks the calibrated "
             "baseline. All parameters other than the two on the axes are held "
             "at their baseline values."),
    "figure6": dict(
        number=6, file="figure6_policies.png", width_cm=17.0,
        caption="Design and policy scenarios. (a) Trajectories of entry "
                "employment relative to the counterfactual; (b) outcomes at "
                "year 25, with the output fulfilment ratio on the right axis.",
        note="Scenario codes are defined in Table 6: S0 baseline; S1 "
             "automation-first intensification; S2 learning-system investment; "
             "S3 work redesign; S4 apprenticeship protection; S5 AI-mediated "
             "knowledge scaffolding; S6 joint socio-technical package."),
    "figure7": dict(
        number=7, file="figure7_sensitivity.png", width_cm=17.0,
        caption="Global sensitivity analysis. (a) Partial rank correlation "
                "coefficients with the 25-year effect on entry employment; "
                "(b) distribution of that effect across the sample.",
        note="Latin hypercube sample of 800 draws from ±30% intervals around the "
             "calibrated parameter values. Blue bars indicate a positive and red "
             "bars a negative partial rank correlation. The dashed line in panel "
             "(b) marks the median outcome."),
}
