---
title: "Reference-dependent home sellers and the liquidity freeze of urban China's housing market"
---

# Reference-dependent home sellers and the liquidity freeze of urban China's housing market

**Yiran Chen^1^, Haoran Lu^1,2^, Meiling Fang^3^ & Jonathan K. Whitfield^4^**

^1^Department of Finance, School of Business, Nanjing University of Finance and Economics, Nanjing 210023, China. ^2^Institute for Real Estate and Urban Studies, Nanjing 210023, China. ^3^School of Economics and Management, Tongji University, Shanghai 200092, China. ^4^Department of Real Estate, Bayes Business School, City St George's, University of London, London EC1Y 8TZ, UK. *e-mail: y.chen@nufe.edu.cn; m.fang@tongji.edu.cn*

---

## Abstract

Housing is the single largest asset on most households' balance sheets, and the liquidity of the resale market shapes household mobility, consumption and macroeconomic stability. During cyclical downturns, however, transaction volumes collapse far more sharply than prices—a "freeze" that competitive equilibrium models struggle to reproduce. Here we show that reference-dependent seller behaviour is a quantitatively important cause of this freeze. Combining 1.2 million resale listings matched to their prior transaction prices across 40 Chinese cities during the 2021–2024 downturn with an original survey of 6,480 homeowners, we find that 39.7% of would-be sellers faced a nominal loss relative to their purchase price. Loss-facing sellers set asking prices that incorporate roughly one-third (γ~L~ = 0.32) of their paper loss, and their listing prices bunch sharply at the original purchase price. This reference dependence lowered their 12-month sale probability by 12.7 percentage points and suppressed resale transaction volume by about 11%, accounting for at least one-eighth of the aggregate volume decline; it also opens a persistent gap between asking and market-clearing prices that biases transaction-based price indices. Trade-in programmes that reset sellers' reference points can materially unfreeze the market.

## Introduction

For most households, the owner-occupied home is by far the largest component of wealth, and shocks to its value transmit powerfully to consumption and aggregate demand^[[mian2013;campbell2007;berger2018;kaplan2020]]^. Yet the welfare consequences of a housing downturn depend not only on how far prices fall but also on whether the market keeps *functioning*—that is, on liquidity. A liquid resale market allows households to relocate for work, to adjust housing consumption over the life cycle, and to release home equity; when it freezes, these adjustments stall even if headline prices decline only modestly.

Nowhere is this tension more consequential than in contemporary China. Real estate and its upstream and downstream activities account for roughly 29% of Chinese gross domestic product, and lower-tier cities alone hold more than 60% of the national housing stock^[[rogoff2020;rogoff2022]]^. After two decades of an extraordinary boom^[[fang2016;glaeser2017;wu2016;chen2017;liu2020]]^, the market turned in 2021. By 2024, the floor area of residential property sold nationwide had fallen to roughly half of its 2021 peak—its lowest level since 2009—while the National Bureau of Statistics' 70-city resale price index declined by only about 10% year-on-year at its trough^[[nbs2024]]^. The most indebted developers were forced into insolvency, with China Evergrande ordered into liquidation in January 2024. The defining feature of the episode, however, is not the price correction but the *collapse in transaction volume*: the secondary market froze far more than it repriced (Fig. 1a).

This price–volume asymmetry is a long-standing puzzle. A frictionless competitive market clears through price; it does not exhibit large swings in the quantity of trade. Existing explanations emphasise search-and-matching frictions^[[krainer2001;head2014;diaz2013;han2015]]^, thick-market and strategic-complementarity effects^[[ngai2014;guren2018]]^, and down-payment constraints that couple prices to volume^[[stein1995]]^. These mechanisms account for much of the positive price–volume comovement observed over the cycle, but they take sellers' willingness to transact as broadly rational and leave open why so many owners simply refuse to sell in a downturn.

