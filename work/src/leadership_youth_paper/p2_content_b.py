# -*- coding: utf-8 -*-
"""Paper 2 content, part B: Results, Discussion, Conclusions, back matter."""

PART_B = [
    ('h1', '4. Results'),

    ('h2', '4.1. Cross-Sectional Relationships Between Enterprise Digital Leadership and Youth Labor-Market Outcomes'),

    ('p', "Across the 27 EU countries, the four digital-leadership indicators display wide "
     "variation: the share of enterprises employing ICT specialists ranges from 9.7% to 36.1% "
     "(mean 21.5%), ICT training from 6.3% to 44.3% (mean 23.0%), AI use from 2.0% to 31.9% "
     "(mean 14.3%), and data analytics from 8.0% to 48.4% (mean 31.4%). The youth employment rate "
     "averages 48.3% (range 32.2–72.0%) and the NEET rate 10.4% (range 4.2–20.6%). The first "
     "multivariate model analyzed the association between the employment of ICT specialists "
     "(⟪EDL_SPEC⟫) and the two youth labor-market indicators. The multivariate tests indicate a "
     "significant global association with a large effect size (Pillai's Trace = 0.605, Wilks' "
     "Lambda = 0.395, F(2, 24) = 18.400, p < 0.001), suggesting that the prevalence of dedicated "
     "digital specialists is associated with both youth indicators. At the univariate level, "
     "⟪EDL_SPEC⟫ is associated with approximately 51% of the cross-sectional variance in the "
     "youth employment rate and 50% of the variation in the NEET rate. Higher shares of "
     "specialist-employing enterprises are associated with a significantly larger youth "
     "employment rate and, at the same time, a lower NEET rate (Table 2)."),

    ('tabcap', 2, 'Parameter estimates for the relationship between the employment of ICT '
     'specialists and youth labor-market indicators.'),
    ('table', [
        ['Dependent Variable', 'Parameter', 'B', 'Std. Error', 't', 'Sig.',
         ['95% CI', 'Lower'], ['95% CI', 'Upper'], ['Partial Eta', 'Squared']],
        ['YER', 'Intercept', '30.223', '3.771', '8.014', '0.000', '22.456', '37.990', '0.720'],
        ['', 'EDL_SPEC', '0.840', '0.166', '5.057', '0.000', '0.498', '1.182', '0.506'],
        ['NEET', 'Intercept', '17.866', '1.560', '11.451', '0.000', '14.652', '21.079', '0.840'],
        ['', 'EDL_SPEC', '−0.345', '0.069', '−5.027', '0.000', '−0.487', '−0.204', '0.503'],
    ], [1750, 1290, 1030, 1120, 940, 850, 890, 890, 880]),
    ('notes', "Source: authors’ calculations. Note: N = 27. CI = confidence interval."),

    ('p', "The curve-fit analysis suggests a linear relationship between ⟪EDL_SPEC⟫ and both "
     "outcomes. Figure 1 illustrates divergent trajectories for the two dependent variables: the "
     "youth employment rate shows an upward trend, whereas the NEET rate exhibits a downward "
     "slope as the prevalence of ICT specialists increases."),

    ('figure', 'p2_fig1.png', 4390000, 5060000, 1),
    ('figcap', 1, 'Youth employment rate (YER) and NEET rate according to the share of '
     'enterprises employing ICT specialists (EDL_SPEC). Source: authors’ design.'),

    ('p', "The second model evaluated the provision of ICT training (⟪EDL_TRAIN⟫). The "
     "multivariate effect remains significant and substantial (Pillai's Trace = 0.479, Wilks' "
     "Lambda = 0.521, F(2, 24) = 11.050, p < 0.001). At the individual level, ⟪EDL_TRAIN⟫ is "
     "positively associated with the youth employment rate (p = 0.001) and negatively with the "
     "NEET rate (p < 0.001), accounting for roughly 38% and 41% of their respective variances. "
     "Training decisions thus correlate almost as strongly with youth outcomes as specialist "
     "employment, consistent with the interpretation that internal skill-formation systems ease "
     "the integration of young workers (Table 3, Figure 2)."),

    ('tabcap', 3, 'Parameter estimates for the relationship between the provision of ICT training '
     'and youth labor-market indicators.'),
    ('table', [
        ['Dependent Variable', 'Parameter', 'B', 'Std. Error', 't', 'Sig.',
         ['95% CI', 'Lower'], ['95% CI', 'Upper'], ['Partial Eta', 'Squared']],
        ['YER', 'Intercept', '34.357', '3.777', '9.097', '0.000', '26.579', '42.136', '0.768'],
        ['', 'EDL_TRAIN', '0.605', '0.153', '3.949', '0.001', '0.290', '0.921', '0.384'],
        ['NEET', 'Intercept', '16.397', '1.520', '10.786', '0.000', '13.266', '19.528', '0.823'],
        ['', 'EDL_TRAIN', '−0.259', '0.062', '−4.197', '0.000', '−0.386', '−0.132', '0.413'],
    ], [1750, 1290, 1030, 1120, 940, 850, 890, 890, 880]),
    ('notes', "Source: authors’ calculations. Note: N = 27. CI = confidence interval."),

    ('figure', 'p2_fig2.png', 4390000, 5060000, 2),
    ('figcap', 2, 'Youth employment rate (YER) and NEET rate according to the share of '
     'enterprises providing ICT training (EDL_TRAIN). Source: authors’ design.'),

    ('p', "The third model, centered on the use of AI technologies (⟪EDL_AI⟫), points to a "
     "weaker but still significant systemic association (Pillai's Trace = 0.342, Wilks' Lambda = "
     "0.658, F(2, 24) = 6.239, p = 0.007). ⟪EDL_AI⟫ explains approximately 24% of the variation "
     "in the youth employment rate (p = 0.009) and 32% of the variation in the NEET rate "
     "(p = 0.002). An increase in enterprise AI adoption is associated simultaneously with higher "
     "youth employment and a consistent decrease in the NEET rate, although the strength of the "
     "association is clearly below that of the capability-building indicators (Table 4, "
     "Figure 3)."),

    ('tabcap', 4, 'Parameter estimates for the relationship between enterprise AI use and youth '
     'labor-market indicators.'),
    ('table', [
        ['Dependent Variable', 'Parameter', 'B', 'Std. Error', 't', 'Sig.',
         ['95% CI', 'Lower'], ['95% CI', 'Upper'], ['Partial Eta', 'Squared']],
        ['YER', 'Intercept', '40.105', '3.264', '12.286', '0.000', '33.382', '46.828', '0.858'],
        ['', 'EDL_AI', '0.575', '0.204', '2.821', '0.009', '0.155', '0.995', '0.241'],
        ['NEET', 'Intercept', '14.311', '1.277', '11.210', '0.000', '11.682', '16.940', '0.834'],
        ['', 'EDL_AI', '−0.272', '0.080', '−3.414', '0.002', '−0.437', '−0.108', '0.318'],
    ], [1750, 1290, 1030, 1120, 940, 850, 890, 890, 880]),
    ('notes', "Source: authors’ calculations. Note: N = 27. CI = confidence interval."),

    ('figure', 'p2_fig3.png', 4390000, 5060000, 3),
    ('figcap', 3, 'Youth employment rate (YER) and NEET rate according to the share of '
     'enterprises using AI technologies (EDL_AI). Source: authors’ design.'),

    ('p', "The final model investigated the performance of data analytics (⟪EDL_DA⟫), the most "
     "direct marker of data-driven decision making. The multivariate effect remains significant "
     "but is the weakest of the four (Pillai's Trace = 0.271, Wilks' Lambda = 0.729, F(2, 24) = "
     "4.458, p = 0.023). ⟪EDL_DA⟫ shows a statistically significant positive association with "
     "the youth employment rate (p = 0.013) and a negative association with the NEET rate "
     "(p = 0.012), each accounting for roughly 22–23% of the cross-sectional variance. This "
     "result suggests that data-driven decision making relates to youth outcomes mainly as part "
     "of a broader capability configuration rather than as an isolated tool (Table 5, "
     "Figure 4)."),

    ('tabcap', 5, 'Parameter estimates for the relationship between enterprise data analytics and '
     'youth labor-market indicators.'),
    ('table', [
        ['Dependent Variable', 'Parameter', 'B', 'Std. Error', 't', 'Sig.',
         ['95% CI', 'Lower'], ['95% CI', 'Upper'], ['Partial Eta', 'Squared']],
        ['YER', 'Intercept', '34.923', '5.220', '6.691', '0.000', '24.173', '45.674', '0.642'],
        ['', 'EDL_DA', '0.427', '0.159', '2.677', '0.013', '0.098', '0.755', '0.223'],
        ['NEET', 'Intercept', '16.017', '2.145', '7.467', '0.000', '11.599', '20.435', '0.690'],
        ['', 'EDL_DA', '−0.178', '0.066', '−2.720', '0.012', '−0.313', '−0.043', '0.228'],
    ], [1750, 1290, 1030, 1120, 940, 850, 890, 890, 880]),
    ('notes', "Source: authors’ calculations. Note: N = 27. CI = confidence interval."),

    ('figure', 'p2_fig4.png', 4390000, 5060000, 4),
    ('figcap', 4, 'Youth employment rate (YER) and NEET rate according to the share of '
     'enterprises performing data analytics (EDL_DA). Source: authors’ design.'),

    ('p', "Overall, the four models suggest a clear gradient rather than uniform associations. "
     "The capability-building dimensions of digital leadership—employing ICT specialists and "
     "training personnel—are most strongly associated with both youth labor-market indicators, "
     "while the deployment dimensions—AI use and data analytics—show weaker though still "
     "significant associations. Therefore, H1 is supported, with the qualification that the "
     "strength of the association differs systematically across the dimensions of digital "
     "leadership."),

    ('p', "Given the low values recorded for Romania across several indicators, an additional "
     "robustness check was conducted by excluding Romania from the sample. The direction of all "
     "associations remained unchanged and the capability-building models remained significant at "
     "the 1% level; however, the multivariate significance of the AI model weakened to p = 0.029 "
     "and that of the data-analytics model to the 5% boundary (p = 0.044). These results suggest that the weaker deployment-side "
     "associations are somewhat sensitive to country-level outliers and should be interpreted as "
     "exploratory cross-sectional associations."),

    ('p', "To address the possible role of broader structural country characteristics, a "
     "supplementary bivariate correlation analysis was conducted. The four digital-leadership "
     "indicators were correlated with contextual variables available in the dataset, namely the "
     "share of the population aged 25–34 with tertiary education, R&D intensity (gross domestic "
     "expenditure on R&D as a share of GDP), and real labour productivity per person (Table 6). "
     "This analysis was not intended to replace a controlled regression model, but rather to "
     "provide a robustness check on whether digital leadership covaries with broader educational "
     "and productivity-related country characteristics."),

    ('tabcap', 6, 'Supplementary bivariate correlations with structural contextual variables.'),
    ('table', [
        ['Structural Contextual Variable', 'EDL_SPEC', 'EDL_TRAIN', 'EDL_AI', 'EDL_DA'],
        ['Tertiary education share (PTE)', '0.501 (p = 0.008)', '0.491 (p = 0.009)',
         '0.453 (p = 0.018)', '0.368 (p = 0.059)'],
        ['R&D intensity (GERD)', '0.587 (p = 0.001)', '0.725 (p < 0.001)',
         '0.767 (p < 0.001)', '0.486 (p = 0.010)'],
        ['Real labour productivity per person (RLPP)', '0.616 (p = 0.001)', '0.492 (p = 0.009)',
         '0.430 (p = 0.025)', '0.530 (p = 0.004)'],
    ], [2960, 1670, 1670, 1670, 1670]),
    ('notes', "Source: authors’ calculations. Note: Pearson correlation coefficients are "
     "reported, with p-values in parentheses. N = 27. PTE = population aged 25–34 with tertiary "
     "education; GERD = gross domestic expenditure on R&D as a share of GDP; RLPP = real labour "
     "productivity per person."),

    ('p', "The supplementary correlations indicate that enterprise digital leadership is not "
     "independent of broader structural country characteristics. The strongest and most "
     "consistent positive associations are observed with R&D intensity and productivity, while "
     "the correlation between data analytics and tertiary education is only marginal. These "
     "results suggest that the observed relationships between digital leadership and youth "
     "labor-market indicators may partly overlap with broader differences in innovation capacity "
     "and productivity across countries. Therefore, the main results should continue to be "
     "interpreted as exploratory cross-sectional associations rather than as estimates of the "
     "independent effect of digital leadership."),

    ('h2', '4.2. The Latent Dimension of Organizational Digital Leadership Capability and Its Systemic Associations'),

    ('p', "The exploratory factor analysis aimed to reduce the four observable variables to a "
     "common factor structure, capturing the aggregate process by which multiple leadership "
     "decisions articulate into a cohesive socio-technical dynamic. The KMO value of 0.797, the "
     "significance of Bartlett's test (χ² = 85.338; df = 6; p < 0.001), and significant "
     "correlations among the variables indicate that the data are suitable for extracting a "
     "common latent construct (Table 7). The factorial solution converges to a single factor "
     "that accounts for 74.4% of the overall variance after extraction, indicating a unified "
     "dimension of organizational digital leadership capability across enterprise populations."),

    ('p', "The communalities indicate that the common latent factor effectively represents the "
     "employment of ICT specialists, the provision of ICT training, and AI use. By contrast, "
     "⟪EDL_DA⟫ has a considerably lower extracted communality (0.390), suggesting that data "
     "analytics shares less variance with the other indicators. This finding does not justify "
     "excluding the variable, since its factor loading remains positive and meaningful (0.625), "
     "but it indicates that data-driven decision making captures a more specific dimension of "
     "digital leadership. Therefore, the latent factor mainly reflects capability building and AI "
     "deployment, while the data-analytics dimension should be interpreted more cautiously."),

    ('tabcap', 7, 'Exploratory factor analysis of enterprise digital-leadership indicators.'),
    ('table', [
        ['Indicator/Statistic', 'Value'],
        ['Kaiser–Meyer–Olkin measure', '0.797'],
        ['Bartlett’s test of sphericity', 'χ² = 85.338; df = 6; p < 0.001'],
        ['Extraction method', 'Principal Axis Factoring'],
        ['Number of factors extracted', '1'],
        ['Initial eigenvalue, Factor 1', '3.182'],
        ['Initial variance explained', '79.556%'],
        ['Extraction sum of squared loadings', '2.975'],
        ['Variance explained after extraction', '74.379%'],
        ['Rotation', 'No rotation'],
        ['Communalities (initial/extraction) — EDL_SPEC', '0.772/0.842; loading 0.918'],
        ['Communalities (initial/extraction) — EDL_TRAIN', '0.861/0.946; loading 0.973'],
        ['Communalities (initial/extraction) — EDL_AI', '0.818/0.796; loading 0.892'],
        ['Communalities (initial/extraction) — EDL_DA', '0.424/0.390; loading 0.625'],
    ], [5140, 4500]),
    ('notes', "Source: authors’ calculations."),

    ('p', "This latent factor, labelled ⟪FACT_EDL⟫, reflects an emerging construct of the "
     "socio-technical system of work, in which enterprise-level leadership decisions aggregate "
     "into a coherent macro-level signal of digital capability. The first regression analyzed the "
     "relationship between ⟪FACT_EDL⟫ and the youth employment rate. The model indicates a "
     "positive and statistically significant relationship, with a correlation coefficient of "
     "0.665 and an explanatory capacity of approximately 44% of the variation in youth employment "
     "(R² = 0.442; adjusted R² = 0.420). The F test indicates that the model is statistically "
     "significant (F = 19.803, p < 0.001). Given the cross-sectional structure of the data and "
     "the absence of a meaningful ordering of countries, no autocorrelation interpretation is "
     "reported (Table 8)."),

    ('tabcap', 8, 'Regression results for the relationship between the latent digital-leadership '
     'factor and the youth employment rate.'),
    ('table', [
        ['Model summary', 'R', 'R Square', ['Adjusted', 'R Square'], ['Std. Error of', 'the Estimate']],
        ['', '0.665', '0.442', '0.420', '6.615'],
        ['ANOVA', ['Sum of', 'Squares'], 'df', ['Mean', 'Square'], 'F (Sig.)'],
        ['Regression', '866.434', '1', '866.434', '19.803 (p < 0.001)'],
        ['Residual', '1093.824', '25', '43.753', ''],
        ['Total', '1960.259', '26', '', ''],
        ['Coefficients', 'B', ['Std.', 'Error'], ['Beta', '(standardized)'], 't (Sig.)'],
        ['(Constant)', '48.307', '1.273', '', '37.933 (p < 0.001)'],
        ['FACT_EDL', '5.770', '1.298', '0.665', '4.446 (p < 0.001)'],
    ], [2340, 1930, 1790, 1790, 1790]),
    ('notes', "Source: authors’ calculations."),

    ('p', "The regression coefficient indicates that, on average, a one-unit rise in the factor "
     "score is associated with an increase of about 5.8 percentage points in the youth employment "
     "rate (B = 5.770, p < 0.001). The standardized coefficient (β = 0.665) indicates a moderate "
     "to strong association, suggesting that the latent dimension of digital leadership is "
     "significantly associated with youth workforce participation. In socio-technical terms, "
     "these results suggest that the latent factor may be interpreted as a broader indicator of "
     "organizational digital capability among national enterprise populations. Its positive "
     "association with youth employment is consistent with the idea that digital leadership, "
     "skills formation, and youth labor-market integration co-occur in more digitally prepared "
     "national contexts. However, this interpretation remains exploratory and should not be taken "
     "as evidence that digital leadership increases youth employment."),

    ('p', "The second regression examines the association between ⟪FACT_EDL⟫ and the NEET rate. "
     "The model shows a substantial negative association (R = 0.682, with a negative slope) and explains around 47% of "
     "the variation in the NEET rate (R² = 0.465; adjusted R² = 0.444). The F test indicates that "
     "the model is statistically significant (F = 21.729, p < 0.001) (Table 9)."),

    ('tabcap', 9, 'Regression results for the relationship between the latent digital-leadership '
     'factor and the NEET rate.'),
    ('table', [
        ['Model summary', 'R', 'R Square', ['Adjusted', 'R Square'], ['Std. Error of', 'the Estimate']],
        ['', '0.682', '0.465', '0.444', '2.671'],
        ['ANOVA', ['Sum of', 'Squares'], 'df', ['Mean', 'Square'], 'F (Sig.)'],
        ['Regression', '155.039', '1', '155.039', '21.729 (p < 0.001)'],
        ['Residual', '178.378', '25', '7.135', ''],
        ['Total', '333.416', '26', '', ''],
        ['Coefficients', 'B', ['Std.', 'Error'], ['Beta', '(standardized)'], 't (Sig.)'],
        ['(Constant)', '10.430', '0.514', '', '20.294 (p < 0.001)'],
        ['FACT_EDL', '−2.443', '0.524', '−0.682', '−4.664 (p < 0.001)'],
    ], [2340, 1930, 1790, 1790, 1790]),
    ('notes', "Source: authors’ calculations."),

    ('p', "The regression coefficient indicates that, on average, a one-unit increase in the "
     "factor score is associated with a decrease of around 2.4 percentage points in the NEET "
     "rate (B = −2.443, p < 0.001). The standardized coefficient (β = −0.682) indicates a "
     "moderate-to-strong relationship, implying that the latent dimension of digital leadership "
     "is consistently associated with lower youth exclusion. From a socio-technical perspective, "
     "the negative association between ⟪FACT_EDL⟫ and the NEET rate suggests that countries whose "
     "enterprises invest more coherently in digital capabilities also tend to integrate their "
     "young people more successfully. This pattern may reflect broader differences in "
     "productivity, digital readiness, organizational adaptation, or economic structure, but the "
     "cross-sectional data do not allow these mechanisms to be tested directly. These results "
     "provide exploratory support for H2 by showing that the latent factor of digital leadership "
     "is statistically associated with both youth labor-market indicators."),

    ('h2', '4.3. Emerging Socio-Technical Typologies: National Profiles of Digital Leadership and Youth Labor-Market Dynamics'),

    ('p', "To explore the latent structure of the relationships between enterprise digital "
     "leadership and youth labor-market indicators, the analysis began with hierarchical "
     "clustering, using the average linkage method and a correlation-based proximity measure "
     "between country profiles. The dendrogram presented in Figure 5 suggests a possible "
     "two-group structure in the sample. Following this exploratory indication, the k-means "
     "algorithm was applied to describe two country profiles. The resulting two-cluster solution "
     "should be interpreted as an exploratory and descriptive typology, not as a definitive "
     "classification of European countries. The k-means partition agrees with the hierarchical "
     "two-group cut for 26 of the 27 countries, indicating a stable exploratory structure."),

    ('figure', 'p2_fig5.png', 4860000, 4490000, 5),
    ('figcap', 5, 'Dendrogram of the hierarchical clustering of European countries based on '
     'enterprise digital leadership and youth labor-market indicators. Source: authors’ design.'),

    ('p', "The cluster centers provide a synthetic view of the two exploratory typologies. In the "
     "first cluster (11 countries), the average levels are 28.5% for enterprises employing ICT "
     "specialists, 31.1% for ICT training, 20.9% for AI use, and 38.3% for data analytics. These "
     "leadership profiles are associated with an average youth employment rate of 54.7% and a "
     "NEET rate of 7.7%. This profile corresponds to an environment with strong digital "
     "leadership capability and favorable youth labor-market dynamics, with high participation "
     "and low exclusion. Conversely, the second cluster (16 countries) has substantially lower "
     "levels across all dimensions of digital leadership: 16.7% for ICT specialists, 17.5% for "
     "training, 9.7% for AI use, and 26.6% for data analytics. This technological profile is "
     "marked by a lower youth employment rate of 43.9% and a considerably higher NEET rate of "
     "12.3%. The resulting typology suggests a less digitally led socio-technical system, in "
     "which weaker organizational capability building is associated with more severe youth "
     "labor-market difficulties."),

    ('p', "As a minimal validation metric, the average silhouette coefficient was computed for "
     "the final two-cluster solution using the six variables included in the clustering "
     "procedure. The average silhouette coefficient is 0.382, with mean values of 0.340 for "
     "Cluster 1 and 0.411 for Cluster 2. These positive values suggest that the two-cluster "
     "solution has acceptable internal coherence for exploratory purposes, although the level of "
     "separation should not be interpreted as strong. Therefore, the silhouette results support "
     "the descriptive usefulness of the two-cluster typology and confirm that the classification "
     "should remain exploratory rather than definitive. The ANOVA results provide a descriptive "
     "characterization of the differences between the two clusters (Table 10)."),

    ('tabcap', 10, 'Differences between clusters for enterprise digital leadership and youth '
     'labor-market indicators (ANOVA).'),
    ('table', [
        ['Variable', ['Cluster', 'Mean Square'], 'df', ['Error', 'Mean Square'], 'df', 'F', 'Sig.'],
        ['EDL_SPEC', '904.669', '1', '20.049', '25', '45.122', '0.000'],
        ['EDL_TRAIN', '1192.604', '1', '34.533', '25', '34.535', '0.000'],
        ['EDL_AI', '828.504', '1', '24.057', '25', '34.439', '0.000'],
        ['EDL_DA', '905.018', '1', '59.744', '25', '15.148', '0.001'],
        ['YER', '752.102', '1', '48.326', '25', '15.563', '0.001'],
        ['NEET', '137.387', '1', '7.841', '25', '17.521', '0.000'],
    ], [1600, 1650, 800, 1650, 800, 1570, 1570]),
    ('notes', "Source: authors’ calculations."),

    ('p', "The high F values for ICT specialists, training, and AI use indicate that these "
     "variables strongly influence cluster separation and are the primary markers of "
     "socio-technical divergence. The observed disparities in the youth employment rate and the "
     "NEET rate indicate that the two exploratory profiles differ not only in digital leadership "
     "but also in youth labor-market characteristics. These ANOVA results should be interpreted "
     "with caution: because the clusters were formed using the same variables that are "
     "subsequently compared, the F values are descriptive and should not be treated as "
     "independent hypothesis tests."),

    ('p', "Table A1 in Appendix A shows the composition of each country across the two clusters, "
     "with a strong concentration of Nordic and Western European economies in the digitally led "
     "category, joined by Slovenia and Malta. The second cluster is primarily composed of "
     "Southern, Central, and Eastern European countries together with France. From the "
     "perspective of complex adaptive systems, these findings show how interactions among "
     "technology, human capital, organizational decision making, and institutional frameworks "
     "produce persistent, emerging patterns {{stsd1|sts4}}. The discovered clusters are "
     "socio-technical regimes in which the co-evolution of digital leadership, youth engagement, "
     "and skill formation produces distinct paths of economic adaptability. Overall, the cluster "
     "analysis supports Hypothesis H3, that European countries can be grouped into meaningful "
     "typologies based on the profiles of enterprise digital leadership and youth labor-market "
     "indicators. The typologies compare socio-technical regimes with varying degrees of digital "
     "capability, youth participation, and exclusion, thus presenting a full picture of the "
     "heterogeneity of digital transformation in Europe."),

    ('h1', '5. Discussion'),

    ('p', "The data suggest a differentiated pattern of associations between enterprise digital "
     "leadership, data-driven decision making, and youth labor-market outcomes across European "
     "countries. Rather than implying a causal process, these findings point to cross-sectional "
     "co-occurrences that may reflect broader socio-technical and economic conditions. This "
     "interpretation is consistent with the literature, which characterizes digital "
     "transformation as a systemic phenomenon whose labor-market effects depend on the adoption "
     "context and on the complementarities between technology and the human factor "
     "{{sts2|acemoglu2019|eu1}}."),

    ('p', "The four models should not be interpreted as comparing the independent or partial "
     "contribution of each leadership dimension. Since the digital-leadership variables are "
     "conceptually related and highly correlated, each single-predictor model may partly reflect "
     "the same broader underlying pattern of digital capability. For this reason, the results are "
     "interpreted as simple cross-sectional associations, while the exploratory factor analysis "
     "provides a complementary means of summarizing their common latent structure. The observed "
     "associations should also be interpreted in relation to broader national development "
     "conditions, since countries with higher income levels, stronger digital infrastructure, "
     "higher educational attainment, and greater R&D intensity may be more likely to build "
     "enterprise digital capabilities earlier and more intensively—a pattern confirmed by the "
     "supplementary correlations with tertiary education, R&D intensity, and productivity."),

    ('p', "The results of the multivariate models support H1 with a clear gradient. The "
     "capability-building dimensions of digital leadership—employing ICT specialists and "
     "providing ICT training—are most strongly associated with youth labor-market performance. "
     "This pattern is consistent with the upper-echelons argument that leadership commitments to "
     "digital human capital are the binding constraint of transformation {{upper1|dl2}}, and with "
     "evidence that training and automation technologies are complements rather than substitutes "
     "in modern workplaces {{training1|training2}}. It also aligns with cross-country evidence "
     "that digitalization is associated with lower youth unemployment {{basol|ogbonna}}. For "
     "young workers specifically, enterprises with specialist teams and training systems offer "
     "structured entry ports: professional digital roles, apprenticeship-like skill development, "
     "and career ladders in which recently acquired digital skills are valued {{eu1|career1}}."),

    ('p', "The deployment dimensions—AI use and data analytics—show weaker although still "
     "significant associations. This finding echoes the task-based literature, in which the "
     "employment effects of AI and automation are theoretically ambiguous, combining displacement "
     "of routine entry-level tasks with the creation of new digitally intensive activities "
     "{{acemoglu2019|acemoglu2022|genai1}}. Recent experimental evidence indicates that "
     "generative AI disproportionately raises the productivity of less experienced workers "
     "{{genai2|genai3}}, which may benefit young employees inside adopting organizations, but our "
     "country-level associations suggest that deployment alone is a weaker marker of "
     "youth-inclusive digital transformation than the leadership decision to build human digital "
     "capability. The lower communality of data analytics in the factor solution reinforces this "
     "reading: data-driven decision making captures a partly distinct dimension of organizational "
     "practice {{ddm1|bda1}}, whose youth-employment implications depend on the capability "
     "context in which it is embedded."),

    ('p', "The second hypothesis is supported by the latent factor of digital leadership derived "
     "from factor analysis and regression models. The KMO score, the significance of Bartlett's "
     "test, and the presence of a single component explaining about three-quarters of the total "
     "variance suggest that the four dimensions are not independent occurrences but rather "
     "represent a shared dimension of organizational digital capability. The latent factor is "
     "strongly positively associated with youth employment and negatively with the NEET rate. "
     "This outcome aligns with the notion of digital leadership as an aggregate process—the "
     "fusion of specialist talent, workforce training, AI deployment, and data-driven decision "
     "routines into a general profile of organizational adaptability to the digital economy "
     "{{dl1|dl3|ddm2}}. This finding theoretically supports the socio-technical systems "
     "perspective, which posits that technology does not produce effects solely through its "
     "technical availability, but rather in conjunction with organizational processes, human "
     "skills, and institutional frameworks {{sts1|sts2|sts4}}."),

    ('p', "The cluster analysis, finally, situates these associations in space. The two "
     "exploratory typologies—a digitally led, youth-inclusive regime concentrated in Northern "
     "and Western Europe, and a lagging regime spanning Southern, Central, and Eastern Europe—"
     "mirror known patterns of the European digital divide {{eu2|eu3}} and extend them by showing "
     "that the divide is jointly organizational and generational: where enterprise digital "
     "leadership is weak, young people are both less employed and more excluded. For "
     "policymakers, this suggests that youth employment strategies and enterprise digitalization "
     "policies are complementary levers of the same socio-technical system, and that active "
     "labor-market programs for youth are likely to be more effective when they are coordinated "
     "with programs that raise the digital capability of enterprises {{alm1|alm2|yg}}."),

    ('h1', '6. Conclusions'),

    ('p', "Using harmonized Eurostat data for the 27 European Union countries, this study "
     "examined how four enterprise-level dimensions of digital leadership and data-driven "
     "decision making—the employment of ICT specialists, the provision of ICT training, the use "
     "of AI technologies, and the performance of data analytics—relate to the youth employment "
     "rate and the NEET rate. The analysis combined MANOVA-type multivariate general linear "
     "models, exploratory factor analysis, and hierarchical and k-means clustering within a "
     "socio-technical systems framework."),

    ('p', "Three main findings emerge. First, all four dimensions of enterprise digital "
     "leadership are significantly associated with youth labor-market outcomes, with a clear "
     "gradient: capability-building decisions (specialists and training) show the strongest "
     "associations, while technology-deployment decisions (AI and data analytics) show weaker "
     "ones. Second, the four dimensions share a single latent factor of organizational digital "
     "leadership capability, which explains about three-quarters of their common variance and is "
     "strongly associated with higher youth employment (β = 0.665) and lower NEET rates "
     "(β = −0.682). Third, European countries form two exploratory socio-technical typologies—a "
     "digitally led, youth-inclusive regime and a lagging regime—confirming that digital "
     "leadership and youth opportunity co-evolve into persistent national configurations."),

    ('p', "The findings carry implications for leaders and policymakers navigating digital "
     "transformation. For organizational leaders, the results suggest that the youth-inclusive "
     "potential of digital transformation lies less in the adoption of particular technologies "
     "than in the decision to build digital capability: recruiting specialist talent, training "
     "the workforce, and institutionalizing data-driven decision processes. Digital "
     "transformation strategies that pair AI deployment with human-capital investment are the "
     "configurations in which young workers appear to thrive. For policymakers, the typologies "
     "indicate that closing Europe's digital divide is simultaneously a youth-employment policy: "
     "support for enterprise digital capability building—particularly in Southern, Central, and "
     "Eastern Europe—complements active labor-market programs for young people, and the two "
     "policy families are likely to reinforce each other within the same socio-technical "
     "system."),

    ('p', "This study has several limitations that provide directions for future research. "
     "First, the analysis is cross-sectional and country-level: it identifies associations, not "
     "causal effects, and aggregation may mask within-country heterogeneity across sectors, firm "
     "sizes, and regions. Panel data on enterprise digitalization and youth outcomes would allow "
     "dynamic and quasi-experimental designs. Second, the sample of 27 countries is small for "
     "multivariate analysis; the parsimonious specifications adopted here mitigate but do not "
     "eliminate this constraint, and the factor and cluster solutions should be treated as "
     "exploratory. Third, the enterprise indicators capture the prevalence of digital "
     "capabilities, not their quality or depth; linked employer–employee data would permit "
     "analyzing which young people are hired into digitally led organizations and how their "
     "careers develop. Finally, future research could extend the framework beyond the EU and "
     "incorporate direct measures of leadership styles and decision-making processes from "
     "management surveys, connecting the macro-level typologies identified here to the "
     "micro-level behavior of leaders navigating digital transformation {{dl1|stsd2}}."),

    ('back', 'Author Contributions:', "Conceptualization, X.C. and T.M.; methodology, X.C.; "
     "software, X.C.; validation, X.C., D.H. and T.M.; formal analysis, X.C.; investigation, "
     "D.H.; resources, T.M.; data curation, D.H.; writing—original draft preparation, X.C.; "
     "writing—review and editing, T.M.; visualization, D.H.; supervision, T.M.; project "
     "administration, T.M.; funding acquisition, X.C. All authors have read and agreed to the "
     "published version of the manuscript."),

    ('back', 'Funding:', "This research was funded by the Zhejiang Provincial Philosophy and "
     "Social Sciences Planning Special Project on Higher Education Basic Research Funding Reform "
     "(Grant Number: 25NDJC153YBMS) and the Major Humanities and Social Sciences Research "
     "Projects in Zhejiang Higher Education Institutions (Grant Number: 2024QN018)."),

    ('back', 'Institutional Review Board Statement:', "Not applicable."),

    ('back', 'Informed Consent Statement:', "Not applicable."),

    ('back', 'Data Availability Statement:', "The data analyzed in this study are publicly "
     "available from Eurostat (https://ec.europa.eu/eurostat). The processed dataset and analysis "
     "code are available from the authors upon reasonable request."),

    ('back', 'Conflicts of Interest:', "The authors declare no conflicts of interest."),

    ('h1', 'Appendix A'),

    ('p', "Table A1 presents the composition of the two exploratory clusters."),

    ('tabcap', 'A1', 'Cluster membership of the EU-27 countries.'),
    ('table', [
        ['Cluster', 'Countries'],
        ['Cluster 1 — digitally led, youth-inclusive (n = 11)',
         'Austria, Belgium, Denmark, Finland, Germany, Ireland, Luxembourg, Malta, Netherlands, Slovenia, Sweden'],
        ['Cluster 2 — lagging digital leadership (n = 16)',
         'Bulgaria, Croatia, Cyprus, Czechia, Estonia, France, Greece, Hungary, Italy, Latvia, Lithuania, Poland, Portugal, Romania, Slovakia, Spain'],
    ], [3540, 6100]),
    ('notes', "Source: authors’ calculations (k-means, k = 2, on standardized indicators)."),
]
