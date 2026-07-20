# Forecasting Supply Chain Disruptions Using Supplier-Level Transaction Data: A Machine Learning Approach

[Author names and affiliations blinded for peer review]

**Abstract.** Operations executives typically monitor supply chain risk with aggregate barometers—purchasing managers' delivery-time surveys and global pressure indices—or with managerial judgment. Aggregation, however, discards the supplier-level heterogeneity, network interactions, and nonlinearity that matter most for anticipating disruptions. We propose a microforecasting approach that forecasts the network-wide supply disruption rate directly from a large panel of supplier-level transaction signals. Using weekly data on 8,437 suppliers in 41 countries from a global manufacturer's procurement platform—2.6 million supplier-week observations drawn from 14.8 million purchase orders—we train machine learning models on lead-time deviations at the supplier level. Random forest reduces out-of-sample mean squared error relative to an autoregressive benchmark by 29.4% on average across horizons of one to eight weeks, and by 38.2% one week ahead. Supplier-level signals dominate the aggregate indices firms actually use, and predictive importance concentrates in central, single-sourced, geographically concentrated, and financially fragile suppliers. Our results establish microdata-based prediction of operational aggregates as a practical paradigm for supply chain early-warning systems.

**Keywords:** supply chain disruption • forecasting • machine learning • production networks • supplier microdata • heterogeneity

# 1. Introduction

Supply chain disruption has moved from a specialist concern to a first-order strategic risk. The COVID-19 pandemic idled factories and ports on every continent, the 2021–2022 semiconductor shortage forced automakers and electronics firms to cut production for months, the grounding of the *Ever Given* in the Suez Canal in March 2021 halted roughly 12% of global trade for six days, and recent geopolitical export controls have injected policy risk into technology supply chains. These events are costly: supply chain glitches are associated with abnormal stock returns of approximately $-10\%$ and persistent declines in operating performance (Hendricks and Singhal 2003, 2005). They are also recurrent—rare only individually, frequent in aggregate (Simchi-Levi et al. 2014). For operations executives, anticipating when the supply network will seize up—even a few weeks ahead—is therefore among the most valuable forecasting problems in modern management, because lead time on the warning is lead time for mitigation: expediting freight, releasing buffer inventory, qualifying alternate sources, and reallocating constrained supply.

Yet the instruments that firms actually use to anticipate disruptions are strikingly coarse. Practitioners and forecasters rely predominantly on aggregate barometers—the Purchasing Managers' Index (PMI) supplier delivery times subindex, or the Federal Reserve Bank of New York's Global Supply Chain Pressure Index (GSCPI) (Benigno et al. 2022)—or on managers' judgment. These aggregates are useful summaries of the state of global logistics, but they are constructed by averaging: survey responses are pooled across purchasing managers, and pressure indices blend freight rates and survey diffusion indices across countries. Averaging discards exactly the information that theory suggests matters for disruption dynamics. Production-network research shows that aggregate fluctuations originate in idiosyncratic shocks to individual, disproportionately important firms and propagate through input–output linkages (Gabaix 2011, Acemoglu et al. 2012, Baqaee and Farhi 2019). Heterogeneity across suppliers, interactions among them, nonlinear amplification, and regime shifts during crises are all invisible in an aggregate index. Moreover, survey-based aggregates arrive with publication delays and are subject to revision, whereas the transaction records sitting in a firm's own procurement systems are available essentially in real time.

In this paper, we propose a microforecasting approach for supply chains: we forecast a network-wide operational aggregate—the weekly Supply Disruption Rate ($SDR_t$), the percentage of purchase orders due in a week that are delivered more than seven days late or cancelled—directly from a large panel of supplier-level transaction signals, using machine learning (ML) methods designed for high-dimensional prediction. The approach is the supply chain analogue of forecasting gross domestic product growth from firm-level accounting earnings: instead of first aggregating microdata into an index and then forecasting with the index, we hand the entire cross-section of supplier signals to methods that can exploit heterogeneity, sparsity, interactions, and nonlinearity. Through a research collaboration with a global electronics and industrial manufacturing group and its business-to-business (B2B) procurement platform, we assemble a weekly panel of 8,437 active suppliers in 41 countries over 2018W1–2025W26 (391 weeks), comprising 2.6 million supplier-week observations constructed from a purchase-order (PO) database of 14.8 million POs. Our primary supplier-level predictor is the order-to-delivery lead-time deviation from each supplier's trailing 52-week norm, complemented by fill rates, PO rejection rates, quote response times, requested price revisions, and payment delay incidence. To manage dimensionality, an elastic-net screening step (Zou and Hastie 2005) preselects 1,200 suppliers, yielding a predictor vector of dimension 2,405; we then apply the least absolute shrinkage and selection operator (LASSO), adaptive LASSO (adaLASSO), Ridge, elastic net, random forest (RF), and gradient boosted regression trees (GBRT) to forecast $SDR_{t+h}$ at horizons $h = 1, 2, 4, 8$ weeks.

The gains are large, statistically significant, and robust. Over an out-of-sample period of 235 weeks (2021W1–2025W26), the RF model achieves mean squared error (MSE) ratios relative to an autoregressive (AR) benchmark of 0.618, 0.674, 0.729, and 0.803 at $h = 1, 2, 4, 8$, respectively—an average MSE reduction of 29.4%, and a reduction of 38.2% one week ahead. All penalized linear models also beat the AR benchmark at every horizon, but the nonlinear tree ensembles dominate: RF is best at $h = 1, 2, 4$ and on average, whereas GBRT is best at the eight-week horizon (MSE ratio 0.797). The advantage of microdata over aggregation is equally stark. A value-weighted aggregate of the same platform lead-time data *fails to improve* on the AR benchmark at any horizon (MSE ratios above 1.06), and the aggregate indices firms actually consult help only marginally: at $h = 1$, the supplier-level micro approach beats the aggregate platform index by 41.8%, the PMI supplier delivery times subindex by 34.5%, and the GSCPI by 32.9%. Pooling the GSCPI with supplier microdata adds little beyond microdata alone (MSE ratio 0.611 versus 0.618 at $h = 1$) and slightly worsens performance at $h = 8$ (0.812 versus 0.803). A principal components regression (PCR) that compresses the supplier panel into common factors is competitive at the one-week horizon (0.641) but deteriorates sharply as the horizon lengthens (1.421 at $h = 4$ and 1.874 at $h = 8$), which indicates that the predictive content of supplier microdata at longer horizons resides in idiosyncratic, granular variation rather than in common factors. Finally, the predictability is strongly time varying: microforecasting gains concentrate in volatile episodes—the COVID-19 aftershocks, the semiconductor shortage, and the Red Sea shipping crisis—precisely when accurate early warning is most valuable.

Our contributions to the literature manifest across three dimensions. First, we develop the first microforecasting framework for supply chain disruption that maps a large panel of supplier-level transaction signals directly into forecasts of a network-wide disruption rate using ML, and we document economically large gains: an average MSE reduction of approximately 29% relative to the AR benchmark, reaching 38% at the one-week horizon. Second, we show that supplier-level microdata dominate the aggregate approaches that both practice and research currently employ—the value-weighted platform aggregate, the PMI supplier delivery times subindex, the GSCPI, and factor compression via PCR at longer horizons—thereby quantifying the informational cost of aggregation in operational forecasting. Third, we open the black box: a variable importance analysis shows that sectoral importance shifts systematically with the horizon (logistics and transportation suppliers dominate short-horizon forecasts, whereas upstream electronic component suppliers dominate long-horizon forecasts), that sector-level importance rises with Domar-style network centrality, and that supplier-level importance concentrates among suppliers that are network central, single sourced, geographically risky, and financially fragile. These results provide new microfoundations for supply chain risk monitoring: they tell managers *which* suppliers to instrument in an early-warning dashboard and *where* predictive risk concentrates.

Our diagnostic results connect the forecasting evidence to theory. Production-network models imply that shocks to central, upstream, or weakly substitutable suppliers propagate disproportionately (Acemoglu et al. 2012, Baqaee and Farhi 2019, Elliott et al. 2022), and empirical work documents such propagation following natural disasters (Barrot and Sauvagnat 2016, Carvalho et al. 2021). If disruption of the network aggregate is the endpoint of propagation processes that begin at individual suppliers, then supplier-level signals should contain early-warning content that aggregation destroys—and the suppliers whose signals matter most should be exactly those that theory identifies as propagation-relevant. Our variable importance regressions confirm both predictions. We emphasize that these relationships are correlational rather than causal: importance in a predictive model identifies where forecasting signal resides, not the counterfactual effect of intervening on a supplier. Even so, the alignment between predictive importance and network-theoretic centrality is, to our knowledge, the first evidence of its kind in an operational setting.

