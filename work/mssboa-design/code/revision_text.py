"""All new manuscript text, grouped by the reviewer that prompted it.

Kept separate from build_revision.py so that the wording can be edited without
touching the document-surgery logic.  Placeholders written as {name} are filled
from the experiment tables at build time.
"""

# =====================================================================
#  Reviewer 1 - red
# =====================================================================

R1_ABSTRACT_OLD = ('To overcome these limitations, this paper proposes a '
                   'multi-strategy secretary bird optimization algorithm '
                   '(MSSBOA) that integrates three improvement strategies.')
R1_ABSTRACT_NEW = (
    'To overcome these limitations, this paper proposes a multi-strategy '
    'secretary bird optimization algorithm (MSSBOA). The contribution is '
    'deliberately framed as a novel integration framework rather than as three '
    'new operators: three known families of operator are re-specified for the '
    'three-stage hunting/escape structure of SBOA and are coupled through '
    'problem-specific adaptations, namely a dynamic lens scaling factor that is '
    'derived from the convex-lens imaging geometry and tied to the iteration '
    'budget, iteration-adaptive Cauchy-Gaussian weights, and an application '
    'policy that confines refraction to the inferior subpopulation and mutation '
    'to the elite so that the two operators cannot interfere.')

R1_CONTRIB_OLD = ('(1) An improved SBOA variant, namely MSSBOA, is proposed by '
                  'integrating good point set initialization, lens '
                  'opposition-based learning and adaptive Cauchy–Gaussian '
                  'mutation.')
R1_CONTRIB_NEW = (
    '(1) A novel integration framework for SBOA, namely MSSBOA, is proposed. '
    'The three constituent operator families - good point set initialization, '
    'lens opposition-based learning and adaptive Cauchy-Gaussian mutation - are '
    'individually well established in the metaheuristic literature, and no '
    'claim of novelty is made for them as such. What is new is (i) the way each '
    'operator is re-specified for SBOA, (ii) the parameter adaptations that '
    'govern them - the dynamic lens factor k(t) of Equation (12) and the '
    'iteration-adaptive weights of Equation (14) - and (iii) the disjoint '
    'application policy that assigns refraction to the inferior subpopulation '
    'and mutation to the elite, which is what makes the three operators '
    'complementary rather than redundant. Section 3.6 states these differences '
    'against the existing applications of the same operators, and Section 4.3 '
    'quantifies the resulting interaction.')

# ---------------------------------------------------------------- Section 3.2
R1_LOBL_DERIVATION = [
    'Lens opposition-based learning replaces the reflection of standard '
    'opposition-based learning by the image that a thin convex lens forms of '
    'the current individual, and the derivation below makes the correspondence '
    'between the optical construction and Equation (11) explicit.',

    'Consider one coordinate axis of the search space, the j-th, restricted to '
    'the interval [lb_j, ub_j], and let o_j = (lb_j + ub_j)/2 denote its '
    'midpoint. In the optical analogy the midpoint plays the role of the '
    'optical centre: a thin convex lens is placed at o_j with its principal '
    'axis perpendicular to the coordinate axis, as illustrated in Figure 2a. '
    'The current individual is modelled as an object of height h whose base '
    'stands on the coordinate axis at x_j. The lens forms an inverted real '
    'image of height h* whose base stands at x*_j on the opposite side of the '
    'optical centre. The ray through the optical centre is undeviated, so the '
    'object triangle and the image triangle share an equal pair of vertically '
    'opposite angles at o_j and are therefore similar. Comparing the '
    'corresponding sides gives the single geometric relation on which the '
    'operator rests, h / h* = (x_j - o_j) / (o_j - x*_j).',

    'The tunable scaling factor k is defined as this ratio of object height to '
    'image height, k = h / h*. It is therefore not a free numerical constant '
    'but the reciprocal of the transverse magnification of the virtual lens, '
    'the one physical lens parameter that the operator exposes: k > 1 '
    'corresponds to a demagnifying lens and k = 1 to unit magnification. '
    'Substituting k into the similarity relation and solving for x*_j gives '
    'x*_j = o_j + (o_j - x_j)/k, which, after writing o_j out in terms of the '
    'bounds, is exactly Equation (11). Setting k = 1 recovers x*_j = lb_j + '
    'ub_j - x_j, that is, classical opposition-based learning, which confirms '
    'that the lens formulation contains standard opposition-based learning as '
    'the unit-magnification special case.',

    'The behaviour of the operator follows directly from the derivation. '
    'Equation (11) implies |x*_j - o_j| = |x_j - o_j| / k, so k controls the '
    'radius at which the refracted solution is placed about the midpoint of the '
    'interval. A small k produces a wide reversal that lands far from the '
    'current individual and probes the opposite side of the domain, which is '
    'the behaviour required early in the search; a large k contracts the image '
    'onto the neighbourhood of o_j, so that the refracted point becomes a '
    'fine-grained, low-variance probe of the central region rather than a large '
    'jump. Figure 2c plots this contraction ratio 1/k over the course of a run. '
    'We take the opportunity to correct a statement in the submitted version, '
    'which described a large k as keeping the refracted solution close to the '
    'current individual; as the derivation shows, a large k keeps the image '
    'close to the midpoint o_j, and it is the amplitude of the reversal, not '
    'the distance to the parent, that the factor controls.',
]

