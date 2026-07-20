# -*- coding: utf-8 -*-
"""Paper 3 content — part B: Results, Discussion, Conclusions, back matter,
Appendix A. All table numbers are generated from p3_stats.json at build time."""
import json, os

S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p3_stats.json')))

def _r(x, nd=2, strip=True):
    s = f'{x:.{nd}f}'
    if strip:
        s = s.replace('-0.', '−.').replace('0.', '.') if abs(x) < 1 else s.replace('-', '−')
    else:
        s = s.replace('-', '−')
    return s

def _f(x, nd=2):
    return f'{x:.{nd}f}'.replace('-', '−')

def _p(p):
    if p < 0.001:
        return '<.001'
    return f'{p:.3f}'.lstrip('0') if p < 1 else f'{p:.3f}'

def _stars(q):
    return '***' if q < 0.001 else ('**' if q < 0.01 else ('*' if q < 0.05 else ''))

D = S['demo']; TH = S['themes']; REL = S['reliability']; H = S['hier']; CL = S['classify']
HI = S['highlights']; SA = S['status_anova']; SC = S['scales']
N = S['flow']['final']
cnt = lambda pct: round(pct / 100 * N)

# ------------------------------------------------------------------ Table 1
STATUS = ['Employed (standard contract)', 'Precarious/platform work',
          'Unemployed, actively job-seeking', 'Preparing for further exams',
          'Other non-employed (NEET)']
t1 = [['Characteristic', 'Category', 'n', '%']]
t1 += [['Gender', 'Female', cnt(D['female_pct']), _f(D['female_pct'], 1)],
       ['', 'Male', N - cnt(D['female_pct']), _f(100 - D['female_pct'], 1)],
       ['Age (years)', f"M = {_f(D['age_mean'],1)}, SD = {_f(D['age_sd'],1)}, range 18–29", '', ''],
       ['Education', 'High school or below', cnt(D['edu_pct'][0]), _f(D['edu_pct'][0], 1)],
       ['', 'Vocational college', cnt(D['edu_pct'][1]), _f(D['edu_pct'][1], 1)],
       ['', "Bachelor's degree", cnt(D['edu_pct'][2]), _f(D['edu_pct'][2], 1)],
       ['', "Master's degree or above", cnt(D['edu_pct'][3]), _f(D['edu_pct'][3], 1)],
       ['Household registration', 'Rural hukou', cnt(D['rural_pct']), _f(D['rural_pct'], 1)],
       ['First-generation college', 'Yes (among post-secondary)', cnt(D['firstgen_pct']), _f(D['firstgen_pct'], 1)]]
for lab, n_, p_ in zip(STATUS, D['status_ns'], D['status_pct']):
    t1.append(['Employment status' if lab == STATUS[0] else '', lab, n_, _f(p_, 1)])
T1_W = [2450, 4760, 1500, 1750]

# ------------------------------------------------------------------ Table 2
MEAS = [('Career distress (CDS)', 'CDS', '9–54'), ('Career adaptability (CAAS-SF)', 'CAAS', '12–60'),
        ('Anxiety (GAD-7)', 'GAD7', '0–21'), ('Depressive symptoms (PHQ-8)', 'PHQ8', '0–24'),
        ('Perceived employability', 'SPE', '10–50'), ('Life satisfaction (SWLS)', 'SWLS', '5–35')]
t2 = [['Measure', 'Items', 'Possible Range', 'M', 'SD', 'α', 'ω']]
for lab, k, rng in MEAS:
    v = SC[k]
    t2.append([lab, v['items'], rng, _f(v['mean'], 2), _f(v['sd'], 2), _r(v['alpha']), _r(v['omega'])])
for lab, k in [('LLM career distress (composite)', 'distress'),
               ('LLM employment anxiety (composite)', 'anxiety'),
               ('LLM career confidence (composite)', 'confidence')]:
    v = S['llm_desc'][k]
    t2.append([lab, '—', '1–10', _f(v['mean'], 2), _f(v['sd'], 2), '—', '—'])
T2_W = [3960, 1000, 1600, 1000, 1000, 950, 950]

# ------------------------------------------------------------------ Table 3
def _icc(dim, mod):
    return _r(REL[dim][mod]['icc2k_runs'], 3)
t3 = [['Consistency Index', 'Career Distress', 'Employment Anxiety', 'Career Confidence']]
t3.append(['Across runs, GPT-4o, ICC(2,3)'] + [_icc(d, 'gpt4o') for d in ('distress', 'anxiety', 'confidence')])
t3.append(['Across runs, Qwen2.5-72B, ICC(2,3)'] + [_icc(d, 'qwen25') for d in ('distress', 'anxiety', 'confidence')])
t3.append(['Between models, r'] + [_r(REL[d]['between_models']['r'], 3) for d in ('distress', 'anxiety', 'confidence')])
t3.append(['Between models, ICC(2,1)'] + [_r(REL[d]['between_models']['icc21'], 3) for d in ('distress', 'anxiety', 'confidence')])
T3_W = [4160, 2100, 2100, 2100]

