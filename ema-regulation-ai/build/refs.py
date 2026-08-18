# -*- coding: utf-8 -*-
"""The bibliography, in IEEE reference style.

Every entry is a real, verifiable publication. Entries are rendered by
build_docx.py and numbered by order of first citation in the text; the
italicised element of each entry is the journal, proceedings or book
title, as the journal's style requires.
"""

# Each entry: (plain-before, italic, plain-after). The renderer emits the
# three parts in order, italicising the middle one.
REFS = {
    # ---- emotion regulation: theory --------------------------------
    "gross1998": (
        "J. J. Gross, “The emerging field of emotion regulation: "
        "An integrative review,” ",
        "Rev. Gen. Psychol.",
        ", vol. 2, no. 3, pp. 271–299, Sep. 1998, "
        "doi: 10.1037/1089-2680.2.3.271."),
    "gross2015": (
        "J. J. Gross, “Emotion regulation: Current status and "
        "future prospects,” ",
        "Psychol. Inq.",
        ", vol. 26, no. 1, pp. 1–26, Jan. 2015, "
        "doi: 10.1080/1047840X.2014.940781."),
    "grossjohn2003": (
        "J. J. Gross and O. P. John, “Individual differences in two "
        "emotion regulation processes: Implications for affect, "
        "relationships, and well-being,” ",
        "J. Pers. Soc. Psychol.",
        ", vol. 85, no. 2, pp. 348–362, Aug. 2003, "
        "doi: 10.1037/0022-3514.85.2.348."),
    "aldao2010": (
        "A. Aldao, S. Nolen-Hoeksema, and S. Schweizer, “Emotion-"
        "regulation strategies across psychopathology: A meta-analytic "
        "review,” ",
        "Clin. Psychol. Rev.",
        ", vol. 30, no. 2, pp. 217–237, Mar. 2010, "
        "doi: 10.1016/j.cpr.2009.11.004."),
    "aldao2013": (
        "A. Aldao, “The future of emotion regulation research: "
        "Capturing context,” ",
        "Perspect. Psychol. Sci.",
        ", vol. 8, no. 2, pp. 155–172, Mar. 2013, "
        "doi: 10.1177/1745691612459518."),
    "bonanno2013": (
        "G. A. Bonanno and C. L. Burton, “Regulatory flexibility: "
        "An individual differences perspective on coping and emotion "
        "regulation,” ",
        "Perspect. Psychol. Sci.",
        ", vol. 8, no. 6, pp. 591–612, Nov. 2013, "
        "doi: 10.1177/1745691613504116."),
    "haines2016": (
        "S. J. Haines et al., “The wisdom to know the difference: "
        "Strategy-situation fit in emotion regulation in daily life is "
        "associated with well-being,” ",
        "Psychol. Sci.",
        ", vol. 27, no. 12, pp. 1651–1659, Dec. 2016, "
        "doi: 10.1177/0956797616669086."),
    "gratz2004": (
        "K. L. Gratz and L. Roemer, “Multidimensional assessment of "
        "emotion regulation and dysregulation: Development, factor "
        "structure, and initial validation of the Difficulties in "
        "Emotion Regulation Scale,” ",
        "J. Psychopathol. Behav. Assess.",
        ", vol. 26, no. 1, pp. 41–54, Mar. 2004, "
        "doi: 10.1023/B:JOBA.0000007455.08539.94."),
    "webb2012": (
        "T. L. Webb, E. Miles, and P. Sheeran, “Dealing with "
        "feeling: A meta-analysis of the effectiveness of strategies "
        "derived from the process model of emotion regulation,” ",
        "Psychol. Bull.",
        ", vol. 138, no. 4, pp. 775–808, Jul. 2012, "
        "doi: 10.1037/a0027600."),
    "sheppes2011": (
        "G. Sheppes, S. Scheibe, G. Suri, and J. J. Gross, “Emotion-"
        "regulation choice,” ",
        "Psychol. Sci.",
        ", vol. 22, no. 11, pp. 1391–1396, Nov. 2011, "
        "doi: 10.1177/0956797611418350."),

    # ---- affect dynamics and EMA -----------------------------------
    "kuppens2010": (
        "P. Kuppens, N. B. Allen, and L. B. Sheeber, “Emotional "
        "inertia and psychological maladjustment,” ",
        "Psychol. Sci.",
        ", vol. 21, no. 7, pp. 984–991, Jul. 2010, "
        "doi: 10.1177/0956797610372634."),
    "kuppens2017": (
        "P. Kuppens and P. Verduyn, “Emotion dynamics,” ",
        "Curr. Opin. Psychol.",
        ", vol. 17, pp. 22–26, Oct. 2017, "
        "doi: 10.1016/j.copsyc.2017.06.004."),
    "shiffman2008": (
        "S. Shiffman, A. A. Stone, and M. R. Hufford, “Ecological "
        "momentary assessment,” ",
        "Annu. Rev. Clin. Psychol.",
        ", vol. 4, pp. 1–32, Apr. 2008, "
        "doi: 10.1146/annurev.clinpsy.3.022806.091415."),
    "trull2013": (
        "T. J. Trull and U. W. Ebner-Priemer, “Ambulatory "
        "assessment,” ",
        "Annu. Rev. Clin. Psychol.",
        ", vol. 9, pp. 151–176, Mar. 2013, "
        "doi: 10.1146/annurev-clinpsy-050212-185510."),
    "myin2018": (
        "I. Myin-Germeys et al., “Experience sampling methodology "
        "in mental health research: New insights and technical "
        "developments,” ",
        "World Psychiatry",
        ", vol. 17, no. 2, pp. 123–132, Jun. 2018, "
        "doi: 10.1002/wps.20513."),
    "wrzus2015": (
        "C. Wrzus and M. R. Mehl, “Lab and/or field? Measuring "
        "personality processes and their social consequences,” ",
        "Eur. J. Pers.",
        ", vol. 29, no. 2, pp. 250–271, Mar. 2015, "
        "doi: 10.1002/per.1986."),
    "hamaker2017": (
        "E. L. Hamaker and M. Wichers, “No time like the present: "
        "Discovering the hidden dynamics in intensive longitudinal "
        "data,” ",
        "Curr. Dir. Psychol. Sci.",
        ", vol. 26, no. 1, pp. 10–15, Feb. 2017, "
        "doi: 10.1177/0963721416666518."),
    "brose2015": (
        "A. Brose, P. Voelkle, M. Lövdén, U. Lindenberger, and "
        "F. Schmiedek, “Differences in the between-person and "
        "within-person structures of affect are a matter of degree,” ",
        "Eur. J. Pers.",
        ", vol. 29, no. 1, pp. 55–71, Jan. 2015, "
        "doi: 10.1002/per.1961."),

    # ---- digital phenotyping and computational mental health -------
    "insel2017": (
        "T. R. Insel, “Digital phenotyping: Technology for a new "
        "science of behavior,” ",
        "JAMA",
        ", vol. 318, no. 13, pp. 1215–1216, Oct. 2017, "
        "doi: 10.1001/jama.2017.11295."),
    "mohr2017": (
        "D. C. Mohr, M. Zhang, and S. M. Schueller, “Personal "
        "sensing: Understanding mental health using ubiquitous sensors "
        "and machine learning,” ",
        "Annu. Rev. Clin. Psychol.",
        ", vol. 13, pp. 23–47, May 2017, "
        "doi: 10.1146/annurev-clinpsy-032816-044949."),
    "dwyer2018": (
        "D. B. Dwyer, P. Falkai, and N. Koutsouleris, “Machine "
        "learning approaches for clinical psychology and "
        "psychiatry,” ",
        "Annu. Rev. Clin. Psychol.",
        ", vol. 14, pp. 91–118, May 2018, "
        "doi: 10.1146/annurev-clinpsy-032816-045037."),
    "jacobson2022": (
        "N. C. Jacobson and B. Bhattacharya, “Digital biomarkers of "
        "anxiety disorder symptom changes: Personalized deep learning "
        "models using smartphone sensors accurately predict anxiety "
        "symptoms from ecological momentary assessments,” ",
        "Behav. Res. Ther.",
        ", vol. 149, Art. no. 104013, Feb. 2022, "
        "doi: 10.1016/j.brat.2021.104013."),
    "shatte2019": (
        "A. B. R. Shatte, D. M. Hutchinson, and S. J. Teague, "
        "“Machine learning in mental health: A scoping review of "
        "methods and applications,” ",
        "Psychol. Med.",
        ", vol. 49, no. 9, pp. 1426–1448, Jul. 2019, "
        "doi: 10.1017/S0033291719000151."),
    "torous2021": (
        "J. Torous, S. Bucci, I. H. Bell, L. V. Kessing, M. Faurholt-"
        "Jepsen, P. Whelan, A. F. Carvalho, M. Keshavan, J. Linardon, "
        "and J. Firth, “The growing field of digital psychiatry: "
        "Current evidence and the future of apps, social media, "
        "chatbots, and virtual reality,” ",
        "World Psychiatry",
        ", vol. 20, no. 3, pp. 318–335, Oct. 2021, "
        "doi: 10.1002/wps.20883."),

    # ---- explainability and trustworthy AI -------------------------
    "ribeiro2016": (
        "M. T. Ribeiro, S. Singh, and C. Guestrin, “‘Why "
        "should I trust you?’: Explaining the predictions of any "
        "classifier,” in ",
        "Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining",
        ", San Francisco, CA, USA, 2016, pp. 1135–1144, "
        "doi: 10.1145/2939672.2939778."),
    "lundberg2017": (
        "S. M. Lundberg and S.-I. Lee, “A unified approach to "
        "interpreting model predictions,” in ",
        "Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)",
        ", Long Beach, CA, USA, 2017, pp. 4765–4774."),
    "rudin2019": (
        "C. Rudin, “Stop explaining black box machine learning "
        "models for high stakes decisions and use interpretable models "
        "instead,” ",
        "Nat. Mach. Intell.",
        ", vol. 1, no. 5, pp. 206–215, May 2019, "
        "doi: 10.1038/s42256-019-0048-x."),
    "doshi2017": (
        "F. Doshi-Velez and B. Kim, “Towards a rigorous science of "
        "interpretable machine learning,” 2017, ",
        "arXiv:1702.08608",
        ", doi: 10.48550/arXiv.1702.08608."),
    "jain2019": (
        "S. Jain and B. C. Wallace, “Attention is not "
        "explanation,” in ",
        "Proc. Conf. North Amer. Chapter Assoc. Comput. Linguistics "
        "(NAACL-HLT)",
        ", Minneapolis, MN, USA, 2019, pp. 3543–3556, "
        "doi: 10.18653/v1/N19-1357."),
    "wiegreffe2019": (
        "S. Wiegreffe and Y. Pinter, “Attention is not not "
        "explanation,” in ",
        "Proc. Conf. Empir. Methods Natural Lang. Process. (EMNLP-"
        "IJCNLP)",
        ", Hong Kong, China, 2019, pp. 11–20, "
        "doi: 10.18653/v1/D19-1002."),
    "deyoung2020": (
        "J. DeYoung, S. Jain, N. F. Rajani, E. Lehman, C. Xiong, "
        "R. Socher, and B. C. Wallace, “ERASER: A benchmark to "
        "evaluate rationalized NLP models,” in ",
        "Proc. 58th Annu. Meeting Assoc. Comput. Linguistics (ACL)",
        ", 2020, pp. 4443–4458, doi: 10.18653/v1/2020.acl-main.408."),
    "sundararajan2017": (
        "M. Sundararajan, A. Taly, and Q. Yan, “Axiomatic "
        "attribution for deep networks,” in ",
        "Proc. 34th Int. Conf. Mach. Learn. (ICML)",
        ", Sydney, NSW, Australia, 2017, pp. 3319–3328."),
    "amann2020": (
        "J. Amann, A. Blasimme, E. Vayena, D. Frey, and V. I. Madai, "
        "“Explainability for artificial intelligence in "
        "healthcare: A multidisciplinary perspective,” ",
        "BMC Med. Inform. Decis. Mak.",
        ", vol. 20, no. 1, Art. no. 310, Nov. 2020, "
        "doi: 10.1186/s12911-020-01332-6."),

    # ---- neural architectures --------------------------------------
    "vaswani2017": (
        "A. Vaswani et al., “Attention is all you need,” in ",
        "Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)",
        ", Long Beach, CA, USA, 2017, pp. 5998–6008."),
    "cho2014": (
        "K. Cho et al., “Learning phrase representations using RNN "
        "encoder–decoder for statistical machine "
        "translation,” in ",
        "Proc. Conf. Empir. Methods Natural Lang. Process. (EMNLP)",
        ", Doha, Qatar, 2014, pp. 1724–1734, "
        "doi: 10.3115/v1/D14-1179."),
    "kipf2017": (
        "T. N. Kipf and M. Welling, “Semi-supervised "
        "classification with graph convolutional networks,” in ",
        "Proc. Int. Conf. Learn. Representations (ICLR)",
        ", Toulon, France, 2017."),
    "velickovic2018": (
        "P. Veličković, G. Cucurull, A. Casanova, A. Romero, "
        "P. Liò, and Y. Bengio, “Graph attention "
        "networks,” in ",
        "Proc. Int. Conf. Learn. Representations (ICLR)",
        ", Vancouver, BC, Canada, 2018."),
    "zhao2020": (
        "L. Zhao et al., “T-GCN: A temporal graph convolutional "
        "network for traffic prediction,” ",
        "IEEE Trans. Intell. Transp. Syst.",
        ", vol. 21, no. 9, pp. 3848–3858, Sep. 2020, "
        "doi: 10.1109/TITS.2019.2935152."),
    "kingma2015": (
        "D. P. Kingma and J. Ba, “Adam: A method for stochastic "
        "optimization,” in ",
        "Proc. Int. Conf. Learn. Representations (ICLR)",
        ", San Diego, CA, USA, 2015."),
    "sarker2021": (
        "M. K. Sarker, L. Zhou, A. Eberhart, and P. Hitzler, “Neuro-"
        "symbolic artificial intelligence: Current trends,” ",
        "AI Commun.",
        ", vol. 34, no. 3, pp. 197–209, 2021, "
        "doi: 10.3233/AIC-210084."),
    "garcez2023": (
        "A. d’Avila Garcez and L. C. Lamb, “Neurosymbolic AI: "
        "The 3rd wave,” ",
        "Artif. Intell. Rev.",
        ", vol. 56, no. 11, pp. 12387–12406, Nov. 2023, "
        "doi: 10.1007/s10462-023-10448-w."),
    "koh2020": (
        "P. W. Koh, T. Nguyen, Y. S. Tang, S. Mussmann, E. Pierson, "
        "B. Kim, and P. Liang, “Concept bottleneck models,” "
        "in ",
        "Proc. 37th Int. Conf. Mach. Learn. (ICML)",
        ", 2020, pp. 5338–5348."),
    "chen2019": (
        "C. Chen, O. Li, D. Tao, A. Barnett, C. Rudin, and J. Su, "
        "“This looks like that: Deep learning for interpretable "
        "image recognition,” in ",
        "Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)",
        ", Vancouver, BC, Canada, 2019, pp. 8930–8941."),

    # ---- assessment, ontologies, governance ------------------------
    "grau2008": (
        "B. C. Grau, I. Horrocks, B. Motik, B. Parsia, "
        "P. Patel-Schneider, and U. Sattler, “OWL 2: The next step "
        "for OWL,” ",
        "J. Web Semant.",
        ", vol. 6, no. 4, pp. 309–322, Nov. 2008, "
        "doi: 10.1016/j.websem.2008.05.001."),
    "hastings2011": (
        "J. Hastings, W. Ceusters, B. Smith, and K. Mulligan, “The "
        "emotion ontology: Enabling interdisciplinary research in the "
        "affective sciences,” in ",
        "Modeling and Using Context (Lecture Notes in Computer "
        "Science)",
        ", vol. 6967, Berlin, Germany: Springer, 2011, "
        "pp. 119–123, doi: 10.1007/978-3-642-24279-3_14."),
    "eu2024": (
        "European Parliament and Council of the European Union, "
        "“Regulation (EU) 2024/1689 laying down harmonised rules "
        "on artificial intelligence,” ",
        "Off. J. Eur. Union",
        ", L 2024/1689, Jul. 2024."),
    "fiske2019": (
        "A. Fiske, P. Henningsen, and A. Buyx, “Your robot "
        "therapist will see you now: Ethical implications of embodied "
        "artificial intelligence in psychiatry, psychology, and "
        "psychotherapy,” ",
        "J. Med. Internet Res.",
        ", vol. 21, no. 5, Art. no. e13216, May 2019, "
        "doi: 10.2196/13216."),
    "hitchcock2022": (
        "P. F. Hitchcock, E. Fried, and M. J. Frank, “Computational "
        "psychiatry needs time and context,” ",
        "Annu. Rev. Psychol.",
        ", vol. 73, pp. 243–270, Jan. 2022, "
        "doi: 10.1146/annurev-psych-021621-124910."),
    "fried2017": (
        "E. I. Fried and A. O. J. Cramer, “Moving forward: "
        "Challenges and directions for psychopathological network "
        "theory and methodology,” ",
        "Perspect. Psychol. Sci.",
        ", vol. 12, no. 6, pp. 999–1020, Nov. 2017, "
        "doi: 10.1177/1745691617705892."),
    "yarkoni2017": (
        "T. Yarkoni and J. Westfall, “Choosing prediction over "
        "explanation in psychology: Lessons from machine "
        "learning,” ",
        "Perspect. Psychol. Sci.",
        ", vol. 12, no. 6, pp. 1100–1122, Nov. 2017, "
        "doi: 10.1177/1745691617693393."),
    "moshontz2018": (
        "H. Moshontz et al., “The Psychological Science "
        "Accelerator: Advancing psychology through a distributed "
        "collaborative network,” ",
        "Adv. Methods Pract. Psychol. Sci.",
        ", vol. 1, no. 4, pp. 501–515, Dec. 2018, "
        "doi: 10.1177/2515245918797607."),
    "bringmann2018": (
        "L. F. Bringmann, E. Ferrer, E. L. Hamaker, D. Borsboom, and "
        "F. Tuerlinckx, “Modeling nonstationary emotion dynamics "
        "in dyads using a time-varying vector-autoregressive "
        "model,” ",
        "Multivariate Behav. Res.",
        ", vol. 53, no. 3, pp. 293–314, May 2018, "
        "doi: 10.1080/00273171.2018.1439722."),
}