We argue that a central part of the answer is behavioural. Prospect theory holds that agents evaluate outcomes as gains or losses relative to a reference point, and that losses loom larger than equivalent gains—loss aversion^[[kahneman1979;tversky1991;tversky1992;koszegi2006]]^. Because the price a household paid for its home is a salient, memorable and psychologically "owned" number, it serves as a natural reference point^[[kahneman1990;shefrin1985;odean1998;barberis2013]]^. A homeowner who would have to sell below that nominal purchase price experiences a loss and is reluctant to realise it. In the housing market specifically, sellers facing nominal losses set higher asking prices, hold out longer, and ultimately transact at higher prices—first documented for Boston condominiums^[[genesove2001]]^ and since confirmed with administrative data in Denmark^[[andersen2022]]^, England and Wales^[[bracke2021]]^, Finland^[[einio2008]]^, and the United States^[[engelhardt2003;anenberg2011]]^, and even among sophisticated commercial investors^[[bokhari2011]]^. When a downturn pushes a large share of owners under water simultaneously, this individually modest reluctance can aggregate into a market-wide freeze. To date, however, the mechanism has been documented mainly through its effect on *prices*; its contribution to the *collapse in liquidity* during a large, synchronised downturn—and the policy levers that might counteract it—has not been quantified at scale.

Here we provide such a quantification for the largest housing market in the world. We assembled a dataset of 1.2 million active resale listings across 40 major Chinese cities during the 2021–2024 downturn, each matched to the price and date of the unit's most recent prior transaction, from a leading online listing platform; we complemented it with an original survey of 6,480 urban homeowners in 30 cities. The prior-transaction match lets us reconstruct, for every listing, the seller's reference point (the purchase price) and, using an automated valuation model, the unit's current market value. We can therefore measure directly how far each would-be seller is under water, how that paper loss maps into their asking price, and how it shapes whether—and how quickly—the unit actually sells.

Our analysis yields four main findings. First, the downturn created a vast stock of paper losses: by 2024, 39.7% of would-be sellers were listing units worth less than they had paid, with the share reaching 49.4% in third-tier cities. Second, sellers are strongly reference-dependent: asking prices trace a "hockey stick" in the potential loss, incorporating roughly one-third of each yuan of nominal loss (γ~L~ = 0.32), with losses weighing about eight times as heavily as gains, and listing prices bunch sharply at the nominal purchase price. Third, this behaviour freezes the market: loss-facing sellers are far less likely to sell and remain listed much longer, and removing reference dependence would raise their sale probability by about a third. Fourth, the aggregate consequences are large: reference dependence suppresses resale transaction volume by roughly 11%—at least one-eighth of the observed decline—opens a persistent gap of about 8% between asking and market-clearing prices, and biases transaction-based price indices, which are composed disproportionately of the least-distressed units. We then use the estimated model to show that policies which reset sellers' reference points, such as the "trade-in" (old-for-new) programmes rolled out across more than 50 Chinese cities in 2024, can unfreeze the market, with the largest gains precisely where losses are deepest.

## Results

### A frozen market and a wall of paper losses

The 2021–2024 downturn in urban China was, first and foremost, a collapse in liquidity. Reconstructing national resale price and transaction-volume indices from our sample, we find that by late 2024 resale volume had fallen to roughly half of its 2021 peak, whereas the resale price index had retreated by less than a quarter (Fig. 1a). Volume fell by more than twice as much as price—the signature of a market that stopped clearing rather than one that simply repriced.

Underlying this freeze is a rapidly accumulating stock of paper losses. Because our listings are matched to prior transactions, we observe each would-be seller's reference point directly. As city price paths turned down, the fraction of would-be sellers whose units were worth less than they had paid rose from below 8% in early 2021 to 39.7% by the end of 2024 (Fig. 1b). The distribution of potential gains and losses (Fig. 2a) is centred close to break-even but has a heavy loss tail: among under-water sellers, the mean paper loss is 18.7% of current market value (median 15.3%).

![](figs/fig1.png){width="16cm"}

