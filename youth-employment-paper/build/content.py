# -*- coding: utf-8 -*-
"""Structured manuscript content.

Each block is a tuple. Supported kinds:
  ('h1', text) ('h2', text) ('h3', text)
  ('p', text)            paragraph; supports inline $latex$ and [[citekey]] citations
  ('eq', latex, number)  numbered display equation
  ('hyp', label, text)   hypothesis statement (bold label)
  ('table', table_id)    table placeholder (rendered by build script)
  ('fig', caption)       figure caption line
  ('abstract', text)
  ('keywords', text)
Citations are semantic keys resolved to MDPI numbers by first appearance.
"""

TITLE = ("Artificial Intelligence Adoption and Youth Employment: A Socio-Technical "
         "Systems Perspective on Business Model Innovation and Entrepreneurial Governance")

ABSTRACT = (
    "The diffusion of artificial intelligence (AI) reshapes not only how firms create value "
    "but also who they hire, making the youth-employment consequences of firm-level AI adoption "
    "a central concern for sustainable entrepreneurship in a dynamic global ecosystem. From a "
    "socio-technical systems perspective, AI adoption represents a technological subsystem shock "
    "that simultaneously displaces routine tasks and reinstates new digitally intensive tasks, "
    "while entrepreneurial governance mechanisms shape whether firms translate this shock into "
    "youth-oriented job creation. Using panel data on 3186 Chinese A-share listed firms from 2011 "
    "to 2023, we examine how firm AI adoption affects youth employment and through which "
    "mechanisms. We employ two-way fixed-effects models, mediation and moderation analyses, and a "
    "battery of robustness checks, including propensity score matching and instrumental-variable "
    "estimation. We find, first, that AI adoption significantly promotes youth employment, and "
    "this result is robust across alternative measures, samples, and identification strategies. "
    "Second, this effect operates through two resource-reconfiguration channels: a value-creation "
    "effect through business model innovation and a skill-restructuring effect through upgrading "
    "of the firm skill structure. Third, entrepreneurial governance plays a decisive moderating "
    "role: stronger digital entrepreneurial orientation, higher sustainability (ESG) performance, "
    "and supportive public AI and digital-economy governance significantly strengthen the positive "
    "effect of AI adoption on youth employment. Moreover, the effect is stronger for high-technology, "
    "larger, non-state-owned, and eastern-region firms. These findings suggest that youth employment "
    "is not a mechanical by-product of automation but a socio-technical adaptation outcome shaped by "
    "technological change, business model transformation, and multi-level governance. The study "
    "offers evidence and implications for sustainable, AI-enabled, and inclusive entrepreneurship."
)

KEYWORDS = ("artificial intelligence adoption; youth employment; business model innovation; "
            "sustainable entrepreneurship; socio-technical systems; entrepreneurial governance; "
            "digital transformation; skill-biased technological change")

BLOCKS = []
def h1(t): BLOCKS.append(('h1', t))
def h2(t): BLOCKS.append(('h2', t))
def h3(t): BLOCKS.append(('h3', t))
def p(t): BLOCKS.append(('p', t))
def eq(latex, num): BLOCKS.append(('eq', latex, num))
def hyp(label, t): BLOCKS.append(('hyp', label, t))
def table(tid): BLOCKS.append(('table', tid))
def fig(cap): BLOCKS.append(('fig', cap))

# =====================================================================================
# 1. INTRODUCTION
# =====================================================================================
h1("1. Introduction")

p("Youth employment has become one of the most pressing challenges of the contemporary global "
  "economy. The International Labour Organization estimates that the global youth unemployment "
  "rate remains substantially higher than the adult rate, and that a large share of young people "
  "are not in employment, education, or training [[ilo-neet]]. At the same time, the rapid "
  "diffusion of artificial intelligence (AI) is transforming the structure of labor demand, "
  "automating routine tasks while creating new digitally intensive occupations [[acemoglu-tasks]]. "
  "How firm-level AI adoption reshapes the demand for young workers is therefore a question of "
  "first-order importance for sustainable entrepreneurship, inclusive growth, and the design of "
  "business models in a dynamic global ecosystem [[ai-future-work]].")

p("The prevailing public debate frames AI mainly as a threat to employment, emphasizing the "
  "displacement of workers by intelligent machines [[frey-automation]]. Yet a growing body of "
  "firm-level evidence suggests a more nuanced picture: AI adoption can complement labor, raise "
  "productivity, and generate new roles associated with data, platforms, and digitally enabled "
  "services [[rammer-ai-innovation]]. For young workers in particular, the net effect is "
  "theoretically ambiguous. On the one hand, youth are overrepresented in entry-level routine "
  "occupations that are most exposed to automation. On the other hand, as digital natives with "
  "recently acquired human capital, young workers hold a comparative advantage in the new "
  "digitally intensive tasks that AI reinstates [[ai-skills-demand]]. Which of these forces "
  "dominates is ultimately an empirical question that depends on how firms redesign their "
  "business models and how entrepreneurial and public governance mechanisms channel technological "
  "change toward inclusive value creation.")

p("This study addresses this question from a socio-technical systems perspective. Socio-technical "
  "systems theory conceptualizes the firm as an adaptive system in which technological and social "
  "subsystems must be jointly optimized rather than changed in isolation [[sociotech-theory]]. "
  "From this perspective, AI adoption constitutes a technological subsystem transformation; the "
  "firm's entrepreneurial governance—its digital entrepreneurial orientation, sustainability "
  "orientation, and embeddedness in supportive public governance—constitutes the social and "
  "organizational subsystem; and youth employment represents a system-level labor and "
  "value-creation outcome. Accordingly, the relationship between AI adoption and youth employment "
  "is not a simple technology–labor substitution, but a socio-technical adaptation process shaped "
  "by technological change, business model transformation, resource reconfiguration, and "
  "multi-level governance [[digital-transformation-st]].")

p("China provides a representative setting for this inquiry. As the world's largest developing "
  "economy and a global leader in AI investment and application, China has experienced both rapid "
  "enterprise AI adoption and acute youth-employment pressure, with the urban youth unemployment "
  "rate reaching historically high levels in recent years [[china-youth-unemp]]. The coexistence "
  "of intensive digital transformation among listed firms, a large cohort of educated young "
  "labor-market entrants, and active industrial and digital-economy policy makes China an "
  "informative laboratory for examining how firm AI adoption, business model innovation, and "
  "entrepreneurial governance jointly shape youth employment [[china-digital-economy]].")

