# -*- coding: utf-8 -*-
"""Manuscript text.

Markup conventions used inside strings:
    $latex$      inline mathematics, rendered as a native Word equation object
    [[key]]      citation; the builder replaces it with the bracketed number
"""

TITLE = ("The Vanishing First Rung? Generative AI, Organisational Learning and "
         "Youth Entry Employment in a Socio-Technical System Dynamics Model")

ABSTRACT = (
    "Generative artificial intelligence (GenAI) is diffusing fastest through exactly "
    "the codified, routine-cognitive tasks that have traditionally formed the entry "
    "port of professional careers, and early evidence indicates a disproportionate "
    "contraction of employment among workers aged 22–25 in exposed occupations. "
    "Reduced-form accounts treat this as a technological outcome. We argue instead "
    "that it is a system-level outcome: the entry port is simultaneously a production "
    "input and the intake stage of the firm's own capability pipeline, so its "
    "contraction feeds back on organisational learning, on the supply of experienced "
    "staff and, with a delay, on the firm's ability to absorb the technology at all. "
    "We formulate a six-stock socio-technical system dynamics model in which "
    "displacement, task reinstatement, learning-by-collaborating, pipeline "
    "replenishment and competitive scale interact, and we calibrate its diffusion and "
    "augmentation parameters to four independent published benchmarks. The model "
    "passes a standard battery of structure, extreme-condition, integration-error and "
    "behaviour-reproduction tests. In the calibrated baseline, entry employment falls "
    "15.0% by year three, troughs at −37.2% in year seven and remains 30.7% below the "
    "no-GenAI counterfactual after 25 years, while the output fulfilment ratio settles "
    "at 0.86 because the experienced-staff pipeline has been thinned. The sign of the "
    "long-run effect is not technologically determined: over a two-dimensional design "
    "space it ranges from −70.0% to +19.2%, and it turns positive in 17.1% of "
    "configurations. A pre-specified 2 × 2 factorial shows that work redesign and "
    "learning-system investment are complements, with a positive interaction of "
    "2.74 percentage points, supporting the joint-optimisation principle of "
    "socio-technical design. An automation-first strategy is a capability trap: it "
    "delivers the fastest unit-cost reduction of any configuration over the first "
    "three years yet leaves output 15.7% below the "
    "counterfactual after 25 years."
)

KEYWORDS = ("generative artificial intelligence; youth employment; system dynamics; "
            "socio-technical systems; organisational learning; human–AI collaboration; "
            "workforce development; feedback loops; capability trap")