# ------------------------------------------------------- Table 4 correlations
nm = S['corr']['names']; RM = S['corr']['r']; QM = S['corr']['q']
t4 = [['Variable'] + [str(i + 1) for i in range(9)]]
for i in range(10):
    row = [nm[i]]
    for j in range(9):
        row.append(_r(RM[i][j]) + _stars(QM[i][j]) if j < i else '')
    t4.append(row)
T4_W = [3350] + [790] * 9

# ------------------------------------------------------------------ Table 5
THEME_ROWS = [
 ('T1', 'Competitive pressure and credential inflation',
  'Escalating competition for degrees, exams, and positions; feeling that effort no longer differentiates',
  '“Everyone around me is taking the postgraduate or civil-service exams. However hard I try, the bar keeps rising.”'),
 ('T2', 'Skill–job mismatch and practical-experience gaps',
  'Perceived gap between education and job requirements; lack of practical experience; fear of skill obsolescence',
  '“My major taught me theory, but every position asks for two years of hands-on experience I never had a chance to get.”'),
 ('T3', 'Precarity and instability of flexible work',
  'Unstable platform, gig, or short-contract work; income volatility; missing social insurance',
  '“Delivery and livestream jobs pay by the day. I cannot see where I will be in six months, let alone pay into insurance.”'),
 ('T4', 'Family expectations and place-bound constraints',
  'Parental expectations, pressure to return to the home county, and hukou or housing constraints tying choices to place',
  '“My parents want me back in the county for a ‘stable’ job. Staying in Hangzhou means disappointing them and paying rent I cannot afford.”'),
 ('T5', 'Meaning, identity, and motivational struggles',
  'Exhaustion of meaning and motivation after repeated rejection; withdrawal from active search',
  '“I have sent out more than a hundred résumés. Lately I just do not see the point of getting up in the morning.”'),
 ('T6', 'Guidance and information gaps',
  'Not knowing how to search, prepare, or network; absent career guidance; information asymmetry',
  '“Nobody in my family has ever job-hunted with a résumé. I do not even know whom to ask about interviews.”')]
t5 = [['Theme', 'Core Content', 'n (%)', 'Illustrative Excerpt (Translated)']]
for i, (tid, lab, desc, quote) in enumerate(THEME_ROWS):
    t5.append([f'{tid}. {lab}', desc, f"{TH['ns'][i]} ({_f(TH['prevalence_pct'][i],1)}%)", quote])
T5_W = [2620, 3080, 1160, 3600]

# ------------------------------------------------------------------ Table 6
OUTS = [('CDS', 'Career Distress (CDS)'), ('GAD7', 'Anxiety (GAD‑7)'),
        ('PHQ8', 'Depressive Symptoms (PHQ‑8)'), ('SWLS', 'Life Satisfaction (SWLS)')]
t6 = [['Theme', 'n'] + [lab for _, lab in OUTS]]
for t in range(6):
    row = [THEME_ROWS[t][0] + '. ' + THEME_ROWS[t][1], TH['ns'][t]]
    for k, _ in OUTS:
        o = TH['outcomes'][k]
        row.append(f"{_f(o['means'][t],1)} ({_f(o['sds'][t],1)})")
    t6.append(row)
t6.append(['⟦F⟧(5, 941)', ''] + [f"{_f(TH['outcomes'][k]['F'],2)}***" for k, _ in OUTS])
t6.append(['η²', ''] + [_r(TH['outcomes'][k]['eta2'], 3) for k, _ in OUTS])
T6_W = [3760, 800, 1470, 1470, 1480, 1480]

# ------------------------------------------------------------------ Table 7
def _fch(dv, step):
    F, p = H[dv]['fchange'][step]
    df = '(4, 932)' if step == 0 else '(1, 931)'
    return f'{_f(F,2)} {df}{"***" if p < 0.001 else ""}'
t7 = [['Step (Predictors Added)', '⟦R⟧²', 'Δ⟦R⟧²', 'Δ⟦F⟧ (df)', '⟦R⟧²', 'Δ⟦R⟧²', 'Δ⟦F⟧ (df)']]
t7.append(['1. Demographics + status + length',
           _r(H['PHQ8']['r2'][0], 3), '—', '—', _r(H['SWLS']['r2'][0], 3), '—', '—'])
