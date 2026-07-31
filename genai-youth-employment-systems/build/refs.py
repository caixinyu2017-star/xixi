# -*- coding: utf-8 -*-
"""Reference database, MDPI (Systems) style.

Every entry has been checked against the publisher record.  Reference numbers
are not stored here: the document builder assigns them in order of first
appearance in the text, as required by the journal.

kind: "article" | "book" | "chapter" | "report" | "preprint"
"""

REFS = {
    # ---- generative AI and work: field evidence ----------------------------
    "brynjolfsson2025": dict(
        kind="article",
        authors="Brynjolfsson, E.; Li, D.; Raymond, L.R.",
        title="Generative AI at Work",
        journal="Q. J. Econ.", year=2025, volume="140", pages="889–942",
        doi="10.1093/qje/qjae044"),
    "noy2023": dict(
        kind="article",
        authors="Noy, S.; Zhang, W.",
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
        authors="Cui, Z.K.; Demirer, M.; Jaffe, S.; Musolff, L.; Peng, S.; Salz, T.",
        title="The Effects of Generative AI on High-Skilled Work: Evidence from "
              "Three Field Experiments with Software Developers",
        journal="Manag. Sci.", year=2026, volume="", pages="in press",
        doi="10.1287/mnsc.2025.00535"),
    "otis2026": dict(
        kind="article",
        authors="Otis, N.G.; Clarke, R.; Delecourt, S.; Holtz, D.; Koning, R.",
        title="The Uneven Impact of Generative Artificial Intelligence on "
              "Entrepreneurial Performance: Evidence from a Field Experiment in Kenya",
        journal="Manag. Sci.", year=2026, volume="", pages="in press",
        doi="10.1287/mnsc.2024.06909"),
    "peng2023": dict(
        kind="preprint",
        authors="Peng, S.; Kalliamvakou, E.; Cihon, P.; Demirer, M.",
        title="The Impact of AI on Developer Productivity: Evidence from GitHub Copilot",
        journal="arXiv", year=2023, volume="", pages="arXiv:2302.06590",
        doi=""),
    "vaccaro2024": dict(
        kind="article",
        authors="Vaccaro, M.; Almaatouq, A.; Malone, T.",
        title="When Combinations of Humans and AI Are Useful: A Systematic Review "
              "and Meta-Analysis",
        journal="Nat. Hum. Behav.", year=2024, volume="8", pages="2293–2303",
        doi="10.1038/s41562-024-02024-1"),
    "humlum2025": dict(
        kind="report",
        authors="Humlum, A.; Vestergaard, E.",
        title="Large Language Models, Small Labor Market Effects",
        publisher="National Bureau of Economic Research", city="Cambridge, MA",
        country="USA", year=2025, series="NBER Working Paper 33777"),
    "canaries2025": dict(
        kind="report",
        authors="Brynjolfsson, E.; Chandar, B.; Chen, R.",
        title="Canaries in the Coal Mine? Six Facts about the Recent Employment "
              "Effects of Artificial Intelligence",
        publisher="Stanford Digital Economy Lab, Stanford University",
        city="Stanford, CA", country="USA", year=2025,
        series="Working Paper"),

    # ---- exposure, tasks and automation economics --------------------------
    "eloundou2024": dict(
        kind="article",
        authors="Eloundou, T.; Manning, S.; Mishkin, P.; Rock, D.",
        title="GPTs Are GPTs: Labor Market Impact Potential of LLMs",
        journal="Science", year=2024, volume="384", pages="1306–1308",
        doi="10.1126/science.adj0998"),
    "felten2021": dict(
        kind="article",
        authors="Felten, E.; Raj, M.; Seamans, R.",
        title="Occupational, Industry, and Geographic Exposure to Artificial "
              "Intelligence: A Novel Dataset and Its Potential Uses",
        journal="Strateg. Manag. J.", year=2021, volume="42", pages="2195–2217",
        doi="10.1002/smj.3286"),
    "acemoglu2018": dict(
        kind="article",
        authors="Acemoglu, D.; Restrepo, P.",
        title="The Race between Man and Machine: Implications of Technology for "
              "Growth, Factor Shares, and Employment",
        journal="Am. Econ. Rev.", year=2018, volume="108", pages="1488–1542",
        doi="10.1257/aer.20160696"),
    "acemoglu2022": dict(
        kind="article",
        authors="Acemoglu, D.; Restrepo, P.",
        title="Tasks, Automation, and the Rise in U.S. Wage Inequality",
        journal="Econometrica", year=2022, volume="90", pages="1973–2016",
        doi="10.3982/ECTA19815"),
    "autor2024": dict(
        kind="article",
        authors="Autor, D.; Chin, C.; Salomons, A.; Seegmiller, B.",
        title="New Frontiers: The Origins and Content of New Work, 1940–2018",
        journal="Q. J. Econ.", year=2024, volume="139", pages="1399–1465",
        doi="10.1093/qje/qjae008"),
    "autor2015": dict(
        kind="article",
        authors="Autor, D.H.",
        title="Why Are There Still So Many Jobs? The History and Future of "
              "Workplace Automation",
        journal="J. Econ. Perspect.", year=2015, volume="29", pages="3–30",
        doi="10.1257/jep.29.3.3"),
    "agrawal2019": dict(
        kind="article",
        authors="Agrawal, A.; Gans, J.S.; Goldfarb, A.",
        title="Artificial Intelligence: The Ambiguous Labor Market Impact of "
              "Automating Prediction",
        journal="J. Econ. Perspect.", year=2019, volume="33", pages="31–50",
        doi="10.1257/jep.33.2.31"),
    "bresnahan1995": dict(
        kind="article",
        authors="Bresnahan, T.F.; Trajtenberg, M.",
        title="General Purpose Technologies: “Engines of Growth”?",
        journal="J. Econom.", year=1995, volume="65", pages="83–108",
        doi="10.1016/0304-4076(94)01598-T"),
    "jcurve2021": dict(
        kind="article",
        authors="Brynjolfsson, E.; Rock, D.; Syverson, C.",
        title="The Productivity J-Curve: How Intangibles Complement General "
              "Purpose Technologies",
        journal="Am. Econ. J. Macroecon.", year=2021, volume="13", pages="333–372",
        doi="10.1257/mac.20180386"),
    "arrow1962": dict(
        kind="article",
        authors="Arrow, K.J.",
        title="The Economic Implications of Learning by Doing",
        journal="Rev. Econ. Stud.", year=1962, volume="29", pages="155–173",
        doi="10.2307/2295952"),

    # ---- youth labour markets ---------------------------------------------
    "vonwachter2020": dict(
        kind="article",
        authors="von Wachter, T.",
        title="The Persistent Effects of Initial Labor Market Conditions for "
              "Young Adults and Their Sources",
        journal="J. Econ. Perspect.", year=2020, volume="34", pages="168–194",
        doi="10.1257/jep.34.4.168"),
    "schwandt2019": dict(
        kind="article",
        authors="Schwandt, H.; von Wachter, T.",
        title="Unlucky Cohorts: Estimating the Long-Term Effects of Entering the "
              "Labor Market in a Recession in Large Cross-Sectional Data Sets",
        journal="J. Labor Econ.", year=2019, volume="37", pages="S161–S198",
        doi="10.1086/701046"),
    "kahn2010": dict(
        kind="article",
        authors="Kahn, L.B.",
        title="The Long-Term Labor Market Consequences of Graduating from College "
              "in a Bad Economy",
        journal="Labour Econ.", year=2010, volume="17", pages="303–316",
        doi="10.1016/j.labeco.2009.09.002"),
    "ilo2024": dict(
        kind="report",
        authors="International Labour Organization",
        title="Global Employment Trends for Youth 2024: Decent Work, Brighter Futures",
        publisher="International Labour Office", city="Geneva",
        country="Switzerland", year=2024, series=""),
    "wef2025": dict(
        kind="report",
        authors="World Economic Forum",
        title="The Future of Jobs Report 2025",
        publisher="World Economic Forum", city="Geneva", country="Switzerland",
        year=2025, series=""),

    # ---- organisational learning and skill formation -----------------------
    "cohen1990": dict(
        kind="article",
        authors="Cohen, W.M.; Levinthal, D.A.",
        title="Absorptive Capacity: A New Perspective on Learning and Innovation",
        journal="Adm. Sci. Q.", year=1990, volume="35", pages="128–152",
        doi="10.2307/2393553"),
    "march1991": dict(
        kind="article",
        authors="March, J.G.",
        title="Exploration and Exploitation in Organizational Learning",
        journal="Organ. Sci.", year=1991, volume="2", pages="71–87",
        doi="10.1287/orsc.2.1.71"),
    "levitt1988": dict(
        kind="article",
        authors="Levitt, B.; March, J.G.",
        title="Organizational Learning",
        journal="Annu. Rev. Sociol.", year=1988, volume="14", pages="319–340",
        doi="10.1146/annurev.so.14.080188.001535"),
    "argote2011": dict(
        kind="article",
        authors="Argote, L.; Miron-Spektor, E.",
        title="Organizational Learning: From Experience to Knowledge",
        journal="Organ. Sci.", year=2011, volume="22", pages="1123–1137",
        doi="10.1287/orsc.1100.0621"),
    "nonaka1994": dict(
        kind="article",
        authors="Nonaka, I.",
        title="A Dynamic Theory of Organizational Knowledge Creation",
        journal="Organ. Sci.", year=1994, volume="5", pages="14–37",
        doi="10.1287/orsc.5.1.14"),
    "lave1991": dict(
        kind="book",
        authors="Lave, J.; Wenger, E.",
        title="Situated Learning: Legitimate Peripheral Participation",
        publisher="Cambridge University Press", city="Cambridge", country="UK",
        year=1991),
    "nelson1982": dict(
        kind="book",
        authors="Nelson, R.R.; Winter, S.G.",
        title="An Evolutionary Theory of Economic Change",
        publisher="Belknap Press of Harvard University Press",
        city="Cambridge, MA", country="USA", year=1982),
    "teece1997": dict(
        kind="article",
        authors="Teece, D.J.; Pisano, G.; Shuen, A.",
        title="Dynamic Capabilities and Strategic Management",
        journal="Strateg. Manag. J.", year=1997, volume="18", pages="509–533",
        doi="10.1002/(SICI)1097-0266(199708)18:7<509::AID-SMJ882>3.0.CO;2-Z"),

    # ---- work, expertise and algorithmic technologies ----------------------
    "beane2019": dict(
        kind="article",
        authors="Beane, M.",
        title="Shadow Learning: Building Robotic Surgical Skill When Approved "
              "Means Fail",
        journal="Adm. Sci. Q.", year=2019, volume="64", pages="87–123",
        doi="10.1177/0001839217751692"),
    "anthony2021": dict(
        kind="article",
        authors="Anthony, C.",
        title="When Knowledge Work and Analytical Technologies Collide: The "
              "Practices and Consequences of Black Boxing Algorithmic Technologies",
        journal="Adm. Sci. Q.", year=2021, volume="66", pages="1173–1212",
        doi="10.1177/00018392211016755"),
    "lebovitz2022": dict(
        kind="article",
        authors="Lebovitz, S.; Lifshitz-Assaf, H.; Levina, N.",
        title="To Engage or Not to Engage with AI for Critical Judgments: How "
              "Professionals Deal with Opacity When Using AI for Medical Diagnosis",
        journal="Organ. Sci.", year=2022, volume="33", pages="126–148",
        doi="10.1287/orsc.2021.1549"),
    "kellogg2020": dict(
        kind="article",
        authors="Kellogg, K.C.; Valentine, M.A.; Christin, A.",
        title="Algorithms at Work: The New Contested Terrain of Control",
        journal="Acad. Manag. Ann.", year=2020, volume="14", pages="366–410",
        doi="10.5465/annals.2018.0174"),
    "raisch2021": dict(
        kind="article",
        authors="Raisch, S.; Krakowski, S.",
        title="Artificial Intelligence and Management: The Automation–Augmentation "
              "Paradox",
        journal="Acad. Manag. Rev.", year=2021, volume="46", pages="192–210",
        doi="10.5465/amr.2018.0072"),
    "krakowski2023": dict(
        kind="article",
        authors="Krakowski, S.; Luger, J.; Raisch, S.",
        title="Artificial Intelligence and the Changing Sources of Competitive "
              "Advantage",
        journal="Strateg. Manag. J.", year=2023, volume="44", pages="1425–1452",
        doi="10.1002/smj.3387"),
    "murray2021": dict(
        kind="article",
        authors="Murray, A.; Rhymer, J.; Sirmon, D.G.",
        title="Humans and Technology: Forms of Conjoined Agency in Organizations",
        journal="Acad. Manag. Rev.", year=2021, volume="46", pages="552–571",
        doi="10.5465/amr.2019.0186"),
    "yang2026": dict(
        kind="article",
        authors="Yang, B.; Sun, Y.; Zeng, Z.; Li, Q.",
        title="Deskilling, Reskilling, or Upskilling? Unpacking the Pathways of "
              "Student Adaptation to Generative Artificial Intelligence",
        journal="Int. J. Inf. Manag.", year=2026, volume="87", pages="103002",
        doi="10.1016/j.ijinfomgt.2025.103002"),
    "dwivedi2023": dict(
        kind="article",
        authors="Dwivedi, Y.K.; Kshetri, N.; Hughes, L.; Slade, E.L.; Jeyaraj, A.; "
                "Kar, A.K.; Baabdullah, A.M.; Koohang, A.; Raghavan, V.; Ahuja, M.; "
                "et al.",
        title="Opinion Paper: “So What If ChatGPT Wrote It?” Multidisciplinary "
              "Perspectives on Opportunities, Challenges and Implications of "
              "Generative Conversational AI for Research, Practice and Policy",
        journal="Int. J. Inf. Manag.", year=2023, volume="71", pages="102642",
        doi="10.1016/j.ijinfomgt.2023.102642"),

    # ---- socio-technical systems and systems science -----------------------
    "trist1951": dict(
        kind="article",
        authors="Trist, E.L.; Bamforth, K.W.",
        title="Some Social and Psychological Consequences of the Longwall Method "
              "of Coal-Getting",
        journal="Hum. Relat.", year=1951, volume="4", pages="3–38",
        doi="10.1177/001872675100400101"),
    "cherns1976": dict(
        kind="article",
        authors="Cherns, A.",
        title="The Principles of Sociotechnical Design",
        journal="Hum. Relat.", year=1976, volume="29", pages="783–792",
        doi="10.1177/001872677602900806"),
    "bostrom1977": dict(
        kind="article",
        authors="Bostrom, R.P.; Heinen, J.S.",
        title="MIS Problems and Failures: A Socio-Technical Perspective. Part I: "
              "The Causes",
        journal="MIS Q.", year=1977, volume="1", pages="17–32",
        doi="10.2307/248710"),
    "sarker2019": dict(
        kind="article",
        authors="Sarker, S.; Chatterjee, S.; Xiao, X.; Elbanna, A.",
        title="The Sociotechnical Axis of Cohesion for the IS Discipline: Its "
              "Historical Legacy and Its Continued Relevance",
        journal="MIS Q.", year=2019, volume="43", pages="695–719",
        doi="10.25300/MISQ/2019/13747"),
    "ashby1956": dict(
        kind="book",
        authors="Ashby, W.R.",
        title="An Introduction to Cybernetics",
        publisher="Chapman & Hall", city="London", country="UK", year=1956),
    "beer1981": dict(
        kind="book",
        authors="Beer, S.",
        title="Brain of the Firm",
        edition="2nd ed.",
        publisher="John Wiley & Sons", city="Chichester", country="UK", year=1981),
    "anderson1999": dict(
        kind="article",
        authors="Anderson, P.",
        title="Complexity Theory and Organization Science",
        journal="Organ. Sci.", year=1999, volume="10", pages="216–232",
        doi="10.1287/orsc.10.3.216"),
    "janssen2025": dict(
        kind="article",
        authors="Janssen, M.",
        title="Responsible Governance of Generative AI: Conceptualizing GenAI as "
              "Complex Adaptive Systems",
        journal="Policy Soc.", year=2025, volume="44", pages="38–51",
        doi="10.1093/polsoc/puae040"),

    # ---- system dynamics ---------------------------------------------------
    "forrester1961": dict(
        kind="book",
        authors="Forrester, J.W.",
        title="Industrial Dynamics",
        publisher="MIT Press", city="Cambridge, MA", country="USA", year=1961),
    "sterman2000": dict(
        kind="book",
        authors="Sterman, J.D.",
        title="Business Dynamics: Systems Thinking and Modeling for a Complex World",
        publisher="Irwin/McGraw-Hill", city="Boston, MA", country="USA", year=2000),
    "meadows2008": dict(
        kind="book",
        authors="Meadows, D.H.",
        title="Thinking in Systems: A Primer",
        publisher="Chelsea Green Publishing",
        city="White River Junction, VT", country="USA", year=2008),
    "senge1990": dict(
        kind="book",
        authors="Senge, P.M.",
        title="The Fifth Discipline: The Art and Practice of the Learning Organization",
        publisher="Doubleday", city="New York, NY", country="USA", year=1990),
    "forrester1980": dict(
        kind="article",
        authors="Forrester, J.W.; Senge, P.M.",
        title="Tests for Building Confidence in System Dynamics Models",
        journal="TIMS Stud. Manag. Sci.", year=1980, volume="14", pages="209–228",
        doi=""),
    "barlas1996": dict(
        kind="article",
        authors="Barlas, Y.",
        title="Formal Aspects of Model Validity and Validation in System Dynamics",
        journal="Syst. Dyn. Rev.", year=1996, volume="12", pages="183–210",
        doi="10.1002/(SICI)1099-1727(199623)12:3<183::AID-SDR103>3.0.CO;2-4"),
    "sterman2018": dict(
        kind="article",
        authors="Sterman, J.D.",
        title="System Dynamics at Sixty: The Path Forward",
        journal="Syst. Dyn. Rev.", year=2018, volume="34", pages="5–47",
        doi="10.1002/sdr.1601"),
    "rahmandad2012": dict(
        kind="article",
        authors="Rahmandad, H.; Sterman, J.D.",
        title="Reporting Guidelines for Simulation-Based Research in Social Sciences",
        journal="Syst. Dyn. Rev.", year=2012, volume="28", pages="396–411",
        doi="10.1002/sdr.1481"),
    "repenning2002": dict(
        kind="article",
        authors="Repenning, N.P.; Sterman, J.D.",
        title="Capability Traps and Self-Confirming Attribution Errors in the "
              "Dynamics of Process Improvement",
        journal="Adm. Sci. Q.", year=2002, volume="47", pages="265–295",
        doi="10.2307/3094806"),
    "rahmandad2016": dict(
        kind="article",
        authors="Rahmandad, H.; Repenning, N.",
        title="Capability Erosion Dynamics",
        journal="Strateg. Manag. J.", year=2016, volume="37", pages="649–672",
        doi="10.1002/smj.2354"),
    "oliva2001": dict(
        kind="article",
        authors="Oliva, R.; Sterman, J.D.",
        title="Cutting Corners and Working Overtime: Quality Erosion in the "
              "Service Industry",
        journal="Manag. Sci.", year=2001, volume="47", pages="894–914",
        doi="10.1287/mnsc.47.7.894.9807"),

    # ---- Systems (MDPI) ----------------------------------------------------
    "xuejin2025": dict(
        kind="article",
        authors="Xue, F.; Jin, S.",
        title="Artificial Intelligence Adoption, Innovation Efficiency, and "
              "Governance Mechanisms: Evidence from China",
        journal="Systems", year=2025, volume="13", pages="1062",
        doi="10.3390/systems13121062"),
    "xue2025": dict(
        kind="article",
        authors="Xue, X.; Li, L.; Chen, J.; Luo, T.",
        title="How Does Digital Technology Innovation Quality Empower Corporate "
              "ESG Performance? The Roles of Digital Transformation and Digital "
              "Technology Diffusion",
        journal="Systems", year=2025, volume="13", pages="929",
        doi="10.3390/systems13110929"),
}
