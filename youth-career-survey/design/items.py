# -*- coding: utf-8 -*-
"""The instrument.

Every item is declared once here. The questionnaire document, the simulated
dataset, the codebook and the analysis all read this module, so the printed
questionnaire and the variable names in the data file cannot disagree.

Items are Chinese-language operationalisations written for this study and
mapped to the published instruments listed in ``SOURCES``. They are not
verbatim translations of the copyrighted originals; before fielding, check the
licensing note for each source in ``SOURCES``.
"""

# --------------------------------------------------------------------------
# response scales
# --------------------------------------------------------------------------
SCALES = {
    "agree5": ("1 = 完全不符合   2 = 比较不符合   3 = 一般   "
               "4 = 比较符合   5 = 完全符合", 5),
    "freq5": ("1 = 从不   2 = 很少   3 = 有时   4 = 经常   5 = 总是", 5),
    "conf5": ("1 = 完全没有信心   2 = 信心不足   3 = 一般   "
              "4 = 比较有信心   5 = 非常有信心", 5),
    "often5": ("1 = 从不   2 = 很少   3 = 有时   4 = 较频繁   "
               "5 = 非常频繁", 5),
    "agree9": ("1 = 完全不符合我   ……   5 = 一般   ……   9 = 完全符合我", 9),
}


# --------------------------------------------------------------------------
# constructs
#   key, 中文名, English name, variable prefix, scale, target latent mean on
#   the response metric, and the items
# --------------------------------------------------------------------------
class C:
    def __init__(self, key, cn, en, scale, loc, items, facets=None):
        self.key, self.cn, self.en = key, cn, en
        self.scale, self.loc = scale, loc
        self.items = items          # list of (code, text, reverse)
        self.facets = facets or {}  # facet name -> list of codes

    @property
    def codes(self):
        return [c for c, _, _ in self.items]


CA = C("CA", "职业决策焦虑", "Career decision-making anxiety", "agree5", 3.42, [
    ("CA1", "一想到毕业后要确定职业方向，我就感到紧张。", False),
    ("CA2", "我担心自己最终会选错职业道路。", False),
    ("CA3", "和同学谈起求职话题时，我会感到不安。", False),
    ("CA4", "想到未来要从事的工作，我心里常常没底。", False),
    ("CA5", "我害怕自己的能力配不上想去的岗位。", False),
    ("CA6", "需要为职业做决定的时候，我会想要回避。", False),
    ("CA7", "在职业选择这件事上，我总体上是从容的。", True),
    ("CA8", "临近毕业，我会因为职业问题而睡不好觉。", False),
])

CE = C("CE", "职业探索行为", "Career exploration", "freq5", 3.18, [
    ("CE1", "认真想过自己在工作中真正看重什么。", False),
    ("CE2", "反思过自己的性格适合哪一类职业。", False),
    ("CE3", "评估过自己在求职上的优势和短板。", False),
    ("CE4", "梳理过以往经历中让我最有成就感的部分。", False),
    ("CE5", "查阅过目标行业的招聘信息或行业报告。", False),
    ("CE6", "向已就业的学长学姐或从业者了解过工作内容。", False),
    ("CE7", "参加过宣讲会、招聘会或职业讲座。", False),
    ("CE8", "通过实习或兼职了解过某一职业的实际情况。", False),
], facets={"自我探索": ["CE1", "CE2", "CE3", "CE4"],
           "环境探索": ["CE5", "CE6", "CE7", "CE8"]})

SE = C("SE", "职业决策自我效能", "Career decision-making self-efficacy",
       "conf5", 3.31, [
    ("SE1", "判断自己的能力适合哪些职业", False),
    ("SE2", "说清楚自己在工作中最看重的三件事", False),
    ("SE3", "查到你感兴趣的职业近三年的就业与薪酬情况", False),
    ("SE4", "找到并联系上在你目标行业工作的人", False),
    ("SE5", "在几个都还不错的方向中选定一个", False),
    ("SE6", "即使家人不完全赞同，仍坚持自己认定的职业目标", False),
    ("SE7", "为实现职业目标制定未来两年的具体计划", False),
    ("SE8", "找出实现职业目标还需要补上的能力", False),
    ("SE9", "第一志愿走不通时，及时调整并另作打算", False),
    ("SE10", "在求职受挫之后重新振作、继续投递", False),
], facets={"自我评价": ["SE1", "SE2"], "信息收集": ["SE3", "SE4"],
           "目标选择": ["SE5", "SE6"], "制定规划": ["SE7", "SE8"],
           "问题解决": ["SE9", "SE10"]})

