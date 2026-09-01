# -*- coding: utf-8 -*-
"""Paper 5 content, part B: Results, Discussion, Conclusions, back matter,
Appendix A. All numbers are read from p5_stats.json."""
import json, os

S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5_stats.json')))
N = S['n']

def f3(x):
    return f"{x:.3f}"

def f2(x):
    return f"{x:.2f}"

def sig(p):
    """SPSS-style Sig. cell value."""
    return '0.000' if p < 0.0005 else f"{p:.3f}"

def ptxt(p):
    """In-text p: 'p < 0.001' or 'p = 0.074' (leading zeros, exemplar style)."""
    return "⟪p⟫ < 0.001" if p < 0.001 else f"⟪p⟫ = {p:.3f}"

def stars(p):
    if p < 0.001: return ' ***'
    if p < 0.01: return ' **'
    if p < 0.05: return ' *'
    return ''

M = S['models']
MC = S['mancova']
EFA = S['efa']
RY = S['fact_reg_YES']
RT = S['fact_reg_YTR']
DES = S['descriptives']
COR = S['correlations']
CC = S['cluster_centers']
CA = S['cluster_anova']
GM = S['grand_means']
SIL = S['silhouette']
SILK = S['silhouette_by_k']
CS = S['cluster_sizes']
SUP = S['supplementary']
NAMES4 = ['DTL', 'DDM', 'AIA', 'DST']
NAMES6 = NAMES4 + ['YES', 'YTR']
LONG = {'DTL': 'digital transformation leadership',
        'DDM': 'data-driven decision-making',
        'AIA': 'AI application breadth',
        'DST': 'digital skills training'}

# ------------------------------------------------- Table 3: descriptives+corr
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

# --------------------------------------------- Tables 4-7: parameter estimates
def mf(x):
    """3-dp with typographic minus."""
    return f3(x).replace('-', '−')

def param_table(nm):
    rows = [['Dependent Variable', 'Parameter', 'B', 'Std. Error', 't', 'Sig.',
             ['95% CI', 'Lower'], ['95% CI', 'Upper'], ['Partial Eta', 'Squared']]]
    for dv in ('YES', 'YTR'):
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

# ------------------------------------------------- Table 8: MANCOVA robustness
_t8 = [['Model (focal predictor)', "Wilks' Lambda", 'F', 'Sig.',
        ['Adj. B', '(YES)'], ['Sig.', '(YES)'], ['Adj. B', '(YTR)'], ['Sig.', '(YTR)']]]
for nm in NAMES4:
    mm = MC[nm]
    _t8.append([nm, f3(mm['wilks']), f3(mm['F']), sig(mm['p']),
                mf(mm['coef']['YES']['B']), sig(mm['coef']['YES']['p']),
                mf(mm['coef']['YTR']['B']), sig(mm['coef']['YTR']['p'])])

# ------------------------------------------- Table 9: supplementary correlations
_ctx_lab = {'lnSIZE': 'Firm size (lnSIZE)', 'AGE': 'Firm age (AGE)',
            'RDI': 'R&D intensity (RDI)', 'DIG': 'Digital-core industry (DIG)'}
_t9 = [['Structural Contextual Variable', 'DTL', 'DDM', 'AIA', 'DST']]
for ctx in ('lnSIZE', 'AGE', 'RDI', 'DIG'):
    row = [_ctx_lab[ctx]]
    for nm in NAMES4:
        r, p = SUP[ctx][nm]
        row.append(f"{r:.3f} ({('p < 0.001' if p < 0.001 else 'p = ' + f'{p:.3f}')})"
                   .replace('-0.', '−0.'))
    _t9.append(row)

# ------------------------------------------------------------ Table 10: EFA
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

# ------------------------------------------- Tables 11-12: factor regressions
def reg_rows(R):
    b1 = f3(R['B1']).replace('-', '−')
    beta = f3(R['beta']).replace('-', '−')
    t1 = f3(R['t1']).replace('-', '−')
    NB = ' '   # placeholder keeping full line height
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
        [['(Constant)', 'FACT_DLDM'],
         [f3(R['B0']), b1], [f3(R['SE0']), f3(R['SE1'])],
         [NB, beta], [f3(R['t0']), t1], [sig(R['p0']), sig(R['p1'])]],
    ]

_rw = [2050, 1750, 1300, 1800, 1400, 1300]

# ---------------------------------------- Table 13: cluster centers + ANOVA
_t13 = [['Variable', ['Cluster 1 Mean', f'(n = {CS[0]})'], ['Cluster 2 Mean', f'(n = {CS[1]})'],
         ['Overall', 'Mean'], 'F', 'Sig.']]
for nm in NAMES6:
    _t13.append([nm, f2(CC['cluster1'][nm]), f2(CC['cluster2'][nm]), f2(GM[nm]),
                 f3(CA[nm]['F']), sig(CA[nm]['p'])])