**Fig. 1 | The great freeze of urban China's housing market.** **a**, National resale price and transaction-volume indices (2021 peak = 100), reconstructed from the listing sample. Transaction volume fell to about half of its peak while the price index declined far less, opening a large volume–price gap. **b**, Share of would-be sellers whose units are worth less than their nominal purchase price ("under water"), which rose from below 8% in early 2021 to 39.7% by the end of 2024.

The freeze is highly uneven across cities, and the geography mirrors the depth of the price correction. Under-water shares range from 19.9% in Guangzhou to 61.2% in Weifang, and they are strongly ordered by city tier: 28.8% in first-tier cities, 41.7% in second-tier cities and 49.4% in third-tier cities (Fig. 2b). Because lower-tier cities experienced both the largest price declines and the greatest overbuilding, they concentrate the paper losses—and, as we show below, the freeze.

![](figs/fig2.png){width="16cm"}

**Fig. 2 | A wall of paper losses across 40 major cities.** **a**, Distribution of would-be sellers' potential capital gains (blue) and losses (red) relative to the nominal purchase price, expressed as a percentage of current market value; 39.7% of would-be sellers are under water. **b**, Share of listings under water in each of the 40 sample cities, coloured by administrative tier. The under-water share rises steeply from first- to third-tier cities.

### Reference dependence in listing prices

Do these paper losses change how owners price their homes? We estimate each unit's current market value with an automated valuation model and define the *listing markup* as the percentage by which the asking price exceeds that value (Methods). Plotting the average markup against each seller's potential gain or loss reveals a pronounced "hockey stick" (Fig. 3a): markups are low and almost flat for sellers with capital gains, but rise steeply once a unit is under water. Sellers who are above water list at an average markup of 3.5%, whereas under-water sellers list at 10.0%—a gap of 6.6 percentage points that widens with the size of the paper loss.

Estimating the relationship formally (Methods, Eq. (5)), we find that asking prices incorporate γ~L~ = 0.321 (s.e. 0.002) of each unit of nominal loss—that is, a seller facing a 10-percentage-point-larger paper loss raises the asking price by about 3.2 percentage points above market value. On the gain side the pass-through is only γ~G~ = 0.039, so losses weigh roughly 8.3 times as heavily as equivalent gains, a marked asymmetry consistent with loss aversion and with the reference-dependence estimates obtained in other markets^[[genesove2001;andersen2022]]^.

Reference dependence is even more visible in a sharp discontinuity at the reference point itself. The distribution of the ratio of the asking price to the original purchase price exhibits pronounced excess mass exactly at one (Fig. 3b): 24.1% of under-water sellers list within ±1.5% of the price they paid, roughly 2.2 times the mass implied by a smooth counterfactual density (Methods, Eq. (6)). Homeowners appear to treat the nominal purchase price as a floor below which they are reluctant to advertise, producing a visible spike—a bunching signature previously observed in apartment markets abroad^[[einio2008;andersen2022]]^ and, to our knowledge, documented here at national scale for China.

![](figs/fig3.png){width="16cm"}

**Fig. 3 | Reference dependence in listing prices.** **a**, Binned mean listing markup over estimated market value against each seller's potential gain/loss relative to the purchase price. The relationship is a "hockey stick": nearly flat for gains (fitted slope γ~G~ = 0.04) and steep for losses (γ~L~ = 0.32). **b**, Distribution of the asking-price-to-purchase-price ratio. Excess mass (red) at a ratio of one—24.1% of under-water sellers list within ±1.5% of their purchase price—stands well above the smooth counterfactual density (dashed), a bunching ratio of 2.2.

Our homeowner survey confirms that the purchase price is psychologically salient rather than a statistical artefact. Among all respondents, 82% reported that they track their home's value relative to what they originally paid, and 70% of under-water owners stated that they would reject an offer below their nominal purchase price. Under-water owners reported a mean reservation markup over an agent's appraised value of 11.1%, against 4.0% for owners sitting on gains—closely matching the listing behaviour we observe in the transaction data.

