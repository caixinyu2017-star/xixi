"""Paper B full manuscript content.

Title: An Enhanced Multi-Strategy Black-Winged Kite Algorithm for Global
Optimization and Customer Segmentation in Marketing Management
"""
from content_paperA import resolve_refs, set_refs, REF_RE  # shared helpers

FIGS = '/home/user/xixi/work/figs'

TITLE = ('An Enhanced Multi-Strategy Black-Winged Kite Algorithm for Global '
         'Optimization and Customer Segmentation in Marketing Management')

AUTHORS = [('Xinyu Cai ', False), ('1,', True), ('*', True)]

AFFILIATIONS = [
    '{sup:1}\tCollege of Business, Jiaxing University, Jiaxing 314001, China; caixinyu@zjxu.edu.cn',
    '*\tCorrespondence: caixinyu@zjxu.edu.cn',
]

KEYWORDS = ('black-winged kite algorithm; metaheuristic algorithm; tent chaotic mapping; '
            'fitness-distance balance; Cauchy-Gaussian mutation; customer segmentation; '
            'clustering; marketing management')


def abstract(st):
    return (
        'Customer segmentation is a fundamental task in marketing management, and its mainstream '
        'implementation, centroid-based clustering, is essentially a non-convex optimization problem that '
        'is highly sensitive to initial conditions. Metaheuristic algorithms provide an effective way to '
        'overcome this difficulty. The black-winged kite algorithm (BKA) is a recently proposed '
        'nature-inspired metaheuristic simulating the attacking and migration behaviors of black-winged '
        'kites. Although BKA exhibits competitive performance, it still suffers from the uneven random '
        'initialization, the self-referential attacking update that lacks information exchange among '
        'individuals, and the excessive attraction of the leader that causes premature convergence. To '
        'address these issues, this paper proposes an enhanced multi-strategy black-winged kite algorithm '
        '(MSBKA) integrating three improvement strategies: a tent chaotic mapping initialization strategy '
        'that generates a diverse and uniformly distributed initial population, a fitness-distance balance '
        'based companion selection strategy that replaces the purely random companion in the migration '
        'phase and coordinates exploitation and exploration, and an adaptive Cauchy-Gaussian hybrid '
        'mutation strategy that perturbs the leader with heavy-tailed steps in the early stage and fine '
        'Gaussian steps in the later stage. MSBKA was evaluated on the CEC2022 test suite in 10 and 20 '
        'dimensions against the basic BKA and eight representative algorithms, and the experimental '
        'results were analyzed by the Friedman test and the Wilcoxon rank-sum test. MSBKA obtains the '
        f'best overall average ranking of {st["frd20_best"]:.3f} in 20 dimensions, and the ablation '
        'experiments confirm the contribution of every strategy. Furthermore, MSBKA was applied to '
        'customer segmentation on two real-world business datasets, the mall customers dataset and the '
        'wholesale customers dataset. Compared with the classical K-means algorithm and eight '
        'metaheuristic competitors, MSBKA achieves the lowest intra-cluster sum of squared errors with '
        'the smallest variance across independent runs, and the resulting segments provide clear '
        'managerial insights for differentiated marketing strategies.'
    )