p("Existing research has examined the employment effects of automation and AI, the determinants "
  "of youth employment, and business model innovation, respectively. However, these streams have "
  "largely developed in parallel. The macro and task-based literature on automation and jobs "
  "rarely distinguishes age-specific effects or connects them to firm-level business model "
  "transformation [[acemoglu-robots]]. The youth-employment literature emphasizes education, "
  "institutions, and macroeconomic conditions but pays limited attention to firm-level technology "
  "adoption [[youth-emp-determinants]]. The business model innovation and digital entrepreneurship "
  "literature analyzes value creation and capture but seldom traces the labor-market, and "
  "especially the youth-employment, consequences of AI-enabled business models [[bmi-value]]. Less "
  "attention has thus been paid to how firm AI adoption, business model innovation, skill "
  "restructuring, and multi-level governance interact within a unified firm-level system to shape "
  "youth employment.")

p("Based on the above analysis, we use panel data on 3186 Chinese A-share listed firms from 2011 "
  "to 2023 to examine the impact of firm AI adoption on youth employment, its underlying "
  "mechanisms, and the moderating role of entrepreneurial governance. The empirical results show "
  "that, first, AI adoption significantly promotes youth employment, and this finding remains "
  "robust after a series of robustness checks, including propensity score matching and "
  "instrumental-variable estimation. Second, entrepreneurial governance plays a crucial "
  "moderating role: firms with stronger digital entrepreneurial orientation, higher sustainability "
  "(ESG) performance, and greater exposure to supportive public AI and digital-economy governance "
  "exhibit a stronger positive response of youth employment to AI adoption. Third, this positive "
  "effect is primarily transmitted through two channels: a value-creation effect and a "
  "skill-restructuring effect. On the one hand, AI adoption fosters business model innovation, "
  "which creates new digitally intensive roles suited to young workers. On the other hand, AI "
  "adoption upgrades the firm skill structure, raising the relative demand for high-skill labor in "
  "which youth hold a comparative advantage. Furthermore, the positive effect of AI adoption on "
  "youth employment is significantly stronger for high-technology, larger, non-state-owned, and "
  "eastern-region firms.")

p("Our contributions are threefold. First, we clarify the theoretical novelty of framing youth "
  "employment as a socio-technical adaptation outcome of firm AI adoption. Prior studies mainly "
  "examine the aggregate or task-level employment effects of automation, or treat AI adoption as a "
  "productivity or innovation input. We extend these studies by showing how external technological "
  "change, business model transformation, resource reconfiguration, and multi-level governance "
  "jointly shape the youth-employment consequences of AI adoption, thereby connecting the "
  "automation–employment debate with research on sustainable and digital entrepreneurship.")

p("Second, we extend the literature on the labor-market effects of AI by identifying two "
  "resource-reconfiguration mechanisms through which AI adoption promotes youth employment: a "
  "value-creation channel operating through business model innovation and a skill-restructuring "
  "channel operating through the upgrading of the firm skill structure. This reveals how firms "
  "reconfigure their value-creation logic and human capital when adopting AI, and why young "
  "workers benefit from this reconfiguration.")

p("Third, we enrich research on entrepreneurial and AI governance by showing that digital "
  "entrepreneurial orientation, sustainability performance, and supportive public AI and "
  "digital-economy governance strengthen the positive effect of AI adoption on youth employment. "
  "This highlights entrepreneurial governance as a key condition that helps firms translate AI "
  "adoption into inclusive, youth-oriented value creation, directly addressing the Special Issue's "
  "concern with governance mechanisms in AI-enabled sustainable entrepreneurship.")

p("The rest of this study is organized as follows. Section 2 presents the theoretical analysis and "
  "hypotheses. Section 3 describes the research design. Section 4 reports the empirical results. "
  "Section 5 discusses the findings and limitations. Section 6 concludes the study and presents "
  "the implications.")

# =====================================================================================
# 2. THEORETICAL ANALYSIS AND HYPOTHESES
# =====================================================================================
h1("2. Theoretical Analysis and Hypotheses")

h2("2.1. AI Adoption and Youth Employment: A Socio-Technical Systems Perspective")

p("Socio-technical systems theory provides an overarching basis for understanding the relationship "
  "between firm AI adoption and youth employment. It emphasizes that organizational transformation "
  "depends on the alignment and joint optimization of social and technical subsystems rather than "
  "on technological change alone [[sociotech-theory]]. In the context of this study, AI adoption "
  "reconfigures the technical subsystem by embedding data-driven prediction, automation, and "
  "decision support into production and service processes. This technological reconfiguration in "
  "turn alters the composition of tasks the firm performs and, therefore, the composition of the "
  "workforce it demands. Youth employment can accordingly be understood as a system-level outcome "
  "that emerges from the interaction between the technical subsystem (AI-enabled tasks) and the "
  "social subsystem (entrepreneurial governance, human capital, and organizational routines) "
  "[[digital-transformation-st]].")

p("The task-based framework of technological change clarifies the mechanisms through which AI "
  "adoption affects labor demand. In this framework, technology exerts two opposing forces: a "
  "displacement effect, whereby automation substitutes machines for labor in tasks previously "
  "performed by workers, and a reinstatement (or productivity and creation) effect, whereby "
  "technology generates new tasks and expands labor demand in activities where labor retains a "
  "comparative advantage [[acemoglu-tasks]]. The net employment effect of AI depends on the "
  "relative strength of these forces, which is itself shaped by how firms reorganize work and "
  "create value [[ai-employment-firm]]. Recent firm-level evidence indicates that, for many firms, "
  "AI adoption is associated with employment growth rather than contraction, because the "
  "productivity and creation effects offset pure displacement [[rammer-ai-innovation]].")

