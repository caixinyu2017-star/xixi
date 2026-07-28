# -*- coding: utf-8 -*-
"""Paper 6 content, part B: Results, Discussion, Conclusions, back matter,
Appendix A. All numbers are read from p6_stats.json."""
import json, os

S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p6_stats.json')))
N = S['n']

def f3(x): return f"{x:.3f}"
def f2(x): return f"{x:.2f}"
def mf(x):
    s = f3(x).replace('-', '−')
    return '0.000' if s == '−0.000' else s

def sig(p):
    return '0.000' if p < 0.0005 else f"{p:.3f}"

def ptxt(p):
    return "⟪p⟫ < 0.001" if p < 0.001 else f"⟪p⟫ = {p:.3f}"

def stars(p):
    if p < 0.001: return ' ***'
    if p < 0.01: return ' **'
    if p < 0.05: return ' *'
    return ''

M = S['models']; MC = S['mancova']; EFA = S['efa']
RY = S['fact_reg_ODA']; RT = S['fact_reg_YMP']
DES = S['descriptives']; COR = S['correlations']
CC = S['cluster_centers']; CA = S['cluster_anova']; GM = S['grand_means']
SIL = S['silhouette']; SILK = S['silhouette_by_k']; CS = S['cluster_sizes']
SUP = S['supplementary']
NAMES4 = ['DLV', 'ADM', 'DPD', 'EDI']
NAMES6 = NAMES4 + ['ODA', 'YMP']

def _corr_cell(a, b):
    key = f'{a}~{b}' if f'{a}~{b}' in COR else f'{b}~{a}'
    r, p = COR[key]
    return f"{r:.3f}{stars(p)}".replace('-0.', '−0.')

_t3 = [['Variable', 'Mean', 'SD', '1', '2', '3', '4', '5']]
for i, nm in enumerate(NAMES6):
    row = [f'{i+1}. {nm}', f2(DES[nm]['mean']), f2(DES[nm]['sd'])]
    for j in range(5):
        row.append(_corr_cell(NAMES6[j], nm) if j < i else '')
    _t3.append(row)

def param_table(nm):
    rows = [['Dependent Variable', 'Parameter', 'B', 'Std. Error', 't', 'Sig.',
             ['95% CI', 'Lower'], ['95% CI', 'Upper'], ['Partial Eta', 'Squared']]]
    for dv in ('ODA', 'YMP'):
        m = M[nm][dv]
        rows.append([dv, 'Intercept', mf(m['B0']), f3(m['SE0']), mf(m['t0']),
                     sig(m['p0']), mf(m['CI0'][0]), mf(m['CI0'][1]), f3(m['eta0'])])
        rows.append(['', nm, mf(m['B1']), f3(m['SE1']), mf(m['t1']), sig(m['p1']),
                     mf(m['CI1'][0]), mf(m['CI1'][1]), f3(m['eta1'])])
    return rows

_pw = [1750, 1300, 1050, 1100, 1000, 900, 950, 950, 1100]

def mv_txt(nm):
    mv = M[nm]['multivariate']
    return (f"Pillai's Trace = {f3(mv['pillai'])}, Wilks' Lambda = {f3(mv['wilks'])}, "
            f"F({mv['df'][0]}, {mv['df'][1]}) = {f3(mv['F'])}, {ptxt(mv['p'])}")

_t8 = [['Model (focal predictor)', "Wilks' Lambda", 'F', 'Sig.',
        ['Adj. B', '(ODA)'], ['Sig.', '(ODA)'], ['Adj. B', '(YMP)'], ['Sig.', '(YMP)']]]
for nm in NAMES4:
    mm = MC[nm]
    _t8.append([nm, f3(mm['wilks']), f3(mm['F']), sig(mm['p']),
                mf(mm['coef']['ODA']['B']), sig(mm['coef']['ODA']['p']),
                mf(mm['coef']['YMP']['B']), sig(mm['coef']['YMP']['p'])])

_ctx_lab = {'lnSIZE': 'Firm size (lnSIZE)', 'AGE': 'Firm age (AGE)',
            'RDI': 'R&D intensity (RDI)', 'DIG': 'Digital-core industry (DIG)'}
_t9 = [['Structural Contextual Variable', 'DLV', 'ADM', 'DPD', 'EDI']]
for ctx in ('lnSIZE', 'AGE', 'RDI', 'DIG'):
    row = [_ctx_lab[ctx]]
    for nm in NAMES4:
        r, p = SUP[ctx][nm]
        cell = f"{r:.3f} ({('p < 0.001' if p < 0.001 else 'p = ' + f'{p:.3f}')})"
        cell = cell.replace('-0.', '−0.').replace('−0.000 ', '0.000 ')
        row.append(cell)
    _t9.append(row)

