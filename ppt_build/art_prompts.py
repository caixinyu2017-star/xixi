# -*- coding: utf-8 -*-
"""中文图释 → 英文提示词。每页一条，标签用中文原样引出。

图释共有的约定（对应 SKILL.md 第 1 步）：
  图型   ：示意图 + 文字解释（无需与真实坐标对齐的概念类图）
  画幅   ：PPT 16:9 内容区，1536x1024 生成后左右补白到 11.22" x 6.04"
  布局   ：标题条在上，主图在左/中，文字解释块在右/下
  风格   ：flat vector infographic、白底、细线、无阴影无 3D
"""

STYLE = (
    "flat vector infographic poster, clean white background, thin uniform "
    "stroke weight, generous white margins on the left and right edges, "
    "modern Chinese training-slide aesthetic, colour palette limited to deep "
    "green #2C6B53, orange #E55E24, blue #2E75B6, crimson #C02F2B, amber "
    "#E67E22 and warm cream #FFF7E8 on white, all text rendered in a clean "
    "Simplified Chinese sans-serif (Microsoft YaHei style), text large and "
    "crisp and perfectly legible, correct Chinese glyphs with no garbled or "
    "invented characters, no photorealism, no 3D bevel, no drop shadows, no "
    "lens flare, no stock-photo people, no watermark, no signature, no "
    "English filler text, no decorative clutter"
)

SPECS = {}


def spec(page, name, body):
    SPECS[page] = (name, body.strip().replace('\n', ' ') + ' ' + STYLE)


spec(13, 'pareto', """
A landscape infographic teaching the Pareto principle for a factory quality
class. Top banner in deep green with white heading text "柏拉图：80% 的损失，
通常来自 20% 的原因". Left two thirds: a Pareto chart with five vertical bars
descending in height, labelled under the axis "内孔超差", "毛刺", "划伤",
"装配错", "其他", with the value written on top of each bar as "42", "18",
"9", "5", "4"; an orange cumulative-percentage line with round markers rises
across the bars and is labelled "53.8%", "76.9%", "88.5%", "94.9%", "100%";
a horizontal dashed reference line near the top labelled "80% 分界线"; the
first two bars are highlighted in crimson and enclosed by a dashed rectangle
tagged "先打这两根". Y axis labelled "不良件数", secondary axis labelled
"累计占比". Right third: a donut chart split 77 / 23 with the large slice in
crimson labelled "前 2 项 占 77%" and the small slice in light grey labelled
"其余 3 项 23%"; beneath the donut two stacked note cards, the first with a
green header bar reading "怎么读这张图" and body text "先排序，再画累计线，
取到 80% 为止；线以左的项目才立课题", the second with an orange header bar
reading "常见误用" and body text "只按件数排序，忘了金额和风险：件数少的一件
就是一次客诉". A full-width amber footer bar with white text "核心要点　
件数、金额、风险三张柏拉图都要画，再决定先做哪一项".
""")


spec(5, 'gap', """
A landscape teaching infographic defining what a problem is. Top banner in
deep green with white heading "问题 = 应有状态 − 现实状态". Centre of the
canvas: a large equation built from three rounded panels in a row — a green
panel labelled "应有状态", a big minus sign, a crimson panel labelled
"现实状态", a big equals sign, a blue panel labelled "问题". Under the green
panel a list "图纸公差 / SOP / 节拍 / 合同交期 / 安全规程"; under the crimson
panel a list "实测尺寸 / 实际产出 / 实际不良 / 实际工时"; under the blue
panel the text "两者之间可测量的差距　差距越具体，越好解". Below that, a
horizontal measuring-bar illustration: a green tick mark on the left labelled
"标准 0.5%", a crimson tick on the right labelled "实际 1.8%", and a
double-headed arrow between them labelled "差距 1.3% ＝ 问题". Bottom left a
cream note card with an amber header "查不下去的原因" and body "“效率低”——
低于什么？“配合不好”——好的标准是什么？". A full-width amber footer bar with
white text "核心要点　标准不存在时，你得到的不是问题，是意见分歧".
""")