p("For young workers, this task reallocation carries a distinctive age-specific logic. First, the "
  "new tasks reinstated by AI—such as data annotation and analysis, algorithm supervision, "
  "digital marketing, platform operations, and human–AI collaboration—are intensive in recently "
  "acquired digital skills. As digital natives whose formal education has more recently "
  "incorporated computational and data competencies, young workers hold a comparative advantage in "
  "these tasks [[ai-skills-demand]]. Second, human capital theory suggests that younger workers "
  "have a longer horizon over which to amortize investments in firm-specific and technology-"
  "specific skills, making them attractive candidates for roles created by AI-enabled business "
  "models [[human-capital-skills]]. Third, from a dynamic capabilities perspective, firms that "
  "adopt AI must sense, seize, and reconfigure resources to exploit new opportunities; recruiting "
  "young, digitally fluent talent is a low-cost, high-flexibility way to build the absorptive "
  "capacity required for AI-enabled renewal [[dynamic-capabilities-ai]].")

p("At the same time, AI adoption may displace some young workers from entry-level routine "
  "positions, and firms facing adjustment costs or skill mismatches may delay hiring. Whether the "
  "creation force dominates the displacement force is therefore not predetermined; it depends on "
  "the firm's capacity to reconfigure its business model and human capital and on the governance "
  "arrangements that guide this reconfiguration. From a socio-technical systems perspective, when "
  "the technical subsystem (AI) and the social subsystem (entrepreneurial governance and human "
  "capital) are jointly optimized, AI adoption is expected to expand the demand for young, "
  "digitally skilled labor. We therefore expect that, on balance, AI adoption promotes youth "
  "employment by reinstating digitally intensive tasks in which young workers hold a comparative "
  "advantage.")

hyp("H1.", "Firm AI adoption promotes youth employment.")

h2("2.2. Mediating Mechanisms Between AI Adoption and Youth Employment")

p("From a socio-technical systems perspective, firms translate technological change into labor "
  "outcomes through the reconfiguration of both their value-creation logic and their human capital. "
  "AI adoption may not only enable firms to design new business models that generate new roles, but "
  "also upgrade the overall skill structure of the workforce. Accordingly, this study identifies "
  "two mediating mechanisms: a value-creation effect through business model innovation and a "
  "skill-restructuring effect through the upgrading of the firm skill structure.")

p("The first mechanism concerns business model innovation. A business model describes how a firm "
  "creates, delivers, and captures value; business model innovation refers to novel "
  "reconfigurations of these elements [[bmi-value]]. AI is a general-purpose technology that "
  "enables new value-creation logics—data-driven personalization, predictive services, platform "
  "orchestration, and servitization—that frequently require the firm to establish new business "
  "units, product lines, and customer-facing digital operations [[ai-bmi]]. These new activities "
  "are labor-using and disproportionately staffed by young, digitally skilled workers, because "
  "they involve emerging competencies and flexible, project-based work arrangements characteristic "
  "of digital entrepreneurship [[digital-entrepreneurship]]. In the language of the task-based "
  "framework, business model innovation is a principal channel through which AI reinstates new "
  "tasks; in socio-technical terms, it is the organizational mechanism that couples the technical "
  "subsystem to expanded and youth-oriented labor demand. We therefore expect that AI adoption "
  "promotes youth employment partly by fostering business model innovation.")

hyp("H2a (Value-Creation Effect).",
    "AI adoption promotes youth employment by fostering business model innovation.")

p("The second mechanism concerns the upgrading of the firm skill structure. Skill-biased "
  "technological change theory holds that advanced technologies are complementary to high-skill "
  "labor and substitutable for low-skill routine labor, thereby raising the relative demand for "
  "skilled workers [[skill-biased-tech]]. AI adoption intensifies this bias: it automates codifiable "
  "routine tasks while increasing the marginal product of workers who can develop, deploy, "
  "interpret, and collaborate with intelligent systems [[ai-skills-demand]]. As firms adopt AI, "
  "they raise the share of high-skill, technically educated employees. Because the most recent "
  "cohorts of graduates are the primary carriers of AI-relevant digital and analytical skills, an "
  "upgrading of the firm skill structure translates into greater relative demand for young, "
  "high-skill workers [[human-capital-skills]]. From a socio-technical systems perspective, skill "
  "upgrading reflects the adaptation of the human-capital component of the social subsystem to the "
  "requirements of the AI-enabled technical subsystem. We therefore expect that AI adoption "
  "promotes youth employment partly by upgrading the firm skill structure.")

hyp("H2b (Skill-Restructuring Effect).",
    "AI adoption promotes youth employment by upgrading the firm skill structure.")

h2("2.3. The Moderating Role of Entrepreneurial Governance")

p("From a socio-technical systems perspective, the extent to which AI adoption is translated into "
  "youth employment depends on the social and organizational subsystem that governs technological "
  "change. Organizational information processing theory argues that environmental and technological "
  "uncertainty increases the demand for information-processing capacity, and that firms with "
  "stronger governance and strategic-orientation capabilities are better able to interpret and "
  "exploit new technologies [[oipt]]. We focus on three governance mechanisms that span the "
  "corporate and public levels emphasized by the Special Issue: digital entrepreneurial "
  "orientation, sustainability orientation, and public AI and digital-economy governance.")

p("Digital entrepreneurial orientation captures a firm's proactive, innovative, and risk-tolerant "
  "posture toward digital opportunities [[digital-entrepreneurship]]. Firms with a stronger digital "
  "entrepreneurial orientation are more likely to interpret AI as an opportunity for new "
  "value creation rather than merely a tool for cost-cutting and headcount reduction. Guided by a "
  "dynamic-capabilities logic, such firms actively sense AI-enabled opportunities, seize them by "
  "launching new digital ventures and business lines, and reconfigure their human capital by hiring "
  "young digital talent [[dynamic-capabilities-ai]]. Digital entrepreneurial orientation thus "
  "strengthens the coupling between the technical subsystem (AI) and youth-oriented labor demand. "
  "We therefore expect it to amplify the positive effect of AI adoption on youth employment.")

hyp("H3a.",
    "The positive effect of AI adoption on youth employment is positively moderated by the firm's "
    "digital entrepreneurial orientation.")

