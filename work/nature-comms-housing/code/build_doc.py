"""Resolve [[key]] citation tags -> superscript numbers by first appearance,
append the numbered reference list + back matter, and convert to .docx via
pandoc (native OMML equations)."""
import re, subprocess, os

OUT = "/tmp/claude-0/-home-user-xixi/3e060dbe-78a7-5945-afbd-f1a988fe044a/scratchpad"
src = open(os.path.join(OUT,"paper.md")).read()

# strip YAML front matter
src = re.sub(r"^---\n.*?\n---\n", "", src, count=1, flags=re.DOTALL)

# number display equations (line-based: whole line is $$...$$) in order
_eqn = [0]
def _num_eq(m):
    _eqn[0]+=1
    inner = m.group(1).rstrip().rstrip(",")
    tail = "," if m.group(1).rstrip().endswith(",") else ""
    return f"$${inner}{tail} \\qquad\\text{{({_eqn[0]})}}$$"
src = re.sub(r"^\$\$(.+)\$\$[ \t]*$", _num_eq, src, flags=re.MULTILINE)
print(f"numbered display equations: {_eqn[0]}")

BIB = {
"mian2013":"Mian, A., Rao, K. & Sufi, A. Household balance sheets, consumption, and the economic slump. <i>Q. J. Econ.</i> <b>128</b>, 1687–1726 (2013).",
"campbell2007":"Campbell, J. Y. & Cocco, J. F. How do house prices affect consumption? Evidence from micro data. <i>J. Monet. Econ.</i> <b>54</b>, 591–621 (2007).",
"berger2018":"Berger, D., Guerrieri, V., Lorenzoni, G. & Vavra, J. House prices and consumer spending. <i>Rev. Econ. Stud.</i> <b>85</b>, 1502–1542 (2018).",
"kaplan2020":"Kaplan, G., Mitman, K. & Violante, G. L. The housing boom and bust: model meets evidence. <i>J. Polit. Econ.</i> <b>128</b>, 3285–3345 (2020).",
"rogoff2020":"Rogoff, K. S. & Yang, Y. <i>Peak China Housing</i>. NBER Working Paper No. 27697 (National Bureau of Economic Research, 2020).",
"rogoff2022":"Rogoff, K. S. & Yang, Y. <i>A Tale of Tier 3 Cities</i>. NBER Working Paper No. 30519 (National Bureau of Economic Research, 2022).",
"fang2016":"Fang, H., Gu, Q., Xiong, W. & Zhou, L.-A. Demystifying the Chinese housing boom. <i>NBER Macroecon. Annu.</i> <b>30</b>, 105–166 (2016).",
"glaeser2017":"Glaeser, E., Huang, W., Ma, Y. & Shleifer, A. A real estate boom with Chinese characteristics. <i>J. Econ. Perspect.</i> <b>31</b>, 93–116 (2017).",
"wu2016":"Wu, J., Gyourko, J. & Deng, Y. Evaluating the risk of Chinese housing markets: what we know and what we need to know. <i>China Econ. Rev.</i> <b>39</b>, 91–114 (2016).",
"chen2017":"Chen, K. & Wen, Y. The great housing boom of China. <i>Am. Econ. J. Macroecon.</i> <b>9</b>, 73–114 (2017).",
"liu2020":"Liu, C. & Xiong, W. China's real estate market. In <i>The Handbook of China's Financial System</i> (eds Amstad, M., Sun, G. & Xiong, W.) 183–207 (Princeton Univ. Press, 2020).",
"nbs2024":"National Bureau of Statistics of China. <i>National Real Estate Development and Sales in 2024</i> https://www.stats.gov.cn (National Bureau of Statistics of China, 2025).",
"krainer2001":"Krainer, J. A theory of liquidity in residential real estate markets. <i>J. Urban Econ.</i> <b>49</b>, 32–53 (2001).",
"head2014":"Head, A., Lloyd-Ellis, H. & Sun, H. Search, liquidity, and the dynamics of house prices and construction. <i>Am. Econ. Rev.</i> <b>104</b>, 1172–1210 (2014).",
"diaz2013":"Díaz, A. & Jerez, B. House prices, sales, and time on the market: a search-theoretic framework. <i>Int. Econ. Rev.</i> <b>54</b>, 837–872 (2013).",
"han2015":"Han, L. & Strange, W. C. The microstructure of housing markets: search, bargaining, and brokerage. In <i>Handbook of Regional and Urban Economics</i> Vol. 5 (eds Duranton, G., Henderson, J. V. & Strange, W. C.) 813–886 (Elsevier, 2015).",
"ngai2014":"Ngai, L. R. & Tenreyro, S. Hot and cold seasons in the housing market. <i>Am. Econ. Rev.</i> <b>104</b>, 3991–4026 (2014).",
"guren2018":"Guren, A. M. House price momentum and strategic complementarity. <i>J. Polit. Econ.</i> <b>126</b>, 1172–1218 (2018).",
"stein1995":"Stein, J. C. Prices and trading volume in the housing market: a model with down-payment effects. <i>Q. J. Econ.</i> <b>110</b>, 379–406 (1995).",
"kahneman1979":"Kahneman, D. & Tversky, A. Prospect theory: an analysis of decision under risk. <i>Econometrica</i> <b>47</b>, 263–291 (1979).",
"tversky1991":"Tversky, A. & Kahneman, D. Loss aversion in riskless choice: a reference-dependent model. <i>Q. J. Econ.</i> <b>106</b>, 1039–1061 (1991).",
"tversky1992":"Tversky, A. & Kahneman, D. Advances in prospect theory: cumulative representation of uncertainty. <i>J. Risk Uncertain.</i> <b>5</b>, 297–323 (1992).",
"koszegi2006":"Kőszegi, B. & Rabin, M. A model of reference-dependent preferences. <i>Q. J. Econ.</i> <b>121</b>, 1133–1165 (2006).",
"kahneman1990":"Kahneman, D., Knetsch, J. L. & Thaler, R. H. Experimental tests of the endowment effect and the Coase theorem. <i>J. Polit. Econ.</i> <b>98</b>, 1325–1348 (1990).",
"shefrin1985":"Shefrin, H. & Statman, M. The disposition to sell winners too early and ride losers too long: theory and evidence. <i>J. Finance</i> <b>40</b>, 777–790 (1985).",
"odean1998":"Odean, T. Are investors reluctant to realize their losses? <i>J. Finance</i> <b>53</b>, 1775–1798 (1998).",
"barberis2013":"Barberis, N. C. Thirty years of prospect theory in economics: a review and assessment. <i>J. Econ. Perspect.</i> <b>27</b>, 173–196 (2013).",
"genesove2001":"Genesove, D. & Mayer, C. Loss aversion and seller behavior: evidence from the housing market. <i>Q. J. Econ.</i> <b>116</b>, 1233–1260 (2001).",
"andersen2022":"Andersen, S., Badarinza, C., Liu, L., Marx, J. & Ramadorai, T. Reference dependence in the housing market. <i>Am. Econ. Rev.</i> <b>112</b>, 3398–3440 (2022).",
"bracke2021":"Bracke, P. & Tenreyro, S. History dependence in the housing market. <i>Am. Econ. J. Macroecon.</i> <b>13</b>, 420–443 (2021).",
"einio2008":"Einiö, M., Kaustia, M. & Puttonen, V. Price setting and the reluctance to realize losses in apartment markets. <i>J. Econ. Psychol.</i> <b>29</b>, 19–34 (2008).",
"engelhardt2003":"Engelhardt, G. V. Nominal loss aversion, housing equity constraints, and household mobility: evidence from the United States. <i>J. Urban Econ.</i> <b>53</b>, 171–195 (2003).",
"anenberg2011":"Anenberg, E. Loss aversion, equity constraints and seller behavior in the real estate market. <i>Reg. Sci. Urban Econ.</i> <b>41</b>, 67–76 (2011).",
"bokhari2011":"Bokhari, S. & Geltner, D. Loss aversion and anchoring in commercial real estate pricing: empirical evidence and price index implications. <i>Real Estate Econ.</i> <b>39</b>, 635–670 (2011).",
"wang2020":"Wang, X., Li, K. & Wu, J. House price index based on online listing information: the case of China. <i>J. Hous. Econ.</i> <b>50</b>, 101715 (2020).",
"saez2010":"Saez, E. Do taxpayers bunch at kink points? <i>Am. Econ. J. Econ. Policy</i> <b>2</b>, 180–212 (2010).",
"kleven2016":"Kleven, H. J. Bunching. <i>Annu. Rev. Econ.</i> <b>8</b>, 435–464 (2016).",
"statecouncil2024":"State Council of the People's Republic of China. <i>Policy Measures to Promote Trade-in (Old-for-New) Housing Programmes</i> https://www.gov.cn (State Council of the People's Republic of China, 2024).",
}

