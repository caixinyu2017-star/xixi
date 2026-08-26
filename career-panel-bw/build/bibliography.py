# -*- coding: utf-8 -*-
"""The reference list.

Every entry was checked against a retrieved record during preparation, to the
standard that its author list, year, title and journal were seen rather than
recalled. Where a volume or page range could not be confirmed it is omitted
rather than guessed at, so a few entries are shorter than the others.
"""
from refs import add as A

# ---------------------------------------------------------------------------
# what a career theory claims, and over what horizon
# ---------------------------------------------------------------------------
A("lent1994", authors=[("Lent", "R. W."), ("Brown", "S. D."),
                       ("Hackett", "G.")], year=1994,
  title=("Toward a unifying social cognitive theory of career and academic "
         "interest, choice, and performance"),
  journal="Journal of Vocational Behavior", volume="45", pages="79–122")

A("lentbrown2013", authors=[("Lent", "R. W."), ("Brown", "S. D.")], year=2013,
  title=("Social cognitive model of career self-management: Toward a "
         "unifying view of adaptive career behavior across the life span"),
  journal="Journal of Counseling Psychology", volume="60", pages="557–568")

A("savickas2013", kind="chapter",
  authors=[("Savickas", "M. L.")], year=2013,
  title="Career construction theory and practice",
  booktitle=("Career development and counseling: Putting theory and "
             "research to work"),
  editors="S. D. Brown & R. W. Lent", publisher="Wiley", pages="147–183")

A("ng2005", authors=[("Ng", "T. W. H."), ("Eby", "L. T."),
                     ("Sorensen", "K. L."), ("Feldman", "D. C.")], year=2005,
  title="Predictors of objective and subjective career success: A "
        "meta-analysis",
  journal="Personnel Psychology", volume="58", pages="367–408")

A("spurk2019", authors=[("Spurk", "D."), ("Hirschi", "A."),
                        ("Dries", "N.")], year=2019,
  title=("Antecedents and outcomes of objective versus subjective career "
         "success: Competing perspectives and future directions"),
  journal="Journal of Management", volume="45", pages="35–69")

# ---------------------------------------------------------------------------
# the between-within distinction
# ---------------------------------------------------------------------------
A("mundlak1978", authors=[("Mundlak", "Y.")], year=1978,
  title="On the pooling of time series and cross section data",
  journal="Econometrica", volume="46", pages="69–85")

A("belljones2015", authors=[("Bell", "A."), ("Jones", "K.")], year=2015,
  title=("Explaining fixed effects: Random effects modeling of time-series "
         "cross-sectional and panel data"),
  journal="Political Science Research and Methods", volume="3",
  pages="133–153")

A("curran2011", authors=[("Curran", "P. J."), ("Bauer", "D. J.")], year=2011,
  title=("The disaggregation of within-person and between-person effects in "
         "longitudinal models of change"),
  journal="Annual Review of Psychology", volume="62", pages="583–619")

A("molenaar2004", authors=[("Molenaar", "P. C. M.")], year=2004,
  title=("A manifesto on psychology as idiographic science: Bringing the "
         "person back into scientific psychology, this time forever"),
  journal="Measurement: Interdisciplinary Research and Perspectives",
  volume="2", pages="201–218")

A("hamaker2015", authors=[("Hamaker", "E. L."), ("Kuiper", "R. M."),
                          ("Grasman", "R. P. P. P.")], year=2015,
  title="A critique of the cross-lagged panel model",
  journal="Psychological Methods", volume="20", pages="102–116")

A("maxwell2007", authors=[("Maxwell", "S. E."), ("Cole", "D. A.")], year=2007,
  title="Bias in cross-sectional analyses of longitudinal mediation",
  journal="Psychological Methods", volume="12", pages="23–44")

A("colepreacher2014", authors=[("Cole", "D. A."), ("Preacher", "K. J.")],
  year=2014,
  title=("Manifest variable path analysis: Potentially serious and "
         "misleading consequences due to uncorrected measurement error"),
  journal="Psychological Methods", volume="19", pages="300–315")