p("Sustainability orientation, captured by firms' environmental, social, and governance (ESG) "
  "performance, reflects a strategic commitment to creating economic, social, and environmental "
  "value simultaneously [[esg-employment]]. The social dimension of ESG explicitly encompasses "
  "responsible employment, human-capital development, and inclusive hiring, which are aligned with "
  "youth-oriented job creation [[sustainable-entrepreneurship]]. Firms with stronger sustainability "
  "orientation are more likely to embed AI adoption within a broader agenda of sustainable value "
  "creation, using AI-enabled growth to expand employment opportunities for young workers rather "
  "than solely to reduce labor costs. In socio-technical terms, sustainability orientation aligns "
  "the normative goals of the social subsystem with inclusive technological adaptation. We "
  "therefore expect it to strengthen the positive effect of AI adoption on youth employment.")

hyp("H3b.",
    "The positive effect of AI adoption on youth employment is positively moderated by the firm's "
    "sustainability (ESG) performance.")

p("Public AI and digital-economy governance captures the quality of the institutional environment "
  "in which the firm is embedded, including regulatory quality, digital-economy policy support, and "
  "AI governance frameworks [[ai-governance-policy]]. Supportive public governance reduces the "
  "uncertainty and adjustment costs associated with AI adoption, provides infrastructure and "
  "skills-training complementarities, and signals a stable long-term commitment to digital and "
  "inclusive growth [[china-digital-economy]]. Institutional support thus lowers the risk that "
  "firms respond to AI adoption with defensive downsizing and raises the returns to AI-enabled "
  "expansion that draws on young digital talent. From a socio-technical systems perspective, public "
  "governance constitutes the institutional layer of the social subsystem that conditions how the "
  "technical subsystem is deployed. We therefore expect supportive public AI and digital-economy "
  "governance to strengthen the positive effect of AI adoption on youth employment.")

hyp("H3c.",
    "The positive effect of AI adoption on youth employment is positively moderated by supportive "
    "public AI and digital-economy governance.")

p("The conceptual framework of this study is illustrated in Figure 1.")
fig("Figure 1. The conceptual framework.")

# =====================================================================================
# 3. RESEARCH DESIGN
# =====================================================================================
h1("3. Research Design")

h2("3.1. Variable Measurement")

h3("3.1.1. Youth Employment")

p("Conceptually, youth employment refers to the firm-level demand for young workers, that is, the "
  "extent to which a firm employs workers in the early stage of their careers. Empirically, "
  "because employee age structure is disclosed with increasing coverage in the corporate-governance "
  "and employee files of Chinese listed firms, we measure youth employment ($YEMP$) as the share of "
  "a firm's employees aged 30 years and below in total employees, as defined in Equation (1):")

eq(r"YEMP_{i,t} = \dfrac{\text{Emp30}_{i,t}}{\text{Emp}_{i,t}}", "1")

p("where $\\text{Emp30}_{i,t}$ is the number of employees aged 30 years and below in firm $i$ in "
  "year $t$, and $\\text{Emp}_{i,t}$ is the firm's total number of employees. Using a share rather "
  "than a level purges the measure of firm-size effects and captures the composition of labor "
  "demand toward young workers. Because a small number of firms report age structure using a "
  "35-year threshold, we construct an alternative measure ($YEMP\\_2$), the share of employees aged "
  "35 and below, for robustness. Employee age-structure and headcount data were obtained from the "
  "China Stock Market and Accounting Research Database (CSMAR) and supplemented by hand-collection "
  "from firms' annual reports. This measure captures the age composition of the firm's workforce "
  "rather than gross youth hiring flows, which are not separately disclosed.")

h3("3.1.2. Firm AI Adoption")

p("We measured firm AI adoption ($AI$) using a text-based indicator constructed from firms' annual "
  "reports, following the digital-transformation measurement literature [[digital-transformation-measure]]. "
  "Specifically, we compiled a dictionary of AI-related terms spanning core technologies and "
  "applications—for example, artificial intelligence, machine learning, deep learning, neural "
  "networks, natural language processing, computer vision, knowledge graphs, intelligent robots, "
  "autonomous driving, and intelligent decision-making—and used Python word segmentation to count "
  "the frequency of these terms in the management discussion and analysis (MD&A) and business "
  "sections of each firm's annual report. Firm AI adoption is measured as the natural logarithm of "
  "one plus the total AI-term frequency, as shown in Equation (2):")

eq(r"AI_{i,t} = \ln\left(1 + \sum_{k=1}^{K} \text{Freq}_{k,i,t}\right)", "2")

p("where $\\text{Freq}_{k,i,t}$ is the frequency of AI-related keyword $k$ in the annual report of "
  "firm $i$ in year $t$, and $K$ is the number of keywords in the dictionary. The logarithmic "
  "transformation mitigates right-skewness and the influence of outliers. To mitigate potential "
  "simultaneity and reverse causality, we used the one-year lag of AI adoption, $AI_{i,t-1}$, in the "
  "regression analysis, ensuring that AI adoption is measured prior to youth-employment outcomes. "
  "As alternative measures, we used the number of AI-related invention patents and a keyword-based "
  "indicator scaled by report length.")

h3("3.1.3. Mediating Variables")

p("To unpack the channels through which AI adoption affects youth employment, we focused on two "
  "mediators: business model innovation and firm skill structure.")

p("Business model innovation ($BMI$). Following the text-based strategy-measurement literature, we "
  "measured business model innovation using the frequency of terms related to new value creation, "
  "delivery, and capture—such as new business model, platform, ecosystem, servitization, "
  "value chain reconstruction, digital service, and new profit model—in the annual report, divided "
  "by the total word count to control for report length, and then min–max normalized to the [0, 1] "
  "interval, as in Equation (3):")

eq(r"X_{i,t}^{\text{norm}} = \dfrac{X_{i,t} - \min(X)}{\max(X) - \min(X)}", "3")

p("where $X_{i,t}$ is the raw length-adjusted frequency for firm $i$ in year $t$. A higher value "
  "indicates more intensive business model innovation. Because text-based measures capture "
  "disclosure emphasis rather than realized outcomes, we also used the ratio of new-product or "
  "new-business revenue to total revenue as an alternative measure of the value-creation channel.")

p("Firm skill structure ($SKILL$). We proxied the firm skill structure by the share of employees "
  "holding a bachelor's degree or above in total employees, based on the education-structure data "
  "in CSMAR. A higher value indicates a more skill-intensive workforce. As an alternative, we used "
  "the share of technical and R&D personnel in total employees. Both measures capture the extent to "
  "which the firm's human capital is oriented toward high-skill, technology-complementary tasks.")

