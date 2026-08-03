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
    "argote2011": dict(
        kind="article", authors="Argote, L.; Miron-Spektor, E.",
        title="Organizational Learning: From Experience to Knowledge",
        journal="Organ. Sci.", year=2011, volume="22", pages="1123–1137",
        doi="10.1287/orsc.1100.0621"),
    "beane2019": dict(
        kind="article", authors="Beane, M.",
        title="Shadow Learning: Building Robotic Surgical Skill When Approved "
              "Means Fail",
        journal="Adm. Sci. Q.", year=2019, volume="64", pages="87–123",
        doi="10.1177/0001839217751692"),
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
    "oster2019": dict(
        kind="article", authors="Oster, E.",
        title="Unobservable Selection and Coefficient Stability: Theory and "
              "Evidence",
        journal="J. Bus. Econ. Stat.", year=2019, volume="37", pages="187–204",
        doi="10.1080/07350015.2016.1227711"),
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
    # ---- production networks and the propagation of shocks -----------------
    # ---- spatial and network econometrics ----------------------------------
    "abadie2023": dict(
        kind="article",
        authors="Abadie, A.; Athey, S.; Imbens, G.W.; Wooldridge, J.M.",
        title="When Should You Adjust Standard Errors for Clustering?",
        journal="Q. J. Econ.", year=2023, volume="138", pages="1–35",
        doi="10.1093/qje/qjac038"),
    "cameron2008": dict(
        kind="article",
        authors="Cameron, A.C.; Gelbach, J.B.; Miller, D.L.",
        title="Bootstrap-Based Improvements for Inference with Clustered Errors",
        journal="Rev. Econ. Stat.", year=2008, volume="90", pages="414–427",
        doi="10.1162/rest.90.3.414"),
    "roodman2019": dict(
        kind="article",
        authors="Roodman, D.; Nielsen, M.Ø.; MacKinnon, J.G.; Webb, M.D.",
        title="Fast and Wild: Bootstrap Inference in Stata Using boottest",
        journal="Stata J.", year=2019, volume="19", pages="4–60",
        doi="10.1177/1536867X19830877"),
    "wooldridge2010": dict(
        kind="book", authors="Wooldridge, J.M.",
        title="Econometric Analysis of Cross Section and Panel Data, 2nd ed.",
        publisher="MIT Press", city="Cambridge", country="MA, USA", year=2010),

    # ---- local labour markets ----------------------------------------------
    "forsythe2022": dict(
        kind="article", authors="Forsythe, E.",
        title="Why Don't Firms Hire Young Workers during Recessions?",
        journal="Econ. J.", year=2022, volume="132", pages="1765–1789",
        doi="10.1093/ej/ueab096"),
    "oreopoulos2012": dict(
        kind="article",
        authors="Oreopoulos, P.; von Wachter, T.; Heisz, A.",
        title="The Short- and Long-Term Career Effects of Graduating in a "
              "Recession", journal="Am. Econ. J. Appl. Econ.", year=2012,
        volume="4", pages="1–29", doi="10.1257/app.4.1.1"),
    "liu2025": dict(
        kind="report", authors="Liu, Y.; Wang, H.; Yu, S.",
        title="Labor Demand in the Age of Generative AI: Early Evidence from "
              "the U.S. Job Posting Data",
        series="Policy Research Working Paper 11263", publisher="World Bank",
        city="Washington", country="DC, USA", year=2025),
    "young2022": dict(
        kind="article", authors="Young, A.",
        title="Consistency without Inference: Instrumental Variables in "
              "Practical Application",
        journal="Eur. Econ. Rev.", year=2022, volume="147", pages="104112",
        doi="10.1016/j.euroecorev.2022.104112"),

    # ---- systems theory, feedback and organisational dynamics --------------
    "forrester1961": dict(
        kind="book", authors="Forrester, J.W.", title="Industrial Dynamics",
        publisher="MIT Press", city="Cambridge, MA", country="USA", year=1961),
    "sterman2000": dict(
        kind="book", authors="Sterman, J.D.",
        title="Business Dynamics: Systems Thinking and Modeling for a Complex "
              "World",
        publisher="Irwin/McGraw-Hill", city="Boston, MA", country="USA",
        year=2000),
    "meadows2008": dict(
        kind="book", authors="Meadows, D.H.",
        title="Thinking in Systems: A Primer",
        publisher="Chelsea Green Publishing", city="White River Junction, VT",
        country="USA", year=2008),
    "senge1990": dict(
        kind="book", authors="Senge, P.M.",
        title="The Fifth Discipline: The Art and Practice of the Learning "
              "Organization",
        publisher="Doubleday", city="New York, NY", country="USA", year=1990),
    "repenning2002": dict(
        kind="article", authors="Repenning, N.P.; Sterman, J.D.",
        title="Capability Traps and Self-Confirming Attribution Errors in the "
              "Dynamics of Process Improvement",
        journal="Adm. Sci. Q.", year=2002, volume="47", pages="265–295",
        doi="10.2307/3094806"),
    "rahmandad2016": dict(
        kind="article", authors="Rahmandad, H.; Repenning, N.",
        title="Capability Erosion Dynamics",
        journal="Strateg. Manag. J.", year=2016, volume="37",
        pages="649–672", doi="10.1002/smj.2354"),
    "trist1951": dict(
        kind="article", authors="Trist, E.L.; Bamforth, K.W.",
        title="Some Social and Psychological Consequences of the Longwall "
              "Method of Coal-Getting",
        journal="Hum. Relat.", year=1951, volume="4", pages="3–38",
        doi="10.1177/001872675100400101"),
    "emery1965": dict(
        kind="article", authors="Emery, F.E.; Trist, E.L.",
        title="The Causal Texture of Organizational Environments",
        journal="Hum. Relat.", year=1965, volume="18", pages="21–32",
        doi="10.1177/001872676501800103"),
    "bertalanffy1968": dict(
        kind="book", authors="von Bertalanffy, L.",
        title="General System Theory: Foundations, Development, Applications",
        publisher="George Braziller", city="New York, NY", country="USA",
        year=1968),
    "checkland1981": dict(
        kind="book", authors="Checkland, P.",
        title="Systems Thinking, Systems Practice",
        publisher="Wiley", city="Chichester", country="UK", year=1981),
    "ashby1956": dict(
        kind="book", authors="Ashby, W.R.",
        title="An Introduction to Cybernetics",
        publisher="Chapman and Hall", city="London", country="UK", year=1956),
    "holland1995": dict(
        kind="book", authors="Holland, J.H.",
        title="Hidden Order: How Adaptation Builds Complexity",
        publisher="Addison-Wesley", city="Reading, MA", country="USA",
        year=1995),
    "levinthal1993": dict(
        kind="article", authors="Levinthal, D.A.; March, J.G.",
        title="The Myopia of Learning", journal="Strateg. Manag. J.",
        year=1993, volume="14", pages="95–112",
        doi="10.1002/smj.4250141009"),
    "nelson1982": dict(
        kind="book", authors="Nelson, R.R.; Winter, S.G.",
        title="An Evolutionary Theory of Economic Change",
        publisher="Harvard University Press", city="Cambridge, MA",
        country="USA", year=1982),
    "teece1997": dict(
        kind="article", authors="Teece, D.J.; Pisano, G.; Shuen, A.",
        title="Dynamic Capabilities and Strategic Management",
        journal="Strateg. Manag. J.", year=1997, volume="18",
        pages="509–533",
        doi="10.1002/(SICI)1097-0266(199708)18:7<509::AID-SMJ882>3.0.CO;2-Z"),
    "arrow1962": dict(
        kind="article", authors="Arrow, K.J.",
        title="The Economic Implications of Learning by Doing",
        journal="Rev. Econ. Stud.", year=1962, volume="29", pages="155–173",
        doi="10.2307/2295952"),

    # ---- human capital, training and internal labour markets ---------------
    "becker1964": dict(
        kind="book", authors="Becker, G.S.",
        title="Human Capital: A Theoretical and Empirical Analysis, with "
              "Special Reference to Education",
        publisher="National Bureau of Economic Research", city="New York, NY",
        country="USA", year=1964),
    "acemoglu1998": dict(
        kind="article", authors="Acemoglu, D.; Pischke, J.-S.",
        title="Why Do Firms Train? Theory and Evidence",
        journal="Q. J. Econ.", year=1998, volume="113", pages="79–119",
        doi="10.1162/003355398555531"),
    "acemoglu1999": dict(
        kind="article", authors="Acemoglu, D.; Pischke, J.-S.",
        title="Beyond Becker: Training in Imperfect Labour Markets",
        journal="Econ. J.", year=1999, volume="109", pages="F112–F142",
        doi="10.1111/1468-0297.00405"),
    "doeringer1971": dict(
        kind="book", authors="Doeringer, P.B.; Piore, M.J.",
        title="Internal Labor Markets and Manpower Analysis",
        publisher="D.C. Heath", city="Lexington, MA", country="USA",
        year=1971),
    "gibbons2004": dict(
        kind="article", authors="Gibbons, R.; Waldman, M.",
        title="Task-Specific Human Capital", journal="Am. Econ. Rev.",
        year=2004, volume="94", pages="203–207",
        doi="10.1257/0002828041301579"),
    "lazear2009": dict(
        kind="article", authors="Lazear, E.P.",
        title="Firm-Specific Human Capital: A Skill-Weights Approach",
        journal="J. Political Econ.", year=2009, volume="117",
        pages="914–940", doi="10.1086/648671"),
    "bloom2007": dict(
        kind="article", authors="Bloom, N.; Van Reenen, J.",
        title="Measuring and Explaining Management Practices across Firms and "
              "Countries",
        journal="Q. J. Econ.", year=2007, volume="122", pages="1351–1408",
        doi="10.1162/qjec.2007.122.4.1351"),

    # ---- dynamic panels, feedback estimation -------------------------------
    "nickell1981": dict(
        kind="article", authors="Nickell, S.",
        title="Biases in Dynamic Models with Fixed Effects",
        journal="Econometrica", year=1981, volume="49", pages="1417–1426",
        doi="10.2307/1911408"),
    "arellano1991": dict(
        kind="article", authors="Arellano, M.; Bond, S.",
        title="Some Tests of Specification for Panel Data: Monte Carlo "
              "Evidence and an Application to Employment Equations",
        journal="Rev. Econ. Stud.", year=1991, volume="58", pages="277–297",
        doi="10.2307/2297968"),
    "arellano1995": dict(
        kind="article", authors="Arellano, M.; Bover, O.",
        title="Another Look at the Instrumental Variable Estimation of "
              "Error-Components Models",
        journal="J. Econom.", year=1995, volume="68", pages="29–51",
        doi="10.1016/0304-4076(94)01642-D"),
    "blundell1998": dict(
        kind="article", authors="Blundell, R.; Bond, S.",
        title="Initial Conditions and Moment Restrictions in Dynamic Panel "
              "Data Models",
        journal="J. Econom.", year=1998, volume="87", pages="115–143",
        doi="10.1016/S0304-4076(98)00009-8"),
    "holtzeakin1988": dict(
        kind="article", authors="Holtz-Eakin, D.; Newey, W.; Rosen, H.S.",
        title="Estimating Vector Autoregressions with Panel Data",
        journal="Econometrica", year=1988, volume="56", pages="1371–1395",
        doi="10.2307/1913103"),
    "love2006": dict(
        kind="article", authors="Love, I.; Zicchino, L.",
        title="Financial Development and Dynamic Investment Behavior: "
              "Evidence from Panel VAR",
        journal="Q. Rev. Econ. Finance", year=2006, volume="46",
        pages="190–210", doi="10.1016/j.qref.2005.11.007"),
    "abrigo2016": dict(
        kind="article", authors="Abrigo, M.R.M.; Love, I.",
        title="Estimation of Panel Vector Autoregression in Stata",
        journal="Stata J.", year=2016, volume="16", pages="778–804",
        doi="10.1177/1536867X1601600314"),
    "chudik2018": dict(
        kind="article", authors="Chudik, A.; Pesaran, M.H.; Yang, J.-C.",
        title="Half-Panel Jackknife Fixed-Effects Estimation of Linear Models "
              "with Weakly Exogenous Regressors",
        journal="J. Appl. Econom.", year=2018, volume="33", pages="816–836",
        doi="10.1002/jae.2623"),
    "sims1980": dict(
        kind="article", authors="Sims, C.A.",
        title="Macroeconomics and Reality", journal="Econometrica",
        year=1980, volume="48", pages="1–48", doi="10.2307/1912017"),
    "baron1986": dict(
        kind="article", authors="Baron, R.M.; Kenny, D.A.",
        title="The Moderator-Mediator Variable Distinction in Social "
              "Psychological Research: Conceptual, Strategic, and Statistical "
              "Considerations",
        journal="J. Pers. Soc. Psychol.", year=1986, volume="51",
        pages="1173–1182", doi="10.1037/0022-3514.51.6.1173"),
    "preacher2008": dict(
        kind="article", authors="Preacher, K.J.; Hayes, A.F.",
        title="Asymptotic and Resampling Strategies for Assessing and "
              "Comparing Indirect Effects in Multiple Mediator Models",
        journal="Behav. Res. Methods", year=2008, volume="40",
        pages="879–891", doi="10.3758/BRM.40.3.879"),
    "zhao2010": dict(
        kind="article", authors="Zhao, X.; Lynch, J.G., Jr.; Chen, Q.",
        title="Reconsidering Baron and Kenny: Myths and Truths about "
              "Mediation Analysis",
        journal="J. Consum. Res.", year=2010, volume="37", pages="197–206",
        doi="10.1086/651257"),
    "rosenbaum1983": dict(
        kind="article", authors="Rosenbaum, P.R.; Rubin, D.B.",
        title="The Central Role of the Propensity Score in Observational "
              "Studies for Causal Effects",
        journal="Biometrika", year=1983, volume="70", pages="41–55",
        doi="10.1093/biomet/70.1.41"),
    "petersen2009": dict(
        kind="article", authors="Petersen, M.A.",
        title="Estimating Standard Errors in Finance Panel Data Sets: "
              "Comparing Approaches",
        journal="Rev. Financ. Stud.", year=2009, volume="22", pages="435–480",
        doi="10.1093/rfs/hhn053"),
    "aiken1991": dict(
        kind="book", authors="Aiken, L.S.; West, S.G.",
        title="Multiple Regression: Testing and Interpreting Interactions",
        publisher="Sage", city="Newbury Park, CA", country="USA", year=1991),

    # ---- the Chinese setting ----------------------------------------------
    "wu2021": dict(
        kind="article", authors="Wu, F.; Hu, H.; Lin, H.; Ren, X.",
        title="Enterprise Digital Transformation and Capital Market "
              "Performance: Empirical Evidence from Stock Liquidity",
        journal="J. Manag. World", year=2021, volume="37", pages="130–144",
        doi=""),
    "yuan2021": dict(
        kind="article", authors="Yuan, C.; Xiao, S.; Geng, C.; Sheng, Y.",
        title="Digital Transformation and Division of Labour between "
              "Enterprises: Vertical Specialisation or Vertical Integration",
        journal="China Ind. Econ.", year=2021, volume="9", pages="137–155",
        doi=""),
    "zhaoc2021": dict(
        kind="article", authors="Zhao, C.; Wang, W.; Li, X.",
        title="How Does Digital Transformation Affect the Total Factor "
              "Productivity of Enterprises?",
        journal="Financ. Trade Econ.", year=2021, volume="42",
        pages="114–129", doi=""),
    "ilo2025": dict(
        kind="report", authors="International Labour Organization",
        title="World Employment and Social Outlook: Trends 2025",
        publisher="International Labour Office", city="Geneva",
        country="Switzerland", year=2025),
    "nbs2025": dict(
        kind="web", authors="National Bureau of Statistics of China",
        title="Surveyed Urban Unemployment Rate of the Population Aged 16 to "
              "24 Excluding Students",
        url="https://www.stats.gov.cn/english/", year=2025,
        accessed="20 March 2026"),
    "moe2025": dict(
        kind="web", authors="Ministry of Education of the People's Republic "
                            "of China",
        title="The Number of College Graduates Nationwide Is Expected to "
              "Reach 12.22 Million in 2025",
        url="http://www.moe.gov.cn/", year=2025,
        accessed="20 March 2026"),
    "statecouncil2025": dict(
        kind="web", authors="State Council of the People's Republic of China",
        title="Opinions on Deepening the Implementation of the \u201cArtificial "
              "Intelligence Plus\u201d Initiative",
        url="https://www.gov.cn/", year=2025, accessed="20 March 2026"),
}
