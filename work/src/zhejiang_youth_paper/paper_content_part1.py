# -*- coding: utf-8 -*-
"""Manuscript content, part 1: front matter, Introduction, Theory & Hypotheses.

Blocks: ('title',t) ('authors',t) ('editorbox',) ('affil',...) ('abstract',t)
('keywords',t) ('h1',t) ('h2',t) ('h3',t) ('p',t) ('hyp',label,t)
('eq',builder_key,n) ('figure',zipname,cx,cy,docid) ('figcap',n,t)
('tabcap',n,t) ('table',rows,widths) ('notes',t) ('back',label,t) ('ref',...)
Citations: {{key}} or {{key1|key2}}.  Inline math: ⟪...⟫.
"""

TITLE = ("Industrial Intelligent Transformation and Youth Employment and Career "
         "Development: A Regional Socio-Economic Systems Analysis of Zhejiang, China")

AUTHORS = "Xinyu Cai 1, Dingpei Hu 1 and Tiantian Mo 1,*"

AFFILS = [
    ("1", "College of Business, Jiaxing University, Jiaxing 314001, China; caixinyu@zjxu.edu.cn"),
    ("*", "Correspondence: 00008227@zjxu.edu.cn"),
]

ABSTRACT = (
    "The coexistence of severe youth employment pressure and persistent shortages of skilled "
    "industrial labor has become a defining dilemma of regional socio-economic systems undergoing "
    "rapid industrial upgrading. From a socio-economic systems perspective, industrial intelligent "
    "transformation constitutes a technological subsystem shock whose youth-employment consequences "
    "are shaped by skill reconfiguration and multi-level employment governance rather than by "
    "technology alone. Using panel data on 668 A-share listed firms registered in Zhejiang "
    "province—China's pioneer region of large-scale “machine substitution” and digital-economy "
    "development—from 2011 to 2023, we examine how firm-level industrial intelligent transformation "
    "affects youth employment and youth career development. We employ two-way fixed-effects models, "
    "mediation and moderation analyses, and a battery of robustness checks, including propensity "
    "score matching and instrumental-variable estimation. We find, first, that industrial "
    "intelligent transformation significantly increases both the youth-employment share and the "
    "representation of young executives, indicating that task creation and organizational renewal "
    "outweigh displacement for young workers. Second, this effect operates through two "
    "resource-reconfiguration channels: a skill-restructuring effect through upgrading of the firm "
    "skill structure and an expansion effect through productivity-driven growth. Third, multi-level "
    "employment governance plays a decisive moderating role: firm training investment, regional "
    "public employment services, and digital-economy policy pilots significantly strengthen the "
    "positive effect of intelligent transformation on youth employment. Moreover, the effect is "
    "stronger for manufacturing, larger, non-state-owned firms and firms located in the digital core "
    "cities. These findings portray youth employment as an emergent outcome of a regional "
    "socio-economic system and inform coordinated countermeasures for youth-inclusive industrial "
    "upgrading."
)

KEYWORDS = ("industrial intelligent transformation; youth employment; career development; "
            "regional socio-economic systems; skill restructuring; multi-level governance; "
            "robot penetration; Zhejiang")

