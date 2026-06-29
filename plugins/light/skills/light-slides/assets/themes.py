"""db06 十大 PPT 主题调色板与字体配对（COLORS / FONTS 常量块）。

每个主题给出一套可直接喂给 python-pptx 的色板（6 位 hex，无 #）与字体配对。
用法：
    from themes import THEMES, get_theme
    t = get_theme("academic")
    bg = t["COLORS"]["bg"]          # "FFFFFF"
    title_font = t["FONTS"]["title"] # "Source Han Serif SC"

设计依据（CONVENTIONS §5：只学版式/配色逻辑，最终原创）：
- 一主色占 60-70% 视觉权重 + 1-2 辅色 + 1 个尖锐强调色。
- bg/surface 给背景与卡片，text/muted 给正文与注释，primary/secondary/accent 给重点。
- 字体均为可商用：思源系/Noto(SIL OFL)、微软雅黑(随 Office)、Times/Helvetica/Consolas(系统)。
  若目标机无对应字体，python-pptx 会回退，建议交付前确认或嵌入字体。

色板字段约定（10 主题统一，便于 patterns/build_deck 复用）：
    bg        页面主背景
    surface   卡片/色块次级背景
    primary   主色（占视觉权重最高）
    secondary 辅助色
    accent    强调色（尖锐，用于一个重点）
    text      正文文字
    muted     注释/次要文字
    line      分隔线/描边
"""

# ---- 主题 01 学术风（浅色高级，对应 db06「学术答辩」卡）----
ACADEMIC = {
    "name": "academic",
    "label": "学术风/浅色高级",
    "scenario": "硕博答辩、毕业设计、会议报告",
    "dark": False,
    "COLORS": {
        "bg": "FFFFFF", "surface": "F2F5F9",
        "primary": "1F4E79", "secondary": "2E75B6", "accent": "C00000",
        "text": "333333", "muted": "808080", "line": "D9D9D9",
    },
    "FONTS": {"title": "Source Han Serif SC", "body": "Source Han Sans SC",
              "en": "Times New Roman", "mono": "Consolas"},
}
# ---- 主题 02 科技风（深色，对应「产品/方案发布」「技术分享」深底分支）----
TECH = {
    "name": "tech",
    "label": "科技风/深色",
    "scenario": "产品发布、技术架构、AI/算法分享",
    "dark": True,
    "COLORS": {
        "bg": "0B1220", "surface": "16203A",
        "primary": "2D9CDB", "secondary": "56CCF2", "accent": "F2C94C",
        "text": "EAF0FA", "muted": "8A98B5", "line": "27324D",
    },
    "FONTS": {"title": "Microsoft YaHei", "body": "Microsoft YaHei",
              "en": "Segoe UI", "mono": "JetBrains Mono"},
}

# ---- 主题 03 农业风（自然绿，土壤/作物场景）----
AGRICULTURE = {
    "name": "agriculture",
    "label": "农业风/自然",
    "scenario": "智慧农业、农学、生态、畜牧检测项目",
    "dark": False,
    "COLORS": {
        "bg": "FBFDF7", "surface": "EAF3DE",
        "primary": "4E7D2C", "secondary": "8AB661", "accent": "E08A1E",
        "text": "2E3A22", "muted": "7A8769", "line": "D2E0BF",
    },
    "FONTS": {"title": "Source Han Sans SC", "body": "Source Han Sans SC",
              "en": "Calibri", "mono": "Consolas"},
}

# ---- 主题 04 医学风（洁净蓝绿，临床/生物医学）----
MEDICAL = {
    "name": "medical",
    "label": "医学风/洁净",
    "scenario": "临床研究、医学影像、生物医学汇报",
    "dark": False,
    "COLORS": {
        "bg": "FFFFFF", "surface": "EAF4F4",
        "primary": "0E7C7B", "secondary": "17A2B8", "accent": "E4572E",
        "text": "1B2A2A", "muted": "6B8080", "line": "CFE3E3",
    },
    "FONTS": {"title": "Source Han Sans SC", "body": "Source Han Sans SC",
              "en": "Arial", "mono": "Consolas"},
}

# ---- 主题 05 商务风（沉稳藏青+金，路演/战略汇报）----
BUSINESS = {
    "name": "business",
    "label": "商务风/沉稳",
    "scenario": "商业计划、战略汇报、投融资",
    "dark": False,
    "COLORS": {
        "bg": "FCFCFD", "surface": "EFF1F5",
        "primary": "1B2A4A", "secondary": "415A77", "accent": "C9A227",
        "text": "212529", "muted": "6C757D", "line": "DDE1E8",
    },
    "FONTS": {"title": "Source Han Serif SC", "body": "Source Han Sans SC",
              "en": "Georgia", "mono": "Consolas"},
}