h3("3.1.4. Moderating Variables")

p("To test the moderating role of entrepreneurial governance, we constructed three variables "
  "spanning corporate strategic orientation, sustainability performance, and public governance.")

p("Digital entrepreneurial orientation ($DEO$). We measured digital entrepreneurial orientation "
  "using a text-based indicator that combines entrepreneurial-orientation terms (innovativeness, "
  "proactiveness, and risk-taking) with digital terms (digitalization, digital platform, digital "
  "ecosystem, and data-driven) in the annual report, scaled by report length and min–max "
  "normalized to the [0, 1] interval [[digital-entrepreneurship]]. A higher value indicates a "
  "stronger proactive posture toward digital opportunity.")

p("Sustainability performance ($ESG$). We measured sustainability orientation using the "
  "third-party Huazheng (SinoSecurities) ESG rating, which assigns firms a nine-grade score that "
  "we converted to a 1–9 numerical scale, with higher values indicating stronger ESG performance "
  "[[esg-employment]]. As an alternative, we used the ESG rating from the SynTao Green Finance "
  "database.")

p("Public AI and digital-economy governance ($GOV$). We measured supportive public governance using "
  "a dummy variable equal to 1 if the firm is registered in a city designated as a national big-data "
  "comprehensive pilot zone or a national new-generation AI innovation development pilot zone in "
  "year $t$, and 0 otherwise [[ai-governance-policy]]. These national pilots provide regulatory "
  "support, digital infrastructure, and skills-training complementarities for AI adoption. As an "
  "alternative, we used the provincial digital-economy policy-support index and the provincial "
  "government regulatory-quality index.")

h3("3.1.5. Control Variables")

p("Following the extant literature, we controlled for a series of firm- and city-level variables "
  "that may affect youth employment. Firm-level controls include firm age ($Age$), firm size "
  "($Size$), leverage ($Lev$), profitability ($RoA$), cash flow ($Cash$), sales growth ($Growth$), "
  "the share of the top ten shareholders ($Top10$), board size ($Board$), CEO–chair separation "
  "($Separation$), and state ownership ($SOE$). To account for regional economic conditions, we "
  "further included the natural logarithm of the gross domestic product of the city where the firm "
  "is registered ($lngdp$), which controls for differences in local economic development, labor-"
  "market conditions, and demand that may be correlated with both AI adoption and youth employment. "
  "Detailed definitions of all variables are provided in Appendix A.1.")

h2("3.2. Regression Model Specification")

h3("3.2.1. Baseline Model")

p("To examine the impact of AI adoption on youth employment, we estimated Equation (4):")

eq(r"YEMP_{i,t} = \alpha + \beta_1 AI_{i,t-1} + \gamma' \text{Controls}_{i,t} + \mu_i + \lambda_t + \varepsilon_{i,t}", "4")

p("Here, $i$ indexes firms and $t$ indexes years. The dependent variable $YEMP_{i,t}$ measures the "
  "youth-employment share of firm $i$ in year $t$ (Section 3.1.1). We used the one-year lag of AI "
  "adoption, $AI_{i,t-1}$, to mitigate simultaneity and reverse-causality concerns and to ensure "
  "that AI adoption is measured prior to youth-employment outcomes (Section 3.1.2). "
  "$\\text{Controls}_{i,t}$ includes the firm- and city-level controls. We included firm fixed "
  "effects $\\mu_i$ and year fixed effects $\\lambda_t$; $\\varepsilon_{i,t}$ is the error term, and "
  "standard errors are robust and clustered at the firm level. The coefficient of interest is "
  "$\\beta_1$, and H1 predicts $\\beta_1 > 0$.")

h3("3.2.2. Mediation Models")

p("To test the mediating mechanisms, we estimated Equations (5) and (6):")

eq(r"M_{i,t} = \alpha + \delta_1 AI_{i,t-1} + \theta' \text{Controls}_{i,t} + \mu_i + \lambda_t + \varepsilon_{i,t}", "5")
eq(r"YEMP_{i,t} = \alpha + \varphi_1 M_{i,t} + \varphi_2 AI_{i,t-1} + \kappa' \text{Controls}_{i,t} + \mu_i + \lambda_t + \varepsilon_{i,t}", "6")

p("$M_{i,t}$ denotes the mediator. For the value-creation effect (H2a), we set $M_{i,t} = BMI_{i,t}$; "
  "we expected $\\delta_1 > 0$ and $\\varphi_1 > 0$, indicating that AI adoption fosters business "
  "model innovation and that business model innovation promotes youth employment. For the "
  "skill-restructuring effect (H2b), we set $M_{i,t} = SKILL_{i,t}$; we expected $\\delta_1 > 0$ and "
  "$\\varphi_1 > 0$, indicating that AI adoption upgrades the firm skill structure and that a more "
  "skill-intensive structure raises youth employment. We report bootstrap confidence intervals for "
  "the indirect effects to assess the statistical significance of mediation.")

h3("3.2.3. Moderation Models")

p("To examine the moderating role of entrepreneurial governance, we estimated Equation (7):")

eq(r"YEMP_{i,t} = \alpha + \eta_1 AI_{i,t-1} + \eta_2 \text{Mod}_{i,t} + \eta_3 (AI_{i,t-1} \times \text{Mod}_{i,t}) + \vartheta' \text{Controls}_{i,t} + \mu_i + \lambda_t + \varepsilon_{i,t}", "7")

p("$\\text{Mod}_{i,t}$ alternatively captures digital entrepreneurial orientation ($DEO$), "
  "sustainability performance ($ESG$), and public AI and digital-economy governance ($GOV$). The "
  "coefficient of interest is $\\eta_3$, which corresponds to H3a–H3c and is expected to be "
  "positive, indicating that stronger entrepreneurial governance amplifies the positive effect of "
  "AI adoption on youth employment.")

h2("3.3. Data and Sample Selection")