A("wang2017", authors=[("Wang", "M."), ("Beal", "D. J."), ("Chan", "D."),
                       ("Newman", "D. A."), ("Vancouver", "J. B."),
                       ("Vandenberg", "R. J.")], year=2017,
  title=("Longitudinal research: A panel discussion on conceptual issues, "
         "research design, and statistical techniques"),
  journal="Work, Aging and Retirement", volume="3", pages="1–24")

# ---------------------------------------------------------------------------
# estimation and inference
# ---------------------------------------------------------------------------
A("wooldridge2010", kind="book", authors=[("Wooldridge", "J. M.")], year=2010,
  title="Econometric analysis of cross section and panel data",
  edition="2nd ed.", publisher="MIT Press")

A("baltagi2021", kind="book", authors=[("Baltagi", "B. H.")], year=2021,
  title="Econometric analysis of panel data", edition="6th ed.",
  publisher="Springer")

A("hausman1978", authors=[("Hausman", "J. A.")], year=1978,
  title="Specification tests in econometrics",
  journal="Econometrica", volume="46", pages="1251–1271")

A("cameron2015", authors=[("Cameron", "A. C."), ("Miller", "D. L.")],
  year=2015,
  title="A practitioner's guide to cluster-robust inference",
  journal="Journal of Human Resources", volume="50", pages="317–372")

A("bh1995", authors=[("Benjamini", "Y."), ("Hochberg", "Y.")], year=1995,
  title=("Controlling the false discovery rate: A practical and powerful "
         "approach to multiple testing"),
  journal="Journal of the Royal Statistical Society: Series B", volume="57",
  pages="289–300")

A("aiken1991", kind="book", authors=[("Aiken", "L. S."), ("West", "S. G.")],
  year=1991,
  title="Multiple regression: Testing and interpreting interactions",
  publisher="Sage")

# ---------------------------------------------------------------------------
# what the two panels have been used to establish
# ---------------------------------------------------------------------------
A("mincer1974", kind="book", authors=[("Mincer", "J.")], year=1974,
  title="Schooling, experience, and earnings",
  publisher="National Bureau of Economic Research")

A("altonji1987", authors=[("Altonji", "J. G."), ("Shakotko", "R. A.")],
  year=1987, title="Do wages rise with job seniority?",
  journal="The Review of Economic Studies", volume="54", pages="437–459")

A("topel1991", authors=[("Topel", "R. H.")], year=1991,
  title="Specific capital, mobility, and wages: Wages rise with job "
        "seniority",
  journal="Journal of Political Economy", volume="99", pages="145–176")

A("vella1998", authors=[("Vella", "F."), ("Verbeek", "M.")], year=1998,
  title=("Whose wages do unions raise? A dynamic model of unionism and wage "
         "rate determination for young men"),
  journal="Journal of Applied Econometrics", volume="13", pages="163–183")

A("gregg2005", authors=[("Gregg", "P."), ("Tominey", "E.")], year=2005,
  title="The wage scar from male youth unemployment",
  journal="Labour Economics", volume="12", pages="487–509")

A("arulampalam2001", authors=[("Arulampalam", "W.")], year=2001,
  title=("Is unemployment really scarring? Effects of unemployment "
         "experiences on wages"),
  journal="The Economic Journal")

# ---------------------------------------------------------------------------
# the data
# ---------------------------------------------------------------------------
A("bls_nlsw", kind="report",
  authors=[("U.S. Bureau of Labor Statistics", None)], year="2024a",
  title="National Longitudinal Survey of Young Women, 1968–1988",
  publisher="U.S. Department of Labor")

A("bls_nlsy79", kind="report",
  authors=[("U.S. Bureau of Labor Statistics", None)], year="2024b",
  title="National Longitudinal Survey of Youth 1979",
  publisher="U.S. Department of Labor")