# Replaces the paragraph of the submitted version that (i) misstated what a
# large k does and (ii) said LOBL is applied to the worst 30%, which contradicts
# the N_min = 0.2N of Table 1 and of the sensitivity study.
R1_LOBL_CORRECTED = (
    'Accordingly, a small k in the early stage places the refracted solution '
    'far from the interval midpoint, on the opposite side of the domain from '
    'the current individual, which favours exploration; a large k in the later '
    'stage contracts the image onto the neighbourhood of the midpoint, which '
    'turns the operator into a fine-grained local probe and favours '
    'exploitation. In MSSBOA the lens opposition-based learning is applied only '
    'to the inferior individuals, that is, to the worst N_min = 0.2N members of '
    'the population, at the end of each iteration; the value 0.2N is the one '
    'selected by the grid search of Section 4.2. (The submitted version stated '
    'the threshold as 30% in this paragraph and in Algorithm 1, which '
    'contradicted the N_min = 0.2N given in Table 3 and used throughout the '
    'experiments; the 30% was a leftover from an earlier draft and has been '
    'corrected here and in Algorithm 1.) As illustrated in Figure 2, restricting '
    'the operator to the inferior subpopulation lets the population escape '
    'local optima while the greedy selection protects the elite individuals.')

R1_LOBL_KJUSTIFY = [
    'The functional form of Equation (12), k(t) = (1 + (t/T)^nu)^mu with '
    'nu = 1/2 and mu = 10, is fixed by three requirements and one grid search. '
    'The requirements are structural. First, k(0) = 1 for any nu and mu, so the '
    'operator begins the run as exact opposition-based learning and the '
    'refraction is at its most aggressive when the population is still '
    'uninformative. Second, k must increase monotonically so that the '
    'refraction radius contracts monotonically and the operator hands over from '
    'exploration to exploitation without oscillating. Third, k must grow by '
    'several orders of magnitude over a run, because the contraction ratio is '
    '1/k and a factor of only a few would leave the operator exploratory to the '
    'end; the exponent mu supplies that range cheaply, since k(T) = 2^mu.',

    'Given those constraints the two exponents are free, and they were selected '
    'empirically rather than derived. The root nu governs where the contraction '
    'happens: nu = 1 spreads it evenly over the run, whereas nu = 1/2 front-'
    'loads it, so that the aggressive reversal is concentrated in the early '
    'iterations during which the hunting strategy of SBOA is itself exploratory '
    '(Figure 2b). The power mu = 10 sets the terminal contraction at 1/k(T) = '
    '2^-10, which is small enough for the refracted point to act as a local '
    'probe but not so small that the operator degenerates into re-evaluating '
    'the midpoint. Table {k_table_no} reports a grid over both exponents on the '
    'CEC2017 suite; {k_conclusion}',
]

# ---------------------------------------------------------------- Section 3.6
R1_LOBL_KJUSTIFY_SHORT = (
    'Within those constraints the two exponents are free and were selected '
    'empirically rather than derived. The root governs where the contraction '
    'happens: a linear root spreads it evenly over the run, whereas a square '
    'root front-loads it, so the aggressive reversal is concentrated in the '
    'early iterations during which the hunting strategy of SBOA is itself '
    'exploratory (Figure 2b). The power sets the terminal contraction, which '
    'must be small enough for the refracted point to act as a local probe but '
    'not so small that the operator degenerates into re-evaluating the '
    'midpoint. Section 4.2 reports a grid over both exponents, including the '
    'constant that reduces the operator to plain opposition-based learning.')

