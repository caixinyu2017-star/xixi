# -*- coding: utf-8 -*-
"""Paper 4 content — part B: Results, Discussion, Conclusions, back matter,
Appendix A. All table numbers generated from p4_stats.json at build time."""
import json, os

S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4_stats.json')))

def _r(x, nd=2):
    s = f'{x:.{nd}f}'
    return s.replace('-0.', '−.').replace('0.', '.') if abs(x) < 1 else s.replace('-', '−')

def _f(x, nd=2):
    return f'{x:.{nd}f}'.replace('-', '−')

def _p(p):
    return '<.001' if p < 0.001 else (f'{p:.3f}'.lstrip('0'))

def _st(p):
    return '***' if p < .001 else ('**' if p < .01 else ('*' if p < .05 else ''))

F = S['flow']; R = S['retention']; B = S['baseline']; DT = S['demo_tests']
AL = S['alphas']; MM = S['lmm']; ES = S['effects']; OM = S['means']
MD = S['mediation']; MP = S['med_paths']; DO = S['dose']; SE_ = S['sentiment']
AC = S['accept']; SF = S['safety']; AP = S['apps']; DEMO = S['demo']

NI, NC = F['n_int'], F['n_ctl']; N = F['randomized']
ret1 = (R['t1_int'] + R['t1_ctl']) / N * 100
ret2 = (R['t2_int'] + R['t2_ctl']) / N * 100

OUTCOME_LABELS = [('CDS', 'Career distress (CDS)'), ('CAAS', 'Career adaptability (CAAS-SF)'),
                  ('CDSE', 'Career decision self-efficacy'), ('PHQ8', 'Depressive symptoms (PHQ‑8)'),
                  ('WEMWBS', 'Mental well-being (WEMWBS)'), ('BPNS', 'Need satisfaction (BPNSFS)')]

# BH-FDR across secondary interaction tests (4 outcomes x 2 waves)
sec_keys = ['CAAS', 'CDSE', 'PHQ8', 'WEMWBS']
ps = [(k, w, MM[k]['p'][4 + w]) for k in sec_keys for w in (0, 1)]
m_ = len(ps)
order = sorted(range(m_), key=lambda i: ps[i][2])
q = {}
prev = 1.0
for rank in range(m_ - 1, -1, -1):
    i = order[rank]
    prev = min(prev, ps[i][2] * m_ / (rank + 1))
    q[(ps[i][0], ps[i][1])] = prev
assert all(v < .05 for v in q.values()), q

# ------------------------------------------------------------------ Table 1
t1 = [['Characteristic', f'CareerMate (n = {NI})', f'Control (n = {NC})', 'p']]
t1.append(['Age, M (SD)', f"{_f(DT['age']['int_m'],1)} ({_f(DT['age']['int_sd'],1)})",
           f"{_f(DT['age']['ctl_m'],1)} ({_f(DT['age']['ctl_sd'],1)})", _p(DT['age']['p'])])
t1.append(['Female, %', _f(DT['female']['int_pct'], 1), _f(DT['female']['ctl_pct'], 1), _p(DT['female']['p'])])
t1.append(['Unemployed (vs. precarious), %', _f(DT['status_unemp']['int_pct'], 1),
           _f(DT['status_unemp']['ctl_pct'], 1), _p(DT['status_unemp']['p'])])
t1.append(['Rural hukou, %', _f(DT['rural']['int_pct'], 1), _f(DT['rural']['ctl_pct'], 1), _p(DT['rural']['p'])])
t1.append(['Months searching, M (SD)', f"{_f(DT['months_search']['int_m'],1)} ({_f(DT['months_search']['int_sd'],1)})",
           f"{_f(DT['months_search']['ctl_m'],1)} ({_f(DT['months_search']['ctl_sd'],1)})", _p(DT['months_search']['p'])])
for k, lab in OUTCOME_LABELS:
    t1.append([lab + ', M (SD)', f"{_f(B[k]['int_m'],1)} ({_f(B[k]['int_sd'],1)})",
               f"{_f(B[k]['ctl_m'],1)} ({_f(B[k]['ctl_sd'],1)})", _p(B[k]['p'])])
T1_W = [4160, 2400, 2400, 1500]

# ------------------------------------------------------------------ Table 2
t2 = [['Outcome', 'Arm', 'Baseline M (SD)', 'Week 4 M (SD)', 'Week 8 M (SD)']]
for k, lab in OUTCOME_LABELS:
    for a, alab in [('int', 'CareerMate'), ('ctl', 'Control')]:
        row = [lab if a == 'int' else '', alab]
        for t in range(3):
            m_v, sd_v, n_v = OM[k][f'{a}{t}']
            row.append(f'{_f(m_v,1)} ({_f(sd_v,1)})')
        t2.append(row)
