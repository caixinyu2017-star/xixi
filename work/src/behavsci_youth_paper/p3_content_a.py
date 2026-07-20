# -*- coding: utf-8 -*-
"""Paper 3 content — part A: front matter, Introduction, Materials and Methods.
Citations: {{key}} parenthetical, {{@key}} narrative; ⟦..⟧ italics; ⟪..⟫ inline math."""

TITLE = ("From Narratives to Numbers: Using Large Language Models to Assess "
         "Career Distress in Chinese Young Adults’ Open-Ended Employment Narratives")

ABSTRACT = (
    "Young people increasingly describe their employment and career difficulties in words that "
    "closed-ended rating scales cannot fully capture. This study examined whether large language "
    "models (LLMs) can transform open-ended career narratives into reliable, valid, and "
    "incrementally informative psychological measurements. In a cross-sectional survey, 947 "
    "Chinese young adults (18–29 years; Zhejiang Province) wrote three short narratives about "
    "their employment situation, feelings, and support needs, and completed validated measures of "
    "career distress, career adaptability, anxiety, depressive symptoms, perceived employability, "
    "and life satisfaction. Two LLMs (GPT-4o and Qwen2.5-72B; three runs each at temperature 0) "
    "rated each de-identified narrative for career distress, employment anxiety, and career "
    "confidence. Ratings were highly stable across runs (ICC ≥ .97), consistent across models "
    "(r = .77–.80), and the pooled LLM distress score agreed with human expert coding (r = "
    ".80). Convergent–discriminant patterns matched theoretical expectations (LLM distress–Career "
    "Distress Scale r = .52). Semantic clustering of narrative embeddings identified six "
    "interpretable difficulty themes; narratives centered on meaning and motivational struggles "
    "showed the poorest psychological adjustment. LLM narrative distress predicted depressive "
    "symptoms and life satisfaction beyond all questionnaires (ΔR² = .024 and .013) and "
    "improved identification of elevated depressive symptoms (AUC .754 to .777). Language-based "
    "AI assessment can complement—not replace—traditional instruments in youth career services.")

KEYWORDS = ("large language models; natural language processing; psychological assessment; "
            "career distress; youth employment; career development; semantic analysis; "
            "open-ended responses; computational psychology; young adults")