PA = C("PA", "父母自主支持型生涯支持", "Autonomy-supportive parental career "
       "support", "agree5", 3.58, [
    ("PA1", "在职业选择上，父母会先听我怎么想。", False),
    ("PA2", "父母鼓励我按照自己的兴趣去尝试。", False),
    ("PA3", "我犹豫的时候，父母会帮我把各个选择的利弊摆出来，但把决定权留给我。",
     False),
    ("PA4", "即使不是他们的首选，父母也尊重我最终的职业决定。", False),
    ("PA5", "父母会帮我留意机会、提供信息，但不替我做选择。", False),
    ("PA6", "父母把找工作看成是我自己的事，并支持我为此负责。", False),
])

PD = C("PD", "父母指导代办型生涯介入", "Directive parental career involvement",
       "agree5", 2.71, [
    ("PD1", "父母已经替我定好了毕业以后该做什么。", False),
    ("PD2", "在职业问题上，父母的意见基本上就是最后的决定。", False),
    ("PD3", "父母会直接替我联系工作机会或者托人打招呼。", False),
    ("PD4", "如果我的想法和父母不一致，他们会反复劝说直到我让步。", False),
    ("PD5", "父母认为我还不够成熟，不适合自己决定职业方向。", False),
    ("PD6", "父母会因为我不接受他们的安排而不高兴。", False),
])

PF = C("PF", "父母生涯参与频率", "Frequency of parental career involvement",
       "often5", 3.26, [
    ("PF1", "父母与我谈论毕业去向的频率。", False),
    ("PF2", "父母主动向我提供求职信息的频率。", False),
    ("PF3", "父母过问我求职进展的频率。", False),
])

CD = C("CD", "职业决策困难", "Career decision-making difficulties",
       "agree9", 4.63, [
    ("CD1", "我平时就不太会做决定，职业选择也不例外。", False),
    ("CD2", "我觉得现在还不到考虑职业的时候。", False),
    ("CD3", "我不太清楚一个职业决定要怎么做才算做好了。", False),
    ("CD4", "我期待一份“完美”的工作，又担心它并不存在。", False),
    ("CD5", "我不清楚自己更适合哪一类职业。", False),
    ("CD6", "我不了解可以选择的职业到底有哪些。", False),
    ("CD7", "我不掌握各个职业真实的工作内容和发展前景。", False),
    ("CD8", "我不知道该从哪里获得可靠的职业信息。", False),
    ("CD9", "关于同一个职业，我听到的说法彼此矛盾。", False),
    ("CD10", "我看重的几个条件（收入、稳定、兴趣）没办法同时满足。", False),
    ("CD11", "我想去的方向和身边重要的人希望的方向不一致。", False),
    ("CD12", "我对某个职业原先的印象和后来了解到的情况对不上。", False),
], facets={"缺乏准备": ["CD1", "CD2", "CD3", "CD4"],
           "缺乏信息": ["CD5", "CD6", "CD7", "CD8"],
           "信息不一致": ["CD9", "CD10", "CD11", "CD12"]})

MK = C("MK", "标记变量（颜色偏好）", "Marker variable (colour preference)",
       "agree5", 3.47, [
    ("MK1", "蓝色是我喜欢的颜色。", False),
    ("MK2", "买衣服或用品时，我倾向于选蓝色的。", False),
    ("MK3", "蓝色让我感到舒服。", False),
])

CONSTRUCTS = [CA, CE, SE, PA, PD, PF, CD, MK]
BY_KEY = {c.key: c for c in CONSTRUCTS}
SUBSTANTIVE = ["CA", "CE", "SE", "PA", "PD", "PF", "CD"]


# --------------------------------------------------------------------------
# attention checks — placed inside blocks, not at the end
# --------------------------------------------------------------------------
ATTENTION = [
    ("AC1", "本题用于检查作答质量，请直接选择“比较符合”。", "agree5", 4,
     "after_CE"),
    ("AC2", "本题不需要判断，请直接选择“5”。", "agree9", 5, "in_CD"),
]