def blocks(st):
    B = []
    ap = B.append

    # ============================ 1. Introduction ============================
    ap({'h1': '1. Introduction'})
    ap({'p': (
        'In the era of digital economy, enterprises accumulate massive customer behavior data, and how to '
        'transform these data into actionable marketing knowledge has become a core issue of modern '
        'marketing management {ref:smith_seg,wedel}. Customer segmentation, which divides a heterogeneous '
        'customer base into relatively homogeneous groups, is the premise of market positioning, precision '
        'marketing, and customer relationship management {ref:rfm_paper}. The most widely used technical '
        'route of customer segmentation is centroid-based clustering represented by the K-means algorithm '
        '{ref:macqueen,jain_clust}. However, minimizing the intra-cluster sum of squared errors is a '
        'non-convex NP-hard optimization problem. The classical K-means algorithm is essentially a local '
        'search procedure that strongly depends on the initial centroids, so it frequently converges to '
        'poor local optima and yields unstable segmentation schemes, even when the improved seeding '
        'method K-means++ is adopted {ref:kmeanspp}. An unstable segmentation directly misleads the '
        'formulation of marketing strategies. Therefore, employing global optimization techniques to '
        'search the cluster centroids has attracted increasing attention, and metaheuristic algorithms '
        'have proven to be one of the most effective tools for this purpose {ref:pso_clust,josegarcia}.'
    )})
    ap({'p': (
        'Metaheuristic algorithms are stochastic search techniques inspired by natural evolution, swarm '
        'intelligence, physical phenomena, mathematical rules, or human behaviors {ref:gwo,nfl}. They do '
        'not require gradient information or convexity assumptions, and can achieve a reasonable balance '
        'between global exploration and local exploitation through population-based probabilistic '
        'operators. According to the source of inspiration, existing metaheuristics can be roughly '
        'divided into five categories, as illustrated in Figure 1: evolution-based algorithms such as the '
        'genetic algorithm (GA) {ref:ga}, differential evolution (DE) {ref:de}, and the advanced LSHADE '
        '{ref:lshade}; swarm-based algorithms such as particle swarm optimization (PSO) {ref:pso}, ant '
        'colony optimization (ACO) {ref:aco}, the grey wolf optimizer (GWO) {ref:gwo}, the whale '
        'optimization algorithm (WOA) {ref:woa}, Harris hawks optimization (HHO) {ref:hho}, the sparrow '
        'search algorithm (SSA) {ref:ssa}, the dung beetle optimizer (DBO) {ref:dbo}, and the crayfish '
        'optimization algorithm (COA) {ref:coa}; physics-based algorithms such as the multi-verse '
        'optimizer (MVO) {ref:mvo}, the equilibrium optimizer (EO) {ref:eo}, and the RIME algorithm '
        '{ref:rime}; mathematics-based algorithms such as the sine cosine algorithm (SCA) {ref:sca} and '
        'the arithmetic optimization algorithm (AOA) {ref:aoa}; and human-based algorithms such as '
        'teaching-learning-based optimization (TLBO) {ref:tlbo}. Nevertheless, the no free lunch theorem '
        '{ref:nfl} reveals that no algorithm can be universally optimal for all problems, which '
        'continuously drives researchers to design new algorithms and improve existing ones for specific '
        'problem classes.'
    )})
    ap({'fig': f'{FIGS}/classification.png',
        'caption': '**Figure 1.** Classification of metaheuristic algorithms.',
        'width_cm': 14.5})
    ap({'p': (
        'The black-winged kite algorithm (BKA) is a novel swarm-based metaheuristic proposed by Wang et '
        'al. in 2024 {ref:bka}, which mathematically models the hovering-diving attack behavior and the '
        'leader-following migration behavior of black-winged kites. BKA has the advantages of a simple '
        'structure, few parameters, and fast convergence, and has been rapidly adopted and improved. For '
        'example, Zhang et al. fused BKA with the osprey optimization algorithm for engineering '
        'applications {ref:ibka1}; Li et al. enhanced BKA with vertical and horizontal crossover '
        '{ref:ibka2}; Mansouri et al. developed a chaotic-map-based modified BKA for real-world global '
        'optimization {ref:ibka3}; and BKA has also been used to optimize variational mode decomposition '
        'for industrial power load prediction {ref:ibka4} and to size hybrid renewable energy systems '
        '{ref:ibka5}. However, a careful analysis of the basic BKA exposes three '
        'deficiencies when it faces complex optimization landscapes. First, the initial population is '
        'generated by uniform random sampling, whose uneven coverage weakens the diversity at the '
        'beginning of the search. Secondly, in the attacking phase, each individual updates its position '
        'only by scaling its own coordinates with random factors. This self-referential update carries '
        'out no information exchange among individuals, so the global exploration ability is limited. '
        'Finally, in the migration phase, the comparison individual is selected completely at random and '
        'the update is strongly attracted by the leader. Once the leader falls into a local optimum, the '
        'population converges prematurely and the segmentation quality deteriorates.'
    )})
    ap({'p': (
        'To overcome the above shortcomings, this paper proposes an enhanced multi-strategy black-winged '
        'kite algorithm (MSBKA) that integrates three improvement strategies. First, a tent chaotic '
        'mapping initialization strategy (TCM) {ref:tent_paper} exploits the ergodicity and randomness of '
        'the tent map to generate a uniformly distributed initial population. Secondly, a '
        'fitness-distance balance based companion selection strategy (FDB) {ref:fdb} is embedded into the '
        'migration phase. By comprehensively scoring each individual with its normalized fitness and its '
        'normalized distance to the leader, FDB selects the most instructive companion instead of a '
        'purely random one, which coordinates the transition between exploitation and exploration and '
        'makes full use of the effective information of the population. Finally, an adaptive '
        'Cauchy-Gaussian hybrid mutation strategy (CGM) {ref:cgm_paper} perturbs the leader in every '
        'iteration, in which the weight of the heavy-tailed Cauchy component decreases and that of the '
        'Gaussian component increases with the iterations, helping the algorithm escape from local '
        'optima in the early stage and refine the solution in the later stage. The main contributions of '
        'this paper are as follows.'
    )})
    ap({'p': '(1) An enhanced BKA variant, called MSBKA, is proposed by integrating the tent chaotic '
             'mapping initialization, the fitness-distance balance based companion selection, and the '
             'adaptive Cauchy-Gaussian hybrid mutation into the basic BKA.', 'style': 'MDPI_3.1_text'})
    ap({'p': '(2) The performance of MSBKA is systematically evaluated on the CEC2022 test suite in 10 '
             'and 20 dimensions. Ablation experiments confirm the effectiveness of each strategy, and '
             'the superiority over nine algorithms is verified by the Friedman test and the Wilcoxon '
             'rank-sum test.', 'style': 'MDPI_3.1_text'})
    ap({'p': '(3) MSBKA is applied to the customer segmentation problem on two real business datasets, '
             'and the managerial implications of the obtained segments are analyzed, which demonstrates '
             'the practical value of MSBKA in marketing management.', 'style': 'MDPI_3.1_text'})
    ap({'p': (
        'The remainder of this paper is organized as follows. Section 2 introduces the mathematical model '
        'of the basic BKA. Section 3 elaborates the three improvement strategies and the framework of '
        'MSBKA, and analyzes its computational complexity. Section 4 reports the numerical experiments on '
        'the CEC2022 test suite. Section 5 formulates the customer segmentation problem, describes the '
        'two business datasets, and discusses the experimental results and managerial insights. Section 6 '
        'concludes this paper and points out future research directions.'
    )})

    # ============================ 2. BKA ============================
    ap({'h1': '2. Black-Winged Kite Algorithm'})
    ap({'p': (
        'The black-winged kite is a small raptor with distinctive hovering hunting skills. BKA {ref:bka} '
        'abstracts two behaviors of black-winged kites into mathematical models: the attacking behavior, '
        'in which the kite hovers to observe and then dives rapidly to strike its prey, and the migration '
        'behavior, in which the population dynamically follows a leader to migrate. The details of BKA '
        'are described as follows.'
    )})
    ap({'h2': '2.1. Initialization'})
    ap({'p': 'BKA randomly generates $N$ individuals in the feasible space at the initial stage, as '
             'expressed in Equation (1).'})
    ap({'eq': r'X_{i,j}=lb_j+rand\times \left( ub_j-lb_j \right),\ \ i=1,2,\ldots ,N,\ \ j=1,2,\ldots ,D', 'num': 1})
    ap({'p': (
        'where $X_{i,j}$ is the position of the $i$th black-winged kite in the $j$th dimension, $rand$ is '
        'a uniform random number in [0, 1], and $lb_j$ and $ub_j$ denote the lower and upper bounds of '
        'the $j$th dimension. After evaluating the fitness of all individuals, the best individual is '
        'selected as the leader $L$.'
    )})
    ap({'h2': '2.2. Attacking Behavior'})
    ap({'p': (
        'Black-winged kites adjust the angles of their wings and tails according to the wind speed during '
        'flight, hover to observe the prey, and then strike with a quick dive. BKA models the hovering '
        'and diving states by Equation (2), and the attacking intensity factor $n$ is defined in '
        'Equation (3).'
    )})
    ap({'eq': r'y_{t+1}^{i,j}=\begin{cases} y_{t}^{i,j}+n\times \left( 1+\sin r \right)\times y_{t}^{i,j}, & p<r \\ y_{t}^{i,j}\times \left( n\times \left( 2\times rand-1 \right)+1 \right), & \mathrm{else} \end{cases}', 'num': 2})
    ap({'eq': r'n=0.05\times \exp \left( -2\times \left( \frac{t}{T} \right)^{2} \right)', 'num': 3})
    ap({'p': (
        'where $y_t^{i,j}$ denotes the position of the $i$th kite in the $j$th dimension at iteration '
        '$t$, $r$ and $rand$ are uniform random numbers in [0, 1], $p=0.9$ is the switching threshold, '
        '$t$ is the current iteration, and $T$ is the maximum number of iterations. The first branch '
        'simulates the rapid dive toward the prey, while the second branch simulates the fine adjustment '
        'in the hovering state.'
    )})
    ap({'h2': '2.3. Migration Behavior'})
    ap({'p': (
        'Bird migration is a complex group behavior. BKA hypothesizes that if the fitness of the current '
        'individual is better than that of a randomly selected individual, the current individual is '
        'qualified to explore away from the leader; otherwise, it should follow the leader. The '
        'migration update is defined in Equations (4) and (5).'
    )})
    ap({'eq': r'y_{t+1}^{i,j}=\begin{cases} y_{t}^{i,j}+C\left( 0,1 \right)\times \left( y_{t}^{i,j}-L_{t}^{j} \right), & F_i<F_{ri} \\ y_{t}^{i,j}+C\left( 0,1 \right)\times \left( L_{t}^{j}-m\times y_{t}^{i,j} \right), & \mathrm{else} \end{cases}', 'num': 4})
    ap({'eq': r'm=2\times \sin \left( r+\frac{\pi }{2} \right)', 'num': 5})
    ap({'p': (
        'where $L_t^j$ is the position of the leader in the $j$th dimension at iteration $t$, $F_i$ is '
        'the fitness of the current individual, $F_{ri}$ is the fitness of a randomly selected '
        'individual, and $C(0,1)$ denotes the standard Cauchy random number. The probability density '
        'function of the standard Cauchy distribution and its sampling formula are given in Equations '
        '(6) and (7).'
    )})
    ap({'eq': r'f\left( x \right)=\frac{1}{\pi }\times \frac{1}{x^{2}+1},\ \ -\infty <x<+\infty', 'num': 6})
    ap({'eq': r'C\left( 0,1 \right)=\tan \left( \left( u-0.5 \right)\times \pi  \right),\ \ u\sim U\left( 0,1 \right)', 'num': 7})
    ap({'p': 'After the attacking and migration updates, BKA adopts the greedy selection in Equation (8) '
             'to determine whether the new position is retained.'})
    ap({'eq': r'X_{i}^{t+1}=\begin{cases} X_{i}^{new}, & f\left( X_{i}^{new} \right)<f\left( X_{i}^{t} \right) \\ X_{i}^{t}, & \mathrm{otherwise} \end{cases}', 'num': 8})

    # ============================ 3. MSBKA ============================
    ap({'h1': '3. Proposed Enhanced Multi-Strategy Black-Winged Kite Algorithm'})
    ap({'p': (
        'This section develops the MSBKA algorithm. The tent chaotic mapping initialization strategy, '
        'the fitness-distance balance based companion selection strategy, and the adaptive '
        'Cauchy-Gaussian hybrid mutation strategy are elaborated in turn, followed by the overall '
        'framework and the complexity analysis.'
    )})
    ap({'h2': '3.1. Tent Chaotic Mapping Initialization Strategy (TCM)'})
    ap({'p': (
        'Chaotic sequences possess the characteristics of ergodicity, randomness, and sensitivity to '
        'initial values, and have been widely used to strengthen the initial population of metaheuristic '
        'algorithms {ref:tent_paper}. Compared with the logistic map whose distribution is dense near '
        'the two ends of the interval, the tent map produces a nearly uniform distribution over [0, 1] '
        'and therefore provides better space-filling capability. The tent map is defined in Equation '
        '(9), and the chaotic variables are mapped into the search space by Equation (10).'
    )})
    ap({'eq': r'z_{k+1}=\begin{cases} z_k/a, & 0\le z_k<a \\ \left( 1-z_k \right)/\left( 1-a \right), & a\le z_k\le 1 \end{cases}', 'num': 9})
    ap({'eq': r'X_{i,j}=lb_j+z_{i,j}\times \left( ub_j-lb_j \right)', 'num': 10})
    ap({'p': (
        'where the control parameter $a$ is set to 0.7 in this paper. Figure 2 compares the initial '
        'populations generated by random sampling and by the tent chaotic mapping in a two-dimensional '
        'space with 100 individuals. It is obvious that the chaotic population spreads over the space '
        'more evenly, which improves the probability of covering the region of the global optimum and '
        'provides a better starting point for the subsequent search.'
    )})
    ap({'fig': f'{FIGS}/tent_vs_random.png',
        'caption': '**Figure 2.** Population distributions of random initialization and tent chaotic '
                   'mapping initialization.', 'width_cm': 12.5})
    ap({'h2': '3.2. Fitness-Distance Balance Based Companion Selection Strategy (FDB)'})
    ap({'p': (
        'In the migration phase of the basic BKA, the comparison individual is chosen from the '
        'population completely at random, and the direction of the position update depends only on the '
        'leader. This mechanism has two drawbacks: the random companion may provide meaningless '
        'comparison information, and the single attraction of the leader accelerates the loss of '
        'population diversity. The fitness-distance balance selection method proposed by Kahraman et '
        'al. {ref:fdb} scores every individual by jointly considering its solution quality and its '
        'positional novelty, and has been verified to effectively improve the search performance of '
        'various metaheuristics. In MSBKA, the FDB score of each individual is calculated by Equations '
        '(11) and (12).'
    )})
    ap({'eq': r'd_i=\left\| X_i-L \right\|=\sqrt{\sum_{j=1}^{D}{\left( x_{i,j}-L_j \right)^{2}}}', 'num': 11})
    ap({'eq': r'S_i=\left( 1-\frac{F_i-F_{\min }}{F_{\max }-F_{\min }} \right)+\frac{d_i}{d_{\max }}', 'num': 12})
    ap({'p': (
        'where $d_i$ is the Euclidean distance between individual $i$ and the leader $L$, and $F_{min}$ '
        'and $F_{max}$ are the minimum and maximum fitness of the current population. The first term of '
        '$S_i$ rewards high solution quality and the second term rewards positional novelty, so an '
        'individual with a high score is both informative and diverse. The companion of the migration '
        'phase is then selected by the roulette wheel over the FDB scores, as shown in Equation (13).'
    )})
    ap({'eq': r'P_i=\frac{S_i}{\sum_{k=1}^{N}{S_k}},\ \ i=1,2,\ldots ,N', 'num': 13})
    ap({'p': (
        'Furthermore, when the current individual is better than the FDB companion, MSBKA lets it '
        'explore away from the companion rather than from the leader, and an annealing factor is '
        'introduced to gradually shrink this exploratory step, as expressed in Equation (14).'
    )})
    ap({'eq': r'y_{t+1}^{i,j}=\begin{cases} y_{t}^{i,j}+\left( 1-\frac{t}{T} \right)\times C\left( 0,1 \right)\times \left( y_{t}^{i,j}-x_{fdb,j}^{t} \right), & F_i<F_{fdb} \\ y_{t}^{i,j}+C\left( 0,1 \right)\times \left( L_{t}^{j}-m\times y_{t}^{i,j} \right), & \mathrm{else} \end{cases}', 'num': 14})
    ap({'p': (
        'where $x_{fdb}^t$ and $F_{fdb}$ are the position and fitness of the FDB-selected companion. '
        'Figure 3a illustrates the FDB scoring mechanism. In the early stage, individuals far from the '
        'leader with decent quality obtain high scores, which drives a wide exploration; in the later '
        'stage, as the population converges, the fitness term dominates and the search naturally '
        'switches to exploitation. In this way, FDB realizes a coordinated transition between '
        'exploration and exploitation.'
    )})
    ap({'h2': '3.3. Adaptive Cauchy-Gaussian Hybrid Mutation Strategy (CGM)'})
    ap({'p': (
        'The leader plays a decisive role in BKA, but the basic algorithm provides no mechanism to '
        'rescue the leader once it is trapped in a local optimum. Inspired by the mutation operators in '
        'the literature {ref:cgm_paper}, an adaptive Cauchy-Gaussian hybrid mutation is applied to the '
        'leader in every iteration, as defined in Equations (15) and (16).'
    )})
    ap({'eq': r'L_{new}=L\times \left( 1+0.1\times \lambda _1\times C\left( 0,1 \right)+0.1\times \lambda _2\times G\left( 0,1 \right) \right)', 'num': 15})
    ap({'eq': r'\lambda _1=1-\left( \frac{t}{T} \right)^{2},\ \ \lambda _2=\left( \frac{t}{T} \right)^{2}', 'num': 16})
    ap({'p': (
        'where $C(0,1)$ and $G(0,1)$ are random vectors sampled from the standard Cauchy distribution '
        'and the standard Gaussian distribution, respectively. As shown in Figure 3b, the Cauchy '
        'distribution has a heavier tail than the Gaussian distribution, so it can generate large jumps '
        'with a higher probability. At the beginning of the search, $\\lambda_1$ is close to 1 and the '
        'mutation is dominated by the Cauchy component, which endows the leader with a strong ability '
        'to escape from local optima. As the iteration proceeds, $\\lambda_2$ gradually dominates and '
        'the mutation degenerates into a small Gaussian perturbation, which supports the fine '
        'exploitation around the promising region. If the mutated leader is better than the original '
        'one, it replaces the worst individual of the population, which supplements the population '
        'diversity without destroying the elite information.'
    )})
    ap({'fig': f'{FIGS}/sketch_fdb.png',
        'caption': '**Figure 3.** Schematic diagrams of the FDB companion selection and the adaptive '
                   'Cauchy-Gaussian mutation.', 'width_cm': 13.5})
    ap({'h2': '3.4. The Framework of MSBKA'})
    ap({'p': (
        'By embedding the three strategies into the basic framework, the MSBKA algorithm is obtained. '
        'TCM acts on the initialization, FDB reshapes the migration phase, and CGM refreshes the leader '
        'at the end of each iteration. The three strategies focus on different stages and cooperate '
        'with each other: TCM improves the starting quality, FDB enhances the information utilization '
        'during the search, and CGM guarantees the vitality of the elite in the whole process. The '
        'pseudo-code of MSBKA is given in Algorithm 1, and Figure 4 shows the flowchart.'
    )})
    ap({'algorithm': {'title': 'Algorithm 1 Enhanced Multi-Strategy Black-Winged Kite Algorithm (MSBKA)',
        'lines': [
            '1: Initialize the population $X$ with the TCM strategy using Equations (9)–(10)',
            '2: Evaluate the fitness of all individuals; determine the leader $L$; set $FEs=N$',
            '3: **while** $FEs<MaxFEs$ **do**',
            '4:  Calculate the FDB scores and selection probabilities using Equations (11)–(13)',
            '5:  **for** $i=1$ to $N$ **do**  //attacking behavior',
            '6:   Update $y_{t+1}^{i,j}$ using Equations (2)–(3)',
            '7:   Evaluate the new position; apply greedy selection using Equation (8); $FEs=FEs+1$',
            '8:  **end for**',
            '9:  **for** $i=1$ to $N$ **do**  //migration behavior with FDB',
            '10:   Select the companion by roulette wheel using Equation (13)',
            '11:   Update $y_{t+1}^{i,j}$ using Equation (14)',
            '12:   Evaluate the new position; apply greedy selection using Equation (8); $FEs=FEs+1$',
            '13:  **end for**',
            '14:  Generate $L_{new}$ with the CGM strategy using Equations (15)–(16)  //CGM',
            '15:  **if** $f(L_{new})<f(L)$ **then** replace the worst individual with $L_{new}$; $FEs=FEs+1$',
            '16: **end while**',
            '17: **return** the best solution',
        ]}})
    ap({'fig': f'{FIGS}/flow_msbka.png',
        'caption': '**Figure 4.** Flowchart of the proposed MSBKA.', 'width_cm': 11.0})
    ap({'h2': '3.5. Computational Complexity Analysis of MSBKA'})
    ap({'p': (
        'Let $N$ be the population size, $D$ the dimensionality, and $T$ the maximum number of '
        'iterations. The basic BKA evaluates each individual twice per iteration, so its time '
        'complexity is $O(2\\times N\\times D\\times T)$, simplified as $O(N\\times D\\times T)$. In '
        'MSBKA, the TCM strategy only changes the initialization rule with the cost $O(N\\times D)$; '
        'the FDB strategy calculates the distances and scores once per iteration with the cost '
        '$O(N\\times D+N)$, which does not change the order of the main loop; and the CGM strategy '
        'introduces one extra evaluation per iteration with the cost $O(D\\times T)$ in total. '
        'Therefore, the time complexity of MSBKA remains $O(N\\times D\\times T)$, which is of the same '
        'order as the basic BKA. The space complexity is dominated by the population matrix, namely '
        '$O(N\\times D)$, identical to that of the basic BKA.'
    )})
    return B