### From sticky asks to a frozen market

Reference-dependent pricing matters for welfare only if it impedes trade. It does. The 12-month sale probability declines steeply with the listing markup (Fig. 4a): a 10-percentage-point increase in the markup lowers the probability that a unit sells within a year by 24.4 percentage points (Methods, Eq. (8)). Because loss-facing sellers set systematically higher markups, they sell far less often. Sorting listings by potential loss (Fig. 4b), the sale probability falls monotonically while the expected time-on-market lengthens; under-water units take a median of 27.3 months to sell, against 16.4 months for units sitting on gains.

The upshot is a two-tier market. Only 36.9% of under-water listings sold within 12 months, compared with 53.6% of listings sitting on gains—a 16.7-percentage-point liquidity gap (Fig. 4c). Under-water sellers were also more likely to give up and withdraw their listing unsold (28.4% versus 20.8%). In effect, a large and growing share of the housing stock became untradeable at prevailing asking prices, not because buyers vanished but because sellers anchored to a reference point the market had left behind.

![](figs/fig4.png){width="16cm"}

**Fig. 4 | From sticky asking prices to a frozen market.** **a**, 12-month sale probability by decile of the listing markup; higher asking prices sharply reduce the likelihood of sale. **b**, Sale probability (blue, left axis) and median time-on-market (red, right axis) by decile of the potential loss. **c**, Share of listings that sold within 12 months versus those withdrawn unsold, for units above and under water. Under-water sellers sell much less often and withdraw more often.

### Aggregate consequences: suppressed volume and mismeasured prices

How much of the freeze can be attributed to reference dependence? We answer this with a counterfactual in which sellers are not loss-averse—that is, we set the loss-aversion pass-through to zero and remove the bunching at the reference point, holding fixed each unit's fundamentals and the rest of the pricing model (Methods, Eq. (10)). Under this counterfactual, the 12-month sale probability of under-water listings rises from 36.9% to 49.6%—an increase of about one-third—and the market-wide sale probability rises from 47.0% to 52.0% (Fig. 5a). Reference dependence therefore suppresses resale transaction volume by roughly 11%. Mapped onto the observed peak-to-2024 decline in resale volume (about 48%), this channel accounts for at least one-eighth (~12%) of the aggregate freeze. Because our data condition on units that were actually listed, this figure is a lower bound: it omits the many loss-averse owners who chose not to list at all.

Reference dependence also drives a wedge between asking and market-clearing prices. Averaging the gap between listing prices and estimated market values, we find that listings sit 6.1% above market value on average, rising to 8.0% among unsold listings and 10.0% among under-water listings (Fig. 5b). This "reference-price gap" is the shadow of the freeze in the price dimension: sellers hold their asking prices above the level that would clear the market, so units accumulate on the market rather than transacting.

A further, subtler consequence is that the freeze biases the prices we observe. Because under-water units are far less likely to sell, transactions over-represent the least-distressed segment of the market: the share of under-water units among *completed transactions* (31.2%) is 8.5 percentage points below their share among *all listings* (39.7%) (Fig. 5c). Standard transaction-based price indices, which by construction can only see units that trade, therefore understate the true correction—in our sample by about 4.9 percentage points. Part of the apparent "resilience" of headline Chinese house prices during the downturn is thus a selection artefact of the freeze itself, a concern also raised for loss-aversion-driven indices in commercial real estate^[[bokhari2011]]^.

![](figs/fig5.png){width="16cm"}

**Fig. 5 | Aggregate consequences of reference dependence.** **a**, Actual 12-month sale probability (red) versus a counterfactual with no reference dependence (green), for all listings and for under-water listings; removing reference dependence raises under-water liquidity by about one-third. **b**, The reference-price gap: listing prices exceed estimated market value by 6.1% on average, rising to 8.0% among unsold and 10.0% among under-water listings. **c**, Under-water share among all listings versus completed transactions; the selection of less-distressed units into trade causes transaction-based indices to understate the correction by about 4.9 percentage points.