# --------------------------------------------------------------------------
# background variables
# --------------------------------------------------------------------------
DEMO = [
    ("D1", "性别", ["1 男", "2 女"]),
    ("D2", "年级", ["1 本科三年级", "2 本科四年级", "3 硕士二年级",
                    "4 硕士三年级"]),
    ("D3", "学科门类", ["1 人文社科", "2 理学与工学", "3 经济与管理",
                        "4 医学", "5 艺术及其他"]),
    ("D4", "就读院校层次", ["1 “双一流”建设高校", "2 普通本科院校",
                            "3 高职高专院校"]),
    ("D5", "是否独生子女", ["1 是", "0 否"]),
    ("D6", "生源地", ["1 城市", "2 县城或城镇", "3 农村"]),
    ("D7", "父母双方的最高学历", ["1 初中及以下", "2 高中或中专", "3 大专",
                                  "4 本科", "5 硕士及以上"]),
    ("D8", "家庭月收入（元）", ["1 5000 以下", "2 5000–9999",
                                "3 10000–19999", "4 20000–29999",
                                "5 30000 及以上"]),
    ("D9", "实习经历", ["0 没有", "1 有，累计不足 3 个月",
                        "2 有，累计 3 个月及以上"]),
    ("D10", "目前的求职状态", ["1 尚未开始", "2 正在投递", "3 已参加面试",
                               "4 已获得录用意向", "5 已签约或已确定升学"]),
]

CONTROLS = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"]


# --------------------------------------------------------------------------
# instrument provenance and licensing
# --------------------------------------------------------------------------
SOURCES = {
    "CA": ("Chartrand, J. M., Robbins, S. B., Morrill, W. H., & Boggs, K. "
           "(1990). Career Factors Inventory 的焦虑分量表；Vignoli, E. "
           "(2015). Journal of Vocational Behavior, 89, 182–191 的生涯焦虑"
           "测量。",
           "两者均在论文正文中公布条目，研究使用需引用来源，无需另行付费授权。"),
    "CE": ("Stumpf, S. A., Colarelli, S. M., & Hartman, K. (1983). Career "
           "Exploration Survey. Journal of Vocational Behavior, 22, 191–226.",
           "条目见原文附录，研究使用需引用来源。"),
    "SE": ("Betz, N. E., Klein, K. L., & Taylor, K. M. (1996). Career "
           "Decision-Making Self-Efficacy Scale — Short Form.",
           "★ 该量表由 Mind Garden 发行，正式使用前必须购买许可并按份计费；"
           "本问卷条目为按五维度自行编写的等价测量，若要直接使用 CDMSE-SF "
           "原条目，请先取得授权。"),
    "PA": ("Turner, S. L., Alliman-Brissett, A., Lapan, R. T., Udipi, S., & "
           "Ergun, D. (2003). Career-Related Parent Support Scale；"
           "Guay, F., Senécal, C., Gauthier, L., & Fernet, C. (2003). "
           "Journal of Counseling Psychology, 50, 165–177 的自主支持测量。",
           "条目见原文，研究使用需引用来源。"),
    "PD": ("Dietrich, J., & Kracke, B. (2009). Career-specific parental "
           "behaviors. Journal of Vocational Behavior, 75, 109–119 的"
           "“干涉”（interference）分量表。",
           "条目见原文附录，研究使用需引用来源。"),
    "PF": ("为本研究编写，用以单独测量“参与的多少”，与 PA、PD 测量的"
           "“参与的方式”相区分。", "自编，无授权问题。"),
    "CD": ("Gati, I., Krausz, M., & Osipow, S. H. (1996). A taxonomy of "
           "difficulties in career decision making. Journal of Counseling "
           "Psychology, 43, 510–526；简版见 Gati, I., & Saka, N. (2001).",
           "CDDQ 可从作者的公开研究网站免费取得，研究使用需引用来源。"),
    "MK": ("Simmering, M. J., Fuller, C. M., Richardson, H. A., Ocal, Y., & "
           "Atinc, G. M. (2015). Organizational Research Methods, 18, "
           "473–511 建议的理论无关标记变量。",
           "自编等价条目，用于标记变量法检验共同方法偏差。"),
}


if __name__ == "__main__":
    n = sum(len(c.items) for c in CONSTRUCTS)
    print("构念 %d 个，条目 %d 条，注意力检测 %d 条，背景变量 %d 项"
          % (len(CONSTRUCTS), n, len(ATTENTION), len(DEMO)))
    for c in CONSTRUCTS:
        print("  %-3s %-14s %2d 条  %s" % (c.key, c.cn, len(c.items), c.scale))