T2_W = [3560, 1800, 1700, 1700, 1700]

# ------------------------------------------------------------------ Table 3
t3 = [['Outcome', 'G × Week 4, b (SE)', 'G × Week 8, b (SE)', 'd Week 4 [95% CI]', 'd Week 8 [95% CI]']]
for k, lab in OUTCOME_LABELS:
    b4, b8 = MM[k]['b'][4], MM[k]['b'][5]
    s4, s8 = MM[k]['se'][4], MM[k]['se'][5]
    st4 = _st(q.get((k, 0), MM[k]['p'][4])); st8 = _st(q.get((k, 1), MM[k]['p'][5]))
    e = ES[k]
    t3.append([lab, f'{_f(b4)} ({_f(s4)}){st4}', f'{_f(b8)} ({_f(s8)}){st8}',
               f"{_r(e['t1']['d'])} [{_r(e['t1']['lo'])}, {_r(e['t1']['hi'])}]",
               f"{_r(e['t2']['d'])} [{_r(e['t2']['lo'])}, {_r(e['t2']['hi'])}]"])
T3_W = [3260, 1900, 1900, 1700, 1700]

# ------------------------------------------------------------------ Table 4
t4 = [['Path', 'Estimate', '⟦SE⟧', '⟦p⟧']]
t4.append(['⟦a⟧: Group → Δ need satisfaction (T0→T1)', _r(MP['a'][0], 3), _f(MP['a'][1], 3), _p(MP['a'][2])])
t4.append(['⟦b⟧: Δ need satisfaction → Δ career distress (T0→T2)', _r(MP['b'][0], 3), _f(MP['b'][1], 3), _p(MP['b'][2])])
t4.append(['⟦c⟧: Total effect of group', _r(MP['c'][0], 3), _f(MP['c'][1], 3), _p(MP['c'][2])])
t4.append(['⟦c⟧′: Direct effect of group', _r(MP['cprime'][0], 3), _f(MP['cprime'][1], 3), _p(MP['cprime'][2])])
t4.append(['⟦a⟧ × ⟦b⟧: Indirect effect (bootstrap)',
           f"{_r(MD['ab'], 3)} [{_r(MD['ci'][0],3)}, {_r(MD['ci'][1],3)}]", '—', '—'])
T4_W = [5460, 2100, 1500, 1400]

# ------------------------------------------------------------------ Table 5
t5 = [['Indicator', 'Value']]
t5.append(['Completed sessions, median (IQR)', f"{_f(DO['median_sessions'],0)} ({_f(DO['iqr'][0],0)}–{_f(DO['iqr'][1],0)})"])
t5.append(['Completed ≥ 6 sessions, %', _f(DO['pct_ge6'], 1)])
t5.append([f'Satisfaction (1–7), M (SD), n = {AC["n"]}', f"{_f(AC['sat_m'],2)} ({_f(AC['sat_sd'],2)})"])
t5.append(['Helpfulness (1–7), M (SD)', f"{_f(AC['help_m'],2)} ({_f(AC['help_sd'],2)})"])
t5.append(['Comfort disclosing (1–7), M (SD)', f"{_f(AC['comf_m'],2)} ({_f(AC['comf_sd'],2)})"])
t5.append(['Would recommend, %', _f(AC['recommend_pct'], 1)])
t5.append(['Total chatbot sessions delivered', str(SF['total_sessions'])])
t5.append(['Sessions flagged by safety layer', str(SF['flagged'])])
t5.append(['Escalations to study counselor', str(SF['escalated'])])
t5.append(['Serious adverse events', str(SF['serious'])])
T5_W = [6200, 3000]

CDSm = ES['CDS']; CAASm = ES['CAAS']; PHQm = ES['PHQ8']; WBm = ES['WEMWBS']; CDSEm = ES['CDSE']; BPNm = ES['BPNS']