PART_A = [
# ============================================================ 1. Introduction
('h1', '1. Introduction'),
('p',
 "Youth labor markets have recovered unevenly from successive global shocks, and difficulties in "
 "finding, keeping, and making sense of work have become a defining developmental stressor for "
 "young adults {{ilo2024}}. Beyond its economic costs, problematic school-to-work passage carries "
 "a substantial psychological burden: unemployment impairs mental health with effects that are "
 "stronger for youth and for people in countries with weaker protection systems {{paul2009}}, "
 "young people not in employment, education, or training (NEET) show elevated rates of mental "
 "ill-health {{gariepy2022|rahmani2024}}, and youth mental health more broadly has deteriorated "
 "at precisely the ages when careers are launched {{mcgorry2024}}. Understanding how young "
 "people experience employment difficulty—and detecting who is struggling most—has therefore "
 "become a behavioral-science problem as much as an economic one {{wanberg2020|vanhooft2021}}."),
('p',
 "These pressures are particularly visible in China. Higher-education expansion has intensified "
 "positional competition among graduates {{ou2022}}, overeducation and major–job mismatch depress "
 "early-career earnings and satisfaction {{jones2025}}, employment stress measurably erodes "
 "college students’ psychological well-being {{peng2024}}, and digitalization is reshaping the "
 "quality and stability of the jobs available to young workers {{xiong2024}}. Popular idioms such "
 "as “involution” (⟦neijuan⟧), “lying flat” (⟦tang ping⟧), and “slow employment” (⟦man jiuye⟧) "
 "have entered public and academic discourse as shorthand for competitive escalation, motivational "
 "withdrawal, and postponed labor-market entry among Chinese youth {{involution|lieflat}}. At the "
 "same time, generative artificial intelligence (AI) is transforming the entry-level task "
 "structure that has traditionally absorbed young labor-market entrants {{eloundou2024|noy2023|"
 "brynjolfsson2025}}, adding a novel layer of career uncertainty that unfolds across career stages "
 "{{bankins2024}}. Zhejiang Province—one of China’s most digitalized provincial economies and the "
 "national “common prosperity” demonstration zone—concentrates these dynamics, making its young "
 "adults an informative population for studying contemporary career difficulty."),
('p',
 "Psychologically, the experience of career difficulty is captured by constructs such as career "
 "distress—negative affect directed at one’s vocational situation and prospects {{creed2016}}—and "
 "by the resources people mobilize against it, notably career adaptability {{savickas2012|"
 "rudolph2017}} and perceived employability {{rothwell2007}}. Career construction theory holds "
 "that people build careers by narrating them: vocational identity takes shape in the stories "
 "people tell about who they are and where they are going {{savickas2013}}. The psychology of "
 "working theory adds that structural constraints—economic resources, marginalization, geographic "
 "and family obligations—shape whether work can fulfill basic needs {{duffy2016}}. Both "
 "perspectives imply that the ⟦words⟧ young people use about their careers carry diagnostic "
 "information that numeric scale scores summarize only partially."),
('p',
 "Behavioral research has nonetheless relied overwhelmingly on closed-ended rating scales, which "
 "constrain respondents to researcher-defined dimensions and lose the nuance, context, and "
 "idiosyncrasy of individual experience {{kjell2019}}. Language-based measurement offers a "
 "complementary route: word use reliably indexes psychological states {{tausczik2010}}, "
 "social-media language predicts clinically relevant outcomes such as depression {{eichstaedt2018|"
 "insel2017}}, and statistical-semantic methods can quantify open-ended answers with an accuracy "
 "approaching the reliability ceiling of the questionnaires they are validated against "
 "{{kjell2022|sikstrom2020}}. Historically, however, such pipelines demanded corpus-specific "
 "dictionaries or task-specific training data, limiting their reach into applied field settings "
 "{{boyd2021}}."),
('p',
 "Large language models (LLMs) change this calculus. Zero-shot LLM scoring produces psychological "
 "text ratings that correlate with expert judgment across constructs and languages {{rathje2024}}, "
 "annotates text more consistently than crowd workers {{gilardi2023}}, matches or exceeds human "
 "performance on emotion-inference tasks {{elyoseph2023}}, infers psychological dispositions from "
 "everyday digital text {{peters2024}}, and predicts mental-health status from natural language "
 "{{xu2024}}. Reviews conclude that LLMs are poised to become standard instruments of "
 "psychological assessment—provided they are evaluated with the same psychometric rigor as any "
 "other measurement device, including reliability, convergent and discriminant validity, and "
 "demonstrable added value over existing instruments {{demszky2023|kjell2024|ziems2024}}, and "
 "provided their risks around privacy, bias, and construct drift are managed {{abdurahman2024}}. "
 "Three gaps remain. First, applications to ⟦career⟧ psychology are scarce: the constructs that "
 "LLM scoring has targeted are mostly clinical or affective, not vocational. Second, most "
 "validation evidence comes from English-language, Western samples; evidence for Chinese-language "
 "narratives from non-WEIRD youth populations is thin. Third, few studies test ⟦incremental⟧ "
 "validity—whether narrative-derived scores add predictive information beyond a full battery of "
 "validated questionnaires rather than merely correlating with one of them."),
('p',
 "The present study addresses these gaps with a preregistered-style, multi-criteria psychometric "
 "evaluation of LLM narrative scoring in a large sample of Chinese young adults facing a "
 "difficult labor market. Participants wrote three short open-ended narratives about their "
 "employment situation and completed six validated scales. Two LLMs—one proprietary (GPT-4o) and "
 "one open-weight (Qwen2.5-72B)—independently rated every de-identified narrative for career "
 "distress, employment anxiety, and career confidence; a human expert panel coded a stratified "
 "subsample; and multilingual sentence embeddings were clustered to map the thematic structure of "
 "narrated difficulty. Four hypotheses were tested:"),
('hyp', 'Hypothesis 1 (H1).',
 "LLM narrative ratings are reliable: stable across repeated runs, consistent across "
 "architecturally independent models, and convergent with human expert coding."),
('hyp', 'Hypothesis 2 (H2).',
 "LLM narrative ratings show a convergent–discriminant pattern: each rated dimension correlates "
 "most strongly with its matching self-report construct and more weakly with non-matching "
 "constructs."),
('hyp', 'Hypothesis 3 (H3).',
 "LLM narrative distress shows incremental validity: it predicts depressive symptoms and life "
 "satisfaction over and above demographics, employment status, and all closed-ended scales, and "
 "improves classification of elevated depressive symptoms."),
('hyp', 'Hypothesis 4 (H4).',
 "Narrated career difficulties form interpretable semantic themes whose members differ "
 "systematically in psychological adjustment and in social-structural composition."),
('p',
 "By treating LLM output as a measurement instrument to be audited—rather than an oracle to be "
 "trusted—the study contributes a template for evaluating AI-based assessment in the behavioral "
 "sciences and provides substantive evidence on what troubles young people in a rapidly "
 "digitalizing labor market, with practical implications for scalable, language-based triage in "
 "youth career services {{demszky2023|kjell2024}}."),

# ============================================== 2. Materials and Methods
('h1', '2. Materials and Methods'),
('h2', '2.1. Participants and Procedure'),
('p',
 "Participants were young adults aged 18–29 years residing in Zhejiang Province, China, recruited "
 "between November 2025 and January 2026 through a professional online survey panel supplemented "
 "by advertisements distributed via university career-guidance centers and municipal youth-service "
 "centers in Hangzhou, Ningbo, Wenzhou, and Jiaxing. Quota targets on gender, education, and "
 "current employment status were used to obtain a heterogeneous—though not probability-based—"
 "sample spanning employed, precariously employed, unemployed, exam-preparing, and other "
 "non-employed youth. Of 1216 individuals who opened the survey, 1102 completed it; 74 were "
 "excluded for failing at least one of two embedded attention checks, 49 for unusable narratives "
 "(fewer than 20 Chinese characters in total or non-substantive strings), and 32 for total "
 "completion times under five minutes, leaving a final sample of ⟦N⟧ = 947 (52.0% female; ⟦M⟧ "
 "age = 23.9 years, ⟦SD⟧ = 2.8). Table 1 reports sample characteristics. Participants received "
 "CNY 15 for completion."),
('p',
 "The study was approved by the Academic Ethics Committee of the College of Business, Jiaxing "
 "University, and conducted in accordance with the Declaration of Helsinki. All participants "
 "provided informed consent on the opening page, which explained that anonymized excerpts of "
 "their written answers might be quoted in translated form, that de-identified text would be "
 "processed by AI systems for research purposes, and that participation could be withdrawn at "
 "any time without penalty. No personally identifying information was requested in the narrative "
 "prompts, and automated plus manual screening removed incidental identifiers (names, employers, "
 "phone numbers) before any text left the research environment, following current guidance for "
 "responsible LLM use in psychological research {{abdurahman2024}}."),
('h2', '2.2. Open-Ended Career Narratives'),
('p',
 "Following the logic of narrative career assessment {{savickas2013}} and open-ended "
 "semantic-measurement designs {{kjell2019}}, participants answered three writing prompts before "
 "any rating scale was displayed: (1) “Please describe your current employment or career "
 "situation and the biggest difficulties you are facing”; (2) “How do you feel when you think "
 "about job seeking and your career future?”; and (3) “Where would you like your career to be in "
 "three years, and what support would help you get there?” (full wording in Appendix A). "
 "Responses were written in Chinese with a 10-character minimum per prompt. Combined narrative "
 "length ranged from 34 to 1307 characters (⟦Mdn⟧ = 155, interquartile range 107–217). Narrative "
 "length was retained as a covariate in all incremental-validity models to guard against "
 "verbosity artifacts."),
('h2', '2.3. Closed-Ended Measures'),
('p',
 "Unless noted otherwise, established Chinese versions of all instruments were administered, and "
 "internal consistency was estimated with both Cronbach’s alpha and McDonald’s omega "
 "{{hayes2020}}. Descriptive statistics and reliabilities appear in Table 2."),
('h3', '2.3.1. Career Distress'),
('p',
 "The 9-item Career Distress Scale (CDS) {{creed2016}} measured negative affect about one’s "
 "career situation and prospects (e.g., feeling stressed, discouraged, or stuck when thinking "
 "about one’s career) on a 6-point scale (1 = ⟦strongly disagree⟧ to 6 = ⟦strongly agree⟧; "
 "α = .89, ω = .89)."),
('h3', '2.3.2. Career Adaptability'),
('p',
 "The 12-item Career Adapt-Abilities Scale–Short Form (CAAS-SF) {{maggiori2017}}, derived from "
 "the international CAAS {{savickas2012}} whose Chinese form shows sound psychometric properties "
 "{{hou2012}}, measured concern, control, curiosity, and confidence resources on a 5-point scale "
 "(1 = ⟦not strong⟧ to 5 = ⟦strongest⟧). The total score was used (α = .88, ω = .88)."),
('h3', '2.3.3. Anxiety Symptoms'),
('p',
 "The 7-item Generalized Anxiety Disorder scale (GAD-7) {{spitzer2006}} measured anxiety symptoms "
 "over the past two weeks on a 4-point scale (0 = ⟦not at all⟧ to 3 = ⟦nearly every day⟧; "
 "α = .85, ω = .85)."),
('h3', '2.3.4. Depressive Symptoms'),
('p',
 "The 8-item Patient Health Questionnaire (PHQ-8) {{kroenke2009}} measured depressive symptoms "
 "over the past two weeks on the same 4-point response format (α = .84, ω = .84). Following "
 "convention, total scores of 10 or above were classified as elevated depressive symptoms for the "
 "classification analyses; this cutoff is a screening indicator, not a diagnosis."),
('h3', '2.3.5. Perceived Employability'),
('p',
 "Ten items adapted from the self-perceived employability scale {{rothwell2007}} measured "
 "perceived internal and external employability (e.g., confidence in one’s skills relative to "
 "labor-market demand) on a 5-point agreement scale (α = .86, ω = .86)."),
('h3', '2.3.6. Life Satisfaction'),
('p',
 "The 5-item Satisfaction With Life Scale (SWLS) {{diener1985}} measured global life satisfaction "
 "on a 7-point agreement scale (α = .86, ω = .86)."),
('h2', '2.4. LLM Narrative Scoring'),
('p',
 "Each participant’s three de-identified narratives were concatenated and scored independently by "
 "two architecturally unrelated LLMs: GPT-4o (version gpt-4o-2024-08-06) {{openai_gpt4o}} accessed "
 "through its application programming interface with a zero-data-retention agreement, and "
 "Qwen2.5-72B-Instruct {{qwen25}}, an open-weight model deployed on local infrastructure so that "
 "no text left institutional servers. Both models received the same Chinese-language instruction "
 "(translated in Appendix A) asking them to act as a career-psychology rater and return integer "
 "ratings from 1 to 10 for three dimensions: ⟦career distress⟧ (criterion construct: CDS), "
 "⟦employment anxiety⟧ (criterion: GAD-7), and ⟦career confidence⟧ (criteria: CAAS-SF and "
 "perceived employability), in machine-readable JSON with no free-text commentary. Temperature "
 "was fixed at 0; each model scored every narrative three times using three semantically "
 "equivalent instruction variants to quantify run-to-run stability. The analysis composite for "
 "each dimension averaged the six model-by-run ratings, as in Equation (1):"),
('eq', 'composite', '1'),
('pni',
 "where ⟪S_{imr}⟫ is the rating of participant ⟦i⟧ by model ⟦m⟧ (⟦M⟧ = 2) on run ⟦r⟧ (⟦R⟧ = 3). "
 "Zero-shot scoring was chosen deliberately: it requires no training data, is reproducible from "
 "the published prompt, and reflects how career services could realistically deploy such tools "
 "{{rathje2024|kjell2024}}."),
('h2', '2.5. Human Expert Coding'),
('p',
 "Two master’s-level raters in applied psychology, blind to all scale scores and LLM outputs, "
 "independently rated a random subsample of 200 narrative sets (stratified by employment status) "
 "for career distress on the same 1–10 rubric after 12 h of joint training on 30 pilot cases "
 "excluded from the study data. The two raters agreed at ICC(2,2) = .71. The same raters "
 "independently assigned each of the 200 cases to one of the six semantic themes described below "
 "to validate the automated thematic solution."),
('h2', '2.6. Semantic Embeddings and Thematic Clustering'),
('p',
 "To map ⟦what⟧ young people narrate—not only how distressed they sound—each concatenated "
 "narrative was embedded with the multilingual BGE-M3 sentence-embedding model {{bgem3}}, which "
 "extends the sentence-transformer paradigm {{reimers2019}} to Chinese text. Embeddings were "
 "reduced to two dimensions with UMAP (15 neighbors, minimum distance 0.1) {{mcinnes2018}} and "
 "partitioned with k-means for candidate solutions ⟦k⟧ = 2–8, following the topic-modeling logic "
 "of embedding-based clustering {{grootendorst2022}}. Solution quality was indexed by the mean "
 "silhouette coefficient {{rousseeuw1987}}, Equation (2) below; the ⟦k⟧ = 6 solution maximized "
 "silhouette (.462) and was most interpretable. Two researchers then read the 20 narratives "
 "closest to each cluster centroid, labeled the themes, and reviewed all boundary cases; 9.1% of "
 "assignments were manually reassigned, yielding the final thematic solution (mean silhouette "
 ".412):"),
('eq', 'sil', '2'),
('pni',
 "where ⟦a⟧(⟦i⟧) is the mean embedding distance of narrative ⟦i⟧ to members of its own theme and "
 "⟦b⟧(⟦i⟧) the smallest mean distance to another theme."),
('h2', '2.7. Statistical Analysis'),
('p',
 "Reliability was quantified with two-way random-effects intraclass correlation coefficients for "
 "absolute agreement {{shrout1979|koo2016}}, Equation (3), where ⟪MS_{R}⟫, ⟪MS_{C}⟫, and ⟪MS_{E}⟫ "
 "are the row (target), column (rater), and error mean squares for ⟦n⟧ targets and ⟦k⟧ raters:"),
('eq', 'icc', '3'),
('p',
 "Convergent and discriminant validity were evaluated with Pearson correlations under "
 "Benjamini–Hochberg false-discovery-rate control across the 45 unique coefficients {{bh1995}}; "
 "theme validation used Cohen’s kappa {{cohen1960}}; theme and status differences used one-way "
 "analyses of variance with η² effect sizes and chi-square tests of independence. Incremental "
 "validity used hierarchical ordinary-least-squares regressions, Equation (4), entering "
 "demographic covariates ⟪D_{i}⟫ (gender, age, education, employment status, log narrative "
 "length) in Step 1, all closed-ended predictors ⟪Q_{i}⟫ (CDS, CAAS-SF, perceived employability, "
 "GAD-7) in Step 2, and the LLM narrative distress composite in Step 3:"),
('eq', 'hier', '4'),
('p',
 "Classification of elevated depressive symptoms (PHQ-8 ≥ 10) compared logistic models with and "
 "without LLM narrative scores using areas under the receiver-operating-characteristic curve and "
 "DeLong’s test for correlated curves {{delong1988}}, with five-fold cross-validation as a "
 "robustness check. Analyses used Python 3.11 (NumPy/SciPy); the full analysis pipeline and "
 "de-identified quantitative data are available from the corresponding author. Tests were "
 "two-tailed with α = .05. The study design and analysis pipeline are summarized in Figure 1."),
('figure', 'p3_fig1.png'),
('figcap', 1,
 "Study design and analysis pipeline. CDS = Career Distress Scale; CAAS-SF = Career "
 "Adapt-Abilities Scale–Short Form; GAD-7 = Generalized Anxiety Disorder scale; PHQ-8 = Patient "
 "Health Questionnaire; SWLS = Satisfaction With Life Scale; ICC = intraclass correlation "
 "coefficient; AUC = area under the receiver-operating-characteristic curve."),
]