The remainder of the paper proceeds as follows. Section 2 overviews the related literature and develops the rationale for supplier-level transaction signals. Section 3 describes the data, the construction of predictors and the target, and the timing protocol, whereas Section 4 details the forecasting models and the evaluation design. The main results are presented in Section 5, followed by comparisons with aggregate approaches in Section 6 and the variable importance analysis in Section 7. Section 8 concludes. Supplementary materials are available in the Online Appendix.

# 2. Related Literature and Rationale

## 2.1. Supply Chain Disruptions and Resilience

A substantial literature documents the incidence, cost, and management of supply chain disruptions. Hendricks and Singhal (2003) show that public announcements of supply chain glitches are associated with abnormal shareholder losses of about 10%, and Hendricks and Singhal (2005) show that disrupted firms experience depressed stock performance and elevated equity risk for up to two years afterward. Conceptual frameworks classify disruption risks and mitigation levers (Chopra and Sodhi 2004, Kleindorfer and Saad 2005, Tang 2006), and analytical work characterizes optimal mitigation and contingency strategies, including inventory buffers, dual sourcing, and contingent rerouting (Tomlin 2006), as well as sourcing design in multitier networks under disruption risk (Ang et al. 2017). Craighead et al. (2007) argue that disruption severity is shaped by supply network design characteristics—density, complexity, and node criticality—a theme echoed by Bode and Wagner (2015), who show empirically that upstream complexity increases disruption frequency. Simchi-Levi et al. (2014) propose the risk-exposure-index approach for prioritizing mitigation when disruption probabilities are unknowable, and Simchi-Levi et al. (2015) implement it in the automotive supply chain at Ford. The COVID-19 pandemic renewed attention to resilience and viability of intertwined supply networks (Ivanov and Dolgui 2020) and to the redesign of global network footprints (Cohen and Lee 2020).

This literature is primarily concerned with *ex ante* design and *ex post* response. The complementary question we study—whether disruptions of the network aggregate can be *forecast* at operational lead times from data the firm already possesses—has received far less attention, despite its immediate managerial value. Osadchiy et al. (2016) show that supply chain structure transmits systematic demand risk upstream, which suggests that network position should shape predictive relationships, a hypothesis we test directly in Section 7.

## 2.2. Production Networks and Shock Propagation

A second stream, in economics, studies how microlevel shocks generate aggregate fluctuations. Hulten (1978) establishes that, in efficient economies, a firm's contribution to aggregate output responds to its shock in proportion to its sales share (its Domar weight). Gabaix (2011) shows that when the firm size distribution is fat tailed, idiosyncratic shocks to large firms do not wash out; Acemoglu et al. (2012) show that asymmetric input–output networks propagate and amplify idiosyncratic shocks; and Baqaee and Farhi (2019) show that, beyond Hulten's first-order benchmark, nonlinearities in production networks make aggregate outcomes disproportionately sensitive to shocks at complementary, weakly substitutable inputs. Elliott et al. (2022) model endogenous supply network formation and show that equilibrium networks are systematically fragile: firms economize on redundancy, leaving the system near a criticality threshold at which small shocks trigger large, discontinuous disruption cascades. Empirically, Barrot and Sauvagnat (2016) and Carvalho et al. (2021) document strong propagation of natural-disaster shocks through customer–supplier links, with input specificity governing the magnitude, and Serpa and Krishnan (2018) show productivity spillovers along supply chains. In operations, related empirical work documents how order flow transforms as it moves through the chain (Cachon et al. 2007, Bray and Mendelson 2012).

Two implications of this literature drive our design. First, if aggregate disruption is generated granularly—by shocks at specific suppliers filtered through network topology—then supplier-level data are not merely a disaggregated version of an index; they contain predictive information that the index provably lacks whenever weights, interactions, or nonlinearities matter. Second, the theory makes sharp cross-sectional predictions about *where* the signal should reside: at central, upstream, weakly substitutable, and fragile nodes. Our Section 7 takes these predictions to the data.

## 2.3. Machine Learning and Data-Driven Operations

A third stream applies ML and rich microdata to operational prediction and decision making. Kesavan et al. (2010) show that incorporating inventory and gross margin microdata improves sales forecasts for U.S. retailers—an early demonstration that operational microdata sharpen forecasts of firm-level aggregates. Ban and Rudin (2019) derive feature-based newsvendor policies that learn directly from data, and Bertsimas and Kallus (2020) develop a general framework linking predictive ML to prescriptive optimization. Mullainathan and Spiess (2017) articulate the econometric perspective: ML excels at $\hat{y}$ problems—high-dimensional prediction with regularization and validation—which is precisely the structure of our task. Methodologically, we draw on the LASSO (Tibshirani 1996), the elastic net (Zou and Hastie 2005), the adaptive LASSO (Zou 2006), random forests (Breiman 2001), gradient boosting (Friedman 2001), and the general statistical learning toolkit (Hastie et al. 2009).

Relative to this stream, our contribution is to change the *object* of prediction: rather than forecasting a firm-level quantity (sales, demand, inventory), we forecast a network-wide operational aggregate from the full cross-section of node-level signals, and we then interrogate the fitted models for what they reveal about the network. In this sense the paper imports the "microdata for macroprediction" logic into operations management.

## 2.4. Why Supplier-Level Transaction Signals Should Forecast Network Disruptions

Why should the cross-section of supplier-level transaction signals forecast the network-wide disruption rate better than the aggregates that firms currently monitor? We present four main reasons: (i) a *direct mechanical link*—the network disruption rate is, by construction, an aggregate of supplier-level delivery outcomes, so supplier-level lead-time deviations are the elementary constituents of the target, and forecasting the aggregate from its own microcomponents avoids the errors introduced when an index averages away compositional shifts; (ii) an *informational link*—deteriorating transaction behavior at a supplier (lengthening lead times, slower quote responses, requests for price revisions, payment delays) reveals unobserved operational or financial stress *before* that stress matures into missed deliveries and propagates to other nodes, so supplier signals carry early-warning content about future disruptions elsewhere in the network, not merely about the supplier's own deliveries; (iii) a *propagation link*—production-network theory implies that the mapping from supplier states to aggregate disruption is heterogeneous (a one-day slip at a central single-sourced chip supplier is not a one-day slip at a peripheral packaging vendor), interactive (simultaneous stress at complementary suppliers is worse than the sum of the parts), and nonlinear (cascades trigger at thresholds), and value-weighted or survey-based aggregation destroys exactly these features, whereas ML methods trained on the microdata can exploit them (Acemoglu et al. 2012, Baqaee and Farhi 2019, Elliott et al. 2022); and (iv) a *data availability and timeliness advantage*—transaction records are generated continuously as a byproduct of procurement operations, are free of the publication delays and retrospective revisions that afflict the PMI and the GSCPI, and are already owned by the firm, so the marginal cost of exploiting them is essentially computational.

These four reasons also discipline our empirical design. Reason (i) motivates lead-time deviations as the primary predictor; reason (ii) motivates testing predictive content at horizons beyond one week; reason (iii) motivates nonlinear learners and the comparison with linear and factor-based compressions of the same data; and reason (iv) motivates the timing protocol of Section 3.4, which ensures that every predictor is observable at the forecast origin.

# 3. Data

## 3.1. The Procurement Platform and Panel Construction

Our data come from a research collaboration with a global electronics and industrial manufacturing group (anonymized per the collaboration agreement) and its B2B procurement platform, through which the group's business units transact with their direct suppliers. The platform records the full life cycle of every PO: creation, supplier acknowledgment, requested and confirmed delivery dates, shipment events, goods receipt, quality acceptance, invoicing, and payment. We extract the universe of POs created between 2015W1 and 2025W26; the pre-2018 records are used only to initialize trailing supplier norms, and the estimation panel covers 2018W1–2025W26, a span of 391 weeks.[^1]