PART1 = [
    ('h1', '1. Introduction'),

    ('p', "Youth employment and career development have become one of the most pressing challenges "
     "confronting regional socio-economic systems in the digital era. The International Labour "
     "Organization estimates that the global youth unemployment rate remains substantially higher "
     "than the adult rate, and that a large share of young people are not in employment, education, "
     "or training {{ilo1|ilo2|ilo3}}. In China, the urban youth unemployment rate reached "
     "historically high levels in recent years, while manufacturing regions simultaneously report "
     "persistent shortages of skilled industrial labor {{china_youth1|china_youth2}}. This "
     "coexistence of “employment difficulty” among educated young job seekers and “recruitment "
     "difficulty” among upgrading firms constitutes the youth employment dilemma: a structural "
     "mismatch between the tasks that regional industrial systems create and the skills, "
     "expectations, and career prospects of the young labor force {{mismatch1|mismatch2}}. At the "
     "same time, the rapid diffusion of industrial robots and intelligent manufacturing is "
     "transforming the structure of labor demand, automating routine production tasks while "
     "creating new digitally intensive occupations {{acemoglu2019|robots_us}}. How industrial "
     "intelligent transformation reshapes the demand for young workers and their career prospects "
     "is therefore a question of first-order importance for regional employment governance and "
     "youth-inclusive industrial upgrading {{robots_age|digital_emp1}}."),

    ('p', "The prevailing public debate frames intelligent transformation mainly as a threat to "
     "employment, emphasizing the displacement of workers by machines {{frey}}. Yet a growing body "
     "of firm-level evidence suggests a more nuanced picture: robot adoption and intelligent "
     "manufacturing can complement labor, raise productivity, and generate new roles associated "
     "with programming, supervision, data analysis, and digitally enabled services "
     "{{robots_japan|robots_china_firm}}. For young workers in particular, the net effect is "
     "theoretically ambiguous. On the one hand, youth are overrepresented in entry-level routine "
     "occupations that are most exposed to automation {{robots_age}}. On the other hand, as digital "
     "natives with recently acquired human capital, young workers hold a comparative advantage in "
     "the new digitally intensive tasks that intelligent transformation reinstates, and "
     "technological renewal may open faster promotion tracks for young technical and managerial "
     "talent {{skill_demand|career1}}. Which of these forces dominates is ultimately an empirical "
     "question that depends on how firms reconfigure their skill structures and how multi-level "
     "governance mechanisms channel technological change toward inclusive value creation."),

    ('p', "This study addresses this question from a socio-economic systems perspective. "
     "Socio-technical and socio-economic systems theory conceptualizes the region and the firm as "
     "adaptive systems in which technological and social subsystems must be jointly optimized "
     "rather than changed in isolation {{sts1|sts2|sts3}}. From this perspective, industrial "
     "intelligent transformation constitutes a technological subsystem transformation; the "
     "employment governance architecture—firm-level training investment, regional public employment "
     "services, and digital-economy policy pilots—constitutes the social and institutional "
     "subsystem; and youth employment and career development represent system-level labor outcomes "
     "that emerge from the interaction of these subsystems {{sts4|ses_regional}}. Accordingly, the "
     "relationship between intelligent transformation and youth employment is not a simple "
     "technology–labor substitution, but a socio-economic adaptation process shaped by skill "
     "reconfiguration, productivity-driven expansion, and multi-level governance."),

    ('p', "Zhejiang province provides a representative regional laboratory for this inquiry. As one "
     "of China's most developed provincial economies and the national pioneer of large-scale "
     "“machine substitution” (jiqi huanren) in manufacturing since 2013, Zhejiang has experienced "
     "both intensive industrial intelligent transformation and acute youth-employment pressure "
     "{{zhejiang1|zhejiang2}}. The province designated the digital economy as its “Number One "
     "Project” in 2017, was selected as the national common prosperity demonstration zone in 2021, "
     "and has committed to building a “youth-development-oriented province”, making the "
     "coordination between industrial upgrading and youth opportunity an explicit policy objective "
     "{{digital_emp2|pilot2}}. The coexistence of a large private manufacturing sector, rapid robot "
     "adoption, a dense cohort of young graduates attracted by the digital economy, and active "
     "employment-governance experimentation makes Zhejiang an informative setting for examining how "
     "industrial intelligent transformation, skill restructuring, and multi-level governance "
     "jointly shape youth employment and career development in a regional socio-economic system."),

    ('p', "Existing research has examined the employment effects of robots and automation, the "
     "determinants of youth employment, and regional socio-economic system analysis, respectively. "
     "However, these streams have largely developed in parallel. The task-based literature on "
     "automation and jobs rarely distinguishes age-specific effects or connects them to career "
     "advancement within firms {{acemoglu2022|robots_japan|robots_age}}. The youth-employment "
     "literature emphasizes education, institutions, and macroeconomic conditions but pays limited "
     "attention to firm-level technology adoption and its governance context {{ilo1|china_youth1}}. "
     "The regional socio-economic systems literature analyzes urban, regional, and industrial "
     "dynamics but seldom traces the youth-labor-market consequences of industrial intelligent "
     "transformation {{ses_regional|ses_urban}}. Less attention has thus been paid to how "
     "intelligent transformation, skill restructuring, productivity-driven expansion, and "
     "multi-level employment governance interact within a unified regional system to shape youth "
     "employment and career development."),

    ('p', "Based on the above analysis, we use panel data on 668 A-share listed firms registered in "
     "Zhejiang province from 2011 to 2023 to examine the impact of firm industrial intelligent "
     "transformation on youth employment and youth career development, its underlying mechanisms, "
     "and the moderating role of multi-level employment governance. The empirical results show "
     "that, first, industrial intelligent transformation significantly increases both the "
     "youth-employment share and the representation of young executives, and these findings remain "
     "robust after a series of robustness checks, including propensity score matching and "
     "instrumental-variable estimation. Second, this positive effect is primarily transmitted "
     "through two channels: a skill-restructuring effect and an expansion effect. On the one hand, "
     "intelligent transformation upgrades the firm skill structure, raising the relative demand for "
     "young, high-skill labor. On the other hand, intelligent transformation raises labor "
     "productivity and firm growth, expanding total hiring capacity in which young workers are "
     "disproportionately represented. Third, multi-level employment governance plays a crucial "
     "moderating role: firm training investment, regional public employment services, and "
     "digital-economy policy pilots significantly strengthen the positive effect of intelligent "
     "transformation on youth employment. Furthermore, the effect is significantly stronger for "
     "manufacturing, larger, and non-state-owned firms and for firms located in Zhejiang's digital "
     "core cities."),

    ('p', "Our contributions are threefold. First, we clarify the theoretical novelty of framing "
     "the youth employment dilemma as an emergent outcome of a regional socio-economic system. "
     "Prior studies mainly examine the aggregate or task-level employment effects of automation, or "
     "analyze youth unemployment from macroeconomic and institutional perspectives. We extend these "
     "studies by showing how a technological subsystem shock, firm-level resource reconfiguration, "
     "and multi-level governance jointly determine whether industrial upgrading absorbs or excludes "
     "young workers, thereby connecting the automation–employment debate with regional "
     "socio-economic system analysis {{sts1|ses_regional}}."),

    ('p', "Second, we extend the literature on the labor-market effects of industrial intelligence "
     "by identifying two resource-reconfiguration mechanisms through which intelligent "
     "transformation promotes youth employment—a skill-restructuring channel operating through the "
     "upgrading of the firm skill structure and an expansion channel operating through "
     "productivity-driven growth—and by tracing the career-development consequences of intelligent "
     "transformation through the representation of young executives. This reveals not only whether "
     "firms hire young workers under technological change, but also whether young talent advances "
     "within transforming organizations {{career1|career2}}."),

    ('p', "Third, we enrich research on employment governance by showing that firm training "
     "investment, regional public employment services, and digital-economy policy pilots strengthen "
     "the positive effect of intelligent transformation on youth employment. This highlights "
     "multi-level governance as a key condition that helps regional systems translate industrial "
     "upgrading into youth-inclusive opportunity, and provides direct evidence for the design of "
     "coordinated countermeasures to the youth employment dilemma "
     "{{alm1|vet1|pilot1}}."),

    ('p', "The rest of this study is organized as follows. Section 2 presents the institutional "
     "background, theoretical analysis, and hypotheses. Section 3 describes the research design. "
     "Section 4 reports the empirical results. Section 5 discusses the findings and limitations. "
     "Section 6 concludes the study and presents the implications."),

    ('h1', '2. Institutional Background, Theoretical Analysis, and Hypotheses'),

    ('h2', '2.1. The Youth Employment Dilemma and Industrial Intelligent Transformation in Zhejiang'),

    ('p', "Zhejiang is one of China's most market-oriented provincial economies, characterized by a "
     "dense private manufacturing sector, extensive county-level industrial clusters, and an "
     "advanced digital economy anchored by the platform ecosystems of Hangzhou {{zhejiang1}}. "
     "Facing rising labor costs and recruitment difficulties in manufacturing, the provincial "
     "government launched a province-wide “machine substitution” program in 2013, subsidizing the "
     "large-scale replacement of routine manual tasks with industrial robots and intelligent "
     "equipment; Zhejiang has since ranked among the leading provinces in robot installation in "
     "China {{robots_china_firm|zhejiang2}}. In 2017, the province designated the digital economy "
     "as its “Number One Project”, and in 2021 it was selected as the national common prosperity "
     "demonstration zone, which explicitly links industrial upgrading to inclusive employment and "
     "income growth {{digital_emp2}}."),

    ('p', "Against this backdrop, the regional youth labor market exhibits a pronounced structural "
     "dilemma. On the demand side, upgrading firms report shortages of technicians, engineers, and "
     "digitally skilled operators, and the skill requirements of newly created positions rise "
     "rapidly with intelligent transformation {{skill_demand|mismatch1}}. On the supply side, a "
     "growing cohort of young graduates—attracted by Zhejiang's digital economy and quality of "
     "life—faces employment difficulty, underemployment, and slow early-career advancement, while "
     "showing a declining willingness to enter traditional manufacturing occupations "
     "{{china_youth2|mismatch2|talent}}. The dilemma is thus not a simple deficiency of labor demand, but "
     "a system-level mismatch among task creation, skill formation, and career expectations within "
     "the regional socio-economic system. Whether industrial intelligent transformation aggravates "
     "or alleviates this mismatch—and under which governance conditions—is the central question of "
     "this study."),

    ('h2', '2.2. Industrial Intelligent Transformation and Youth Employment: A Socio-Economic Systems Perspective'),

    ('p', "Socio-technical and socio-economic systems theory provides an overarching basis for "
     "understanding the relationship between industrial intelligent transformation and youth "
     "employment. It emphasizes that organizational and regional transformation depends on the "
     "alignment and joint optimization of social and technical subsystems rather than on "
     "technological change alone {{sts1|sts2|sts3}}. In the context of this study, intelligent "
     "transformation reconfigures the technical subsystem by embedding programmable automation, "
     "adaptive production, and data-driven control into manufacturing and service processes. This "
     "technological reconfiguration in turn alters the composition of tasks the firm performs and, "
     "therefore, the composition of the workforce it demands. Youth employment can accordingly be "
     "understood as a system-level outcome that emerges from the interaction between the technical "
     "subsystem (intelligent production) and the social subsystem (skill formation, employment "
     "governance, and organizational routines) {{sts4|oipt}}."),

    ('p', "The task-based framework of technological change clarifies the mechanisms through which "
     "intelligent transformation affects labor demand. In this framework, technology exerts two "
     "opposing forces: a displacement effect, whereby automation substitutes machines for labor in "
     "tasks previously performed by workers, and a reinstatement (or productivity and creation) "
     "effect, whereby technology generates new tasks and expands labor demand in activities where "
     "labor retains a comparative advantage {{acemoglu2019|acemoglu2022}}. Cross-country and "
     "firm-level evidence indicates that the net employment effect of robot adoption is highly "
     "heterogeneous: negative in some aggregate settings {{robots_us}}, but frequently positive at "
     "the firm level, where adopters expand output, upgrade products, and hire complementary labor "
     "{{robots_japan|robots_china_firm|robots_china2}}."),

    ('p', "For young workers, this task reallocation carries a distinctive age-specific logic. "
     "First, the new tasks reinstated by intelligent transformation—such as robot programming and "
     "maintenance, industrial data analysis, digital quality control, and human–machine "
     "collaboration—are intensive in recently acquired digital skills, in which young workers hold "
     "a comparative advantage {{skill_demand|robots_age}}. Second, human capital theory suggests "
     "that younger workers have a longer horizon over which to amortize investments in firm- and "
     "technology-specific skills, making them attractive candidates for the newly created technical "
     "positions {{training1}}. Third, from a dynamic capabilities perspective, firms undertaking "
     "intelligent transformation must sense, seize, and reconfigure resources to exploit new "
     "opportunities; recruiting young, digitally fluent talent is a low-cost, high-flexibility way "
     "to build the absorptive capacity required for technological renewal {{teece}}. At the same "
     "time, intelligent transformation may displace some young workers from entry-level routine "
     "positions, and firms facing adjustment costs may delay hiring. Whether the creation force "
     "dominates is therefore an empirical question; on balance, in a region whose transformation is "
     "growth-oriented rather than purely cost-cutting, we expect the creation and reinstatement "
     "forces to dominate for young workers."),

    ('hyp', 'H1a.', "Industrial intelligent transformation increases the firm's youth-employment share."),

    ('p', "Beyond the quantity of youth employment, intelligent transformation may also reshape the "
     "career development of young workers within the firm. Organizational renewal driven by new "
     "technology tends to revalue the knowledge base of the workforce: seniority-based advantages "
     "erode when production logic shifts toward digital and data-driven competencies, opening "
     "promotion opportunities for younger technical and managerial talent {{career1|career2}}. "
     "Firms undergoing intelligent transformation are more likely to establish new digital business "
     "units, smart-manufacturing divisions, and data teams, which create management positions "
     "disproportionately filled by young professionals {{textmeasure1}}. From a socio-economic "
     "systems perspective, the advancement of young managers reflects the adaptation of the "
     "organizational authority structure to the requirements of the transformed technical "
     "subsystem. We therefore expect intelligent transformation to increase the representation of "
     "young executives, an observable marker of youth career development."),

    ('hyp', 'H1b.', "Industrial intelligent transformation increases the representation of young "
     "executives, promoting youth career development."),

    ('h2', '2.3. Mediating Mechanisms: Skill Restructuring and Productivity-Driven Expansion'),

    ('p', "From a socio-economic systems perspective, firms translate technological change into "
     "labor outcomes through the reconfiguration of both their human capital and their scale of "
     "activity. Accordingly, this study identifies two mediating mechanisms: a skill-restructuring "
     "effect through the upgrading of the firm skill structure and an expansion effect through "
     "productivity-driven growth."),

    ('p', "The first mechanism concerns skill restructuring. Skill-biased technological change "
     "theory holds that advanced technologies are complementary to high-skill labor and "
     "substitutable for low-skill routine labor, thereby raising the relative demand for skilled "
     "workers {{acemoglu2022|skill_demand}}. Intelligent transformation intensifies this bias: it "
     "automates codifiable routine tasks while increasing the marginal product of workers who can "
     "program, deploy, maintain, and collaborate with intelligent systems {{robots_japan|sbtc1|im_hc}}. "
     "As firms upgrade their production systems, they raise the share of technically educated, "
     "high-skill employees. Because the most recent cohorts of graduates are the primary carriers "
     "of digital and analytical skills, an upgrading of the firm skill structure translates into "
     "greater relative demand for young, high-skill workers {{skill_demand|mismatch1}}. In "
     "socio-technical terms, skill upgrading reflects the adaptation of the human-capital component "
     "of the social subsystem to the requirements of the intelligent technical subsystem. We "
     "therefore expect intelligent transformation to promote youth employment partly by upgrading "
     "the firm skill structure."),

    ('hyp', 'H2a (Skill-Restructuring Effect).', "Industrial intelligent transformation promotes "
     "youth employment by upgrading the firm skill structure."),

    ('p', "The second mechanism concerns productivity-driven expansion. The productivity effect in "
     "the task-based framework implies that automation lowers production costs, improves quality "
     "and flexibility, and thereby expands product demand and firm scale "
     "{{acemoglu2019|robots_china2}}. Firm-level studies find that robot adopters grow faster in "
     "output and employment than non-adopters, as scale expansion offsets within-task displacement "
     "{{robots_japan|robots_china_firm}}. Expanding firms recruit disproportionately from the "
     "external labor market, where young job seekers are concentrated; growth also relaxes the "
     "budget constraints that otherwise bias hiring toward experienced incumbents "
     "{{digital_emp1|prod1}}. In socio-economic system terms, the expansion effect couples the "
     "technical subsystem to the regional youth labor market through the growth of the firm's "
     "value-creation activities. We therefore expect intelligent transformation to promote youth "
     "employment partly by raising labor productivity and expanding firm scale."),

    ('hyp', 'H2b (Expansion Effect).', "Industrial intelligent transformation promotes youth "
     "employment by raising labor productivity and expanding the firm's scale of activity."),

    ('h2', '2.4. The Moderating Role of Multi-Level Employment Governance'),

    ('p', "From a socio-economic systems perspective, the extent to which intelligent "
     "transformation is translated into youth employment depends on the social and institutional "
     "subsystem that governs skill formation and labor-market matching. Organizational information "
     "processing theory argues that environmental and technological change increases the demand for "
     "information-processing and coordination capacity, and that organizations embedded in stronger "
     "governance arrangements are better able to absorb and exploit new technologies {{oipt}}. We "
     "focus on three governance mechanisms that span the firm, regional, and policy levels "
     "emphasized by regional socio-economic system analysis: firm training investment, regional "
     "public employment services, and digital-economy policy pilots."),

    ('p', "Firm training investment captures the organization's internal capability to convert new "
     "technology into usable skills. Firms that invest more in employee training can rapidly equip "
     "newly hired young workers with the firm- and technology-specific competencies required by "
     "intelligent production, lowering the effective cost of youth recruitment and reducing "
     "skill-mismatch frictions {{training1|training2}}. Training investment also signals a "
     "human-capital-augmenting rather than labor-displacing transformation strategy, which "
     "encourages complementary hiring. We therefore expect firm training investment to amplify the "
     "positive effect of intelligent transformation on youth employment."),

    ('hyp', 'H3a.', "The positive effect of industrial intelligent transformation on youth "
     "employment is positively moderated by firm training investment."),

    ('p', "Regional public employment services capture the quality of the local labor-market "
     "matching infrastructure, including public job-placement platforms, vocational training "
     "programs, and employment subsidies {{alm1|vet1}}. Effective public employment services reduce "
     "search and matching costs between upgrading firms and young job seekers, provide "
     "complementary vocational training that aligns graduate skills with the requirements of "
     "intelligent manufacturing, and cushion the adjustment costs of displaced routine workers "
     "{{alm2}}. In system terms, public employment services strengthen the coupling between the "
     "regional skill-formation subsystem and the firm's technical subsystem. We therefore expect "
     "stronger regional public employment services to amplify the youth-employment benefits of "
     "intelligent transformation."),

    ('hyp', 'H3b.', "The positive effect of industrial intelligent transformation on youth "
     "employment is positively moderated by regional public employment services."),

    ('p', "Digital-economy policy pilots capture the supportiveness of the institutional "
     "environment for intelligent transformation, including national big-data comprehensive pilot "
     "zones and new-generation artificial intelligence innovation and development pilot zones "
     "{{pilot1|pilot2}}. Such pilots provide regulatory clarity, digital infrastructure, fiscal "
     "incentives, and talent-attraction programs that lower the uncertainty and adjustment costs of "
     "transformation and raise the returns to expansion strategies that draw on young digital "
     "talent {{pilot1|esg_labor}}. From a socio-economic systems perspective, policy pilots "
     "constitute the institutional layer of the social subsystem that conditions how the technical "
     "subsystem is deployed. We therefore expect supportive digital-economy policy pilots to "
     "strengthen the positive effect of intelligent transformation on youth employment."),

    ('hyp', 'H3c.', "The positive effect of industrial intelligent transformation on youth "
     "employment is positively moderated by supportive digital-economy policy pilots."),

    ('p', "The conceptual framework of this study is illustrated in Figure 1."),

    ('figure', 'fig_framework.png', 4860000, 2700000, 1),
    ('figcap', 1, 'The conceptual framework.'),
]