# ---- 主题 06 极简风（黑白灰 + 单强调色）----
MINIMAL = {
    "name": "minimal",
    "label": "极简风/黑白",
    "scenario": "组会、技术分享、强内容场合",
    "dark": False,
    "COLORS": {
        "bg": "FFFFFF", "surface": "F4F4F4",
        "primary": "111111", "secondary": "555555", "accent": "FF3B30",
        "text": "1A1A1A", "muted": "999999", "line": "E0E0E0",
    },
    "FONTS": {"title": "Source Han Sans SC", "body": "Source Han Sans SC",
              "en": "Helvetica", "mono": "JetBrains Mono"},
}

# ---- 主题 07 浅色高级风（莫兰迪低饱和，结题/工作汇报）----
LIGHT_ELEGANT = {
    "name": "light_elegant",
    "label": "浅色高级/莫兰迪",
    "scenario": "项目结题、工作汇报、通用浅色",
    "dark": False,
    "COLORS": {
        "bg": "FAF8F5", "surface": "ECE6DD",
        "primary": "7C6F64", "secondary": "A39788", "accent": "B5651D",
        "text": "3A352F", "muted": "8C8378", "line": "DED7CC",
    },
    "FONTS": {"title": "Source Han Sans SC", "body": "Source Han Sans SC",
              "en": "Calibri", "mono": "Consolas"},
}

# ---- 主题 08 深色高对比（聚光灯式，发布会/keynote）----
DARK_BOLD = {
    "name": "dark_bold",
    "label": "深色高对比/Keynote",
    "scenario": "产品发布会、主题演讲、视觉冲击场",
    "dark": True,
    "COLORS": {
        "bg": "0A0A0A", "surface": "1C1C1E",
        "primary": "FFFFFF", "secondary": "B0B0B5", "accent": "0A84FF",
        "text": "F5F5F7", "muted": "8E8E93", "line": "2C2C2E",
    },
    "FONTS": {"title": "Source Han Sans SC", "body": "Source Han Sans SC",
              "en": "Helvetica Neue", "mono": "JetBrains Mono"},
}

# ---- 主题 09 数据可视化风（中性底 + 色盲友好数据色）----
DATAVIZ = {
    "name": "dataviz",
    "label": "数据可视化/色盲友好",
    "scenario": "数据分析汇报、BI、实验结果展示",
    "dark": False,
    "COLORS": {
        "bg": "FFFFFF", "surface": "F0F2F5",
        "primary": "0072B2", "secondary": "E69F00", "accent": "D55E00",
        "text": "2B2B2B", "muted": "707070", "line": "DADDE1",
        # 额外：Okabe-Ito 色盲友好序列，供多序列图表取用
        "series": ["0072B2", "E69F00", "009E73", "D55E00",
                   "CC79A7", "56B4E9", "F0E442", "000000"],
    },
    "FONTS": {"title": "Source Han Sans SC", "body": "Source Han Sans SC",
              "en": "Arial", "mono": "Consolas"},
}

# ---- 主题 10 竞赛路演风（高对比品牌色，互联网+/挑战杯）----
PITCH = {
    "name": "pitch",
    "label": "竞赛路演/科技感",
    "scenario": "互联网+、挑战杯、创业大赛路演",
    "dark": True,
    "COLORS": {
        "bg": "10131A", "surface": "1B2030",
        "primary": "7B61FF", "secondary": "00D1B2", "accent": "FF4D6D",
        "text": "F2F4F8", "muted": "9AA3B5", "line": "2A3145",
    },
    "FONTS": {"title": "Microsoft YaHei", "body": "Microsoft YaHei",
              "en": "Montserrat", "mono": "JetBrains Mono"},
}

# ---- 注册表 ----
THEMES = {
    t["name"]: t for t in (
        ACADEMIC, TECH, AGRICULTURE, MEDICAL, BUSINESS,
        MINIMAL, LIGHT_ELEGANT, DARK_BOLD, DATAVIZ, PITCH,
    )
}


def get_theme(name):
    """按名取主题；未知名回退到 academic 并打印提示。"""
    if name not in THEMES:
        print(f"[themes] 未知主题 {name!r}，可选 {list(THEMES)}；回退 academic")
        return THEMES["academic"]
    return THEMES[name]


def list_themes():
    """返回 (name, label, scenario, dark) 列表，供选风格时速览。"""
    return [(t["name"], t["label"], t["scenario"], t["dark"])
            for t in THEMES.values()]


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"db06 主题数：{len(THEMES)}")
    for name, label, scen, dark in list_themes():
        tag = "深色" if dark else "浅色"
        c = THEMES[name]["COLORS"]
        print(f"  {name:14s} [{tag}] {label:20s} primary=#{c['primary']} accent=#{c['accent']}")
        print(f"                 场景：{scen}")
    # 自检：字段完整性
    required = {"bg", "surface", "primary", "secondary", "accent", "text", "muted", "line"}
    bad = [n for n, t in THEMES.items() if not required <= set(t["COLORS"])]
    assert not bad, f"色板字段缺失：{bad}"
    assert len(THEMES) == 10, f"应为 10 主题，实际 {len(THEMES)}"
    print("自检通过：10 主题，色板字段齐全。")