BLOCKS = [

    # =====================================================================
    ("h1", "1. Introduction"),

    ("p",
     "Within three years of the public release of large language models, generative "
     "artificial intelligence (GenAI) has moved from novelty to infrastructure in "
     "knowledge-intensive work. Field experiments and quasi-experiments consistently "
     "report double-digit productivity gains: customer-support agents resolved 14% "
     "more issues per hour [[brynjolfsson2025]], professional writers completed tasks "
     "roughly 40% faster with higher rated quality [[noy2023]], consultants improved both "
     "speed and quality on tasks inside the technology's frontier [[dellacqua2026]], "
     "and software developers completed 26% more tasks across three randomised "
     "deployments [[cui2026]]. A robust and consequential regularity runs through "
     "these studies: the gains are concentrated among the least experienced. Novice "
     "support agents gained about 30% while their most experienced colleagues gained "
     "little or nothing [[brynjolfsson2025]], the lowest-performing entrepreneurs benefited "
     "while the highest-performing ones did not [[otis2026]], and less experienced "
     "developers both adopted the tool more readily and gained more from it "
     "[[cui2026]]. GenAI compresses experience."),

    ("p",
     "That same property has a darker corollary. Experience compression means that "
     "the technology is closest to substituting for precisely those workers whose "
     "comparative advantage was the codified, routine-cognitive work that constitutes "
     "the entry port of a professional career: first-draft writing, structured "
     "summarisation, basic coding, standard analysis. Occupational exposure measures "
     "confirm the concentration [[eloundou2024]],[[felten2021]], and the earliest "
     "high-frequency employment evidence is consistent with it. Using United States "
     "payroll microdata, Brynjolfsson, Chandar and Chen document a relative employment "
     "decline on the order of 13–16% for workers aged 22–25 in the most AI-exposed "
     "occupations after late 2022, with essentially no corresponding movement for "
     "experienced workers in the same occupations and firms, and with the adjustment "
     "operating through headcount rather than pay [[canaries2025]]. Other designs find "
     "much smaller aggregate effects over the same window [[humlum2025]], which is "
     "itself informative: the impact is not a technological constant but something "
     "that varies across organisational settings."),

    ("p",
     "The stakes are high because entry employment is not an ordinary margin of "
     "adjustment. Entering the labour market in a weak period depresses earnings for a "
     "decade or more and leaves durable marks on occupational attainment and health "
     "[[kahn2010]],[[schwandt2019]],[[vonwachter2020]]. Globally, youth unemployment "
     "and the share of young people not in employment, education or training remain "
     "the most stubborn features of the labour market [[ilo2024]], and employers "
     "themselves anticipate that AI will simultaneously displace and create work at "
     "unprecedented speed [[wef2025]]. Whether GenAI narrows or widens the first rung "
     "of the career ladder is therefore a first-order question for workforce "
     "development."),

    ("p",
     "Existing answers are dominated by two literatures that, taken separately, cannot "
     "settle it. The task-based framework in economics explains the tension between "
     "displacement and reinstatement effects and shows that the net employment "
     "consequence of automation depends on which of the two dominates "
     "[[acemoglu2018]],[[acemoglu2022]],[[autor2024]]. It is, however, largely silent "
     "on the organisational conditions that determine the balance, and it treats "
     "skill supply as exogenous to the firm. The management literature on human–AI "
     "collaboration, in turn, has established that automation and augmentation are "
     "interdependent rather than alternative design choices [[raisch2021]], that "
     "agency is conjoined rather than partitioned [[murray2021]], and that competitive "
     "advantage migrates towards the capabilities that complement the machine "
     "[[krakowski2023]]. It rarely models the intertemporal consequences of those "
     "choices for the stock of human capability that the firm will need later."),

    ("p",
     "What both perspectives under-weight is that the entry port performs two "
     "functions at once. It is a factor of production, and it is the intake stage of "
     "the firm's own capability pipeline. Junior work is where tacit judgement is "
     "acquired through legitimate peripheral participation in real tasks "
     "[[lave1991]],[[argote2011]]. When a technology absorbs that work, it removes not "
     "only a cost but also a curriculum. Ethnographic evidence from robotic surgery "
     "shows exactly this displacement of the learning opportunity, and the informal "
     "workarounds that trainees devise when the approved route to competence "
     "disappears [[beane2019]]; parallel findings concern the black-boxing of "
     "analytical technologies in knowledge work [[anthony2021]] and the reluctance of "
     "professionals to engage with opaque systems for critical judgements "
     "[[lebovitz2022]]. Because the resulting capability deficit appears only after "
     "the time required to develop a senior professional, it is invisible in the "
     "short-run accounting that drives the hiring decision. This is the structural "
     "signature of a capability trap [[repenning2002]],[[rahmandad2016]]."),

    ("p",
     "A problem with interdependent stocks, accumulation, delays and feedback is a "
     "systems problem, and we address it with the systems method that is designed for "
     "it. We formulate and analyse a socio-technical system dynamics model "
     "[[trist1951]],[[forrester1961]],[[sterman2000]] of a representative "
     "knowledge-intensive organisation, in which six stocks — early-career staff, "
     "experienced staff, GenAI capability, human–AI collaboration routines, planned "
     "output and perceived unit cost — interact through five explicit feedback loops. "
     "Displacement, task reinstatement, learning-by-collaborating, pipeline "
     "replenishment and competitive scale are all endogenous. The diffusion and "
     "augmentation parameters are calibrated to four independent published "
     "benchmarks, the model is subjected to the standard battery of validity tests "
     "[[forrester1980]],[[barlas1996]], and the analysis follows current reporting "
     "guidelines for simulation-based social science [[rahmandad2012]]."),

    ("p",
     "The paper makes three contributions. First, it reframes the effect of GenAI on "
     "youth employment as a property of loop dominance rather than of technology. We "
     "derive a closed-form net entry-port elasticity that decomposes the marginal "
     "effect of AI capability on entry labour demand into displacement, reinstatement "
     "and headcount-saving components, and we show that its sign is governed by two "
     "organisational design parameters — how far the firm pushes automation into entry "
     "tasks, and how far it reinstates higher-level work to AI-assisted juniors. Over "
     "the resulting design space the 25-year effect on entry employment ranges from "
     "−70.0% to +19.2%. Second, it identifies and quantifies the delayed feedback that "
     "makes an automation-first strategy self-defeating: thinning the entry port "
     "depletes the learning stock and the promotion flow, and because the sector's "
     "external market for experienced staff is itself fed by that promotion flow, the "
     "shortfall cannot be purchased back. Under an automation-first strategy the firm "
     "obtains the largest short-run unit-cost reduction of any scenario yet ends the "
     "horizon with output 15.7% below the no-GenAI counterfactual. Third, it supplies "
     "a direct numerical test of the joint-optimisation principle that has been "
     "asserted in socio-technical design since Trist and Bamforth [[trist1951]] and "
     "Cherns [[cherns1976]] but rarely quantified: in a pre-specified 2 × 2 factorial, "
     "changing the technical subsystem (work redesign) and the social subsystem "
     "(investment in collaboration routines) interact positively, with an interaction "
     "term of 2.74 percentage points on entry employment."),

    ("p",
     "The remainder of the paper is organised as follows. Section 2 develops the "
     "theoretical background and the feedback structure and states four propositions. "
     "Section 3 formulates the model, reports its parameterisation and calibration, "
     "and documents validation. Section 4 presents the baseline dynamics, the loop "
     "dominance analysis, the regime maps, the design experiments, the model-boundary "
     "comparison and the global sensitivity analysis. Section 5 discusses theoretical, "
     "managerial and policy implications and the limitations of the study. Section 6 "
     "concludes."),

    # =====================================================================
    ("h1", "2. Theoretical Background and Feedback Structure"),

    ("h2", "2.1. Generative AI and the Task Composition of Entry-Level Work"),

    ("p",
     "The task-based framework treats production as a continuum of tasks allocated "
     "between capital and labour. Automation reassigns tasks from labour to capital "
     "and reduces labour demand at given output, whereas reinstatement creates or "
     "reallocates tasks in which labour holds the comparative advantage; the net "
     "effect on employment is the difference between the two forces, augmented by the "
     "scale effect that follows from lower unit costs "
     "[[acemoglu2018]],[[acemoglu2022]],[[agrawal2019]]. Applied to GenAI, the "
     "framework has an "
     "unusual implication. Because the technology is a general-purpose technology "
     "whose complementary intangibles must be built inside organisations "
     "[[bresnahan1995]],[[jcurve2021]], both the automation frontier and the "
     "reinstatement frontier are partly endogenous to organisational choice rather "
     "than fixed by the artefact."),

    ("p",
     "Two empirical regularities discipline the way we represent this. The first is "
     "the concentration of exposure. Roughly 46% of occupations have at least half "
     "their tasks exposed once complementary software is accounted for "
     "[[eloundou2024]], and exposure is highest in the codified, verifiable, "
     "text-and-code tasks that firms conventionally allocate to new entrants "
     "[[felten2021]]. The second is experience compression. Across settings the "
     "measured productivity gain is largest for the least experienced and smallest, "
     "sometimes zero or negative, for the most experienced "
     "[[brynjolfsson2025]],[[noy2023]],[[peng2023]],[[otis2026]],[[cui2026]]; the "
     "meta-analytic evidence on human–AI combinations reaches the same conclusion, "
     "with gains concentrated where the human baseline is weak [[vaccaro2024]]."),

    ("p",
     "Experience compression cuts both ways, and this ambivalence is the substantive "
     "core of the paper. On the displacement side it raises the automatable share of "
     "entry tasks. On the reinstatement side it means that an AI-assisted junior can "
     "now perform work that previously required a senior, which expands rather than "
     "contracts the entry port. Whether the second channel is realised is not a "
     "property of the model weights. It requires the organisation to redesign the "
     "division of labour so that such work is actually delegated, and to possess the "
     "routines, review protocols and quality assurance that make the delegation safe "
     "[[raisch2021]],[[murray2021]],[[kellogg2020]]. We therefore represent the "
     "automation ceiling and the reinstatement ceiling as two distinct design "
     "parameters and let the realised reinstatement depend on an accumulated stock of "
     "collaboration routines."),

    ("h2", "2.2. The Entry Port as an Organisational Learning System"),

    ("p",
     "The second building block is that entry-level work produces skill as a joint "
     "product. Occupational competence is acquired through participation in "
     "consequential tasks under supervision, an argument that runs from situated "
     "learning theory [[lave1991]] through the experience-to-knowledge conversion "
     "literature in organisation science [[levitt1988]],[[march1991]],[[argote2011]],[[nonaka1994]], is embedded in "
     "the idea of the learning organisation [[senge1990]] "
     "and is grounded in the classic account of learning by doing [[arrow1962]]. "
     "Three implications follow for a system model."),

    ("p",
     "First, the promotion flow from junior to senior is not a free parameter: it is "
     "constrained by mentoring capacity, which is itself proportional to the senior "
     "stock. This creates a reinforcing loop in which a large senior stock sustains "
     "the development of its own successors and a depleted one cannot. Second, the "
     "learning content of junior work is not invariant to how that work is done. "
     "Ethnographic and survey evidence indicates that AI-mediated task performance "
     "builds less tacit skill per unit of time than unmediated performance unless the "
     "organisation deliberately designs for it — trainees are pushed to the periphery "
     "of the consequential work [[beane2019]], analytic assumptions are black-boxed "
     "[[anthony2021]], and dependence on the tool can produce deskilling as readily as "
     "upskilling [[yang2026]]. Third, the firm's ability to absorb the technology at "
     "all depends on prior related knowledge [[cohen1990]]; absorptive capacity is "
     "accumulated, not purchased, and it decays [[teece1997]],[[nelson1982]]."),

    ("p",
     "Taken together, these features imply that the entry port sits at the "
     "intersection of the firm's production system and its capability system. A "
     "decision that is locally efficient in the first can be destructive in the "
     "second, and because the second responds only after the time required to develop "
     "a senior professional, the destruction is not visible when the decision is "
     "taken. Analogous structures — where a locally rational reduction in an "
     "unmeasured investment erodes the capability that generated the performance in "
     "the first place — have been formalised as quality erosion in services "
     "[[oliva2001]], as capability traps in process improvement [[repenning2002]] and "
     "as capability erosion dynamics in strategy [[rahmandad2016]]. Our contribution "
     "is to identify the youth entry port as a site where the same structure operates, "
     "and to show that GenAI activates it."),

    ("h2", "2.3. A Socio-Technical Reading: Joint Optimisation and Loop Dominance"),

    ("p",
     "Socio-technical systems theory holds that the social and technical subsystems of "
     "an organisation are jointly responsible for performance, so that optimising "
     "either in isolation degrades the whole [[trist1951]],[[cherns1976]]. The "
     "principle has been carried into information systems as the sociotechnical axis "
     "of the discipline [[bostrom1977]],[[sarker2019]], and it is being restated for "
     "GenAI, which is increasingly analysed as a complex adaptive system of people, "
     "policies, data and processes rather than as a tool [[janssen2025]],[[dwivedi2023]]. "
     "In our setting the technical subsystem is the allocation of tasks between the "
     "model, the junior and the senior; the social subsystem is the set of routines, "
     "review practices and mentoring arrangements through which people and models work "
     "together. Joint optimisation predicts a positive interaction between changes in "
     "the two, which is a testable statement about a simulated system rather than a "
     "metaphor, and which we test directly in Section 4.4."),

    ("p",
     "Systems theory also supplies the analytical vocabulary for the central question, "
     "from the law of requisite variety [[ashby1956]] to the conditions a system must "
     "satisfy if it is to remain viable by reproducing its own capability over time "
     "[[beer1981]]. "
     "Whether the entry port widens or narrows is a question of loop dominance: which "
     "of the reinforcing and balancing structures shown in Figure 1 governs behaviour "
     "at a given time and in a given configuration [[sterman2000]],[[sterman2018]]. "
     "Because dominance can shift over time, and because the shift is driven by "
     "accumulations with different time constants, the sign of the effect can differ "
     "between the short and the long run — a possibility that reduced-form estimation "
     "over a three-year window cannot detect, and that complexity-theoretic accounts "
     "of organisation lead us to expect [[anderson1999]],[[meadows2008]]."),

    ("h2", "2.4. Feedback Structure and Propositions"),

    ("p",
     "Figure 1 summarises the causal structure. Five loops are relevant. Loop B1, "
     "entry-port displacement, is balancing: greater GenAI capability automates a "
     "larger share of entry tasks, which reduces the volume of entry work available to "
     "juniors and hence early-career employment, which in turn slows the accumulation "
     "of collaboration routines and therefore the firm's capacity to absorb further "
     "capability. Loop B2 is the classical productivity–headcount channel: higher "
     "junior effective productivity reduces the headcount required for a given task "
     "volume. Loop R1, task reinstatement, is reinforcing: collaboration routines "
     "allow core work to be delegated to AI-assisted juniors, which raises the entry "
     "task volume. Loop R2, the organisational learning engine, is the mechanism by "
     "which routines accumulate — learning by collaborating requires both the "
     "experimentation of juniors and the judgement of seniors, so it is strongest when "
     "the two stocks are balanced and collapses when either is depleted. Loop R3, the "
     "development pipeline, is reinforcing and slow: promotions replenish the senior "
     "stock, seniors provide the mentoring that makes promotion possible, and a "
     "thinning of either end of the pipeline is self-propagating. Loop R4 is the scale "
     "loop: lower unit cost raises demand and hence all task volumes "
     "[[acemoglu2018]],[[autor2015]]."),

    ("fig", "figure1"),

    ("p",
     "This structure yields four propositions, which the model in Section 3 makes "
     "precise and the experiments in Section 4 test."),

    ("prop", "Proposition 1.",
     "The sign of the long-run effect of GenAI on entry employment is not determined "
     "by the technology. It is determined by loop dominance, which in turn is set by "
     "the organisational parameters governing how far automation is pushed into entry "
     "tasks and how far higher-level work is reinstated to AI-assisted juniors."),

    ("prop", "Proposition 2.",
     "Because the reinstatement loop R1 is gated by an accumulated stock of "
     "collaboration routines while the displacement loop B1 is not, displacement "
     "dominates in the short run even in configurations in which reinstatement "
     "dominates in the long run. The trajectory of entry employment is therefore "
     "worse before better."),

    ("prop", "Proposition 3.",
     "Contraction of the entry port propagates, with a delay of the order of the time "
     "to competence, into the stock of experienced staff, into mentoring capacity and "
     "into the learning engine. An automation-first strategy that maximises short-run "
     "cost reduction is consequently a capability trap: it lowers long-run output "
     "relative to the counterfactual in which the technology is not adopted at all."),

    ("prop", "Proposition 4.",
     "Interventions in the technical subsystem (work redesign) and in the social "
     "subsystem (investment in collaboration routines) are complements. Their joint "
     "effect on entry employment exceeds the sum of their separate effects."),

    # =====================================================================
    ("h1", "3. Model Formulation"),

    ("h2", "3.1. Model Boundary, Aggregation and Assumptions"),

    ("p",
     "The model represents a representative knowledge-intensive organisation in a "
     "highly exposed sector over a 25-year horizon, with $t=0$ corresponding to the "
     "point at which a general-purpose GenAI frontier becomes available. Six state "
     "variables are endogenous: early-career staff $J$, experienced staff $S$, GenAI "
     "capability $A$, human–AI collaboration routines $K$, planned output $Y_d$ and "
     "perceived unit cost $\\hat{C}$. The external technological frontier, the "
     "autonomous growth of demand and relative wages are exogenous. Table 1 lists all "
     "variables and Figure 2 shows the stock-and-flow structure."),

    ("fig", "figure2"),

    ("p",
     "Three modelling choices deserve comment because they define the boundary. "
     "First, the workforce is aggregated into two competence classes rather than a "
     "continuous vintage structure. This is the minimum representation that supports "
     "a pipeline with a development delay, and it keeps the number of free parameters "
     "small enough for the sensitivity analysis to be informative "
     "[[rahmandad2012]],[[sterman2000]]. Second, the representative organisation is "
     "interpreted as the sector, so the external market for experienced staff is fed "
     "by the sector's own promotion flow. Buying experienced staff is therefore "
     "possible but bounded, and the bound tightens when the sector as a whole thins "
     "its entry port. We treat this sector-consistent closure as the default and "
     "report the partial-equilibrium closure, in which the external market is "
     "unaffected by the firm's own behaviour, as a comparison in Section 4.5. Third, "
     "the model is deterministic. Uncertainty is handled through global sensitivity "
     "analysis over the parameter space rather than through stochastic shocks, which "
     "is the appropriate treatment when the object of interest is structural "
     "behaviour rather than forecast intervals [[barlas1996]]."),

    ("table", "table1"),

    ("h2", "3.2. Stocks, Flows and Auxiliary Relationships"),

    ("p",
     "The external frontier follows a logistic path that represents the maturation of "
     "generally available model capability,"),

    ("eq", r"F(t)=\frac{F_{\text{max}}}{1+e^{-g_F(t-t_F)}}", 1),

    ("p",
     "and the firm closes the gap to that frontier at a rate that is gated by its own "
     "absorptive capacity, so that capability is accumulated rather than bought "
     "[[cohen1990]],[[jcurve2021]],"),

    ("eq", r"\frac{dA}{dt}=\nu\,\Lambda_A\,[F(t)-A]-\delta_A A,"
            r"\quad\quad \Lambda_A=\phi_0+(1-\phi_0)\Lambda", 2),

    ("p",
     "where $\\Lambda$ is the absorptive-capacity multiplier defined below and "
     "$\\phi_0$ is the floor that a firm with no routines still achieves. Utilisation "
     "intensity and the multiplier are increasing, saturating functions of the two "
     "capability stocks,"),

    ("eq", r"u=u_{\text{max}}\frac{A}{A+a_u},"
            r"\quad\quad \Lambda=\frac{K}{K+k_h}", 3),

    ("p",
     "The automated share of entry tasks rises with capability along a sigmoid whose "
     "ceiling $\\alpha_{\\text{max}}$ is the technical design parameter of the "
     "organisation, that is, how far it chooses and is able to push automation into "
     "the entry port,"),

    ("eq", r"\alpha=\alpha_{\text{max}}\frac{A^{\gamma}}"
            r"{A^{\gamma}+a_{\alpha}^{\gamma}}", 4),

    ("p",
     "The reinstatement share is the share of core tasks that the organisation "
     "delegates to AI-assisted juniors. It is bounded by a second design parameter "
     "$\\rho_{\\text{max}}$ and, crucially, is gated by both utilisation and routines, "
     "because delegation without collaboration routines is unsafe and is not "
     "sustained [[raisch2021]],[[lebovitz2022]],"),

    ("eq", r"\rho=\rho_{\text{max}}\,u\,\Lambda", 5),

    ("p",
     "Effective productivities embody experience compression through "
     "$\\beta_J>\\beta_S$,"),

    ("eq", r"\pi_J=\pi_{J0}(1+\beta_J u\Lambda),"
            r"\quad\quad \pi_S=\pi_{S0}(1+\beta_S u\Lambda)", 6),

    ("p",
     "Total task volume is normalised to unity and partitioned into entry tasks "
     "$\\theta_E$, core tasks $\\theta_C$ and judgement tasks $\\theta_G$. Task "
     "intensities per unit of output for the two labour classes are then"),

    ("eq", r"i_J=(1-\alpha)\theta_E+\rho\theta_C,"
            r"\quad\quad i_S=\theta_G+(1-\rho)\theta_C", 7),

    ("p",
     "so that desired labour, anchored on planned output, is"),

    ("eq", r"D_J=\frac{Y_d\,i_J}{\pi_J},\quad\quad D_S=\frac{Y_d\,i_S}{\pi_S}", 8),

    ("p",
     "Delivered output is limited by whichever class is short. The output fulfilment "
     "ratio $\\Phi$ and realised output are"),

    ("eq", r"\Phi=\min\left(1,\frac{\pi_J J}{Y_d i_J},\frac{\pi_S S}{Y_d i_S}\right),"
            r"\quad\quad Y=\Phi\,Y_d", 9),

    ("p",
     "Hiring follows the standard anchoring-and-adjustment formulation: the firm "
     "replaces separations and promotions and closes a fraction of the remaining gap "
     "each period [[sterman2000]],"),

    ("eq", r"h=\max\left(0,\frac{D_J-J}{\tau_J}+\delta_J J+c\right)", 10),

    ("p",
     "The development pipeline is where the socio-technical structure bites. Mentoring "
     "adequacy per junior combines human supervision, proportional to the senior "
     "stock, with AI-mediated scaffolding, and the fraction of juniors who reach "
     "competence is a saturating function of it,"),

    ("eq", r"q=\frac{m S}{J}+\eta A\Lambda,\quad\quad \psi=\frac{q}{q+q_0}", 11),

    ("p",
     "Skill formation also depends on what juniors actually do. Unmediated entry work "
     "is a full teacher; AI-mediated core work builds tacit skill only to the extent "
     "that the organisation has built the routines that make the mediation "
     "instructive [[beane2019]],[[anthony2021]],[[yang2026]]. We capture this with an "
     "experiential-quality index that equals one in the pre-GenAI state,"),

    ("eq", r"x=\frac{(1-\alpha)\theta_E+\rho\theta_C[\zeta_0+(1-\zeta_0)\Lambda]}"
            r"{i_J}", 12),

    ("p", "so that the promotion flow is"),

    ("eq", r"c=\psi\,x\,\frac{J}{\tau_{\text{dev}}}", 13),

    ("p",
     "Experienced staff can also be recruited externally, subject to a ceiling that "
     "is itself proportional to the sector's promotion flow relative to its "
     "replacement need. This is the formal expression of the sector-consistent "
     "closure: when every organisation thins its entry port, the external pool from "
     "which experienced staff are drawn contracts as well,"),

    ("eq", r"e_S=\min\left(\max\left(\frac{D_S-S}{\tau_S},0\right),"
            r"\chi_S S\,\Omega\right),\quad\quad "
            r"\Omega=\min\left[\left(\frac{c}{\delta_S S}\right)^{\omega},"
            r"\Omega_{\text{max}}\right]", 14),

    ("p", "The workforce stocks then evolve according to"),

    ("eq", r"\frac{dJ}{dt}=h-c-\delta_J J,"
            r"\quad\quad \frac{dS}{dt}=c+e_S-\delta_S S", 15),

    ("p",
     "Collaboration routines accumulate through learning by collaborating. The inflow "
     "is the geometric mean of the two workforce stocks scaled by utilisation, a "
     "specification that formalises the requirement that codified human–AI practice "
     "needs both the experimentation of newcomers and the judgement of incumbents "
     "[[nonaka1994]],[[argote2011]]; routines also depreciate rapidly, because model "
     "generations turn over,"),

    ("eq", r"\ell=\frac{2\lambda u\sqrt{J S}}{N_{\text{ref}}},"
            r"\quad\quad \frac{dK}{dt}=\ell-\delta_K K", 16),

    ("p",
     "Unit cost aggregates compensation, the operating cost of the technology and the "
     "cost of the learning investment,"),

    ("eq", r"C=\frac{w_J J+w_S S+p_A u Y+p_K \ell N_{\text{ref}}}{Y}", 17),

    ("p",
     "and planned output adjusts with a delay towards the level implied by autonomous "
     "growth and by competitiveness, with unit cost perceived through a first-order "
     "smooth,"),

    ("eq", r"\frac{dY_d}{dt}=\frac{1}{\tau_Y}\left[Y_0 e^{g_Y t}"
            r"\left(\frac{C_0}{\hat{C}}\right)^{\varepsilon}-Y_d\right],"
            r"\quad\quad \frac{d\hat{C}}{dt}=\frac{C-\hat{C}}{\tau_C}", 18),

    ("h2", "3.3. The Net Entry-Port Elasticity"),

    ("p",
     "Loop dominance can be read directly from the model. Differentiating desired "
     "junior labour in Equation (8) with respect to AI capability at constant planned "
     "output yields the net entry-port elasticity"),

    ("eq", r"E=\frac{\partial \ln D_J}{\partial \ln A}="
            r"\frac{\theta_C\frac{\partial\rho}{\partial\ln A}-"
            r"\theta_E\frac{\partial\alpha}{\partial\ln A}}{i_J}-"
            r"\frac{\partial\ln\pi_J}{\partial\ln A}", 19),

    ("p",
     "whose three components are the reinstatement force, the displacement force and "
     "the headcount-saving force. All three are available in closed form; in "
     "particular"),

    ("eq", r"\frac{\partial\alpha}{\partial\ln A}="
            r"\frac{\alpha_{\text{max}}\gamma A^{\gamma}a_{\alpha}^{\gamma}}"
            r"{(A^{\gamma}+a_{\alpha}^{\gamma})^{2}},\quad\quad "
            r"\frac{\partial\rho}{\partial\ln A}=\rho_{\text{max}}\Lambda "
            r"u_{\text{max}}\frac{a_u A}{(A+a_u)^{2}}", 20),

    ("p",
     "Equation (20) makes the central asymmetry explicit. The displacement force does "
     "not depend on the routine stock, whereas the reinstatement force is proportional "
     "to $\\Lambda$. A firm that adopts the technology without building routines "
     "therefore experiences the displacement force at full strength and the "
     "reinstatement force at a fraction of it, which is the analytical content of "
     "Proposition 2. $E>0$ indicates that the reinforcing loops R1 and R2 dominate "
     "and the entry port widens with capability; $E<0$ indicates dominance of B1 and "
     "B2."),

    ("h2", "3.4. Parameterisation and Calibration"),

    ("p",
     "Table 2 reports the full parameter set with sources. Structural parameters are "
     "taken from the literature or from accounting identities. The task shares follow "
     "the exposure literature, which places roughly one third of the task volume of "
     "highly exposed knowledge occupations in the codified, entry-level band "
     "[[eloundou2024]],[[felten2021]]. The time to competence, separation rates and "
     "relative productivities are conventional values for professional service work. "
     "The mentoring coefficient $m$ is not free: it is derived analytically as the "
     "value at which the workforce structure implied by task-based labour demand "
     "coincides with the structure implied by the promotion–separation balance, which "
     "places the model in an exact pre-GenAI steady state and eliminates initialisation "
     "drift as a source of spurious behaviour."),

    ("table", "table2"),

    ("p",
     "Four parameters that govern diffusion and augmentation — the frontier inflection "
     "$t_F$, the adoption rate $\\nu$, the utilisation half-saturation $a_u$ and the "
     "junior productivity elasticity $\\beta_J$, with $\\beta_S$ tied to $\\beta_J$ by "
     "the compression ratio of three reported in the field evidence — were estimated "
     "by nonlinear least squares against four independent published benchmarks. The "
     "targets and the fitted values are reported in Table 3. Because four parameters "
     "are fitted to four targets, the exercise is an exact calibration rather than a "
     "statistical test; its purpose is to place the simulated trajectory on the same "
     "quantitative scale as the observed one so that the counterfactual experiments "
     "are interpretable [[barlas1996]],[[rahmandad2012]]."),

    ("table", "table3"),

    ("h2", "3.5. Simulation Design and Model Validation"),

    ("p",
     "The system is integrated with a fourth-order Runge–Kutta scheme at a step of "
     "1/16 year over 25 years. Every reported outcome is expressed relative to a "
     "counterfactual run of the identical model with $F(t)\\equiv 0$, so that the "
     "autonomous growth of demand and the pre-existing workforce structure are "
     "differenced out. Model confidence was established through the standard sequence "
     "of tests for system dynamics models [[forrester1980]],[[barlas1996]], reported "
     "in Table 4: dimensional and structural consistency; an equilibrium test in which "
     "the model is run for a century with the technology and autonomous growth "
     "switched off; four extreme-condition tests that switch off learning investment, "
     "close the development pipeline entirely, remove displacement and remove "
     "reinstatement; an integration-error test in which the time step is halved twice; "
     "and behaviour reproduction against the calibration benchmarks. All tests pass."),

    ("table", "table4"),

    ("p",
     "Two of the extreme-condition tests are worth reading closely because they "
     "discriminate the structure rather than merely confirming the code. With the "
     "development pipeline closed the senior stock decays at exactly the separation "
     "rate, $S(25)/S(0)=0.1353$ against the analytical value "
     "$e^{-\\delta_S T}=0.1353$. With the automation ceiling set to zero, so that GenAI "
     "augments but never displaces, entry employment ends 3.7% above the counterfactual "
     "rather than below it — the model is capable of generating the complementarity "
     "regime and does not build the paper's conclusion into its structure."),

    # =====================================================================
    ("h1", "4. Results"),

    ("h2", "4.1. Baseline Dynamics: Displacement, Overshoot and Partial Recovery"),

    ("p",
     "Figure 3 and Table 5 report the calibrated baseline. GenAI capability reaches "
     "three quarters of its eventual level within five years and 94.5% of the external "
     "frontier by year 25, whereas the routine stock accumulates far more slowly: the absorptive-capacity multiplier "
     "$\\Lambda$ is still only 0.19 in year three and 0.53 in year 25. This is the "
     "quantitative expression of the asymmetry in Equation (20). By year three, "
     "automation has removed 25.7% of entry tasks while reinstatement has returned only "
     "3.8% of core tasks, and entry employment is 15.0% below the counterfactual."),

    ("fig", "figure3"),
    ("table", "table5"),

    ("p",
     "The trajectory then overshoots. Entry employment troughs at 37.2% below the "
     "counterfactual in year seven, and entry hiring — the flow rather than the stock — "
     "troughs at 56.1% below it in year three and a half, because the firm both stops replacing "
     "separations and absorbs the gap through attrition. Recovery is slow and "
     "incomplete: routines accumulate, reinstatement rises from 3.8% to 12.8% of core "
     "tasks and the scale loop adds demand, but entry employment is still 30.7% below "
     "the counterfactual after 25 years, and cumulative entry hiring over the horizon "
     "is 27.8% lower. The pattern is a worse-before-better trajectory of the kind "
     "familiar from the productivity J-curve for general-purpose technologies "
     "[[jcurve2021]], and it confirms Proposition 2."),

    ("p",
     "The delayed consequence appears in the other stocks. The experienced-staff stock "
     "peels away from the counterfactual only after year three, once the thinner junior "
     "cohorts begin to reach the promotion stage, and settles about 8% below it. The "
     "experiential-quality index falls to 0.91, so the juniors who are hired also learn "
     "more slowly per unit of time. Because promotions no longer cover senior "
     "separations, the sector-wide availability index $\\Omega$ falls below one and the "
     "external market cannot close the gap. The result is a persistent capability gap: "
     "the output fulfilment ratio $\\Phi$ declines from unity to 0.86, meaning that by "
     "the end of the horizon the organisation delivers 14% less than it plans to "
     "deliver, not because demand is missing but because the experienced staff required "
     "for judgement-intensive work are missing. Output nevertheless ends 9.4% above the "
     "counterfactual and unit cost 16.9% below it: the technology is profitable, and "
     "the capability gap is the price paid for it."),

    ("h2", "4.2. Loop Dominance and the Anatomy of the Entry-Port Elasticity"),

    ("p",
     "Figure 4a decomposes the net entry-port elasticity of Equation (19) into its "
     "three components. The displacement force peaks early, at the point of steepest "
     "growth in capability, and then decays as the automation sigmoid saturates. The "
     "headcount-saving force builds more slowly and stabilises. The reinstatement force "
     "is the slowest of the three because it is proportional to the routine stock, and "
     "it is still rising at the end of the horizon. The net elasticity is therefore "
     "sharply negative early — reaching −0.40 in year four — and recovers only to −0.27 "
     "by year 25. Loop dominance in the calibrated baseline never switches: B1 and B2 "
     "dominate throughout, and the partial recovery in Figure 3 is driven by the scale "
     "loop R4 rather than by a change in the sign of $E$."),

    ("fig", "figure4"),

    ("p",
     "Figure 4b shows that the elasticity path is a design variable. Under an "
     "automation-first strategy the net elasticity falls to −0.60 and remains at −0.48 "
     "after 25 years, whereas the joint socio-technical package lifts it to −0.20. The "
     "ordering of the five scenarios by elasticity in year 25 is identical to their ordering "
     "by entry employment, which confirms that Equation (19) is an adequate summary "
     "statistic for loop dominance in this model."),

    ("h2", "4.3. Regime Analysis: When Does Generative AI Widen the Entry Port?"),

    ("p",
     "Proposition 1 asserts that the sign of the effect is a property of organisational "
     "design rather than of the technology. Figure 5a maps the 25-year effect on entry "
     "employment over the two design parameters that define the technical division of "
     "labour, the automation ceiling $\\alpha_{\\text{max}}$ and the reinstatement "
     "ceiling $\\rho_{\\text{max}}$, holding every other parameter at its calibrated "
     "value. The effect ranges from −70.0% to +19.2%, and it is positive in 17.1% of "
     "the design space. The zero contour is close to linear, "
     "$\\alpha_{\\text{max}}=-0.335+1.207\\rho_{\\text{max}}$, which has a direct "
     "managerial reading: for every additional percentage point of the entry-task band "
     "that an organisation automates, it must reinstate roughly 0.83 percentage points "
     "of the core band to AI-assisted juniors in order to hold the entry port constant. The calibrated baseline lies well "
     "inside the displacement-dominant region."),

    ("fig", "figure5"),

    ("p",
     "Figure 5b repeats the exercise over the reinstatement ceiling and the "
     "learning-investment rate $\\lambda$, at the baseline automation ceiling. The "
     "contours are strongly convex rather than parallel, which is the visual signature "
     "of complementarity: increasing the reinstatement ceiling alone yields little when "
     "the routine stock is thin, because Equation (5) multiplies the ceiling by "
     "$\\Lambda$, and increasing learning investment alone yields little when the "
     "organisation does not delegate the work that the routines would support. The "
     "positive region is much smaller in this panel (2.5%) than in Figure 5a, which is "
     "the appropriate conclusion: at an automation ceiling of 0.60, no feasible "
     "combination of the two social-subsystem levers restores the entry port on its "
     "own."),

    ("h2", "4.4. Design Interventions and the Joint-Optimisation Test"),

    ("p",
     "Table 6 and Figure 6 report seven scenarios. Relative to the baseline S0, an "
     "automation-first intensification S1 — a higher automation ceiling combined with "
     "halved learning investment, which is the configuration a firm reaches if it "
     "treats GenAI as a cost-reduction programme — lowers unit cost faster than the "
     "baseline over the first three years, and by year 25 leaves "
     "entry employment 46.4% below the counterfactual, the experienced stock 23.9% "
     "below it, the fulfilment ratio at 0.695 and output 15.7% below the counterfactual "
     "in which the technology was never adopted. This is Proposition 3: the "
     "automation-first configuration is not merely bad for young workers, it is bad for "
     "the firm, and the damage is invisible in the first five years, when its output "
     "path is barely distinguishable from the baseline."),

    ("table", "table6"),
    ("fig", "figure6"),

    ("p",
     "The four constructive interventions differ in what they repair. Work redesign S3 "
     "acts directly on the entry port and delivers the largest single improvement in "
     "entry employment, 9.9 percentage points. Learning-system investment S2 acts on "
     "the gate and delivers 4.1 points on employment while lifting the fulfilment ratio "
     "from 0.864 to 0.948. Apprenticeship "
     "protection S4 and AI-mediated scaffolding S5 act on the pipeline: their effect on "
     "entry employment is small, 1.8 and 0.8 points, but S4 is the only single "
     "intervention that leaves the experienced stock above the counterfactual, and both "
     "raise output substantially by relieving the senior bottleneck. The joint package "
     "S6 halves the long-run entry-employment loss to 14.6%, cuts the cumulative "
     "shortfall in entry hiring from 27.8% to 9.2%, restores the experienced stock and "
     "raises the fulfilment ratio to 0.979 and output to 31.7% above the counterfactual."),

    ("p",
     "Proposition 4 requires a cleaner test than a comparison of packages, because the "
     "four interventions act partly on the same bottleneck. Table 7 therefore reports a "
     "pre-specified 2 × 2 factorial on the one technical lever and the one social lever "
     "that the theory identifies as jointly optimised: the reinstatement ceiling and "
     "the learning-investment rate. The main effect of work redesign is 11.29 "
     "percentage points, the main effect of learning investment is 5.50 points, and the "
     "interaction is +2.74 points, or 20% of the combined main effects. Joint "
     "optimisation is therefore not a slogan in this system: it is a measurable "
     "superadditivity that follows directly from the multiplicative form of "
     "Equation (5). For completeness we note that the four-lever decomposition "
     "underlying Table 6 is close to additive overall, with an interaction of −0.5 "
     "points, because the mentoring and scaffolding levers substitute for one another "
     "in relieving the same senior bottleneck. Complementarity holds between "
     "subsystems, not between every pair of instruments."),

    ("table", "table7"),

    ("h2", "4.5. Model Boundary: Why the Sector-Consistent Closure Matters"),

    ("p",
     "A firm considering these trade-offs in isolation would reason that experienced "
     "staff can be recruited if the internal pipeline underdelivers. Table 8 quantifies "
     "what that reasoning misses. Under the partial-equilibrium closure, in which the "
     "external market for experienced staff is unaffected by the sector's own "
     "behaviour, the baseline loss of experienced staff is 3.8% and output is 14.5% "
     "above the counterfactual. Under the sector-consistent closure the same "
     "configuration loses 7.9% of experienced staff and gains only 9.4% of output. The "
     "divergence widens sharply in the automation-first scenario: 16.6% against 23.9% "
     "for the experienced stock, and −7.4% against −15.7% for output. Partial "
     "equilibrium understates the long-run cost of entry-port erosion by roughly a "
     "factor of two, and it does so precisely in the configurations in which the cost "
     "matters most."),

    ("table", "table8"),

    ("p",
     "This is a composition fallacy of the classic kind [[meadows2008]],[[sterman2018]]. "
     "Each organisation can rationally treat the external market for experienced staff "
     "as a substitute for its own training pipeline; the sector cannot. The result also "
     "identifies where the boundary of a model of AI adoption has to be drawn: an "
     "analysis conducted at the level of the individual firm will systematically "
     "under-predict the capability consequences of a technology that every firm is "
     "adopting at the same time."),

    ("h2", "4.6. Global Sensitivity Analysis"),

    ("p",
     "Robustness was assessed by Latin hypercube sampling of 800 parameter vectors "
     "drawn from a ±30% interval around the calibrated values of fifteen parameters, "
     "with the mentoring coefficient re-derived in each draw so that every sampled "
     "configuration starts from its own exact pre-GenAI equilibrium. Table 9 reports "
     "partial rank correlation coefficients and Figure 7 displays them alongside the "
     "distribution of outcomes."),

    ("table", "table9"),
    ("fig", "figure7"),

    ("p",
     "Three conclusions follow. First, the baseline result is robust in magnitude: the "
     "median 25-year effect on entry employment is −30.6%, the interquartile range is "
     "[−37.6%, −24.0%] and the 5th–95th percentile range is [−45.9%, −15.5%]; no draw "
     "in the neighbourhood of the calibrated configuration produces a positive effect. "
     "The sign reversals documented in Section 4.3 require design choices well outside "
     "a ±30% perturbation, which is the correct interpretation of Proposition 1: they "
     "are strategic decisions, not parameter noise. Second, the ranking of drivers "
     "matches the theory. The automation ceiling dominates (PRCC −0.975), followed by "
     "the reinstatement ceiling (+0.896), the demand elasticity (+0.789) and the junior "
     "productivity elasticity (−0.787); the learning-investment rate and the routine "
     "obsolescence rate enter with the expected opposite signs (+0.513 and −0.488). "
     "Third, the pipeline parameters matter more for the capability outcome than for "
     "the employment outcome: the senior separation rate and the time to competence "
     "rank first and third for the experienced stock (−0.843 and −0.784) but only "
     "seventh and ninth for entry employment, and the experienced stock is below its "
     "counterfactual in 73.4% of draws. The employment effect and the capability effect "
     "are driven by partly different parts of the structure, which is why a policy "
     "designed for one of them will not automatically deliver the other."),

    # =====================================================================
    ("h1", "5. Discussion"),

    ("h2", "5.1. Theoretical Contributions"),

    ("p",
     "The study makes three theoretical contributions. First, it moves the question of "
     "GenAI and youth employment from the technology to the system. The task-based "
     "framework establishes that the net effect depends on the balance between "
     "displacement and reinstatement [[acemoglu2018]],[[acemoglu2022]]; what has been "
     "missing is a specification of what sets that balance. We show that in a "
     "socio-technical system it is set by two organisational design parameters and by "
     "an accumulated stock of collaboration routines that gates one force but not the "
     "other, and we derive a closed-form elasticity, Equation (19), that makes loop "
     "dominance observable. This connects the automation–augmentation paradox "
     "[[raisch2021]],[[krakowski2023]] to a dynamic, quantitative criterion rather than "
     "a typology."),

    ("p",
     "Second, it extends the capability-trap family of models "
     "[[oliva2001]],[[repenning2002]],[[rahmandad2016]] to workforce entry. The "
     "mechanism has the canonical structure — a locally rational reduction in an "
     "investment whose returns are delayed and unmeasured erodes the capability that "
     "produced the performance — but the eroding asset here is the intake stage of the "
     "firm's own skill pipeline, and the erosion operates through two channels rather "
     "than one: fewer juniors, and less learning per junior. The second channel "
     "formalises the shadow-learning and black-boxing findings of the qualitative "
     "literature [[beane2019]],[[anthony2021]] as a state variable, which allows their "
     "long-run consequences to be traced. Adding the sector-consistent closure shows "
     "that the trap is not escapable by recruitment, which is the escape route the "
     "existing firm-level models implicitly allow."),

    ("p",
     "Third, it supplies a quantitative test of joint optimisation. That the social and "
     "technical subsystems must be designed together is the founding claim of "
     "socio-technical theory [[trist1951]],[[cherns1976]],[[sarker2019]], but it is "
     "usually argued qualitatively. In our system the claim has a precise counterpart: "
     "because realised reinstatement is the product of a design ceiling and an "
     "absorptive-capacity multiplier, Equation (5), interventions in the two subsystems "
     "must interact positively, and they do, by 2.74 percentage points, or 20% of the "
     "sum of their main effects. Equally important is the negative result: the four-way "
     "decomposition is close to additive, because instruments acting on the same "
     "bottleneck substitute for one another. Complementarity in socio-technical design "
     "is a property of subsystems, not of instruments, and treating every combination "
     "of interventions as synergistic is a design error."),

    ("h2", "5.2. Managerial Implications"),

    ("p",
     "For organisations, the model changes the object of the decision. The relevant "
     "question is not how much of the entry-level work GenAI can do, but what "
     "proportion of core work the organisation is willing and able to move down to "
     "AI-assisted juniors, and whether it has built the routines that make that "
     "movement safe. The regime map in Figure 5a converts this into a planning rule: "
     "holding the entry port constant requires roughly 0.7 points of reinstatement for "
     "every point of automation. Firms that automate the entry band without a matching "
     "reinstatement programme are choosing the displacement-dominant regime, whether or "
     "not they intend to."),

    ("p",
     "Second, the fulfilment ratio $\\Phi$ is the metric that management systems "
     "currently lack. In the baseline it declines to 0.86 and in the automation-first "
     "scenario to 0.695, while unit cost improves throughout. A firm tracking cost per "
     "unit of output would record success in every year of the simulation; the "
     "capability gap appears only as an unexplained inability to staff "
     "judgement-intensive work, roughly a decade after the decision that caused it. "
     "Monitoring the ratio of promotion flow to senior separations, which is the "
     "internal analogue of $\\Omega$ in Equation (14), gives management a leading "
     "indicator of the same phenomenon."),

    ("p",
     "Third, the sequencing matters. The two interventions that operate through the "
     "learning stock, S2 and S4, are worse than the baseline on entry employment in "
     "year five (−35.2% and −34.4% against −33.0%) and clearly better by year 25 "
     "(−26.6% and −28.9% against −30.7%), because the stock has to accumulate before "
     "it can gate anything. Organisations "
     "that evaluate a reskilling or work-redesign programme on a three-year horizon "
     "will abandon it in the trough. This is the practical content of the "
     "worse-before-better dynamic [[jcurve2021]],[[repenning2002]] and it argues for "
     "explicitly protecting such programmes from short-horizon review."),

    ("h2", "5.3. Policy Implications"),

    ("p",
     "For policy, the sector-consistent closure result is the most consequential. "
     "Because the external market for experienced staff is fed by the same entry ports "
     "that firms are individually thinning, the depletion of mid-career capability is "
     "an externality: each organisation captures the full cost saving from automating "
     "its entry band and bears only its own share of the resulting scarcity. This is a "
     "standard justification for public intervention in training, and the model "
     "indicates where the intervention should bite. Instruments that subsidise the "
     "reinstatement of core work to supervised early-career staff — structured "
     "apprenticeship in professional services, graduate rotation schemes with protected "
     "task content, conditional hiring subsidies tied to task design rather than "
     "headcount — act on $\\rho_{\\text{max}}$, the parameter with the second-largest "
     "partial rank correlation in Table 9. Instruments that fund generic AI literacy "
     "act on $u$, which is already close to saturation in the baseline by year five."),

    ("p",
     "Second, the transition is long relative to the electoral and reporting cycle. "
     "Entry employment troughs in year seven and is still below the counterfactual "
     "after 25 years even in the joint package. Cohorts entering during the trough "
     "will carry the scarring documented in the youth labour market literature "
     "[[kahn2010]],[[schwandt2019]],[[vonwachter2020]] regardless of what happens "
     "afterwards, which is an argument for treating the entry port as a target of "
     "stabilisation policy in its own right rather than as a residual of aggregate "
     "labour demand [[ilo2024]]. Third, governance frameworks for GenAI are "
     "predominantly organised around risk, safety and accountability "
     "[[janssen2025]],[[xuejin2025]]. The model suggests adding a capability-continuity "
     "dimension: disclosure of entry-level hiring and internal promotion rates would "
     "make the erosion mechanism observable to regulators and investors at the point "
     "where intervention is still cheap, in the same way that disclosure has been used "
     "to make other slow-moving organisational risks visible [[xue2025]]."),

    ("h2", "5.4. Limitations and Future Research"),

    ("p",
     "Four limitations qualify the results. First, the model is calibrated rather than "
     "estimated. Four diffusion and augmentation parameters are fitted exactly to four "
     "published benchmarks, and the structural parameters are taken from the literature "
     "or derived from equilibrium conditions; the quantitative results should therefore "
     "be read as the behaviour of a disciplined structure, not as a forecast. The "
     "natural next step is estimation on firm-level panel data linking measured GenAI "
     "adoption to the age composition of hiring and to internal promotion rates, which "
     "would allow the elasticity in Equation (19) to be identified directly rather "
     "than derived."),

    ("p",
     "Second, the workforce is aggregated into two classes and the sector into a "
     "representative organisation. A vintage-structured workforce would permit the "
     "cohort-scarring channel to be modelled explicitly rather than inferred, and a "
     "multi-firm formulation would allow heterogeneous strategies to compete, which is "
     "where the composition fallacy of Section 4.5 would become a genuine "
     "coordination problem with free-riding on other firms' training. Third, the "
     "external frontier is exogenous and smooth. Discrete capability jumps, and the "
     "possibility that the automation ceiling itself is endogenous to how much "
     "codified practice the sector has published, are outside the boundary. Fourth, "
     "the model represents a highly exposed knowledge-intensive sector. Sectors in "
     "which the entry band is physical rather than cognitive will have different task "
     "shares and, plausibly, a different sign; extending the analysis across "
     "occupational groups using published exposure indices "
     "[[felten2021]],[[eloundou2024]] is a direct application of the same structure. "
     "Finally, the model treats the quality of AI-mediated skill formation through a "
     "single index $x$; the qualitative literature suggests this process is "
     "heterogeneous across professions and worth modelling in more detail "
     "[[beane2019]],[[lebovitz2022]],[[yang2026]]."),

    # =====================================================================
    ("h1", "6. Conclusions"),

    ("p",
     "Generative artificial intelligence is diffusing fastest through the tasks that "
     "have historically formed the first rung of the professional career ladder, and "
     "the earliest employment evidence shows that rung narrowing. This paper has argued "
     "that the narrowing is not a technological verdict but a system outcome, and it "
     "has built and validated a socio-technical system dynamics model to demonstrate "
     "the point. In the calibrated baseline, entry employment falls 15.0% within three "
     "years, troughs at 37.2% below the counterfactual in year seven and remains 30.7% "
     "below it after 25 years, while the thinning of the pipeline leaves the "
     "organisation delivering 14% less output than it plans. Yet across the design "
     "space the same technology produces effects ranging from −70.0% to +19.2%, and the "
     "boundary between the two regimes is drawn by two organisational parameters: how "
     "far automation is pushed into the entry band, and how far higher-level work is "
     "reinstated to AI-assisted juniors. Work redesign and investment in human–AI "
     "collaboration routines are complements, interacting positively by 2.74 percentage "
     "points, while an automation-first strategy is a capability trap that ends the "
     "horizon with output 15.7% below the level the organisation would have reached "
     "without the technology."),

    ("p",
     "The practical implication is that the entry port should be managed as "
     "infrastructure rather than as a cost line. It is the mechanism through which a "
     "sector reproduces the experienced judgement that its future depends on, and it is "
     "also, for a generation of young workers, the mechanism through which a career "
     "begins. Whether generative AI closes that mechanism or reopens it at a higher "
     "level of capability is being decided now, in decisions about task design, "
     "learning investment and apprenticeship that are made one organisation at a time "
     "and whose consequences arrive a decade later. The value of a systems approach is "
     "that it makes those consequences visible while the decisions are still open."),

    # =====================================================================
    ("h1b", "Author Contributions"),
    ("stmt", "",
     "Conceptualization, [A.B.]; methodology, [A.B.]; software, [A.B.]; validation, "
     "[A.B.]; formal analysis, [A.B.]; investigation, [A.B.]; writing—original draft "
     "preparation, [A.B.]; writing—review and editing, [A.B.]; visualization, [A.B.]. "
     "The author has read and agreed to the published version of the manuscript."),

    ("h1b", "Funding"),
    ("stmt", "", "This research received no external funding."),

    ("h1b", "Data Availability Statement"),
    ("stmt", "",
     "No new empirical data were created. The model source code, the calibration "
     "routine, the complete simulation output underlying every table and figure, and "
     "the scripts that regenerate them are available from the author on request."),

    ("h1b", "Conflicts of Interest"),
    ("stmt", "", "The author declares no conflicts of interest."),
]
