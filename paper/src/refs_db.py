"""Master reference database (MDPI style). Reused template refs + new verified refs.
A Citation manager in the build script numbers only the tags actually cited, in order.
All DOIs verified to resolve (see research_output.json)."""
import json, re, os

_T = json.load(open(os.path.join(os.path.dirname(__file__), "data", "template_refs.json")))
def _t(n):  # template reference text by number (already MDPI-formatted with doi:)
    return _T[str(n)].strip()

# tag -> template number (reused, all have DOIs)
REUSE = {
 "jin_ultra":1,"slowik_nature":2,"tang_mrfomod":3,"jin_facial":4,"tang_smamod":5,
 "dai_jobshop":6,"tang_sparrow":7,"shen_sched":8,"cao_edge":9,"zeng_pso":10,
 "wang_giga":11,"zhao_xfem":12,"tang_eouav":13,"hu_mahaco":14,"sowmya_nrbo":15,
 "houssein_seahorse":16,"abualigah_rsa":17,"hu_gsrpso":18,"seyyed_apo_fs":19,"jia_mpa":20,
 "ga":21,"es":22,"de":23,"cmaes":24,"heoa":25,"ceo":26,"mvo":27,"fla":28,"sao":29,"plo":30,
 "srs":31,"mso":32,"koa":33,"sca":34,"aoa":35,"qrfs":36,"waa":37,"ttao":38,"etoa":39,
 "pso":40,"aco":41,"gwo":42,"ala":43,"coa":44,"dmo":45,"sdo":46,"sma":47,"apo":48,"gkso":49,
 "pdoa":50,"sboa":51,"nfl":52,"lshade":58,"rime":60,"qio":62,"mrfo":64,
}

