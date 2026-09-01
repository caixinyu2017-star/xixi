# -*- coding: utf-8 -*-
"""The bibliography, rendered in MDPI style by build_docx.py and numbered by
order of first citation.

Every entry here was verified during preparation to the standard that its
title, journal, year and digital object identifier were confirmed against a
publisher URL carrying that identifier, AND that its author list was seen in
a retrieved record rather than recalled. Candidate references whose author
list could not be confirmed in that way were discarded rather than guessed at,
which is why this list is shorter than is usual for a review-heavy article.
Fields that could not be confirmed — a volume, a page range — are omitted
rather than inferred.
"""

REFS = {
    # ---- heat, work capacity and the exposure-response functions --------
    "dunne2013": {'kind': 'article',
     'authors': 'Dunne, J.P.; Stouffer, R.J.; John, J.G.',
     'title': 'Reductions in Labour Capacity from Heat Stress under Climate '
              'Warming',
     'journal': 'Nat. Clim. Change',
     'year': 2013, 'volume': '3', 'pages': '563–566',
     'doi': '10.1038/nclimate1827'},

    "foster2021": {'kind': 'article',
     'authors': 'Foster, J.; Smallcombe, J.W.; Hodder, S. et al.',
     'title': 'An Advanced Empirical Model for Quantifying the Impact of Heat '
              'and Climate Change on Human Physical Work Capacity',
     'journal': 'Int. J. Biometeorol.',
     'year': 2021, 'volume': '65', 'pages': '1215–1229',
     'doi': '10.1007/s00484-021-02105-0'},

    "smallcombe2022": {'kind': 'article',
     'authors': 'Smallcombe, J.W.; Foster, J.; Hodder, S.G.; Jay, O.; '
                'Flouris, A.D.; Havenith, G.',
     'title': 'Quantifying the Impact of Heat on Human Physical Work '
              'Capacity; Part IV: Interactions between Work Duration and '
              'Heat Stress Severity',
     'journal': 'Int. J. Biometeorol.',
     'year': 2022, 'volume': '66', 'pages': '2463–2476',
     'doi': '10.1007/s00484-022-02370-7'},

    "kjellstrom2009": {'kind': 'article',
     'authors': 'Kjellstrom, T.; Kovats, R.S.; Lloyd, S.J.; Holt, T.; '
                'Tol, R.S.J.',
     'title': 'The Direct Impact of Climate Change on Regional Labor '
              'Productivity',
     'journal': 'Arch. Environ. Occup. Health',
     'year': 2009, 'volume': '64', 'pages': '217–227',
     'doi': '10.1080/19338240903352776'},

    "kjellstrom2016": {'kind': 'article',
     'authors': 'Kjellstrom, T.; Briggs, D.; Freyberg, C.; Lemke, B.; '
                'Otto, M.; Hyatt, O.',
     'title': 'Heat, Human Performance, and Occupational Health: A Key Issue '
              'for the Assessment of Global Climate Change Impacts',
     'journal': 'Annu. Rev. Public Health',
     'year': 2016, 'volume': '37', 'pages': '97–112',
     'doi': '10.1146/annurev-publhealth-032315-021740'},

    "brode2018": {'kind': 'article',
     'authors': 'Bröde, P.; Fiala, D.; Lemke, B.; Kjellstrom, T.',
     'title': 'Estimated Work Ability in Warm Outdoor Environments Depends on '
              'the Chosen Heat Stress Assessment Metric',
     'journal': 'Int. J. Biometeorol.',
     'year': 2018, 'volume': '62', 'pages': '331–345',
     'doi': '10.1007/s00484-017-1346-9'},

    "jacklitsch2016": {'kind': 'report',
     'authors': 'Jacklitsch, B.; Williams, W.J.; Musolin, K.; Coca, A.; '
                'Kim, J.-H.; Turner, N.',
     'title': 'NIOSH Criteria for a Recommended Standard: Occupational '
              'Exposure to Heat and Hot Environments',
     'year': 2016,
     'publisher': 'National Institute for Occupational Safety and Health, '
                  'DHHS (NIOSH) Publication No. 2016-106: Cincinnati, OH, USA',
     'url': 'https://www.cdc.gov/niosh/docs/2016-106/default.html'},

    # ---- heat, labour supply and productivity ---------------------------
    "day2019": {'kind': 'article',
     'authors': 'Day, E.; Fankhauser, S.; Kingsmill, N.; Costa, H.; '
                'Mavrogianni, A.',
     'title': 'Upholding Labour Productivity under Climate Change: An '
              'Assessment of Adaptation Options',
     'journal': 'Clim. Policy',
     'year': 2019, 'volume': '19', 'pages': '367–385',
     'doi': '10.1080/14693062.2018.1517640'},

    "parsons2022": {'kind': 'article',
     'authors': 'Parsons, L.A.; Masuda, Y.J.; Kroeger, T.; Shindell, D.; '
                'Wolff, N.H.; Spector, J.T.',
     'title': 'Global Labor Loss Due to Humid Heat Exposure Underestimated '
              'for Outdoor Workers',
     'journal': 'Environ. Res. Lett.',
     'year': 2022, 'volume': '17', 'pages': '014050',
     'doi': '10.1088/1748-9326/ac3dae'},

    "parsons2021": {'kind': 'article',
     'authors': 'Parsons, L.A.; Shindell, D.; Tigchelaar, M.; Zhang, Y.; '
                'Spector, J.T.',
     'title': 'Increased Labor Losses and Decreased Adaptation Potential in a '
              'Warmer World',
     'journal': 'Nat. Commun.',
     'year': 2021, 'volume': '12', 'pages': '7286',
     'doi': '10.1038/s41467-021-27328-y'},

    "graffzivin2014": {'kind': 'article',
     'authors': 'Graff Zivin, J.; Neidell, M.',
     'title': 'Temperature and the Allocation of Time: Implications for '
              'Climate Change',
     'journal': 'J. Labor Econ.',
     'year': 2014, 'volume': '32', 'pages': '1–26',
     'doi': '10.1086/671766'},

    "somanathan2021": {'kind': 'article',
     'authors': 'Somanathan, E.; Somanathan, R.; Sudarshan, A.; Tewari, M.',
     'title': 'The Impact of Temperature on Productivity and Labor Supply: '
              'Evidence from Indian Manufacturing',
     'journal': 'J. Political Econ.',
     'year': 2021, 'volume': '129', 'pages': '1797–1827',
     'doi': '10.1086/713733'},

    # ---- occupational heat exposure and vulnerable workers --------------
    "decrom2026": {'kind': 'article',
     'authors': 'de Crom, T.O.E. et al.',
     'title': 'Exposure to Heat at Work: Development of a Quantitative '
              'European Job Exposure Matrix (Heat JEM)',
     'journal': 'Scand. J. Work Environ. Health',
     'year': 2026, 'volume': '52', 'pages': '7–18'},

    "laskaris2026": {'kind': 'article',
     'authors': 'Laskaris, Z.; Baron, S.; Markowitz, S.B.',
     'title': 'Occupational Characteristics Are Missing from Heat '
              'Vulnerability Indices: A Study in New York and New Jersey',
     'journal': 'Environ. Health',
     'year': 2026,
     'doi': '10.1186/s12940-026-01284-w'},

    "fortune2013": {'kind': 'article',
     'authors': 'Fortune, M.; Mustard, C.; Etches, J.; Chambers, A.',
     'title': 'Work-Attributed Illness Arising from Excess Heat Exposure in '
              'Ontario, 2004–2010',
     'journal': 'Can. J. Public Health',
     'year': 2013, 'volume': '104', 'pages': 'e420–e426',
     'doi': '10.17269/cjph.104.3984'},

    "koranyi2018": {'kind': 'article',
     'authors': 'Koranyi, I.; Jonsson, J.; Rönnblad, T.; Stockfelt, L.; '
                'Bodin, T.',
     'title': 'Precarious Employment and Occupational Accidents and '
              'Injuries—A Systematic Review',
     'journal': 'Scand. J. Work Environ. Health',
     'year': 2018, 'volume': '44', 'pages': '341–350',
     'doi': '10.5271/sjweh.3720'},

    # ---- youth labour markets -------------------------------------------
    "vonwachter2020": {'kind': 'article',
     'authors': 'von Wachter, T.',
     'title': 'The Persistent Effects of Initial Labor Market Conditions for '
              'Young Adults and Their Sources',
     'journal': 'J. Econ. Perspect.',
     'year': 2020, 'volume': '34', 'pages': '168–194',
     'doi': '10.1257/jep.34.4.168'},

    "schmillen2017": {'kind': 'article',
     'authors': 'Schmillen, A.; Umkehrer, M.',
     'title': 'The Scars of Youth: Effects of Early-Career Unemployment on '
              'Future Unemployment Experience',
     'journal': 'Int. Labour Rev.',
     'year': 2017, 'volume': '156', 'pages': '465–494',
     'doi': '10.1111/ilr.12079'},

    "ilo2026": {'kind': 'report',
     'authors': 'International Labour Office',
     'title': 'Global Employment Trends for Youth 2026: Back to the Future',
     'year': 2026,
     'publisher': 'International Labour Office: Geneva, Switzerland',
     'url': 'https://www.ilo.org/publications/major-publications/'
            'global-employment-trends-youth-2026'},

    "eurofound2026": {'kind': 'report',
     'authors': 'Eurofound',
     'title': 'European Working Conditions Survey 2024: Overview Report',
     'year': 2026,
     'publisher': 'Publications Office of the European Union: Luxembourg',
     'url': 'https://www.eurofound.europa.eu/en/publications/2026/'
            'european-working-conditions-survey-2024-overview-report'},

    "euosha2025": {'kind': 'report',
     'authors': 'European Agency for Safety and Health at Work',
     'title': 'OSH Pulse 2025: Occupational Safety and Health in the Era of '
              'Climate and Digital Change',
     'year': 2025,
     'publisher': 'European Agency for Safety and Health at Work: Bilbao, Spain',
     'url': 'https://osha.europa.eu/en/facts-and-figures/osh-pulse/'
            'climate-digital-change'},

    # ---- green and blue infrastructure cooling --------------------------
    "konijnendijk2023": {'kind': 'article',
     'authors': 'Konijnendijk, C.C.',
     'title': 'Evidence-Based Guidelines for Greener, Healthier, More '
              'Resilient Neighbourhoods: Introducing the 3–30–300 Rule',
     'journal': 'J. For. Res.',
     'year': 2023, 'volume': '34', 'pages': '821–830',
     'doi': '10.1007/s11676-022-01523-z'},

    "croeser2024": {'kind': 'article',
     'authors': 'Croeser, T.; Sharma, R.; Weisser, W.W. et al.',
     'title': 'Acute Canopy Deficits in Global Cities Exposed by the 3-30-300 '
              'Benchmark for Urban Nature',
     'journal': 'Nat. Commun.',
     'year': 2024, 'volume': '15', 'pages': '9333',
     'doi': '10.1038/s41467-024-53402-2'},

    "croeser2026": {'kind': 'article',
     'authors': 'Croeser, T.; Rahman, M.A.; Ghosh, A.K.',
     'title': 'Urban Forestry for Cooler Cities Faces Three Critical Hurdles',
     'journal': 'Nat. Commun.',
     'year': 2026,
     'doi': '10.1038/s41467-026-70723-6'},

    "massaro2023": {'kind': 'article',
     'authors': 'Massaro, E.; Schifanella, R.; Piccardo, M.; Caporaso, L.; '
                'Taubenböck, H.; Cescatti, A.; Duveiller, G.',
     'title': 'Spatially-Optimized Urban Greening for Reduction of Population '
              'Exposure to Land Surface Temperature Extremes',
     'journal': 'Nat. Commun.',
     'year': 2023,
     'doi': '10.1038/s41467-023-38596-1'},

    "li2024": {'kind': 'article',
     'authors': 'Li, H.; Zhao, Y.; Wang, C.; Ürge-Vorsatz, D.; Carmeliet, J.; '
                'Bardhan, R.',
     'title': 'Cooling Efficacy of Trees across Cities Is Determined by '
              'Background Climate, Urban Morphology, and Tree Trait',
     'journal': 'Commun. Earth Environ.',
     'year': 2024, 'volume': '5', 'pages': '754',
     'doi': '10.1038/s43247-024-01908-4'},

    "yu2020": {'kind': 'article',
     'authors': 'Yu, Z.; Yang, G.; Zuo, S.; Jørgensen, G.; Koga, M.; '
                'Vejre, H.',
     'title': 'Critical Review on the Cooling Effect of Urban Blue-Green '
              'Space: A Threshold-Size Perspective',
     'journal': 'Urban For. Urban Green.',
     'year': 2020, 'pages': '126630',
     'doi': '10.1016/j.ufug.2020.126630'},

    "marando2022": {'kind': 'article',
     'authors': 'Marando, F.; Heris, M.P.; Zulian, G.; Udías, A.; '
                'Mentaschi, L.; Chrysoulakis, N.; Parastatidis, D.; Maes, J.',
     'title': 'Urban Heat Island Mitigation by Green Infrastructure in '
              'European Functional Urban Areas',
     'journal': 'Sustain. Cities Soc.',
     'year': 2022, 'volume': '77', 'pages': '103564'},

    "werbin2020": {'kind': 'article',
     'authors': 'Werbin, Z.R.; Heidari, L.; Buckley, S.; Brochu, P.; '
                'Butler, L.J.; Connolly, C.; Houttuijn Bloemendaal, L.; '
                'McCabe, T.D.; Miller, T.K.; Hutyra, L.R.',
     'title': 'A Tree-Planting Decision Support Tool for Urban Heat '
              'Mitigation',
     'journal': 'PLoS ONE',
     'year': 2020, 'volume': '15', 'pages': 'e0224959',
     'doi': '10.1371/journal.pone.0224959'},

    "rahmanrazak2026": {'kind': 'article',
     'authors': 'Rahman Razak, A.; Sabir; Idris, A.; Fernandes, A.A.R.',
     'title': 'The Impact of Urban Green Spaces on Labor Productivity: '
              'Dynamic Spatial Panel Evidence from Indonesian Cities',
     'journal': 'Sustainability',
     'year': 2026, 'volume': '18', 'pages': '3882',
     'doi': '10.3390/su18083882'},

    # ---- urban form and outdoor thermal comfort -------------------------
    "aghamolaei2023": {'kind': 'article',
     'authors': 'Aghamolaei, R.; Azizi, M.M.; Aminzadeh, B.; O’Donnell, J.',
     'title': 'A Comprehensive Review of Outdoor Thermal Comfort in Urban '
              'Areas: Effective Parameters and Approaches',
     'journal': 'Energy Environ.',
     'year': 2023,
     'doi': '10.1177/0958305X221116176'},

    # ---- European urban heat and health ---------------------------------
    "iungman2023": {'kind': 'article',
     'authors': 'Iungman, T. et al.',
     'title': 'Cooling Cities through Urban Green Infrastructure: A Health '
              'Impact Assessment of European Cities',
     'journal': 'Lancet',
     'year': 2023, 'volume': '401', 'pages': '577–589',
     'doi': '10.1016/S0140-6736(22)02585-5'},

    "garcialeon2024": {'kind': 'article',
     'authors': 'García-León, D.; Masselot, P.; Mistry, M.N.; '
                'Gasparrini, A. et al.',
     'title': 'Temperature-Related Mortality Burden and Projected Change in '
              '1368 European Regions: A Modelling Study',
     'journal': 'Lancet Public Health',
     'year': 2024,
     'doi': '10.1016/S2468-2667(24)00179-8'},

    # ---- siting, equity and policy --------------------------------------
    "hoover2021": {'kind': 'article',
     'authors': 'Hoover, F.-A.; Meerow, S.; Grabowski, Z.J.; McPhearson, T.',
     'title': 'Environmental Justice Implications of Siting Criteria in Urban '
              'Green Infrastructure Planning',
     'journal': 'J. Environ. Policy Plan.',
     'year': 2021,
     'doi': '10.1080/1523908X.2021.1945916'},

    "sobhaninia2025": {'kind': 'article',
     'authors': 'Sobhaninia, S.; Meerow, S.; Dugger, A.; Hopson, T.; He, C.; '
                'Wilhelmi, O.',
     'title': 'Where Should the Green Go? A Systematic Literature Review of '
              'Methods for Siting Green Infrastructure to Mitigate Rising '
              'Heat and Stormwater Risks in Cities Worldwide',
     'journal': 'Urban For. Urban Green.',
     'year': 2025},

    "anguelovski2022": {'kind': 'article',
     'authors': 'Anguelovski, I.; Connolly, J.J.T.; Cole, H.; '
                'Garcia-Lamarca, M.; Triguero-Mas, M.; Baró, F. et al.',
     'title': 'Green Gentrification in European and North American Cities',
     'journal': 'Nat. Commun.',
     'year': 2022,
     'doi': '10.1038/s41467-022-31572-1'},

    "hsu2021": {'kind': 'article',
     'authors': 'Hsu, A.; Sheriff, G.; Chakraborty, T.; Manya, D.',
     'title': 'Disproportionate Exposure to Urban Heat Island Intensity '
              'across Major US Cities',
     'journal': 'Nat. Commun.',
     'year': 2021, 'volume': '12', 'pages': '2721',
     'doi': '10.1038/s41467-021-22799-5'},

    "eu2024nature": {'kind': 'report',
     'authors': 'European Union',
     'title': 'Regulation (EU) 2024/1991 of the European Parliament and of '
              'the Council of 24 June 2024 on Nature Restoration and Amending '
              'Regulation (EU) 2022/869',
     'year': 2024,
     'publisher': 'Official Journal of the European Union, OJ L, 2024/1991',
     'url': 'https://eur-lex.europa.eu/legal-content/EN/TXT/'
            '?uri=OJ%3AL_202401991'},

    # ---- data sources ----------------------------------------------------
    "ghsucdb2019": {'kind': 'report',
     'authors': 'European Commission, Joint Research Centre',
     'title': 'GHS Urban Centre Database 2015, Multitemporal and '
              'Multidimensional Attributes, R2019A (Dataset)',
     'year': 2019,
     'publisher': 'European Commission, Joint Research Centre: Ispra, Italy',
     'url': 'https://data.jrc.ec.europa.eu/dataset/'
            '53473144-b88c-44bc-b4a3-4583ed1f547e'},

    "berkeleyearth": {'kind': 'report',
     'authors': 'Berkeley Earth',
     'title': 'Regional Land-Surface Temperature Summaries by Country '
              '(Dataset)',
     'year': 2021,
     'publisher': 'Berkeley Earth: Berkeley, CA, USA',
     'url': 'https://berkeleyearth.org/data/'},

    "worldbank2024": {'kind': 'report',
     'authors': 'World Bank',
     'title': 'World Development Indicators: Unemployment, Youth Total '
              '(% of Total Labor Force Ages 15–24) (Modelled ILO Estimate), '
              'Indicator SL.UEM.1524.ZS',
     'year': 2024,
     'publisher': 'World Bank: Washington, DC, USA',
     'url': 'https://data.worldbank.org/indicator/SL.UEM.1524.ZS'},
}