spec(7, 'sangen', """
A landscape teaching infographic about the Toyota three-actuals principle.
Top banner in deep green with white heading "三现主义：不到现场，你分析的都是
想象". Centre: three large circles in a row joined by right-pointing arrows,
each with a simple flat line icon above its label — a factory floor icon over
the green circle labelled "现场", a defective part icon over the orange
circle labelled "现物", a clipboard-with-chart icon over the blue circle
labelled "现实"; captions under the circles read "到问题发生的那个地点去",
"拿到那个出问题的实物", "看真实的数据，不听转述". Lower left a cream card
with a crimson header "不去现场会发生什么" and body "办公室听到的是“操作
不当”，现场才发现工装定位块已磨损；报表上是“不良率 2%”，现场才发现全部集中
在夜班某一台". Lower right a cream card with a green header "到现场要带三样
东西" and body "① 不良实物（不是照片）② 当时的参数记录和批次号 ③ 一个不预设
答案的脑子". A full-width amber footer bar with white text "核心要点　
“我觉得是……”这五个字出现时，就该起身去现场了".
""")

spec(8, 'w5h2', """
A landscape teaching infographic for the 5W2H problem-framing tool. Top
banner in deep green with white heading "5W2H：把一句抱怨拆成一个可查的问题".
Left half: seven coloured rounded tags stacked vertically, each followed by a
cream answer strip — "What" with "什么问题" and answer "X 型阀体内孔尺寸超差";
"Where" with "哪里发生" and answer "B 线 3 号机，精镗工序"; "When" with
"什么时候" and answer "近两周，集中在夜班后半程"; "Who" with "涉及谁" and
answer "夜班 2 名操作工，同一名技术员改机"; "Why" with "为何是问题" and
answer "标准 ≤0.5%，实际 1.8%，已致客诉 1 起"; "How" with "怎么发现的" and
answer "下工序装配压不进，返查尺寸"; "How much" with "多大代价" and answer
"报废 42 件，返工 6.5 工时". Right half: a large before-and-after comparison,
a crimson card headed "填之前" containing "“质量不好，要加强巡检。”" and
below it a downward arrow, then a green card headed "填之后" containing
"“B 线 3 号机 X 型阀体内孔超差 42 件，占 1.8%，标准 ≤0.5%。”". A full-width
amber footer bar with white text "核心要点　填不出来的那一格，就是你现在最该
去查的地方".
""")

spec(11, 'iceberg', """
A landscape teaching infographic drawn as an iceberg cross-section. Top
banner in deep green with white heading "症状、问题、真因：你在哪一层解决，
决定了它会不会回来". A horizontal light-blue waterline runs across the
canvas. Above the waterline the small crimson iceberg tip is labelled
"症状层" with the caption "客户投诉、返工、停机". Just at the waterline an
orange band of the iceberg is labelled "问题层" with the caption "某工序某
尺寸超差 1.8%". Deep below the waterline the large green mass of the iceberg
is labelled "真因层" with the caption "定位块磨损，无更换标准". To the right
of each layer a matching cream note strip: beside 症状层 "处理方式：救火　
效果：立刻见效，必然复发"; beside 问题层 "处理方式：加强管控　效果：能压住，
人一松就回来"; beside 真因层 "处理方式：改标准、改工装　效果：慢，但不再
回来". A downward arrow along the left edge labelled "越往下越治本". A
full-width amber footer bar with white text "自检　对策里出现“加强、注意、
强调、增加检查”，说明你还在症状层".
""")

spec(18, 'strata', """
A landscape teaching infographic about data stratification. Top banner in
deep green with white heading "层别法：把一堆数据拆开看，问题自己会跳出来".
Top of the body: a wide crimson bar containing "不层别：本月不良率 1.2%　→　
结论：“大家再注意一点”". Below it a fan of four downward arrows splitting
into four columns. Each column is a cream card with a coloured header and a
small two-bar comparison chart inside: green header "按班次" with bars
labelled "白班 0.4%" and "夜班 2.1%"; orange header "按机台" with bars
"1~4 号 0.5%" and "3 号机 3.6%"; blue header "按人员" with bars "熟手 0.3%"
and "新人 2.8%"; purple header "按批次" with bars "A 供应商 0.4%" and
"B 供应商 2.4%"; in every pair the second bar is drawn much taller and in a
warning colour. A full-width amber footer bar with white text "核心要点　
层别之后，“大家注意”变成四个能立刻派人去查的方向".
""")

