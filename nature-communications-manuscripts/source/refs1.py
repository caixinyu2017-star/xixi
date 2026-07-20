# -*- coding: utf-8 -*-
"""Verified real references for Paper 1 (ML/NLP detection of greenwashing).
Nature Communications style. Numbering assigned by order of first appearance."""

REFS = {
 # --- greenwashing theory / definition ---
 "delmas2011": "Delmas, M. A. & Burbano, V. C. The drivers of greenwashing. *Calif. Manage. Rev.* **54**, 64–87 (2011).",
 "lyon2015": "Lyon, T. P. & Montgomery, A. W. The means and end of greenwash. *Organ. Environ.* **28**, 223–249 (2015).",
 "marquis2016": "Marquis, C., Toffel, M. W. & Zhou, Y. Scrutiny, norms, and selective disclosure: a global study of greenwashing. *Organ. Sci.* **27**, 483–504 (2016).",
 "lyon2011": "Lyon, T. P. & Maxwell, J. W. Greenwash: corporate environmental disclosure under threat of audit. *J. Econ. Manag. Strategy* **20**, 3–41 (2011).",
 # --- symbolic vs substantive / decoupling ---
 "meyer1977": "Meyer, J. W. & Rowan, B. Institutionalized organizations: formal structure as myth and ceremony. *Am. J. Sociol.* **83**, 340–363 (1977).",
 "bromley2012": "Bromley, P. & Powell, W. W. From smoke and mirrors to walking the talk: decoupling in the contemporary world. *Acad. Manag. Ann.* **6**, 483–530 (2012).",
 "berrone2017": "Berrone, P., Fosfuri, A. & Gelabert, L. Does greenwashing pay off? Understanding the relationship between environmental actions and environmental legitimacy. *J. Bus. Ethics* **144**, 363–379 (2017).",
 "testa2018": "Testa, F., Boiral, O. & Iraldo, F. Internalization of environmental practices and institutional complexity: can stakeholders pressures encourage greenwashing? *J. Bus. Ethics* **147**, 287–307 (2018).",
 # --- net-zero pledges / credibility ---
 "rogelj2016": "Rogelj, J. et al. Paris Agreement climate proposals need a boost to keep warming well below 2 °C. *Nature* **534**, 631–639 (2016).",
 "rogelj2021": "Rogelj, J., Geden, O., Cowie, A. & Reisinger, A. Net-zero emissions targets are vague: three ways to fix. *Nature* **591**, 365–368 (2021).",
 "fankhauser2022": "Fankhauser, S. et al. The meaning of net zero and how to get it right. *Nat. Clim. Change* **12**, 15–21 (2022).",
 "hale2022": "Hale, T. et al. Assessing the rapidly-emerging landscape of net zero targets. *Clim. Policy* **22**, 18–29 (2022).",
 "hohne2021": "Höhne, N. et al. Wave of net zero emission targets opens window to meeting the Paris Agreement. *Nat. Clim. Change* **11**, 820–822 (2021).",
 # --- textual analysis in finance/accounting ---
 "loughran2011": "Loughran, T. & McDonald, B. When is a liability not a liability? Textual analysis, dictionaries, and 10-Ks. *J. Finance* **66**, 35–65 (2011).",
 "loughran2016": "Loughran, T. & McDonald, B. Textual analysis in accounting and finance: a survey. *J. Account. Res.* **54**, 1187–1230 (2016).",
 "tetlock2007": "Tetlock, P. C. Giving content to investor sentiment: the role of media in the stock market. *J. Finance* **62**, 1139–1168 (2007).",
 "gentzkow2019": "Gentzkow, M., Kelly, B. & Taddy, M. Text as data. *J. Econ. Lit.* **57**, 535–574 (2019).",
 # --- ML for text classification & interpretability ---
 "breiman2001": "Breiman, L. Random forests. *Mach. Learn.* **45**, 5–32 (2001).",
 "friedman2001": "Friedman, J. H. Greedy function approximation: a gradient boosting machine. *Ann. Stat.* **29**, 1189–1232 (2001).",
 "chen2016": "Chen, T. & Guestrin, C. XGBoost: a scalable tree boosting system. In *Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining* 785–794 (ACM, 2016).",
 "devlin2019": "Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. BERT: pre-training of deep bidirectional transformers for language understanding. In *Proc. 2019 Conf. North American Chapter of the ACL: Human Language Technologies* 4171–4186 (ACL, 2019).",
 "reimers2019": "Reimers, N. & Gurevych, I. Sentence-BERT: sentence embeddings using Siamese BERT-networks. In *Proc. 2019 Conf. Empirical Methods in Natural Language Processing* 3982–3992 (ACL, 2019).",
 "vaswani2017": "Vaswani, A. et al. Attention is all you need. In *Advances in Neural Information Processing Systems* **30**, 5998–6008 (2017).",
 "lundberg2017": "Lundberg, S. M. & Lee, S.-I. A unified approach to interpreting model predictions. In *Advances in Neural Information Processing Systems* **30**, 4765–4774 (2017).",
 "mikolov2013": "Mikolov, T., Sutskever, I., Chen, K., Corrado, G. & Dean, J. Distributed representations of words and phrases and their compositionality. In *Advances in Neural Information Processing Systems* **26**, 3111–3119 (2013).",
 # --- disclosure regulation ---
 "tcfd2017": "Task Force on Climate-related Financial Disclosures. *Recommendations of the Task Force on Climate-related Financial Disclosures* (Financial Stability Board, 2017).",
 "csrd2022": "European Parliament and Council of the European Union. Directive (EU) 2022/2464 as regards corporate sustainability reporting. *Off. J. Eur. Union* **L322**, 15–80 (2022).",
 "taxonomy2020": "European Parliament and Council of the European Union. Regulation (EU) 2020/852 on the establishment of a framework to facilitate sustainable investment. *Off. J. Eur. Union* **L198**, 13–43 (2020).",
 "sec2024": "U.S. Securities and Exchange Commission. *The Enhancement and Standardization of Climate-Related Disclosures for Investors*. Final rule, File No. S7-10-22. *Fed. Regist.* **89**, 21668 (2024).",
 "issb2023": "International Sustainability Standards Board. *IFRS S2 Climate-related Disclosures* (IFRS Foundation, 2023).",
 "ilhan2023": "Ilhan, E., Krueger, P., Sautner, Z. & Starks, L. T. Climate risk disclosure and institutional investors. *Rev. Financ. Stud.* **36**, 2617–2650 (2023).",
 # --- scope 1/2/3 emissions accounting ---
 "klaassen2021": "Klaaßen, L. & Stoll, C. Harmonizing corporate carbon footprints. *Nat. Commun.* **12**, 6149 (2021).",
 "matsumura2014": "Matsumura, E. M., Prakash, R. & Vera-Muñoz, S. C. Firm-value effects of carbon emissions and carbon disclosures. *Account. Rev.* **89**, 695–724 (2014).",
 "patchell2018": "Patchell, J. Can the implications of the GHG Protocol's scope 3 standard be realized? *J. Clean. Prod.* **185**, 941–958 (2018).",
 "hettler2024": "Hettler, M. & Graf-Vlachy, L. Corporate scope 3 carbon emission reporting as an enabler of supply chain decarbonization: a systematic review and comprehensive research agenda. *Bus. Strategy Environ.* **33**, 263–282 (2024).",
 # --- investor / market reactions & ESG-rating disagreement ---
 "berg2022": "Berg, F., Kölbel, J. F. & Rigobon, R. Aggregate confusion: the divergence of ESG ratings. *Rev. Finance* **26**, 1315–1344 (2022).",
 "krueger2020": "Krueger, P., Sautner, Z. & Starks, L. T. The importance of climate risks for institutional investors. *Rev. Financ. Stud.* **33**, 1067–1111 (2020).",
 "ilhan2021": "Ilhan, E., Sautner, Z. & Vilkov, G. Carbon tail risk. *Rev. Financ. Stud.* **34**, 1540–1571 (2021).",
 "bolton2021": "Bolton, P. & Kacperczyk, M. Do investors care about carbon risk? *J. Financ. Econ.* **142**, 517–549 (2021).",
 "yu2020": "Yu, E. P., Luu, B. V. & Chen, C. H. Greenwashing in environmental, social and governance disclosures. *Res. Int. Bus. Finance* **52**, 101192 (2020).",
 # --- AI/ML applied to sustainability / climate text mining ---
 "bingler2022": "Bingler, J. A., Kraus, M., Leippold, M. & Webersinke, N. Cheap talk and cherry-picking: what ClimateBert has to say on corporate climate risk disclosures. *Financ. Res. Lett.* **47**, 102776 (2022).",
 "sautner2023": "Sautner, Z., van Lent, L., Vilkov, G. & Zhang, R. Firm-level climate change exposure. *J. Finance* **78**, 1449–1498 (2023).",
 "kolbel2024": "Kölbel, J. F., Leippold, M., Rillaerts, J. & Wang, Q. Ask BERT: how regulatory disclosure of transition and physical climate risks affects the CDS term structure. *J. Financ. Econom.* **22**, 30–69 (2024).",
 "stammbach2023": "Stammbach, D., Webersinke, N., Bingler, J. A., Kraus, M. & Leippold, M. Environmental claim detection. In *Proc. 61st Annual Meeting of the Association for Computational Linguistics (Vol. 2: Short Papers)* 1051–1066 (ACL, 2023).",
 "webersinke2021": "Webersinke, N., Kraus, M., Bingler, J. A. & Leippold, M. ClimateBert: a pretrained language model for climate-related text. Preprint at https://arxiv.org/abs/2110.12010 (2021).",
 # --- multidisciplinary anchors ---
 "griscom2017": "Griscom, B. W. et al. Natural climate solutions. *Proc. Natl Acad. Sci. USA* **114**, 11645–11650 (2017).",
 "friedlingstein2023": "Friedlingstein, P. et al. Global Carbon Budget 2023. *Earth Syst. Sci. Data* **15**, 5301–5369 (2023).",
}
