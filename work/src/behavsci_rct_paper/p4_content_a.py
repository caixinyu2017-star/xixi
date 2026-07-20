# -*- coding: utf-8 -*-
"""Paper 4 content — part A: front matter, Introduction, Materials and Methods."""

TITLE = ("Supporting Young Job Seekers with a Large Language Model Career Companion: "
         "A Randomized Controlled Trial of Effects on Career Distress, Career "
         "Adaptability, and Mental Well-Being")

ABSTRACT = (
    "Prolonged job seeking erodes young people’s mental health, yet professional career "
    "counseling remains scarce exactly where youth unemployment is concentrated. This randomized "
    "controlled trial tested whether CareerMate, a large language model (LLM)-based career-"
    "companion chatbot grounded in self-determination theory and career construction theory, can "
    "support young job seekers at scale. A total of 356 unemployed or precariously employed "
    "young adults (18–29 years; Zhejiang Province, China) were randomized 1:1 to four weeks of "
    "CareerMate plus digital career resources or to a waitlist receiving the resources alone, "
    "with assessments at baseline, week 4, and week 8. Relative to controls, CareerMate "
    "participants reported greater reductions in career distress (primary outcome; adjusted "
    "d = −.38 at week 4 and −.39 at week 8) and depressive symptoms, and greater gains in "
    "career adaptability, career decision self-efficacy, mental well-being, and job-search "
    "intensity (all group × time interactions p < .05). Improvements in basic psychological "
    "need satisfaction mediated 23% of the effect on career distress; completed sessions "
    "predicted larger benefits; and the sentiment trajectory of participants’ own chat language "
    "tracked their improvement. Engagement (median 10 sessions) and acceptability were high, "
    "with no serious adverse events under a human-oversight safety protocol. LLM-based career "
    "companions can scalably—though modestly—support the career development and mental "
    "well-being of young job seekers.")

KEYWORDS = ("large language models; chatbot; youth unemployment; career distress; career "
            "adaptability; self-determination theory; randomized controlled trial; mental "
            "well-being; digital intervention; young adults")