### Heterogeneity: who is locked in

The freeze is concentrated among the owners for whom the reference point bites hardest: those who bought near the peak. Owners who purchased in 2020–2021, when prices were highest, make up 37.5% of would-be sellers but are overwhelmingly under water (77.9%, versus 15.2% for those who bought in 2019 or earlier). They post higher markups (9.3% versus 4.0%) and sell far less often (a 12-month sale probability of 39.3% versus 51.9%) (Fig. 6a). Reference dependence thus falls disproportionately on recent buyers, many of them younger, first-time or trade-up households whose mobility is most impaired by the lock-in.

Across cities, the intensity of the freeze tracks the depth of the price correction almost perfectly. The share of under-water listings rises steeply with the peak-to-2024 price decline (correlation r = 0.93; Fig. 6b), and the reference-price gap is similarly ordered (r = 0.95). The behavioural channel is therefore strongest exactly where the fundamental shock is largest—amplifying, rather than cushioning, the downturn in the weakest markets.

![](figs/fig6.png){width="16cm"}

**Fig. 6 | Heterogeneity in the freeze.** **a**, Under-water share, listing markup and 12-month sale probability for owners who bought near the 2021 peak (2020–2021) versus those who bought earlier (≤2019). Peak-cohort buyers are far more likely to be locked in. **b**, Across the 40 cities, the share of under-water listings rises steeply with the peak-to-2024 resale price decline (r = 0.93); marker size is proportional to the number of listings and colour denotes tier.

### Unfreezing the market

Because our estimates identify the behavioural friction directly, they let us evaluate policies that target it. We consider three interventions (Methods, Eq. (11)). A broad *transaction-cost relief*—for example, cuts to deed and value-added taxes that lower the effective reservation ask by two percentage points across the board—raises resale volume by 12.2%. A *trade-in* ("old-for-new") programme, in which a developer or a government platform purchases the seller's existing home at an appraised value and thereby resets the reference point, raises volume by 4.2% when 40% of under-water owners participate, and by 10.4% under full participation (Fig. 7a). Crucially, because trade-in acts on the reference point rather than on price, its benefits are largest exactly where reference dependence is most binding: the volume uplift rises from 2.0% in first-tier cities to 7.0% in third-tier cities (Fig. 7b), precisely the markets where the freeze is deepest.

![](figs/fig7.png){width="16cm"}

**Fig. 7 | Unfreezing the market: policy scenarios.** **a**, Simulated increase in resale transaction volume under transaction-cost relief, a trade-in programme with 40% participation, and a full reference-point reset. **b**, Volume uplift from the trade-in programme by city tier; gains are largest in third-tier cities, where paper losses and the freeze are deepest.

## Discussion

Using transaction-matched listings for the world's largest housing market, we have shown that reference-dependent seller behaviour is a first-order driver of the liquidity freeze that accompanies a housing downturn. When a synchronised price decline pushes a large share of owners under water, their reluctance to sell below the nominal purchase price aggregates into a market-wide collapse in transaction volume, a persistent gap between asking and market-clearing prices, and a selection bias that flatters headline price statistics. In our data, this behavioural channel accounts for at least one-eighth of the observed decline in resale volume—almost certainly an underestimate, because it excludes owners who declined to list at all.

These findings reframe how the health of a housing market should be read during a downturn. Prices alone are a misleading gauge: a market can appear to be correcting gently while it is in fact seizing up, with mobility, equity release and consumption smoothing all impaired for the growing share of households who are locked in. The macroeconomic stakes are considerable given that housing wealth is a powerful determinant of consumption^[[mian2013;campbell2007;berger2018;kaplan2020]]^ and that real estate constitutes so large a share of Chinese output^[[rogoff2020;rogoff2022;liu2020]]^.

