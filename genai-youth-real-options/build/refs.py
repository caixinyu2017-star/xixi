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
    "argote2011": dict(
        kind="article", authors="Argote, L.; Miron-Spektor, E.",
        title="Organizational Learning: From Experience to Knowledge",
        journal="Organ. Sci.", year=2011, volume="22", pages="1123–1137",
        doi="10.1287/orsc.1100.0621"),
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

    # ---- irreversibility, uncertainty and the option value of waiting ------
    "dixit1994": dict(
        kind="book", authors="Dixit, A.K.; Pindyck, R.S.",
        title="Investment under Uncertainty", publisher="Princeton University "
              "Press", city="Princeton", country="NJ, USA", year=1994),
    "bernanke1983": dict(
        kind="article", authors="Bernanke, B.S.",
        title="Irreversibility, Uncertainty, and Cyclical Investment",
        journal="Q. J. Econ.", year=1983, volume="98", pages="85\u2013106",
        doi="10.2307/1885568"),
    "abel1996": dict(
        kind="article", authors="Abel, A.B.; Eberly, J.C.",
        title="Optimal Investment with Costly Reversibility",
        journal="Rev. Econ. Stud.", year=1996, volume="63", pages="581\u2013593",
        doi="10.2307/2297794"),
    "bloom2007": dict(
        kind="article", authors="Bloom, N.; Bond, S.; Van Reenen, J.",
        title="Uncertainty and Investment Dynamics",
        journal="Rev. Econ. Stud.", year=2007, volume="74", pages="391\u2013415",
        doi="10.1111/j.1467-937X.2007.00426.x"),
    "bloom2009": dict(
        kind="article", authors="Bloom, N.",
        title="The Impact of Uncertainty Shocks",
        journal="Econometrica", year=2009, volume="77", pages="623\u2013685",
        doi="10.3982/ECTA6248"),
    "bloom2014": dict(
        kind="article", authors="Bloom, N.",
        title="Fluctuations in Uncertainty",
        journal="J. Econ. Perspect.", year=2014, volume="28", pages="153\u2013176",
        doi="10.1257/jep.28.2.153"),
    "baker2016": dict(
        kind="article", authors="Baker, S.R.; Bloom, N.; Davis, S.J.",
        title="Measuring Economic Policy Uncertainty",
        journal="Q. J. Econ.", year=2016, volume="131", pages="1593\u20131636",
        doi="10.1093/qje/qjw024"),
    "gulen2016": dict(
        kind="article", authors="Gulen, H.; Ion, M.",
        title="Policy Uncertainty and Corporate Investment",
        journal="Rev. Financ. Stud.", year=2016, volume="29", pages="523\u2013564",
        doi="10.1093/rfs/hhv050"),
    "kim2017": dict(
        kind="article", authors="Kim, H.; Kung, H.",
        title="The Asset Redeployability Channel: How Uncertainty Affects "
              "Corporate Investment",
        journal="Rev. Financ. Stud.", year=2017, volume="30", pages="245\u2013280",
        doi="10.1093/rfs/hhv076"),
    "guiso1999": dict(
        kind="article", authors="Guiso, L.; Parigi, G.",
        title="Investment and Demand Uncertainty",
        journal="Q. J. Econ.", year=1999, volume="114", pages="185\u2013227",
        doi="10.1162/003355399555981"),
    "handley2017": dict(
        kind="article", authors="Handley, K.; Lim\u00e3o, N.",
        title="Policy Uncertainty, Trade, and Welfare: Theory and Evidence for "
              "China and the United States",
        journal="Am. Econ. Rev.", year=2017, volume="107", pages="2731\u20132783",
        doi="10.1257/aer.20141419"),
    "schaal2017": dict(
        kind="article", authors="Schaal, E.",
        title="Uncertainty and Unemployment",
        journal="Econometrica", year=2017, volume="85", pages="1675\u20131721",
        doi="10.3982/ECTA10557"),
    "leduc2016": dict(
        kind="article", authors="Leduc, S.; Liu, Z.",
        title="Uncertainty Shocks Are Aggregate Demand Shocks",
        journal="J. Monet. Econ.", year=2016, volume="82", pages="20\u201335",
        doi="10.1016/j.jmoneco.2016.07.002"),
    "hassan2019": dict(
        kind="article",
        authors="Hassan, T.A.; Hollander, S.; van Lent, L.; Tahoun, A.",
        title="Firm-Level Political Risk: Measurement and Effects",
        journal="Q. J. Econ.", year=2019, volume="134", pages="2135\u20132202",
        doi="10.1093/qje/qjz021"),
    "huang2020": dict(
        kind="article", authors="Huang, Y.; Luk, P.",
        title="Measuring Economic Policy Uncertainty in China",
        journal="China Econ. Rev.", year=2020, volume="59", pages="101367",
        doi="10.1016/j.chieco.2019.101367"),
    "loughran2016": dict(
        kind="article", authors="Loughran, T.; McDonald, B.",
        title="Textual Analysis in Accounting and Finance: A Survey",
        journal="J. Account. Res.", year=2016, volume="54", pages="1187\u20131230",
        doi="10.1111/1475-679X.12123"),

    # ---- labour adjustment costs, firm-specific skill and contingent work --
    "bentolila1990": dict(
        kind="article", authors="Bentolila, S.; Bertola, G.",
        title="Firing Costs and Labour Demand: How Bad Is Eurosclerosis?",
        journal="Rev. Econ. Stud.", year=1990, volume="57", pages="381\u2013402",
        doi="10.2307/2298020"),
    "hamermesh1996": dict(
        kind="article", authors="Hamermesh, D.S.; Pfann, G.A.",
        title="Adjustment Costs in Factor Demand",
        journal="J. Econ. Lit.", year=1996, volume="34", pages="1264\u20131292",
        doi=""),
    "pfann1993": dict(
        kind="article", authors="Pfann, G.A.; Palm, F.C.",
        title="Asymmetric Adjustment Costs in Non-Linear Labour Demand Models "
              "for the Netherlands and U.K. Manufacturing Sectors",
        journal="Rev. Econ. Stud.", year=1993, volume="60", pages="397\u2013412",
        doi="10.2307/2298063"),
    "becker1962": dict(
        kind="article", authors="Becker, G.S.",
        title="Investment in Human Capital: A Theoretical Analysis",
        journal="J. Political Econ.", year=1962, volume="70", pages="9\u201349",
        doi="10.1086/258724"),
    "acemoglu1998": dict(
        kind="article", authors="Acemoglu, D.; Pischke, J.-S.",
        title="Why Do Firms Train? Theory and Evidence",
        journal="Q. J. Econ.", year=1998, volume="113", pages="79\u2013119",
        doi="10.1162/003355398555531"),
    "lazear2009": dict(
        kind="article", authors="Lazear, E.P.",
        title="Firm-Specific Human Capital: A Skill-Weights Approach",
        journal="J. Political Econ.", year=2009, volume="117", pages="914\u2013940",
        doi="10.1086/648671"),
    "caggese2008": dict(
        kind="article", authors="Caggese, A.; Cu\u00f1at, V.",
        title="Financing Constraints and Fixed-Term Employment Contracts",
        journal="Econ. J.", year=2008, volume="118", pages="2013\u20132046",
        doi="10.1111/j.1468-0297.2008.02200.x"),
    "booth2002": dict(
        kind="article", authors="Booth, A.L.; Francesconi, M.; Frank, J.",
        title="Temporary Jobs: Stepping Stones or Dead Ends?",
        journal="Econ. J.", year=2002, volume="112", pages="F189\u2013F213",
        doi="10.1111/1468-0297.00043"),
    "autor2003jole": dict(
        kind="article", authors="Autor, D.H.",
        title="Outsourcing at Will: The Contribution of Unjust Dismissal "
              "Doctrine to the Growth of Employment Outsourcing",
        journal="J. Labor Econ.", year=2003, volume="21", pages="1\u201342",
        doi="10.1086/344122"),
    "autor2010": dict(
        kind="article", authors="Autor, D.H.; Houseman, S.N.",
        title="Do Temporary-Help Jobs Improve Labor Market Outcomes for "
              "Low-Skilled Workers? Evidence from \u201cWork First\u201d",
        journal="Am. Econ. J. Appl. Econ.", year=2010, volume="2", pages="96\u2013128",
        doi="10.1257/app.2.3.96"),
    "cahuc2016": dict(
        kind="article", authors="Cahuc, P.; Charlot, O.; Malherbet, F.",
        title="Explaining the Spread of Temporary Jobs and Its Impact on Labor "
              "Turnover", journal="Int. Econ. Rev.", year=2016, volume="57",
        pages="533\u2013572", doi="10.1111/iere.12167"),
    "katz2019": dict(
        kind="article", authors="Katz, L.F.; Krueger, A.B.",
        title="The Rise and Nature of Alternative Work Arrangements in the "
              "United States, 1995\u20132015",
        journal="ILR Rev.", year=2019, volume="72", pages="382\u2013416",
        doi="10.1177/0019793918820008"),
    "gallagher2015": dict(
        kind="article",
        authors="Gallagher, M.; Giles, J.; Park, A.; Wang, M.",
        title="China's 2008 Labor Contract Law: Implementation and Implications "
              "for China's Workers",
        journal="Hum. Relat.", year=2015, volume="68", pages="197\u2013235",
        doi="10.1177/0018726713509418"),
    "forsythe2022": dict(
        kind="article", authors="Forsythe, E.",
        title="Why Don't Firms Hire Young Workers during Recessions?",
        journal="Econ. J.", year=2022, volume="132", pages="1765\u20131789",
        doi="10.1093/ej/ueab096"),
    "oreopoulos2012": dict(
        kind="article",
        authors="Oreopoulos, P.; von Wachter, T.; Heisz, A.",
        title="The Short- and Long-Term Career Effects of Graduating in a "
              "Recession", journal="Am. Econ. J. Appl. Econ.", year=2012,
        volume="4", pages="1\u201329", doi="10.1257/app.4.1.1"),
    "moscarini2012": dict(
        kind="article", authors="Moscarini, G.; Postel-Vinay, F.",
        title="The Contribution of Large and Small Employers to Job Creation "
              "in Times of High and Low Unemployment",
        journal="Am. Econ. Rev.", year=2012, volume="102", pages="2509\u20132539",
        doi="10.1257/aer.102.6.2509"),

    # ---- estimation --------------------------------------------------------
    "silva2006": dict(
        kind="article", authors="Santos Silva, J.M.C.; Tenreyro, S.",
        title="The Log of Gravity", journal="Rev. Econ. Stat.", year=2006,
        volume="88", pages="641\u2013658", doi="10.1162/rest.88.4.641"),
    "correia2020": dict(
        kind="article", authors="Correia, S.; Guimar\u00e3es, P.; Zylkin, T.",
        title="Fast Poisson Estimation with High-Dimensional Fixed Effects",
        journal="Stata J.", year=2020, volume="20", pages="95\u2013115",
        doi="10.1177/1536867X20909691"),
    "cameron2008": dict(
        kind="article",
        authors="Cameron, A.C.; Gelbach, J.B.; Miller, D.L.",
        title="Bootstrap-Based Improvements for Inference with Clustered Errors",
        journal="Rev. Econ. Stat.", year=2008, volume="90", pages="414\u2013427",
        doi="10.1162/rest.90.3.414"),
    "roodman2019": dict(
        kind="article",
        authors="Roodman, D.; Nielsen, M.\u00d8.; MacKinnon, J.G.; Webb, M.D.",
        title="Fast and Wild: Bootstrap Inference in Stata Using boottest",
        journal="Stata J.", year=2019, volume="19", pages="4\u201360",
        doi="10.1177/1536867X19830877"),
    "abadie2023": dict(
        kind="article",
        authors="Abadie, A.; Athey, S.; Imbens, G.W.; Wooldridge, J.M.",
        title="When Should You Adjust Standard Errors for Clustering?",
        journal="Q. J. Econ.", year=2023, volume="138", pages="1\u201335",
        doi="10.1093/qje/qjac038"),
    "young2022": dict(
        kind="article", authors="Young, A.",
        title="Consistency without Inference: Instrumental Variables in "
              "Practical Application",
        journal="Eur. Econ. Rev.", year=2022, volume="147", pages="104112",
        doi="10.1016/j.euroecorev.2022.104112"),
    "wooldridge2010": dict(
        kind="book", authors="Wooldridge, J.M.",
        title="Econometric Analysis of Cross Section and Panel Data, 2nd ed.",
        publisher="MIT Press", city="Cambridge", country="MA, USA", year=2010),
    "liu2025": dict(
        kind="report", authors="Liu, Y.; Wang, H.; Yu, S.",
        title="Labor Demand in the Age of Generative AI: Early Evidence from "
              "the U.S. Job Posting Data",
        series="Policy Research Working Paper 11263", publisher="World Bank",
        city="Washington", country="DC, USA", year=2025),
}