spec(22, 'fivewhy', """
A landscape teaching infographic for the 5 Why method. Top banner in deep
green with white heading "5Why：不是问五次，是每一次都能被验证". The body is
a descending staircase of six rows, each row a coloured tag on the left, a
cream statement box in the middle and a bordered verification box on the
right, connected top to bottom by downward arrows. Row one, crimson tag
"现象", statement "机器停了", verification "——". Row two, blue tag "Why 1",
statement "超负荷，保险丝断了", verification "查：电流记录". Row three, blue
tag "Why 2", statement "轴承润滑不足", verification "查：油量与油压". Row
four, blue tag "Why 3", statement "油泵抽油不足", verification "查：泵的
排量". Row five, blue tag "Why 4", statement "泵轴磨损", verification
"拆：看磨损痕迹". Row six, green tag "Why 5", statement "没装过滤器，铁屑
进入", verification "查：有无过滤器". A vertical label down the right edge
reads "每一层都要有一个能去现场做的动作". A full-width amber footer bar with
white text "核心要点　问不动的时候，不是问题问完了，是你还没去现场".
""")

spec(24, 'fishbone', """
A landscape teaching infographic drawn as a classic cause-and-effect fishbone
diagram. Top banner in deep green with white heading "鱼骨图 5M1E：先穷举，
再收敛". A long horizontal spine arrow points right into a crimson box at the
head labelled "内孔超差 1.8%". Six diagonal ribs join the spine, three from
above and three from below, each rib ending in a coloured label box with two
or three small twigs carrying short text. Upper ribs, green "人 Man" with
twigs "技能经验", "疲劳", "交接"; blue "机 Machine" with twigs "精度磨损",
"保养", "参数"; orange "料 Material" with twigs "来料波动", "批次", "存放".
Lower ribs, purple "法 Method" with twigs "SOP", "节拍", "检验方法"; teal
"测 Measurement" with twigs "量具校准", "判定标准"; crimson "环 Environment"
with twigs "温度湿度", "照明", "振动". Three of the twigs are circled with a
dashed crimson ring and tagged "圈出 3~5 条去验证". A full-width amber footer
bar with white text "三条纪律　先发散不评价　每根小骨都要能查　画完必须收敛".
""")

spec(28, 'threecond', """
A landscape teaching infographic built on a three-circle Venn diagram. Top
banner in deep green with white heading "真因的三个条件：同时成立才算数". In
the centre three large overlapping translucent circles — a green circle
labelled "① 能解释", a blue circle labelled "② 能重现", an orange circle
labelled "③ 能消除" — and the small central overlap is filled crimson and
labelled "真 因". A short caption sits outside each circle: beside the green
one "能解释所有已观察到的事实，包括“为什么别的机台没有”"; beside the blue one
"人为制造这个条件，问题会再次出现——最硬的证据"; beside the orange one "去掉
它问题消失，恢复它问题又回来". Bottom left a cream card with a blue header
"为什么“能重现”最容易被跳过" and body "因为要故意把不良做出来，很多人觉得
浪费；不做这一步，你永远只是在赌". Bottom right a cream card with a green
header "半小时的做法" and body "拿 3~5 件料，在受控条件下把怀疑的因素还原
一次，看问题是否出现". A full-width amber footer bar with white text
"反常识　找到一个“很有道理”的原因时，先想办法把它证伪，而不是立刻改".
""")

