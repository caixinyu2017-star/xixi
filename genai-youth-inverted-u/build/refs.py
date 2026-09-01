# -*- coding: utf-8 -*-
"""Reference database in MDPI (Systems) style.

Reference numbers are assigned by the document builder in order of first
appearance in the text, as the journal requires.
kind: "article" | "book" | "chapter" | "report" | "preprint"
"""

REFS = {
    # ---- generative AI and work: field evidence ----------------------------
    "brynjolfsson2025": dict(
        kind="article", authors="Brynjolfsson, E.; Li, D.; Raymond, L.R.",
        title="Generative AI at Work", journal="Q. J. Econ.", year=2025,
        volume="140", pages="889–942", doi="10.1093/qje/qjae044"),
    "noy2023": dict(
        kind="article", authors="Noy, S.; Zhang, W.",
        title="Experimental Evidence on the Productivity Effects of Generative "
              "Artificial Intelligence",
        journal="Science", year=2023, volume="381", pages="187–192",
        doi="10.1126/science.adh2586"),
    "dellacqua2026": dict(
        kind="article",
        authors="Dell'Acqua, F.; McFowland, E., III; Mollick, E.R.; "
                "Lifshitz-Assaf, H.; Kellogg, K.C.; Rajendran, S.; Krayer, L.; "
                "Candelon, F.; Lakhani, K.R.",
        title="Navigating the Jagged Technological Frontier: Field Experimental "
              "Evidence of the Effects of Artificial Intelligence on Knowledge "
              "Worker Productivity and Quality",
        journal="Organ. Sci.", year=2026, volume="", pages="in press",
        doi="10.1287/orsc.2025.21838"),
    "cui2026": dict(
        kind="article",
        authors="Cui, Z.K.; Demirer, M.; Jaffe, S.; Musolff, L.; Peng, S.; "
                "Salz, T.",
        title="The Effects of Generative AI on High-Skilled Work: Evidence from "
              "Three Field Experiments with Software Developers",
        journal="Manag. Sci.", year=2026, volume="", pages="in press",
        doi="10.1287/mnsc.2025.00535"),
    "otis2026": dict(
        kind="article",
        authors="Otis, N.G.; Clarke, R.; Delecourt, S.; Holtz, D.; Koning, R.",
        title="The Uneven Impact of Generative Artificial Intelligence on "
              "Entrepreneurial Performance: Evidence from a Field Experiment in "
              "Kenya",
        journal="Manag. Sci.", year=2026, volume="", pages="in press",
        doi="10.1287/mnsc.2024.06909"),
    "peng2023": dict(
        kind="preprint",
        authors="Peng, S.; Kalliamvakou, E.; Cihon, P.; Demirer, M.",
        title="The Impact of AI on Developer Productivity: Evidence from GitHub "
              "Copilot",
        journal="arXiv", year=2023, volume="", pages="arXiv:2302.06590", doi=""),
    "vaccaro2024": dict(
        kind="article", authors="Vaccaro, M.; Almaatouq, A.; Malone, T.",
        title="When Combinations of Humans and AI Are Useful: A Systematic "
              "Review and Meta-Analysis",
        journal="Nat. Hum. Behav.", year=2024, volume="8", pages="2293–2303",
        doi="10.1038/s41562-024-02024-1"),
    "humlum2025": dict(
        kind="report", authors="Humlum, A.; Vestergaard, E.",
        title="Large Language Models, Small Labor Market Effects",
        publisher="National Bureau of Economic Research", city="Cambridge, MA",
        country="USA", year=2025, series="NBER Working Paper 33777"),
    "canaries2025": dict(
        kind="report", authors="Brynjolfsson, E.; Chandar, B.; Chen, R.",
        title="Canaries in the Coal Mine? Six Facts about the Recent Employment "
              "Effects of Artificial Intelligence",
        publisher="Stanford Digital Economy Lab, Stanford University",
        city="Stanford, CA", country="USA", year=2025, series="Working Paper"),

    "hui2024": dict(
        kind="article", authors="Hui, X.; Reshef, O.; Zhou, L.",
        title="The Short-Term Effects of Generative Artificial Intelligence on "
              "Employment: Evidence from an Online Labor Market",
        journal="Organ. Sci.", year=2024, volume="35", pages="1977–1989",
        doi="10.1287/orsc.2023.18441"),
    "bick2024": dict(
        kind="report", authors="Bick, A.; Blandin, A.; Deming, D.J.",
        title="The Rapid Adoption of Generative AI",
        publisher="National Bureau of Economic Research",
        city="Cambridge, MA", country="USA", year=2024,
        series="NBER Working Paper 32966"),
    "babina2024": dict(
        kind="article", authors="Babina, T.; Fedyk, A.; He, A.; Hodson, J.",
        title="Artificial Intelligence, Firm Growth, and Product Innovation",
        journal="J. Financ. Econ.", year=2024, volume="151", pages="103745",
        doi="10.1016/j.jfineco.2023.103745"),

    # ---- tasks, exposure and the economics of automation -------------------
    "eloundou2024": dict(
        kind="article",
        authors="Eloundou, T.; Manning, S.; Mishkin, P.; Rock, D.",
        title="GPTs Are GPTs: Labor Market Impact Potential of LLMs",
        journal="Science", year=2024, volume="384", pages="1306–1308",
        doi="10.1126/science.adj0998"),
    "felten2021": dict(
        kind="article", authors="Felten, E.; Raj, M.; Seamans, R.",
        title="Occupational, Industry, and Geographic Exposure to Artificial "
              "Intelligence: A Novel Dataset and Its Potential Uses",
        journal="Strateg. Manag. J.", year=2021, volume="42", pages="2195–2217",
        doi="10.1002/smj.3286"),
    "autor2003": dict(
        kind="article", authors="Autor, D.H.; Levy, F.; Murnane, R.J.",
        title="The Skill Content of Recent Technological Change: An Empirical "
              "Exploration",
        journal="Q. J. Econ.", year=2003, volume="118", pages="1279–1333",
        doi="10.1162/003355303322552801"),
    "acemoglu2018": dict(
        kind="article", authors="Acemoglu, D.; Restrepo, P.",
        title="The Race between Man and Machine: Implications of Technology for "
              "Growth, Factor Shares, and Employment",
        journal="Am. Econ. Rev.", year=2018, volume="108", pages="1488–1542",
        doi="10.1257/aer.20160696"),
    "acemoglu2022": dict(
        kind="article", authors="Acemoglu, D.; Restrepo, P.",
        title="Tasks, Automation, and the Rise in U.S. Wage Inequality",
        journal="Econometrica", year=2022, volume="90", pages="1973–2016",
        doi="10.3982/ECTA19815"),
    "acemoglu2020": dict(
        kind="article", authors="Acemoglu, D.; Restrepo, P.",
        title="Robots and Jobs: Evidence from US Labor Markets",
        journal="J. Political Econ.", year=2020, volume="128", pages="2188–2244",
        doi="10.1086/705716"),
    "autor2024": dict(
        kind="article",
        authors="Autor, D.; Chin, C.; Salomons, A.; Seegmiller, B.",
        title="New Frontiers: The Origins and Content of New Work, 1940–2018",
        journal="Q. J. Econ.", year=2024, volume="139", pages="1399–1465",
        doi="10.1093/qje/qjae008"),
    "autor2015": dict(
        kind="article", authors="Autor, D.H.",
        title="Why Are There Still So Many Jobs? The History and Future of "
              "Workplace Automation",
        journal="J. Econ. Perspect.", year=2015, volume="29", pages="3–30",
        doi="10.1257/jep.29.3.3"),
    "agrawal2019": dict(
        kind="article", authors="Agrawal, A.; Gans, J.S.; Goldfarb, A.",
        title="Artificial Intelligence: The Ambiguous Labor Market Impact of "
              "Automating Prediction",
        journal="J. Econ. Perspect.", year=2019, volume="33", pages="31–50",
        doi="10.1257/jep.33.2.31"),
    "bresnahan1995": dict(
        kind="article", authors="Bresnahan, T.F.; Trajtenberg, M.",
        title="General Purpose Technologies: “Engines of Growth”?",
        journal="J. Econom.", year=1995, volume="65", pages="83–108",
        doi="10.1016/0304-4076(94)01598-T"),
    "jcurve2021": dict(
        kind="article",
        authors="Brynjolfsson, E.; Rock, D.; Syverson, C.",
        title="The Productivity J-Curve: How Intangibles Complement General "
              "Purpose Technologies",
        journal="Am. Econ. J. Macroecon.", year=2021, volume="13",
        pages="333–372", doi="10.1257/mac.20180386"),

    "acemoglu2022jole": dict(
        kind="article",
        authors="Acemoglu, D.; Autor, D.; Hazell, J.; Restrepo, P.",
        title="Artificial Intelligence and Jobs: Evidence from Online Vacancies",
        journal="J. Labor Econ.", year=2022, volume="40", pages="S293–S340",
        doi="10.1086/718327"),
    "bonfiglioli2024": dict(
        kind="article",
        authors="Bonfiglioli, A.; Crinò, R.; Fadinger, H.; Gancia, G.",
        title="Robot Imports and Firm-Level Outcomes",
        journal="Econ. J.", year=2024, volume="134", pages="3428–3444",
        doi="10.1093/ej/ueae055"),
    "autorai2024": dict(
        kind="report", authors="Autor, D.",
        title="Applying AI to Rebuild Middle Class Jobs",
        publisher="National Bureau of Economic Research",
        city="Cambridge, MA", country="USA", year=2024,
        series="NBER Working Paper 32140"),
    "liang2025": dict(
        kind="article", authors="Liang, H.; Fan, J.; Wang, Y.",
        title="Artificial Intelligence, Technological Innovation, and "
              "Employment Transformation for Sustainable Development: "
              "Evidence from China",
        journal="Sustainability", year=2025, volume="17", pages="3842",
        doi="10.3390/su17093842"),
    "machucho2025": dict(
        kind="article", authors="Machucho, R.; Ortiz, D.",
        title="The Impacts of Artificial Intelligence on Business Innovation: "
              "A Comprehensive Review of Applications, Organizational "
              "Challenges, and Ethical Considerations",
        journal="Systems", year=2025, volume="13", pages="264",
        doi="10.3390/systems13040264"),

    # ---- youth labour markets ---------------------------------------------
    "kahn2010": dict(
        kind="article", authors="Kahn, L.B.",
        title="The Long-Term Labor Market Consequences of Graduating from "
              "College in a Bad Economy",
        journal="Labour Econ.", year=2010, volume="17", pages="303–316",
        doi="10.1016/j.labeco.2009.09.002"),
    "schwandt2019": dict(
        kind="article", authors="Schwandt, H.; von Wachter, T.",
        title="Unlucky Cohorts: Estimating the Long-Term Effects of Entering the "
              "Labor Market in a Recession in Large Cross-Sectional Data Sets",
        journal="J. Labor Econ.", year=2019, volume="37", pages="S161–S198",
        doi="10.1086/701046"),
    "vonwachter2020": dict(
        kind="article", authors="von Wachter, T.",
        title="The Persistent Effects of Initial Labor Market Conditions for "
              "Young Adults and Their Sources",
        journal="J. Econ. Perspect.", year=2020, volume="34", pages="168–194",
        doi="10.1257/jep.34.4.168"),
    "ilo2024": dict(
        kind="report", authors="International Labour Organization",
        title="Global Employment Trends for Youth 2024: Decent Work, Brighter "
              "Futures",
        publisher="International Labour Office", city="Geneva",
        country="Switzerland", year=2024, series=""),
    "wef2025": dict(
        kind="report", authors="World Economic Forum",
        title="The Future of Jobs Report 2025", publisher="World Economic Forum",
        city="Geneva", country="Switzerland", year=2025, series=""),

    # ---- organisational learning, skill formation and human-AI work --------
    "cohen1990": dict(
        kind="article", authors="Cohen, W.M.; Levinthal, D.A.",
        title="Absorptive Capacity: A New Perspective on Learning and Innovation",
        journal="Adm. Sci. Q.", year=1990, volume="35", pages="128–152",
        doi="10.2307/2393553"),
    "march1991": dict(
        kind="article", authors="March, J.G.",
        title="Exploration and Exploitation in Organizational Learning",
        journal="Organ. Sci.", year=1991, volume="2", pages="71–87",
        doi="10.1287/orsc.2.1.71"),
    "levitt1988": dict(
        kind="article", authors="Levitt, B.; March, J.G.",
        title="Organizational Learning", journal="Annu. Rev. Sociol.", year=1988,
        volume="14", pages="319–340", doi="10.1146/annurev.so.14.080188.001535"),
    "argote2011": dict(
        kind="article", authors="Argote, L.; Miron-Spektor, E.",
        title="Organizational Learning: From Experience to Knowledge",
        journal="Organ. Sci.", year=2011, volume="22", pages="1123–1137",
        doi="10.1287/orsc.1100.0621"),
    "nonaka1994": dict(
        kind="article", authors="Nonaka, I.",
        title="A Dynamic Theory of Organizational Knowledge Creation",
        journal="Organ. Sci.", year=1994, volume="5", pages="14–37",
        doi="10.1287/orsc.5.1.14"),
    "lave1991": dict(
        kind="book", authors="Lave, J.; Wenger, E.",
        title="Situated Learning: Legitimate Peripheral Participation",
        publisher="Cambridge University Press", city="Cambridge", country="UK",
        year=1991),
    "teece1997": dict(
        kind="article", authors="Teece, D.J.; Pisano, G.; Shuen, A.",
        title="Dynamic Capabilities and Strategic Management",
        journal="Strateg. Manag. J.", year=1997, volume="18", pages="509–533",
        doi="10.1002/(SICI)1097-0266(199708)18:7<509::AID-SMJ882>3.0.CO;2-Z"),
    "beane2019": dict(
        kind="article", authors="Beane, M.",
        title="Shadow Learning: Building Robotic Surgical Skill When Approved "
              "Means Fail",
        journal="Adm. Sci. Q.", year=2019, volume="64", pages="87–123",
        doi="10.1177/0001839217751692"),
    "anthony2021": dict(
        kind="article", authors="Anthony, C.",
        title="When Knowledge Work and Analytical Technologies Collide: The "
              "Practices and Consequences of Black Boxing Algorithmic "
              "Technologies",
        journal="Adm. Sci. Q.", year=2021, volume="66", pages="1173–1212",
        doi="10.1177/00018392211016755"),
    "lebovitz2022": dict(
        kind="article",
        authors="Lebovitz, S.; Lifshitz-Assaf, H.; Levina, N.",
        title="To Engage or Not to Engage with AI for Critical Judgments: How "
              "Professionals Deal with Opacity When Using AI for Medical "
              "Diagnosis",
        journal="Organ. Sci.", year=2022, volume="33", pages="126–148",
        doi="10.1287/orsc.2021.1549"),
    "kellogg2020": dict(
        kind="article",
        authors="Kellogg, K.C.; Valentine, M.A.; Christin, A.",
        title="Algorithms at Work: The New Contested Terrain of Control",
        journal="Acad. Manag. Ann.", year=2020, volume="14", pages="366–410",
        doi="10.5465/annals.2018.0174"),
    "raisch2021": dict(
        kind="article", authors="Raisch, S.; Krakowski, S.",
        title="Artificial Intelligence and Management: The "
              "Automation–Augmentation Paradox",
        journal="Acad. Manag. Rev.", year=2021, volume="46", pages="192–210",
        doi="10.5465/amr.2018.0072"),
    "krakowski2023": dict(
        kind="article", authors="Krakowski, S.; Luger, J.; Raisch, S.",
        title="Artificial Intelligence and the Changing Sources of Competitive "
              "Advantage",
        journal="Strateg. Manag. J.", year=2023, volume="44", pages="1425–1452",
        doi="10.1002/smj.3387"),
    "murray2021": dict(
        kind="article", authors="Murray, A.; Rhymer, J.; Sirmon, D.G.",
        title="Humans and Technology: Forms of Conjoined Agency in Organizations",
        journal="Acad. Manag. Rev.", year=2021, volume="46", pages="552–571",
        doi="10.5465/amr.2019.0186"),
    "yang2026": dict(
        kind="article", authors="Yang, B.; Sun, Y.; Zeng, Z.; Li, Q.",
        title="Deskilling, Reskilling, or Upskilling? Unpacking the Pathways of "
              "Student Adaptation to Generative Artificial Intelligence",
        journal="Int. J. Inf. Manag.", year=2026, volume="87", pages="103002",
        doi="10.1016/j.ijinfomgt.2025.103002"),
    "dwivedi2023": dict(
        kind="article",
        authors="Dwivedi, Y.K.; Kshetri, N.; Hughes, L.; Slade, E.L.; "
                "Jeyaraj, A.; Kar, A.K.; Baabdullah, A.M.; Koohang, A.; "
                "Raghavan, V.; Ahuja, M.; et al.",
        title="Opinion Paper: “So What If ChatGPT Wrote It?” Multidisciplinary "
              "Perspectives on Opportunities, Challenges and Implications of "
              "Generative Conversational AI for Research, Practice and Policy",
        journal="Int. J. Inf. Manag.", year=2023, volume="71", pages="102642",
        doi="10.1016/j.ijinfomgt.2023.102642"),

    # ---- socio-technical systems and AI governance -------------------------
    "trist1951": dict(
        kind="article", authors="Trist, E.L.; Bamforth, K.W.",
        title="Some Social and Psychological Consequences of the Longwall Method "
              "of Coal-Getting",
        journal="Hum. Relat.", year=1951, volume="4", pages="3–38",
        doi="10.1177/001872675100400101"),
    "cherns1976": dict(
        kind="article", authors="Cherns, A.",
        title="The Principles of Sociotechnical Design", journal="Hum. Relat.",
        year=1976, volume="29", pages="783–792",
        doi="10.1177/001872677602900806"),
    "sarker2019": dict(
        kind="article",
        authors="Sarker, S.; Chatterjee, S.; Xiao, X.; Elbanna, A.",
        title="The Sociotechnical Axis of Cohesion for the IS Discipline: Its "
              "Historical Legacy and Its Continued Relevance",
        journal="MIS Q.", year=2019, volume="43", pages="695–719",
        doi="10.25300/MISQ/2019/13747"),
    "janssen2025": dict(
        kind="article", authors="Janssen, M.",
        title="Responsible Governance of Generative AI: Conceptualizing GenAI as "
              "Complex Adaptive Systems",
        journal="Policy Soc.", year=2025, volume="44", pages="38–51",
        doi="10.1093/polsoc/puae040"),
    "xuejin2025": dict(
        kind="article", authors="Xue, F.; Jin, S.",
        title="Artificial Intelligence Adoption, Innovation Efficiency, and "
              "Governance Mechanisms: Evidence from China",
        journal="Systems", year=2025, volume="13", pages="1062",
        doi="10.3390/systems13121062"),
    "xue2025": dict(
        kind="article", authors="Xue, X.; Li, L.; Chen, J.; Luo, T.",
        title="How Does Digital Technology Innovation Quality Empower Corporate "
              "ESG Performance? The Roles of Digital Transformation and Digital "
              "Technology Diffusion",
        journal="Systems", year=2025, volume="13", pages="929",
        doi="10.3390/systems13110929"),

    # ---- curvilinear relationships -----------------------------------------
    "lindmehlum2010": dict(
        kind="article", authors="Lind, J.T.; Mehlum, H.",
        title="With or Without U? The Appropriate Test for a U-Shaped "
              "Relationship",
        journal="Oxf. Bull. Econ. Stat.", year=2010, volume="72",
        pages="109\u2013118", doi="10.1111/j.1468-0084.2009.00569.x"),
    "haans2016": dict(
        kind="article", authors="Haans, R.F.J.; Pieters, C.; He, Z.-L.",
        title="Thinking about U: Theorizing and Testing U- and Inverted "
              "U-Shaped Relationships in Strategy Research",
        journal="Strateg. Manag. J.", year=2016, volume="37",
        pages="1177\u20131195", doi="10.1002/smj.2399"),
    "simonsohn2018": dict(
        kind="article", authors="Simonsohn, U.",
        title="Two Lines: A Valid Alternative to the Invalid Testing of "
              "U-Shaped Relationships with Quadratic Regressions",
        journal="Adv. Methods Pract. Psychol. Sci.", year=2018, volume="1",
        pages="538\u2013555", doi="10.1177/2515245918805755"),

    # ---- econometric method ------------------------------------------------
    "oster2019": dict(
        kind="article", authors="Oster, E.",
        title="Unobservable Selection and Coefficient Stability: Theory and "
              "Evidence",
        journal="J. Bus. Econ. Stat.", year=2019, volume="37", pages="187–204",
        doi="10.1080/07350015.2016.1227711"),
    "hainmueller2012": dict(
        kind="article", authors="Hainmueller, J.",
        title="Entropy Balancing for Causal Effects: A Multivariate Reweighting "
              "Method to Produce Balanced Samples in Observational Studies",
        journal="Polit. Anal.", year=2012, volume="20", pages="25–46",
        doi="10.1093/pan/mpr025"),
    "rosenbaum1983": dict(
        kind="article", authors="Rosenbaum, P.R.; Rubin, D.B.",
        title="The Central Role of the Propensity Score in Observational Studies "
              "for Causal Effects",
        journal="Biometrika", year=1983, volume="70", pages="41–55",
        doi="10.1093/biomet/70.1.41"),
    "kleibergen2006": dict(
        kind="article", authors="Kleibergen, F.; Paap, R.",
        title="Generalized Reduced Rank Tests Using the Singular Value "
              "Decomposition",
        journal="J. Econom.", year=2006, volume="133", pages="97–126",
        doi="10.1016/j.jeconom.2005.02.011"),
    "stockyogo2005": dict(
        kind="chapter", authors="Stock, J.H.; Yogo, M.",
        title="Testing for Weak Instruments in Linear IV Regression",
        booktitle="Identification and Inference for Econometric Models: Essays "
                  "in Honor of Thomas Rothenberg",
        editors="Andrews, D.W.K., Stock, J.H., Eds.",
        publisher="Cambridge University Press", city="Cambridge", country="UK",
        year=2005, pages="pp. 80–108"),
    "bertrand2004": dict(
        kind="article",
        authors="Bertrand, M.; Duflo, E.; Mullainathan, S.",
        title="How Much Should We Trust Differences-in-Differences Estimates?",
        journal="Q. J. Econ.", year=2004, volume="119", pages="249–275",
        doi="10.1162/003355304772839588"),
    "goodmanbacon2021": dict(
        kind="article", authors="Goodman-Bacon, A.",
        title="Difference-in-Differences with Variation in Treatment Timing",
        journal="J. Econom.", year=2021, volume="225", pages="254–277",
        doi="10.1016/j.jeconom.2021.03.014"),
    "callaway2021": dict(
        kind="article", authors="Callaway, B.; Sant'Anna, P.H.C.",
        title="Difference-in-Differences with Multiple Time Periods",
        journal="J. Econom.", year=2021, volume="225", pages="200–230",
        doi="10.1016/j.jeconom.2020.12.001"),
    "sunabraham2021": dict(
        kind="article", authors="Sun, L.; Abraham, S.",
        title="Estimating Dynamic Treatment Effects in Event Studies with "
              "Heterogeneous Treatment Effects",
        journal="J. Econom.", year=2021, volume="225", pages="175–199",
        doi="10.1016/j.jeconom.2020.09.006"),
    "dechaisemartin2020": dict(
        kind="article",
        authors="de Chaisemartin, C.; D'Haultfœuille, X.",
        title="Two-Way Fixed Effects Estimators with Heterogeneous Treatment "
              "Effects",
        journal="Am. Econ. Rev.", year=2020, volume="110", pages="2964–2996",
        doi="10.1257/aer.20181169"),
    "goldsmith2020": dict(
        kind="article",
        authors="Goldsmith-Pinkham, P.; Sorkin, I.; Swift, H.",
        title="Bartik Instruments: What, When, Why, and How",
        journal="Am. Econ. Rev.", year=2020, volume="110", pages="2586–2624",
        doi="10.1257/aer.20181047"),
    "borusyak2022": dict(
        kind="article", authors="Borusyak, K.; Hull, P.; Jaravel, X.",
        title="Quasi-Experimental Shift-Share Research Designs",
        journal="Rev. Econ. Stud.", year=2022, volume="89", pages="181–213",
        doi="10.1093/restud/rdab030"),
}
