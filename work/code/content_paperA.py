"""Paper A full manuscript content.

Title: A Multi-Strategy Secretary Bird Optimization Algorithm for Global
Optimization and Cardinality-Constrained Portfolio Selection

Text placeholders {ref:key} are resolved to [n] citations by resolve_refs().
Numeric results are injected through the `st` dict produced by make_results_A.py.
"""
import re

FIGS = '/home/user/xixi/work/figs'

TITLE = ('A Multi-Strategy Secretary Bird Optimization Algorithm for Global '
         'Optimization and Cardinality-Constrained Portfolio Selection')

AUTHORS = [('Xinyu Cai ', False), ('1,', True), ('*', True)]

AFFILIATIONS = [
    '{sup:1}\tCollege of Business, Jiaxing University, Jiaxing 314001, China; caixinyu@zjxu.edu.cn',
    '*\tCorrespondence: caixinyu@zjxu.edu.cn',
]

KEYWORDS = ('secretary bird optimization algorithm; metaheuristic algorithm; good point set; '
            'elite-guided differential search; quadratic interpolation; portfolio selection; '
            'financial management')


def abstract(st):
    return (
        'Complex optimization problems are widespread in modern business management and engineering practice, '
        'and metaheuristic algorithms have become an important tool for solving them. The secretary bird '
        'optimization algorithm (SBOA) is a recently proposed metaheuristic inspired by the survival behavior '
        'of secretary birds. Although SBOA shows competitive performance, it still suffers from insufficient '
        'population diversity, a blind random search in the early hunting stage, and a tendency to fall into '
        'local optima when facing complex multimodal landscapes. To overcome these deficiencies, this paper '
        'proposes a multi-strategy secretary bird optimization algorithm (MSSBOA) that integrates three '
        'improvement strategies. Firstly, a good point set initialization strategy is introduced to generate '
        'a uniformly distributed initial population and improve the quality of the initial solutions. '
        'Secondly, an elite-guided differential search strategy is designed to replace the undirected '
        'differential move of the first hunting stage; it strengthens the information exchange between the '
        'elite group and ordinary individuals and accelerates convergence, while a dimension-wise crossover '
        'preserves the population diversity. Finally, an elite refinement mechanism, which alternates an '
        'adaptive t-distribution perturbation with a quadratic interpolation operator, is applied to the '
        'global best individual, helping the population escape from local optima in the early stage and '
        'refining the solution accuracy in the later stage. MSSBOA is comprehensively evaluated on '
        'the CEC2017 test suite in 10 and 30 dimensions against the basic SBOA and eight well-known and '
        'state-of-the-art algorithms, and the results are analyzed using the Friedman test and the Wilcoxon '
        f'rank-sum test. MSSBOA achieves {st.get("abs_rank_phrase", "a highly competitive overall ranking")} '
        'in the Friedman test, and the ablation experiments confirm the effectiveness of each strategy. In addition, '
        'MSSBOA is successfully applied to the cardinality-constrained portfolio selection problem on five '
        'real-world capital market datasets from the OR-Library. In all cases, MSSBOA provides the lowest '
        'objective values and the most stable investment schemes among the compared algorithms, indicating '
        'its practical value as a decision-support tool in financial management.'
    )


# --------------------------------------------------------------------------- refs
REFS = {}  # filled by set_refs()


def set_refs(mapping):
    REFS.clear()
    REFS.update(mapping)


REF_RE = re.compile(r'\{ref:([A-Za-z0-9_,\- ]+)\}')


def resolve_refs(blocks):
    """Replace {ref:a,b} placeholders with [n] numbers; return blocks + ordered keys."""
    order = []

    def key_num(k):
        k = k.strip()
        if k not in order:
            order.append(k)
        return order.index(k) + 1

    def collapse(nums):
        nums = sorted(set(nums))
        parts = []
        i = 0
        while i < len(nums):
            j = i
            while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                j += 1
            if j - i >= 2:
                parts.append(f'{nums[i]}–{nums[j]}')
            else:
                parts.extend(str(n) for n in nums[i:j + 1])
            i = j + 1
        return '[' + ','.join(parts) + ']'

    def sub(text):
        def repl(m):
            keys = m.group(1).split(',')
            return collapse([key_num(k) for k in keys])
        return REF_RE.sub(repl, text)

    out = []
    for b in blocks:
        b = dict(b)
        for k in ('p', 'caption', 'h1', 'h2', 'h3'):
            if k in b and isinstance(b[k], str):
                b[k] = sub(b[k])
        out.append(b)
    missing = [k for k in order if k not in REFS]
    if missing:
        raise KeyError(f'missing reference entries: {missing}')
    reflist = [REFS[k] for k in order]
    return out, reflist