Our results also carry direct policy implications. Because the friction is a reference point rather than a fundamental, the most effective interventions are those that move or neutralise the reference point rather than those that merely subsidise price. This is the logic of the "trade-in" (old-for-new) schemes that more than 50 Chinese cities adopted in 2024, often paired with a personal income-tax refund for owners who buy a new home within a year of selling their old one^[[nbs2024;statecouncil2024]]^: by allowing an owner to exit an under-water unit at an appraised value while rolling into a new purchase, such schemes let households sidestep the psychological loss and re-enter the market. Our simulations suggest these programmes can raise resale volume most where the freeze is worst. Transaction-cost relief and credit easing help through the same channel by narrowing the gap between reservation and market-clearing prices; consistent with this, the September 2024 easing of mortgage rates and down-payments was followed by a marked rebound in second-hand transactions in cities such as Beijing even as new-home sales stayed weak^[[nbs2024]]^. A complementary, longer-run lever is expectation management: because reference points are shaped by beliefs about future prices^[[koszegi2006]]^, credibly stabilising price expectations can itself soften the lock-in.

Several limitations qualify our conclusions. First, our market-value estimates rely on an automated valuation model; although we validate it extensively (Methods), measurement error in fundamentals could attenuate or exaggerate the estimated reference dependence. Second, we identify the behavioural friction from cross-sectional and cohort variation rather than from an exogenous shock to reference points; the trade-in roll-out offers a promising natural experiment for future work. Third, we observe listing and withdrawal but not the full bargaining path, so our liquidity estimates capture the extensive margin of sale more cleanly than the intensive margin of negotiated price. Fourth, and most importantly, because we condition on units that were listed, we cannot observe the owners whom loss aversion deterred from listing altogether; our aggregate estimates are therefore conservative. Quantifying that extensive margin—ideally by linking listings to the underlying ownership registry—should be a priority for future research.

Reference dependence in housing is not unique to China; it has been documented across advanced economies^[[genesove2001;andersen2022;bracke2021;engelhardt2003;anenberg2011]]^. What the Chinese downturn provides is a setting large and severe enough to reveal its aggregate consequences, and a policy laboratory—the trade-in programmes—for testing remedies. As housing markets in many countries confront higher interest rates and the prospect of price corrections, understanding how the psychology of loss can freeze a market, and how policy can thaw it, is of broad and pressing importance.

## Methods

### Data

Our primary data are the universe of active resale (second-hand) residential listings on a leading online listing platform in mainland China, collected by web crawler between October 2020 and December 2024 for 40 major cities spanning all three administrative tiers (4 first-tier, 16 second-tier and 20 third-tier cities). In China, sellers and their agents post resale units on such platforms together with the asking price, detailed unit and community attributes, and—critically for this study—the date and price of the unit's most recent prior transaction, because the holding period partly determines resale transaction taxes and is therefore prominently displayed^[[wang2020]]^. We retain listings in communities completed between 2001 and 2022, drop the top and bottom 1% of units by unit price, floor area and community size in each city, and keep units with a valid prior-transaction record, yielding a working sample of 1,200,000 listings observed over 2022Q1–2024Q4. For each listing we observe the asking price, unit size, floor, building age, community, listing and withdrawal dates, and whether the unit sold within our observation window. The 40 sample cities together accounted for a large share of national resale activity during the period.

We complement the listing data with an original cross-sectional survey of 6,480 urban homeowners across 30 cities, fielded in early 2024 through an online panel stratified by city tier, age and dwelling vintage. The survey elicited each respondent's original purchase price and date, an agent-appraised current value, their stated reservation price, and attitudinal items on the salience of the purchase price and willingness to sell at a nominal loss. The survey provides direct evidence on the reference point that complements the revealed behaviour in the listing data.

### Estimating market value

To measure how far each seller is under water and how much their asking price departs from fundamentals, we require an estimate of each unit's current market value, $V_i$, that is independent of the asking price. We estimate a hedonic automated valuation model (AVM) on the subsample of *completed transactions*, regressing the log transaction price on unit and community attributes, with city and listing-quarter fixed effects, as in Eq. (1):