def blocks_experiments(st):
    B = []
    ap = B.append

    # ============================ 4. CEC2022 experiments ============================
    ap({'h1': '4. Numerical Experiments Using the CEC2022 Test Suite'})
    ap({'p': (
        'This section evaluates the optimization performance of MSBKA on the CEC2022 test suite '
        '{ref:cec2022}. Section 4.1 describes the experimental settings. Section 4.2 reports the '
        'ablation experiments of the three strategies. Section 4.3 presents the comparison with nine '
        'algorithms together with the statistical analysis.'
    )})
    ap({'h2': '4.1. Experimental Settings and Performance Metrics'})
    ap({'p': (
        'The CEC2022 test suite consists of 12 benchmark functions with challenging characteristics, '
        'where F1 is a unimodal function, F2–F5 are basic multimodal functions, F6–F8 are hybrid '
        'functions, and F9–F12 are composition functions. The experiments were carried out in 10 and 20 '
        'dimensions with the search range $[-100,100]^D$. The maximum number of function evaluations '
        'was adopted as the unified stopping criterion and set to $1000\\times D$, namely 10,000 for 10 '
        'dimensions and 20,000 for 20 dimensions. The population size of all algorithms was 30, and '
        'each algorithm was independently run 30 times on every function. The best value, mean value, '
        'and standard deviation were recorded, and the Friedman test and the Wilcoxon rank-sum test at '
        'the 0.05 significance level {ref:derrac} were used for statistical analysis. All experiments '
        'were implemented in Python 3.11 on a Linux server with a 4-core CPU and 16 GB of memory. Nine '
        'algorithms were selected for comparison, including the basic BKA {ref:bka}, the classical SSA '
        '{ref:ssa}, COA {ref:coa}, GWO {ref:gwo}, SCA {ref:sca}, PSO {ref:pso}, DE {ref:de}, HHO '
        '{ref:hho}, and RIME {ref:rime}. Their parameters follow the original literature, as listed in '
        'Table 1.'
    )})
    ap({'table': st['tab_params']})
    ap({'h2': '4.2. Ablation Experiments'})
    ap({'p': (
        'To quantify the contribution of each strategy, three MSBKA variants embedding a single '
        'strategy were constructed: BKA-TCM only adopts the tent chaotic initialization, BKA-FDB only '
        'adopts the fitness-distance balance based companion selection, and BKA-CGM only adopts the '
        'adaptive Cauchy-Gaussian mutation. The five algorithms including the basic BKA and the '
        'complete MSBKA were run 30 times on the CEC2022 suite in 10 and 20 dimensions, and the '
        'Friedman test was applied. Table 2 lists the average rankings, which are visualized in Figure '
        '5, and the raw statistics are given in Tables A1 and A2 of Appendix A.'
    )})
    ap({'table': st['tab_ablation']})
    ap({'fig': f'{FIGS}/B_ablation_friedman.png',
        'caption': '**Figure 5.** Friedman rankings of BKA variants with different strategies.',
        'width_cm': 12.5})
    ap({'p': st['ablation_discussion']})
    ap({'h2': '4.3. Comparison with Other Algorithms'})
    ap({'p': (
        'This subsection compares MSBKA with the nine competitors. The complete best, mean, and '
        'standard deviation results are provided in Tables A3 and A4 of Appendix A, where the best mean '
        'on each function is marked in bold. Table 3 gives the average Friedman rankings with the '
        'corresponding p-values, and Table 4 summarizes the win/tie/loss statistics of the Wilcoxon '
        'rank-sum test from the perspective of MSBKA.'
    )})
    ap({'table': st['tab_friedman']})
    ap({'table': st['tab_wilcoxon']})
    ap({'p': st['comparison_discussion']})
    ap({'p': (
        'Figure 6 and Figure 7 display the average convergence curves on six representative functions '
        'in 10 and 20 dimensions, and Figure 8 shows the boxplots of the 30 independent results in 20 '
        'dimensions. It can be seen that MSBKA converges faster and reaches lower fitness values than '
        'the basic BKA on most functions, and its boxes are lower and more compact than those of the '
        'competitors, reflecting both accuracy and robustness. Figure 9 further visualizes the overall '
        'Friedman rankings. These results demonstrate that the three strategies significantly improve '
        'the global optimization capability of BKA on complex landscapes.'
    )})
    ap({'fig': f'{FIGS}/B_convergence_10.png',
        'caption': '**Figure 6.** Convergence curves of MSBKA and its competitors on representative '
                   'CEC2022 functions (D = 10).', 'width_cm': 14.5})
    ap({'fig': f'{FIGS}/B_convergence_20.png',
        'caption': '**Figure 7.** Convergence curves of MSBKA and its competitors on representative '
                   'CEC2022 functions (D = 20).', 'width_cm': 14.5})
    ap({'fig': f'{FIGS}/B_boxplot_20.png',
        'caption': '**Figure 8.** Boxplots of MSBKA and its competitors on representative CEC2022 '
                   'functions (D = 20).', 'width_cm': 14.5})
    ap({'fig': f'{FIGS}/B_friedman_bar.png',
        'caption': '**Figure 9.** Average Friedman rankings of all algorithms on CEC2022.',
        'width_cm': 14.0})

    # ============================ 5. Customer segmentation ============================
    ap({'h1': '5. Application to Customer Segmentation in Marketing Management'})
    ap({'p': (
        'Since Smith formally put forward the concept of market segmentation in 1956 {ref:smith_seg}, '
        'dividing customers into homogeneous groups and serving them with differentiated strategies has '
        'become the cornerstone of modern marketing management {ref:wedel}. With the popularization of '
        'point-of-sale and membership systems, data-driven customer segmentation based on clustering has '
        'become the mainstream practice {ref:rfm_paper}. In this section, MSBKA is applied to the '
        'centroid-based customer segmentation problem to verify its effectiveness on real business data.'
    )})
    ap({'h2': '5.1. Problem Formulation'})
    ap({'p': (
        'Given a customer dataset $O=\\{o_1,o_2,\\ldots ,o_M\\}$ with $M$ customers described by $d$ '
        'attributes, the goal of centroid-based segmentation is to find $K$ cluster centroids '
        '$c_1,c_2,\\ldots ,c_K$ that minimize the intra-cluster sum of squared errors (SSE), as defined '
        'in Equation (17).'
    )})
    ap({'eq': r'\min\ J\left( c_1,\ldots ,c_K \right)=\sum_{i=1}^{M}{\min_{k=1,\ldots ,K}\left\| o_i-c_k \right\|^{2}}', 'num': 17})
    ap({'p': (
        'Each customer is assigned to its nearest centroid according to Equation (18), which forms the '
        'segmentation scheme.'
    )})
    ap({'eq': r'label\left( o_i \right)=\arg \min_{k=1,\ldots ,K}\left\| o_i-c_k \right\|', 'num': 18})
    ap({'p': (
        'When a metaheuristic algorithm is used to solve this problem, each individual encodes a '
        'complete set of centroids by concatenation, as shown in Equation (19), so the dimensionality '
        'of the search space is $K\\times d$, and the search bounds of each coordinate are the '
        'attribute-wise minimum and maximum of the dataset.'
    )})
    ap({'eq': r'X=\left[ c_{1,1},\ldots ,c_{1,d},c_{2,1},\ldots ,c_{2,d},\ldots ,c_{K,1},\ldots ,c_{K,d} \right]', 'num': 19})
    ap({'p': (
        'Besides the SSE, the silhouette coefficient {ref:silhouette} defined in Equation (20) is '
        'employed to assess the quality of the final segmentation, where $a(i)$ is the average distance '
        'from customer $i$ to the other customers of its own segment and $b(i)$ is the smallest average '
        'distance from customer $i$ to the customers of any other segment. A larger silhouette '
        'coefficient indicates more compact and better separated segments.'
    )})
    ap({'eq': r's\left( i \right)=\frac{b\left( i \right)-a\left( i \right)}{\max \left\{ a\left( i \right),b\left( i \right) \right\}},\ \ SC=\frac{1}{M}\sum_{i=1}^{M}{s\left( i \right)}', 'num': 20})
    ap({'h2': '5.2. Datasets and Experimental Settings'})
    ap({'p': (
        'Two publicly available real-world business datasets were used. The first is the mall customers '
        'dataset, which records the annual income (thousand dollars) and the spending score (1–100) of '
        '200 shopping mall members; following the common practice, the number of segments was set to '
        '$K=5$. The second is the wholesale customers dataset from the UCI machine learning repository '
        '{ref:uci}, which contains the annual monetary spending of 440 wholesale channel clients on six '
        'product categories: fresh products, milk products, grocery, frozen products, '
        'detergents and paper products, and delicatessen. Because the spending variables are highly '
        'right-skewed, a logarithmic transformation was applied before clustering, and the number of '
        'segments was set to $K=3$. Table 5 summarizes the two datasets. MSBKA was compared with the '
        'classical K-means and K-means++ algorithms {ref:macqueen,kmeanspp} as well as the nine '
        'metaheuristics used in Section 4. For all metaheuristic algorithms, the population size was '
        '30, the maximum number of function evaluations was 20,000, and 30 independent runs were '
        'executed; for K-means and K-means++, a single random initialization was used in each of the 30 '
        'runs to reflect their sensitivity to the starting centroids.'
    )})
    ap({'table': st['tab_clustdata']})
    ap({'h2': '5.3. Results and Analysis'})
    ap({'p': st['clust_discussion']})
    ap({'table': st['tab_clust']})
    ap({'fig': f'{FIGS}/B_clust_convergence.png',
        'caption': '**Figure 10.** Convergence curves of the metaheuristic algorithms on the two '
                   'customer segmentation datasets.', 'width_cm': 13.5})
    ap({'fig': f'{FIGS}/B_clust_scatter.png',
        'caption': '**Figure 11.** Customer segments of the mall customers dataset obtained by MSBKA.',
        'width_cm': 11.5})
    ap({'p': st['managerial_discussion']})

    # ============================ 6. Conclusion ============================
    ap({'h1': '6. Conclusions'})
    ap({'p': (
        'This paper proposed an enhanced multi-strategy black-winged kite algorithm called MSBKA to '
        'overcome the deficiencies of the basic BKA, including the uneven random initialization, the '
        'lack of information exchange in the attacking phase, and the premature convergence caused by '
        'the excessive attraction of the leader. The tent chaotic mapping initialization generates a '
        'uniformly distributed initial population; the fitness-distance balance based companion '
        'selection integrates solution quality and positional novelty to choose instructive companions '
        'in the migration phase and realizes a coordinated transition between exploration and '
        'exploitation; and the adaptive Cauchy-Gaussian hybrid mutation keeps refreshing the leader '
        'throughout the search. The complexity analysis shows that the three strategies do not raise '
        'the order of the computational cost.'
    )})
    ap({'p': st['conclusion_numbers']})
    ap({'p': (
        'There are still some limitations worth noting. The control parameter of the tent map and the '
        'mutation amplitude of CGM are determined empirically, and the number of customer segments $K$ '
        'must be specified in advance. In future work, we will study the adaptive determination of $K$ '
        'by combining internal validity indices, extend MSBKA to binary and multi-objective versions, '
        'and apply it to a wider range of business analytics problems such as credit scoring, customer '
        'churn prediction, and supply chain site selection.'
    )})

    ap({'backmatter': [
        '**Author Contributions:** Conceptualization, X.C.; methodology, X.C.; software, X.C.; '
        'validation, X.C.; formal analysis, X.C.; investigation, X.C.; resources, X.C.; data curation, '
        'X.C.; writing—original draft preparation, X.C.; writing—review and editing, X.C.; '
        'visualization, X.C. The author has read and agreed to the published version of the manuscript.',
        '**Funding:** This research received no external funding.',
        '**Institutional Review Board Statement:** Not applicable.',
        '**Informed Consent Statement:** Not applicable.',
        '**Data Availability Statement:** The CEC2022 benchmark functions are publicly available. The '
        'mall customers dataset and the wholesale customers dataset are publicly available online. The '
        'source code is available from the author on reasonable request.',
        '**Conflicts of Interest:** The author declares no conflicts of interest.',
    ]})
    return B