# --------------------------------------------------------------------------- body
def blocks(st):
    B = []
    ap = B.append

    # ============================ 1. Introduction ============================
    ap({'h1': '1. Introduction'})
    ap({'p': (
        'With the continuous development of the economy and society, decision-making problems arising in '
        'business management, engineering design, and scientific research are becoming increasingly '
        'complicated {ref:indus,jain_clust}. A large number of these problems can be abstracted as '
        'optimization problems, whose essence is to find the decision variables that minimize or maximize '
        'one or more objective functions under a set of constraints {ref:derrac}. Typical examples include '
        'production scheduling {ref:jobshop}, unmanned aerial vehicle path planning {ref:uav}, feature '
        'selection {ref:feasel}, image segmentation {ref:imgseg}, wireless sensor network coverage {ref:wsn}, '
        'hyperparameter optimization of machine learning models {ref:svm}, and portfolio selection in '
        'financial management {ref:markowitz,chang}. However, real-world optimization problems usually '
        'exhibit high dimensionality, non-linearity, non-convexity, multimodality, and non-differentiability, '
        'and many of them have been proven to be NP-hard. Traditional deterministic methods, such as linear '
        'programming, branch-and-bound, and gradient-based techniques, rely on strict mathematical properties '
        'of the problem and often become computationally prohibitive or fall into local optima when these '
        'assumptions do not hold {ref:kalayci}. Consequently, there is an urgent demand for optimization '
        'techniques that are efficient, robust, and insensitive to the mathematical structure of the problem.'
    )})
    ap({'p': (
        'Metaheuristic algorithms are stochastic optimization techniques inspired by natural phenomena, '
        'physical laws, mathematical rules, or social behaviors. Instead of requiring gradient information, '
        'they iteratively improve a population of candidate solutions through probabilistic search operators, '
        'and achieve a trade-off between global exploration and local exploitation {ref:gwo,nfl}. Owing to '
        'their simple structure, flexibility, and gradient-free character, metaheuristic algorithms have been '
        'successfully applied to a wide range of complex problems. According to the source of inspiration, '
        'metaheuristic algorithms can be roughly classified into five categories, as shown in Figure 1. '
        'Evolution-based algorithms simulate the mechanisms of biological evolution such as selection, '
        'crossover, and mutation, and representative examples include the genetic algorithm (GA) {ref:ga}, '
        'differential evolution (DE) {ref:de}, evolution strategies (ES) {ref:es}, the covariance matrix '
        'adaptation evolution strategy (CMA-ES) {ref:cmaes}, and the success-history based adaptive '
        'differential evolution with linear population size reduction (LSHADE) {ref:lshade}. Swarm-based '
        'algorithms imitate the collective foraging, hunting, and migration behaviors of biological groups. '
        'Classical and recent members include particle swarm optimization (PSO) {ref:pso}, ant colony '
        'optimization (ACO) {ref:aco}, the grey wolf optimizer (GWO) {ref:gwo}, the whale optimization '
        'algorithm (WOA) {ref:woa}, Harris hawks optimization (HHO) {ref:hho}, the sparrow search algorithm '
        '(SSA) {ref:ssa}, the dung beetle optimizer (DBO) {ref:dbo}, the crayfish optimization algorithm '
        '(COA) {ref:coa}, and the cuckoo search (CS) {ref:cs}. Physics-based algorithms draw on physical '
        'laws or chemical mechanisms, such as the multi-verse optimizer (MVO) {ref:mvo}, the equilibrium '
        'optimizer (EO) {ref:eo}, the RIME algorithm inspired by rime-ice formation {ref:rime}, the snow '
        'ablation optimizer (SAO) {ref:sao}, and the Kepler optimization algorithm (KOA) {ref:koa}. '
        'Mathematics-based algorithms are built on mathematical functions and theories, and typical examples '
        'are the sine cosine algorithm (SCA) {ref:sca} and the arithmetic optimization algorithm (AOA) '
        '{ref:aoa}. Human-based algorithms mimic human social activities and cognitive processes; a representative '
        'example is teaching-learning-based optimization (TLBO) {ref:tlbo}. In addition, new swarm-based '
        'algorithms such as the parrot optimizer (PO) {ref:po} continue to emerge, which reflects the '
        'vitality of this research field.'
    )})
    ap({'fig': f'{FIGS}/classification.png',
        'caption': '**Figure 1.** Classification of metaheuristic algorithms.',
        'width_cm': 14.5})
    ap({'p': (
        'Although metaheuristic algorithms have achieved remarkable success in various fields, they still '
        'face common challenges, such as the difficulty of balancing exploration and exploitation, premature '
        'convergence caused by the loss of population diversity, and performance degradation on complex '
        'high-dimensional problems. More importantly, the no free lunch (NFL) theorem {ref:nfl} states that '
        'no single optimization algorithm can outperform all other algorithms on every class of problems. '
        'The excellent performance of an algorithm on one set of problems does not guarantee similar '
        'performance on other problems. This theorem motivates researchers to continuously design new '
        'algorithms or improve existing ones for specific classes of optimization problems.'
    )})
    ap({'p': (
        'The secretary bird optimization algorithm (SBOA) is a novel swarm-based metaheuristic proposed by '
        'Fu et al. in 2024 {ref:sboa}, which mathematically models the hunting and escape behaviors of '
        'secretary birds surviving in their natural environment. Owing to its clear structure, few control '
        'parameters, and competitive search accuracy, SBOA has quickly attracted the attention of '
        'researchers and has been applied or improved in several studies. For example, Qin et al. '
        'integrated a feedback regulation mechanism and golden sine guidance into SBOA to solve '
        'engineering optimization problems {ref:isboa1}; Wang et al. designed an enhanced SBOA with '
        'multi-strategy fusion and Cauchy-Gaussian crossover {ref:isboa2}; Zhu et al. combined '
        'quantum-computing-based mutation with SBOA to optimize kernel extreme learning machines for '
        'medical classification {ref:isboa3}; and SBOA has also been employed to optimize the allocation '
        'of renewable distributed generation in power systems {ref:isboa4}. Nevertheless, in-depth '
        'analysis of the basic SBOA reveals that it still has the following shortcomings when solving '
        'complex optimization problems. First, the initial population is generated in a purely random '
        'manner, which cannot guarantee a uniform coverage of the solution space and directly weakens the '
        'quality of the subsequent search. Secondly, in the first hunting stage, individuals update their '
        'positions only through the difference of two randomly selected individuals. This undirected random '
        'walk ignores the guiding information of the dominant group, resulting in slow convergence and '
        'blind exploration in the early stage. Finally, in the middle and later stages, the search is '
        'strongly attracted by the current global best individual, so the population diversity decreases '
        'rapidly and the algorithm is prone to stagnation in local optima on multimodal landscapes.'
    )})
    ap({'p': (
        'Motivated by the above observations and the NFL theorem, this paper proposes a multi-strategy '
        'secretary bird optimization algorithm (MSSBOA) to systematically address the deficiencies of the '
        'basic SBOA. MSSBOA organically integrates three improvement strategies. First, a good point set '
        '(GPS) initialization strategy based on number theory {ref:hua} is adopted to construct a uniformly '
        'distributed initial population, which improves the coverage of the solution space at the very '
        'beginning of the search. Secondly, an elite-guided differential search strategy (EDS) is designed '
        'for the first hunting stage. By introducing an elite pool composed of the three best individuals '
        'and the centroid of the top 10% of the population, EDS pulls each individual toward the elite '
        'region with a guided differential move and then inherits about half of the parent dimensions '
        'through a binomial crossover, which strengthens the exploitation ability without sacrificing the '
        'randomness needed for exploration. Finally, an elite refinement '
        'mechanism (ERM) is executed in each iteration, which alternately applies an adaptive '
        't-distribution perturbation {ref:tdist} and a three-point quadratic interpolation to the global '
        'best individual. The degrees of freedom of the t-distribution grow with the iteration counter, '
        'so the perturbation behaves like a heavy-tailed Cauchy mutation in the early stage to help the '
        'population jump out of local optima, while the quadratic interpolation exploits the local '
        'curvature information to continuously refine the solution accuracy. The main contributions of '
        'this paper are summarized as follows.'
    )})
    ap({'p': '(1) A multi-strategy SBOA variant, called MSSBOA, is proposed by integrating the good point '
             'set initialization, the elite-guided differential search, and the elite refinement '
             'mechanism into the basic SBOA.', 'style': 'MDPI_3.1_text'})
    ap({'p': '(2) The performance of MSSBOA is comprehensively examined on the 29 functions of the CEC2017 '
             'test suite in 10 and 30 dimensions. Ablation experiments verify the effectiveness of each '
             'strategy, and comparisons with nine basic and advanced algorithms are analyzed by the '
             'Friedman test and the Wilcoxon rank-sum test.', 'style': 'MDPI_3.1_text'})
    ap({'p': '(3) MSSBOA is applied to the cardinality-constrained portfolio selection problem on five '
             'real capital market datasets from the OR-Library, demonstrating its ability to support '
             'practical investment decision-making in financial management.', 'style': 'MDPI_3.1_text'})
    ap({'p': (
        'The rest of this paper is organized as follows. Section 2 reviews the mathematical model of the '
        'basic SBOA. Section 3 describes the three improvement strategies and the framework of the proposed '
        'MSSBOA in detail, and analyzes its computational complexity. Section 4 presents the experimental '
        'results on the CEC2017 test suite, including the ablation study, the comparison experiments, and '
        'the statistical analysis. Section 5 formulates the cardinality-constrained portfolio selection '
        'problem and reports the application results on five real market datasets. Finally, Section 6 '
        'concludes the whole work and outlines future research directions.'
    )})

    # ============================ 2. SBOA ============================
    ap({'h1': '2. Secretary Bird Optimization Algorithm'})
    ap({'p': (
        'The secretary bird is a large terrestrial raptor living in the African savanna, famous for preying '
        'on snakes. SBOA {ref:sboa} abstracts two typical survival behaviors of secretary birds into '
        'mathematical models: the hunting strategy, which corresponds to the exploration phase, and the '
        'escape strategy, which corresponds to the exploitation phase. In each iteration, every individual '
        'first performs one hunting update and then one escape update, and each update is followed by a '
        'greedy selection. The details are described as follows.'
    )})
    ap({'h2': '2.1. Initialization'})
    ap({'p': (
        'Like most population-based metaheuristics, SBOA starts the search from a randomly generated '
        'population. The position of the $i$th secretary bird in the $j$th dimension is initialized by '
        'Equation (1).'
    )})
    ap({'eq': r'X_{i,j}=lb_j+r\times \left( ub_j-lb_j \right),\ \ i=1,2,\ldots ,N,\ \ j=1,2,\ldots ,D', 'num': 1})
    ap({'p': (
        'where $X_{i,j}$ denotes the position of the $i$th individual in the $j$th dimension, $r$ is a '
        'uniform random number within the range [0, 1], $lb_j$ and $ub_j$ are the lower and upper bounds '
        'of the $j$th dimension, $N$ is the population size, and $D$ is the dimensionality of the problem.'
    )})
    ap({'h2': '2.2. Hunting Strategy (Exploration Phase)'})
    ap({'p': (
        'The hunting process of secretary birds preying on snakes is divided into three equal time stages: '
        'searching for prey, consuming prey, and attacking prey. In the first stage ($t<T/3$), the '
        'secretary bird searches the environment for possible prey, and its position is updated by the '
        'differential information of two randomly selected individuals, as shown in Equation (2).'
    )})
    ap({'eq': r'x_{i,j}^{new,P1}=x_{i,j}^{t}+\left( x_{r_1,j}^{t}-x_{r_2,j}^{t} \right)\times R_1', 'num': 2})
    ap({'p': (
        'where $t$ is the current iteration, $T$ is the maximum number of iterations, $x_{r_1,j}^t$ and '
        '$x_{r_2,j}^t$ are the positions of two randomly selected distinct individuals, and $R_1$ is a '
        'random vector whose elements obey the uniform distribution in [0, 1]. In the second stage '
        '($T/3\\le t<2T/3$), the secretary bird consumes the prey and hovers around the current optimal '
        'position with Brownian motion, which is modeled by Equation (3).'
    )})
    ap({'eq': r'x_{i,j}^{new,P1}=X_{best,j}^{t}+\exp \left( \left( t/T \right)^4 \right)\times \left( RB-0.5 \right)\times \left( X_{best,j}^{t}-x_{i,j}^{t} \right)', 'num': 3})
    ap({'p': (
        'where $X_{best,j}^t$ is the position of the current global best individual and $RB$ is a random '
        'vector generated from the standard normal distribution, which simulates Brownian motion. In the '
        'third stage ($t\\ge 2T/3$), the secretary bird attacks the prey with a Levy flight trajectory, '
        'and the convergence factor $CF$ gradually shrinks the step size, as defined in Equations (4) '
        'and (5).'
    )})
    ap({'eq': r'CF=\left( 1-\frac{t}{T} \right)^{2t/T}', 'num': 4})
    ap({'eq': r'x_{i,j}^{new,P1}=X_{best,j}^{t}+CF\times x_{i,j}^{t}\times RL,\ \ RL=0.5\times Levy\left( D \right)', 'num': 5})
    ap({'p': 'where $Levy(D)$ denotes the Levy flight distribution function {ref:levy}, which is calculated '
             'by Equations (6) and (7).'})
    ap({'eq': r'Levy\left( D \right)=\frac{u\times \sigma }{\left| v \right|^{1/\beta }}', 'num': 6})
    ap({'eq': r'\sigma =\left( \frac{\Gamma \left( 1+\beta  \right)\times \sin \left( \pi \beta /2 \right)}{\Gamma \left( \left( 1+\beta  \right)/2 \right)\times \beta \times 2^{\left( \beta -1 \right)/2}} \right)^{1/\beta }', 'num': 7})
    ap({'p': (
        'where $u$ and $v$ are random numbers obeying the standard normal distribution, $\\Gamma$ is the '
        'gamma function, and the constant $\\beta$ is set to 1.5. After each hunting update, the trial '
        'position is evaluated and accepted only if its fitness is not worse than the current one.'
    )})
    ap({'h2': '2.3. Escape Strategy (Exploitation Phase)'})
    ap({'p': (
        'When facing threats from predators, secretary birds adopt two escape behaviors: camouflage by the '
        'environment and flying or running away. SBOA selects one of the two behaviors with equal '
        'probability, as described in Equations (8) and (9).'
    )})
    ap({'eq': r'x_{i,j}^{new,P2}=X_{best,j}^{t}+\left( 1-\frac{t}{T} \right)^{2}\times \left( 2\times RB-1 \right)\times x_{i,j}^{t},\ \ r<0.5', 'num': 8})
    ap({'eq': r'x_{i,j}^{new,P2}=x_{i,j}^{t}+R_2\times \left( x_{rand,j}^{t}-K\times x_{i,j}^{t} \right),\ \ r\ge 0.5', 'num': 9})
    ap({'p': 'where $r$ is a uniform random number in [0, 1], $R_2$ is a random vector obeying the uniform '
             'distribution in [0, 1], $x_{rand,j}^t$ is a randomly selected individual from the current '
             'population, and $K$ is a random integer factor calculated by Equation (10).'})
    ap({'eq': r'K=\mathrm{round}\left( 1+rand\left( 0,1 \right) \right)', 'num': 10})
    ap({'p': 'After each update, SBOA performs the greedy selection defined in Equation (11) to retain the '
             'better solution, which guarantees that the population quality is monotonically non-decreasing.'})
    ap({'eq': r'X_{i}^{t+1}=\begin{cases} X_{i}^{new}, & f\left( X_{i}^{new} \right)\le f\left( X_{i}^{t} \right) \\ X_{i}^{t}, & \mathrm{otherwise} \end{cases}', 'num': 11})

    # ============================ 3. MSSBOA ============================
    ap({'h1': '3. Proposed Multi-Strategy Secretary Bird Optimization Algorithm'})
    ap({'p': (
        'As analyzed in Section 1, the basic SBOA suffers from the non-uniform random initialization, the '
        'blind differential search in the first hunting stage, and the rapid loss of population diversity '
        'in the later stage. To overcome these limitations, this section proposes the MSSBOA algorithm, '
        'which integrates the good point set initialization strategy, the elite-guided differential search '
        'strategy, and the elite refinement mechanism into the basic framework. The '
        'three strategies are described in detail below, followed by the overall framework and the '
        'complexity analysis of MSSBOA.'
    )})
    ap({'h2': '3.1. Good Point Set Initialization Strategy (GPS)'})
    ap({'p': (
        'The quality of the initial population directly affects the convergence speed and the solution '
        'accuracy of metaheuristic algorithms. A purely random initial population tends to cluster in some '
        'regions of the solution space while leaving other regions uncovered. The good point set theory '
        'proposed by Hua and Wang {ref:hua} provides a deterministic method to construct point sets with '
        'much lower discrepancy than random sampling. Let $p$ be the smallest prime satisfying $p\\ge 2D+3$. '
        'The good point is constructed by Equation (12), and the initial population is mapped into the '
        'search space by Equation (13).'
    )})
    ap({'eq': r'r_j=2\cos \left( \frac{2\pi j}{p} \right),\ \ j=1,2,\ldots ,D', 'num': 12})
    ap({'eq': r'X_{i,j}=lb_j+\left\{ r_j\times i \right\}\times \left( ub_j-lb_j \right)', 'num': 13})
    ap({'p': (
        'where $\\{\\cdot\\}$ denotes the operation of taking the fractional part. Figure 2 compares the '
        'population distributions generated by the random initialization and the good point set '
        'initialization with 100 points in a two-dimensional unit space. It can be clearly observed that '
        'the good point set covers the space more uniformly, which enriches the initial population '
        'diversity and lays a solid foundation for the subsequent search.'
    )})
    ap({'fig': f'{FIGS}/gps_vs_random.png',
        'caption': '**Figure 2.** Population distributions of random initialization and good point set '
                   'initialization.', 'width_cm': 12.5})
    ap({'h2': '3.2. Elite-Guided Differential Search Strategy (EDS)'})
    ap({'p': (
        'In the first hunting stage of the basic SBOA, the position update in Equation (2) depends only on '
        'the difference between two randomly selected individuals. Although this operator maintains '
        'randomness, it completely ignores the guiding information accumulated by the dominant group, so '
        'the early search is blind and inefficient. To address this issue, this paper designs an '
        'elite-guided differential search strategy. First, an elite pool is constructed as shown in Equation (14).'
    )})
    ap({'eq': r'E=\left\{ X_{best1}^{t},X_{best2}^{t},X_{best3}^{t},X_{mean}^{t} \right\},\ \ X_{mean}^{t}=\frac{1}{n_e}\sum_{k=1}^{n_e}{X_{k}^{t}}', 'num': 14})
    ap({'p': (
        'where $X_{best1}^t$, $X_{best2}^t$, and $X_{best3}^t$ are the three best individuals of the '
        'current population, and $X_{mean}^t$ is the centroid of the top $n_e$ individuals, with '
        '$n_e=\\max (3,\\lfloor 0.1N \\rfloor )$, namely 10% of the population size and at least three '
        'individuals. Drawing on the successful current-to-pbest mutation idea of advanced differential '
        'evolution variants {ref:de,lshade}, a guided mutant vector is generated for each individual by '
        'Equation (15).'
    )})
    ap({'eq': r'v_{i,j}^{t}=x_{i,j}^{t}+r_3\times \left( X_{E,j}^{t}-x_{i,j}^{t} \right)+r_4\times \left( x_{r_1,j}^{t}-x_{r_2,j}^{t} \right)', 'num': 15})
    ap({'p': (
        'where $X_E^t$ is an individual randomly selected from the elite pool $E$, $x_{r_1}^t$ and '
        '$x_{r_2}^t$ are two randomly selected distinct individuals, and $r_3$ and $r_4$ are random '
        'vectors whose elements obey the uniform distribution in [0, 1]. The first difference term pulls '
        'the individual toward the elite region, and the second difference term preserves the random '
        'perturbation of the original operator. Then, the mutant vector is combined with the parent '
        'through the dimension-wise binomial crossover in Equation (16), which replaces the original '
        'update of the first hunting stage.'
    )})
    ap({'eq': r'x_{i,j}^{new,P1}=\begin{cases} v_{i,j}^{t}, & rand_j<CR\ \mathrm{or}\ j=j_{rand} \\ x_{i,j}^{t}, & \mathrm{otherwise} \end{cases}', 'num': 16})
    ap({'p': (
        'where $rand_j$ is a uniform random number generated for the $j$th dimension, $j_{rand}$ is a '
        'randomly chosen dimension index that guarantees at least one dimension is inherited from the '
        'mutant vector, and the crossover rate $CR$ is set to 0.5. Figure 3 illustrates the mechanism of '
        'the EDS strategy. On the one hand, the elite pool provides diverse and reliable guidance so that '
        'ordinary individuals no longer move blindly, and the randomness of elite selection avoids '
        'over-concentration toward a single leader, which alleviates premature convergence; on the other '
        'hand, the binomial crossover lets each trial vector inherit about half of its dimensions from '
        'the parent, which softens the guidance into a moderate step and effectively protects the '
        'population diversity in the early stage.'
    )})
    ap({'fig': f'{FIGS}/sketch_eds.png',
        'caption': '**Figure 3.** Schematic diagram of the elite-guided differential search strategy.',
        'width_cm': 13.5})
    ap({'h2': '3.3. Elite Refinement Mechanism (ERM)'})
    ap({'p': (
        'In the middle and later stages of SBOA, both the hunting and the escape updates are strongly '
        'attracted by the global best individual. Once the best individual falls into a local optimum, '
        'the whole population is easily trapped; meanwhile, the accuracy of the final solution completely '
        'depends on the best individual, which is never refined by a dedicated operator in the basic '
        'algorithm. To address this issue, an elite refinement mechanism is designed, which refines the '
        'global best individual once in every iteration by alternately applying two complementary '
        'operators. In odd-numbered iterations, an adaptive t-distribution perturbation is applied. The '
        't-distribution, also known as Student\'s t-distribution, is controlled by the '
        'degrees-of-freedom parameter $df$. When $df=1$ the t-distribution degenerates to the '
        'heavy-tailed Cauchy distribution, and when $df\\to \\infty$ it approaches the Gaussian '
        'distribution {ref:tdist}. Making use of this property, the perturbation is constructed as shown '
        'in Equation (17).'
    )})
    ap({'eq': r'X_{ref}=X_{best}^{t}\times \left( 1+0.5\times \left( 1-\frac{t}{T} \right)\times t_{df}\left( t \right) \right)', 'num': 17})
    ap({'p': (
        'where $t_{df}(t)$ denotes a random vector sampled from the t-distribution whose degrees of '
        'freedom equal the current iteration counter $t$. In the early stage, the small degrees of '
        'freedom produce heavy-tailed perturbations similar to the Cauchy mutation, which gives the best '
        'individual a large probability of jumping out of local optima; as the iteration proceeds, the '
        'perturbation gradually approaches a small Gaussian noise, and the shrinking factor $0.5(1-t/T)$ '
        'further controls the amplitude. In even-numbered iterations, a three-point quadratic '
        'interpolation is applied instead. Using the best individual and two randomly selected '
        'individuals $X_{r_1}^t$ and $X_{r_2}^t$, the vertex of the parabola fitted through the three '
        'points is calculated dimension by dimension, as shown in Equation (18).'
    )})
    ap({'eq': r'x_{ref,j}=\frac{1}{2}\times \frac{\left( x_{r_1,j}^{2}-x_{r_2,j}^{2} \right)f_{best}+\left( x_{r_2,j}^{2}-x_{best,j}^{2} \right)f_{r_1}+\left( x_{best,j}^{2}-x_{r_1,j}^{2} \right)f_{r_2}}{\left( x_{r_1,j}-x_{r_2,j} \right)f_{best}+\left( x_{r_2,j}-x_{best,j} \right)f_{r_1}+\left( x_{best,j}-x_{r_1,j} \right)f_{r_2}}', 'num': 18})
    ap({'p': (
        'where $f_{best}$, $f_{r_1}$, and $f_{r_2}$ are the fitness values of the three individuals. The '
        'quadratic interpolation exploits the curvature information implied by the fitness landscape and '
        'usually produces a high-quality candidate near the promising region at the cost of only one '
        'function evaluation. Whichever operator is applied, the refined solution $X_{ref}$ competes with '
        'the worst individual of the population through the greedy rule in Equation (19). In this way, '
        'the mechanism keeps injecting either diversity (t-distribution perturbation) or accuracy '
        '(quadratic interpolation) into the population without losing any elite information.'
    )})
    ap({'eq': r'X_{worst}^{t+1}=\begin{cases} X_{ref}, & f\left( X_{ref} \right)<f\left( X_{worst}^{t} \right) \\ X_{worst}^{t}, & \mathrm{otherwise} \end{cases}', 'num': 19})
    ap({'h2': '3.4. The Framework of MSSBOA'})
    ap({'p': (
        'The MSSBOA algorithm is obtained by embedding the three improvement strategies into the basic '
        'SBOA. GPS acts on the initialization step, EDS reconstructs the position update of the first '
        'hunting stage, and ERM is executed at the end of each iteration. It should be emphasized that the three '
        'strategies work on different stages of the search process and complement each other: GPS improves '
        'the starting point of the search, EDS strengthens the guided exploration in the early stage, and '
        'ERM maintains the vitality and accuracy of the population in the whole process. The pseudo-code of MSSBOA is '
        'given in Algorithm 1, and the corresponding flowchart is presented in Figure 4.'
    )})
    ap({'algorithm': {'title': 'Algorithm 1 Multi-Strategy Secretary Bird Optimization Algorithm (MSSBOA)',
        'lines': [
            '1: Initialize the population $X$ with the GPS strategy using Equations (12)–(13)',
            '2: Evaluate the fitness of all individuals; determine $X_{best}$; set $FEs=N$',
            '3: **while** $FEs<MaxFEs$ **do**',
            '4:  **for** $i=1$ to $N$ **do**  //hunting strategy',
            '5:   **if** $t<T/3$ **then** update $x_i^{new,P1}$ with the EDS strategy using Equations (14)–(16)',
            '6:   **else if** $t<2T/3$ **then** update $x_i^{new,P1}$ using Equation (3)',
            '7:   **else** update $x_i^{new,P1}$ using Equations (4)–(5)',
            '8:   **end if**',
            '9:   Evaluate $x_i^{new,P1}$; apply greedy selection using Equation (11); $FEs=FEs+1$',
            '10:  **end for**',
            '11:  **for** $i=1$ to $N$ **do**  //escape strategy',
            '12:   Update $x_i^{new,P2}$ using Equations (8)–(10)',
            '13:   Evaluate $x_i^{new,P2}$; apply greedy selection using Equation (11); $FEs=FEs+1$',
            '14:  **end for**',
            '15:  Generate $X_{ref}$ with the ERM strategy using Equation (17) or Equation (18) and evaluate it; $FEs=FEs+1$  //ERM',
            '16:  Replace the worst individual using Equation (19)',
            '17: **end while**',
            '18: **return** the best solution $X_{best}$',
        ]}})
    ap({'fig': f'{FIGS}/flow_mssboa.png',
        'caption': '**Figure 4.** Flowchart of the proposed MSSBOA.', 'width_cm': 11.5})
    ap({'h2': '3.5. Computational Complexity Analysis of MSSBOA'})
    ap({'p': (
        'The computational complexity of MSSBOA is analyzed from the perspectives of time and space. Let '
        '$N$ denote the population size, $D$ the problem dimensionality, and $T$ the maximum number of '
        'iterations. For the basic SBOA, the initialization costs $O(N\\times D)$, and each iteration '
        'performs two position updates and evaluations for every individual, so the total time complexity '
        'is $O(2\\times N\\times D\\times T)$, which is simplified as $O(N\\times D\\times T)$. For MSSBOA, '
        'the GPS strategy only changes the generation rule of the initial population and its complexity is '
        'still $O(N\\times D)$. The EDS strategy only modifies the update formula of the first hunting '
        'stage without extra fitness evaluations, so it does not increase the order of complexity. The ERM '
        'strategy introduces one additional evaluation per iteration, whose cost $O(D\\times T)$ is far '
        'smaller than the main loop. Therefore, the overall time complexity of MSSBOA remains '
        '$O(N\\times D\\times T)$, the same order as the basic SBOA. In terms of space, the dominant '
        'storage is the population position matrix and the fitness vector, so the space complexity of '
        'MSSBOA is $O(N\\times D)$, which is also identical to that of the basic SBOA. In conclusion, the '
        'three improvement strategies enhance the search ability of SBOA without increasing the order of '
        'computational complexity.'
    )})
    return B