p("We constructed a panel of Chinese A-share listed firms from 2011 to 2023. Following standard "
  "practice, we excluded: (1) specially treated firms (ST, *ST, or PT); (2) firms in the financial "
  "industry; and (3) firm-year observations with missing key variables. Firm financial, employee, "
  "and governance data were obtained from CSMAR; ESG ratings were obtained from the Huazheng and "
  "SynTao Green Finance databases; AI-adoption and text-based measures were constructed from firms' "
  "annual reports; and city-level GDP was obtained from the China City Statistical Yearbook. AI and "
  "text-based variables were winsorized at the 1st and 99th percentiles to mitigate the influence of "
  "outliers. The final sample comprised 28,974 firm-year observations for 3186 unique firms.")

h2("3.4. Descriptive Statistics")

p("Table 1 reports the descriptive statistics for all variables. Table 2 presents the correlation "
  "matrix. The correlations suggest a positive association between AI adoption and youth employment. "
  "Appendix A.2 reports the variance inflation factor (VIF) values, with a mean VIF of 1.98, "
  "indicating that multicollinearity is not a serious concern.")
table("T1")
table("T2")

# =====================================================================================
# 4. EMPIRICAL RESULTS
# =====================================================================================
h1("4. Empirical Results")

h2("4.1. Baseline Regression Results")

p("We estimated Equation (4) to examine the effect of AI adoption on youth employment; Table 3 "
  "reports the baseline results. Column (1) presents the parsimonious specification with firm and "
  "year fixed effects, while Column (2) adds the firm- and city-level controls. Columns (3) and (4) "
  "replace year fixed effects with industry-by-year fixed effects to control for time-varying "
  "industry shocks, with Column (4) further including the full set of controls. As an additional "
  "comparison, Columns (5) and (6) use contemporaneous AI adoption instead of the lagged measure "
  "and follow the same parsimonious-to-full-control structure. Across all specifications, the "
  "coefficient on AI adoption is positive and statistically significant at the 1% level. When using "
  "lagged AI adoption, the estimated coefficient ranges from 0.0142 to 0.0156 and remains "
  "significant after adding controls and adopting more stringent fixed effects, supporting H1.")

p("Beyond statistical significance, the results are economically meaningful. Taking the full "
  "specification with firm and year fixed effects (Column (2)) as an example, a one-standard-"
  "deviation increase in AI adoption is associated with an increase of approximately 1.7 percentage "
  "points in the youth-employment share, equivalent to about 5.6% of the mean youth-employment "
  "share in the sample. From a socio-technical systems perspective, this result suggests that AI "
  "adoption acts as a technological subsystem transformation that expands the demand for young, "
  "digitally skilled workers through task reinstatement and organizational adaptation, rather than "
  "simply displacing labor.")
table("T3")

p("From a practical perspective, AI adoption does not necessarily reduce the demand for young "
  "workers. Instead, as firms embed AI into their production and service processes, they create new "
  "digitally intensive roles and reorganize work in ways that favor the recruitment of young, "
  "digitally fluent employees. Overall, the baseline results indicate that firm AI adoption "
  "significantly promotes youth employment and may serve as an important firm-level driver of "
  "inclusive, technology-enabled labor demand.")

h2("4.2. Robustness Checks")

h3("4.2.1. Alternative Measures and Sample Restrictions")

p("To further assess robustness, we re-estimated Equation (4) using alternative measures and "
  "subsamples; Table 4 summarizes the results. First, Column (1) replaced the dependent variable "
  "with the alternative youth-employment measure based on the 35-year threshold ($YEMP\\_2$); the "
  "coefficient on AI adoption remained positive and significant. Second, Column (2) replaced the "
  "explanatory variable with the AI-patent-based measure, and the result was unchanged. Third, "
  "Column (3) excluded the year 2020 to rule out potential confounding effects of the COVID-19 "
  "shock, and the estimated effect remained significantly positive. Fourth, Column (4) excluded "
  "firms in municipalities directly under the central government, where labor markets differ "
  "substantially, and the result was robust. Fifth, Column (5) restricted the sample to "
  "manufacturing firms, and the coefficient on AI adoption remained positive and significant. "
  "Sixth, Column (6) reported results based on two-way clustered standard errors at the firm and "
  "city levels. Finally, Column (7) further included province-by-year fixed effects to control for "
  "time-varying regional factors. Across all specifications, the estimated effect of AI adoption on "
  "youth employment was consistently positive and statistically significant.")
table("T4")

h3("4.2.2. Propensity Score Matching")

p("Our baseline estimates may be subject to endogeneity from firms' self-selection into AI "
  "adoption. To address this concern, we employed propensity score matching (PSM). We defined "
  "$AI\\_dummy$ as an indicator equal to 1 for firms with AI adoption above the annual median and 0 "
  "otherwise, and estimated a probit model in the first stage using the baseline covariates and "
  "industry fixed effects. We implemented one-to-one nearest-neighbor matching without replacement "
  "and imposed a caliper of 0.01 to enhance comparability between the treatment and control groups "
  "[[psm-wellman]]. Table 5 reports the results before and after matching. The coefficient on "
  "$AI\\_dummy$ remained positive and statistically significant after matching, and its significance "
  "strengthened, suggesting that our main finding is not driven by observable differences between "
  "high- and low-AI-adoption firms. Figure 2 further shows improved covariate balance after "
  "matching.")
table("T5")
fig("Figure 2. Standardized mean differences of covariates: pre-match vs. post-match.")

h3("4.2.3. Instrumental Variable Regression")

p("To further alleviate endogeneity concerns, we employed a two-stage least squares (2SLS) "
  "instrumental-variable approach. Following the shift-share (Bartik) tradition [[bartik-iv]], we "
  "constructed the first instrument ($IV1$) as the interaction between the industry-level average AI "
  "adoption of peer firms (excluding the focal firm) and the firm's baseline digital exposure. Peer "
  "AI adoption reflects industry-wide technological trends that affect the focal firm's AI adoption "
  "but are unlikely to directly determine its youth-employment share. Following the literature that "
  "uses geographic and infrastructural conditions as exogenous drivers of technology adoption "
  "[[ai-governance-policy]], we used the second instrument ($IV2$), the historical density of fixed "
  "telephone lines in the firm's city interacted with a time trend, capturing local digital-"
  "infrastructure endowments. Table 6 reports the results. In the first stage, both instruments are "
  "positive and statistically significant, with first-stage F-statistics well above the "
  "weak-instrument threshold. In the second stage, the fitted value of AI adoption remains positively "
  "and significantly associated with youth employment, consistent with the baseline findings.")
