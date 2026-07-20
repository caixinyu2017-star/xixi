#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single source of truth for the research-methodology flowchart.

`BOXES` and `CONNS` are plain data (authored in the pixel space of the reference
image, ~1400x1040).  Two emitters consume them:
  * build_vsdx.py  -> native, editable Microsoft Visio .vsdx
  * make_preview.py -> HTML/SVG rendered to PNG (Chromium) for visual QA

Keeping one data model guarantees the QA preview matches the shipped .vsdx.
"""

# ---- reference-image pixel canvas ---------------------------------------- #
IMG_W, IMG_H = 1400.0, 1040.0

# ---- palette ------------------------------------------------------------- #
FONT       = "Microsoft YaHei"
TITLE_BLUE = "#2A5599"   # box titles + left-column labels + centred blue lines
LINE_BLUE  = "#3A6EB5"   # box borders
DASH_BLUE  = "#2E5B9E"   # dashed validation connector + inter-box double arrows
BLACK      = "#1A1A1A"
WHITE      = "#FFFFFF"
CONT_FILL  = "#E9F1FB"   # light-blue fill of the row-5 container
GRAY_DOT   = "#B4B4B4"   # left-column dotted row separators

# ---- named text styles: (size_pt, colour, align) ------------------------- #
# align: 0 left / 1 centre / 2 right
STYLES = {
    "label":     dict(size=17.0, color=TITLE_BLUE, align=0),
    "maintitle": dict(size=15.0, color=TITLE_BLUE, align=1),
    "title":     dict(size=13.5, color=TITLE_BLUE, align=1),
    "conttitle": dict(size=14.5, color=TITLE_BLUE, align=1),
    "body":      dict(size=11.5, color=BLACK,      align=0),
    "center_bk": dict(size=11.5, color=BLACK,      align=1),
    "center_bl": dict(size=12.0, color=TITLE_BLUE, align=1),
    "caption":   dict(size=11.0, color=BLACK,      align=0),
}

def P(style, text):
    return (style, text)

def box(px, paras, *, fill=WHITE, line=LINE_BLUE, line_w=1.4, rounding=6,
        valign="top", kind="box", name="Box"):
    """px = (left, top, right, bottom) in image pixels; valign top|middle."""
    return dict(kind=kind, px=px, paras=paras, fill=fill, line=line,
                line_w=line_w, rounding=rounding, valign=valign, name=name)

def text(px, paras, *, valign="middle", name="Lbl"):
    return box(px, paras, fill=None, line=None, line_w=0, rounding=0,
               valign=valign, kind="text", name=name)

def conn(points, *, begin=False, end=True, color=BLACK, w=1.3,
         dash=False, name="Conn"):
    return dict(points=points, begin=begin, end=end, color=color, w=w,
                dash=dash, name=name)

def vseg(x, y1, y2, **kw):
    return conn([(x, y1), (x, y2)], **kw)

def hseg(x1, x2, y, **kw):
    return conn([(x1, y), (x2, y)], **kw)


# ========================================================================= #
#  BOXES
# ========================================================================= #
BOXES = [
    # ---- left-column numbered labels ------------------------------------ #
    text((8, 40, 185, 95),   [P("label", "1. Sample")], name="L1"),
    text((8, 210, 185, 292), [P("label", "2. Data"), P("label", "collection")], name="L2"),
    text((4, 412, 188, 494), [P("label", "3. Narrative"), P("label", "preprocessing")], name="L3"),
    text((8, 582, 186, 664), [P("label", "4. Narrative"), P("label", "analysis")], name="L4"),
    text((4, 792, 188, 908), [P("label", "5. Psychometric"), P("label", "and substantive"), P("label", "evaluation")], name="L5"),

    # ---- row 1 : survey ------------------------------------------------- #
    box((475, 15, 935, 120), [
        P("maintitle", "Cross-sectional online survey"),
        P("center_bk", "N = 947 young adults aged 18–29"),
        P("center_bk", "Zhejiang Province, China"),
    ], valign="middle", name="Survey"),

    # ---- row 2 : A open-ended narratives -------------------------------- #
    box((218, 172, 672, 402), [
        P("title", "A. Open-ended career narratives"),
        P("body", "•  3 prompts completed before questionnaires"),
        P("body", "•  Current employment situation and main difficulties"),
        P("body", "•  Feelings about job seeking and career future"),
        P("body", "•  Three-year career goals and support needs"),
        P("body", " "),
        P("center_bl", "Median length ≈ 155 Chinese characters"),
    ], name="NarrA"),

    # ---- row 2 : B closed-ended measures -------------------------------- #
    box((742, 172, 1250, 402), [
        P("title", "B. Validated closed-ended measures"),
        P("body", "•  CDS (Career Distress Scale)"),
        P("body", "•  CAAS-SF (Career Adapt-Abilities Scale–Short Form)"),
        P("body", "•  GAD-7"),
        P("body", "•  PHQ-8"),
        P("body", "•  Perceived Employability"),
        P("body", "•  SWLS"),
    ], name="MeasB"),

    # ---- row 3 : de-identification -------------------------------------- #
    box((225, 425, 668, 478), [
        P("title", "De-identification and preprocessing"),
    ], valign="middle", name="Deid"),

    # ---- row 4 : A LLM scoring ------------------------------------------ #
    box((218, 528, 478, 732), [
        P("title", "A. LLM zero-shot scoring"),
        P("body", "•  GPT-4o and Qwen2.5-72B"),
        P("body", "•  3 runs per model; temperature = 0"),
        P("body", "•  Outputs: career distress, employment anxiety, career confidence"),
        P("body", "•  Ratings on 1–10 scales"),
    ], name="LLM"),

    # ---- row 4 : B embeddings & clustering ------------------------------ #
    box((525, 528, 882, 732), [
        P("title", "B. Semantic embeddings &"),
        P("title", "thematic clustering"),
        P("body", "•  BGE-M3 sentence embeddings"),
        P("body", "•  UMAP dimension reduction"),
        P("body", "•  k-means clustering"),
        P("body", "•  k = 6 (silhouette-guided)"),
        P("body", "•  Researcher-refined narrative themes"),
    ], name="Embed"),

    # ---- row 4 : C human coding ----------------------------------------- #
    box((930, 528, 1235, 732), [
        P("title", "C. Human expert coding"),
        P("body", "•  n = 200 stratified subsample"),
        P("body", "•  2 trained raters"),
        P("body", "•  Career-distress rubric (1–10)"),
        P("body", "•  Theme validation"),
    ], name="Human"),

    # ---- row 5 : container ---------------------------------------------- #
    box((185, 768, 1335, 978), [
        P("conttitle", "Psychometric and substantive evaluation"),
    ], fill=CONT_FILL, line=LINE_BLUE, line_w=2.0, rounding=8,
       valign="top", kind="container", name="EvalBox"),

    # ---- row 5 : four evaluation boxes ---------------------------------- #
    box((198, 818, 425, 968), [
        P("title", "A. Reliability"),
        P("body", "•  Run-level ICCs"),
        P("body", "•  Between-model agreement"),
        P("body", "•  Human-rater agreement"),
    ], name="RelA"),
    box((455, 818, 672, 968), [
        P("title", "B. Convergent &"),
        P("title", "discriminant validity"),
        P("body", "•  Multitrait correlation pattern"),
        P("body", "•  BH-FDR control"),
    ], name="ConvB"),
    box((738, 818, 992, 968), [
        P("title", "C. Incremental validity"),
        P("body", "•  Hierarchical ΔR²"),
        P("body", "•  ROC / AUC comparison"),
        P("body", "•  PHQ-8 and SWLS outcomes"),
    ], name="IncrC"),
    box((1045, 818, 1292, 968), [
        P("title", "D. Theme profiles"),
        P("body", "•  Theme prevalence"),
        P("body", "•  χ² by employment status"),
        P("body", "•  ANOVA on adjustment outcomes"),
    ], name="ThemeD"),

    # ---- bottom caption ------------------------------------------------- #
    text((185, 990, 1230, 1035), [
        P("caption", "Closed-ended scale scores served as validation criteria; inferential tests were two-tailed with Benjamini–Hochberg"),
        P("caption", "false-discovery-rate control where applicable."),
    ], valign="top", name="Cap"),
]

# ========================================================================= #
#  CONNECTORS
# ========================================================================= #
CONNS = [
    # left-column dotted row separators
    hseg(0, 178, 128, end=False, color=GRAY_DOT, w=1.0, dash=True, name="Sep"),
    hseg(0, 178, 405, end=False, color=GRAY_DOT, w=1.0, dash=True, name="Sep"),
    hseg(0, 178, 500, end=False, color=GRAY_DOT, w=1.0, dash=True, name="Sep"),
    hseg(0, 178, 745, end=False, color=GRAY_DOT, w=1.0, dash=True, name="Sep"),

    # survey -> A / B
    vseg(705, 120, 145, end=False),
    hseg(445, 996, 145, end=False),
    vseg(445, 145, 170),
    vseg(996, 145, 170),

    # A -> de-identification
    vseg(445, 402, 423),

    # de-identification -> 4A / 4B / 4C
    vseg(446, 478, 503, end=False),
    hseg(348, 1082, 503, end=False),
    vseg(348, 503, 526),
    vseg(703, 503, 526),
    vseg(1082, 503, 526),

    # 4A / 4B / 4C -> container
    vseg(348, 732, 766),
    vseg(703, 732, 766),
    vseg(1082, 732, 766),

    # closed-ended measures --> container (dashed blue, right margin)
    conn([(1250, 352), (1362, 352), (1362, 872), (1337, 872)],
         color=DASH_BLUE, w=1.6, dash=True, name="Dash"),

    # double-headed arrows between the four evaluation boxes
    hseg(425, 455, 893, begin=True, end=True, color=DASH_BLUE, w=1.6, name="Dbl"),
    hseg(672, 738, 893, begin=True, end=True, color=DASH_BLUE, w=1.6, name="Dbl"),
    hseg(992, 1045, 893, begin=True, end=True, color=DASH_BLUE, w=1.6, name="Dbl"),
]