R1_NOVELTY_HEADING = '3.6. Novelty of the proposed integration framework'
R1_NOVELTY_TEXT = [
    'The three operator families used above are established techniques, and '
    'their individual novelty is not claimed here. Good point set '
    'initialization has been applied to many swarm algorithms, lens '
    'opposition-based learning has been combined with, among others, sand cat '
    'swarm optimization and whale optimization, and Cauchy-Gaussian mutation is '
    'a standard device for rebalancing exploration and exploitation; a closely '
    'related combination of opposition-based learning with Cauchy mutation, '
    'velocity clamping and a mirror operator has recently been reported for the '
    'ideal gas molecular movement algorithm [81]. The contribution of this '
    'paper is therefore the integration framework: how each operator is '
    're-specified for SBOA, how its control parameter is adapted, and how the '
    'three are assigned to disjoint parts of the population so that they '
    'reinforce rather than duplicate one another. Table {novelty_table_no} '
    'states these differences explicitly against representative existing '
    'applications of the same operators.',

    'Three design decisions distinguish the present framework. First, the '
    'refraction and the mutation act on disjoint subsets: LOBL is applied only '
    'to the inferior individuals and ACGM only to the elite, so that the '
    'diversity-restoring operator can never displace the best solution and the '
    'intensification operator can never be wasted on individuals that the '
    'greedy selection is about to discard. Most existing applications apply '
    'opposition-based learning to the whole population and mutation to a '
    'randomly chosen individual, which lets the two interfere. Second, the lens '
    'factor is a schedule derived from the imaging geometry and tied to the '
    'iteration budget rather than a constant chosen by hand, and its two '
    'exponents are exposed and tuned (Section 4.2). Third, the operators are '
    'placed at the points of the SBOA iteration where its own three-stage '
    'hunting strategy is weakest: refraction is applied after the escape phase, '
    'when the population has just contracted towards the elite, and mutation is '
    'applied to the elite itself, which is the single individual that both '
    'SBOA phases depend on and that neither can perturb.',
]

# ---------------------------------------------------------------- Section 4.4
R1_WILCOXON_OLD = ('As shown in Table 7 and Figure 11, MSSBOA significantly '
                   'outperforms each comparison algorithm on the majority of '
                   'functions.')
R1_WILCOXON_BALANCED = [
    'The statistical picture deserves a more balanced reading than a count of '
    'wins. Against the weaker comparison algorithms the outcome is '
    'unambiguous - MSSBOA wins all 116 cases against the basic SBOA, GWO and '
    'SCA - but against the two strongest competitors it is not. MSSBOA loses '
    '15 of 116 cases to QIO and 15 of 116 to LSHADE, that is 12.9% of the '
    'comparisons in each case, and a further 18 and 19 cases respectively are '
    'statistically indistinguishable. Taken together, MSSBOA is significantly '
    'better than QIO on 71.6% of the cases and than LSHADE on 70.7%, so on '
    'roughly three cases in ten these two algorithms are at least as good as '
    'the proposed method. This is a real limitation and not a rounding error.',

    'Table {loss_table_no} breaks the losses down by function class, using the '
    'per-function ranks of Tables A5-A8. The losses are not distributed '
    'uniformly. Against QIO they concentrate on the composition functions '
    'F21-F30, which account for 8 of the 16 rank losses although composition '
    'functions supply only 40 of the 116 cases, and none occurs on a unimodal '
    'function. Against LSHADE the profile is the opposite: 10 of the 20 rank '
    'losses fall on the unimodal and simple multimodal functions F1-F10, which '
    'is consistent with the linear population size reduction and archive of '
    'LSHADE being particularly effective on landscapes with a single dominant '
    'basin. The pattern indicates a specific weakness rather than a general '
    'one: the elite-guided intensification of MSSBOA pays off on hybrid '
    'landscapes but is less effective when a problem has many equally deep '
    'basins whose relative depth only becomes apparent late in the run, which '
    'is precisely the structure of the CEC2017 composition functions.',

    'The dimensional trend confirms the concern raised in the limitations '
    'section. The mean rank gap between MSSBOA and QIO falls monotonically from '
    '2.103 at 30 dimensions to 1.103 at 100 dimensions, and the corresponding '
    'gap against RIME falls from 2.379 to 1.517, while the number of losses '
    'against QIO, RIME and LSHADE rises from 0, 0 and 3 at 30 dimensions to 7, '
    '6 and 6 at 100 dimensions. The advantage of MSSBOA is therefore real but '
    'shrinking in dimension, and the results should be read as establishing '
    'that MSSBOA is competitive with the best available algorithms at high '
    'dimension rather than that it dominates them.',
]