table("T6")

h2("4.3. Mechanism Analysis")

p("Having established that AI adoption promotes youth employment, we examined the underlying "
  "mechanisms. Drawing on our hypotheses, we considered two mediating channels: business model "
  "innovation (value-creation channel) and firm skill structure (skill-restructuring channel). We "
  "estimated the mediation models in Equations (5) and (6); Table 7 reports the results.")

p("Columns (1) and (2) report the value-creation channel. Column (1) shows that AI adoption "
  "significantly increases business model innovation ($\\delta_1 = 0.087$, $p < 0.01$). Column (2) "
  "shows that business model innovation is positively and significantly associated with youth "
  "employment ($\\varphi_1 = 0.152$, $p < 0.01$), while the coefficient on AI adoption remains "
  "positive. These results are consistent with H2a, indicating that AI adoption promotes youth "
  "employment partly by fostering business model innovation. Columns (3) and (4) report the "
  "skill-restructuring channel. Column (3) shows that AI adoption significantly upgrades the firm "
  "skill structure ($\\delta_1 = 0.061$, $p < 0.01$), and Column (4) shows that a more skill-"
  "intensive structure is positively and significantly associated with youth employment "
  "($\\varphi_1 = 0.203$, $p < 0.01$). This supports H2b. Bootstrap tests confirm that both indirect "
  "effects are statistically significant. A comparison of the indirect effects indicates that the "
  "value-creation channel accounts for a somewhat larger share of the total effect than the skill-"
  "restructuring channel, suggesting that AI promotes youth employment mainly by enabling new "
  "value-creating business models, with skill upgrading serving as a complementary channel.")
table("T7")

h2("4.4. Moderating Effects of Entrepreneurial Governance")

p("Table 8 reports the moderating role of entrepreneurial governance. Consistent with H3, the "
  "interaction terms between AI adoption and the governance variables are positive and statistically "
  "significant. Column (1) shows that the interaction $AI \\times DEO$ is positive and significant "
  "($\\eta_3 = 0.041$, $p < 0.01$), indicating that firms with stronger digital entrepreneurial "
  "orientation exhibit a stronger positive response of youth employment to AI adoption, supporting "
  "H3a. Column (2) shows that the interaction $AI \\times ESG$ is positive and significant "
  "($\\eta_3 = 0.008$, $p < 0.05$), supporting H3b and indicating that sustainability orientation "
  "reinforces the youth-employment benefits of AI adoption. Column (3) shows that the interaction "
  "$AI \\times GOV$ is positive and significant ($\\eta_3 = 0.019$, $p < 0.05$), supporting H3c and "
  "indicating that supportive public AI and digital-economy governance strengthens the AI–youth-"
  "employment linkage. From a socio-technical systems perspective, these results show that "
  "entrepreneurial governance is a key social-subsystem condition that helps firms translate AI "
  "adoption into inclusive, youth-oriented value creation, and that differences in governance "
  "capacity partly explain heterogeneous youth-employment responses across firms.")
table("T8")

h2("4.5. Heterogeneity Analysis")

p("Building on the benchmark results, we explored whether the effect of AI adoption on youth "
  "employment differs across firms. We conducted subsample regressions along four dimensions: "
  "technological intensity, firm size, ownership, and region. The results are reported in Table 9. "
  "Columns (1) and (2) show that the positive effect of AI adoption on youth employment is "
  "significant for high-technology firms but insignificant for traditional firms. Columns (3) and "
  "(4) show that the effect is significant for large firms but not for small firms. Columns (5) and "
  "(6) show that the effect is significant for non-state-owned firms but not for state-owned firms. "
  "Columns (7) and (8) show that the effect is stronger for firms in the eastern region than for "
  "those in the central and western regions.")

p("Overall, the heterogeneity results suggest that the positive AI–youth-employment relationship is "
  "concentrated among high-technology, larger, non-state-owned, and eastern-region firms. From a "
  "socio-technical systems perspective, these findings indicate that firms' youth-employment "
  "responses to AI adoption depend on the alignment among technological capacity, resource "
  "endowments, entrepreneurial autonomy, and supportive regional ecosystems. High-technology and "
  "large firms possess greater capacity to reconfigure business models and human capital; non-state-"
  "owned firms have stronger entrepreneurial incentives and flexibility; and eastern-region firms "
  "benefit from more developed digital infrastructure and talent markets. AI adoption is therefore "
  "more likely to be translated into youth employment when firms have both stronger internal "
  "capabilities and stronger external ecosystem support for socio-technical adaptation.")
table("T9")

# =====================================================================================
# 5. DISCUSSION AND LIMITATIONS
# =====================================================================================
h1("5. Discussion and Limitations")

h2("5.1. Discussion")

p("First, this study shows that firm AI adoption significantly promotes youth employment. This "
  "finding suggests that, at the firm level, the creation and reinstatement forces of AI outweigh "
  "its displacement force for young workers. Unlike the pessimistic narrative that frames AI as a "
  "wholesale threat to jobs, our evidence indicates that AI adoption can expand the demand for "
  "young, digitally skilled labor. From a socio-technical systems perspective, youth employment can "
  "be understood as an adaptive labor outcome through which firms reconfigure tasks and human "
  "capital under technological change.")

p("Second, the mechanism analysis shows that this effect operates through two resource-"
  "reconfiguration pathways. The value-creation effect indicates that AI adoption fosters business "
  "model innovation, which generates new digitally intensive roles suited to young workers. The "
  "skill-restructuring effect shows that AI adoption upgrades the firm skill structure, raising the "
  "relative demand for high-skill labor in which youth hold a comparative advantage. These findings "
  "suggest that youth employment is driven both by the creation of new value-creating activities and "
  "by the upgrading of the firm's human capital.")

p("Third, the moderating results highlight the role of entrepreneurial governance as a social-"
  "subsystem condition. Firms with stronger digital entrepreneurial orientation, higher "
  "sustainability performance, and greater exposure to supportive public AI and digital-economy "
  "governance are better able to translate AI adoption into youth employment. This finding supports "
  "the view that technological change alone does not determine labor outcomes; rather, corporate and "
  "public governance mechanisms shape whether AI adoption produces inclusive, youth-oriented value "
  "creation, directly addressing the Special Issue's concern with governance in AI-enabled "
  "sustainable entrepreneurship.")