# new references (MDPI style; DOIs verified). Format mirrors template: ... doi:XX
NEW = {
 # --- SBOA variants ---
 "sboa_misboa":"Qin, S.; Liu, J.; Bai, X.; Hu, G. A Multi-Strategy Improvement Secretary Bird Optimization Algorithm for Engineering Optimization Problems. Biomimetics 2024, 9, 478, doi:10.3390/biomimetics9080478.",
 "sboa_cg":"Wang, X.; Wei, P.; Li, Y. Enhanced Secretary Bird Optimization Algorithm with Multi-Strategy Fusion and Cauchy-Gaussian Crossover. Sci. Rep. 2025, 15, 23163, doi:10.1038/s41598-025-04469-4.",
 "sboa_cross":"Mai, X.; Zhong, Y.; Li, L. The Crossover Strategy Integrated Secretary Bird Optimization Algorithm and Its Application in Engineering Design Problems. Electron. Res. Arch. 2025, 33, 471-512, doi:10.3934/era.2025023.",
 "sboa_msv":"Seyyedabbasi, A. Multi-Strategy Variable Secretary Bird Optimization Algorithm (MSVSBOA) for Global Optimization and UAV 3D Path Planning. Symmetry 2026, 18, 273, doi:10.3390/sym18020273.",
 # --- improvement strategies ---
 "goodpoint":"Hua, L.K.; Wang, Y. Applications of Number Theory to Numerical Analysis; Springer-Verlag: Berlin/Heidelberg, Germany, 1981, doi:10.1007/978-3-642-67829-5.",
 "obl":"Tizhoosh, H.R. Opposition-Based Learning: A New Scheme for Machine Intelligence. In Proceedings of the International Conference on Computational Intelligence for Modelling, Control and Automation (CIMCA), Vienna, Austria, 28-30 November 2005; pp. 695-701, doi:10.1109/CIMCA.2005.1631345.",
 "qobl":"Rahnamayan, S.; Tizhoosh, H.R.; Salama, M.M.A. Quasi-Oppositional Differential Evolution. In Proceedings of the IEEE Congress on Evolutionary Computation (CEC), Singapore, 25-28 September 2007; pp. 2229-2236, doi:10.1109/CEC.2007.4424748.",
 "lensobl":"Long, W.; Jiao, J.; Wu, T.; Xu, M.; Tang, M. An Improved Sand Cat Swarm Optimization with Lens Opposition-Based Learning. Sci. Rep. 2024, 14, 21115, doi:10.1038/s41598-024-71581-2.",
 "mantegna":"Mantegna, R.N. Fast, Accurate Algorithm for Numerical Simulation of Levy Stable Stochastic Processes. Phys. Rev. E 1994, 49, 4677-4683, doi:10.1103/PhysRevE.49.4677.",
 "cuckoo":"Yang, X.-S.; Deb, S. Cuckoo Search via Levy Flights. In Proceedings of the World Congress on Nature & Biologically Inspired Computing (NaBIC), Coimbatore, India, 9-11 December 2009; pp. 210-214, doi:10.1109/NABIC.2009.5393690.",
 "fep":"Yao, X.; Liu, Y.; Lin, G. Evolutionary Programming Made Faster. IEEE Trans. Evol. Comput. 1999, 3, 82-102, doi:10.1109/4235.771163.",
 "woa":"Mirjalili, S.; Lewis, A. The Whale Optimization Algorithm. Adv. Eng. Softw. 2016, 95, 51-67, doi:10.1016/j.advengsoft.2016.01.008.",
 "tdist":"Li, C.; Zhao, W.; et al. A Novel Adaptive Sparrow Search Algorithm Based on Chaotic Mapping and t-Distribution Mutation. Appl. Sci. 2021, 11, 11192, doi:10.3390/app112311192.",
 "sandcat":"Zhang, X.; Wang, S.; et al. A Modified Sand Cat Swarm Optimization Algorithm Based on Multi-Strategy Fusion and Its Application in Engineering Problems. Mathematics 2024, 12, 2153, doi:10.3390/math12142153.",
 # --- color / aesthetics / design ---
 "cohenor":"Cohen-Or, D.; Sorkine, O.; Gal, R.; Leyvand, T.; Xu, Y.-Q. Color Harmonization. ACM Trans. Graph. 2006, 25, 624-630, doi:10.1145/1179352.1141933.",
 "odonovan_compat":"O'Donovan, P.; Agarwala, A.; Hertzmann, A. Color Compatibility from Large Datasets. ACM Trans. Graph. 2011, 30, 63:1-63:12, doi:10.1145/2010324.1964958.",
 "tokumaru":"Tokumaru, M.; Muranaka, N.; Imanishi, S. Color Design Support System Considering Color Harmony. In Proceedings of the 2002 IEEE International Conference on Fuzzy Systems (FUZZ-IEEE), Honolulu, HI, USA, 12-17 May 2002; pp. 378-383, doi:10.1109/FUZZ.2002.1005020.",
 "ngo":"Ngo, D.C.L.; Teo, L.S.; Byrne, J.G. Modelling Interface Aesthetics. Inf. Sci. 2003, 152, 25-46, doi:10.1016/S0020-0255(02)00404-8.",
 "lai":"Lai, C.-Y.; Chen, P.-H.; Shih, S.-W.; Liu, Y.; Hong, J.-S. Computational Models and Experimental Investigations of Effects of Balance and Symmetry on the Aesthetics of Text-Overlaid Images. Int. J. Hum.-Comput. Stud. 2010, 68, 41-56, doi:10.1016/j.ijhcs.2009.08.003.",
 "odonovan_layout":"O'Donovan, P.; Agarwala, A.; Hertzmann, A. Learning Layouts for Single-Page Graphic Designs. IEEE Trans. Vis. Comput. Graph. 2014, 20, 1200-1213, doi:10.1109/TVCG.2014.48.",
 "zhang_aes":"Zhang, J.; Miao, Y.; Yu, J. A Comprehensive Survey on Computational Aesthetic Evaluation of Visual Art Images: Metrics and Challenges. IEEE Access 2021, 9, 77164-77187, doi:10.1109/ACCESS.2021.3083075.",
 "deng_aes":"Deng, Y.; Loy, C.C.; Tang, X. Image Aesthetic Assessment: An Experimental Survey. IEEE Signal Process. Mag. 2017, 34, 80-106, doi:10.1109/MSP.2017.2696576.",
 "feng_paint":"Feng, S.-Y.; Ting, C.-K. Painting Using Genetic Algorithm with Aesthetic Evaluation of Visual Quality. In Technologies and Applications of Artificial Intelligence; Lecture Notes in Computer Science; Springer: Cham, Switzerland, 2014; Volume 8916, pp. 124-135, doi:10.1007/978-3-319-13987-6_12.",
 "galanter":"Galanter, P. Generative Art Theory. In A Companion to Digital Art; Paul, C., Ed.; John Wiley & Sons: Chichester, UK, 2016; pp. 146-180, doi:10.1002/9781118475249.ch5.",
 "hsiao_form":"Hsiao, S.-W.; Chiu, F.-Y.; Lu, S.-H. Product-Form Design Model Based on Genetic Algorithms. Int. J. Ind. Ergon. 2010, 40, 237-246, doi:10.1016/j.ergon.2010.01.009.",
 "lo_aes":"Lo, C.-H.; Ko, Y.-C.; Hsiao, S.-W. A Study That Applies Aesthetic Theory and Genetic Algorithms to Product Form Optimization. Adv. Eng. Inform. 2015, 29, 662-679, doi:10.1016/j.aei.2015.06.004.",
 "yang_kansei":"Yang, C.-C. Constructing a Hybrid Kansei Engineering System Based on Multiple Affective Responses: Application to Product Form Design. Comput. Ind. Eng. 2011, 60, 760-768, doi:10.1016/j.cie.2011.01.011.",
 "hu_colorscheme":"Hu, G.; Pan, Z.; Zhang, M.; Chen, D.; Yang, W.; Chen, J. An Interactive Method for Generating Harmonious Color Schemes. Color Res. Appl. 2014, 39, 70-78, doi:10.1002/col.21762.",
 "deng_colormatch":"Deng, L.; Zhou, F.; Zhang, Z. Interactive Genetic Color Matching Design of Cultural and Creative Products Considering Color Image and Visual Aesthetics. Heliyon 2022, 8, e10768, doi:10.1016/j.heliyon.2022.e10768.",
 "jiang_colorregen":"Jiang, Z.; Xia, J.; Xu, Y.; Zhang, Y. Cultural Heritage Color Regeneration: Interactive Genetic Algorithm Optimization Based on Color Network and Harmony Models. Appl. Sci. 2025, 15, 1720, doi:10.3390/app15041720.",
 # --- statistics / benchmark ---
 "derrac":"Derrac, J.; Garcia, S.; Molina, D.; Herrera, F. A Practical Tutorial on the Use of Nonparametric Statistical Tests as a Methodology for Comparing Evolutionary and Swarm Intelligence Algorithms. Swarm Evol. Comput. 2011, 1, 3-18, doi:10.1016/j.swevo.2011.02.002.",
 "cec2017":"Awad, N.H.; Ali, M.Z.; Liang, J.J.; Qu, B.Y.; Suganthan, P.N. Problem Definitions and Evaluation Criteria for the CEC 2017 Special Session and Competition on Single Objective Bound Constrained Real-Parameter Numerical Optimization; Technical Report; Nanyang Technological University: Singapore, 2016.",
}

def citation(tag):
    if tag in REUSE: return _t(REUSE[tag])
    if tag in NEW:  return NEW[tag]
    raise KeyError(f"unknown reference tag: {tag}")

ALL_TAGS = list(REUSE) + list(NEW)

if __name__ == "__main__":
    # sanity: every tag resolves and has a doi (except cec2017 tech report)
    missing=[]
    for t in ALL_TAGS:
        c=citation(t)
        if "doi:" not in c and t!="cec2017": missing.append(t)
    print(f"{len(ALL_TAGS)} references defined; {len(missing)} without doi:", missing)