$$\ln V_{i} = \mathbf{x}_{i}^{\prime}\boldsymbol{\beta} + \delta_{c(i)} + \eta_{\tau(i)} + \varepsilon_{i},$$

where $\mathbf{x}_i$ contains unit size, building age, floor, and community-level controls, $\delta_{c(i)}$ is a city fixed effect and $\eta_{\tau(i)}$ a listing-quarter fixed effect. To capture non-linearities and interactions we also estimate a gradient-boosted regression-tree version of Eq. (1) and use its out-of-sample prediction as $V_i$; the two approaches yield very similar valuations (out-of-sample $R^2 = 0.89$). Because $V_i$ is fitted on transacted units and applied to all listings, it provides a market-clearing benchmark that is not mechanically related to a given seller's asking price.

### Reference points, gains and losses, and markups

We take the unit's most recent prior transaction price, $P_i^{\text{purchase}}$, as the seller's reference point^[[genesove2001;andersen2022]]^. The potential gain or loss is the gap between this reference price and current market value, expressed as a fraction of value (Eq. (2)):

$$L_{i} = \frac{P_{i}^{\text{purchase}} - V_{i}}{V_{i}},$$

so that $L_i > 0$ denotes a would-be seller who is "under water" (the reference price exceeds current value). The listing markup measures how far the asking price $P_i^{\text{list}}$ exceeds current market value (Eq. (3)):

$$m_{i} = \frac{P_{i}^{\text{list}} - V_{i}}{V_{i}}.$$

### A reference-dependent reservation price

We motivate the empirical specification with a simple reference-dependent selling problem^[[kahneman1979;tversky1991;koszegi2006]]^. A seller values sale proceeds relative to the reference point $P_i^{\text{purchase}}$ through a gain–loss value function (Eq. (4)):

$$v(z) = \begin{cases} z, & z \ge 0, \\ \lambda\, z, & z < 0, \end{cases} \qquad \lambda > 1,$$

where $z = p - P_i^{\text{purchase}}$ is the sale price net of the reference point and $\lambda$ is the coefficient of loss aversion. A seller facing a potential loss ($V_i < P_i^{\text{purchase}}$) therefore sets a reservation price above market value; optimally trading off a higher price against a lower probability of sale, the seller's reservation price increases in the reference point, generating an asking price that embeds part of the nominal loss.

### Estimating reference dependence

We estimate the mapping from potential loss to asking price with the piecewise-linear "hockey-stick" regression in Eq. (5):

$$m_{i} = \alpha + \gamma_{L}\max\!\left(L_{i},0\right) + \gamma_{G}\min\!\left(L_{i},0\right) + \mathbf{z}_{i}^{\prime}\boldsymbol{\theta} + \delta_{c} + u_{i},$$

where $\gamma_L$ is the pass-through of nominal losses into the asking-price markup, $\gamma_G$ the corresponding pass-through of gains, $\mathbf{z}_i$ a vector of unit controls (log size, building age, floor) and $\delta_c$ city fixed effects. Standard errors are clustered by city. The ratio $\gamma_L/\gamma_G$ measures the asymmetry between the treatment of losses and gains, the empirical counterpart of the loss-aversion coefficient $\lambda$.

### Bunching at the reference point

To quantify the excess concentration of asking prices at the purchase price, we apply a bunching estimator^[[saez2010;kleven2016]]^ to the distribution of the ratio $r_i = P_i^{\text{list}}/P_i^{\text{purchase}}$. We bin $r_i$ finely and fit a flexible polynomial counterfactual density that excludes a window $[\underline{r},\overline{r}]$ around $r=1$ (Eq. (6)):

$$c_{j} = \sum_{k=0}^{K}\beta_{k}\, r_{j}^{k} + \sum_{r\in[\underline{r},\overline{r}]}\rho_{r}\,\mathbf{1}\!\left[r_{j}=r\right] + \nu_{j},$$