spec(33, 'fourlevel', """
A landscape teaching infographic drawn as a four-step ascending staircase,
lowest step on the left and highest on the right, with a long arrow rising
left-to-right above the staircase labelled "越往后越治本". Top banner in deep
green with white heading "对策的四个层次：越往后越治本". Step one in crimson labelled
"第一层　强调" with the caption "开会讲、贴标语、班前会强调" and a small tag
"有效期：约 3 天". Step two in orange labelled "第二层　检查" with the caption
"加抽检、加巡检、加一道全检" and a tag "有效期：只要还在检就有效，成本持续".
Step three in blue labelled "第三层　提示" with the caption "贴样板、做标识、
加颜色区分、加提示灯" and a tag "有效期：较长，但没杜绝". Step four in deep
green labelled "第四层　防错" with the caption "装错就装不进、漏做就走不到
下一步" and a tag "有效期：永久". A dashed bracket spans steps one and two
tagged "大多数班组停在这里". A full-width amber footer bar with white text
"反常识　“加强教育”不是最容易的对策，是最贵的对策——成本被摊到未来每一天".
""")

spec(34, 'pokayoke', """
A landscape teaching infographic for Poka-Yoke mistake-proofing. Top banner
in deep green with white heading "防错法 Poka-Yoke：让错误做不出来". The body
is a two-row grid of six cream tiles, each with a coloured header strip, a
simple flat line icon, a definition line and an example line. Tile one, green
header "断根", definition "从根本上消除出错的可能", example "非对称设计：
装反就装不进去". Tile two, blue header "保险", definition "几个条件同时满足
才能进行", example "安全门没关，设备就不能启动". Tile three, orange header
"自动", definition "用机器代替人的判断", example "扭矩扳手到值自动跳停". Tile
four, purple header "相符", definition "用比对来检查正误", example "用样板
卡一下，对不上就是错的". Tile five, teal header "顺序", definition "按步骤
锁定，不能跳步", example "上一步没扫码，下一步不放行". Tile six, crimson
header "隔离", definition "把不同的东西物理分开", example "相似零件用不同
颜色料盒". A long left-to-right arrow runs beneath the grid labelled
"选型顺序：断根 → 保险 → 自动 → 相符 → 顺序 → 隔离". A full-width amber
footer bar with white text "核心要点　越靠前的方案越不依赖人，成本往往还更低".
""")

spec(38, 'sdca', """
A landscape teaching infographic contrasting two improvement cycles. Top
banner in deep green with white heading "PDCA 之后是 SDCA：改善的成果靠标准
锁住". Left half: two circular arrow cycles side by side on a rising slope. The
first wheel has four quadrants labelled "P", "D", "C", "A" and the caption
"改善：把水平提上去"; the second wheel has four quadrants labelled "S", "D",
"C", "A" and the caption "标准化：把水平垫住". A wedge-shaped chock drawn
under the second wheel is labelled "标准 = 防滑楔"; a crimson dashed arrow
curving backwards down the slope is labelled "没有 S，转一圈就回到原点". Right
half: two stacked cream cards. The upper card has a green header "标准化要写
清楚的五件事" and body lines "① 做什么：具体动作 ② 做到什么程度：数值和判定
③ 什么时候做：频次和时点 ④ 谁做、谁查 ⑤ 异常找谁、多久响应". The lower card
has a crimson header "标准写了没人用的三个原因" and body lines "① 太长：十页
没人看 ② 太远：锁在柜里不在工位 ③ 没参与：写的人和做的人不是一批人". A
full-width amber footer bar with white text "核心要点　成果不写进标准，就只是
这一批人的临时表现，不是班组的能力".
""")


# ---------------------------------------------------------------- 《价值 & 开发》
def vspec(page, name, body):
    SPECS[page] = (name, body.strip().replace('\n', ' ') + ' ' + STYLE)


vspec(1009, 'v9_iceberg', """
A landscape iceberg infographic for a sales-talent training class. Top banner in
deep green with white heading "潜力评估：冰山之上教得会，冰山之下换不掉". A light
blue waterline crosses the canvas. The small tip above the water is blue and
carries two labelled bands, "知识" and "技能", with the caption to its right
"教得会：培训一周补一半，刻意练习三个月见变化". The large mass below the water is
deep green and carries four stacked labelled bands from top to bottom,
"社会角色", "自我认知", "特质", "动机", with the caption to its right "换不掉：
选比育更划算，决定这个人的天花板". A crimson downward arrow along the left edge is
labelled "越往下越难改". On the right a cream note card with an orange header
"投放顺序" and body "培训预算：技能 → 知识；招聘筛选：动机 → 特质。很多公司把两者
搞反了". A full-width amber footer bar with white text "反常识　面试最该问的不是
「你会什么」，而是「上一次被客户拒绝后你做了什么」".
""")