def blocks_experiments(st):
    """Sections 4-6 + back matter. `st` carries computed statistics."""
    B = []
    ap = B.append

    # ============================ 4. CEC2017 experiments ============================
    ap({'h1': '4. Numerical Experiments Using the CEC2017 Test Suite'})
    ap({'p': (
        'In this section, the performance of the proposed MSSBOA is comprehensively evaluated on the '
        'CEC2017 test suite {ref:cec2017}. Section 4.1 introduces the experimental settings and the '
        'performance metrics. Section 4.2 reports the ablation experiments that verify the effectiveness '
        'of the three improvement strategies. Section 4.3 compares MSSBOA with nine basic and advanced '
        'algorithms and analyzes the results by means of statistical tests, convergence curves, and '
        'boxplots.'
    )})
    ap({'h2': '4.1. Experimental Settings and Performance Metrics'})
    ap({'p': (
        'The CEC2017 test suite contains 29 benchmark functions (the unstable F2 is officially excluded), '
        'in which F1 and F3 are unimodal functions, F4–F10 are simple multimodal functions, F11–F20 are '
        'hybrid functions, and F21–F30 are composition functions. Unimodal functions examine the '
        'convergence accuracy and exploitation ability of an algorithm, multimodal functions test the '
        'ability to escape from local optima, while hybrid and composition functions simulate the complex '
        'landscapes of real-world problems and provide a comprehensive assessment of the balance between '
        'exploration and exploitation. The experiments were conducted in 10 and 30 dimensions with the '
        'search range $[-100,100]^D$. In order to compare all algorithms fairly, the maximum number of '
        'function evaluations ($MaxFEs$) was used as the unified stopping criterion and was set to '
        '$1000\\times D$, namely 10,000 for 10 dimensions and 30,000 for 30 dimensions. The population '
        'size of all algorithms was set to 30, and each algorithm was run independently 30 times on every '
        'function. Since $MaxFEs$ serves as the stopping criterion, the nominal maximum iteration number '
        'of MSSBOA is $T=\\lfloor MaxFEs/(2N+1) \\rfloor$ and the ratio $t/T$ is truncated to 1 when '
        'necessary. The best value, mean value, and standard deviation of the 30 runs were recorded, and '
        'the Friedman test and the Wilcoxon rank-sum test with the significance level of 0.05 {ref:derrac} '
        'were employed to detect statistical differences. All experiments were implemented in Python 3.11 '
        'and executed on a Linux server with a 4-core CPU and 16 GB of memory.'
    )})
    ap({'p': (
        'To thoroughly assess MSSBOA, nine widely used and state-of-the-art algorithms were selected as '
        'competitors, including the basic SBOA {ref:sboa}, the classical swarm-based GWO {ref:gwo} and '
        'WOA {ref:woa}, the mathematics-based SCA {ref:sca}, the classical PSO {ref:pso}, and the recent '
        'swarm-based HHO {ref:hho}, DBO {ref:dbo}, COA {ref:coa}, together with the physics-based RIME '
        '{ref:rime}. The parameter settings of all algorithms follow the recommendations of their '
        'original literature, as listed in Table 1.'
    )})
    ap({'table': st['tab_params']})
    ap({'h2': '4.2. Ablation Experiments'})
    ap({'p': (
        'In order to verify the contribution of each improvement strategy, three MSSBOA variants '
        'incorporating a single strategy were constructed: SBOA-GPS only adopts the good point set '
        'initialization, SBOA-EDS only adopts the elite-guided differential search, and SBOA-ERM only '
        'adopts the elite refinement mechanism. The basic SBOA, the three single-strategy '
        'variants, and the complete MSSBOA were run independently 30 times on the CEC2017 test suite in '
        '10 and 30 dimensions, and the Friedman test was applied to the mean errors. The average '
        'rankings are summarized in Table 2 and visualized in Figure 5. The raw statistical results are '
        'provided in Tables A1 and A2 of Appendix A.'
    )})
    ap({'table': st['tab_ablation']})
    ap({'fig': f'{FIGS}/A_ablation_friedman.png',
        'caption': '**Figure 5.** Friedman rankings of SBOA variants with different strategies.',
        'width_cm': 12.5})
    ap({'p': st['ablation_discussion']})
    ap({'h2': '4.3. Comparison with Other Algorithms'})
    ap({'p': (
        'This subsection compares MSSBOA with the nine competitor algorithms on the CEC2017 test suite in '
        '10 and 30 dimensions. The complete statistical results, including the best value, mean value, '
        'and standard deviation of each algorithm on every function, are reported in Tables A3 and A4 of '
        'Appendix A, where the best mean value on each function is highlighted in bold. Table 3 '
        'summarizes the average Friedman rankings and the corresponding p-values, and Table 4 counts the '
        'win/tie/loss results of the Wilcoxon rank-sum test between MSSBOA and each competitor at the '
        '0.05 significance level.'
    )})
    ap({'table': st['tab_friedman']})
    ap({'table': st['tab_wilcoxon']})
    ap({'p': st['comparison_discussion']})
    ap({'p': (
        'Figure 6 and Figure 7 depict the average convergence curves of all algorithms on six '
        'representative functions in 10 and 30 dimensions, respectively, where the vertical axis is drawn '
        'in the logarithmic scale. It can be observed that MSSBOA descends noticeably faster than the '
        'basic SBOA in the early stage benefiting from the GPS initialization and the EDS guidance, and '
        'keeps refining the solution in the later stage when most competitors have stagnated, which is '
        'attributed to the ERM strategy continuously injecting vitality and accuracy into the population. Figure 8 '
        'presents the boxplots of the 30 independent results on the same representative functions in 30 '
        'dimensions. The boxes of MSSBOA are generally lower and narrower than those of the competitors, '
        'and contain fewer outliers, indicating that MSSBOA is not only more accurate but also more '
        'stable and robust. Figure 9 further visualizes the overall Friedman rankings of all algorithms '
        'under the two dimensionality settings (10D and 30D).'
    )})
    ap({'fig': f'{FIGS}/A_convergence_10.png',
        'caption': '**Figure 6.** Convergence curves of MSSBOA and its competitors on representative '
                   'CEC2017 functions (D = 10).', 'width_cm': 14.5})
    ap({'fig': f'{FIGS}/A_convergence_30.png',
        'caption': '**Figure 7.** Convergence curves of MSSBOA and its competitors on representative '
                   'CEC2017 functions (D = 30).', 'width_cm': 14.5})
    ap({'fig': f'{FIGS}/A_boxplot_30.png',
        'caption': '**Figure 8.** Boxplots of MSSBOA and its competitors on representative CEC2017 '
                   'functions (D = 30).', 'width_cm': 14.5})
    ap({'fig': f'{FIGS}/A_friedman_bar.png',
        'caption': '**Figure 9.** Average Friedman rankings of all algorithms on CEC2017.',
        'width_cm': 14.0})

    # ============================ 5. Portfolio application ============================
    ap({'h1': '5. Application to Cardinality-Constrained Portfolio Selection'})
    ap({'p': (
        'Portfolio selection is one of the most fundamental decision-making problems in financial '
        'management. The mean-variance framework pioneered by Markowitz {ref:markowitz} formulates the '
        'problem as the trade-off between the expected return and the risk measured by the variance of '
        'returns. However, the classical model allows an investor to hold arbitrarily many assets with '
        'arbitrarily small proportions, which is inconsistent with practice because of transaction costs, '
        'monitoring burdens, and institutional rules. Introducing the cardinality constraint that limits '
        'the number of held assets and the floor-ceiling constraints on investment proportions transforms '
        'the problem into a mixed-integer quadratic programming problem, which has been proven to be '
        'NP-hard and cannot be solved exactly within an acceptable time for realistic instance sizes '
        '{ref:chang,woodside}. Therefore, metaheuristic algorithms have become the mainstream approach '
        'for this problem {ref:fernandez,cura,deng,kalayci,portmeta}. In this section, MSSBOA is applied '
        'to the cardinality-constrained portfolio selection problem to examine its capability of solving '
        'practical financial management problems.'
    )})
    ap({'h2': '5.1. Problem Formulation'})
    ap({'p': (
        'Suppose there are $n$ candidate assets, $\\mu_i$ is the expected return of asset $i$, and '
        '$\\sigma_{ij}$ is the covariance between the returns of assets $i$ and $j$. Let $w_i$ denote the '
        'proportion of capital invested in asset $i$. The expected return and the risk of the portfolio '
        'are expressed by Equations (20) and (21).'
    )})
    ap({'eq': r'R_p=\sum_{i=1}^{n}{w_i\mu _i}', 'num': 20})
    ap({'eq': r'\sigma _p^2=\sum_{i=1}^{n}{\sum_{j=1}^{n}{w_iw_j\sigma _{ij}}}', 'num': 21})
    ap({'p': (
        'Following the classical formulation of Chang et al. {ref:chang}, the two objectives are '
        'aggregated by the risk-aversion parameter $\\lambda \\in [0,1]$, and the cardinality and '
        'floor-ceiling constraints are imposed, as shown in Equations (22) and (23).'
    )})
    ap({'eq': r'\min\ F\left( w \right)=\lambda \times \sigma _p^2-\left( 1-\lambda  \right)\times R_p', 'num': 22})
    ap({'eq': r'\mathrm{s.t.}\ \sum_{i=1}^{n}{w_i}=1,\ \ \sum_{i=1}^{n}{z_i}=K,\ \ \varepsilon z_i\le w_i\le \delta z_i,\ \ z_i\in \left\{ 0,1 \right\}', 'num': 23})
    ap({'p': (
        'where $z_i$ is a binary variable indicating whether asset $i$ is held, $K$ is the required '
        'number of held assets, and $\\varepsilon$ and $\\delta$ are the minimum and maximum investment '
        'proportions of a held asset. When $\\lambda$ approaches 1 the investor is extremely conservative '
        'and only cares about risk, while $\\lambda$ close to 0 corresponds to an aggressive investor '
        'pursuing return. In this paper, a continuous encoding with a proportional repair operator is '
        'adopted. Each individual is a real vector $z\\in [0,1]^n$; the $K$ assets with the largest '
        'components are selected to be held, and their weights are repaired by Equation (24) so that all '
        'constraints are satisfied automatically.'
    )})
    ap({'eq': r'w_i=\varepsilon +\frac{z_i}{\sum_{k\in S}{z_k}}\times \left( 1-K\varepsilon  \right),\ \ i\in S', 'num': 24})
    ap({'p': 'where $S$ denotes the index set of the $K$ selected assets. This decoding scheme guarantees '
             'the feasibility of every candidate solution without penalty parameters.'})
    ap({'h2': '5.2. Datasets and Experimental Settings'})
    ap({'p': (
        'Five publicly available benchmark datasets from the OR-Library {ref:beasley} were used, which '
        'contain the weekly return statistics of the constituent stocks of five real capital market '
        'indices from March 1992 to September 1997: Hang Seng (Hong Kong, 31 assets), DAX 100 (Germany, '
        '85 assets), FTSE 100 (UK, 89 assets), S&P 100 (USA, 98 assets), and Nikkei 225 (Japan, 225 '
        'assets), as summarized in Table 5. Following the common settings in the literature '
        '{ref:chang,cura,deng}, the cardinality was set to $K=10$, the floor and ceiling proportions '
        'were $\\varepsilon =0.01$ and $\\delta =1$, and the risk-aversion parameter was fixed to '
        '$\\lambda =0.5$, which represents a balanced investor. MSSBOA was compared with SBOA, GWO, WOA, '
        'SCA, PSO, HHO, DBO, RIME, and COA. For all algorithms, the population size was 30, the '
        'maximum number of function evaluations was 20,000, and 30 independent runs were performed on '
        'each dataset.'
    )})
    ap({'table': st['tab_portdata']})
    ap({'h2': '5.3. Results and Analysis'})
    ap({'p': st['port_discussion']})
    ap({'table': st['tab_port']})
    ap({'fig': f'{FIGS}/A_port_convergence.png',
        'caption': '**Figure 10.** Convergence curves of all algorithms on the five portfolio datasets '
                   '($\\lambda =0.5$).', 'width_cm': 14.5})
    ap({'p': (
        'To further examine the practical value of MSSBOA, the risk-return trade-off curve of the Hang '
        'Seng dataset was traced by varying the risk-aversion parameter $\\lambda$ from 0 to 1 with a '
        'step of 0.05, and each point was obtained from five independent runs. As displayed in Figure 11, '
        'the constrained frontier constructed by MSSBOA strictly dominates that of the basic SBOA in the '
        'middle-risk region and almost coincides with it at the two extreme ends, which means that under '
        'the same level of risk, the portfolios recommended by MSSBOA provide investors with higher '
        'expected returns. From the perspective of financial management, the experimental results '
        'indicate that MSSBOA can serve as a reliable computational engine of decision-support systems '
        'for fund managers: it selects a small and manageable subset of assets, satisfies the practical '
        'trading constraints automatically, and delivers stable allocation schemes across repeated runs, '
        'which is essential for the credibility of quantitative investment decisions.'
    )})
    ap({'fig': f'{FIGS}/A_frontier.png',
        'caption': '**Figure 11.** Cardinality-constrained risk-return frontiers obtained by MSSBOA and '
                   'SBOA on the Hang Seng dataset.', 'width_cm': 11.0})

    # ============================ 6. Conclusion ============================
    ap({'h1': '6. Conclusions'})
    ap({'p': (
        'Aiming at the shortcomings of the recently proposed secretary bird optimization algorithm, '
        'including the non-uniform random initialization, the blind differential search in the early '
        'hunting stage, and the rapid loss of population diversity in the later stage, this paper '
        'proposed a multi-strategy variant called MSSBOA. The good point set initialization strategy '
        'generates a uniformly distributed initial population from number theory; the elite-guided '
        'differential search strategy reconstructs the undirected random walk of the first hunting stage '
        'into a guided differential move with dimension-wise crossover driven by an elite pool; and the elite refinement mechanism '
        'alternately applies an adaptive t-distribution perturbation and a quadratic interpolation '
        'operator to the global best individual. The three strategies act on different '
        'stages of the search and complement each other without raising the order of computational '
        'complexity.'
    )})
    ap({'p': st['conclusion_numbers']})
    ap({'p': (
        'Certainly, MSSBOA also has some limitations. First, the elite pool size, the crossover rate of EDS, and the perturbation '
        'amplitude of ERM are fixed empirically, and their optimal settings on a wider range of problems '
        'deserve further investigation. Secondly, the improvement of MSSBOA on high-dimensional problems '
        'is smaller than that on low-dimensional problems, and the search efficiency in '
        'very-high-dimensional spaces still needs to be strengthened. In future work, we plan to develop '
        'binary and multi-objective versions of MSSBOA, extend it to portfolio models with transaction '
        'costs and market-neutral constraints, and apply it to other business management problems such '
        'as supply chain network design and project scheduling.'
    )})

    # ============================ back matter ============================
    ap({'backmatter': [
        '**Author Contributions:** Conceptualization, X.C.; methodology, X.C.; software, X.C.; validation, '
        'X.C.; formal analysis, X.C.; investigation, X.C.; resources, X.C.; data curation, X.C.; '
        'writing—original draft preparation, X.C.; writing—review and editing, X.C.; visualization, X.C. '
        'The author has read and agreed to the published version of the manuscript.',
        '**Funding:** This research received no external funding.',
        '**Institutional Review Board Statement:** Not applicable.',
        '**Informed Consent Statement:** Not applicable.',
        '**Data Availability Statement:** The CEC2017 benchmark functions are publicly available, and the '
        'portfolio datasets can be obtained from the OR-Library. The source code is available from the '
        'author on reasonable request.',
        '**Conflicts of Interest:** The author declares no conflicts of interest.',
    ]})
    return B