# ---------------------------------------------------------------- Section 5.1
R1_COLOR_SPACE = [
    'Colours are represented in the HSV space, and the choice is dictated by '
    'the objective rather than by convenience. Matsuda\'s harmonic templates, '
    'on which the harmony term is built, are defined as angular sectors on the '
    'hue wheel, so the model needs hue as an explicit cyclic coordinate; RGB '
    'has no such coordinate and CIE L*a*b* carries hue only implicitly as the '
    'argument of (a*, b*), which would make the sector membership test and the '
    'template rotation awkward and would prevent the arc distance of Equation '
    '(15) from being written in closed form. HSV also supplies the two '
    'quantities that the remaining terms need directly: saturation, which '
    'weights how much hue information a colour actually carries, and value, '
    'which supplies the tonal contrast. The decision variables are therefore '
    'the triples (h_i, s_i, v_i), i = 1, ..., K, with h_i in [0, 360), s_i in '
    '[0.2, 1] and v_i in [0.15, 1]; the lower bounds on saturation and value '
    'exclude the near-grey and near-black region in which hue is perceptually '
    'meaningless. Where a perceptually uniform measurement is required, the '
    'optimized palette is converted to CIE L*a*b* for reporting.',

    'The harmonic template is not learned from the data; it is selected, per '
    'candidate palette, from the fixed catalogue of Matsuda in the '
    'parameterization of Cohen-Or et al. [70,72]. Table {template_table_no} '
    'lists the seven chromatic templates, each of which consists of one or two '
    'sectors of fixed angular width whose relative offsets are fixed; the '
    'achromatic N-type template is excluded because it carries no hue '
    'information. A template may be rotated rigidly on the hue wheel by an '
    'arbitrary angle alpha, which is the only free parameter. For a given '
    'palette the disharmony energy of Equation (16) is minimized over the seven '
    'templates and over alpha, sampled on a 5-degree grid, and the '
    'best-fitting pair (template, alpha) is the one reported in Figure 12a. In '
    'other words, the template shown in that figure is an output of the '
    'evaluation, not an input chosen by the designer, which is what allows the '
    'same objective to score palettes of different harmonic families on a '
    'common scale.',
]

R1_COLOR_EQ_TEXT = (
    'A purely harmonic palette may collapse into nearly identical colours, so '
    'a hue diversity term is introduced by Equation (18) to encourage '
    'perceptually distinct colours, and a tonal-contrast term CON rewards a '
    'usable lightness spread. In Equation (18), DIV is the mean normalized '
    'pairwise arc distance of the K hues, so that DIV = 0 for a monochrome '
    'palette and DIV = 1 when every pair of hues is complementary; in the '
    'tonal-contrast term, CON = min(1, (max_i v_i - min_i v_i)/0.6) saturates '
    'once the palette spans 60% of the value range, which is the spread a '
    'palette needs before text set in one of its colours remains legible on '
    'another.')

R1_COLOR_OBJ_TEXT = (
    'The decision vector is the stacked palette P of dimension 3K, and the '
    'optimizer maximizes the aesthetic objective defined by Equation (19), '
    'f(P) = w_har HAR(P) + w_div DIV(P) + w_con CON(P), where HAR is the '
    'harmony term of Equation (17), DIV the diversity term of Equation (18) and '
    'CON the tonal-contrast term, and the weights w_har = 0.60, w_div = 0.25 '
    'and w_con = 0.15 sum to one. All three terms take values in [0, 1], so '
    'f(P) is in [0, 1] and the harmony score reported in Table 8 is 100 f(P) '
    'expressed as a percentage.')

# ---------------------------------------------------------------- Section 5.2
R1_WEIGHTS_TEXT = [
    'The weights of Equation (22) require comment, because they carry the '
    'designer\'s priorities into the objective. The values BM = 0.30, '
    'OV = 0.22, AL = 0.18, SY = 0.15 and DEN = 0.15 follow the relative '
    'importance that Ngo et al. [73] assign to their aesthetic measures, with '
    'balance dominant and the structural terms subordinate. They are not '
    'universal constants. Ngo et al. derived them from a specific corpus of '
    'screen interfaces, and there is no reason to expect the same ordering to '
    'hold for, say, a packaging label, where overlap is a hard production '
    'constraint rather than an aesthetic preference. They were not '
    'independently validated on the eight problems of Table 9; adopting them '
    'unchanged is a modelling choice, and it should be read as one.',
]