vspec(1016, 'v16_flow', """
A landscape infographic drawn as a four-step ascending staircase, lowest on the
left. Top banner in deep green with white heading "价值流：从「可训练」到「胜任
愉快」，卡点在哪一段". Step one blue labelled "可训练" with caption "愿意学、教得会，
还不能独立交付"; step two teal labelled "可用" with caption "能做完标准动作，遇到
例外就卡住"; step three deep green labelled "胜任" with caption "独立拿结果，例外
也能处理"; step four orange labelled "胜任愉快" with caption "越干越有劲，开始产出
方法和人". Between the steps three crimson gap markers each carry a short label:
between one and two "没人教，或者只让他跟着看", between two and three "只做重复的事，
从不给例外", between three and four "看不到下一步——这一段最容易丢人". A dashed
crimson box hovering between step three and four is tagged "能干但不想干". A
full-width amber footer bar with white text "现场动作　把团队每个人贴到这四级上，
这就是写 IDP 的起点".
""")

vspec(1021, 'v21_funnel', """
A landscape sales-funnel infographic. Top banner in deep green with white heading
"过程跟踪：结果出来才管，就永远在救火". The left two thirds show a horizontal funnel
narrowing left to right, split into six coloured segments labelled in order
"触达", "首访", "试用", "报价", "成交", "复购"; under each segment a small caption
reads "拿到对的人", "拿到工况", "占住一个工位", "拿到决策链", "写进图纸", "扩品类".
Small crimson drip arrows fall out of the bottom of the 首访 and 试用 segments,
tagged "漏得最多". Above the funnel a dashed bracket spans 触达 to 报价 labelled
"这一段才管得住结果". The right third holds two stacked cream cards: the first with
a blue header "该盯的过程指标" and body "拿到工况参数的家数 / 送样上机的工位数 /
试用后两周内跟进的家数"; the second with an orange header "两个被低估的事实" and
body "平均要七次以上触达才成交，多数人第三次就停了；决策链常有 5~8 人，技术话语权
远高于采购". A full-width amber footer bar with white text "周会只问一句　这周漏斗
每一环各推进了几家".
""")

vspec(1026, 'v26_ninebox', """
A landscape nine-box talent grid infographic. Top banner in deep green with white
heading "九宫格：把「绩效 × 潜力」摆到桌面上". The body is a 3 by 3 grid of rounded
cells. A vertical axis label on the left reads "潜力" with tick labels "高", "中",
"低" from top to bottom; a horizontal axis label under the grid reads "绩效" with
tick labels "低", "中", "高" from left to right. Top row cells, left to right:
green "疑似错配 / 换位置或换主管" is at the LEFT, mid-green "潜力新秀 / 找卡点、加
陪练" in the middle, bright green "明日之星 / 给舞台、给难题" at the RIGHT. Middle
row: amber "待观察 / 定期限、给标准" left, teal "核心员工 / 稳定输出、别折腾" middle,
blue "中坚骨干 / 守住他、扩品类" right. Bottom row: crimson "待改进 / 三个月内给结论"
left, grey "一般贡献 / 维持、控成本" middle, purple "专才熟手 / 认可、别硬提拔" right.
The top-right cell has a thicker highlighted border. A full-width amber footer bar
with white text "盘点不产生价值，盘点之后的那三次谈话才产生价值".
""")