# 1) find all [[...]] in order, assign numbers by first appearance
order = []
seen = {}
def collect(m):
    for key in m.group(1).split(";"):
        key = key.strip()
        if key not in seen:
            seen[key] = len(order)+1
            order.append(key)
    return m.group(0)
re.sub(r"\[\[([^\]]+)\]\]", collect, src)

# sanity: every key has a bib entry
missing = [k for k in order if k not in BIB]
assert not missing, f"missing bib entries: {missing}"

# 2) replace tags with collapsed superscript numbers (ranges with en-dash)
def collapse(nums):
    nums = sorted(nums)
    out=[]; i=0
    while i < len(nums):
        j=i
        while j+1 < len(nums) and nums[j+1]==nums[j]+1: j+=1
        if j-i>=2: out.append(f"{nums[i]}–{nums[j]}")
        else: out.extend(str(n) for n in nums[i:j+1])
        i=j+1
    return ",".join(out)
def repl(m):
    nums=[seen[k.strip()] for k in m.group(1).split(";")]
    return collapse(nums)
body = re.sub(r"\[\[([^\]]+)\]\]", repl, src)

# 3) build reference list (ordered by number)
reflines = ["", "## References", ""]
for i,key in enumerate(order,1):
    reflines.append(f"{i}. {BIB[key]}")
    reflines.append("")