R1_LIMITATIONS = [
    'Nevertheless, MSSBOA has limitations, and it is worth separating those it '
    'inherits from SBOA from those that belong to this variant. Two of the '
    'three limitations noted in the submitted version are inherited. The '
    'empirical determination of control parameters is a property of SBOA and '
    'indeed of essentially every metaheuristic of this family; what is specific '
    'to MSSBOA is that the framework adds three further parameters - the LOBL '
    'subpopulation ratio, the mutation probability p_m and the two exponents of '
    'the lens schedule - so the tuning burden grows rather than changes in '
    'kind. Section 4.2 now reports the sensitivity of all of them, which shows '
    'that the ranking is flat near the adopted values, but a self-adaptive '
    'scheme in which p_m and the LOBL ratio respond to a measured diversity '
    'statistic would remove the burden altogether and is the natural next step.',

    'The weakening of the advantage at high dimension is likewise partly '
    'inherited, but Section 4.4 now shows that it has a MSSBOA-specific '
    'component. The mean rank gap against the strongest competitors contracts '
    'monotonically from 30 to 100 dimensions, and the losses concentrate on the '
    'composition functions. The mechanism is identifiable: both added search '
    'operators are elite-centred, and the fraction of the budget they consume '
    'is independent of dimension, so as D grows the same number of refractions '
    'and mutations has to cover a search space whose volume grows '
    'exponentially. A dimension-aware budget, in which the LOBL subpopulation '
    'or the mutation frequency scales with D, is a concrete remedy that we '
    'intend to test.',

    'The limitation that is genuinely specific to this variant concerns the '
    'lens operator itself. Equation (11) refracts about the midpoint of the '
    'static search interval, so the operator is most useful when the optimum is '
    'not close to the centre of the domain and becomes progressively less '
    'informative as k grows and the image contracts onto a fixed point that '
    'carries no information about where the population currently is. Replacing '
    'the static bounds by the per-dimension extrema of the current population, '
    'so that the optical centre tracks the population centroid, would make the '
    'late-stage refraction a genuine local operator; this is a change to '
    'Equation (11) and not merely to its parameters, and it is left to future '
    'work.',

    'Third, the aesthetic objectives used here are computational models. '
    'Neither the colour-harmony objective nor the layout objective has been '
    'validated against human judgements in this study, so the claim that MSSBOA '
    'produces better designs is, strictly, a claim that it optimizes these '
    'models better. The models are themselves well grounded - the harmonic '
    'templates come from Matsuda\'s scheme as formalized by Cohen-Or et al. '
    '[70,72], and the layout measures are those of Ngo et al. [73,75], which '
    'were calibrated against human ratings in their original studies - but that '
    'grounding transfers only as far as the models do. A controlled study in '
    'which trained designers and naive participants rank the generated palettes '
    'and layouts against baselines, with agreement measured against the '
    'computational scores, is a necessary complement to the present results and '
    'is planned as the next stage of this work.',

    'Finally, the two design problems studied here are offline: the objective '
    'is fixed before the search starts and the designer sees only the result. '
    'Interactive and real-time settings, in which a user supplies subjective '
    'feedback while the search runs, are a natural extension and the structure '
    'of MSSBOA is well suited to them, because a human evaluation budget is '
    'small and the framework is explicitly designed to spend few evaluations on '
    'the elite. Adapting it would mean replacing the analytic objective by a '
    'surrogate model fitted to accumulated user judgements, so that only a '
    'small number of candidates is ever shown to the user, and reducing the '
    'population and iteration budget accordingly; interactive genetic methods '
    'for colour matching in cultural-creative design [79,80] provide the '
    'protocol, and combining that protocol with the present framework is a '
    'direction we intend to pursue.',
]

R1_CONCL_FRAMING_OLD = ('Three improvement strategies were integrated into the '
                        'basic SBOA:')
R1_CONCL_FRAMING_NEW = (
    'The contribution is an integration framework rather than three new '
    'operators: three established operator families were re-specified for the '
    'three-stage hunting/escape structure of SBOA, given parameter adaptations '
    'tied to the iteration budget, and assigned to disjoint parts of the '
    'population, namely')

R1_DATA_AVAILABILITY = (
    'Data Availability Statement: The source code of MSSBOA, the '
    're-implementations of the comparison algorithms, the two design-problem '
    'formulations and all raw experimental results are openly available at '
    'https://github.com/caixinyu2017-star/xixi (directory work/mssboa-design), '
    'so that every table and figure in this paper can be reproduced.')

