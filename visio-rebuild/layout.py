#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single source of truth for the methodology-flowchart layout.

Coordinates are authored in a top-left "design pixel" space that mirrors the
reference image (1456 x 1120).  Both the Visio emitter (build_vsdx.py) and the
raster preview (preview.py) consume the specs returned by build_shapes(), so the
thing that is visually checked is exactly the thing that is written to .vsdx.
"""

SCALE = 100.0
DESIGN_W = 1456.0
DESIGN_H = 1120.0

# palette ------------------------------------------------------------------
NAVY   = "#1F3864"
BLUE   = "#2E5C9E"
DARK   = "#1A1A1A"
BORDER = "#2E5C9E"
GRAY   = "#AEB6C2"
WHITE  = "#FFFFFF"
CFILL  = "#EEF3FB"
BLK    = "#000000"
CAP    = "#333333"
FONT   = "微软雅黑"        # Microsoft YaHei (bold everywhere)

# font sizes (points) ------------------------------------------------------
SZ_SURVEY_T = 16.5
SZ_SURVEY_S = 13.5
SZ_TITLE    = 14.0
SZ_TITLE4   = 13.5
SZ_BULLET   = 12.5
SZ_BULLET4  = 12.0
SZ_ACCENT   = 12.5
SZ_ROWLBL   = 15.5
SZ_CTITLE   = 15.5
SZ_STITLE   = 13.0
SZ_SBULLET  = 11.5
SZ_CAPTION  = 11.5
SZ_DEID     = 14.0


def T(text, size, color, align=0, spafter=0.0):
    return dict(text=text, size=size, color=color, align=align, spafter=spafter)


def bullets(items, size, color=DARK):
    return [T("•  " + it, size, color, align=0, spafter=0.012) for it in items]


def build_shapes():
    S = []
    box = lambda **k: S.append(dict(kind="box", **k))
    lab = lambda **k: S.append(dict(kind="label", **k))
    ln = lambda **k: S.append(dict(kind="line", **k))

    # ---- left dotted stage separators (back) ----------------------------
    for sy in (150, 430, 522, 792):
        ln(x1=16, y1=sy, x2=178, y2=sy, color=GRAY, lw=0.01, pattern=3, name="Sep")

    # ---- connectors (behind boxes) --------------------------------------
    ln(x1=733, y1=126, x2=733, y2=150, color=BLK, name="c_stub")
    ln(x1=463, y1=150, x2=1042, y2=150, color=BLK, name="c_bus1")
    ln(x1=463, y1=150, x2=463, y2=172, color=BLK, end_arrow=4, name="c_toA")
    ln(x1=1042, y1=150, x2=1042, y2=172, color=BLK, end_arrow=4, name="c_toB")
    ln(x1=463, y1=412, x2=463, y2=448, color=BLK, end_arrow=4, name="c_toDeid")
    ln(x1=463, y1=502, x2=463, y2=522, color=BLK, name="c_deidstub")
    ln(x1=358, y1=522, x2=1119, y2=522, color=BLK, name="c_bus2")
    ln(x1=358, y1=522, x2=358, y2=556, color=BLK, end_arrow=4, name="c_to4A")
    ln(x1=731, y1=522, x2=731, y2=556, color=BLK, end_arrow=4, name="c_to4B")
    ln(x1=1119, y1=522, x2=1119, y2=556, color=BLK, end_arrow=4, name="c_to4C")
    ln(x1=358, y1=764, x2=358, y2=795, color=BLK, end_arrow=4, name="c_5A")
    ln(x1=731, y1=764, x2=731, y2=795, color=BLK, end_arrow=4, name="c_5B")
    ln(x1=1119, y1=764, x2=1119, y2=795, color=BLK, end_arrow=4, name="c_5C")
    # dashed validation link (B measures -> evaluation band)
    ln(x1=1322, y1=292, x2=1410, y2=292, color=BLUE, lw=0.014, pattern=2, name="v1")
    ln(x1=1410, y1=292, x2=1410, y2=905, color=BLUE, lw=0.014, pattern=2, name="v2")
    ln(x1=1410, y1=905, x2=1346, y2=905, color=BLUE, lw=0.014, pattern=2,
       end_arrow=4, name="v3")

    # ---- top survey box -------------------------------------------------
    box(x=490, y=18, w=486, h=108, valign=1, name="Survey", paras=[
        T("Cross-sectional online survey", SZ_SURVEY_T, NAVY, 1, 0.03),
        T("N = 947 young adults aged 18–29", SZ_SURVEY_S, BLUE, 1),
        T("Zhejiang Province, China", SZ_SURVEY_S, BLUE, 1),
    ])

    # ---- row 2: narratives (A) & measures (B) ---------------------------
    box(x=226, y=172, w=474, h=240, valign=0, name="BoxA", paras=(
        [T("A. Open-ended career narratives", SZ_TITLE, NAVY, 1, 0.05)]
        + bullets([
            "3 prompts completed before questionnaires",
            "Current employment situation and main difficulties",
            "Feelings about job seeking and career future",
            "Three-year career goals and support needs",
        ], SZ_BULLET)
        + [T("", 8, DARK, 1, 0.04),
           T("Median length ≈ 155 Chinese characters", SZ_ACCENT, BLUE, 1)]))

    box(x=762, y=172, w=560, h=240, valign=0, name="BoxB", paras=(
        [T("B. Validated closed-ended measures", SZ_TITLE, NAVY, 1, 0.05)]
        + bullets([
            "CDS (Career Distress Scale)",
            "CAAS-SF (Career Adapt-Abilities Scale–Short Form)",
            "GAD-7",
            "PHQ-8",
            "Perceived Employability",
            "SWLS",
        ], SZ_BULLET)))

    # divider rule inside Box A (drawn on top of the box)
    ln(x1=240, y1=360, x2=686, y2=360, color=BLUE, lw=0.012, pattern=1, name="A_rule")

    # ---- row 3: de-identification ---------------------------------------
    box(x=226, y=448, w=474, h=54, valign=1, name="Deid", paras=[
        T("De-identification and preprocessing", SZ_DEID, NAVY, 1)])

    # ---- row 4: three analysis tracks -----------------------------------
    box(x=193, y=556, w=330, h=208, valign=0, name="Box4A", paras=(
        [T("A. LLM zero-shot scoring", SZ_TITLE4, NAVY, 1, 0.05)]
        + bullets([
            "GPT-4o and Qwen2.5-72B",
            "3 runs per model; temperature = 0",
            "Outputs: career distress, employment anxiety, career confidence",
            "Ratings on 1–10 scales",
        ], SZ_BULLET4)))

    box(x=552, y=556, w=358, h=208, valign=0, name="Box4B", paras=(
        [T("B. Semantic embeddings & thematic clustering", SZ_TITLE4, NAVY, 1, 0.05)]
        + bullets([
            "BGE-M3 sentence embeddings",
            "UMAP dimension reduction",
            "k-means clustering",
            "k = 6 (silhouette-guided)",
            "Researcher-refined narrative themes",
        ], SZ_BULLET4)))

    box(x=947, y=556, w=344, h=208, valign=0, name="Box4C", paras=(
        [T("C. Human expert coding", SZ_TITLE4, NAVY, 1, 0.05)]
        + bullets([
            "n = 200 stratified subsample",
            "2 trained raters",
            "Career-distress rubric (1–10)",
            "Theme validation",
        ], SZ_BULLET4)))

    # ---- row 5: evaluation container + four sub-boxes -------------------
    box(x=185, y=795, w=1187, h=205, fill=CFILL, valign=0, rounding=0.09,
        name="EvalContainer", paras=[
            T("Psychometric and substantive evaluation", SZ_CTITLE, NAVY, 1)])

    box(x=208, y=845, w=222, h=150, valign=0, name="EvalA", paras=(
        [T("A. Reliability", SZ_STITLE, NAVY, 1, 0.05)]
        + bullets(["Run-level ICCs", "Between-model agreement",
                   "Human-rater agreement"], SZ_SBULLET)))

    box(x=462, y=845, w=258, h=150, valign=0, name="EvalB", paras=(
        [T("B. Convergent & discriminant validity", SZ_STITLE, NAVY, 1, 0.05)]
        + bullets(["Multitrait correlation pattern", "BH-FDR control"],
                  SZ_SBULLET)))

    box(x=772, y=845, w=258, h=150, valign=0, name="EvalC", paras=(
        [T("C. Incremental validity", SZ_STITLE, NAVY, 1, 0.05)]
        + bullets(["Hierarchical ΔR²", "ROC / AUC comparison",
                   "PHQ-8 and SWLS outcomes"], SZ_SBULLET)))

    box(x=1078, y=845, w=268, h=150, valign=0, name="EvalD", paras=(
        [T("D. Theme profiles", SZ_STITLE, NAVY, 1, 0.05)]
        + bullets(["Theme prevalence", "χ² by employment status",
                   "ANOVA on adjustment outcomes"], SZ_SBULLET)))

    # double-headed arrows between the evaluation sub-boxes
    ln(x1=430, y1=915, x2=462, y2=915, color=BLK, lw=0.015,
       begin_arrow=4, end_arrow=4, arrow_size=1, name="d1")
    ln(x1=720, y1=915, x2=772, y2=915, color=BLK, lw=0.015,
       begin_arrow=4, end_arrow=4, arrow_size=1, name="d2")
    ln(x1=1030, y1=915, x2=1078, y2=915, color=BLK, lw=0.015,
       begin_arrow=4, end_arrow=4, arrow_size=1, name="d3")

    # ---- left stage labels ----------------------------------------------
    lab(x=14, y=40, w=178, h=44, name="lbl1",
        paras=[T("1. Sample", SZ_ROWLBL, BLUE, 0)])
    lab(x=14, y=214, w=178, h=74, name="lbl2",
        paras=[T("2. Data", SZ_ROWLBL, BLUE, 0),
               T("collection", SZ_ROWLBL, BLUE, 0)])
    lab(x=14, y=432, w=184, h=74, name="lbl3",
        paras=[T("3. Narrative", SZ_ROWLBL, BLUE, 0),
               T("preprocessing", SZ_ROWLBL, BLUE, 0)])
    lab(x=14, y=574, w=178, h=74, name="lbl4",
        paras=[T("4. Narrative", SZ_ROWLBL, BLUE, 0),
               T("analysis", SZ_ROWLBL, BLUE, 0)])
    lab(x=14, y=806, w=184, h=120, name="lbl5",
        paras=[T("5. Psychometric", SZ_ROWLBL, BLUE, 0),
               T("and substantive", SZ_ROWLBL, BLUE, 0),
               T("evaluation", SZ_ROWLBL, BLUE, 0)])

    # ---- bottom caption --------------------------------------------------
    lab(x=196, y=1032, w=1046, h=66, name="Caption", paras=[
        T("Closed-ended scale scores served as validation criteria; inferential "
          "tests were two-tailed with Benjamini–Hochberg false-discovery-rate "
          "control where applicable.", SZ_CAPTION, CAP, 1)])

    return S