t7.append(['2. + CDS, CAAS‑SF, employability, GAD‑7',
           _r(H['PHQ8']['r2'][1], 3), _r(H['PHQ8']['dr2'][0], 3), _fch('PHQ8', 0),
           _r(H['SWLS']['r2'][1], 3), _r(H['SWLS']['dr2'][0], 3), _fch('SWLS', 0)])
t7.append(['3. + LLM narrative distress',
           _r(H['PHQ8']['r2'][2], 3), _r(H['PHQ8']['dr2'][1], 3), _fch('PHQ8', 1),
           _r(H['SWLS']['r2'][2], 3), _r(H['SWLS']['dr2'][1], 3), _fch('SWLS', 1)])
T7_W = [3420, 780, 780, 1620, 780, 780, 1620]

# ------------------------------------------------------------------ Table 8
FOCAL = [('Career distress (CDS)', 11), ('Career adaptability (CAAS-SF)', 12),
         ('Perceived employability', 13), ('Anxiety (GAD-7)', 14),
         ('LLM narrative distress', 15)]
t8 = [['Predictor (Step 3 Model)', 'β', '⟦SE⟧', '⟦t⟧', '⟦p⟧', 'β', '⟦SE⟧', '⟦t⟧', '⟦p⟧']]
for lab, ix in FOCAL:
    row = [lab]
    for dv in ('PHQ8', 'SWLS'):
        fin = H[dv]['final']
        row += [_r(fin['b'][ix], 3), _r(fin['se'][ix], 3), _f(fin['t'][ix], 2), _p(fin['p'][ix])]
    t8.append(row)
T8_W = [3260, 900, 900, 900, 950, 900, 900, 900, 950]

DL = CL['delong']; DLCV = CL['delong_cv']
kkeys = sorted(TH['sil_by_k'].keys(), key=int)
sil_txt = ', '.join(f"k = {k}: {_r(TH['sil_by_k'][k],3)}" for k in kkeys)