_t10 = [['Indicator/Statistic', 'Value'],
        ['Kaiser–Meyer–Olkin measure', f3(EFA['KMO'])],
        ["Bartlett's test of sphericity",
         f"χ2 = {f3(EFA['bartlett_chi2'])}; df = {EFA['bartlett_df']}; p < 0.001"],
        ['Extraction method', 'Principal Axis Factoring'],
        ['Number of factors extracted', '1'],
        ['Initial eigenvalue, Factor 1', f3(EFA['eig1'])],
        ['Initial variance explained', f"{EFA['init_var']:.3f}%"],
        ['Extraction sum of squared loadings', f3(EFA['ssl'])],
        ['Variance explained after extraction', f"{EFA['extract_var']:.3f}%"],
        ['Rotation', 'No rotation'],
        ['', ''],
        ['Communalities (initial/extraction); factor loadings', ''],
]
for j, nm in enumerate(NAMES4):
    _t10.append([nm, f"{f3(EFA['communal_init'][j])} / {f3(EFA['communal_extract'][j])};  "
                 f"loading = {f3(EFA['loadings'][j])}"])

def reg_rows(R):
    NB = ' '
    return [
        ['Model', 'R', 'R Square', ['Adjusted', 'R Square'], ['Std. Error of', 'the Estimate'], NB],
        ['1', f3(R['R']), f3(R['R2']), f3(R['adjR2']), f3(R['SEest']), NB],
        ['Model', ['Sum of', 'Squares'], 'df', 'Mean Square', 'F', 'Sig.'],
        [['Regression', 'Residual', 'Total'],
         [f3(R['SSR']), f3(R['SSE']), f3(R['SST'])],
         ['1', str(N - 2), str(N - 1)],
         [f3(R['MSR']), f3(R['MSE']), NB],
         [f3(R['F']), NB, NB], [sig(R['pF']), NB, NB]],
        ['Model', ['Unstandardized', 'Coefficients: B'], ['Std.', 'Error'],
         ['Standardized', 'Coefficients: Beta'], 't', 'Sig.'],
        [['(Constant)', 'FACT_LDC'],
         [f3(R['B0']), mf(R['B1'])], [f3(R['SE0']), f3(R['SE1'])],
         [NB, mf(R['beta'])], [f3(R['t0']), mf(R['t1'])], [sig(R['p0']), sig(R['p1'])]],
    ]

_rw = [2050, 1750, 1300, 1800, 1400, 1300]

_t13 = [['Variable', ['Cluster 1 Mean', f'(n = {CS[0]})'], ['Cluster 2 Mean', f'(n = {CS[1]})'],
         ['Overall', 'Mean'], 'F', 'Sig.']]
for nm in NAMES6:
    _t13.append([nm, f2(CC['cluster1'][nm]), f2(CC['cluster2'][nm]), f2(GM[nm]),
                 f3(CA[nm]['F']), sig(CA[nm]['p'])])

ITEM_TEXT = {
 'DLV': ["Our senior leaders communicate a compelling vision of the firm's digital future.",
         "Top management personally sponsors major digital transformation projects.",
         "Our leaders encourage managers to experiment with digital ways of working.",
         "Senior leadership commits substantial resources to digital initiatives.",
         "Our leaders actively dismantle barriers to digital change.",
         "Digital transformation is a standing item on our top-management agenda."],
 'DPD': ["Key operating indicators are available to decision makers in real time.",
         "Management meetings in this firm start from a shared, data-based picture of the situation.",
         "We digitally track decisions and review their outcomes against data.",
         "Scenario analyses based on data or models inform our major decisions.",
         "When judgment and data conflict, we systematically re-examine the data before deciding."],
 'EDI': ["Employees under 35 are formally represented in our digital transformation committees or councils.",
         "We operate reverse-mentoring arrangements in which young employees advise senior managers on digital topics.",
         "Task forces for transformation projects deliberately include young employees.",
         "Ideas submitted by young employees regularly reach top management through dedicated channels."],
 'ODA': ["We make major decisions quickly compared with competitors.",
         "This firm responds rapidly when market conditions shift.",
         "Decisions here rarely stall while awaiting additional approvals.",
         "We can commit to a course of action under uncertainty and adjust as information arrives.",
         "The quality of our fast decisions is high."],
}
_ta1 = [['Construct', 'Code', 'Item wording (English translation)', 'Loading']]
for con, items in ITEM_TEXT.items():
    for j, it in enumerate(items):
        _ta1.append([con if j == 0 else '', f'{con}{j+1}', it,
                     f3(S['reliability']['item_loadings'][con][j])])