where $c_j$ is the count of listings in bin $j$ and $\hat{c}_j^{0} = \sum_k \hat{\beta}_k r_j^{k}$ is the estimated counterfactual. The excess mass at the reference point is then given by Eq. (7):

$$\hat{B} = \frac{\sum_{j\in[\underline{r},\overline{r}]}\left(c_{j}-\hat{c}_{j}^{0}\right)}{\hat{c}^{0}},$$

with $\hat{c}^{0}$ the average counterfactual density in the window. We report both $\hat{B}$ and the bunching ratio, the observed count in the window relative to the counterfactual.

### Liquidity: sale hazard and time-on-market

We relate the probability of sale to the asking price with the discrete-time hazard model in Eq. (8):

$$\Pr\!\left(\text{sale}_{i}=1 \mid \cdot\right) = \Lambda\!\left(a + b\, m_{i} + \mathbf{z}_{i}^{\prime}\boldsymbol{\psi}\right), \qquad \Lambda(t) = \frac{1}{1+e^{-t}},$$

where $\text{sale}_i$ indicates a sale within 12 months, $m_i$ is the listing markup, and $\mathbf{z}_i$ includes tier and unit controls. The expected time-on-market follows from the implied monthly hazard $h_i$ as in Eq. (9):

$$\mathbb{E}\!\left[\text{TOM}_{i}\right] = \frac{1}{h_{i}}, \qquad p_i \equiv \Pr\!\left(\text{sale within 12 months}\right) = 1-\left(1-h_{i}\right)^{12}.$$

### Aggregate counterfactual and the reference-price gap

Aggregate resale transaction volume is the sum of individual sale probabilities, $Q = \sum_{i=1}^{N} p_i(m_i)$. To isolate the contribution of reference dependence, we construct a counterfactual asking price for each seller by setting the loss pass-through to zero and removing the bunching mass—that is, replacing $m_i$ with the markup a reference-independent seller with the same fundamentals would post—and recompute the implied volume $Q^{0}$. The share of volume suppressed by reference dependence is given by Eq. (10):

$$\Delta = 1 - \frac{Q}{Q^{0}}.$$

We benchmark $\Delta$ against the observed peak-to-2024 decline in resale volume to obtain the share of the aggregate freeze attributable to the behavioural channel. The reference-price gap is the mean proportional wedge between asking prices and market value among unsold listings, $G = N_u^{-1}\sum_{i:\,\text{unsold}} m_i$.

### Policy scenario analysis

We evaluate three interventions by re-simulating $Q$ under modified asking-price distributions. Transaction-cost relief lowers every seller's effective reservation ask by two percentage points, $m_i \rightarrow m_i - 0.02$. A trade-in (old-for-new) programme resets the reference point for a participating share $s$ of under-water owners, who then price at the reference-independent markup, as in Eq. (11):

$$m_{i}^{\text{policy}} = \begin{cases} m_{i}^{0}, & \text{with probability } s \ \text{(reference reset)},\\[2pt] m_{i}, & \text{with probability } 1-s, \end{cases}$$

and we report the resulting volume uplift $Q^{\text{policy}}/Q - 1$ overall and by tier. All monetary comparisons are nominal, consistent with the reference point being the nominal purchase price.

### Reporting summary

Further information on research design is available in the Reporting Summary linked to this article.

## Data availability

The city-level aggregates and the code parameters required to reproduce all figures and statistics reported in this study are available from the corresponding author on reasonable request. The individual online listings were obtained from a commercial platform under a data-use agreement that precludes public redistribution of unit-level records; derived, de-identified variables are available for non-commercial academic use subject to that agreement. Survey microdata are available from the corresponding author under the conditions of the study's ethics approval.

## Code availability

All code required to reproduce the estimation, counterfactuals and figures is available from the corresponding author on reasonable request.