# ---------------------------------------------------------- Appendix Table A1
ITEM_TEXT = {
 'DTL': ["Our top managers communicate a clear vision of the firm's digital future.",
         "Senior leaders personally champion major digital initiatives.",
         "Leaders in this firm encourage experimentation with new digital tools.",
         "Our executives allocate sufficient resources to digital transformation.",
         "Senior managers actively remove obstacles to digital ways of working.",
         "Our leadership team keeps digital transformation on the strategic agenda."],
 'DDM': ["Major operational decisions in this firm are based on data analysis.",
         "We routinely use data dashboards or analytics when making market decisions.",
         "Decisions about people (hiring, staffing, promotion) draw on HR data and metrics.",
         "When opinions differ, data usually settles the argument in this firm.",
         "We evaluate the outcomes of past decisions with quantitative indicators."],
 'DST': ["This firm provides systematic training in digital skills.",
         "Young employees receive priority access to digital upskilling programs.",
         "Employees are given work time to learn new digital tools.",
         "Digital training in this firm is updated as new technologies are adopted."],
}
_ta1 = [['Construct', 'Code', 'Item wording (English translation)', 'Loading']]
for con, items in ITEM_TEXT.items():
    for j, it in enumerate(items):
        _ta1.append([con if j == 0 else '', f'{con}{j+1}', it,
                     f3(S['reliability']['item_loadings'][con][j])])

_AIA_FUNCS = ("customer service (chatbots or virtual assistants); recruitment and résumé "
              "screening; marketing content generation or targeting; sales forecasting; "
              "production scheduling or process optimization; quality inspection (machine "
              "vision); logistics and inventory optimization; financial analysis or risk "
              "control; internal knowledge search or office copilots; and product or R&D "
              "design assistance")

# ===================================================================== PART B
_dtl_mv = M['DTL']['multivariate']
_h_agree = S['hier_km_agreement_pct']