_ADM_DOMAINS = ("demand forecasting; pricing; budgeting and resource allocation; hiring, "
                "staffing, or promotion analytics; production or service scheduling; risk "
                "assessment and compliance; marketing-mix decisions; supply-chain and "
                "inventory decisions; performance monitoring and target setting; and "
                "strategic scenario analysis")

PART_B = [
    ('h1', '4. Results'),

    ('h2', '4.1. Descriptive Statistics and the Association of Decision Practices with Agility '
           'and Young Managerial Presence'),

    ('p', f"Table 3 presents descriptive statistics and correlations. The average firm applies "
     f"AI or advanced analytics in {DES['ADM']['mean']:.2f} of ten managerial decision domains "
     f"(SD = {DES['ADM']['sd']:.2f}), rates its decision agility at {DES['ODA']['mean']:.2f} "
     f"on the five-point scale, and reports that {DES['YMP']['mean']:.2f}% of managerial "
     f"positions (SD = {DES['YMP']['sd']:.2f}) are held by employees aged 35 or younger. The "
     "four practices are positively intercorrelated, and each correlates positively with both "
     "outcomes at the bivariate level—but with strengths that differ sharply across "
     "practice–outcome pairs, foreshadowing the differentiated pattern that the multivariate "
     "models formalize."),

    ('tabcap', 3, 'Descriptive statistics and Pearson correlations (N = 285).'),
    ('table', _t3, [1650, 1100, 1000, 1250, 1250, 1250, 1250, 1250]),
    ('notes', "Source: authors’ calculations. * p < 0.05; ** p < 0.01; *** p < 0.001 "
     "(two-tailed). DLV, DPD, EDI, and ODA are scale means (1–5); ADM is a 0–10 count; YMP "
     "is a percentage."),

    ('p', "The first multivariate model concerns digital transformation leadership "
     f"({mv_txt('DLV')}), the strongest global association among the four. At the univariate "
     f"level, leadership accounts for {100 * M['DLV']['ODA']['eta1']:.0f}% of the variance in "
     f"decision agility (B = {f3(M['DLV']['ODA']['B1'])}, {ptxt(M['DLV']['ODA']['p1'])}) and "
     f"{100 * M['DLV']['YMP']['eta1']:.1f}% of the variance in young managerial presence: one "
     "additional scale point of leadership is associated with "
     f"{M['DLV']['YMP']['B1']:.2f} percentage points more young managers "
     f"({ptxt(M['DLV']['YMP']['p1'])}) (Table 4, Figure 1)."),

    ('tabcap', 4, 'Parameter estimates for the relationship between digital transformation '
                  'leadership and the two outcomes.'),
    ('table', param_table('DLV'), _pw),
    ('notes', f"Source: authors’ calculations. Note: N = {N}. CI = confidence interval."),

    ('figure', 'p6_fig1.png', 5.35, None, 20),
    ('figcap', 1, 'Decision agility and young managerial presence in relation to digital '
                  'transformation leadership. Source: authors’ design.'),

    ('p', f"The second model examines AI-assisted decision-making breadth ({mv_txt('ADM')}). "
     "Here the two outcomes part ways. ADM is strongly associated with agility: each "
     f"additional AI-supported decision domain corresponds to {M['ADM']['ODA']['B1']:.3f} "
     f"scale points of agility ({ptxt(M['ADM']['ODA']['p1'])}, partial ⟪η_{{p}}^{{2}}⟫ = "
     f"{f3(M['ADM']['ODA']['eta1'])}). Its association with young managerial presence, "
     f"however, does not reach the 5% threshold (B = {f3(M['ADM']['YMP']['B1'])}, "
     f"{ptxt(M['ADM']['YMP']['p1'])}) and is treated as marginal: automating the analytics "
     "of deciding is linked to faster firms, but not—by itself—to younger management "
     "(Table 5, Figure 2)."),

    ('tabcap', 5, 'Parameter estimates for the relationship between AI-assisted '
                  'decision-making breadth and the two outcomes.'),
    ('table', param_table('ADM'), _pw),
    ('notes', f"Source: authors’ calculations. Note: N = {N}. CI = confidence interval."),

    ('figure', 'p6_fig2.png', 5.35, None, 21),
    ('figcap', 2, 'Decision agility and young managerial presence in relation to AI-assisted '
                  'decision-making breadth. Source: authors’ design.'),

    ('p', f"The third model addresses decision-process digitalization ({mv_txt('DPD')}). Like "
     "leadership, digitalized decision processes are significantly associated with both "
     f"outcomes: agility (B = {f3(M['DPD']['ODA']['B1'])}, {ptxt(M['DPD']['ODA']['p1'])}, "
     f"partial ⟪η_{{p}}^{{2}}⟫ = {f3(M['DPD']['ODA']['eta1'])}) and young managerial "
     f"presence (B = {M['DPD']['YMP']['B1']:.2f}, {ptxt(M['DPD']['YMP']['p1'])}). Firms "
     "whose meetings begin from shared data and whose decisions are reviewed against "
     "outcomes are both faster and younger at the management level (Table 6, Figure 3)."),

    ('tabcap', 6, 'Parameter estimates for the relationship between decision-process '
                  'digitalization and the two outcomes.'),
    ('table', param_table('DPD'), _pw),
    ('notes', f"Source: authors’ calculations. Note: N = {N}. CI = confidence interval."),

    ('figure', 'p6_fig3.png', 5.35, None, 22),
    ('figcap', 3, 'Decision agility and young managerial presence in relation to '
                  'decision-process digitalization. Source: authors’ design.'),

    ('p', f"The final model concerns young-employee decision involvement ({mv_txt('EDI')}), "
     "and it mirrors the AI model in reverse. Involvement is the practice most strongly "
     f"associated with young managerial presence: one scale point corresponds to "
     f"{M['EDI']['YMP']['B1']:.2f} percentage points more young managers "
     f"({ptxt(M['EDI']['YMP']['p1'])}, partial ⟪η_{{p}}^{{2}}⟫ = "
     f"{f3(M['EDI']['YMP']['eta1'])}), the strongest association with young managerial "
     "presence among the four practices. Its "
     f"association with agility is positive but only marginal (B = "
     f"{f3(M['EDI']['ODA']['B1'])}, {ptxt(M['EDI']['ODA']['p1'])}), consistent with the "
     "theoretical ambivalence of participation for decision speed (Table 7, Figure 4)."),

    ('tabcap', 7, 'Parameter estimates for the relationship between young-employee decision '
                  'involvement and the two outcomes.'),
    ('table', param_table('EDI'), _pw),
    ('notes', f"Source: authors’ calculations. Note: N = {N}. CI = confidence interval."),

    ('figure', 'p6_fig4.png', 5.35, None, 23),
    ('figcap', 4, 'Decision agility and young managerial presence in relation to '
                  'young-employee decision involvement. Source: authors’ design.'),

    ('p', "In sum, the four models describe a division of labor among practices: leadership "
     "and digitalized decision processes travel with both outcomes; AI-assisted "
     "decision-making travels with agility but only marginally with young management; and "
     "youth involvement travels with young management but only marginally with agility. H1 "
     "is therefore partially supported. Diagnostics are unremarkable: Shapiro–Wilk tests do "
     "not reject residual normality in any specification (all "
     f"⟪p⟫ ≥ {min(v[k] for v in S['resid_normality'].values() for k in ('ODA_p','YMP_p')):.3f}), "
     f"and the largest Cook's distance is {S['max_cooks']:.3f}."),

    ('h2', '4.2. Robustness: Covariate Adjustment and Structural Correlates'),

    ('p', "Table 8 reports MANCOVA re-estimations with firm size, firm age, R&D intensity, "
     "and the digital-core indicator as covariates. The multivariate association of every "
     "practice survives adjustment, and the coefficient pattern is intact: DLV and DPD "
     "remain significant for both outcomes, ADM for agility, and EDI for young managerial "
     "presence. The two marginal associations shift slightly in opposite directions—the "
     f"adjusted ADM–YMP association remains marginal ({ptxt(MC['ADM']['coef']['YMP']['p'])}), "
     f"while the adjusted EDI–ODA association crosses the 5% threshold "
     f"({ptxt(MC['EDI']['coef']['ODA']['p'])})—so both should be read as borderline rather "
     "than established. Supplementary correlations (Table 9) show that the practices are "
     "essentially unrelated to firm age, R&D intensity, and the digital-core indicator, "
     "with only a modest positive correlation between leadership and firm size; the "
     "practice constructs are thus not proxies for structural position; the covariate-adjusted models nevertheless anchor our "
     "conclusions."),

    ('tabcap', 8, 'Covariate-adjusted (MANCOVA) estimates for the four practices.'),
    ('table', _t8, [1900, 1300, 950, 950, 1150, 950, 1150, 950]),
    ('notes', "Source: authors’ calculations. Covariates: lnSIZE, AGE, RDI, DIG. Adj. B = "
     "adjusted unstandardized coefficient of the focal predictor; multivariate statistics "
     "are Wilks’ Lambda F-tests for the focal predictor."),

    ('tabcap', 9, 'Supplementary bivariate correlations of the practices with structural '
                  'contextual variables.'),
    ('table', _t9, [2750, 1720, 1720, 1720, 1720]),
    ('notes', "Source: authors’ calculations. Pearson correlation coefficients with p-values "
     "in parentheses. N = 285."),

    ('h2', '4.3. The Latent Leadership–Decision Configuration and Its Association with the '
           'Two Outcomes'),

    ('p', f"Factor-analytic prerequisites are met (KMO = {f3(EFA['KMO'])}; Bartlett's "
     f"χ2({EFA['bartlett_df']}) = {f3(EFA['bartlett_chi2'])}, ⟪p⟫ < 0.001), and Principal "
     f"Axis Factoring retains a single factor whose initial eigenvalue "
     f"({f3(EFA['eig1'])}) accounts for {EFA['init_var']:.1f}% of total variance, with "
     f"{EFA['extract_var']:.1f}% explained after extraction (Table 10). The loading "
     "hierarchy is informative. Digital transformation leadership "
     f"({f3(EFA['loadings'][0])}) and decision-process digitalization "
     f"({f3(EFA['loadings'][2])}) anchor the configuration; AI-assisted decision breadth "
     f"({f3(EFA['loadings'][1])}) and youth involvement ({f3(EFA['loadings'][3])}) load "
     "substantially but carry the lowest communalities "
     f"({f3(EFA['communal_extract'][1])} and {f3(EFA['communal_extract'][3])}). The "
     "configuration's core, in other words, is managerial rather than technological or "
     "participative: tools and voice are attached to it without being reducible to it. The "
     "factor is labelled ⟪FACT_LDC⟫, the leadership–decision configuration."),

    ('tabcap', 10, 'Exploratory factor analysis of the leadership and decision-making '
                   'practice indicators.'),
    ('table', _t10, [4820, 4820]),
    ('notes', "Source: authors’ calculations. Principal Axis Factoring on the correlation "
     "matrix of DLV, ADM, DPD, and EDI; one factor retained; factor scores by the "
     "regression method."),

    ('p', f"Regressions of the outcomes on the factor scores support H2. For decision "
     f"agility, the model yields R = {f3(RY['R'])} and ⟪R^{{2}}⟫ = {f3(RY['R2'])} "
     f"(adjusted ⟪R^{{2}}⟫ = {f3(RY['adjR2'])}; F = {f3(RY['F'])}, ⟪p⟫ < 0.001): one "
     f"standard deviation of the configuration corresponds to {RY['B1']:.3f} scale points "
     f"of agility (β = {f3(RY['beta'])}) (Table 11). For young managerial presence, the "
     f"association is smaller but clearly significant (R = {f3(RT['R'])}; ⟪R^{{2}}⟫ = "
     f"{f3(RT['R2'])}; F = {f3(RT['F'])}, ⟪p⟫ < 0.001), with one standard deviation of the "
     f"configuration corresponding to {RT['B1']:.2f} percentage points more young managers "
     f"(β = {f3(RT['beta'])}) (Table 12). The leadership–decision configuration is thus "
     "systematically related to both the tempo and the generational profile of enterprise "
     "decision systems, although it accounts for a considerably larger share of the "
     "variance in agility than in advancement."),

    ('tabcap', 11, 'Regression results for the relationship between the leadership–decision '
                   'configuration factor and organizational decision agility.'),
    ('table', reg_rows(RY), _rw, 'norepeat'),
    ('notes', "Source: authors’ calculations. Dependent variable: ODA. Predictor: factor "
     "scores of FACT_LDC (standardized)."),

    ('tabcap', 12, 'Regression results for the relationship between the leadership–decision '
                   'configuration factor and young managerial presence.'),
    ('table', reg_rows(RT), _rw, 'norepeat'),
    ('notes', "Source: authors’ calculations. Dependent variable: YMP. Predictor: factor "
     "scores of FACT_LDC (standardized)."),

    ('h2', '4.4. Two Decision Regimes: Cluster Typologies of Practice, Agility, and '
           'Managerial Rejuvenation'),

    ('p', "Ward-linkage hierarchical clustering of the six standardized variables suggests a "
     "two-group structure (Figure 5), and the k-means comparison concurs: the average "
     f"silhouette coefficient is highest for k = 2 ({f3(SILK['2'])} versus "
     f"{f3(SILK['3'])} for k = 3 and {f3(SILK['4'])} for k = 4), and the hierarchical and "
     f"k-means partitions coincide for {S['hier_km_agreement_pct']:.1f}% of firms. The "
     "typology is exploratory and descriptive, not a definitive classification."),

    ('figure', 'p6_fig5.png', 5.5, None, 24),
    ('figcap', 5, 'Dendrogram of the hierarchical clustering of firms based on decision '
                  'practices, agility, and young managerial presence (Ward linkage, '
                  'truncated to the last 34 merges). Source: authors’ design.'),

    ('p', f"Table 13 contrasts the two regimes. The agile, digitally led regime "
     f"(n = {CS[0]}) combines strong leadership ({f2(CC['cluster1']['DLV'])}), broad "
     f"AI-assisted deciding ({f2(CC['cluster1']['ADM'])} of ten domains), digitalized "
     f"processes ({f2(CC['cluster1']['DPD'])}), and institutionalized youth involvement "
     f"({f2(CC['cluster1']['EDI'])}) with high agility ({f2(CC['cluster1']['ODA'])}) and a "
     f"young management corps ({f2(CC['cluster1']['YMP'])}% of managerial positions). The "
     f"conventional hierarchical regime (n = {CS[1]}) sits markedly lower on every practice "
     f"({f2(CC['cluster2']['DLV'])}, {f2(CC['cluster2']['ADM'])}, "
     f"{f2(CC['cluster2']['DPD'])}, {f2(CC['cluster2']['EDI'])}), decides more slowly "
     f"({f2(CC['cluster2']['ODA'])}), and promotes fewer young people "
     f"({f2(CC['cluster2']['YMP'])}%). Strikingly, the regimes barely differ in sectoral "
     f"composition—digital-core firms make up {S['cluster_sector_pct']['cluster1']['digital-core']:.1f}% "
     f"of the first and {S['cluster_sector_pct']['cluster2']['digital-core']:.1f}% of the "
     "second, with manufacturing the plurality in both—indicating that decision regimes are "
     "chosen, not sectorally determined."),

    ('p', f"The average silhouette coefficient of the final solution is {f3(SIL['avg'])} "
     f"({f3(SIL['c1'])} and {f3(SIL['c2'])} for the two clusters), indicating modest but "
     "coherent separation appropriate for an exploratory typology. The ANOVA statistics in "
     "Table 13 describe the between-regime differences; because the clusters were built "
     "from the same variables, these F values characterize rather than test the "
     "separation. With that caveat, the practices—led by leadership itself—separate the "
     "regimes most strongly, and both outcomes differ substantially. Overall, the cluster "
     "analysis supports H3: leadership and decision-making practices, agility, and the "
     "generational profile of management cohere into recognizable socio-technical decision "
     "regimes."),

    ('tabcap', 13, 'Cluster centers and differences between clusters (ANOVA).'),
    ('table', _t13, [1500, 1900, 1900, 1400, 1500, 1440]),
    ('notes', f"Source: authors’ calculations. k-means with k = 2 on standardized variables; "
     f"means reported in original units. ANOVA df = ({CA['DLV']['df1']}, "
     f"{CA['DLV']['df2']}); F values are descriptive (see text)."),

    ('h1', '5. Discussion'),

    ('p', "Read together, the three analytical stages tell a consistent story: in the "
     "enterprises of China's most digitalized macro-region, how leaders decide and whom "
     "they let decide are bound up with how fast the organization moves and how young its "
     "management is. The associations are cross-sectional and must not be read causally; "
     "agile, youthful firms may adopt the practices as readily as the practices may "
     "produce agility and youth, and unobserved quality of management may drive both "
     "{{tmt_age_digital|teece}}. What the data do establish is a systematic co-occurrence "
     "that variable-by-variable research would have missed."),

    ('p', "The differentiated support for H1 sharpens several literatures. That digital "
     "transformation leadership and digitalized decision processes accompany both agility "
     "and rejuvenation extends the digital-leadership literature {{dl1|dl2|dl4}} beyond its "
     "usual performance outcomes, and gives micro-level content to the finding that younger "
     "executive cohorts and digital transformation go together {{tmt_age_digital|upper1}}. "
     "The asymmetry between the AI and involvement models is the study's most instructive "
     "result. Broad AI-assisted deciding is linked to speed—consistent with experimental "
     "evidence on algorithmic decision support {{csaszar_ai|genai2|aidm1}}—but not, on its "
     "own, to a younger managerial corps; conversely, institutionalized youth involvement "
     "is linked to a younger corps but only marginally to speed {{voice_part|"
     "reverse_mentor}}. Technology and participation thus appear as complements with "
     "different comparative advantages, exactly as the socio-technical tradition would "
     "predict {{sts1|sts2|sts_ai}}: the technical subsystem accelerates, the social "
     "subsystem renews, and neither substitutes for the other."),

    ('p', "The factor analysis qualifies the configuration argument in an important way. A "
     "single leadership–decision configuration exists, supports H2, and predicts both "
     "outcomes; but its core is carried by leadership and process digitalization, while AI "
     "breadth and youth involvement are its least redundant elements. Practically, this "
     "means the configuration cannot be inferred from a firm's AI inventory or its "
     "participation rhetoric alone {{shrestha2019|vial2019}}. Theoretically, it locates the "
     "'engine' of the configuration in managerial practice, echoing dynamic-capabilities "
     "arguments that orchestration, not assets, differentiates firms {{teece|"
     "upper_digital}}. The cluster analysis then shows that this configuration is lived as "
     "a regime: firms are either broadly in or broadly out, sector notwithstanding, and "
     "the two regimes differ in managerial age structure by more than six percentage "
     "points {{kmeans_biz|stsd2}}. That the regimes cut across sectors within one "
     "macro-region suggests organizational choice, not environment, as the proximate "
     "differentiator {{ses_regional|digital_sme}}."),

    ('h2', '5.1. Theoretical Implications'),

    ('p', "Three implications follow for theory. First, for upper echelons research, the "
     "results extend the theory's outcome space: leadership orientations are imprinted not "
     "only on strategy and performance but on the demography of the managerial pipeline "
     "itself {{upper1|upper2|young_promotion}}. Second, for the decision-making literature, "
     "decision agility emerges as a property of configurations—leadership, process, tools, "
     "and participation jointly—rather than of structures alone, refining classic "
     "speed-of-decision arguments {{eisenhardt1989|baum2003}} for the AI era "
     "{{shrestha2019|csaszar_ai}}. Third, for socio-technical systems theory, the "
     "complementary asymmetry documented here (technology speeds, participation renews) "
     "offers a concrete, falsifiable instance of joint optimization in contemporary "
     "decision systems {{sts_ai|stsd1}}."),

    ('h2', '5.2. Practical Implications'),

    ('p', "For executives navigating digital transformation, the message is compositional. "
     "Firms seeking agility should extend AI-assisted deciding across managerial domains "
     "and digitalize the decision process itself; firms seeking to renew their management "
     "ranks should institutionalize youth involvement—councils, reverse mentoring, "
     "cross-level task forces—rather than expect rejuvenation to follow from technology "
     "{{reverse_mentor|budhwar2023}}. Because the two marginal associations were "
     "borderline, neither shortcut is reliable: AI without involvement leaves the ladder "
     "unchanged, and involvement without digitalized process leaves speed on the table. "
     "For young professionals, the regime typology offers a screening heuristic: firms "
     "that decide from data and include the young in transformation governance are also "
     "the firms where young people reach management {{genz_work|china_newgen}}. For "
     "policy-makers concerned with youth career development, demand-side instruments—"
     "recognizing youth decision-involvement practices in talent-program criteria, or "
     "diffusing digital decision infrastructure to SMEs—complement conventional supply-side "
     "training {{talent|digital_sme|ilo1|ilo2}}."),

    ('h2', '5.3. Limitations and Further Research'),

    ('p', "Several constraints bound the findings. The cross-sectional design precludes "
     "causal claims; longitudinal designs tracking regime shifts and subsequent agility "
     "and promotion outcomes are the natural next step. Practices and agility share one "
     "informant, and although the second outcome is a reported statistic, common-method "
     "checks were passed, and the differentiated pattern resists a single-factor "
     "explanation, multi-informant or archival replication would strengthen inference "
     "{{podsakoff2003|podsakoff2024|textmeasure1}}. Young managerial presence is a stock indicator that "
     "conflates promotion, hiring, and attrition flows; personnel-record data could "
     "decompose it {{young_promotion}}. The Yangtze River Delta is a revealing but "
     "advanced setting, and the regime structure may differ where digital infrastructure "
     "is thinner {{digital_sme}}. Finally, the factor and cluster analyses are "
     "exploratory: the one-factor solution is a first approximation, the modest silhouette "
     "values counsel restraint, and alternative clustering specifications should be tested "
     "{{rousseeuw|jain|kmeans_biz}}. Extending the design to decision quality, error "
     "rates, and the career trajectories of the young managers themselves would deepen "
     "the link between decision systems and youth career development {{career1|career2}}."),

    ('h1', '6. Conclusions'),

    ('p', "This study asked how the leadership and decision-making practices of digitally "
     "transforming enterprises relate to two properties of today's enterprise systems: the "
     "agility of organizational decisions and the advancement of young people into "
     "management. Drawing on an executive survey of 285 firms in the Yangtze River Delta "
     "and combining MANOVA-type models, exploratory factor analysis, and cluster analysis, "
     "it provides a system-level description of how transformation is steered—and by "
     "whom—inside firms. All findings are exploratory associations rather than causal "
     "effects."),

    ('p', "Three conclusions stand out. First, the practices divide their labor: "
     "transformation leadership and digitalized decision processes accompany both agility "
     "and managerial rejuvenation, whereas broad AI-assisted deciding accompanies agility "
     "only, and institutionalized youth involvement accompanies rejuvenation only, each "
     "showing merely marginal associations with the other outcome. Second, a single "
     "leadership–decision configuration underlies the four practices—anchored in "
     "leadership and process, not in tools or rhetoric—and is significantly associated "
     "with both outcomes. Third, firms occupy one of two socio-technical decision regimes, "
     "agile-and-young versus conventional-and-senior, and the divide runs through sectors "
     "rather than between them."),

    ('p', "For the navigation of digital transformation, these results counsel against "
     "equating transformation with technology and against expecting any single practice to "
     "deliver the whole configuration. Leadership that digitalizes how decisions are made, "
     "extends analytical support across decision domains, and deliberately seats young "
     "employees at the decision table is associated with enterprises that are at once "
     "faster and generationally renewed. Future research should establish the causal "
     "structure of this configuration, trace the careers of the young managers it "
     "surfaces, and test whether the two-regime topology generalizes beyond advanced "
     "digital regions."),

    ('back', 'Author Contributions:', "Conceptualization, X.C. and T.M.; methodology, X.C.; "
     "software, X.C.; validation, X.C., D.H. and T.M.; formal analysis, X.C.; "
     "investigation, D.H.; resources, T.M.; data curation, D.H.; writing—original draft "
     "preparation, X.C.; writing—review and editing, T.M.; visualization, D.H.; "
     "supervision, T.M.; project administration, T.M.; funding acquisition, X.C. All "
     "authors have read and agreed to the published version of the manuscript."),

    ('back', 'Funding:', "This research was funded by the Zhejiang Provincial Philosophy and "
     "Social Sciences Planning Special Project on Higher Education Basic Research Funding "
     "Reform (Grant Number: 25NDJC153YBMS) and the Major Humanities and Social Sciences "
     "Research Projects in Zhejiang Higher Education Institutions (Grant Number: "
     "2024QN018)."),

    ('back', 'Institutional Review Board Statement:', "The study was conducted in "
     "accordance with the Declaration of Helsinki and approved by the Academic Ethics "
     "Committee of the College of Business, Jiaxing University (protocol code "
     "JXU-BUS-2026-021, approved on 2 March 2026)."),

    ('back', 'Informed Consent Statement:', "Informed consent was obtained from all "
     "respondents involved in the study."),

    ('back', 'Data Availability Statement:', "The data presented in this study are "
     "available on request from the corresponding author due to confidentiality "
     "commitments made to participating firms. The analysis code is available from the "
     "authors upon reasonable request."),

    ('back', 'Conflicts of Interest:', "The authors declare no conflicts of interest."),

    ('h1', 'Abbreviations'),
    ('p', "The following abbreviations are used in this manuscript:"),
    ('table', [
        ['Abbreviation', 'Definition'],
        ['DLV', 'Digital transformation leadership'],
        ['ADM', 'AI-assisted decision-making breadth'],
        ['DPD', 'Decision-process digitalization'],
        ['EDI', 'Young-employee decision involvement'],
        ['ODA', 'Organizational decision agility'],
        ['YMP', 'Young managerial presence (% of managerial positions held by employees ≤35)'],
        ['FACT_LDC', 'Latent leadership–decision configuration factor'],
        ['AI', 'Artificial intelligence'],
        ['EFA', 'Exploratory factor analysis'],
        ['PAF', 'Principal Axis Factoring'],
        ['KMO', 'Kaiser–Meyer–Olkin measure of sampling adequacy'],
        ['MANOVA/MANCOVA', 'Multivariate analysis of (co)variance'],
        ['CI', 'Confidence interval'],
        ['RDI', 'R&D intensity'],
        ['SME', 'Small and medium-sized enterprise'],
        ['TMT', 'Top management team'],
    ], [2600, 7040]),

    ('h1', 'Appendix A'),

    ('p', "Table A1 lists the measurement items of the four reflective constructs and their "
     "standardized loadings from within-construct Principal Axis Factoring. Items were "
     "administered in Chinese on five-point Likert scales after translation and "
     "back-translation {{brislin1970}}."),

    ('tabcap', 'A1', 'Measurement items and standardized factor loadings.'),
    ('table', _ta1, [1300, 900, 6100, 1340]),
    ('notes', "Source: authors’ design. Loadings from within-construct Principal Axis "
     "Factoring (N = 285)."),

    ('p', "The AI-assisted decision-making breadth (ADM) index asked whether AI or advanced "
     "analytics tools support each of the following ten managerial decision domains: "
     f"{_ADM_DOMAINS}. The index counts the domains marked."),
]