The resulting panel contains 8,437 active suppliers in 41 countries, where a supplier is classified as active if it receives at least 26 POs per year in at least three sample years. The panel is unbalanced—suppliers enter and exit as sourcing relationships change—and comprises 2.6 million supplier-week observations, corresponding to an average of roughly 6,650 suppliers transacting in any given week. The underlying PO database contains 14.8 million POs, or approximately 37,850 POs due for delivery in an average week. Suppliers are classified by the platform's commodity taxonomy into nine sectors: electronic components; logistics and transportation; chemicals and materials; machinery and equipment; metals and mining; packaging; electrical equipment; plastics and rubber; and textiles and apparel. Geographically, the largest supplier concentrations are in China (21.4% of suppliers), the United States (14.2%), Germany (9.8%), and Japan (7.1%). Summary statistics for the panel are reported in Table A.1 of Online Appendix A.

[^1]: Weeks follow the ISO 8601 convention, so a calendar year contains 52 or 53 weeks; 2020 contains 53 ISO weeks. All weekly quantities are computed on ISO week boundaries (Monday–Sunday).

## 3.2. Supplier-Level Predictors

For each supplier $i$ and week $t$, we construct six transaction signals. The primary predictor is the order-to-delivery *lead-time deviation*: letting $L_{i,t}$ denote the mean realized order-to-delivery lead time (in days) of supplier $i$'s POs receipted in week $t$, we define $x_{i,t} = (L_{i,t} - \bar{L}_{i,t}^{52})/\sigma_{i,t}^{52}$, where $\bar{L}_{i,t}^{52}$ and $\sigma_{i,t}^{52}$ are the mean and standard deviation of supplier $i$'s lead times over the trailing 52 weeks ending in week $t-1$. Standardizing by the supplier's own trailing norm removes persistent cross-supplier differences in product complexity and shipping distance and expresses each signal as an abnormal deviation, in supplier-specific standard deviation units. Mirroring the change-based construction used when forecasting macroeconomic aggregates from firm-level earnings growth, our primary specification uses the first differences $\Delta x_{i,t} = x_{i,t} - x_{i,t-1}$ and their one-period lags $\Delta x_{i,t-1}$; differencing sharpens the timing of incipient stress and removes any residual low-frequency drift in supplier norms.

The five complementary signals are the *fill rate* (fraction of ordered quantity delivered by the confirmed date; sample mean 94.7%), the *PO rejection rate* (fraction of POs the supplier declines or fails to acknowledge within five business days; mean 1.8%), the *quote response time* (days from request for quotation to supplier quote; mean 3.4 days), the *requested price revision* incidence (fraction of open POs on which the supplier requests a price adjustment; mean 2.9%), and the *payment delay incidence* (indicator that the supplier requests early payment or factoring on outstanding invoices; mean 4.1%). These signals enter the elastic-net screening stage described below and the robustness specifications of Section 5.3; the primary forecasting specification uses lead-time deviations and their lags, which we find carry the dominant share of predictive content. All supplier-level signals are winsorized at the 1st and 99th percentiles of their training-window distributions.[^2]

[^2]: Winsorization thresholds are computed within each rolling training window only, so no out-of-sample information enters the transformation. Missing supplier-weeks (no POs receipted) are set to zero deviation, with an accompanying activity indicator absorbed in the screening stage.

Because the full cross-section of 8,437 suppliers with two terms each would yield a predictor space of more than 16,800 columns, we reduce computational cost with a preselection step: within each rolling training window, an elastic-net regression of $SDR_{t+1}$ on all supplier signals (Zou and Hastie 2005) screens the panel, and we retain the 1,200 suppliers with the largest selection frequencies across the elastic-net regularization path. The preselected set spans all nine sectors and 38 of the 41 countries, and it is stable over time: the median week-over-week turnover of the selected set is 1.8%. Robustness checks with 800 suppliers, 2,000 suppliers, and the full panel are summarized in Section 5.3 and detailed in Online Appendix B.3.

## 3.3. The Network-Wide Supply Disruption Rate

Our forecast target is the weekly network-wide Supply Disruption Rate, $SDR_t$, defined as the percentage of POs due in week $t$ that are delivered more than 7 days late or cancelled. The 7-day threshold reflects the collaborating group's own service-level definition of a disrupted order; results with a 14-day threshold are similar and are reported in Online Appendix B.1.[^3] Over the full sample, $SDR_t$ has a mean of 6.9% and a standard deviation of 3.8%; the series is persistent (first-order autocorrelation 0.93) and strongly episodic. It reaches its sample peak of 23.4% in 2021W34, at the height of the semiconductor shortage and the pandemic-related closure of major Chinese port terminals, and its sample minimum of 3.2% in 2019W22. The formal definition of the target and of the forecasting mapping appears in Section 4.

[^3]: Cancellation is included because cancelled POs typically force emergency re-sourcing and hence represent a disruption of supply from the buyer's perspective, even though no late delivery is recorded.

## 3.4. Timing Protocol and the Absence of Look-Ahead Bias

A forecasting exercise is only as credible as its information timing, so we adopt a strict protocol that parallels the release-timing discussions in the macroeconomic microforecasting literature. Two features of transaction data make the protocol clean. First, every PO event in the platform is timestamped at entry, and the platform retains immutable weekly ledger snapshots; we build all predictors from the snapshot taken at the end of the forecast origin week $t$, so the predictor set reflects exactly what a decision maker logging into the platform at that moment could have seen. Second, unlike survey-based indices, transaction records are never revised: a goods receipt booked in week $t$ remains booked in week $t$. Predictors are lagged so that all supplier signals are observable at the forecast origin: forecasting $SDR_{t+h}$ uses $\Delta x_{i,t}$, $\Delta x_{i,t-1}$, and lags of $SDR_t$, all measurable from the week-$t$ snapshot. The target $SDR_{t+h}$ is computed from POs *due* in week $t+h$, whose disruption status is determined only in or after week $t+h$; there is no mechanical overlap between the information sets. By contrast, the PMI is released in the first week of the following month, and the GSCPI is released monthly and back-revised as source series are updated; when we use these indices as competing predictors in Section 6, we align them to their real-time release dates so that the comparison does not favor our approach.[^4]

[^4]: The GSCPI is monthly, so in weekly regressions it enters as a step function holding the most recently *released* value, not the current-month value that would only be published later. The same convention applies to the PMI supplier delivery times subindex.

## 3.5. Volatile Episodes and Summary Statistics

Three volatile episodes play a prominent role in the time-varying analysis of Section 5.2: the COVID-19 aftershocks (2020W10–2021W26), during which pandemic-related closures and transportation constraints reverberated through the network; the semiconductor shortage (2021W1–2022W26), during which allocation and decommitment by upstream component suppliers dominated; and the Red Sea shipping crisis (2023W50–2024W26), during which rerouting around the Cape of Good Hope lengthened ocean transit times abruptly. During these episodes, the mean of $SDR_t$ rises to 11.7%, compared with 5.2% in the remaining weeks, and the cross-sectional dispersion of supplier lead-time deviations roughly doubles. Full summary statistics of the target, the supplier signals, and their episode-conditional moments are provided in Online Appendix A.

# 4. Forecasting Models

## 4.1. The Microforecasting Framework

We cast the problem as direct $h$-step-ahead prediction of the network aggregate from the supplier cross-section:

$$SDR_{t+h} = F_h(\mathbf{X}_t; \boldsymbol{\gamma}) + \varepsilon_{t+h}, \quad t = 1, 2, \ldots, T-h, \qquad (1)$$

where $h$ is the forecast horizon in weeks, $F_h(\cdot)$ is a horizon-specific prediction function with parameters $\boldsymbol{\gamma}$, $\varepsilon_{t+h}$ is the forecast error, and $\mathbf{X}_t$ is the $(N+1) \times 1$ predictor vector stacking the supplier-level lead-time deviations $\Delta x_{i,t}$ for the 1,200 preselected suppliers, their one-period lags $\Delta x_{i,t-1}$, and four lags of $SDR_t$, together with a constant; with $N = 2 \times 1{,}200 + 4 = 2{,}404$, the dimension of $\mathbf{X}_t$ is 2,405. Because the initial rolling training window contains 156 weekly observations, the predictor dimension exceeds the time-series length by more than an order of magnitude, which makes regularized and nonparametric ML methods essential rather than optional (Mullainathan and Spiess 2017).

The target is the network-wide disruption rate

$$SDR_t = 100 \times D_t / N_t, \qquad (2)$$

where $D_t$ is the number of POs due in week $t$ that are delivered more than 7 days late or are cancelled, and $N_t$ is the total number of POs due in week $t$.