# =====================================================================
#  Reviewer 2 - blue
# =====================================================================
R2_WHY_SBOA = [
    'The choice of SBOA as the basis of this work deserves explicit '
    'justification, since a large number of metaheuristics could in principle '
    'have been improved instead. Three reasons motivated it. First, and most '
    'importantly, the structure of SBOA matches the structure of the design '
    'problems studied here. Aesthetic objectives such as Equations (19) and '
    '(22) are sums of competing terms whose trade-off surface has many broad, '
    'shallow optima rather than one sharp optimum, so an algorithm must survey '
    'widely before committing. SBOA is one of the few recent metaheuristics '
    'that splits its exploration phase into three explicitly time-gated stages '
    'with qualitatively different step distributions - a differential '
    'perturbation, a Brownian move towards the elite and a Levy flight - which '
    'gives a scheduled and inspectable progression from survey to commitment, '
    'and which provides well-defined points at which further operators can be '
    'inserted. Second, SBOA is economical: it has a single control parameter '
    'beyond the population size, so a study of added operators is not confounded '
    'by the tuning of the base algorithm. Third, SBOA is recent enough that its '
    'weaknesses are documented but not yet addressed for this problem class, '
    'and it has been shown competitive on standard suites [51], which makes it '
    'a meaningful baseline rather than a straw man.',
]

R2_VARIANTS_HEADING = '4.5. Comparison with recent SBOA variants and multi-strategy algorithms'
R2_VARIANTS_INTRO = [
    'Section 1 reviews several recent SBOA variants but the submitted version '
    'compared MSSBOA only with the basic SBOA, which is not sufficient to '
    'locate the proposed framework within the literature. This subsection '
    'therefore compares MSSBOA directly with three published SBOA variants and, '
    'following the suggestion of a reviewer, with two recent multi-strategy '
    'algorithms from outside the SBOA family. The SBOA variants are MISBOA '
    '[53], which adds incremental-PID feedback regulation and a co-operative '
    'camouflage strategy; CGSBOA [54], which fuses several strategies with a '
    'Cauchy-Gaussian crossover on the elite; and LTSBOA [55], which combines '
    'logistic-tent chaotic initialization with a crossover strategy. The two '
    'external methods are MS-TSA [82], a tree-seed algorithm with a '
    'self-adaptive weighting mechanism, chaotic elite learning and '
    'experience-based learning, and I-CPA [83], a carnivorous plant algorithm '
    'whose exploitation phase is strengthened by a teaching-factor strategy. '
    'The base algorithms TSA and CPA are included as well, so that the gain of '
    'each variant over its own base can be read off directly rather than '
    'assumed.',

    'The source codes of these methods are not publicly distributed, so each '
    'was re-implemented following the equations, control parameters and '
    'pseudo-code given in the corresponding publication; the implementations '
    'are released with this paper so that the comparison can be audited. All '
    'algorithms use the population size and evaluation budget of Section 4.1, '
    'and every algorithm is charged for every function evaluation it performs, '
    'including those consumed by auxiliary operators.',
]

# =====================================================================
#  Reviewer 3 - green
# =====================================================================
R3_ABLATION_INTRO = [
    'The submitted version isolated each strategy on its own, which shows that '
    'every strategy helps but not whether the three are complementary or '
    'partly redundant. To settle that question the ablation is extended here to '
    'the complete 2^3 factorial design: all eight combinations of the three '
    'strategies, from the basic SBOA to the full MSSBOA, are run under '
    'identical conditions. The factorial design allows the average main effect '
    'of each strategy to be separated from the interaction between them, and it '
    'is the interaction that determines whether combining the three is '
    'justified.',
]

R3_FIGURE_NOTE = (
    'Figures 4 and 5 have been redrawn. In the submitted version the annotation '
    'marking the best setting was placed below the corresponding point and was '
    'difficult to read; it is now placed above the point, enlarged, and set in '
    'a boxed callout with a leader line to the marker.')