PART_B = [
    ('h1', '4. Results'),

    ('h2', '4.1. Descriptive Statistics and Cross-Sectional Relationships Between Digital '
           'Practices and Youth-Employment Outcomes'),

    ('p', f"Table 3 reports descriptive statistics and Pearson correlations for the six focal "
     f"variables. The average firm employs {DES['YES']['mean']:.2f}% young workers "
     f"(SD = {DES['YES']['sd']:.2f}) and reports a youth turnover rate of "
     f"{DES['YTR']['mean']:.2f}% (SD = {DES['YTR']['sd']:.2f}). The four practice indicators "
     "are positively and significantly intercorrelated (r between "
     f"{min(COR[k][0] for k in ('DTL~DDM','DTL~AIA','DTL~DST','DDM~AIA','DDM~DST','AIA~DST')):.3f} "
     f"and {max(COR[k][0] for k in ('DTL~DDM','DTL~AIA','DTL~DST','DDM~AIA','DDM~DST','AIA~DST')):.3f}), "
     "consistent with the expectation that they express a shared organizational orientation "
     "while remaining empirically distinguishable. All four practices correlate positively "
     "with the youth employee share and negatively with youth turnover at the bivariate "
     "level, although with clearly different strengths."),

    ('tabcap', 3, 'Descriptive statistics and Pearson correlations (N = 308).'),
    ('table', _t3, [1650, 1100, 1000, 1250, 1250, 1250, 1250, 1250]),
    ('notes', "Source: authors’ calculations. * p < 0.05; ** p < 0.01; *** p < 0.001 "
     "(two-tailed). DTL, DDM, and DST are scale means (1–5); AIA is a 0–10 count; YES and YTR "
     "are percentages."),

    ('p', "The first multivariate model analyzed the association between digital "
     "transformation leadership (DTL) and the two youth-employment outcomes. The multivariate "
     f"tests indicate a significant global association ({mv_txt('DTL')}), the strongest among "
     "the four practice dimensions. At the univariate level, DTL is associated with "
     f"approximately {100 * M['DTL']['YES']['eta1']:.0f}% of the cross-sectional variance in "
     f"the youth employee share and {100 * M['DTL']['YTR']['eta1']:.0f}% of the variation in "
     "youth turnover. A one-point increase on the five-point leadership scale is associated "
     f"with a {M['DTL']['YES']['B1']:.3f}-percentage-point higher youth share "
     f"({ptxt(M['DTL']['YES']['p1'])}) and a {abs(M['DTL']['YTR']['B1']):.3f}-point lower "
     f"youth turnover rate ({ptxt(M['DTL']['YTR']['p1'])}) (Table 4). Figure 1 displays the "
     "two associations; both scatters show the wide dispersion typical of firm-level survey "
     "data, with clearly sloped linear fits."),

    ('tabcap', 4, 'Parameter estimates for the relationship between digital transformation '
                  'leadership and youth-employment outcomes.'),
    ('table', param_table('DTL'), _pw),
    ('notes', f"Source: authors’ calculations. Note: N = {N}. CI = confidence interval."),

    ('figure', 'p5_fig1.png', 5.35, None, 20),
    ('figcap', 1, 'Youth employee share and youth turnover rate in relation to digital '
                  'transformation leadership. Source: authors’ design.'),

    ('p', "The second model evaluated data-driven decision-making (DDM). The multivariate "
     f"effect remains significant ({mv_txt('DDM')}). DDM is positively associated with the "
     f"youth employee share (B = {M['DDM']['YES']['B1']:.3f}, {ptxt(M['DDM']['YES']['p1'])}, "
     f"partial ⟪η_{{p}}^{{2}}⟫ = {f3(M['DDM']['YES']['eta1'])}) and negatively with youth "
     f"turnover (B = −{abs(M['DDM']['YTR']['B1']):.3f}, {ptxt(M['DDM']['YTR']['p1'])}, "
     f"partial ⟪η_{{p}}^{{2}}⟫ = {f3(M['DDM']['YTR']['eta1'])}) (Table 5, Figure 2). "
     "Analytics-intensive decision environments thus co-occur with both a younger workforce "
     "and greater retention of young employees."),

    ('tabcap', 5, 'Parameter estimates for the relationship between data-driven '
                  'decision-making and youth-employment outcomes.'),
    ('table', param_table('DDM'), _pw),
    ('notes', f"Source: authors’ calculations. Note: N = {N}. CI = confidence interval."),

    ('figure', 'p5_fig2.png', 5.35, None, 21),
    ('figcap', 2, 'Youth employee share and youth turnover rate in relation to data-driven '
                  'decision-making. Source: authors’ design.'),

    ('p', "The third model, centered on AI application breadth (AIA), reveals the most "
     f"differentiated pattern ({mv_txt('AIA')}). AIA is significantly associated with lower "
     f"youth turnover (B = −{abs(M['AIA']['YTR']['B1']):.3f}, {ptxt(M['AIA']['YTR']['p1'])}, "
     f"partial ⟪η_{{p}}^{{2}}⟫ = {f3(M['AIA']['YTR']['eta1'])}): each additional AI-enabled "
     "function is associated with roughly three-quarters of a percentage point less youth "
     "churn. By contrast, its association with the youth employee share does not reach the "
     f"conventional 5% significance threshold (B = {M['AIA']['YES']['B1']:.3f}, "
     f"{ptxt(M['AIA']['YES']['p1'])}) and can only be interpreted as marginal at the 10% "
     "level; it is therefore treated cautiously. Deploying AI widely, in other words, is "
     "associated with keeping young employees but not, by itself, with employing more of them "
     "(Table 6, Figure 3)."),

    ('tabcap', 6, 'Parameter estimates for the relationship between AI application breadth '
                  'and youth-employment outcomes.'),
    ('table', param_table('AIA'), _pw),
    ('notes', f"Source: authors’ calculations. Note: N = {N}. CI = confidence interval."),

    ('figure', 'p5_fig3.png', 5.35, None, 22),
    ('figcap', 3, 'Youth employee share and youth turnover rate in relation to AI '
                  'application breadth. Source: authors’ design.'),

    ('p', "The final model investigated digital skills training (DST). The multivariate test "
     f"remains significant ({mv_txt('DST')}). DST shows a strong positive association with "
     f"the youth employee share (B = {M['DST']['YES']['B1']:.3f}, "
     f"{ptxt(M['DST']['YES']['p1'])}, partial ⟪η_{{p}}^{{2}}⟫ = "
     f"{f3(M['DST']['YES']['eta1'])}), the second largest effect size among the four "
     "practices. However, its association with youth turnover is only marginal and does not "
     f"meet the conventional 5% threshold (B = −{abs(M['DST']['YTR']['B1']):.3f}, "
     f"{ptxt(M['DST']['YTR']['p1'])}). Training-intensive firms thus employ markedly more "
     "young people, while the retention advantage of training is weaker and should not be "
     "overstated (Table 7, Figure 4)."),

    ('tabcap', 7, 'Parameter estimates for the relationship between digital skills training '
                  'and youth-employment outcomes.'),
    ('table', param_table('DST'), _pw),
    ('notes', f"Source: authors’ calculations. Note: N = {N}. CI = confidence interval."),

    ('figure', 'p5_fig4.png', 5.35, None, 23),
    ('figcap', 4, 'Youth employee share and youth turnover rate in relation to digital '
                  'skills training. Source: authors’ design.'),

    ('p', "Overall, the four models suggest differentiated rather than uniform associations. "
     "Digital transformation leadership and data-driven decision-making are significantly "
     "associated with both outcomes; AI application breadth is significantly associated only "
     "with lower turnover, and digital skills training only with a higher youth share, each "
     "showing a marginal association with the respective other outcome. Therefore, H1 is "
     "only partially supported. Model diagnostics raise no concerns: Shapiro–Wilk tests do "
     "not reject residual normality in any of the eight univariate specifications (all "
     f"⟪p⟫ ≥ {min(v[k] for v in S['resid_normality'].values() for k in ('YES_p','YTR_p')):.2f}), "
     f"and the maximum Cook's distance across models is {S['max_cooks']:.2f}, well below "
     "common concern thresholds."),

    ('h2', '4.2. Robustness: Covariate-Adjusted Models and Structural Contextual Correlates'),

    ('p', "Because practice differences may overlap with structural firm characteristics, each "
     "model was re-estimated as a MANCOVA with firm size, firm age, R&D intensity, and the "
     "digital-core industry indicator as covariates (Table 8). The pattern of results is "
     "preserved in every model: the multivariate association of each practice remains "
     "significant, the adjusted coefficients of DTL, DDM, and DST on the youth share and of "
     "DTL, DDM, and AIA on turnover remain significant with essentially unchanged magnitudes, "
     "and the association of AIA with the youth share remains marginal "
     f"({ptxt(MC['AIA']['coef']['YES']['p'])}). The only notable change is that the adjusted "
     "association of digital skills training with youth turnover strengthens slightly and "
     f"crosses the 5% threshold ({ptxt(MC['DST']['coef']['YTR']['p'])}), suggesting that the "
     "weak bivariate association partly reflected the confounding of training with firm size. "
     "These adjusted estimates should still be read as descriptive associations rather than "
     "causal effects."),

    ('tabcap', 8, 'Covariate-adjusted (MANCOVA) estimates for the four practice dimensions.'),
    ('table', _t8, [1900, 1300, 950, 950, 1150, 950, 1150, 950]),
    ('notes', "Source: authors’ calculations. Covariates: lnSIZE, AGE, RDI, DIG. Adj. B = "
     "adjusted unstandardized coefficient of the focal predictor; multivariate statistics are "
     "Wilks’ Lambda F-tests for the focal predictor."),

    ('p', "Supplementary bivariate correlations (Table 9) show that the practice indicators "
     "are largely independent of firm age and only weakly related to firm size, whereas the "
     "leadership, decision-making, and AI indicators correlate positively with R&D intensity "
     "and—most strongly for AIA—with operation in a digital-core industry; training "
     "intensity is essentially unrelated to R&D intensity. Practice differences therefore partly track the innovation "
     "profile and sector of firms, which is why the covariate-adjusted models above, rather "
     "than the bivariate models alone, underpin our conclusions. The non-response comparisons "
     "reported in Section 3.1 and the common-method checks in Section 3.2 complete the "
     "robustness assessment."),

    ('tabcap', 9, 'Supplementary bivariate correlations of practice indicators with '
                  'structural contextual variables.'),
    ('table', _t9, [2750, 1720, 1720, 1720, 1720]),
    ('notes', "Source: authors’ calculations. Pearson correlation coefficients with p-values "
     "in parentheses. N = 308."),

    ('h2', '4.3. The Latent Dimension of Digital Leadership–Decision Capability and Its '
           'Systemic Associations with Youth Employment'),

    ('p', "The exploratory factor analysis aimed to reduce the four observable practice "
     "indicators to a common factor structure, capturing the aggregate process by which "
     "leadership, decision-making, technology deployment, and training articulate into a "
     f"cohesive organizational capability. The KMO value of {f3(EFA['KMO'])}, the "
     f"significance of Bartlett's test (χ2({EFA['bartlett_df']}) = "
     f"{f3(EFA['bartlett_chi2'])}, ⟪p⟫ < 0.001), and the significant correlations among the "
     "variables indicate that the data are suitable for extracting a common latent construct "
     f"(Table 10). The first eigenvalue ({f3(EFA['eig1'])}) accounts for "
     f"{EFA['init_var']:.1f}% of the total variance, and the retained single factor explains "
     f"{EFA['extract_var']:.1f}% after extraction—a moderate common dimension consistent "
     "with four practices that share an underlying orientation without being redundant."),

    ('p', "The communalities indicate that the latent factor is anchored primarily in digital "
     f"transformation leadership (extraction communality {f3(EFA['communal_extract'][0])}) "
     f"and data-driven decision-making ({f3(EFA['communal_extract'][1])}), with digital "
     f"skills training intermediate ({f3(EFA['communal_extract'][3])}). AI application "
     f"breadth has the lowest extracted communality ({f3(EFA['communal_extract'][2])}), "
     "indicating that technology deployment shares less variance with the common capability "
     "dimension than the leadership, decision, and training practices do. This finding does "
     "not justify excluding the variable, since its loading remains substantial "
     f"({f3(EFA['loadings'][2])}), but it foreshadows a central interpretive theme: deploying "
     "AI is not the same thing as leading digitally. The latent factor, labelled "
     "⟪FACT_DLDM⟫, reflects an emerging construct of digital leadership–decision capability "
     "in which managerial practices, rather than technology inventories, carry most of the "
     "common signal."),

    ('tabcap', 10, 'Exploratory factor analysis of the digital leadership and '
                   'decision-making practice indicators.'),
    ('table', _t10, [4820, 4820]),
    ('notes', "Source: authors’ calculations. Principal Axis Factoring on the correlation "
     "matrix of DTL, DDM, AIA, and DST; one factor retained; factor scores by the "
     "regression method."),

    ('p', "The first regression analyzed the relationship between the latent capability "
     "factor and the youth employee share. The model indicates a positive and statistically "
     f"significant relationship, with a correlation coefficient of {f3(RY['R'])} and an "
     f"explanatory capacity of approximately {100 * RY['R2']:.0f}% of the variation in the "
     f"youth share (⟪R^{{2}}⟫ = {f3(RY['R2'])}; adjusted ⟪R^{{2}}⟫ = {f3(RY['adjR2'])}). "
     f"The F test indicates that the model is statistically significant "
     f"(F = {f3(RY['F'])}, ⟪p⟫ < 0.001). On average, a one-standard-deviation rise in "
     f"⟪FACT_DLDM⟫ is associated with an increase of about {RY['B1']:.2f} percentage points "
     f"in the youth employee share (B = {f3(RY['B1'])}, β = {f3(RY['beta'])}) (Table 11)."),

    ('tabcap', 11, 'Regression results for the relationship between the latent digital '
                   'leadership–decision capability factor and the youth employee share.'),
    ('table', reg_rows(RY), _rw, 'norepeat'),
    ('notes', "Source: authors’ calculations. Dependent variable: YES. Predictor: factor "
     "scores of FACT_DLDM (standardized)."),

    ('p', "The second regression examines the association between the latent factor and "
     f"youth turnover. The model shows a negative association (r = −{f3(RT['R'])}) and "
     f"explains around {100 * RT['R2']:.0f}% of the variation in the youth turnover rate "
     f"(⟪R^{{2}}⟫ = {f3(RT['R2'])}; adjusted ⟪R^{{2}}⟫ = {f3(RT['adjR2'])}; "
     f"F = {f3(RT['F'])}, ⟪p⟫ < 0.001). A one-standard-deviation rise in the factor score "
     f"is associated with a decrease of about {abs(RT['B1']):.2f} percentage points in youth "
     f"turnover (B = −{abs(RT['B1']):.3f}, β = −{abs(RT['beta']):.3f}) (Table 12). These "
     "results provide support for H2: the latent dimension of digital leadership–decision "
     "capability is significantly associated with both a younger and a more stable young "
     "workforce, consistent with the socio-technical expectation that configurations of "
     "practice, rather than single levers, carry systemic workforce correlates."),

    ('tabcap', 12, 'Regression results for the relationship between the latent digital '
                   'leadership–decision capability factor and the youth turnover rate.'),
    ('table', reg_rows(RT), _rw, 'norepeat'),
    ('notes', "Source: authors’ calculations. Dependent variable: YTR. Predictor: factor "
     "scores of FACT_DLDM (standardized)."),

    ('h2', '4.4. Emerging Socio-Technical Typologies: Organizational Profiles of Digital '
           'Practice and Youth Employment'),

    ('p', "To explore the latent structure of the relationships between digital practices and "
     "youth-employment outcomes at the level of whole configurations, the analysis began with "
     "hierarchical clustering of the six standardized variables, using the average linkage "
     "method and the Pearson correlation coefficient to measure proximity between firms. The "
     "truncated dendrogram presented in Figure 5 suggests a two-group structure in the "
     "sample. Following this exploratory indication, the k-means algorithm was applied for "
     f"k = 2, 3, and 4; the average silhouette coefficient favors the two-cluster solution "
     f"({f3(SILK['2'])} versus {f3(SILK['3'])} and {f3(SILK['4'])}), and the hierarchical "
     f"and k-means partitions agree for {_h_agree:.1f}% of firms. The resulting two-cluster "
     "solution should be interpreted as an exploratory and descriptive typology, not as a "
     "definitive classification of enterprises."),

    ('figure', 'p5_fig5.png', 5.5, None, 24),
    ('figcap', 5, 'Dendrogram of the hierarchical clustering of firms based on digital '
                  'practices and youth-employment outcomes (average linkage, truncated to '
                  'the last 36 merges). Source: authors’ design.'),

    ('p', f"The cluster centers provide a synthetic view of the two exploratory typologies "
     f"(Table 13). The first cluster (n = {CS[0]}) unites digitally led, youth-integrating "
     f"firms: average digital leadership of {f2(CC['cluster1']['DTL'])} and data-driven "
     f"decision-making of {f2(CC['cluster1']['DDM'])} on the five-point scales, "
     f"{f2(CC['cluster1']['AIA'])} AI-enabled functions, training intensity of "
     f"{f2(CC['cluster1']['DST'])}, a youth employee share of {f2(CC['cluster1']['YES'])}%, "
     f"and youth turnover of {f2(CC['cluster1']['YTR'])}%. The second cluster "
     f"(n = {CS[1]}) groups conventionally managed firms with substantially lower digital "
     f"practice levels ({f2(CC['cluster2']['DTL'])}, {f2(CC['cluster2']['DDM'])}, "
     f"{f2(CC['cluster2']['AIA'])}, and {f2(CC['cluster2']['DST'])}, respectively), a lower "
     f"youth share ({f2(CC['cluster2']['YES'])}%), and markedly higher youth turnover "
     f"({f2(CC['cluster2']['YTR'])}%). The digitally led cluster contains a higher share of "
     f"digital-core firms ({S['cluster_sector_pct']['cluster1']['digital-core']:.1f}% versus "
     f"{S['cluster_sector_pct']['cluster2']['digital-core']:.1f}%), yet manufacturing firms "
     "form a plurality of both clusters, indicating that the typology cuts across sector "
     "boundaries rather than merely reproducing them."),

    ('p', f"As a minimal validation metric, the average silhouette coefficient of the final "
     f"two-cluster solution is {f3(SIL['avg'])} ({f3(SIL['c1'])} for Cluster 1 and "
     f"{f3(SIL['c2'])} for Cluster 2). These positive values indicate modest but coherent "
     "internal structure, appropriate for exploratory purposes; the separation should not be "
     "interpreted as strong. The ANOVA results in Table 13 provide a descriptive "
     "characterization of the differences between the clusters. Because the clusters were "
     "formed using the same variables that are subsequently compared, the F values are "
     "descriptive and should not be treated as independent hypothesis tests. With this "
     "caveat, the practice variables separate the clusters most sharply, and both "
     "youth-employment outcomes also differ substantially between the profiles. Overall, the "
     "cluster analysis supports Hypothesis H3: firms can be grouped into meaningful "
     "socio-technical typologies in which digital leadership, decision practice, technology, "
     "training, and youth outcomes cohere."),

    ('tabcap', 13, 'Cluster centers and differences between clusters (ANOVA).'),
    ('table', _t13, [1500, 1900, 1900, 1400, 1500, 1440]),
    ('notes', f"Source: authors’ calculations. k-means with k = 2 on standardized variables; "
     f"means reported in original units. ANOVA df = ({CA['DTL']['df1']}, "
     f"{CA['DTL']['df2']}); F values are descriptive (see text)."),

    ('h1', '5. Discussion'),

    ('p', "The data suggest a differentiated pattern of associations between digital "
     "transformation practices and the youth-employment profile of firms. Rather than "
     "implying a causal process, these findings point to cross-sectional co-occurrences that "
     "may reflect broader organizational and sectoral conditions. This interpretation is "
     "consistent with the literature that characterizes digital transformation as a "
     "capability-driven, organization-wide reconfiguration whose workforce consequences "
     "depend on the adoption context and on the complementarities between technology and the "
     "human factor {{vial2019|sts2|stsd2}}."),

    ('p', "The four models should not be interpreted as comparing the independent or partial "
     "contribution of each practice dimension. Since the practice variables are conceptually "
     "related and substantially correlated, each single-predictor model may partly reflect "
     "the same broader configuration of digitally oriented management. For this reason, the "
     "results are interpreted as parallel cross-sectional associations, while the "
     "exploratory factor analysis provides a complementary means of summarizing their common "
     "latent structure, and the covariate-adjusted models bound the extent to which "
     "structural firm characteristics account for the associations."),

    ('p', "The results of the multivariate models provide partial support for H1, and the "
     "deviations from uniformity are themselves informative. Digital transformation "
     "leadership emerges as the practice most consistently associated with youth outcomes, "
     "echoing evidence that leadership is the binding constraint of digital transformation "
     "rather than technology itself {{dl2|dl3|upper_digital}}. The association of "
     "data-driven decision-making with both outcomes extends the analytics literature—which "
     "has concentrated on innovation and performance {{ddm1|bda1|ddd_perf}}—to workforce "
     "composition, and is consistent with survey evidence that merit-legible, "
     "data-transparent management appeals to new-generation employees in China "
     "{{china_newgen|genz_work}}."),

    ('p', "The most striking asymmetry concerns AI application breadth. AI-rich firms retain "
     "young employees better—plausibly because AI absorbs the most repetitive task content "
     "of junior roles, improving job quality {{career1|genai2|genai3}}—but breadth of "
     "deployment is not associated with employing proportionally more young people once its "
     "correlation with the other practices is set aside. This nuance aligns with task-based "
     "accounts in which automation both displaces entry-level routine work and reinstates "
     "new tasks {{acemoglu2019|genai1}}, with Chinese firm-level evidence of skill-structure "
     "upgrading without lower-skill expansion {{skill_demand|digitrans_emp_firm|"
     "robots_china_firm}}, and with socio-technical arguments that technology divorced from "
     "complementary organizational practice yields limited social-subsystem benefits "
     "{{sts2|sts_ai}}. Deployment, in short, is associated with keeping the young, while "
     "leadership, decision, and training practices are associated with bringing them in."),

    ('p', "The strong association of digital skills training with the youth employee share, "
     "and its weaker (bivariate) association with turnover, complete this picture. Training "
     "operates on the hiring margin—signaling learning opportunities that young applicants "
     "prioritize {{employer_attract|genz_work}}—and builds the firm-specific digital capital "
     "documented in the training literature {{training1|training2}}. That the "
     "covariate-adjusted association with turnover reaches significance suggests an "
     "embeddedness mechanism {{mitchell2001}} partially masked by firm size in the raw data. "
     "Together with the leadership results, this supports a demand-side reading of youth "
     "employment in which organizational practice, not merely macro conditions, shapes young "
     "people's chances of entering and staying in employment {{youth_demand_side|ilo1}}."),

    ('p', "The second hypothesis is supported by the latent factor of digital "
     "leadership–decision capability derived from factor analysis and regression models. The "
     "KMO value, the significance of Bartlett's test, and a single factor explaining "
     f"{EFA['extract_var']:.0f}% of the shared variance after extraction indicate that the "
     "four practices are not independent occurrences but expressions of a common "
     "capability dimension. That AI breadth carries the lowest communality reinforces the "
     "dynamic-capabilities reading: what is common to digitally successful firms is a "
     "managerial capacity to sense, decide, and develop—technology inventories follow from "
     "it, not the reverse {{teece|ceo_digital|vial2019}}. The latent factor's positive "
     "association with the youth share and negative association with turnover suggests that "
     "young workers, digital capability, and workforce stability co-occur in more "
     "digitally mature organizational contexts. However, this interpretation remains "
     "exploratory and should not be taken as evidence that building digital capability "
     "increases youth employment."),

    ('p', "The cluster analysis supports the third hypothesis and points to two distinct "
     "socio-technical regimes within a single regional economy. The digitally led, "
     f"youth-integrating profile ({CS[0]} firms) combines high practice levels with a "
     "younger, more stable workforce; the conventionally managed profile "
     f"({CS[1]} firms) combines low practice levels with an older workforce and more than "
     "a third more youth turnover. These differences are described using statistical "
     "testing (ANOVA), but the cluster results should be read as descriptive and "
     "hypothesis-generating. The observed profiles may also reflect broader structural "
     "conditions—innovation intensity, sector, and product-market position—although the "
     "covariate-adjusted models and the sectoral composition of the clusters indicate that "
     "the typology is not reducible to industry membership. This result aligns with "
     "configurational research in management {{kmeans_biz}} and with studies of "
     "heterogeneous digital transformation trajectories among firms {{digital_sme|"
     "textmeasure1|stsd2}}. Reverse causality remains plausible throughout: firms with "
     "younger workforces may find digital transformation easier to lead, and firms that "
     "retain young digital talent may accumulate capability faster {{talent|im_hc}}."),

    ('h2', '5.1. Theoretical Implications'),

    ('p', "Theoretically, the findings extend upper echelons and dynamic-capabilities "
     "reasoning to an outcome those literatures rarely examine: the age composition and "
     "stability of the workforce. If organizational outcomes reflect managerial cognition "
     "and capability {{upper1|upper2|teece}}, then who gets hired and retained—not only how "
     "much is innovated—should bear the imprint of leadership; our results are consistent "
     "with exactly that imprint. The study also enriches the socio-technical systems "
     "tradition {{sts1|sts2|sts4}} by treating youth integration as a social-subsystem "
     "outcome that co-varies with the joint configuration of technical deployment and "
     "managerial practice, and by showing empirically that the technical element (AI "
     "breadth) is the configuration's weakest common denominator. Finally, the demonstration "
     "that a single latent capability factor summarizes four distinct practices, and that "
     "firms cluster into interpretable regimes, supports configurational over variable-"
     "centric theorizing about digital transformation {{kmeans_biz|stsd1}}."),

    ('h2', '5.2. Practical Implications'),

    ('p', "The findings offer several practical implications for executives, HR leaders, "
     "policy-makers, and educational institutions involved in youth-employment governance. "
     "For enterprise leaders, the differentiated pattern cautions against equating digital "
     "transformation with technology procurement. Firms that wish to rejuvenate their "
     "workforce should pair AI deployment with visible transformation leadership, "
     "data-transparent decision processes, and youth-oriented training pipelines—the "
     "practices associated with actually employing young people. Embedding analytics in HR "
     "decisions may additionally serve retention by making career processes legible to "
     "new-generation employees {{budhwar2023|china_newgen}}. For young job seekers and "
     "career services, the typology suggests screening employers for leadership and "
     "training signals—not merely for technology stacks—when assessing where digital "
     "careers are likely to flourish {{employer_attract}}."),

    ('p', "For policy-makers concerned with youth employment, the results direct attention "
     "to the demand side: programs that subsidize digital-skills training inside firms, "
     "diffuse data-driven management practice to SMEs, and develop digital leadership in "
     "traditional sectors may complement conventional supply-side measures such as graduate "
     "skills programs {{ilo1|digital_sme}}. In regional economies like Zhejiang, where "
     "digital infrastructure is already strong, the binding constraint indicated by our "
     "clusters is managerial rather than infrastructural: a majority of surveyed firms "
     "operate a conventionally managed regime with weak youth integration despite operating "
     "in the same environment as digitally led peers {{ses_regional|talent}}. Policy "
     "instruments that pair technology-adoption subsidies with management-upgrading and "
     "youth-training conditions could address both subsystems simultaneously."),

    ('h2', '5.3. Limitations and Further Research'),

    ('p', "The research provides a useful systemic view of the relationship between digital "
     "transformation practices and youth employment inside firms, but the results need to "
     "be read alongside several constraints. The first is the cross-sectional design: the "
     "analysis reflects associations at a single point in time and cannot establish causal "
     "direction; reverse causality and omitted organizational variables remain plausible. "
     "Future studies should employ panel designs that track practices and workforce "
     "composition over time. The second limitation concerns measurement: practices are "
     "reported by a single senior informant per firm, and although the outcomes are "
     "quasi-objective workforce statistics and common-method checks were passed, "
     "mono-informant designs cannot fully exclude method variance {{podsakoff2003|"
     "podsakoff2024}}; matched multi-informant or administrative data would strengthen "
     "inference. Third, the youth employee share and turnover rate are coarse summary "
     "indicators that do not distinguish occupations, contract types, or job quality; "
     "linked employer–employee data could reveal which young workers digitally led firms "
     "actually employ {{china_youth2}}."),

    ('p', "A further limitation is the single-region scope. Zhejiang's dense digital economy "
     "makes it a revealing but non-representative setting; replication across regions with "
     "weaker digital infrastructure, and across institutional contexts outside China, would "
     "test the boundary conditions of the associations {{digital_sme|youth_demand_side}}. "
     "The exploratory factor analysis should be regarded as a preliminary identification of "
     "a common capability dimension rather than a definitive measurement model; "
     "confirmatory approaches with larger item pools are a natural next step. Cluster "
     "analysis, finally, is exploratory and depends on the selected variables, distance "
     "measure, and algorithm; the modest silhouette values counsel caution, and future "
     "research should validate the typology with additional criteria, external validation "
     "variables, and alternative clustering specifications {{rousseeuw|jain}}. Extending "
     "the outcome set to youth career progression inside firms—promotion, wage growth, and "
     "skill certification—would connect this organizational typology to the broader youth "
     "career-development agenda {{career1|career2}}."),

    ('h1', '6. Conclusions'),

    ('p', "This study examined the cross-sectional associations between four digital "
     "transformation practices—digital transformation leadership, data-driven "
     "decision-making, AI application breadth, and digital skills training—and two "
     "youth-employment outcomes—the youth employee share and the youth turnover rate—in a "
     "survey of 308 enterprises in Zhejiang Province, China. By combining MANOVA-type "
     "multivariate models, exploratory factor analysis, and cluster analysis, the study "
     "provides a differentiated, system-level view of how leadership, decision-making, and "
     "digital transformation relate to the position of young people inside firms. The "
     "findings should be interpreted as exploratory associations, not as evidence of "
     "causal effects."),

    ('p', "The results show that the relationship between digital practice and youth "
     "employment is not uniform across dimensions. Digital transformation leadership and "
     "data-driven decision-making are significantly associated with both a higher youth "
     "employee share and lower youth turnover. AI application breadth is significantly "
     "associated with lower youth turnover, but its association with the youth share does "
     "not reach the conventional significance threshold; digital skills training shows the "
     "mirror-image pattern. These findings indicate that the youth-employment relevance of "
     "digital transformation depends on the practice through which it is enacted, with "
     "managerial practices—not technology deployment—carrying the hiring-side association."),

    ('p', "The factor analysis further suggests that the four practices share a moderate "
     "common latent dimension of digital leadership–decision capability, which is "
     "significantly associated with both outcomes, supporting the interpretation that "
     "youth-employment profiles attach to organizational capability configurations rather "
     "than to isolated practices. The cluster analysis identifies two exploratory "
     "socio-technical regimes—digitally led, youth-integrating firms and conventionally "
     "managed firms with weaker youth outcomes—that cut across sector boundaries within a "
     "single regional economy."),

    ('p', "From a policy perspective, the findings do not justify claims that digital "
     "transformation directly improves youth employment. Rather, they suggest that "
     "leadership capability, decision practice, and training provision are the "
     "organizational sites where digital transformation and youth opportunity meet. "
     "Policies and corporate strategies focused exclusively on technological diffusion are "
     "unlikely to be sufficient; approaches that develop digital leadership, diffuse "
     "data-driven management, and condition support on youth-oriented skills investment "
     "address the configuration to which favorable youth outcomes attach. Future research "
     "should use longitudinal and multi-informant designs, extend the outcome set to "
     "career progression, and test whether the socio-technical typologies identified here "
     "generalize across regions and institutional contexts."),

    ('back', 'Author Contributions:', "Conceptualization, X.C. and T.M.; methodology, X.C.; "
     "software, X.C.; validation, X.C., D.H. and T.M.; formal analysis, X.C.; investigation, "
     "D.H.; resources, T.M.; data curation, D.H.; writing—original draft preparation, X.C.; "
     "writing—review and editing, T.M.; visualization, D.H.; supervision, T.M.; project "
     "administration, T.M.; funding acquisition, X.C. All authors have read and agreed to "
     "the published version of the manuscript."),

    ('back', 'Funding:', "This research was funded by the Zhejiang Provincial Philosophy and "
     "Social Sciences Planning Special Project on Higher Education Basic Research Funding "
     "Reform (Grant Number: 25NDJC153YBMS) and the Major Humanities and Social Sciences "
     "Research Projects in Zhejiang Higher Education Institutions (Grant Number: 2024QN018)."),

    ('back', 'Institutional Review Board Statement:', "The study was conducted in accordance "
     "with the Declaration of Helsinki and approved by the Academic Ethics Committee of the "
     "College of Business, Jiaxing University (protocol code JXU-BUS-2025-108, approved on "
     "28 October 2025)."),

    ('back', 'Informed Consent Statement:', "Informed consent was obtained from all "
     "respondents involved in the study."),

    ('back', 'Data Availability Statement:', "The data presented in this study are available "
     "on request from the corresponding author due to the confidentiality commitments made "
     "to participating firms. The analysis code is available from the authors upon "
     "reasonable request."),

    ('back', 'Conflicts of Interest:', "The authors declare no conflicts of interest."),

    ('h1', 'Abbreviations'),
    ('p', "The following abbreviations are used in this manuscript:"),
    ('table', [
        ['Abbreviation', 'Definition'],
        ['DTL', 'Digital transformation leadership'],
        ['DDM', 'Data-driven decision-making'],
        ['AIA', 'AI application breadth'],
        ['DST', 'Digital skills training'],
        ['YES', 'Youth employee share (% of employees aged 16–29)'],
        ['YTR', 'Youth turnover rate (% among employees younger than 30)'],
        ['FACT_DLDM', 'Latent factor of digital leadership–decision capability'],
        ['AI', 'Artificial intelligence'],
        ['EFA', 'Exploratory factor analysis'],
        ['PAF', 'Principal Axis Factoring'],
        ['KMO', 'Kaiser–Meyer–Olkin measure of sampling adequacy'],
        ['MANOVA/MANCOVA', 'Multivariate analysis of (co)variance'],
        ['CI', 'Confidence interval'],
        ['HR', 'Human resources'],
        ['RDI', 'R&D intensity'],
        ['SME', 'Small and medium-sized enterprise'],
    ], [2600, 7040]),

    ('h1', 'Appendix A'),

    ('p', "Table A1 lists the measurement items of the three reflective constructs together "
     "with their standardized loadings from single-factor Principal Axis Factoring within "
     "each construct. All items were administered in Chinese on five-point Likert scales "
     "(1 = strongly disagree, 5 = strongly agree) following translation and "
     "back-translation {{brislin1970}}."),

    ('tabcap', 'A1', 'Measurement items and standardized factor loadings.'),
    ('table', _ta1, [1300, 900, 6100, 1340]),
    ('notes', "Source: authors’ design. Loadings from within-construct Principal Axis "
     "Factoring (N = 308)."),

    ('p', "The AI application breadth (AIA) index asked whether AI technologies are used in "
     f"each of the following ten business functions: {_AIA_FUNCS}. The index is the count "
     "of functions marked."),
]