## 4.2. The Autoregressive Benchmark

Because $SDR_t$ is highly persistent, the natural benchmark is a univariate AR model estimated by ordinary least squares:

$$SDR_{t+h} = \mu_h + A(L)\, SDR_t + \varepsilon_{t+h}, \qquad (3)$$

where $\mu_h$ is an intercept and $A(L)$ is a lag polynomial whose order is selected in each training window by the Bayesian information criterion (BIC), with a maximum of eight lags; the selected order is four in most windows. The AR benchmark is demanding: it captures the persistence and mean reversion of the disruption rate, and—as Section 6 shows—several widely used aggregate indices fail to improve on it.

## 4.3. Penalized Linear Models

Our first family of microforecasting models is linear in $\mathbf{X}_t$ with penalized estimation. The LASSO (Tibshirani 1996) solves

$$\hat{\boldsymbol{\beta}} = \arg\min_{\boldsymbol{\beta}} \sum_{t}\left(SDR_{t+h} - \mathbf{X}_t'\boldsymbol{\beta}\right)^2 + \lambda \sum_{j}|\beta_j|, \qquad (4)$$

where $\lambda \geq 0$ is a tuning parameter governing the strength of the $\ell_1$ penalty, which shrinks coefficients toward zero and sets many exactly to zero, performing variable selection. Ridge regression replaces the $\ell_1$ penalty with the $\ell_2$ penalty $\lambda \sum_j \beta_j^2$, shrinking without selecting; the elastic net uses a convex combination of the $\ell_1$ and $\ell_2$ penalties, which stabilizes selection among correlated suppliers (Zou and Hastie 2005); and the adaptive LASSO (adaLASSO) reweights the $\ell_1$ penalty by first-stage coefficient magnitudes, $\lambda \sum_j |\beta_j|/|\tilde{\beta}_j|^\tau$, which restores oracle selection properties (Zou 2006). All tuning parameters are chosen on the validation segment of each rolling window, as described in Section 4.5.

## 4.4. Tree-Based Ensembles

Linear models cannot represent the interactions and threshold effects that production-network theory predicts, so our second family comprises tree-based ensembles. The random forest (Breiman 2001) averages a large number of regression trees, each grown on a bootstrap resample of the training window with a random subset of predictors considered at each split; averaging decorrelated trees reduces variance while preserving the trees' ability to capture nonlinearities and high-order interactions among supplier signals. We grow 2,000 trees with the number of candidate predictors per split set to the square root of the predictor dimension (49) and tune the minimum leaf size on the validation segment. Gradient boosted regression trees (Friedman 2001) instead build shallow trees sequentially, each fit to the residuals of the current ensemble, with a learning rate of 0.05, a maximum tree depth of three, and the number of boosting rounds chosen by early stopping on the validation segment. Both methods are standard in the statistical learning literature (Hastie et al. 2009); their comparative advantage here is that a split-based model can express statements such as "long-horizon disruption risk is elevated when lead-time deviations at central electronic component suppliers and at logistics providers are simultaneously positive," which no linear aggregate can encode.

## 4.5. Evaluation Design

We evaluate all models with a rolling-window scheme. The first estimation window covers the first 156 weeks of the sample, and the window rolls forward one week at a time with its length held fixed, so every forecast is produced strictly out of sample; the out-of-sample evaluation period runs from 2021W1 through 2025W26, providing 235 weekly forecast evaluations at each horizon. Within each rolling window, we use a chronological 80% training / 20% validation split for hyperparameter tuning: hyperparameters ($\lambda$, elastic-net mixing, penalty exponents, leaf sizes, boosting rounds) are chosen to minimize validation MSE, and the model is then refit on the full window before forecasting. Preselection, winsorization, tuning, and estimation are all repeated within each window, so no information from the evaluation period leaks backward.

Out-of-sample accuracy is measured by the mean squared error

$$MSE = \frac{1}{T-h}\sum_{t=1}^{T-h}\left(SDR_{t+h} - \widehat{SDR}_{t+h}\right)^2, \qquad (5)$$

where the sum runs over the out-of-sample forecast origins, $\widehat{SDR}_{t+h}$ is the model's forecast, and $T-h$ denotes the number of evaluated forecasts at horizon $h$. We report each model's MSE as a *ratio* to the AR benchmark's MSE, so that values below one indicate an improvement over the benchmark. Because the AR model is nested in the linear microforecasting models, we assess statistical significance with the Clark and West (2007) adjusted test for equal predictive accuracy in nested models, using one-sided $p$-values; results using the Diebold and Mariano (1995) test, which is conservative in nested comparisons, are similar and reported in Online Appendix B.2.[^5]

[^5]: For the tree-based models the nesting is not exact, but the AR lags are included in $\mathbf{X}_t$, so the Clark–West correction for the noise introduced by estimating the larger model remains the appropriate default; the Diebold–Mariano statistics lead to identical conclusions at the 5% level.

# 5. Empirical Evidence

## 5.1. Microforecasting versus the Autoregressive Benchmark

Table 1 presents the out-of-sample MSE ratios of the six microforecasting models relative to the AR benchmark at horizons $h = 1, 2, 4, 8$ weeks, together with the average across horizons. Three findings stand out.

Table 1. Forecasting Performance of Microforecasting Models: Network-Wide Supply Disruption Rate (MSE Ratio Relative to the AR Benchmark)

| Model | $h=1$ | $h=2$ | $h=4$ | $h=8$ | Average |
|---|---|---|---|---|---|
| adaLASSO | 0.671** | 0.729** | 0.798** | 0.874* | 0.768 |
| LASSO | 0.652** | 0.718** | 0.784** | 0.861* | 0.754 |
| Elastic Net | 0.648** | 0.722** | 0.791* | 0.869* | 0.758 |
| Ridge | 0.694** | 0.741** | 0.802** | 0.881* | 0.780 |
| RF | 0.618*** | 0.674*** | 0.729** | 0.803** | 0.706 |
| GBRT | 0.633*** | 0.689** | 0.741** | 0.797** | 0.715 |

*Notes.* This table reports the ratio of each microforecasting model's out-of-sample MSE to that of the AR benchmark in Equation (3) for forecasting the network-wide supply disruption rate $SDR_{t+h}$ at horizons $h = 1, 2, 4, 8$ weeks; values below one indicate an improvement over the benchmark. The out-of-sample period is 2021W1–2025W26 (235 weeks), with rolling-window estimation and an 80%/20% chronological training/validation split for hyperparameter tuning within each window. Predictors are the lead-time deviations and their one-period lags for the 1,200 elastic-net-preselected suppliers plus four lags of $SDR_t$. The Average column reports the simple mean of the ratios across the four horizons. \*\*\*, \*\*, and \* denote statistical significance at the 1%, 5%, and 10% levels, respectively, based on one-sided Clark and West (2007) tests of equal predictive accuracy against the nested AR benchmark.

First, *every* microforecasting model beats the AR benchmark at *every* horizon, with MSE ratios ranging from 0.618 to 0.881, and every improvement is statistically significant at the 10% level or better by the Clark and West (2007) test. The information in supplier-level lead-time deviations is thus not an artifact of a particular estimator: sparse selection (LASSO, adaLASSO), dense shrinkage (Ridge), correlated-group selection (elastic net), and nonparametric ensembles (RF, GBRT) all extract genuine predictive content beyond the history of the disruption rate itself.

Second, the nonlinear ensembles dominate the penalized linear models. RF attains the best performance at $h = 1, 2, 4$—MSE ratios of 0.618, 0.674, and 0.729—and the best average ratio of 0.706, an average MSE reduction of 29.4% relative to the AR benchmark; at the one-week horizon the reduction reaches 38.2%. GBRT is a close second on average (0.715) and is the best model at the eight-week horizon (0.797). The best linear model, LASSO, achieves an average ratio of 0.754, so nonlinearity contributes roughly an additional 6.4% relative MSE reduction beyond what sparse linear aggregation of the same signals delivers. This gap is consistent with the propagation mechanisms of Section 2.4: threshold effects and interactions among suppliers are exactly what trees can represent and linear combinations cannot. In economic terms, at $h = 1$ the RF root mean squared error is 1.09 percentage points of the disruption rate, compared with 1.39 percentage points for the AR benchmark—against a sample mean disruption rate of 6.9%, a material sharpening of the early-warning signal.

Third, the gains decay with the horizon but remain economically and statistically significant eight weeks ahead: the RF ratio rises from 0.618 at $h = 1$ to 0.803 at $h = 8$, and the GBRT ratio to 0.797. The decay is expected—supplier-level stress signals are most informative about imminent deliveries—but a 20% MSE reduction two months ahead is operationally valuable, because eight weeks approximates the replenishment lead time for many of the group's intercontinental supply lanes, which is the window within which expediting, re-sourcing, and allocation decisions must be made (Tomlin 2006).

Expressed as out-of-sample fit, the RF forecast attains an out-of-sample $R^2$ of 66.1% at $h = 1$, versus 45.2% for the AR benchmark; the complementary accuracy metrics discussed in Section 5.3 (mean absolute error and out-of-sample $R^2$ at all horizons) tell the same story.

## 5.2. Time-Varying Predictability

Averages over a 235-week evaluation period conceal substantial time variation, and the time variation is informative about *when* microforecasting earns its keep. Figure 1 shows the weekly absolute out-of-sample forecast errors of the RF microforecasting model and the AR benchmark at $h = 1$, with the volatile episodes shaded.

![Figure 1. (Color online) Absolute Forecast Errors of Microforecasting (RF) vs. AR Benchmark: Network-Wide Supply Disruption Rate, h = 1](/tmp/claude-0/-home-user-xixi/c700b243-db1e-53b1-9664-970dce4c2150/scratchpad/fig1_paper2.png)

*Notes.* The figure plots the weekly absolute out-of-sample forecast errors, in percentage points of the supply disruption rate, of the random forest (RF) microforecasting model and the autoregressive (AR) benchmark at the one-week horizon over the evaluation period 2021W1–2025W26. Shaded bands mark the volatile episodes: the overlap of the COVID-19 aftershocks with the evaluation period and the semiconductor shortage (2021W1–2022W26), and the Red Sea shipping crisis (2023W50–2024W26). The RF errors are computed from the same rolling-window design as Table 1.

Two patterns emerge. First, the two error series track each other closely in calm periods, whereas the AR errors spike far above the RF errors when the disruption rate accelerates: the largest gap occurs around the 2021W34 peak of 23.4%, when the AR benchmark—anchored to its own lags—systematically underpredicts the run-up, whereas supplier-level lead-time deviations had begun deteriorating four to six weeks earlier. Restricting Equation (5) to episode weeks, the RF MSE ratio at $h = 1$ is 0.583 within the volatile episodes, versus 0.789 in the remaining calm weeks; because volatile weeks dominate squared errors, the full-sample ratio of 0.618 is closer to the episode value. Microforecasting is therefore most valuable precisely when forecast failures are most costly, a property that aggregate indices—which are themselves smoothed—cannot deliver.

Second, the horizon profile of the gains differs across episodes in a way that matches the underlying economics. During the semiconductor shortage (2021W1–2022W26), the gains are largest at the longer horizons: episode-specific RF MSE ratios are 0.652 at $h = 4$ and 0.688 at $h = 8$, compared with full-sample values of 0.729 and 0.803. Component decommitments by upstream suppliers were visible in lead-time deviations and quote behavior months before they matured into missed deliveries downstream, so the microdata carried unusually long-lived signal. During the Red Sea shipping crisis (2023W50–2024W26), by contrast, the gains concentrate at short horizons—episode ratios of 0.547 at $h = 1$ and 0.611 at $h = 2$, but only 0.858 at $h = 8$—because rerouting shocks arrive quickly, propagate through transit times within one to three weeks, and are partially anticipated at longer horizons even by the AR benchmark once the level of the disruption rate has adjusted. Episode-by-episode results for all models and horizons are tabulated in Online Appendix B.4.

## 5.3. Robustness

We probe the robustness of Table 1 along seven dimensions; details are provided in Online Appendix B. First, *alternative targets*: value-weighting $D_t$ and $N_t$ by PO spend, replacing the disruption rate with the mean delay in days, and computing sectoral disruption rates all preserve the ranking of models and the magnitude of the gains. Second, *alternative metrics*: mean absolute error ratios and out-of-sample $R^2$ comparisons, along with Diebold and Mariano (1995) tests, confirm the Clark–West inference. Third, *preselection intensity*: with 800 preselected suppliers the RF average MSE ratio is 0.718, with 2,000 it is 0.702, and with the full panel it is 0.699 at roughly six times the computational cost, so the 1,200-supplier screen sacrifices little. Fourth, *temporal aggregation*: at the monthly frequency the RF one-month-ahead MSE ratio is 0.694, so the result is not an artifact of weekly noise. Fifth, *subnetwork analysis*: restricting both predictors and target to the European subnetwork yields an average RF ratio of 0.734. Sixth, *excluding COVID-19 from training*: dropping 2020W10–2021W26 from every training window (while keeping the evaluation period unchanged) yields an RF ratio of 0.641 at $h = 1$, so the gains are not merely memorized pandemic dynamics. Seventh, *predictor sets*: adding the five complementary transaction signals of Section 3.2 to the lead-time deviations improves the RF average ratio modestly (to 0.698), with lead-time deviations retaining more than three-quarters of total variable importance (Table B.6).

# 6. Microforecasting versus Aggregate Approaches

The results of Section 5 establish that supplier microdata forecast network disruptions. This section asks the sharper question: is the granularity itself the source of the gains? We compare the microforecasting approach with (i) the aggregate indices that firms and forecasters actually use and (ii) a factor-based compression of our own supplier panel.

## 6.1. Aggregate Platform Index, PMI, and GSCPI

We consider three aggregate competitors, each entering an augmented version of Equation (3) as an additional predictor with lags selected by BIC. The first is a *value-weighted aggregate platform lead-time index*—the spend-weighted average of the same supplier lead-time deviations $x_{i,t}$ that feed our microforecasting models. This comparison isolates pure aggregation: identical raw data, identical timing, with the cross-section collapsed to one series. The second is the PMI supplier delivery times subindex, and the third is the GSCPI (Benigno et al. 2022), both aligned to real-time release dates as described in Section 3.4. Panels A–C of Table 2 report these aggregate models' MSE ratios; Panel D reproduces the supplier-level RF results from Table 1 for comparison, and Panel C also reports a pooled model that gives the RF both the GSCPI and the supplier microdata.

Table 2. Microdata versus Aggregate Predictors: MSE Ratios Relative to the AR Benchmark

| Predictor set | $h=1$ | $h=2$ | $h=4$ | $h=8$ |
|---|---|---|---|---|
| Panel A. Aggregate platform lead-time index | | | | |
| Value-weighted platform index | 1.062 | 1.118 | 1.204 | 1.157 |
| Panel B. Survey-based aggregate | | | | |
| PMI supplier delivery times | 0.943 | 0.981 | 1.026 | 1.094 |
| Panel C. Global pressure index | | | | |
| GSCPI | 0.921 | 0.958 | 1.011 | 1.083 |
| Pooling (GSCPI + supplier micro, RF) | 0.611 | 0.669 | 0.734 | 0.812 |
| Panel D. Supplier-level microdata | | | | |
| Supplier-level micro (RF) | 0.618 | 0.674 | 0.729 | 0.803 |

*Notes.* This table reports out-of-sample MSE ratios relative to the AR benchmark over 2021W1–2025W26 (235 weeks) at horizons $h = 1, 2, 4, 8$ weeks. Panel A augments the AR benchmark with the spend-weighted average of the same supplier-level lead-time deviations used by the microforecasting models. Panel B augments the benchmark with the Purchasing Managers' Index (PMI) supplier delivery times subindex and Panel C with the Global Supply Chain Pressure Index (GSCPI), each aligned to real-time release dates; the pooling row adds the GSCPI to the supplier-level predictor set of the RF model. Panel D reproduces the RF microforecasting results from Table 1. Values below one indicate an improvement over the AR benchmark.

The results are striking. The value-weighted platform index—built from *exactly* the same underlying transaction data as the microforecasting models—fails to improve on the AR benchmark at any horizon, with MSE ratios between 1.062 and 1.204. Aggregation does not merely dilute the signal; it destroys it. The economics is transparent: spend-weighting averages a sharply deteriorating signal at a handful of critical suppliers with thousands of stable signals elsewhere, and the compositional information—*which* suppliers are slipping—is lost, even though that composition is precisely what determines whether slippage will cascade (Acemoglu et al. 2012, Elliott et al. 2022).

The external aggregates fare somewhat better at short horizons but still add little. The PMI subindex yields ratios of 0.943 and 0.981 at $h = 1, 2$ and is counterproductive at $h = 4, 8$ (1.026, 1.094); the GSCPI yields 0.921 and 0.958 at short horizons and 1.011 and 1.083 at long horizons. At $h = 1$, the supplier-level micro approach beats the aggregate platform index by 41.8%, the PMI by 34.5%, and the GSCPI by 32.9% in MSE-ratio terms. Moreover, pooling the GSCPI with the supplier microdata adds little beyond the microdata alone—0.611 versus 0.618 at $h = 1$—and slightly worsens performance at $h = 8$ (0.812 versus 0.803), which indicates that essentially all of the aggregate indices' usable information is already contained in, and dominated by, the supplier-level signals. For a firm deciding where to invest in early-warning capability, the implication is direct: its own transaction microdata dominate the external barometers it currently purchases or monitors.

## 6.2. Principal Components Regression

A more sophisticated aggregation compresses the supplier panel into a small number of estimated common factors. We extract principal components from the 2,400 supplier-level predictor columns within each rolling window, select the number of components on the validation segment (typically 8–12), and forecast with the components in a linear regression—the standard PCR approach in diffusion-index macroforecasting. Table 3 compares PCR with RF and Ridge, the natural dense-linear comparator.

Table 3. Factor Compression versus Microforecasting: MSE Ratios Relative to the AR Benchmark

| Model | $h=1$ | $h=2$ | $h=4$ | $h=8$ |
|---|---|---|---|---|
| PCR | 0.641 | 0.892 | 1.421 | 1.874 |
| RF | 0.618 | 0.674 | 0.729 | 0.803 |
| Ridge | 0.694 | 0.741 | 0.802 | 0.881 |

*Notes.* This table reports out-of-sample MSE ratios relative to the AR benchmark over 2021W1–2025W26 at horizons $h = 1, 2, 4, 8$ weeks. PCR denotes principal components regression on the supplier-level predictor panel, with the number of components selected on the validation segment of each rolling window; RF and Ridge rows reproduce the corresponding results from Table 1. Values below one indicate an improvement over the AR benchmark.

PCR is competitive at the one-week horizon (0.641, within 4% of RF's 0.618): imminent disruptions load on a broad common deterioration—congestion, freight capacity, pandemic waves—that a few factors capture well. But PCR deteriorates sharply as the horizon lengthens, underperforming even the AR benchmark at $h = 4$ (1.421) and $h = 8$ (1.874), whereas RF degrades gracefully (0.729, 0.803). The contrast identifies *where* the long-horizon signal lives: not in common factors, but in granular, idiosyncratic variation at specific suppliers whose stress takes weeks to propagate into the aggregate—precisely the granular channel emphasized by Gabaix (2011) and the network-propagation channel of Acemoglu et al. (2012) and Baqaee and Farhi (2019). Factor compression, like value weighting, is a form of aggregation, and at long horizons aggregation is again the enemy. Ridge, which shrinks densely but never collapses the cross-section, sits in between, and its stability across horizons (0.694–0.881) reinforces the same interpretation.

# 7. Variable Importance Analysis

The forecasting results establish *that* supplier microdata predict network disruptions; this section opens the fitted models to ask *which* suppliers carry the signal and *why*. Beyond its diagnostic value, the answer has direct managerial content, because it identifies the nodes a firm should instrument most intensively in an early-warning system.

## 7.1. Sectoral Importance Across Horizons

For the RF model, we compute permutation variable importance: the increase in out-of-sample MSE when a predictor's values are randomly permuted, averaged over trees and rolling windows. We normalize importances to sum to one across all predictors and aggregate them to the sector level:

$$VI_s^{(h)} = \sum_{i \in \mathcal{S}_s} VI_i^{(h)}, \quad \text{with} \quad \sum_{i=1}^{N} VI_i^{(h)} = 1, \qquad (6)$$

where $VI_i^{(h)}$ is the normalized permutation importance of predictor $i$ in the horizon-$h$ model (summing, for each supplier, the contributions of $\Delta x_{i,t}$ and $\Delta x_{i,t-1}$), and $\mathcal{S}_s$ is the set of predictors associated with suppliers in sector $s$; the four AR lag terms are reported as their own category. Table 4 presents the sectoral importance shares, in percent, by horizon.

Table 4. Sectoral Variable Importance in the RF Microforecasting Model, by Forecast Horizon (%)

| Sector | $h=1$ | $h=2$ | $h=4$ | $h=8$ | Average |
|---|---|---|---|---|---|
| Electronic components | **26.83** | **29.47** | **33.62** | **34.98** | **31.23** |
| Logistics & transportation | **33.91** | **28.64** | **19.42** | **16.73** | **24.68** |
| Chemicals & materials | **11.02** | **13.28** | **16.44** | **16.51** | **14.31** |
| Machinery & equipment | 8.14 | 9.03 | 10.87 | 11.42 | 9.87 |
| Metals & mining | 5.83 | 6.21 | 6.74 | 6.90 | 6.42 |
| Packaging | 4.36 | 4.28 | 3.91 | 3.89 | 4.11 |
| Electrical equipment | 3.62 | 3.87 | 4.12 | 4.19 | 3.95 |
| Plastics & rubber | 2.61 | 2.79 | 3.02 | 3.06 | 2.87 |
| Textiles & apparel | 1.42 | 1.31 | 1.22 | 1.21 | 1.29 |
| AR term | 2.26 | 1.12 | 0.64 | 0.11 | 1.03 |

*Notes.* This table reports permutation variable importance from the RF microforecasting model, normalized to sum to one across all predictors as in Equation (6), aggregated by supplier sector, and expressed in percent; columns sum to approximately 100. Importances are averaged across the rolling windows of the out-of-sample period 2021W1–2025W26. The AR term row aggregates the four lags of $SDR_t$. The three sectors with the largest average importance are shown in bold.

Three patterns are noteworthy. First, importance is highly concentrated: the top three sectors—electronic components, logistics and transportation, and chemicals and materials—account for 70.22% of total importance on average, far in excess of their 38.6% share of preselected suppliers, which is the granularity logic of Gabaix (2011) operating inside a single firm's supply network. Second, the horizon profile is systematic. Logistics and transportation suppliers matter most at short horizons—33.91% at $h = 1$, the largest single entry in the table—and their share declines monotonically with $h$ to 16.73% at $h = 8$: transportation stress converts into late deliveries within one or two transit cycles, so its signal is powerful but short lived. Electronic component suppliers show the mirror image, growing from 26.83% at $h = 1$ to 34.98% at $h = 8$: these upstream, central suppliers sit several tiers from final delivery, so their stress takes weeks to propagate downstream—exactly the propagation lag that production-network models predict for upstream shocks (Acemoglu et al. 2012, Carvalho et al. 2021). Chemicals and materials, also upstream, display the same rising profile (11.02% to 16.51%). Third, the AR term's importance collapses from 2.26% at $h = 1$ to 0.11% at $h = 8$: at long horizons, essentially *all* of the model's predictive content comes from the supplier cross-section rather than from the aggregate's own history.

If propagation through the production network is the operative mechanism, sectoral importance should align with network centrality. For each sector we compute a spend-share Domar-style weight—the sector's share of total platform spend, augmented by its indirect exposure through the platform's intersector input–output linkages, in the spirit of Hulten (1978)—and regress sectoral importance shares on this centrality measure across sectors and rolling windows, pooled and by horizon. Table 5 reports the results.

Table 5. Sectoral Variable Importance and Network Centrality

| | Pooled | $h=1$ | $h=2$ and $4$ | $h=8$ |
|---|---|---|---|---|
| Domar-style centrality | 0.294** | 0.131 | 0.322** | 0.451*** |
| | (0.089) | (0.118) | (0.101) | (0.114) |
| Observations | 468 | 117 | 234 | 117 |
| $R^2$ | 0.118 | 0.031 | 0.146 | 0.219 |

*Notes.* This table reports regressions of sectoral variable importance shares (from Table 4, computed within each rolling window) on the sector's spend-share Domar-style centrality weight, standardized to unit variance. The unit of observation is a sector–window cell for the nine supplier sectors across 13 evaluation blocks; the pooled column stacks all four horizons with horizon fixed effects, and the intermediate horizons $h = 2$ and $h = 4$ are pooled to preserve power. Standard errors, clustered by sector, are in parentheses. \*\*\*, \*\*, and \* denote statistical significance at the 1%, 5%, and 10% levels, respectively, based on two-sided $t$-tests.

Centrality predicts importance, and increasingly so at longer horizons: the pooled coefficient is 0.294 (standard error 0.089), statistically insignificant at $h = 1$ (0.131), significant at the intermediate horizons (0.322), and largest at $h = 8$ (0.451, significant at the 1% level). The gradient is exactly what propagation implies: at one week, what matters is proximity to delivery (hence logistics); at two months, what matters is position in the network, because only shocks at central nodes survive propagation long enough to move the aggregate eight weeks later (Baqaee and Farhi 2019).

## 7.2. Supplier Characteristics and Forecasting Importance

We next descend to the supplier level and ask which observable characteristics predict a supplier's forecasting importance. We estimate

$$VI_{i} = \alpha + \boldsymbol{\theta}'\mathbf{Z}_i + \eta_i, \qquad (7)$$

where $VI_i$ is supplier $i$'s normalized permutation importance (scaled by $10^4$) in a given horizon model and evaluation block, and $\mathbf{Z}_i$ is a vector of standardized supplier characteristics measured in the corresponding training window: eigenvector centrality in the platform's PO network; single-source status (an indicator that the supplier is the sole qualified source for at least one part family); a geographic risk index combining country-level political risk and natural-hazard exposure; lead-time volatility (the trailing standard deviation $\sigma_{i,t}^{52}$); buffer inventory (weeks of cover the buyer holds for the supplier's parts); a multi-region footprint indicator (shipping from two or more regions); a financial distress score from the platform's credit monitoring; and relationship length in years. The regression includes time (evaluation block) and sector fixed effects, so identification comes from within-sector, within-period variation across suppliers; the unit of observation is a supplier–horizon–block cell (1,200 suppliers, four horizons, 13 blocks, less cells with missing characteristics), for 61,204 observations. Table 6 reports pooled and horizon-specific estimates.

Table 6. Supplier Characteristics and Supplier-Level Variable Importance ($VI_i \times 10^4$)

| Characteristic | Pooled | $h=1$ | $h=2$ | $h=4$ | $h=8$ |
|---|---|---|---|---|---|
| Eigenvector centrality | 3.51*** | 2.42*** | 3.18*** | 3.87*** | 4.55*** |
| | (0.42) | (0.84) | (0.82) | (0.86) | (0.95) |
| Single-source status | 2.83*** | 2.31*** | 2.68*** | 3.05*** | 3.28*** |
| | (0.31) | (0.62) | (0.60) | (0.63) | (0.66) |
| Geographic risk index | 1.94*** | 1.52*** | 1.83*** | 2.11*** | 2.30*** |
| | (0.28) | (0.55) | (0.56) | (0.57) | (0.59) |
| Lead-time volatility | 3.12*** | 4.21*** | 3.44*** | 2.71*** | 2.12** |
| | (0.47) | (0.96) | (0.93) | (0.94) | (0.98) |
| Buffer inventory (weeks of cover) | −0.92** | −0.71 | −0.86 | −1.01 | −1.10 |
| | (0.36) | (0.73) | (0.71) | (0.72) | (0.74) |
| Multi-region footprint | −1.47*** | −1.18** | −1.39** | −1.58*** | −1.73*** |
| | (0.29) | (0.59) | (0.58) | (0.59) | (0.61) |
| Financial distress score | 1.28** | 1.64 | 1.41 | 1.12 | 0.95 |
| | (0.51) | (1.04) | (1.02) | (1.03) | (1.05) |
| Relationship length (years) | 0.36*** | 0.29 | 0.34* | 0.39** | 0.42** |
| | (0.09) | (0.18) | (0.18) | (0.19) | (0.19) |
| Observations | 61,204 | 15,301 | 15,301 | 15,301 | 15,301 |
| $R^2$ | 0.043 | 0.038 | 0.041 | 0.046 | 0.049 |

*Notes.* This table reports estimates of Equation (7): supplier-level normalized permutation importance from the RF model, multiplied by $10^4$, regressed on standardized supplier characteristics measured in the corresponding training window. The unit of observation is a supplier–horizon–evaluation-block cell over the out-of-sample period 2021W1–2025W26; the pooled column stacks all four horizons. All specifications include time (evaluation block) and sector fixed effects. Continuous characteristics are standardized to zero mean and unit variance within the estimation sample; single-source status and multi-region footprint are indicators. Standard errors, clustered by supplier, are in parentheses. \*\*\*, \*\*, and \* denote statistical significance at the 1%, 5%, and 10% levels, respectively, based on two-sided $t$-tests.

The cross-sectional anatomy of predictive importance matches production-network theory closely. Eigenvector centrality carries the largest pooled coefficient: a one-standard-deviation increase in centrality is associated with an increase in importance of $3.51 \times 10^{-4}$, roughly 43% of the mean supplier-level importance of $8.2 \times 10^{-4}$, and the effect strengthens monotonically with the horizon (from 2.42 at $h = 1$ to 4.55 at $h = 8$), mirroring the sector-level gradient of Table 5. Single-source status adds $2.83 \times 10^{-4}$: where no qualified alternative exists, a supplier's stress cannot be diversified away and must surface in the aggregate—the fragility mechanism of Elliott et al. (2022) and the input-specificity mechanism of Barrot and Sauvagnat (2016). Geographic risk ($1.94 \times 10^{-4}$) and the financial distress score ($1.28 \times 10^{-4}$) also raise importance—financially fragile suppliers transmit stress through their transaction behavior, and notably the distress gradient is *steepest at short horizons* (1.64 at $h = 1$, declining to 0.95 at $h = 8$), consistent with financial stress being a late-stage symptom. Lead-time volatility shows the same short-horizon tilt (4.21 falling to 2.12), as befits a signal-to-noise characteristic of the predictor itself.

Conversely, the two mitigation-related characteristics *reduce* importance: an additional standard deviation of buffer inventory lowers importance by $0.92 \times 10^{-4}$, and a multi-region footprint lowers it by $1.47 \times 10^{-4}$. Buffers and geographic redundancy do not merely reduce a supplier's expected disruption contribution ex post; they decouple the supplier's stress signals from the network aggregate ex ante, which is the prediction-side counterpart of the classic mitigation results of Tomlin (2006) and the risk-diversification logic of Chopra and Sodhi (2004). Relationship length enters positively but modestly ($0.36 \times 10^{-4}$), plausibly because long-standing suppliers hold larger and more specialized order books. The modest $R^2$ of 0.043 indicates that observable characteristics explain only part of the importance distribution—much of a supplier's predictive relevance is idiosyncratic—which itself argues for learning importance from data rather than assigning it by rule. We emphasize again that Equation (7) describes correlates of *predictive* importance, not causal effects of the characteristics; additional specifications, including horizon-interacted and within-country estimates, appear in Table C.2 in Online Appendix C.

## 7.3. Further Remarks and Managerial Implications

The variable importance results convert the forecasting exercise into an actionable monitoring design, with three concrete implications for practice.

First, *instrument the right nodes*. An early-warning dashboard need not track all 8,437 suppliers with equal intensity: predictive signal concentrates in a subpopulation—central, single-sourced, geographically concentrated, financially fragile suppliers, disproportionately in electronic components, logistics, and chemicals—and Equation (7) provides a scoring rule for prioritizing instrumentation when a firm first builds such a system, before enough history exists to estimate importances directly. In our data, the top 300 suppliers by fitted importance account for 71% of total importance; a dashboard restricted to them sacrifices only a small fraction of the RF model's accuracy (average MSE ratio 0.724 versus 0.706; see Online Appendix C).

Second, *match the monitoring horizon to the node*. Logistics signals warrant high-frequency, short-horizon alerting tied to expediting decisions, whereas upstream component and materials suppliers warrant slower-moving but longer-horizon review tied to allocation, qualification, and buffer decisions. The horizon rotation in Table 4 is, in effect, an empirically estimated map from supplier type to actionable lead time.

Third, *target mitigation where predictive risk concentrates*. Because buffers and multi-region footprints demonstrably decouple supplier stress from the network aggregate (Table 6), the importance scores identify where incremental buffer inventory or dual-sourcing investments purchase the most systemic stability—a data-driven refinement of the risk-exposure prioritization of Simchi-Levi et al. (2015) and the segmentation advice of Kleindorfer and Saad (2005). More broadly, the finding that a firm's own transaction records dominate purchased aggregate indices (Table 2) reorders the early-warning investment agenda: the binding constraint is not data acquisition but the analytical capability to exploit data the firm already generates.

# 8. Conclusion

This paper proposes and validates a microforecasting approach to supply chain disruption: rather than forecasting a network-wide disruption rate from aggregate barometers, we hand the full cross-section of supplier-level transaction signals to machine learning methods built for high-dimensional prediction. In a weekly panel of 8,437 suppliers from a global manufacturer's procurement platform, the approach delivers large and robust gains—an average out-of-sample MSE reduction of 29.4% relative to an autoregressive benchmark across horizons of one to eight weeks, and 38.2% at the one-week horizon—with the gains concentrated in exactly the volatile episodes when early warning is most valuable. The granularity is the mechanism: a value-weighted aggregate of the identical data destroys the signal entirely, the PMI and GSCPI add only marginal short-horizon content, and factor compression fails beyond one month. Predictive importance concentrates among network-central, single-sourced, geographically concentrated, and financially fragile suppliers, aligning the black-box models with production-network theory and yielding a practical scoring rule for early-warning system design.

The framework generalizes beyond disruption rates. Any operational aggregate that is generated by aggregation over heterogeneous, networked microunits—demand across customers and channels, quality failure rates across production lines, congestion across ports and lanes—is a candidate for the same design: preselect informative microunits, forecast the aggregate directly from the microdata with regularized and nonparametric learners, and interrogate the fitted model for structure. We view the results as evidence for a broader microdata-for-macroprediction paradigm in operations management, paralleling the microdata movement in macroeconomic forecasting: as transaction systems instrument ever more of the physical economy, the informational cost of aggregation grows, and the comparative advantage shifts to methods that can consume the microdata whole.

We close with two limitations that chart the research agenda. First, our evidence comes from a single—if very large and global—buyer network; replication across platforms, industries, and network topologies is needed to establish external validity, and multibuyer data would permit forecasting disruptions that originate outside any one firm's supplier set. Second, variable importance is correlational: it locates predictive signal but does not identify the counterfactual effect of intervening on a supplier, so coupling the forecasting layer with prescriptive models of mitigation (Bertsimas and Kallus 2020) and with causal designs exploiting quasi-random shocks remains an open and important problem. Within those bounds, the message for both scholars and executives is simple: the early warnings firms seek are already latent in the transaction data they own—provided the data are not averaged away before being asked to speak.

# Acknowledgments

The authors thank seminar participants and the collaborating firm's procurement analytics team for helpful comments and for facilitating access to the data.

# References

Acemoglu D, Carvalho VM, Ozdaglar A, Tahbaz-Salehi A (2012) The network origins of aggregate fluctuations. *Econometrica* 80(5):1977–2016.

Ang E, Iancu DA, Swinney R (2017) Disruption risk and optimal sourcing in multitier supply networks. *Management Sci.* 63(8):2397–2419.

Ban GY, Rudin C (2019) The big data newsvendor: Practical insights from machine learning. *Oper. Res.* 67(1):90–108.

Baqaee DR, Farhi E (2019) The macroeconomic impact of microeconomic shocks: Beyond Hulten's theorem. *Econometrica* 87(4):1155–1203.

Barrot JN, Sauvagnat J (2016) Input specificity and the propagation of idiosyncratic shocks in production networks. *Quart. J. Econom.* 131(3):1543–1592.

Benigno G, di Giovanni J, Groen JJJ, Noble AI (2022) The GSCPI: A new barometer of global supply chain pressures. Staff Report No. 1017, Federal Reserve Bank of New York, New York.

Bertsimas D, Kallus N (2020) From predictive to prescriptive analytics. *Management Sci.* 66(3):1025–1044.

Bode C, Wagner SM (2015) Structural drivers of upstream supply chain complexity and the frequency of supply chain disruptions. *J. Oper. Management* 36:215–228.

Bray RL, Mendelson H (2012) Information transmission and the bullwhip effect: An empirical investigation. *Management Sci.* 58(5):860–875.

Breiman L (2001) Random forests. *Machine Learn.* 45(1):5–32.

Cachon GP, Randall T, Schmidt GM (2007) In search of the bullwhip effect. *Manufacturing Service Oper. Management* 9(4):457–479.

Carvalho VM, Nirei M, Saito YU, Tahbaz-Salehi A (2021) Supply chain disruptions: Evidence from the Great East Japan Earthquake. *Quart. J. Econom.* 136(2):1255–1321.

Chopra S, Sodhi MS (2004) Managing risk to avoid supply-chain breakdown. *MIT Sloan Management Rev.* 46(1):53–61.

Clark TE, West KD (2007) Approximately normal tests for equal predictive accuracy in nested models. *J. Econometrics* 138(1):291–311.

Cohen MA, Lee HL (2020) Designing the right global supply chain network. *Manufacturing Service Oper. Management* 22(1):15–24.

Craighead CW, Blackhurst J, Rungtusanatham MJ, Handfield RB (2007) The severity of supply chain disruptions: Design characteristics and mitigation capabilities. *Decision Sci.* 38(1):131–156.

Diebold FX, Mariano RS (1995) Comparing predictive accuracy. *J. Bus. Econom. Statist.* 13(3):253–263.

Elliott M, Golub B, Leduc MV (2022) Supply network formation and fragility. *Amer. Econom. Rev.* 112(8):2701–2747.

Friedman JH (2001) Greedy function approximation: A gradient boosting machine. *Ann. Statist.* 29(5):1189–1232.

Gabaix X (2011) The granular origins of aggregate fluctuations. *Econometrica* 79(3):733–772.

Hastie T, Tibshirani R, Friedman J (2009) *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd ed. (Springer, New York).

Hendricks KB, Singhal VR (2003) The effect of supply chain glitches on shareholder wealth. *J. Oper. Management* 21(5):501–522.

Hendricks KB, Singhal VR (2005) An empirical analysis of the effect of supply chain disruptions on long-run stock price performance and equity risk of the firm. *Production Oper. Management* 14(1):35–52.

Hulten CR (1978) Growth accounting with intermediate inputs. *Rev. Econom. Stud.* 45(3):511–518.

Ivanov D, Dolgui A (2020) Viability of intertwined supply networks: Extending the supply chain resilience angles towards survivability. A position paper motivated by COVID-19 outbreak. *Internat. J. Production Res.* 58(10):2904–2915.

Kesavan S, Gaur V, Raman A (2010) Do inventory and gross margin data improve sales forecasts for U.S. public retailers? *Management Sci.* 56(9):1519–1533.

Kleindorfer PR, Saad GH (2005) Managing disruption risks in supply chains. *Production Oper. Management* 14(1):53–68.

Mullainathan S, Spiess J (2017) Machine learning: An applied econometric approach. *J. Econom. Perspect.* 31(2):87–106.

Osadchiy N, Gaur V, Seshadri S (2016) Systematic risk in supply chain networks. *Management Sci.* 62(6):1755–1777.

Serpa JC, Krishnan H (2018) The impact of supply chains on firm-level productivity. *Management Sci.* 64(2):511–532.

Simchi-Levi D, Schmidt W, Wei Y (2014) From superstorms to factory fires: Managing unpredictable supply-chain disruptions. *Harvard Bus. Rev.* 92(1–2):96–101.

Simchi-Levi D, Schmidt W, Wei Y, Zhang PY, Combs K, Ge Y, Gusikhin O, Sanders M, Zhang D (2015) Identifying risks and mitigating disruptions in the automotive supply chain. *Interfaces* 45(5):375–390.

Tang CS (2006) Perspectives in supply chain risk management. *Internat. J. Production Econom.* 103(2):451–488.

Tibshirani R (1996) Regression shrinkage and selection via the lasso. *J. Roy. Statist. Soc. Ser. B* 58(1):267–288.

Tomlin B (2006) On the value of mitigation and contingency strategies for managing supply chain disruption risks. *Management Sci.* 52(5):639–657.

Zou H (2006) The adaptive lasso and its oracle properties. *J. Amer. Statist. Assoc.* 101(476):1418–1429.

Zou H, Hastie T (2005) Regularization and variable selection via the elastic net. *J. Roy. Statist. Soc. Ser. B* 67(2):301–320.