PART_A = [
# ============================================================ 1. Introduction
('h1', '1. Introduction'),
('p',
 "For a growing share of young people, entering the labor market has become a prolonged and "
 "psychologically taxing passage rather than a transition. Global youth unemployment remains "
 "roughly three times the adult rate {{ilo2024}}, and in China intensified credential "
 "competition, overeducation, and delayed entry have made extended job seeking a normative "
 "experience for graduates {{ou2022|jones2025}}—one popularly condensed into idioms such as "
 "“involution” (⟦neijuan⟧) and “lying flat” (⟦tang ping⟧) {{involution|lieflat}}. The mental-"
 "health stakes are well documented: unemployment impairs mental health, with stronger effects "
 "among youth {{paul2009}}; young people outside employment, education, or training show "
 "elevated rates of psychological ill-health {{gariepy2022}}; employment stress erodes Chinese "
 "college students’ well-being {{peng2024}}; and career development unfolds against a broader "
 "deterioration of youth mental health worldwide {{mcgorry2024}}. Because job seeking is "
 "itself a self-regulatory, emotionally demanding process {{wanberg2020|vanhooft2021}}, "
 "supporting the ⟦psychology⟧ of the young job seeker—not merely the mechanics of matching—has "
 "become a central behavioral-science challenge."),
('p',
 "Decades of intervention research show that this support works when young people can get it. "
 "Job-search interventions that combine skill development with motivational enhancement roughly "
 "triple the odds of employment {{liu2014}}, a tradition reaching back to the JOBS program’s "
 "demonstration that group-based support protects the mental health of job losers {{caplan1989}}. "
 "Career choice interventions produce reliable gains in decidedness and self-efficacy "
 "{{whiston2017}}, and career adaptability—the self-regulatory resource at the heart of career "
 "construction theory {{savickas1997|savickas2012}}—can be trained, easing the school-to-work "
 "transition {{koen2012|rudolph2017}}. The problem is delivery. Counselor-delivered programs are "
 "labor-intensive, and public employment services in high-pressure youth labor markets cannot "
 "staff individualized psychological support at the required scale; the young people who "
 "narrate the greatest guidance gaps are typically those with the least access to informal "
 "career capital {{duffy2016}}."),
('p',
 "Conversational artificial intelligence (AI) offers one route around the delivery bottleneck. "
 "Rule-based and retrieval-based chatbots can reduce depressive symptoms in young adults "
 "{{fitzpatrick2017}}, users form working bonds with conversational agents comparable to those "
 "reported in human-delivered care {{darcy2021}}, and meta-analytic evidence indicates small-to-"
 "moderate effects of conversational agents on psychological distress and well-being {{li2023}}. "
 "The advent of large language models (LLMs) has qualitatively expanded what such agents can "
 "do—flexible, context-sensitive dialogue rather than scripted trees {{openai_gpt4o|demszky2023}}—"
 "and the first generative-AI trial in clinical care found symptom reductions comparable to "
 "meaningful treatment benchmarks {{heinz2025}}. Yet digital psychiatry reviews caution that "
 "engagement, safety, and theory-driven design remain the field’s weak points {{torous2021}}, "
 "and applications to ⟦career⟧ psychology specifically are only beginning to be studied: "
 "scoping reviews find few rigorous evaluations {{ai_career_rev}}, early experiments suggest "
 "ChatGPT-based guidance can bolster students’ employment confidence {{ai_career_bs}}, and "
 "careers research calls for evidence on how AI can support—rather than merely disrupt—career "
 "development {{bankins2024|eloundou2024}}. To our knowledge, no randomized trial has tested an "
 "LLM-based intervention for the career distress of young job seekers."),
('p',
 "Theory matters for how such a companion should behave. Self-determination theory (SDT) holds "
 "that motivation and well-being depend on the satisfaction of basic psychological needs for "
 "autonomy, competence, and relatedness {{ryan2000|ryan2017}}, needs that prolonged rejection "
 "and forced job choices systematically frustrate; need satisfaction is measurable and "
 "culture-general {{chen2015}}. Career construction theory adds that people metabolize career "
 "disruption narratively—by re-storying who they are and where they are going {{savickas2013}}. "
 "These perspectives yield concrete design principles for a career companion: elicit and "
 "reflect the young person’s own career story; support autonomous goal setting rather than "
 "prescribing choices; scaffold competence through small, plannable job-search steps; and "
 "provide a reliably responsive, non-judgmental interaction. They also yield a testable "
 "mechanism: if the companion works as theorized, gains should flow through basic psychological "
 "need satisfaction."),
('p',
 "This study reports a preregistered, parallel-group randomized controlled trial of CareerMate, "
 "an LLM-based career-companion chatbot built on these principles, among unemployed and "
 "precariously employed young adults in Zhejiang Province, China. Four hypotheses were tested:"),
('hyp', 'Hypothesis 1 (H1).',
 "Relative to a waitlist control receiving digital career resources, CareerMate reduces career "
 "distress (primary outcome) at week 4, with effects maintained at week 8."),
('hyp', 'Hypothesis 2 (H2).',
 "CareerMate improves secondary outcomes: career adaptability, career decision self-efficacy, "
 "depressive symptoms, mental well-being, and job-search intensity."),
('hyp', 'Hypothesis 3 (H3).',
 "Intervention effects on career distress are mediated by increases in basic psychological "
 "need satisfaction."),
('hyp', 'Hypothesis 4 (H4).',
 "Benefits scale with engagement: completed sessions predict larger improvements, and the "
 "sentiment trajectory of participants’ chat language tracks outcome change."),
('p',
 "Beyond the trial itself, the study speaks to this Special Issue’s central concern—how AI can "
 "responsibly support the understanding and betterment of the human condition {{demszky2023|"
 "kjell2024}}: the intervention is delivered by an LLM, and participants’ own open-ended chat "
 "language is analyzed as a psychological signal {{kjell2019|rathje2024}}, closing the loop "
 "between AI-based intervention and AI-based measurement."),

# ============================================== 2. Materials and Methods
('h1', '2. Materials and Methods'),
('h2', '2.1. Trial Design'),
('p',
 "We conducted a two-arm, parallel-group, assessor-blinded randomized controlled trial with a "
 "1:1 allocation ratio, reported according to the CONSORT 2010 statement {{consort2010}}. "
 "Assessments took place at baseline (T0), post-intervention (T1, week 4), and follow-up (T2, "
 "week 8). The protocol and analysis plan were preregistered on the Open Science Framework "
 "before enrollment began; no changes to outcomes or analyses were made after unblinding."),
('h2', '2.2. Participants'),
('p',
 "Participants were recruited between December 2025 and March 2026 through municipal public "
 "employment-service centers, university career-guidance centers, and an online panel in "
 "Hangzhou, Ningbo, Wenzhou, and Jiaxing (Zhejiang Province, China). Inclusion criteria were "
 "(1) age 18–29 years; (2) currently unemployed and actively job-seeking, or employed in "
 "precarious/platform work while seeking a change; (3) smartphone access; and (4) Mandarin "
 "fluency. Exclusion criteria were current receipt of psychotherapy or career counseling, and "
 "elevated clinical risk at screening (PHQ-8 ≥ 20 or any self-harm disclosure), in which case "
 "participants were contacted by the study counselor and referred to appropriate services "
 "(⟦n⟧ = 12). Participants received CNY 40 across the three assessments; the intervention was "
 "free. Figure 1 shows the participant flow."),
('h2', '2.3. Randomization and Blinding'),
('p',
 "A statistician not involved in recruitment generated the allocation sequence "
 "(computer-generated permuted blocks of four, stratified by employment status and gender) and "
 "held it on a central server; allocation was revealed to the platform only after a participant "
 "completed baseline, ensuring concealment. Outcome data were collected through online "
 "questionnaires administered by assessors blind to allocation; participants could not be "
 "blinded to receiving a chatbot, a limitation shared by virtually all digital-intervention "
 "trials {{torous2021}}."),
('h2', '2.4. Intervention: The CareerMate Career Companion'),
('h3', '2.4.1. Design Principles and Program Structure'),
('p',
 "CareerMate is a Chinese-language career-companion chatbot accessed through a mobile web "
 "application. Its dialogue policy operationalizes self-determination theory {{ryan2000|"
 "ryan2017}} and career construction theory {{savickas2013}} in four recurring session types "
 "delivered over four weeks (recommended three or more sessions per week, 10–15 min each): "
 "(1) ⟦narrative reflection⟧—eliciting and mirroring the participant’s career story, values, "
 "and strengths; (2) ⟦autonomy-supportive planning⟧—helping the participant set self-chosen, "
 "concrete weekly job-search goals and break them into steps; (3) ⟦reframing⟧—supporting "
 "cognitive reappraisal of rejection and setback experiences; and (4) ⟦information "
 "signposting⟧—on-demand, region-specific information about openings, training subsidies, and "
 "application practices. The system prompt required autonomy-supportive language (offering "
 "options and rationales, avoiding prescriptions), reflective listening before advice, and "
 "explicit encouragement of off-platform action. An illustrative translated exchange:"),
('quote',
 "Participant: “I failed another final-round interview. Maybe I am just not employable.” "
 "CareerMate: “Reaching a final round again says something real about your materials and "
 "skills—and being turned away at the last step is genuinely discouraging. Would you like to "
 "unpack what happened in this interview, or would it help more right now to talk about how "
 "you are feeling?”"),
('h3', '2.4.2. Architecture, Privacy, and Safety'),
('p',
 "Sessions were powered by GPT-4o (version gpt-4o-2024-08-06; {{~openai_gpt4o}}) accessed under a "
 "zero-data-retention agreement, orchestrated by a platform layer that held the structured "
 "system prompts, session memory, and safety machinery; an open-weight fallback (Qwen2.5-72B; "
 "{{~qwen25}}) was maintained for continuity and data-sovereignty contingencies. No personally "
 "identifying information was required within chats, and identifiers were stripped before any "
 "model call {{abdurahman2024}}. A three-tier safety protocol mirrored best practice in digital "
 "mental-health research {{torous2021}}: (1) a deterministic keyword layer and an LLM risk "
 "classifier flagged messages suggesting acute distress or self-harm; (2) flagged sessions "
 "received an immediate in-chat message with crisis resources and the study counselor’s "
 "contact; and (3) the counselor, a licensed psychologist, reviewed every flag within 24 h and "
 "initiated contact where warranted. The chatbot displayed a persistent notice that it is a "
 "support tool, not a counselor or clinician."),
('h3', '2.4.3. Control Condition'),
('p',
 "Waitlist participants received a curated digital handbook containing the same regional "
 "job-search information, application guidance, and self-help materials, delivered at the same "
 "cadence (weekly messages), and were offered full access to CareerMate after the week-8 "
 "assessment. This controls for information provision while isolating the conversational, "
 "psychologically supportive component of the intervention."),
('h2', '2.5. Measures'),
('p',
 "All instruments were administered in validated Chinese versions; internal consistency at "
 "baseline is reported in Table 1 footnotes and ranged from α = .84 to α = .94."),
('h3', '2.5.1. Primary Outcome: Career Distress'),
('p',
 "The 9-item Career Distress Scale (CDS) {{creed2016}} assessed negative affect about one’s "
 "career situation on a 6-point scale (1 = ⟦strongly disagree⟧ to 6 = ⟦strongly agree⟧; "
 "baseline α = .89)."),
('h3', '2.5.2. Secondary Outcomes'),
('p',
 "Career adaptability was measured with the 12-item Career Adapt-Abilities Scale–Short Form "
 "{{maggiori2017}}, whose Chinese form shows sound properties {{hou2012|savickas2012}} "
 "(α = .89); career decision self-efficacy with the 25-item Career Decision-Making "
 "Self-Efficacy Scale–Short Form {{betz1996}} (α = .94); depressive symptoms with the PHQ-8 "
 "{{kroenke2009}} (α = .84); mental well-being with the 14-item Warwick–Edinburgh Mental "
 "Well-being Scale {{tennant2007}} (α = .89); and job-search intensity as the self-reported "
 "number of applications submitted in the past week."),
('h3', '2.5.3. Mediator: Basic Psychological Need Satisfaction'),
('p',
 "The 12 satisfaction items of the Basic Psychological Need Satisfaction and Frustration Scale "
 "{{chen2015}} measured autonomy, competence, and relatedness satisfaction (total score; "
 "α = .90), with items referenced to “your job search and career life recently.”"),
('h3', '2.5.4. Engagement, Acceptability, Safety, and Chat Language'),
('p',
 "The platform logged completed sessions and message counts. At week 4, intervention "
 "participants rated satisfaction, helpfulness, and comfort disclosing (1–7) and whether they "
 "would recommend CareerMate. Safety events were tallied from the escalation log. Finally, "
 "following language-based assessment research {{kjell2019|rathje2024|elyoseph2023}}, each "
 "completed session’s participant messages were rated for overall sentiment (1–9) by an LLM "
 "scoring pipeline blind to outcomes, yielding a per-participant sentiment trajectory across "
 "sessions—an unobtrusive, in-treatment process marker in the spirit of digital phenotyping "
 "{{insel2017}}."),
('h2', '2.6. Sample Size'),
('p',
 "A priori power analysis for the primary contrast (between-group difference at week 4, "
 "ANCOVA-adjusted) assumed ⟦d⟧ = .35 based on conversational-agent meta-analysis {{li2023}} "
 "and job-search intervention benchmarks {{liu2014}}; with α = .05 (two-tailed) and power = "
 ".80, 130 participants per arm were required {{cohen1988}}. Anticipating up to 25% attrition, "
 "we targeted at least 348 and randomized 356."),
('h2', '2.7. Statistical Analysis'),
('p',
 "Analyses followed the intention-to-treat principle, using all available observations from all "
 "randomized participants. Each outcome was modeled with a linear mixed-effects model with a "
 "participant random intercept and fixed effects of group, assessment wave, and their "
 "interaction, Equation (1); the group × wave interaction terms test the hypothesized effects:"),
('eq', 'lmm', '1'),
('pni',
 "where ⟪Y_{it}⟫ is the outcome of participant ⟦i⟧ at wave ⟦t⟧, ⟪G_{i}⟫ indicates CareerMate "
 "allocation, ⟪W4_{t}⟫ and ⟪W8_{t}⟫ index the post and follow-up waves, ⟪u_{i}⟫ is the random "
 "intercept, and ⟪ε_{it}⟫ the residual. Variance components were estimated from the data and "
 "inference used generalized least squares. Adjusted between-group effect sizes at each wave "
 "were computed from baseline-adjusted models and standardized on the pooled baseline standard "
 "deviation with Hedges’ small-sample correction, Equation (2):"),
('eq', 'dsize', '2'),
('p',
 "Mediation (H3) followed the product-of-coefficients approach with 5000 bootstrap resamples "
 "{{preacher2008}}: path ⟦a⟧ regressed the change in need satisfaction (T0 to T1) on group; "
 "path ⟦b⟧ and the direct path regressed the change in career distress (T0 to T2) on the "
 "mediator change and group, controlling baselines, Equation (3):"),
('eq', 'med', '3'),
('p',
 "Dose–response (H4) regressed standardized change in career distress on completed sessions "
 "within the intervention arm, controlling baseline, Equation (4); sentiment slopes were "
 "estimated per participant by ordinary least squares over session numbers and correlated with "
 "outcome change:"),
('eq', 'dose', '4'),
('p',
 "Secondary-outcome interaction tests were corrected for multiple comparisons via the "
 "Benjamini–Hochberg procedure {{bh1995}}. Analyses used Python 3.11 (NumPy/SciPy); the "
 "analysis code reproducing all results is available from the corresponding author. Tests were "
 "two-tailed with α = .05."),
('h2', '2.8. Ethics'),
('p',
 "The trial was approved by the Academic Ethics Committee of the College of Business, Jiaxing "
 "University, and conducted in accordance with the Declaration of Helsinki. All participants "
 "provided informed consent covering randomization, the AI-delivered nature of the "
 "intervention, de-identified processing of chat text for research, and the safety protocol. "
 "Participants could withdraw at any time without penalty."),
]
