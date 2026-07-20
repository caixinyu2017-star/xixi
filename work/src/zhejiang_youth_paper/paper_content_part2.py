# -*- coding: utf-8 -*-
"""Manuscript content, part 2: Research Design and Empirical Results."""

PART2 = [
    ('h1', '3. Research Design'),

    ('h2', '3.1. Variable Measurement'),

    ('h3', '3.1.1. Youth Employment and Youth Career Development'),

    ('p', "Conceptually, youth employment refers to the firm-level demand for young workers, that "
     "is, the extent to which a firm employs workers in the early stage of their careers. "
     "Empirically, because employee age structure is disclosed with increasing coverage in the "
     "corporate-governance and employee files of Chinese listed firms, we measure youth employment "
     "(⟪YEMP⟫) as the share of a firm's employees aged 30 years and below in total employees, as "
     "defined in Equation (1):"),

    ('eq', 'eq1', 1),

    ('p', "where ⟪Emp30_{i,t}⟫ is the number of employees aged 30 years and below in firm ⟪i⟫ in "
     "year ⟪t⟫, and ⟪Emp_{i,t}⟫ is the firm's total number of employees. Using a share rather than "
     "a level purges the measure of firm-size effects and captures the composition of labor demand "
     "toward young workers. Because a 35-year threshold is also commonly used in disclosure "
     "practice, we construct an alternative measure (⟪YEMP2⟫), the share of employees aged 35 and "
     "below, for robustness. Employee age-structure and headcount data were obtained from the China "
     "Stock Market and Accounting Research Database (CSMAR) and supplemented by hand-collection "
     "from firms' annual reports."),

    ('p', "Youth career development (⟪YCAR⟫) captures whether young talent advances into "
     "decision-making positions within the firm. Following the executive-profile literature, we "
     "measure ⟪YCAR⟫ as the proportion of a firm's directors, supervisors, and senior executives "
     "aged 40 years and below in the total executive team in year ⟪t⟫, constructed from the CSMAR "
     "executive-characteristics files {{career2|textmeasure1}}. A higher value indicates that young "
     "professionals occupy a larger share of managerial positions, an observable marker of "
     "early-career advancement within the organizational hierarchy. As an alternative measure, we "
     "use the share of executives aged 45 and below."),

    ('h3', '3.1.2. Industrial Intelligent Transformation'),

    ('p', "Conceptually, industrial intelligent transformation refers to the firm-level "
     "transformation of production systems toward intelligent, adaptive, and data-enabled "
     "manufacturing. Empirically, because it is difficult to observe all dimensions of intelligent "
     "transformation at the firm-year level, we use industrial robot penetration as a proxy for the "
     "embodied, production-side dimension of intelligent transformation, following current research "
     "{{robots_china_firm|robots_china2}}. We construct a firm-level industrial intelligent "
     "transformation (⟪II⟫) measure based on robot penetration using a shift-share (Bartik) "
     "approach {{bartik}}. First, we construct the industry-level penetration rate of industrial "
     "robots in China according to Equation (2):"),

    ('eq', 'eq2', 2),

    ('p', "where ⟪II_{m,t}⟫ denotes the penetration rate of industrial robots in industry ⟪m⟫ in "
     "year ⟪t⟫; ⟪ROBOT_{m,t}⟫ represents the operational stock of industrial robots in industry "
     "⟪m⟫ in year ⟪t⟫ in China, drawn from the International Federation of Robotics (IFR) "
     "database; and ⟪L_{m,2010}⟫ represents employment in the base year 2010 in industry ⟪m⟫. "
     "Fixing the employment denominator at the pre-period level mitigates concerns about "
     "endogenous adjustments in industry employment. Second, we construct the firm-level exposure "
     "to robot penetration according to Equations (3) and (4):"),

    ('eq', 'eq3', 3),
    ('eq', 'eq4', 4),

    ('p', "where ⟪II_{i,t}⟫ represents firm ⟪i⟫'s exposure to industrial robot penetration in year "
     "⟪t⟫, and ⟪ω_{i,m}⟫ is a time-invariant exposure weight that captures firm ⟪i⟫'s baseline "
     "intensity of production activities within industry ⟪m⟫. ⟪RS_{i,m,2011}⟫ denotes firm ⟪i⟫'s "
     "share of employees in production-related positions in the base year 2011, and "
     "⟪RS_{m,2011}⟫ denotes the industry-⟪m⟫ median of the same measure in 2011. The ratio serves "
     "as the baseline exposure weight, which is interacted with the time-varying industry-level "
     "penetration ⟪II_{m,t}⟫ to obtain the firm-year measure. As an alternative measure, we "
     "construct a text-based intelligent-transformation index (⟪TII⟫) from the frequency of "
     "intelligent-manufacturing-related keywords in firms' annual reports, following the "
     "text-measurement literature {{textdata|textmeasure1|textmeasure2}}."),

    ('h3', '3.1.3. Mediating Variables'),

    ('p', "To unpack the channels through which intelligent transformation affects youth "
     "employment, we focus on two mediators: the firm skill structure and labor productivity."),

    ('p', "Firm skill structure (⟪SKILL⟫). We proxy the firm skill structure by the share of "
     "employees holding a bachelor's degree or above in total employees, based on the "
     "education-structure data in CSMAR {{skill_demand}}. A higher value indicates a more "
     "skill-intensive workforce. As an alternative, we use the share of technical and R&D "
     "personnel in total employees."),

    ('p', "Labor productivity (⟪lnPROD⟫). We measure the expansion channel by labor productivity, "
     "defined as the natural logarithm of operating revenue per employee "
     "{{prod1|robots_japan}}. Productivity growth captures the cost-reduction and scale-expansion "
     "force through which automation enlarges the firm's activity and hiring capacity. As an "
     "alternative, we use total factor productivity estimated with the Levinsohn–Petrin method."),

    ('h3', '3.1.4. Moderating Variables'),

    ('p', "To test the moderating role of multi-level employment governance, we construct three "
     "variables spanning the firm, regional, and policy levels."),

    ('p', "Firm training investment (⟪TRAIN⟫). We measure training investment as employee "
     "education and training expenses per employee, hand-collected from the notes to firms' "
     "financial statements, min–max normalized to the [0, 1] interval "
     "{{training1|training2}}. A higher value indicates a stronger internal skill-formation "
     "capability."),

    ('p', "Regional public employment services (⟪PES⟫). We measure the intensity of public "
     "employment services in the prefecture-level city where the firm is registered by the natural "
     "logarithm of per-capita fiscal expenditure on education and employment-related programs, "
     "drawn from the China City Statistical Yearbook and provincial fiscal accounts {{alm1|vet1}}. "
     "This variable captures the local supply of job-placement platforms, vocational training, and "
     "employment subsidies available to young job seekers."),

    ('p', "Digital-economy policy pilots (⟪POLICY⟫). We measure policy support using a dummy "
     "variable equal to 1 if the firm is registered in a city designated as a national big-data "
     "comprehensive pilot zone or a national new-generation artificial intelligence innovation and "
     "development pilot zone in year ⟪t⟫, and 0 otherwise {{pilot1|pilot2}}. These national pilots "
     "provide regulatory support, digital infrastructure, and talent-attraction complementarities "
     "for intelligent transformation."),

    ('h3', '3.1.5. Control Variables'),

    ('p', "Following the extant literature, we control for a series of firm- and city-level "
     "variables that may affect youth employment. Firm-level controls include firm age (⟪Age⟫), "
     "firm size (⟪Size⟫), leverage (⟪Lev⟫), profitability (⟪RoA⟫), cash flow (⟪Cash⟫), sales "
     "growth (⟪Growth⟫), the shareholding of the top ten shareholders (⟪Top10⟫), board size "
     "(⟪Board⟫), CEO–chair separation (⟪Separation⟫), and state ownership (⟪SOE⟫). To account for "
     "regional economic conditions, we further include the natural logarithm of the gross domestic "
     "product of the city where the firm is registered (⟪lngdp⟫), which controls for differences "
     "in local economic development, labor-market conditions, and demand that may be correlated "
     "with both intelligent transformation and youth employment. Detailed definitions of all "
     "variables are provided in Appendix A.1."),

    ('h2', '3.2. Regression Model Specification'),

    ('h3', '3.2.1. Baseline Model'),

    ('p', "To examine the impact of industrial intelligent transformation on youth employment and "
     "career development, we estimate Equation (5):"),

    ('eq', 'eq5', 5),

    ('p', "Here, ⟪i⟫ indexes firms and ⟪t⟫ indexes years. The dependent variable ⟪Y_{i,t}⟫ "
     "alternatively denotes the youth-employment share ⟪YEMP_{i,t}⟫ and the young-executive share "
     "⟪YCAR_{i,t}⟫ (Section 3.1.1). We use the one-year lag of intelligent transformation, "
     "⟪II_{i,t−1}⟫, to mitigate simultaneity and reverse-causality concerns and to ensure that "
     "transformation is measured prior to labor outcomes (Section 3.1.2). ⟪Controls_{i,t}⟫ "
     "includes the firm- and city-level controls. We include firm fixed effects ⟪μ_{i}⟫ and year "
     "fixed effects ⟪λ_{t}⟫ in a two-way fixed-effects design {{twfe}}; ⟪ε_{i,t}⟫ is the error term, and standard errors are robust and "
     "clustered at the firm level. The coefficient of interest is ⟪β_{1}⟫; H1a and H1b predict "
     "⟪β_{1}⟫ > 0."),

    ('h3', '3.2.2. Mediation Models'),

    ('p', "To test the mediating mechanisms, we estimate Equations (6) and (7):"),

    ('eq', 'eq6', 6),
    ('eq', 'eq7', 7),

    ('p', "⟪M_{i,t}⟫ denotes the mediator. For the skill-restructuring effect (H2a), we set "
     "⟪M_{i,t}⟫ = ⟪SKILL_{i,t}⟫; we expect ⟪δ_{1}⟫ > 0 and ⟪φ_{1}⟫ > 0, indicating that "
     "intelligent transformation upgrades the firm skill structure and that a more skill-intensive "
     "structure raises youth employment. For the expansion effect (H2b), we set ⟪M_{i,t}⟫ = "
     "⟪lnPROD_{i,t}⟫; we expect ⟪δ_{1}⟫ > 0 and ⟪φ_{1}⟫ > 0, indicating that transformation "
     "raises labor productivity and that productivity-driven expansion promotes youth employment. "
     "We report bootstrap confidence intervals for the indirect effects to assess the statistical "
     "significance of mediation {{mediation1|mediation2}}."),

    ('h3', '3.2.3. Moderation Models'),

    ('p', "To examine the moderating role of multi-level employment governance, we estimate "
     "Equation (8):"),

    ('eq', 'eq8', 8),

    ('p', "⟪Mod_{i,t}⟫ alternatively captures firm training investment (⟪TRAIN⟫), regional public "
     "employment services (⟪PES⟫), and digital-economy policy pilots (⟪POLICY⟫). The coefficient "
     "of interest is ⟪η_{3}⟫, which corresponds to H3a–H3c and is expected to be positive, "
     "indicating that stronger employment governance amplifies the positive effect of intelligent "
     "transformation on youth employment. Continuous moderators are mean-centered before "
     "constructing the interaction terms."),

    ('h2', '3.3. Data and Sample Selection'),

    ('p', "We construct a panel of A-share listed firms registered in Zhejiang province from 2011 "
     "to 2023. Zhejiang hosts one of the largest provincial populations of listed firms in China, "
     "dominated by private manufacturing enterprises, which makes the sample well suited to "
     "studying the labor-market consequences of regional industrial upgrading. Following standard "
     "practice, we exclude: (1) specially treated firms (ST, *ST, or PT); (2) firms in the "
     "financial industry; and (3) firm-year observations with missing key variables. Firm "
     "financial, employee, executive, and governance data were obtained from CSMAR; industry robot "
     "data were obtained from the IFR database; training expenses were hand-collected from annual "
     "reports; and city-level fiscal and GDP data were obtained from the China City Statistical "
     "Yearbook. All continuous variables were winsorized at the 1st and 99th percentiles to "
     "mitigate the influence of outliers. Because the IFR robot stock is available from 2010 "
     "onward, the one-year-lagged transformation measure is defined for every sample year. The "
     "final sample comprises 6,124 firm-year observations for 668 unique firms."),

    ('h2', '3.4. Descriptive Statistics'),

    ('p', "Table 1 reports the descriptive statistics for all variables. The mean youth-employment "
     "share is 0.312, indicating that employees aged 30 and below account for roughly one-third of "
     "the workforce of Zhejiang listed firms, with substantial cross-firm variation (standard "
     "deviation 0.147). The mean young-executive share is 0.186. Table 2 presents the correlation "
     "matrix; the correlations suggest a positive association between intelligent transformation "
     "and both youth-employment outcomes. Appendix A.2 reports the variance inflation factor (VIF) "
     "values, with a mean VIF of 1.53, indicating that multicollinearity is not a serious "
     "concern."),

    ('tabcap', 1, 'Descriptive statistics for variables.'),
    ('table', [
        ['Variables', 'Obs', 'Mean', 'Std. Dev.', 'Min', 'Max'],
        ['YEMP', '6,124', '0.312', '0.147', '0', '0.826'],
        ['YCAR', '6,124', '0.186', '0.118', '0', '0.667'],
        ['II', '6,124', '0.573', '0.804', '0', '4.116'],
        ['SKILL', '6,124', '0.247', '0.169', '0.021', '0.913'],
        ['lnPROD', '6,124', '13.62', '0.94', '11.08', '16.47'],
        ['TRAIN', '6,124', '0.318', '0.201', '0', '1'],
        ['PES', '6,124', '8.74', '0.52', '7.36', '10.01'],
        ['POLICY', '6,124', '0.462', '0.499', '0', '1'],
        ['Age', '6,124', '2.87', '0.34', '1.61', '3.53'],
        ['Size', '6,124', '22.14', '1.18', '19.87', '26.32'],
        ['Lev', '6,124', '0.417', '0.196', '0.048', '0.892'],
        ['RoA', '6,124', '0.043', '0.062', '−0.284', '0.226'],
        ['Cash', '6,124', '0.048', '0.071', '−0.163', '0.251'],
        ['Growth', '6,124', '0.146', '0.352', '−0.517', '2.418'],
        ['Top10', '6,124', '0.588', '0.147', '0.216', '0.924'],
        ['Board', '6,124', '2.11', '0.19', '1.61', '2.71'],
        ['Separation', '6,124', '0.281', '0.450', '0', '1'],
        ['SOE', '6,124', '0.194', '0.396', '0', '1'],
        ['lngdp', '6,124', '8.92', '0.63', '7.44', '9.86'],
    ], None),
    ('notes', "YEMP is the youth-employment share; YCAR is the young-executive share; II is "
     "industrial intelligent transformation. All variable definitions are provided in Appendix "
     "A.1."),

    ('tabcap', 2, 'Correlation matrix.'),
    ('table', [
        ['Variables', '(1)', '(2)', '(3)', '(4)', '(5)', '(6)', '(7)', '(8)'],
        ['(1) YEMP', '1.000', '', '', '', '', '', '', ''],
        ['(2) YCAR', '0.214 ***', '1.000', '', '', '', '', '', ''],
        ['(3) II', '0.118 ***', '0.087 ***', '1.000', '', '', '', '', ''],
        ['(4) SKILL', '0.126 ***', '0.153 ***', '0.204 ***', '1.000', '', '', '', ''],
        ['(5) lnPROD', '0.095 ***', '0.061 ***', '0.172 ***', '0.238 ***', '1.000', '', '', ''],
        ['(6) TRAIN', '0.083 ***', '0.079 ***', '0.146 ***', '0.187 ***', '0.117 ***', '1.000', '', ''],
        ['(7) PES', '0.071 ***', '0.048 ***', '0.139 ***', '0.162 ***', '0.128 ***', '0.094 ***', '1.000', ''],
        ['(8) POLICY', '0.064 ***', '0.042 ***', '0.151 ***', '0.148 ***', '0.106 ***', '0.088 ***', '0.312 ***', '1.000'],
    ], None),
    ('notes', "*, **, and *** denote significance at the 10%, 5%, and 1% levels, respectively."),

    ('h1', '4. Empirical Results'),

    ('h2', '4.1. Baseline Regression Results'),

    ('p', "We estimate Equation (5) to examine the effect of industrial intelligent transformation "
     "on youth employment and career development; Table 3 reports the baseline results. Columns "
     "(1) and (2) take the youth-employment share as the dependent variable, presenting the "
     "parsimonious specification with firm and year fixed effects and the full specification with "
     "firm- and city-level controls, respectively. Columns (3) and (4) repeat this structure for "
     "the young-executive share. Columns (5) and (6) replace year fixed effects with "
     "industry-by-year fixed effects to control for time-varying industry shocks. Across all "
     "specifications, the coefficient on lagged intelligent transformation is positive and "
     "statistically significant. For youth employment, the estimated coefficient ranges from "
     "0.0112 to 0.0127 and remains significant at the 1% level after adding controls and more "
     "stringent fixed effects, supporting H1a. For the young-executive share, the coefficient "
     "ranges from 0.0068 to 0.0078 and remains significant, supporting H1b."),

    ('p', "Beyond statistical significance, the results are economically meaningful. Taking the "
     "full specification in Column (2) as an example, a one-standard-deviation increase in "
     "intelligent transformation is associated with an increase of approximately 0.96 percentage "
     "points in the youth-employment share, equivalent to about 3.1% of the sample mean. The "
     "corresponding effect on the young-executive share (Column (4)) is 0.57 percentage points, "
     "also about 3.1% of its mean. From a socio-economic systems perspective, these results "
     "suggest that intelligent transformation acts as a technological subsystem shock that expands "
     "both the demand for young, digitally skilled workers and the advancement opportunities of "
     "young managerial talent, rather than simply displacing labor {{robots_japan|sts4}}."),

    ('tabcap', 3, 'Baseline regression results.'),
    ('table', [
        ['Variables', '(1)', '(2)', '(3)', '(4)', '(5)', '(6)'],
        ['', 'YEMP', 'YEMP', 'YCAR', 'YCAR', 'YEMP', 'YCAR'],
        ['L.II', ['0.0127 ***', '(0.0035)'], ['0.0119 ***', '(0.0036)'], ['0.0078 ***', '(0.0027)'],
         ['0.0071 **', '(0.0028)'], ['0.0112 ***', '(0.0037)'], ['0.0068 **', '(0.0029)']],
        ['Controls', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes'],
        ['Firm FE', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Year FE', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'No'],
        ['Industry × Year FE', 'No', 'No', 'No', 'No', 'Yes', 'Yes'],
        ['Observations', '6,124', '6,124', '6,124', '6,124', '6,124', '6,124'],
        ['R-squared', '0.612', '0.634', '0.548', '0.567', '0.651', '0.583'],
    ], [1810, 1305, 1305, 1305, 1305, 1305, 1305]),
    ('notes', "All columns use one-year-lagged II (L.II). *, **, and *** denote significance at "
     "the 10%, 5%, and 1% levels, respectively. Robust standard errors clustered at the firm level "
     "are reported in parentheses."),

    ('p', "From a practical perspective, industrial intelligent transformation does not aggravate "
     "the youth employment dilemma at the firm level. Instead, as Zhejiang firms embed robots and "
     "intelligent equipment into their production processes, they create new digitally intensive "
     "roles, recruit young technical talent, and promote young managers, indicating that the "
     "regional dilemma stems less from technology itself than from frictions in skill formation "
     "and matching—an interpretation we examine directly in the mechanism and moderation analyses "
     "below."),

    ('h2', '4.2. Robustness Checks'),

    ('h3', '4.2.1. Alternative Measures, Sample Restrictions, and Fixed Effects'),

    ('p', "To further assess robustness, we re-estimate Equation (5) using alternative measures "
     "and subsamples; Table 4 summarizes the results for the youth-employment share. First, Column "
     "(1) replaces the dependent variable with the alternative measure based on the 35-year "
     "threshold (⟪YEMP2⟫); the coefficient on intelligent transformation remains positive and "
     "significant. Second, Column (2) replaces the explanatory variable with the text-based "
     "intelligent-transformation index (⟪TII⟫), and the result is unchanged. Third, Column (3) "
     "excludes the year 2020 to rule out potential confounding effects of the COVID-19 shock, and "
     "the estimated effect remains significantly positive. Fourth, Column (4) excludes firms "
     "listed after 2018 to mitigate composition effects from new listings, and the result is "
     "robust. Fifth, Column (5) restricts the sample to a balanced panel of firms observed in "
     "every sample year, mitigating concerns about entry and exit, and the coefficient "
     "remains positive and significant. Sixth, Column (6) reports two-way clustered standard "
     "errors at the firm and city levels. Finally, Column (7) further includes city-by-year fixed "
     "effects to control for time-varying local shocks, such as city-level talent-attraction "
     "policies. Across all specifications, the estimated effect of intelligent transformation on "
     "youth employment is consistently positive and statistically significant."),

    ('tabcap', 4, 'Robustness checks: alternative measures, sample restrictions, and fixed effects.'),
    ('table', [
        ['Variables', '(1)', '(2)', '(3)', '(4)', '(5)', '(6)', '(7)'],
        ['', ['Alt. DV', '(YEMP2)'], ['Alt. IV', '(TII)'], ['Excl.', '2020'], ['Excl. new', 'listings'],
         ['Balanced', 'panel'], ['Two-way', 'cluster'], ['City × Year', 'FE']],
        ['L.II', ['0.0148 ***', '(0.0044)'], ['0.0086 ***', '(0.0027)'], ['0.0121 ***', '(0.0038)'],
         ['0.0115 ***', '(0.0039)'], ['0.0126 ***', '(0.0043)'], ['0.0119 **', '(0.0047)'],
         ['0.0108 ***', '(0.0040)']],
        ['Controls', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Firm FE', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Year FE', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No'],
        ['Observations', '5,893', '6,124', '5,652', '5,417', '4,551', '6,124', '6,124'],
        ['R-squared', '0.618', '0.629', '0.641', '0.639', '0.643', '0.634', '0.662'],
    ], [1310, 1190, 1190, 1190, 1190, 1190, 1190, 1190]),
    ('notes', "Column (2) uses the text-based intelligent-transformation index as the explanatory "
     "variable. Column (6) reports two-way clustered standard errors (firm and city). *, **, and "
     "*** denote significance at the 10%, 5%, and 1% levels, respectively. Robust standard errors "
     "clustered at the firm level are reported in parentheses unless otherwise noted."),

    ('h3', '4.2.2. Propensity Score Matching'),

    ('p', "Our baseline estimates may be subject to endogeneity from firms' self-selection into "
     "intelligent transformation. To address this concern, we employ propensity score matching "
     "(PSM). We define ⟪II_{dummy}⟫ as an indicator equal to 1 for firms with intelligent "
     "transformation above the annual median and 0 otherwise, and estimate a probit model in the "
     "first stage using the baseline covariates and industry fixed effects. We implement "
     "one-to-one nearest-neighbor matching without replacement and impose a caliper of 0.01 to "
     "enhance comparability between the treatment and control groups {{psm}}. Table 5 reports the "
     "results before and after matching. The coefficient on ⟪II_{dummy}⟫ remains positive and "
     "statistically significant after matching, suggesting that our main finding is not driven by "
     "observable differences between high- and low-transformation firms. Figure 2 reports the "
     "signed standardized bias of each covariate before and after matching. After matching, the "
     "absolute standardized bias of every covariate falls from as high as 27.6% to below 5%, "
     "well within the conventional 10% threshold, indicating that the matching procedure "
     "achieves satisfactory covariate balance."),

    ('tabcap', 5, 'Robustness check: propensity score matching.'),
    ('table', [
        ['Variables', '(1)', '(2)'],
        ['', ['Pre-Match', 'YEMP'], ['Post-Match', 'YEMP']],
        ['II_dummy', ['0.0102 *', '(0.0058)'], ['0.0131 **', '(0.0061)']],
        ['Age', ['−0.0241 ***', '(0.0056)'], ['−0.0228 ***', '(0.0060)']],
        ['Size', ['−0.0119 ***', '(0.0031)'], ['−0.0113 ***', '(0.0034)']],
        ['Controls', 'Yes', 'Yes'],
        ['Firm FE', 'Yes', 'Yes'],
        ['Year FE', 'Yes', 'Yes'],
        ['Observations', '6,124', '4,682'],
        ['R-squared', '0.634', '0.629'],
    ], None),
    ('notes', "*, **, and *** denote significance at the 10%, 5%, and 1% levels, respectively. "
     "Robust standard errors clustered at the firm level are reported in parentheses."),

    ('figure', 'fig_psm.png', 4860000, 2659606, 2),
    ('figcap', 2, 'Covariate balance before and after matching. Hollow circles (crosses) show the '
     'signed standardized bias (%) of each covariate in the unmatched (matched) sample; covariates '
     'are ordered by absolute pre-match bias, and the dashed lines mark the conventional ±10% '
     'threshold.'),

    ('h3', '4.2.3. Instrumental Variable Regression'),

    ('p', "To further alleviate endogeneity concerns, we employ a two-stage least squares (2SLS) "
     "instrumental-variable approach. Following the shift-share (Bartik) tradition {{bartik}}, we "
     "construct the first instrument (IV1) as the robot penetration of the same industry in other "
     "East Asian economies interacted with the firm's baseline production exposure. Foreign "
     "industry-level robot adoption reflects global technological trends that affect the focal "
     "firm's transformation but are unlikely to directly determine its youth-employment share "
     "{{robots_us|robots_japan}}. Following the literature that uses geographic and "
     "infrastructural conditions as exogenous drivers of technology adoption {{broadband|pilot2}}, we "
     "use the second instrument (IV2), the historical density of fixed telephone lines in the "
     "firm's city interacted with a time trend, capturing local digital-infrastructure endowments. "
     "Table 6 reports the results. In the first stage, both instruments are positive and "
     "statistically significant, with Kleibergen–Paap first-stage F-statistics well above the "
     "weak-instrument threshold. In the second stage, the fitted value of intelligent "
     "transformation remains positively and significantly associated with youth employment, "
     "consistent with the baseline findings."),

    ('tabcap', 6, 'Robustness check: instrumental-variable regression.'),
    ('table', [
        ['Variables', '(1)', '(2)', '(3)', '(4)'],
        ['', ['First Stage', 'L.II'], ['Second Stage', 'YEMP'], ['First Stage', 'L.II'],
         ['Second Stage', 'YEMP']],
        ['IV1 (foreign robots)', ['0.386 ***', '(0.052)'], '', '', ''],
        ['IV2 (infrastructure)', '', '', ['0.242 ***', '(0.043)'], ''],
        ['L.II (fitted)', '', ['0.0217 ***', '(0.0071)'], '', ['0.0195 **', '(0.0084)']],
        ['Controls', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Firm FE', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Year FE', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['K–P F-statistic', '54.7', '', '31.6', ''],
        ['Observations', '6,124', '6,124', '6,124', '6,124'],
    ], None),
    ('notes', "Kleibergen–Paap first-stage F-statistics exceed the Stock–Yogo weak-instrument "
     "critical values. *, **, and *** denote significance at the 10%, 5%, and 1% levels, "
     "respectively. Robust standard errors clustered at the firm level are reported in "
     "parentheses."),

    ('h2', '4.3. Mechanism Analysis'),

    ('p', "Having established that intelligent transformation promotes youth employment and career "
     "development, we examine the underlying mechanisms. Drawing on our hypotheses, we consider "
     "two mediating channels: the firm skill structure (skill-restructuring effect) and labor "
     "productivity (expansion effect). We estimate the mediation models in Equations (6) and (7); "
     "Table 7 reports the results."),

    ('p', "Columns (1) and (2) report the skill-restructuring channel. Column (1) shows that "
     "intelligent transformation significantly upgrades the firm skill structure (⟪δ_{1}⟫ = "
     "0.0436, p < 0.01). Column (2) shows that a more skill-intensive structure is positively and "
     "significantly associated with youth employment (⟪φ_{1}⟫ = 0.048, p < 0.01), while the "
     "coefficient on intelligent transformation remains positive, consistent with partial "
     "mediation. These results support H2a, indicating that intelligent transformation promotes "
     "youth employment partly by raising the demand for young, high-skill workers. Columns (3) "
     "and (4) report the expansion channel. Column (3) shows that intelligent transformation "
     "significantly raises labor productivity (⟪δ_{1}⟫ = 0.0571, p < 0.01), and Column (4) shows "
     "that higher productivity is positively and significantly associated with youth employment "
     "(⟪φ_{1}⟫ = 0.0089, p < 0.01). This supports H2b. Bootstrap tests confirm that both indirect "
     "effects are statistically significant. A comparison of the indirect effects indicates that "
     "the skill-restructuring channel accounts for a larger share of the mediated effect "
     "than the expansion channel, suggesting that intelligent transformation promotes youth "
     "employment mainly by reconfiguring the skill composition of labor demand, with "
     "productivity-driven expansion serving as a complementary channel."),

    ('tabcap', 7, 'Mechanism analysis results.'),
    ('table', [
        ['Variables', '(1)', '(2)', '(3)', '(4)'],
        ['', 'SKILL', 'YEMP', 'lnPROD', 'YEMP'],
        ['L.II', ['0.0436 ***', '(0.0072)'], ['0.0098 ***', '(0.0036)'], ['0.0571 ***', '(0.0148)'],
         ['0.0106 ***', '(0.0037)']],
        ['SKILL', '', ['0.048 ***', '(0.011)'], '', ''],
        ['lnPROD', '', '', '', ['0.0089 ***', '(0.0021)']],
        ['Controls', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Firm FE', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Year FE', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Observations', '6,124', '6,124', '6,124', '6,124'],
        ['R-squared', '0.703', '0.641', '0.688', '0.638'],
    ], None),
    ('notes', "Columns (1)–(2) report the skill-restructuring channel; Columns (3)–(4) report the "
     "expansion (productivity) channel. *, **, and *** denote significance at the 10%, 5%, and 1% "
     "levels, respectively. Robust standard errors clustered at the firm level are reported in "
     "parentheses."),

    ('h2', '4.4. Moderating Effects of Multi-Level Employment Governance'),

    ('p', "Table 8 reports the moderating role of multi-level employment governance. Consistent "
     "with H3a–H3c, the interaction terms between intelligent transformation and the governance "
     "variables are positive and statistically significant. Column (1) shows that the interaction "
     "⟪L.II × TRAIN⟫ is positive and significant (⟪η_{3}⟫ = 0.0311, p < 0.05), indicating that "
     "firms with stronger training investment convert transformation into youth hiring more "
     "effectively, supporting H3a. Column (2) shows that the interaction ⟪L.II × PES⟫ is positive "
     "and significant (⟪η_{3}⟫ = 0.0158, p < 0.05), supporting H3b and indicating that regional "
     "public employment services reinforce the youth-employment benefits of transformation. "
     "Column (3) shows that the interaction ⟪L.II × POLICY⟫ is positive and significant (⟪η_{3}⟫ = "
     "0.0136, p < 0.05), supporting H3c and indicating that digital-economy policy pilots "
     "strengthen the transformation–youth-employment linkage. From a socio-economic systems "
     "perspective, these results show that employment governance is a key social-subsystem "
     "condition that helps regional systems translate industrial upgrading into youth-inclusive "
     "opportunity, and that differences in governance capacity partly explain heterogeneous "
     "youth-employment responses across firms and cities {{alm1|pilot1}}."),

    ('tabcap', 8, 'The moderating role of multi-level employment governance.'),
    ('table', [
        ['Variables', '(1)', '(2)', '(3)'],
        ['', 'YEMP', 'YEMP', 'YEMP'],
        ['L.II', ['0.0104 ***', '(0.0038)'], ['0.0109 ***', '(0.0037)'], ['0.0113 ***', '(0.0036)']],
        ['TRAIN', ['0.0218 **', '(0.0104)'], '', ''],
        ['L.II × TRAIN', ['0.0311 **', '(0.0128)'], '', ''],
        ['PES', '', ['0.0125', '(0.0093)'], ''],
        ['L.II × PES', '', ['0.0158 **', '(0.0071)'], ''],
        ['POLICY', '', '', ['0.0158 **', '(0.0067)']],
        ['L.II × POLICY', '', '', ['0.0136 **', '(0.0062)']],
        ['Controls', 'Yes', 'Yes', 'Yes'],
        ['Firm FE', 'Yes', 'Yes', 'Yes'],
        ['Year FE', 'Yes', 'Yes', 'Yes'],
        ['Observations', '6,124', '6,124', '6,124'],
        ['R-squared', '0.638', '0.636', '0.637'],
    ], None),
    ('notes', "TRAIN = firm training investment; PES = regional public employment services; "
     "POLICY = digital-economy policy pilots. Continuous moderators are mean-centered. *, **, and "
     "*** denote significance at the 10%, 5%, and 1% levels, respectively. Robust standard errors "
     "clustered at the firm level are reported in parentheses."),

    ('h2', '4.5. Heterogeneity Analysis'),

    ('p', "Building on the benchmark results, we explore whether the effect of intelligent "
     "transformation on youth employment differs across firms and locations within the regional "
     "system. We conduct subsample regressions along four dimensions: industry, firm size, "
     "ownership, and intra-provincial location. The results are reported in Table 9. Columns (1) "
     "and (2) show that the positive effect is significant for manufacturing firms but "
     "insignificant for services firms, consistent with the production-side nature of robot-based "
     "transformation. Columns (3) and (4) show that the effect is significant for large firms but "
     "not for small firms, reflecting differences in transformation capacity and internal labor "
     "markets. Columns (5) and (6) show that the effect is significant for non-state-owned firms "
     "but not for state-owned firms, consistent with stronger market-driven hiring flexibility in "
     "Zhejiang's private sector. Columns (7) and (8) show that the effect is stronger for firms "
     "registered in the digital core cities (Hangzhou and Ningbo) than for firms in the other "
     "cities of the province."),

    ('p', "Overall, the heterogeneity results suggest that the youth-employment benefits of "
     "intelligent transformation are concentrated among manufacturing, larger, non-state-owned, "
     "and digital-core-city firms. From a socio-economic systems perspective, these findings "
     "indicate that firms' youth-employment responses depend on the alignment among technological "
     "capacity, resource endowments, market-driven governance, and supportive regional ecosystems. "
     "Manufacturing and large firms possess greater capacity to reconfigure production systems and "
     "job structures; non-state-owned firms have stronger incentives and flexibility in "
     "recruitment; and digital-core-city firms benefit from denser digital infrastructure, talent "
     "pools, and policy experimentation {{digital_emp1|pilot1}}. Industrial intelligent "
     "transformation is therefore more likely to be translated into youth employment when firms "
     "have both stronger internal capabilities and stronger external ecosystem support for "
     "socio-technical adaptation."),

    ('tabcap', 9, 'Heterogeneity analysis results.'),
    ('table', [
        ['Variables', '(1)', '(2)', '(3)', '(4)', '(5)', '(6)', '(7)', '(8)'],
        ['', 'Manuf.', 'Services', 'Large', 'Small', ['Non-', 'SOE'], 'SOE', ['Core', 'cities'],
         ['Other', 'cities']],
        ['L.II', ['0.0141 ***', '(0.0042)'], ['0.0054', '(0.0058)'], ['0.0138 ***', '(0.0043)'],
         ['0.0052', '(0.0064)'], ['0.0132 ***', '(0.0040)'], ['0.0061', '(0.0069)'],
         ['0.0149 ***', '(0.0046)'], ['0.0071 *', '(0.0042)']],
        ['Controls', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Firm FE', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Year FE', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'],
        ['Observations', '4,238', '1,886', '3,062', '3,062', '4,936', '1,188', '2,975', '3,149'],
        ['R-squared', '0.647', '0.619', '0.652', '0.611', '0.641', '0.628', '0.649', '0.622'],
    ], [1240, 1050, 1050, 1050, 1050, 1050, 1050, 1050, 1050]),
    ('notes', "Core cities are Hangzhou and Ningbo; large (small) firms are those above (below) "
     "the annual median of total assets. *, **, and *** denote significance at the 10%, 5%, and "
     "1% levels, respectively. Robust standard errors clustered at the firm level are reported in "
     "parentheses."),
]