# =====================================================================
#  Static tables
# =====================================================================
NOVELTY_TABLE = [
    ['Strategy', 'Typical existing application',
     'Implementation in MSSBOA', 'What differs'],
    ['Good point set initialization (GPSI)',
     'Applied to the whole initial population of a swarm algorithm to lower '
     'discrepancy; the prime p is usually fixed in advance [60].',
     'p is the smallest prime with p >= 2D + 3, recomputed for every problem '
     'dimension, and the set is generated once and passed unchanged to the '
     'three-stage hunting phase.',
     'Dimension-adaptive choice of p rather than a fixed prime, so the '
     'discrepancy bound holds at every dimension tested (10-100D) instead of '
     'only at the dimension the prime was chosen for.'],
    ['Lens opposition-based learning (LOBL)',
     'Applied to the whole population, or to a randomly chosen individual, '
     'usually with a constant scaling factor k, e.g. in sand cat swarm '
     'optimization [63] and whale optimization.',
     'Applied only to the inferior subpopulation (the worst N_min = 0.2N '
     'individuals) after the escape phase, with the scaling factor driven by '
     'the schedule of Equation (12).',
     'Restriction to the inferior subset means the elite is structurally '
     'protected, so refraction cannot undo intensification; and k is a derived '
     'schedule with two exposed exponents (Section 4.2) rather than a hand-set '
     'constant.'],
    ['Adaptive Cauchy-Gaussian mutation (ACGM)',
     'Applied to a randomly selected individual or to the whole population, '
     'often with fixed mixing weights, to rebalance exploration and '
     'exploitation [64].',
     'Applied only to the current elite, with probability p_m, using the '
     'iteration-adaptive weights lambda_1 = 1 - t^2/T^2 and lambda_2 = t^2/T^2 '
     'of Equation (14); the mutant replaces the worst individual when it '
     'improves the elite.',
     'The elite is the one individual that both SBOA phases read from and that '
     'neither can perturb, so mutating it is the targeted repair of a '
     'structural weakness of the base algorithm rather than a generic diversity '
     'injection; and the weights are tied to the iteration budget.'],
]

TEMPLATE_TABLE = [
    ['Template', 'Sectors (offset, angular width)', 'Harmonic relation'],
    ['i-type', '(0 deg, 18 deg)', 'monochromatic; one narrow hue band'],
    ['V-type', '(0 deg, 93.6 deg)', 'analogous; one broad hue band'],
    ['L-type', '(0 deg, 18 deg) and (90 deg, 79.2 deg)',
     'one narrow accent plus a broad band in quadrature'],
    ['I-type', '(0 deg, 18 deg) and (180 deg, 18 deg)',
     'complementary; two narrow opposite bands'],
    ['T-type', '(0 deg, 180 deg)', 'half of the hue wheel'],
    ['Y-type', '(0 deg, 93.6 deg) and (180 deg, 18 deg)',
     'broad band plus an opposite narrow accent'],
    ['X-type', '(0 deg, 93.6 deg) and (180 deg, 93.6 deg)',
     'two broad opposite bands'],
]


# =====================================================================
#  Repositioning the paper on the design contribution
#  (Reviewer 2, comment 2: "the novelty of the new algorithm is limited ...
#   but the application is interesting")
# =====================================================================

PIVOT_TITLE_OLD = ('A Multi-Strategy Secretary Bird Optimization Algorithm for '
                   'Aesthetic Color and Layout Optimization in Visual Art Design')
PIVOT_TITLE_NEW = ('Computational Aesthetics as an Optimization Problem: A '
                   'Reproducible Colour-Harmony and Graphic-Layout Formulation '
                   'and a Benchmark of Bio-Inspired Optimizers')

PIVOT_ABSTRACT = (
    'Visual art and graphic design tasks such as choosing a harmonious colour '
    'palette or arranging the elements of a page can be posed as optimization '
    'problems, but the objective functions that make this possible are rarely '
    'stated in full, which makes results difficult to reproduce and impossible '
    'to compare across papers. This article contributes, first, a complete and '
    'openly implemented formulation of two such problems: an aesthetic '
    'colour-harmony objective built on Matsuda\'s harmonic templates in the '
    'parameterization of Cohen-Or et al., in which the best-fitting template '
    'and its rotation are outputs of the evaluation rather than inputs chosen '
    'by the designer; and a graphic-layout objective built on the quantitative '
    'aesthetic measures of Ngo et al. Every variable, the colour space and the '
    'reason for choosing it, and every weight are specified. Second, it uses '
    'that formulation as a testbed: eleven bio-inspired and evolutionary '
    'optimizers, including the recent secretary bird optimization algorithm '
    '(SBOA) and a multi-strategy variant of it (MSSBOA) developed here, are '
    'compared on the two design problems and on the CEC2017 suite under an '
    'identical evaluation budget, with every auxiliary function evaluation '
    'charged to that budget. Third, it reports how far the conclusions depend '
    'on the modelling choices, through a sensitivity analysis over the '
    'aesthetic weight vector and a scalability study that extends the layout '
    'problem from six to thirty elements. The emphasis throughout is on '
    'reproducibility: the objectives, the optimizers, the raw results and the '
    'analysis scripts are all released.')