vspec(1036, 'v36_702010', """
A landscape infographic explaining the 70-20-10 development mix. Top banner in
deep green with white heading "三条开发路径：七成靠做事，两成靠带教，一成靠上课".
Centre-left: a large donut chart split into three arcs — a deep green arc taking
70 percent labelled "70　在岗做事", a blue arc taking 20 percent labelled
"20　他人带教", an orange arc taking 10 percent labelled "10　脱岗学习"; the donut
centre reads "行为改变发生在现场". Right side: three stacked cream note cards
matching the arc colours. The green one headed "在岗做事" with body "任务委派、陪访
复盘、独立负责一块客户——关键不在让他做，在做完有人陪他复盘". The blue one headed
"他人带教" with body "师徒制、案例分享；产出物必须是可复用的东西，不只是跟着跑了几趟".
The orange one headed "脱岗学习" with body "课程、展会、认证；回来没有任务承接，两周
后就归零". A small grey footnote strip under the donut reads "这个比例是启发式，不是
被严格验证过的定律". A full-width amber footer bar with white text "安排培训时真正该问
的是——他回来用哪一件真实的事把它跑一遍".
""")

vspec(1037, 'v37_ojt', """
A landscape infographic showing a four-step teaching ladder, left to right, joined
by arrows. Top banner in deep green with white heading "OJT 的正确姿势：任务委派的
四个台阶". Step one blue labelled "我做你看" with caption "边做边说，把判断讲出来";
step two green labelled "你做我看" with caption "他上手，我不插嘴"; step three
orange labelled "你做我问" with caption "做完复盘，只问不评"; step four purple
labelled "你做你说" with caption "他能教别人，才算真会". Under step one a crimson
callout box reads "最容易被跳过的一步" and beside it three quoted lines in a cream
card headed "要讲出来的三句判断": "我为什么先问节拍不问预算", "他说「再考虑」时我为什么
没追价格", "这一单我为什么宁可不接". On the right a cream card with a green header
"任务委派三件套" and body "① 交付物：两周内拿到产线节拍与现用型号 ② 权限边界：他能自己
定什么 ③ 复盘时间：开始时就约进日程". A full-width amber footer bar with white text
"检验　新人能不能把你的判断复述出来——复述不出来，他只是模仿了动作".
""")

vspec(1042, 'v42_tco', """
A landscape infographic titled as a cost-of-ownership calculator for industrial
sales. Top banner in deep green with white heading "把价格谈判掰成价值谈判：四个算账
锚点". A large equation strip near the top reads "客户的一年总成本 ＝ 采购价 ＋ 停机
損失 ＋ 备件持有 ＋ 换型时间" — render that strip with the correct characters
"客户的一年总成本 ＝ 采购价 ＋ 停机损失 ＋ 备件持有 ＋ 换型时间". Below it a row of four
equal cream cards, each with a coloured header, a large number and a caption. Card
one, crimson header "停机", big number "63.6 万元/小时", caption "行业调研给出的中国
企业均值——先问他这条线是多少". Card two, blue header "寿命", big number "1000 万次",
caption "标准工况气缸平均往复次数，按每分钟 10 次约合 3 年". Card three, purple header
"备件", big number "20%~30%", caption "备件年持有成本占账面价值的比例". Card four,
green header "换型", big number "＋12.5%", caption "换型由 45 分钟压到 25 分钟带来的
OEE 提升". Under the four cards a horizontal arrow points from a grey box labelled
"只谈单价" to a green box labelled "谈一年总成本". A full-width amber footer bar with
white text "客户越是只谈价格，越说明你还没让他看见别的账".
""")

vspec(1052, 'v52_grow', """
A landscape infographic for the GROW coaching model, drawn as four large connected
circles in a row joined by right-pointing arrows, each circle carrying one big
letter and a Chinese label beneath. Top banner in deep green with white heading
"GROW：把「我告诉你怎么做」换成「你打算怎么做」". Circle one green with letter "G" and
label "Goal　收窄"; circle two blue with letter "R" and label "Reality　只问事实";
circle three orange with letter "O" and label "Options　逼出三个"; circle four
crimson with letter "W" and label "Will　落到日期". Under each circle a cream speech
bubble holds a ready-made question: under G "这 20 分钟，你最想理清哪一件事？"; under
R "你上一次跟他联系是什么时候、他说了什么原话？"; under O "如果不能降价，你还能给他
什么？"; under W "具体哪一天？需要我做什么？". Two crimson warning tags float above
the row: one over R reading "别在这一步给答案", one over W reading "别接受「我尽快」".
A full-width amber footer bar with white text "他说出口的才会做；你说的，他只记住你
说过".
""")