p("Finally, the heterogeneity analysis identifies the boundary conditions of this relationship. The "
  "effect of AI adoption is stronger among high-technology, larger, non-state-owned, and eastern-"
  "region firms, which possess stronger transformation capabilities, entrepreneurial incentives, or "
  "ecosystem support. These findings further suggest that youth employment emerges from the "
  "interaction among technological change, business model transformation, human-capital "
  "reconfiguration, and multi-level governance, reflecting a dynamic socio-technical adaptation "
  "process.")

h2("5.2. Limitations and Future Research")

p("This study has several limitations that provide directions for future research. First, although "
  "we measured youth employment using the share of employees aged 30 and below and adopted an "
  "alternative age threshold for robustness, this measure captures the age composition of the "
  "workforce rather than gross youth hiring and separation flows. Future research may use linked "
  "employer–employee or social-security data to examine youth hiring, retention, and job quality "
  "more directly.")

p("Second, our AI-adoption and business-model-innovation measures are text-based and therefore "
  "capture disclosure emphasis in addition to realized activity. Although we used patent-based and "
  "revenue-based alternatives for robustness, future research may combine text analysis with "
  "detailed technology-deployment, investment, and micro-level task data to better capture the "
  "multidimensional nature of AI adoption and business model innovation.")

p("Third, this study focused on Chinese A-share listed firms. The long-term consequences and "
  "contextual boundaries of the findings should therefore be interpreted with caution. Future "
  "research may examine whether AI-driven youth employment improves job quality, wages, and career "
  "development, and may test the generalizability of the findings across countries, firm types, and "
  "institutional contexts, including small and young ventures and the informal economy.")

# =====================================================================================
# 6. CONCLUSIONS AND IMPLICATIONS
# =====================================================================================
h1("6. Conclusions and Implications")

h2("6.1. Conclusions")

p("Using panel data on 3186 Chinese A-share listed firms from 2011 to 2023, this study examined the "
  "relationship between firm AI adoption and youth employment from a socio-technical systems "
  "perspective, with particular attention to business model innovation and entrepreneurial "
  "governance. The results show that AI adoption significantly promotes youth employment, and this "
  "finding remains robust across a range of tests, including propensity score matching and "
  "instrumental-variable estimation.")

p("The mechanism analysis shows that AI adoption promotes youth employment through two pathways: a "
  "value-creation effect through business model innovation and a skill-restructuring effect through "
  "the upgrading of the firm skill structure. The moderation analysis further shows that "
  "entrepreneurial governance strengthens this relationship: the positive effect of AI adoption is "
  "stronger in firms with higher digital entrepreneurial orientation, stronger sustainability "
  "performance, and greater exposure to supportive public AI and digital-economy governance. The "
  "heterogeneity analysis shows that the effect is more pronounced among high-technology, larger, "
  "non-state-owned, and eastern-region firms. These findings indicate that youth employment is not "
  "a mechanical by-product of automation, but a socio-technical adaptation outcome shaped by "
  "technological change, business model transformation, human-capital reconfiguration, and multi-"
  "level governance.")

h2("6.2. Implications")

p("This study provides several practical implications. First, firms should treat AI adoption as an "
  "opportunity for inclusive value creation rather than solely as a tool for labor cost reduction. "
  "By embedding AI within new business models and reconfiguring their human capital, firms can "
  "create new digitally intensive roles and expand opportunities for young workers, thereby aligning "
  "technological transformation with sustainable and inclusive growth.")

p("Second, firms should strengthen their entrepreneurial governance for AI-enabled transformation. "
  "Cultivating a digital entrepreneurial orientation, integrating sustainability objectives into "
  "AI strategy, and building the capabilities to sense and seize AI-enabled opportunities can help "
  "firms translate AI adoption into youth-oriented job creation. Boards and senior managers should "
  "coordinate AI investment, business model innovation, talent acquisition, and skills development "
  "to ensure that AI adoption expands rather than contracts youth employment.")

p("Third, firms should invest in the human capital that complements AI. Combining AI deployment with "
  "training, reskilling, and campus recruitment can enlarge the pool of young, digitally skilled "
  "talent and strengthen the skill-restructuring channel through which AI promotes youth employment. "
  "This is especially important for high-technology, large, and eastern-region firms, which have "
  "greater capacity to undertake system-level adaptation.")

p("Finally, policymakers can support this adaptation process by strengthening public AI and digital-"
  "economy governance. Providing regulatory clarity, digital infrastructure, AI governance "
  "frameworks, and youth-oriented skills-training programs can reduce the uncertainty and adjustment "
  "costs of AI adoption and help firms translate technological change into inclusive youth "
  "employment. Coordinating industrial, digital, and labor-market policies can foster an "
  "entrepreneurial ecosystem in which AI adoption supports sustainable and inclusive value creation "
  "across the global economy.")

# =====================================================================================
# BACK MATTER + APPENDIX
# =====================================================================================
def stmt(label, text): BLOCKS.append(('stmt', label, text))

stmt("Funding:", "This research received no external funding.")
stmt("Institutional Review Board Statement:", "Not applicable.")
stmt("Informed Consent Statement:", "Not applicable.")
stmt("Data Availability Statement:", "The datasets analyzed in this study were obtained from "
     "commercial databases (CSMAR, Huazheng, and SynTao Green Finance) under license agreements "
     "and from firms' publicly available annual reports. The processed data are available from the "
     "author upon reasonable request, subject to the licensing terms of the original providers.")
stmt("Conflicts of Interest:", "The author declares no conflicts of interest.")

h1("Appendix A")
h2("Appendix A.1")
p("Table A1 presents the detailed definitions of all variables.")
table("A1")
h2("Appendix A.2")
p("Table A2 reports the variance inflation factor (VIF) test for the main explanatory and control "
  "variables. The maximum VIF was 2.03 and the mean VIF was 1.98, both well below the commonly "
  "used threshold of 10, suggesting that multicollinearity is not a serious concern.")
table("A2")