PIVOT_CONTRIBUTIONS = [
    '(1) Two visual-design optimization problems are formulated completely and '
    'released as executable code. For colour harmony, the hue-wheel geodesic, '
    'the saturation-weighted disharmony energy over the seven chromatic '
    'templates of Matsuda, the hue-diversity term and the tonal-contrast term '
    'are each given in closed form, and the choice of the HSV space is argued '
    'from the structure of the objective rather than asserted. For graphic '
    'layout, the balance, non-overlap, alignment, symmetry and density '
    'measures of Ngo et al. are specified together with the canvas penalty. '
    'Stating these models in full is the prerequisite for anyone else to '
    'reproduce or contest the results, and it is the gap this paper is '
    'primarily meant to close.',

    '(2) The two problems are used to benchmark eleven optimizers, which to '
    'our knowledge is the first comparison of this breadth on explicitly '
    'stated computational-aesthetics objectives. The study includes a '
    'multi-strategy SBOA variant (MSSBOA) that integrates good point set '
    'initialization, lens opposition-based learning and an adaptive '
    'Cauchy-Gaussian mutation, and the same protocol is applied to the '
    'CEC2017 suite so that behaviour on the design problems can be read '
    'against behaviour on a standard suite. Results are reported as measured, '
    'including where the proposed variant does not lead.',

    '(3) The robustness of the conclusions to the modelling choices is '
    'quantified. The aesthetic weight vector of Equation (22) is varied over '
    'five configurations and the resulting orderings of the algorithms are '
    'compared by rank correlation; the layout problem is scaled from six to '
    'thirty elements, that is from twelve to sixty decision variables, to '
    'establish that neither the formulation nor the optimizers break down at '
    'realistic design sizes.',
]

PIVOT_SECTION4_INTRO = (
    'The purpose of this section is not to establish that any one algorithm is '
    'universally superior, which the no free lunch theorem forbids in any case, '
    'but to answer a practical question for the design problems of Section 5: '
    'given a fixed evaluation budget, which class of optimizer should a '
    'practitioner reach for, and does behaviour on a standard suite predict '
    'behaviour on an aesthetic objective? The CEC2017 suite is used because it '
    'is standard, its function classes are well characterized, and its results '
    'can be compared with the wider literature. Every algorithm is charged for '
    'every function evaluation it performs, including those consumed by '
    'auxiliary operators, and all results below are reported as measured.')

PIVOT_SECTION5_INTRO = (
    'This section presents the main contribution of the paper: two visual-design '
    'problems stated completely enough to be reproduced, and what happens when '
    'a representative set of optimizers is applied to them. Both are formulated '
    'as continuous maximization problems over a fixed evaluation budget, and '
    'both are released as executable code together with the raw results. '
    'Interestingly, both the optimizers considered here and the colour-harmony '
    'objective itself are bio-inspired: the harmonic templates formalize '
    'regularities first catalogued in natural colour schemes, which makes the '
    'pairing a natural one for biomimetic design.')

PIVOT_CONCLUSION_OPEN = (
    'This paper set out to make two computational-aesthetics problems '
    'reproducible and then to use them as a testbed. The colour-harmony and '
    'graphic-layout objectives are stated in full - every term, every variable, '
    'the colour space and the reason for it, and the provenance of the harmonic '
    'templates - and are released as executable code alongside the raw results '
    'of every run reported here. A multi-strategy variant of the secretary bird '
    'optimization algorithm was developed in the course of the study and is '
    'included in the comparison.')

PIVOT_CONCLUSION_HONEST = (
    'We want to be explicit about what the benchmark does and does not show. '
    'The three strategies integrated into MSSBOA are individually well '
    'established, and under the fair-budget protocol used here they do not '
    'produce a statistically significant improvement over the basic SBOA on the '
    'CEC2017 suite. We report this rather than omit it, because a negative '
    'result obtained under a stated protocol is more useful to the field than '
    'an unreproducible positive one, and because the released code allows the '
    'measurement to be checked. The value of the study lies in the formulation '
    'and the comparison rather than in the variant.')

PIVOT_FUTURE = (
    'Two directions follow naturally. The first is perceptual validation: the '
    'objectives used here are computational models, and although the harmonic '
    'templates and the layout measures were each calibrated against human '
    'judgements in the studies that introduced them, that grounding transfers '
    'only as far as the models do. A controlled experiment in which trained '
    'designers and naive participants rank generated palettes and layouts, with '
    'agreement measured against the computational scores, is the necessary next '
    'step and is planned. The second is interactive design: the problems studied '
    'here are offline, whereas a designer in practice supplies subjective '
    'feedback while the search runs. Replacing the analytic objective by a '
    'surrogate fitted to accumulated user judgements, so that only a few '
    'candidates are ever shown, would adapt the present framework to that '
    'setting; the interactive genetic protocols for colour matching in '
    'cultural-creative design provide the experimental design.')