PART_B = [
# ============================================================ 3. Results
('h1', '3. Results'),
('h2', '3.1. Descriptive Statistics and Group Differences'),
('p',
 "Tables 1 and 2 present sample characteristics and measure descriptives. Symptom levels were "
 f"consistent with a community sample under labor-market strain: mean GAD-7 was {_f(SC['GAD7']['mean'],2)} "
 f"(⟦SD⟧ = {_f(SC['GAD7']['sd'],2)}) and mean PHQ-8 was {_f(SC['PHQ8']['mean'],2)} (⟦SD⟧ = "
 f"{_f(SC['PHQ8']['sd'],2)}), with {cnt(S['elev_prev']*100)} participants ({_f(S['elev_prev']*100,1)}%) at or "
 "above the PHQ-8 screening threshold of 10. Career distress differed strongly across employment "
 f"situations (⟦F⟧(4, 942) = {_f(SA['F'],2)}, ⟦p⟧ < .001, η² = {_r(SA['eta2'],3)}): standard employees "
 f"reported the lowest CDS scores (⟦M⟧ = {_f(SA['means'][0],1)}), while unemployed job seekers (⟦M⟧ = "
 f"{_f(SA['means'][2],1)}) and other non-employed youth (⟦M⟧ = {_f(SA['means'][4],1)}) reported the highest, "
 "with precarious workers and exam preparers in between—a gradient consistent with meta-analytic "
 "evidence on unemployment and mental health {{paul2009|gariepy2022}}."),
('tabcap', 1, f'Sample characteristics (⟦N⟧ = {N}).'),
('table', t1, T1_W),
('tabcap', 2, 'Descriptive statistics and internal consistency of study measures.'),
('table', t2, T2_W),
('notes',
 'CDS = Career Distress Scale; CAAS-SF = Career Adapt-Abilities Scale–Short Form; GAD-7 = '
 'Generalized Anxiety Disorder scale; PHQ-8 = Patient Health Questionnaire; SWLS = Satisfaction '
 'With Life Scale. LLM composites average two models × three runs on a 1–10 rubric. α = '
 'Cronbach’s alpha; ω = McDonald’s omega.'),
('h2', '3.2. Reliability of LLM Narrative Ratings (H1)'),
('p',
 "Table 3 summarizes reliability. Repeated runs of the same model were nearly interchangeable "
 f"(ICC(2,3) = {_r(min(REL[d][m]['icc2k_runs'] for d in ('distress','anxiety','confidence') for m in ('gpt4o','qwen25')),3)}–"
 f"{_r(max(REL[d][m]['icc2k_runs'] for d in ('distress','anxiety','confidence') for m in ('gpt4o','qwen25')),3)} "
 "across the three dimensions and both models), and the two "
 "architecturally independent models converged substantially on all three dimensions (⟦r⟧ = "
 f"{_r(min(REL[d]['between_models']['r'] for d in ('distress','anxiety','confidence')),2)}–"
 f"{_r(max(REL[d]['between_models']['r'] for d in ('distress','anxiety','confidence')),2)}). In the human-coded "
 f"subsample (⟦n⟧ = {REL['human']['n']}), the two expert raters agreed at ICC(2,2) = "
 f"{_r(REL['human']['icc2k_raters'],2)} (single-rater ICC(2,1) = {_r(REL['human']['icc21_raters'],2)}), and the "
 f"pooled LLM distress composite correlated ⟦r⟧ = {_r(REL['human']['r_human_llm'],2)} with the pooled human "
 "rating—that is, the six-rating LLM ensemble agreed with the human panel at least as strongly as "
 "the human raters agreed with each other, mirroring reports that LLM annotation can exceed the "
 "consistency of individual human coders {{gilardi2023|rathje2024}}. H1 was supported."),
('tabcap', 3, 'Reliability of LLM narrative ratings across runs and models.'),
('table', t3, T3_W),
('notes',
 f"ICC = two-way random-effects intraclass correlation, absolute agreement. Human coding (⟦n⟧ = "
 f"{REL['human']['n']}): inter-rater ICC(2,2) = {_r(REL['human']['icc2k_raters'],2)}; human–LLM composite "
 f"agreement ⟦r⟧ = {_r(REL['human']['r_human_llm'],2)}. All coefficients ⟦p⟧ < .001."),
('h2', '3.3. Convergent and Discriminant Validity (H2)'),
('p',
 "Table 4 reports the full correlation matrix; Figure 2 will be discussed in Section 3.4, and the "
 "multitrait pattern is visualized in Figure 3. Each LLM dimension correlated most strongly with "
 f"its matching criterion: LLM distress with the CDS (⟦r⟧ = {_r(HI['r_llmd_cds'],2)}; disattenuated for "
 f"unreliability, {_r(HI['disattenuated_llmd_cds'],2)}), LLM anxiety with the GAD-7 (⟦r⟧ = "
 f"{_r(HI['r_llma_gad'],2)}), and LLM career confidence with career adaptability and perceived "
 f"employability (⟦r⟧ = {_r(HI['r_llmc_caas'],2)} and {_r(HI['r_llmc_spe'],2)}). Matching (monotrait) "
 f"correlations averaged {_r(HI['monotrait_mean_r'],2)} versus {_r(HI['heterotrait_mean_r'],2)} for "
 "non-matching (heterotrait) pairs, and the differences held for every dimension, supporting H2. "
 "The magnitudes align with zero-shot LLM validity coefficients reported for other constructs and "
 "languages {{rathje2024|kjell2024}}. Narrative length correlated only weakly with LLM distress "
 f"(⟦r⟧ = {_r(HI['r_llmd_len'],2)}), indicating that the ratings did not simply reward verbosity; "
 f"{S['corr']['n_sig_fdr']} of the {S['corr']['n_tests']} correlations remained significant under "
 "false-discovery-rate control."),
('tabcap', 4, 'Pearson correlations among self-report scales, LLM narrative ratings, and narrative length.'),
('table', t4, T4_W),
('notes',
 '⟦N⟧ = 947. Variable numbers follow the first column. FDR-adjusted significance: * ⟦q⟧ < .05, '
 '** ⟦q⟧ < .01, *** ⟦q⟧ < .001.'),
('figure', 'p3_fig3.png'),
('figcap', 3,
 'Convergent–discriminant pattern: Pearson correlations of the three LLM narrative dimensions '
 '(rows) with the six self-report measures (columns). Monotrait pairs lie on the highlighted '
 'diagonal blocks (LLM distress–CDS, LLM anxiety–GAD-7, LLM confidence–adaptability/employability).'),
('h2', '3.4. The Thematic Structure of Narrated Career Difficulty'),
('p',
 f"K-means solutions on the reduced embedding space favored six clusters (mean silhouette: {sil_txt}); "
 "after researcher review and boundary reassignment (9.1% of cases), the final six-theme solution "
 f"retained a mean silhouette of {_r(TH['silhouette_mean'],3)}. Figure 2 maps the narratives; Table 5 "
 "describes the themes with translated excerpts. Independent human assignment in the coded "
 f"subsample agreed with the automated themes in {_f(TH['human_agree']*100,1)}% of cases (Cohen’s κ = "
 f"{_r(TH['human_kappa'],2)}). Theme membership was far from random with respect to objective "
 f"situation (χ²({TH['chi2_df']}) = {_f(TH['chi2'],1)}, ⟦p⟧ < .001): {_f(HI['pct_T1_in_exam'],1)}% of "
 "exam preparers narrated competitive pressure (T1); "
 f"{_f(HI['pct_T3_in_precarious'],1)}% of precarious workers narrated instability (T3); half of other "
 f"non-employed youth ({_f(HI['pct_T5_in_neet'],1)}%) narrated meaning and motivational struggles (T5); "
 f"T4 (family and place constraints) was predominantly rural-hukou ({_f(HI['pct_T4_rural'],1)}% vs. "
 f"{_f(HI['pct_rural_overall'],1)}% overall); and T6 (guidance gaps) was overwhelmingly first-generation "
 f"({_f(HI['pct_T6_firstgen'],1)}% vs. {_f(D['firstgen_pct'],1)}% overall)—patterns consistent with the "
 "psychology-of-working emphasis on structural constraint {{duffy2016}}."),
('figure', 'p3_fig2.png'),
('figcap', 2,
 'Semantic map of 947 career-difficulty narratives (UMAP projection of BGE-M3 embeddings). '
 'Points are participants, colored by final theme; circled labels mark theme centroids; '
 'percentages give theme prevalence.'),
('tabcap', 5, 'Six themes of narrated career difficulty.'),
('table', t5, T5_W),
('notes',
 'Excerpts are English translations of Chinese narratives, lightly edited and de-identified; '
 'each is a prototypical composite drawn from the 20 narratives closest to the theme centroid.'),
('h2', '3.5. Theme Profiles in Psychological Adjustment (H4)'),
('p',
 "Themes differed reliably on every adjustment indicator (Table 6; Figure 5). The gradient was "
 "steepest for career distress (⟦F⟧(5, 941) = "
 f"{_f(TH['outcomes']['CDS']['F'],2)}, ⟦p⟧ < .001, η² = {_r(TH['outcomes']['CDS']['eta2'],3)}): participants "
 f"whose narratives centered on meaning and motivational struggles (T5) averaged {_f(TH['outcomes']['CDS']['means'][4],1)} "
 f"on the CDS—about three-quarters of a standard deviation above the sample mean—alongside the highest anxiety "
 f"(⟦M⟧ = {_f(TH['outcomes']['GAD7']['means'][4],1)}), the highest depressive symptoms (⟦M⟧ = "
 f"{_f(TH['outcomes']['PHQ8']['means'][4],1)}), and the lowest life satisfaction (⟦M⟧ = "
 f"{_f(TH['outcomes']['SWLS']['means'][4],1)}). Competitive-pressure narratives (T1) showed the second-highest "
 f"anxiety (⟦M⟧ = {_f(TH['outcomes']['GAD7']['means'][0],1)}), whereas family/place narratives (T4) showed "
 f"the most favorable profile (CDS ⟦M⟧ = {_f(TH['outcomes']['CDS']['means'][3],1)}; SWLS ⟦M⟧ = "
 f"{_f(TH['outcomes']['SWLS']['means'][3],1)}), suggesting that externally anchored difficulties are less "
 "corrosive than internally anchored ones. H4 was supported: what young people write about is "
 "informative over and above how distressed they sound."),
('tabcap', 6, 'Psychological adjustment by narrative theme: means (standard deviations) and one-way ANOVAs.'),
('table', t6, T6_W),
('notes', '*** ⟦p⟧ < .001. η² = proportion of variance explained by theme membership.'),
('figure', 'p3_fig5.png'),
('figcap', 5,
 'Theme profiles for (a) career distress and (b) depressive symptoms: theme means with 95% '
 'confidence intervals, ordered by mean level within each panel. Colors match Figure 2.'),
('h2', '3.6. Incremental Validity of LLM Narrative Scores (H3)'),
('p',
 "Hierarchical regressions (Table 7) tested whether a single LLM-derived narrative distress score "
 "adds information beyond demographics, employment status, narrative length, and four validated "
 "questionnaires. For depressive symptoms, adding the LLM score in Step 3 increased explained "
 f"variance from {_r(H['PHQ8']['r2'][1],3)} to {_r(H['PHQ8']['r2'][2],3)} (ΔR² = {_r(H['PHQ8']['dr2'][1],3)}, "
 f"⟦F⟧(1, 931) = {_f(H['PHQ8']['fchange'][1][0],2)}, ⟦p⟧ < .001; β = "
 f"{_r(H['PHQ8']['final']['b'][15],3)}); for life satisfaction, ΔR² = {_r(H['SWLS']['dr2'][1],3)} "
 f"(⟦F⟧(1, 931) = {_f(H['SWLS']['fchange'][1][0],2)}, ⟦p⟧ < .001; β = {_r(H['SWLS']['final']['b'][15],3)}). "
 "Table 8 shows that the LLM score outpredicted the CDS itself in the depressive-symptoms model and retained a coefficient of comparable magnitude for life satisfaction, implying that "
 "narratives carry adjustment-relevant signal that the matching questionnaire does not fully "
 "absorb—consistent with findings that language-based measures capture variance beyond rating "
 "scales {{kjell2022|eichstaedt2018}}."),
('tabcap', 7, 'Hierarchical regressions predicting depressive symptoms (PHQ-8) and life satisfaction (SWLS).'),
('table', t7, T7_W),
('notes',
 'Left panel: PHQ-8; right panel: SWLS (both standardized). Step 1 covariates: gender, age, '
 'education, employment status, log narrative length. *** ⟦p⟧ < .001.'),
('tabcap', 8, 'Focal standardized coefficients in the final (Step 3) models.'),
('table', t8, T8_W),
('notes',
 'Demographic and status covariates included but omitted from the table. β = standardized '
 'coefficient; SE = standard error; df = 931.'),
('p',
 "Classification results converged (Figure 4). A logistic model with demographics and all "
 f"closed-ended scales identified elevated depressive symptoms with AUC = {_r(DL['auc2'],3)} (95% CI "
 f"[{_r(DL['ci2'][0],3)}, {_r(DL['ci2'][1],3)}]); adding the two LLM narrative scores raised AUC to "
 f"{_r(DL['auc1'],3)} [{_r(DL['ci1'][0],3)}, {_r(DL['ci1'][1],3)}] (ΔAUC = {_r(round(DL['auc1'],3)-round(DL['auc2'],3),3)}; "
 f"DeLong ⟦z⟧ = {_f(DL['z'],2)}, ⟦p⟧ = {_p(DL['p'])}). Five-fold cross-validation showed the same "
 f"increment out of sample (AUC {_r(DLCV['auc2'],3)} vs. {_r(DLCV['auc1'],3)}), indicating the gain is "
 "not an overfitting artifact. H3 was supported."),
('figure', 'p3_fig4.png'),
('figcap', 4,
 'Receiver-operating-characteristic curves for identifying elevated depressive symptoms '
 '(PHQ-8 ≥ 10) from questionnaires only versus questionnaires plus LLM narrative scores.'),

# ============================================================ 4. Discussion
('h1', '4. Discussion'),
('h2', '4.1. Principal Findings'),
('p',
 "This study asked whether large language models can turn young adults’ own words about their "
 "careers into psychologically meaningful numbers. Four answers emerged. First, zero-shot LLM "
 "ratings of career distress, employment anxiety, and career confidence behaved like reliable "
 "measurements: virtually deterministic across repeated runs, convergent across two independent "
 "architectures, and in agreement with a human expert panel at the level the human raters "
 "achieved with each other. Second, the ratings displayed the convergent–discriminant structure "
 "that psychometric theory demands, correlating most with their matching constructs and "
 "distinctly less with non-matching ones. Third, narratives contained incremental signal: a "
 "single LLM distress score improved the prediction of depressive symptoms and life satisfaction "
 "beyond six validated questionnaires and measurably sharpened the identification of young "
 "people with elevated depressive symptoms. Fourth, the semantic structure of narrated "
 "difficulty was interpretable and socially patterned, resolving into six themes—from "
 "competitive escalation to meaning loss—whose members differed in adjustment and in structural "
 "position."),
('h2', '4.2. LLMs as Psychometric Instruments'),
('p',
 "The convergent validities observed here (⟦r⟧ ≈ 0.34–0.52; disattenuated up to 0.59) sit "
 "squarely in the range reported when zero-shot GPT ratings are benchmarked against "
 "dictionary-based and fine-tuned pipelines across 15 datasets and multiple languages "
 "{{rathje2024}}, and approach the levels achieved by trained transformer models on well-being "
 "scales {{kjell2022}}. Two features of the present design strengthen the measurement claim. "
 "The dual-model strategy—one proprietary, one open-weight and locally deployable—shows that "
 "the construct signal is not an artifact of a single vendor’s training pipeline, echoing calls "
 "for reproducibility safeguards in LLM-based research {{abdurahman2024|demszky2023}}. And the "
 "ensemble logic of Equation (1) explains an apparent paradox in the reliability results: "
 "averaging six machine ratings suppresses unsystematic error, so the composite can agree with "
 "a two-rater human panel more strongly than two humans agree with each other, exactly as "
 "classical test theory predicts and as crowd-annotation comparisons have found {{gilardi2023}}. "
 "In sensitivity terms, the incremental contribution was modest in variance metrics (ΔR² ≈ "
 "0.01–0.02) yet diagnostic at the decision margin (ΔAUC ≈ 0.02 replicated out of sample)—a "
 "profile typical of useful auxiliary indicators rather than replacement instruments."),
('h2', '4.3. What Young Adults Narrate: Themes and Theory'),
('p',
 "The thematic map gives empirical shape to constructs that career theory has long emphasized. "
 "That narratives—not just symptom levels—differentiate adjustment supports the career "
 "construction claim that vocational identity lives in stories {{savickas2013}}: participants "
 "narrating meaning loss and motivational withdrawal (T5) were markedly worse off than those "
 "narrating equally objective but externally anchored obstacles such as family and place "
 "constraints (T4), even though both groups face real structural pressure. The social patterning "
 "of themes—rural-hukou youth over-represented in place-bound narratives, first-generation "
 "youth in guidance-gap narratives—operationalizes the psychology-of-working insight that "
 "constraint and marginalization shape career experience {{duffy2016}}. The prominence of "
 "competitive-pressure narratives among exam preparers resonates with accounts of involution "
 "and delayed labor-market entry among Chinese youth {{involution|lieflat|ou2022}}, and the "
 "precarity theme tracks the platform-work realities documented in China’s digital economy "
 "{{xiong2024}}. Notably, guidance-gap narratives (T6) describe a remediable deficit: unlike "
 "credential competition, information asymmetry is exactly what career services can address "
 "{{wanberg2020}}."),
('h2', '4.4. Practical Implications'),
('p',
 "For youth career services operating at scale—university career centers, public employment "
 "services, online guidance platforms—the findings sketch a concrete augmentation pathway. "
 "Open-ended intake questions are already common; language-based scoring can convert them into "
 "(a) a triage signal that flags clients whose narratives indicate elevated distress for "
 "priority human follow-up, (b) a thematic router that matches the type of narrated difficulty "
 "to the type of support (e.g., skill-gap clients to training and internship pipelines, T6 "
 "clients to structured guidance and mentoring, T5 clients to counseling rather than yet more "
 "job listings), and (c) an aggregate dashboard tracking how the composition of youth career "
 "difficulty shifts with policy and labor-market conditions—a form of population-level digital "
 "phenotyping {{insel2017}}. Locally deployable open-weight models make this feasible under "
 "strict data-sovereignty requirements {{qwen25}}. Two guardrails follow directly from the "
 "results: scores are screening aids below diagnostic thresholds, and every consequential "
 "decision requires human review, since even well-calibrated ratings misorder individual cases "
 "{{kjell2024|abdurahman2024}}. For AI-assisted career interventions themselves, evidence is "
 "emerging but still preliminary—scoping reviews find mostly small, heterogeneous studies "
 "{{ai_career_rev}}, though early experiments suggest that tools such as ChatGPT can bolster "
 "students’ employment confidence and career readiness {{ai_career_bs}}—reinforcing the "
 "complement-not-replace framing."),
('h2', '4.5. Ethical Considerations'),
('p',
 "Language is more identifying than a Likert response, and career narratives can reveal "
 "employers, families, and health information. The protocol here—explicit consent for AI "
 "processing, removal of identifiers before any model call, a zero-retention agreement for the "
 "proprietary model, and local deployment of the open-weight alternative—illustrates a "
 "practicable floor, not a ceiling {{abdurahman2024}}. Fairness auditing is a further "
 "obligation: rating models may encode dialectal, gender, or class biases in how they read "
 "distress, and the present design cannot fully rule out differential validity across "
 "subgroups. Finally, deploying distress scoring creates a duty of care—flagged individuals "
 "must be routed to qualified support, echoing escalation standards in digital mental-health "
 "research {{demszky2023}}."),
('h2', '4.6. Limitations and Future Directions'),
('p',
 "Several limitations bound the conclusions. First, the design is cross-sectional; the "
 "adjustment differences across themes and the incremental prediction of symptoms are "
 "associations, not causal effects, and reverse influence (distress shaping both narration and "
 "symptom reports) is plausible. Second, the sample, while heterogeneous and quota-guided, is a "
 "non-probability online sample from a single, economically advanced province; generalization "
 "to other regions and to youth without internet access requires caution. Third, narratives "
 "were short (median 155 characters); richer prompts or interview transcripts might raise—or "
 "complicate—validity. Fourth, common-method variance operates on the text side: LLM distress "
 "and human coding read the same words, so their agreement partly reflects shared surface "
 "cues; the questionnaire criteria mitigate but do not eliminate this. Fifth, only two models "
 "and one language were tested, and model updates may drift; versioned prompts and periodic "
 "revalidation are essential {{demszky2023|ziems2024}}. Sixth, the PHQ-8 threshold is a "
 "screening convention, not a clinical diagnosis {{kroenke2009}}. Future work should follow "
 "narrators longitudinally across the school-to-work passage {{vanhooft2021}}, test fairness "
 "across dialects and demographic groups, benchmark newer and smaller models against the "
 "present zero-shot baseline, and embed narrative scoring in randomized evaluations of career "
 "services so that measurement gains can be traced to counseling outcomes {{bankins2024}}."),

# ============================================================ 5. Conclusions
('h1', '5. Conclusions'),
('p',
 "Treating large language models as measurement instruments—and auditing them accordingly—this "
 "study showed that the words Chinese young adults use about their careers can be converted "
 "into reliable, construct-valid, and incrementally informative assessments of career distress. "
 "Narrative-based AI scoring reproduced expert judgment, respected the convergent–discriminant "
 "structure of established questionnaires, added predictive signal beyond an entire battery of "
 "validated scales, and mapped the difficulty landscape of a generation navigating credential "
 "competition, precarious work, place-bound obligations, guidance gaps, and, most consequentially, "
 "struggles of meaning and motivation. For the behavioral sciences, the results support a "
 "methodological fusion in which open-ended language supplements—rather than supplants—"
 "psychometric tradition; for youth employment policy and services, they offer a scalable way to "
 "hear, quantify, and act on what young people are actually saying about their working lives."),

# ============================================================ back matter
('back', 'Supplementary Materials:',
 'The analysis code that reproduces all statistics and figures from the de-identified data is '
 'available from the corresponding author.'),
('back', 'Author Contributions:',
 'Conceptualization, X.C.; methodology, X.C. and D.H.; software, D.H.; formal analysis, D.H. and '
 'T.M.; investigation, T.M.; data curation, T.M.; writing—original draft preparation, X.C. and '
 'D.H.; writing—review and editing, X.C. and T.M.; visualization, D.H.; supervision, X.C.; '
 'project administration, X.C.; funding acquisition, X.C. All authors have read and agreed to '
 'the published version of the manuscript.'),
('back', 'Funding:',
 'This research was funded by the Zhejiang Provincial Philosophy and Social Sciences Planning '
 'Special Project on Higher Education Basic Research Funding Reform (Grant Number: 25NDJC153YBMS) '
 'and the Major Humanities and Social Sciences Research Projects in Zhejiang Higher Education '
 'Institutions (Grant Number: 2024QN018).'),
('back', 'Institutional Review Board Statement:',
 'The study was conducted in accordance with the Declaration of Helsinki and approved by the '
 'Academic Ethics Committee of the College of Business, Jiaxing University (protocol code '
 'JXU-COB-2025-014; approved 16 October 2025).'),
('back', 'Informed Consent Statement:',
 'Informed consent was obtained from all subjects involved in the study, including explicit '
 'consent for de-identified narrative text to be processed by AI systems for research purposes.'),
('back', 'Data Availability Statement:',
 'De-identified quantitative data and analysis code are available from the corresponding author '
 'upon reasonable request. Raw narrative texts are not publicly shared to protect participant '
 'privacy.'),
('back', 'Conflicts of Interest:',
 'The authors declare no conflicts of interest. The funders had no role in the design of the '
 'study; in the collection, analyses, or interpretation of data; in the writing of the '
 'manuscript; or in the decision to publish the results.'),

# ============================================================ Appendix A
('h1', 'Appendix A'),
('h2', 'Appendix A.1. Open-Ended Narrative Prompts (Translated from Chinese)'),
('pni',
 "Prompt 1. “Please describe your current employment or career situation and the biggest "
 "difficulties you are facing. There are no right or wrong answers—please write whatever feels "
 "true to your experience (at least 10 characters).”"),
('pni',
 "Prompt 2. “How do you feel when you think about job seeking and your career future? Please "
 "describe your feelings and thoughts in your own words.”"),
('pni',
 "Prompt 3. “Where would you like your career to be in three years, and what support or help "
 "would make the biggest difference in getting there?”"),
('h2', 'Appendix A.2. LLM Rating Instruction (Translated from Chinese)'),
('pni',
 "“You are an experienced career-psychology rater. Below are three anonymous written answers "
 "from one young adult describing their employment situation, feelings about their career "
 "future, and support needs. Read all three answers together and rate the writer on the "
 "following dimensions, using integers from 1 (extremely low) to 10 (extremely high): (1) "
 "⟦career distress⟧—negative affect about their career situation and prospects; (2) ⟦employment "
 "anxiety⟧—worry, nervousness, or dread connected to job seeking and work; (3) ⟦career "
 "confidence⟧—confidence in their own resources and prospects for career development. Output "
 "strictly as JSON in the format {\"distress\": x, \"anxiety\": x, \"confidence\": x} with no "
 "additional text. Base your ratings only on the text provided.”"),
('pni',
 "Three semantically equivalent Chinese variants of this instruction (identical rubric, "
 "re-ordered sentences and synonyms) defined the three scoring runs per model. Temperature was "
 "0 for all calls; outputs failing JSON validation (0.4% of calls) were re-requested once."),
]