backmatter = """
## Acknowledgements

We thank participants at the Asian Real Estate Society and Urban Economics Association meetings for constructive comments, and the online listing platform for facilitating access to the listing data under a data-use agreement. This work was supported by the National Natural Science Foundation of China (Grant Nos 72174091 and 72373067) and the Humanities and Social Sciences Foundation of the Ministry of Education of China (Grant No. 23YJA790015). The funders had no role in study design, data collection and analysis, decision to publish or preparation of the manuscript.

## Author contributions

Y.C. and M.F. conceived the study and designed the empirical strategy. Y.C. and H.L. assembled and cleaned the listing data and implemented the automated valuation model. H.L. designed and fielded the homeowner survey. Y.C. estimated the reference-dependence and liquidity models and conducted the counterfactual and policy simulations. J.K.W. contributed to the theoretical framing and the interpretation of the bunching and search results. Y.C., M.F. and J.K.W. wrote the manuscript, and all authors reviewed and approved the final version.

## Competing interests

The authors declare no competing interests.

## Additional information

**Correspondence and requests for materials** should be addressed to Y.C. or M.F.

**Peer review information** *Nature Communications* thanks the anonymous reviewers for their contribution to the peer review of this work.

**Reprints and permissions information** is available at http://www.nature.com/reprints.
"""

final = body.rstrip() + "\n" + "\n".join(reflines) + "\n" + backmatter
open(os.path.join(OUT,"paper_final.md"),"w").write(final)
print(f"references: {len(order)} | resolved citations OK")

# 4) pandoc -> docx with reference.docx styling if present
cmd = ["pandoc", os.path.join(OUT,"paper_final.md"),
       "-f","markdown+tex_math_dollars+raw_html+superscript",
       "-o", os.path.join(OUT,"paper.docx"),
       "--resource-path", OUT]
ref = os.path.join(OUT,"reference.docx")
if os.path.exists(ref): cmd += ["--reference-doc", ref]
r = subprocess.run(cmd, capture_output=True, text=True)
print("pandoc rc:", r.returncode)
if r.stderr: print(r.stderr[-1500:])
print("wrote paper.docx")