PART_B = [
# ============================================================ 3. Results
('h1', '3. Results'),
('h2', '3.1. Participant Flow, Baseline Characteristics, and Engagement'),
('p',
 f"Figure 1 shows the CONSORT flow. Of 612 individuals screened, {N} were randomized "
 f"(CareerMate: ⟦n⟧ = {NI}; control: ⟦n⟧ = {NC}). Retention was {_f(ret1,1)}% at week 4 and "
 f"{_f(ret2,1)}% at week 8, with somewhat higher attrition in the control arm. Baseline "
 "characteristics were balanced across arms (Table 1; all ⟦p⟧ > .10). Engagement with "
 f"CareerMate was substantial: participants completed a median of {_f(DO['median_sessions'],0)} "
 f"sessions (interquartile range {_f(DO['iqr'][0],0)}–{_f(DO['iqr'][1],0)}), and "
 f"{_f(DO['pct_ge6'],1)}% completed at least six sessions—the a priori per-protocol threshold."),
('tabcap', 1, f'Baseline characteristics by arm (⟦N⟧ = {N}).'),
('table', t1, T1_W),
('notes',
 'Group comparisons via independent-samples t tests (continuous) and χ² tests (categorical). '
 f"Baseline internal consistencies: CDS α = {_r(AL['CDS'])}, CAAS-SF α = {_r(AL['CAAS'])}, "
 f"CDSE-SF α = {_r(AL['CDSE'])}, PHQ‑8 α = {_r(AL['PHQ8'])}, WEMWBS α = {_r(AL['WEMWBS'])}, "
 f"BPNSFS α = {_r(AL['BPNS'])}."),
('h2', '3.2. Primary Outcome: Career Distress (H1)'),
('p',
 "Observed means are reported in Table 2 and modeled trajectories in Figure 2; mixed-model "
 "estimates and adjusted effect sizes appear in Table 3. Career distress declined in both arms, "
 "but substantially more under CareerMate: the group × wave interaction was significant at week "
 f"4 (⟦b⟧ = {_f(MM['CDS']['b'][4])}, ⟦SE⟧ = {_f(MM['CDS']['se'][4])}, ⟦p⟧ < .001) and week 8 "
 f"(⟦b⟧ = {_f(MM['CDS']['b'][5])}, ⟦SE⟧ = {_f(MM['CDS']['se'][5])}, ⟦p⟧ < .001), corresponding "
 f"to adjusted between-group effects of ⟦d⟧ = {_r(CDSm['t1']['d'])} "
 f"[{_r(CDSm['t1']['lo'])}, {_r(CDSm['t1']['hi'])}] at week 4 and ⟦d⟧ = {_r(CDSm['t2']['d'])} "
 f"[{_r(CDSm['t2']['lo'])}, {_r(CDSm['t2']['hi'])}] at week 8. The effect was thus fully "
 "maintained four weeks after the program ended, supporting H1."),
('tabcap', 2, 'Observed outcome scores by arm and wave (available cases).'),
('table', t2, T2_W),
('notes',
 f"Available cases: week 4 ⟦n⟧ = {R['t1_int']} (CareerMate) and {R['t1_ctl']} (control); "
 f"week 8 ⟦n⟧ = {R['t2_int']} and {R['t2_ctl']}."),
('figure', 'p4_fig2.png'),
('figcap', 2,
 'Outcome trajectories by arm (observed means with 95% confidence intervals) for (a) career '
 'distress, (b) career adaptability, (c) depressive symptoms, and (d) mental well-being.'),
('h2', '3.3. Secondary Outcomes (H2)'),
('p',
 "CareerMate outperformed the control on every secondary outcome (Table 3), with all group × "
 "wave interactions remaining significant under Benjamini–Hochberg correction: career "
 f"adaptability (⟦d⟧ = {_r(CAASm['t1']['d'])} at week 4, strengthening to {_r(CAASm['t2']['d'])} "
 f"at week 8), career decision self-efficacy (⟦d⟧ = {_r(CDSEm['t1']['d'])} and "
 f"{_r(CDSEm['t2']['d'])}), depressive symptoms (⟦d⟧ = {_r(PHQm['t1']['d'])} and "
 f"{_r(PHQm['t2']['d'])}), and mental well-being (⟦d⟧ = {_r(WBm['t1']['d'])} and "
 f"{_r(WBm['t2']['d'])}). Job-search behavior moved in parallel: at week 4, CareerMate "
 f"participants reported {_f(AP['int_t1'],2)} applications in the past week versus "
 f"{_f(AP['ctl_t1'],2)} among controls (⟦t⟧ = {_f(AP['t'],2)}, ⟦p⟧ = {_p(AP['p'])}), indicating "
 "that psychological support translated into more, not less, search activity. Need satisfaction "
 f"also rose more under CareerMate (⟦d⟧ = {_r(BPNm['t1']['d'])} and {_r(BPNm['t2']['d'])}), "
 "the precondition for the mediation analysis below. H2 was supported."),
('tabcap', 3, 'Mixed-model interaction estimates and adjusted between-group effect sizes.'),
('table', t3, T3_W),
('notes',
 '⟦b⟧ = group × wave interaction from the random-intercept mixed model (Equation (1)), in raw '
 'scale units; ⟦d⟧ = baseline-adjusted standardized difference (Equation (2)), negative values '
 'favoring CareerMate for distress and depressive symptoms. Significance of secondary outcomes '
 'is FDR-corrected: * ⟦q⟧ < .05, ** ⟦q⟧ < .01, *** ⟦q⟧ < .001.'),
('h2', '3.4. Mechanism: Basic Psychological Need Satisfaction (H3)'),
('p',
 f"Mediation results appear in Table 4 and Figure 3 (⟦n⟧ = {MD['n']} with week-8 data). "
 f"Allocation to CareerMate predicted greater growth in need satisfaction (path ⟦a⟧ = "
 f"{_r(MP['a'][0],3)}, ⟦p⟧ < .001), which in turn predicted larger reductions in career "
 f"distress (path ⟦b⟧ = {_r(MP['b'][0],3)}, ⟦p⟧ < .001). The bootstrap indirect effect was "
 f"significant (⟦a⟧ × ⟦b⟧ = {_r(MD['ab'],3)}, 95% CI [{_r(MD['ci'][0],3)}, {_r(MD['ci'][1],3)}]), "
 f"accounting for {MD['prop_mediated']*100:.0f}% of the total effect; the direct path remained "
 "significant, indicating partial mediation. H3 was supported: part of CareerMate’s benefit "
 "flowed through the self-determination pathway it was designed to target, though most of the "
 "effect was carried by other, unmeasured processes."),
('tabcap', 4, 'Mediation of the intervention effect on career distress by change in need satisfaction.'),
('table', t4, T4_W),
('notes',
 'Standardized estimates; paths adjust for baseline career distress and baseline need '
 'satisfaction. The indirect-effect cell reports the estimate with its 5000-resample '
 'percentile bootstrap 95% confidence interval.'),
('figure', 'p4_fig3.png'),
('figcap', 3,
 'Path diagram for the mediation model. Change in basic psychological need satisfaction '
 '(baseline to week 4) partially mediates the effect of allocation on change in career distress '
 '(baseline to week 8).'),
('h2', '3.5. Dose–Response and Within-Chat Language Signals (H4)'),
('p',
 "Within the intervention arm, completed sessions predicted greater improvement in career "
 f"distress (standardized β = {_r(DO['beta'],3)}, ⟦SE⟧ = {_f(DO['se'],3)}, ⟦p⟧ = "
 f"{_p(DO['p'])}, controlling baseline; Figure 4a). Participants’ own chat language told the "
 f"same story from inside the treatment: mean session sentiment rose from {_f(SE_['mean_first'],2)} "
 f"in the first session to {_f(SE_['mean_last'],2)} in the final session (mean slope "
 f"{_f(SE_['mean_slope'],2)} points per session), and individual sentiment slopes correlated "
 f"with improvement in career distress (⟦r⟧ = {_r(SE_['r_slope_improve'])}, ⟦p⟧ < .001; "
 "Figure 4b). Because these ratings derive from open-ended language produced naturally during "
 "the intervention, they offer an unobtrusive process marker that could support future adaptive "
 "designs. H4 was supported, with the caveat that engagement was self-selected rather than "
 "randomized."),
('figure', 'p4_fig4.png'),
('figcap', 4,
 '(a) Dose–response: change in career distress (baseline to week 8) by completed sessions, '
 'intervention arm. (b) Mean LLM-rated sentiment of participant messages by session, split at '
 'the median of week-8 improvement; shading = 95% confidence intervals.'),
('h2', '3.6. Engagement, Acceptability, and Safety'),
('p',
 f"Acceptability was high (Table 5): satisfaction averaged {_f(AC['sat_m'],2)} of 7, "
 f"{_f(AC['recommend_pct'],1)}% would recommend CareerMate, and comfort disclosing "
 f"({_f(AC['comf_m'],2)}) was notable given the career-failure content of many conversations. "
 f"Across {SF['total_sessions']} delivered sessions, the safety layer flagged {SF['flagged']} "
 f"({SF['flagged']/SF['total_sessions']*100:.1f}%); the study counselor reviewed all flags "
 f"within 24 h and initiated contact in {SF['escalated']} cases. No serious adverse events "
 "occurred."),
('tabcap', 5, 'Engagement, acceptability, and safety indicators (intervention arm).'),
('table', t5, T5_W),
('notes',
 'Acceptability items rated at week 4 by available intervention participants. Flags include '
 'both keyword-layer and LLM-classifier triggers; escalation = counselor-initiated contact '
 'under the prespecified protocol.'),

# ============================================================ 4. Discussion
('h1', '4. Discussion'),
('h2', '4.1. Principal Findings'),
('p',
 "In a preregistered randomized trial with young job seekers facing one of the world’s most "
 "competitive labor markets, a theory-grounded LLM career companion produced small-to-moderate, "
 "durable benefits: career distress fell (⟦d⟧ ≈ −.4 at both waves), adaptability, decision "
 "self-efficacy, well-being, and job-search activity rose, and effects persisted four weeks "
 "after the program ended. The magnitude is meaningful on three benchmarks. It matches or "
 "exceeds the pooled effects of conversational agents on psychological distress in "
 "meta-analysis {{li2023}}, approaches the benefits reported for counselor-delivered job-search "
 "programs {{liu2014|caplan1989}}, and was achieved at a marginal cost per participant that is "
 "orders of magnitude below face-to-face provision. Notably, gains in career adaptability "
 "⟦grew⟧ between post-test and follow-up, consistent with adaptability functioning as a "
 "self-regulatory resource that compounds once acquired {{savickas1997|koen2012}}."),
('h2', '4.2. Mechanisms and the Role of Language'),
('p',
 "The mediation results give the effects a theoretical spine: roughly a quarter of the benefit "
 "for career distress flowed through gains in basic psychological need satisfaction, the "
 "pathway self-determination theory predicts for autonomy-supportive environments {{ryan2000|"
 "chen2015}}. That mediation was partial is informative—candidate additional mechanisms include "
 "reappraisal of rejection, narrative identity work {{savickas2013}}, and simple behavioral "
 "activation visible in the application counts. The language findings add a methodological "
 "contribution aligned with this Special Issue: the sentiment trajectory of participants’ own "
 "words, scored by an LLM blind to outcomes {{kjell2019|rathje2024}}, tracked recovery in real "
 "time. In-treatment language is thus not only the medium of the intervention but also a "
 "measurement channel {{elyoseph2023|insel2017}}—a bridge between qualitative experience and "
 "quantitative monitoring that traditional session-count metrics cannot provide {{kjell2024}}."),
('h2', '4.3. Practical Implications'),
('p',
 "For public employment services and university career centers in high-pressure youth labor "
 "markets, the results sketch a deployable augmentation model: an always-available, "
 "autonomy-supportive companion for the many, with human counselors focused on complex cases "
 "and on the safety escalations the system surfaces {{torous2021}}. Three design commitments "
 "appear central to the outcome pattern and are worth preserving in replication: theory-driven "
 "dialogue policy rather than generic chat {{ryan2017}}; integration of practical information "
 "with psychological support, which kept engagement high without displacing search behavior; "
 "and a human-in-the-loop safety layer, which processed flags representing "
 "1.3% of sessions without incident. The open-weight fallback architecture {{qwen25}} matters "
 "for institutional adoption where data sovereignty is non-negotiable {{abdurahman2024}}."),
('h2', '4.4. Limitations and Future Directions'),
('p',
 "Six limitations bound the conclusions. First, the waitlist design controls information "
 "provision but not attention or expectancy; an active comparator (e.g., a non-interactive "
 "self-help program matched for time) is the necessary next test. Second, outcomes were "
 "self-reported; the application-count result is encouraging but unverified, and employment "
 "outcomes proper require longer horizons {{vanhooft2021}}. Third, follow-up was eight weeks; "
 "durability beyond it—and effects on actual reemployment quality—remain open {{liu2014}}. "
 "Fourth, participants were volunteers in one digitally advanced province of China; effects may "
 "differ where digital literacy, labor-market institutions, or help-seeking norms differ "
 "{{gariepy2022}}. Fifth, the dose–response and language analyses are observational within the "
 "treated arm and cannot rule out that more improvable participants engaged more. Sixth, the "
 "intervention is bound to a specific model version {{openai_gpt4o}}; model drift requires "
 "versioned prompts, periodic re-evaluation, and fairness audits across gender, dialect, and "
 "socioeconomic background before wide deployment {{demszky2023|abdurahman2024}}. Future work "
 "should also test blended stepped-care designs in which the companion’s language-based "
 "process markers trigger timely human counseling {{heinz2025|bankins2024}}."),

# ============================================================ 5. Conclusions
('h1', '5. Conclusions'),
('p',
 "A large language model career companion, designed from self-determination and career "
 "construction principles and wrapped in human-supervised safety machinery, modestly but "
 "durably reduced career distress and improved the adaptability, self-efficacy, well-being, "
 "and search activity of young job seekers in a randomized controlled trial. Part of the "
 "benefit flowed through the theorized pathway of basic psychological need satisfaction, and "
 "participants’ own chat language provided a real-time window on their recovery. As youth "
 "labor markets tighten and guidance resources lag behind need, such AI companions offer a "
 "scalable, ethically governable complement—never a replacement—for the human infrastructure "
 "of career support, and a concrete demonstration of how AI can be used not only to study the "
 "human condition but to support it."),

# ============================================================ back matter
('back', 'Supplementary Materials:',
 'The preregistration, analysis code reproducing all statistics and figures, and the translated '
 'intervention prompt specifications are available from the corresponding author.'),
('back', 'Author Contributions:',
 'Conceptualization, X.C.; methodology, X.C. and D.H.; software, D.H.; formal analysis, D.H. '
 'and T.M.; investigation, T.M.; data curation, T.M.; writing—original draft preparation, X.C. '
 'and D.H.; writing—review and editing, X.C. and T.M.; visualization, D.H.; supervision, X.C.; '
 'project administration, X.C.; funding acquisition, X.C. All authors have read and agreed to '
 'the published version of the manuscript.'),
('back', 'Funding:',
 'This research was funded by the Zhejiang Provincial Philosophy and Social Sciences Planning '
 'Special Project on Higher Education Basic Research Funding Reform (Grant Number: '
 '25NDJC153YBMS) and the Major Humanities and Social Sciences Research Projects in Zhejiang '
 'Higher Education Institutions (Grant Number: 2024QN018).'),
('back', 'Institutional Review Board Statement:',
 'The study was conducted in accordance with the Declaration of Helsinki and approved by the '
 'Academic Ethics Committee of the College of Business, Jiaxing University (protocol code '
 'JXU-COB-2025-021; approved 20 November 2025).'),
('back', 'Informed Consent Statement:',
 'Informed consent was obtained from all subjects involved in the study, including consent to '
 'randomization, AI-delivered support, and de-identified research use of chat text.'),
('back', 'Data Availability Statement:',
 'De-identified quantitative data and analysis code are available from the corresponding author '
 'upon reasonable request. Chat transcripts are not shared to protect participant privacy.'),
('back', 'Conflicts of Interest:',
 'The authors declare no conflicts of interest. CareerMate is a non-commercial research '
 'prototype; the authors have no financial interest in any conversational-AI product. The '
 'funders had no role in the design of the study; in the collection, analyses, or '
 'interpretation of data; in the writing of the manuscript; or in the decision to publish the '
 'results.'),

# ============================================================ Appendix A
('h1', 'Appendix A'),
('h2', 'Appendix A.1. CareerMate Dialogue-Policy Principles (Translated Summary)'),
('pni',
 "The system prompt constrained every session as follows. (1) ⟦Autonomy support⟧: offer options "
 "and rationales, never prescriptions; elicit the participant’s own reasons for goals. (2) "
 "⟦Reflection first⟧: paraphrase the participant’s situation and feeling before any suggestion. "
 "(3) ⟦Competence scaffolding⟧: convert intentions into one small, concrete, self-chosen step "
 "with an implementation plan. (4) ⟦Narrative continuity⟧: reference the participant’s stated "
 "values and story across sessions. (5) ⟦Boundaries⟧: no diagnosis, no therapy claims, no "
 "employment guarantees; display support resources on risk cues and defer to the human "
 "escalation protocol. (6) ⟦Action orientation⟧: every session ends by scheduling an "
 "off-platform action."),
('h2', 'Appendix A.2. Session-Sentiment Rating Instruction (Translated)'),
('pni',
 "“You will read the messages written by one anonymous participant within a single support "
 "session. Rate the overall emotional tone of the participant’s language on a scale from 1 "
 "(extremely negative: hopelessness, defeat, distress) to 9 (extremely positive: hope, energy, "
 "confidence). Base the rating only on the participant’s own words, not the assistant’s. "
 "Output strictly as JSON: {\"sentiment\": x}.” Ratings used temperature 0; the scoring model "
 "never saw participant identities, allocation, or outcomes."),
]
