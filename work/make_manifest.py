# -*- coding: utf-8 -*-
import json

STYLE = ("A flat vector infographic diagram, academic journal figure style, clean white background, "
         "thin uniform stroke weight, restrained academic palette of {pal}, generous white space, "
         "crisp geometric shapes, sans-serif labels.")
CONSTR = ("All text in English, spelled exactly as quoted, sans-serif, legible at small size. "
          "No photorealism, no 3D bevel, no drop shadows, no gradients on text, no lens flare, "
          "no stock-photo people, no watermark, no signature, no extra decorative elements, "
          "no invented labels beyond those listed, no Chinese characters.")

PAL1 = "graphite #333B44, steel blue #3D6E9E and amber #E0A33E"
PAL2 = "ink #2C3E50, sage #7A9E7E and clay #B5651D"
PAL3 = "deep navy #1F3B63, slate gray #6B7A8F and warm orange #C9622E"
PAL4 = "teal #2A7F7F, sand #D9C08C and brick #A8423F"
PAL5 = "graphite #333B44, steel blue #3D6E9E and brick #A8423F"

items = []
def add(fn, pal, layout, elements, relations, size="1536x1024"):
    items.append({
        "filename": fn,
        "size": size,
        "quality": "high",
        "prompt": " ".join([STYLE.format(pal=pal), "Layout:", layout, "Elements:", elements,
                            "Relations:", relations, CONSTR])
    })

# ===================== PAPER 1 =====================
add("p1_f1_roadmap.png", PAL1,
    "a left-to-right technical roadmap with four sequential vertical stage columns of equal width, "
    "each column having a header bar and three stacked sub-boxes beneath it, all aligned on a strict grid.",
    'column 1 header "1 Problem Diagnosis" with sub-boxes "Low Sampling Coverage", "Slow Evidence Retrieval", '
    '"Procedural Defects"; column 2 header "2 System Design" with sub-boxes "Data Layer", "Model Layer", '
    '"Application Layer"; column 3 header "3 Domain Adaptation" with sub-boxes "Adaptive Key-frame Sampling", '
    '"LoRA Fine-tuning", "Rule Engine"; column 4 header "4 Validation and Governance" with sub-boxes '
    '"Ablation Experiment", "Cost-sensitive Threshold", "Human-in-the-loop Review".',
    "one thick horizontal arrow running along the top from column 1 through column 2 and column 3 to column 4; "
    "a curved dashed feedback arrow running along the bottom from column 4 back to column 3 labeled "
    '"Iterative Refinement".')

add("p1_f2_architecture.png", PAL1,
    "top-down layered architecture, three horizontal bands stacked vertically, each band a wide rounded "
    "rectangle containing four equal small boxes in a row, a narrow vertical side bar on the right spanning all bands.",
    'top band labeled "Application Layer" containing "Legal Supervision Console", "Case Handling Console", '
    '"Management Dashboard", "Open API"; middle band labeled "Model Layer" containing "Qwen Omni Inference Engine", '
    '"LoRA Domain Adapter", "Compliance Rule Engine", "Model Service Gateway"; bottom band labeled "Data Layer" '
    'containing "Body-cam Video Ingest", "Case and Officer Records", "Feature and Vector Store", "Hot-Cold Storage"; '
    'the right vertical side bar labeled "Security and Privacy Governance".',
    "two vertical double-headed arrows connecting bottom band to middle band and middle band to top band; "
    "short horizontal arrows from the right side bar pointing left into each of the three bands.")

add("p1_f3_mechanism.png", PAL1,
    "left-to-right mechanism diagram on one horizontal axis, three input rows on the left merging into a single "
    "center module, then continuing to two outputs on the right, with one time-axis strip drawn under the center module.",
    'three left input boxes stacked vertically labeled "Video Frames", "Audio Stream", "Document Text"; three small '
    'encoder boxes to their right labeled "SigLIP2 Visual Encoder", "AuT Audio Encoder", "Text Tokenizer"; one center '
    'large rounded rectangle labeled "Unified Token Sequence"; a horizontal ruler strip beneath it labeled '
    '"TMRoPE Absolute Time Axis"; to the right a rounded rectangle labeled "Thinker MoE Reasoning"; two right output '
    'boxes labeled "Procedure Compliance Verdict" and "Evidence Timeline".',
    "one solid arrow from each input box into its own encoder box; one solid arrow from each encoder box converging "
    'into "Unified Token Sequence"; a dashed vertical arrow from the "TMRoPE Absolute Time Axis" strip pointing up '
    'into "Unified Token Sequence"; one solid arrow from "Unified Token Sequence" to "Thinker MoE Reasoning"; two '
    'solid arrows from "Thinker MoE Reasoning" to the two right output boxes.')

add("p1_f4_statemachine.png", PAL1,
    "a horizontal left-to-right process chain of seven rounded rectangles evenly spaced in a single row, with a "
    "small diamond gate placed directly above each of the first six rectangles, and one wide banner bar under the whole chain.",
    'the seven chain boxes labeled in order "Enter Premises", "Show Credentials", "State Identity", "Notify Rights", '
    '"On-site Inspection", "Collect Evidence", "Serve Documents"; each diamond gate labeled "Check"; the banner bar '
    'under the chain labeled "Temporal Order Constraint".',
    "solid arrows connecting the seven chain boxes strictly left to right in order; a short dashed vertical arrow "
    "from each chain box up to its own diamond gate and a dashed arrow back down; the banner bar spans and touches "
    "the bottom edge of all seven boxes with small tick marks.")

add("p1_f5_governance.png", PAL1,
    "a closed clockwise feedback loop of six rounded rectangles arranged around an oval track, with one large dashed "
    "boundary rectangle enclosing the left half of the loop.",
    'the six loop boxes labeled clockwise starting at top-left "Body-cam Video Capture", "De-identification and '
    'Minimization", "Private Model Inference", "Advisory Risk Flags", "Human Reviewer Decision", "Appeal and '
    'Correction"; the dashed boundary rectangle labeled "Personal Information Protection Boundary"; one small side '
    'box outside the loop on the right labeled "Training Feedback".',
    "solid clockwise arrows connecting the six loop boxes in the listed order and closing the loop; a dashed arrow "
    'from "Appeal and Correction" to the side box "Training Feedback"; a dashed arrow from "Training Feedback" back '
    'into "Private Model Inference".')

# ===================== PAPER 2 =====================
add("p2_f1_framework.png", PAL2,
    "top-down research framework in four horizontal tiers of decreasing width, centered, each tier a rounded "
    "rectangle band containing three small boxes in a row.",
    'tier 1 band labeled "Theoretical Lens" containing "Multi-layer Principal-Agent", "Collaborative Governance", '
    '"Penetrating Regulation"; tier 2 band labeled "Problem Diagnosis" containing "Hierarchy Attenuation", '
    '"Data Silos", "Weak Accountability"; tier 3 band labeled "Four-Dimensional Penetration" containing '
    '"Institution and Data", "Process and Responsibility", "Workforce"; tier 4 band labeled "Outcome Evaluation" '
    'containing "Supervision Efficacy Index", "Cost-Benefit Balance", "Staged Rollout".',
    "one solid downward arrow from the center of each tier to the center of the tier below; one curved dashed arrow "
    'running along the right side from tier 4 back up to tier 2 labeled "Evidence Feedback".')

add("p2_f2_agency.png", PAL2,
    "top-down layered chain of four horizontal bars of equal width stacked vertically, plus a vertical decay bar "
    "drawn on the right side spanning all four levels, and a small legend-free triangle wedge next to it.",
    'the four bars labeled from top to bottom "National Bureau", "Provincial Bureau", "Municipal Bureau", '
    '"County Bureau"; the vertical bar on the right labeled "Supervision Intensity"; a downward-narrowing triangle '
    'wedge beside the vertical bar labeled "Attenuation"; two small side ellipses on the left labeled '
    '"Information Asymmetry" and "Dual Role Conflict".',
    "a solid downward arrow from each bar to the bar below labeled in turn \"delegate\"; a dashed upward arrow on "
    'the far left from "County Bureau" to "National Bureau" labeled "report"; a dashed arrow from each of the two '
    "left ellipses pointing onto the middle of the downward delegate arrows, indicating they weaken those arrows.")

add("p2_f3_fourdim.png", PAL2,
    "radial hub-and-spoke, one central circle with four rounded rectangles placed at up, right, down and left "
    "positions around it, and one outer dashed ring passing through all four.",
    'the central circle labeled "Penetrating Supervision"; the top box labeled "Institutional Penetration" with '
    'sub-caption "unified standards"; the right box labeled "Data Penetration" with sub-caption "one collection '
    'many uses"; the bottom box labeled "Process Penetration" with sub-caption "embedded checkpoints"; the left box '
    'labeled "Responsibility Penetration" with sub-caption "rigid accountability".',
    "a solid double-headed arrow between the central circle and each of the four boxes; the outer dashed ring "
    "connects the four boxes clockwise with small arrowheads showing a continuous cycle.")

add("p2_f4_rollout.png", PAL2,
    "a horizontal timeline roadmap, one long arrow running left to right across the middle, three milestone "
    "markers on it, each milestone having a box above the line and a box below the line.",
    'the long arrow labeled "Implementation Timeline"; milestone 1 marker labeled "Phase I 0-6 months" with an '
    'upper box "Standards and Responsibility Lists" and a lower box "Pilot County Bureaus"; milestone 2 marker '
    'labeled "Phase II 6-18 months" with an upper box "Data Middle Platform" and a lower box "Risk Warning Models"; '
    'milestone 3 marker labeled "Phase III 18-36 months" with an upper box "Full Rollout and Audit" and a lower box '
    '"Efficacy Index Assessment".',
    "the single long horizontal arrow passes through all three milestone markers pointing right; a short vertical "
    "connector from each milestone marker up to its upper box and down to its lower box.")

add("p2_f5_dataplatform.png", PAL2,
    "top-down layered data platform, five horizontal bands stacked vertically, the middle band being the widest, "
    "with a narrow vertical bar on the left spanning all bands.",
    'top band labeled "Supervision Applications" containing "Risk Alert", "Clue Dispatch", "Rectification Tracking"; '
    'second band labeled "Analytical Models" containing "Bid Collusion Model", "Expense Anomaly Model", '
    '"Approval Anomaly Model"; middle band labeled "Unified Supervision Data Platform"; fourth band labeled '
    '"Data Standards and Access Control"; bottom band labeled "Business Systems" containing "Tobacco Leaf", '
    '"Marketing", "Procurement", "Finance", "Monopoly Enforcement"; the left vertical bar labeled '
    '"Collect Once, Reuse Many Times".',
    "solid upward arrows from the bottom band into the fourth band, from the fourth band into the middle band, from "
    "the middle band into the second band, and from the second band into the top band; a dashed arrow from the left "
    "vertical bar pointing right into the middle band.")

# ===================== PAPER 3 =====================
add("p3_f1_mapping.png", PAL3,
    "two vertical columns of four boxes each, left column and right column, connected across the gap, with a "
    "vertical dashed divider line down the middle.",
    'left column header "Refined Management Principles" with boxes "Precise Objects", "Standardized Process", '
    '"Clear Responsibility", "Scientific Evaluation"; right column header "Contractor Safety Mechanisms" with boxes '
    '"Classified and Graded Control", "Closed-loop Whole-process Supervision", "Contract and Economic Levers", '
    '"Performance Rating and Incentive".',
    "one solid horizontal arrow from each left box to the right box directly opposite it; no crossing arrows.")

add("p3_f2_bowtie.png", PAL3,
    "a symmetric bow-tie diagram, a single hazard box in the exact center, three cause boxes fanning out to the "
    "left, three consequence boxes fanning out to the right, with two vertical dashed barrier lines, one between "
    "causes and center and one between center and consequences.",
    'the center box labeled "Loss of Control in Contractor Operation"; the three left cause boxes labeled '
    '"Unqualified Personnel", "Unpermitted Hot Work", "Temporary Electricity Violation"; the three right consequence '
    'boxes labeled "Injury", "Fire and Explosion", "Business Interruption"; the left dashed line labeled '
    '"Preventive Barriers"; the right dashed line labeled "Mitigative Barriers".',
    "one solid arrow from each left cause box to the center box, each crossing the left dashed barrier line; one "
    "solid arrow from the center box to each right consequence box, each crossing the right dashed barrier line.",
    "1536x1024")

add("p3_f3_matrix.png", PAL3,
    "a three by three grid matrix occupying the center of the canvas, with a labeled vertical axis on the left and "
    "a labeled horizontal axis at the bottom, and a short caption strip on the right.",
    'the vertical axis labeled "Operation Risk Level" with tick labels from bottom to top "Low", "Medium", "High"; '
    'the horizontal axis labeled "Contractor Safety Capability" with tick labels from left to right "Weak", '
    '"Fair", "Strong"; the nine grid cells labeled respectively "C3", "C2", "B3", "C2", "B2", "B1", "A1", "A2", "B1"; '
    'the right caption strip listing three lines "A: Full-time Supervision", "B: Enhanced Inspection", '
    '"C: Routine Management".',
    "no arrows; the grid cells are shaded in three intensity steps, darkest at the top-left cell and lightest at "
    "the bottom-right cell.",
    "1024x1024")

add("p3_f4_closedloop.png", PAL3,
    "a closed clockwise loop of six rounded rectangles arranged around a wide oval track, with one small center circle.",
    'the six loop boxes labeled clockwise starting from the top "Qualification Admission", "Contract and Safety '
    'Agreement", "Pre-task Briefing and Permit", "On-site Supervision", "Acceptance and Performance Rating", '
    '"Analysis and Improvement"; the center circle labeled "Closed-loop Control".',
    "solid clockwise arrows connecting the six boxes in the listed order and closing back to the first; six thin "
    "dashed lines connecting each loop box inward to the center circle.",
    "1024x1024")

add("p3_f5_digital.png", PAL3,
    "top-down layered architecture, four horizontal bands stacked vertically, each band containing three or four "
    "equal small boxes in a row.",
    'top band labeled "Decision Support" containing "Risk Heat Map", "Rating Ranking", "Resource Allocation"; '
    'second band labeled "Supervision Applications" containing "Electronic Work Permit", "Mobile Hazard Reporting", '
    '"Video Behaviour Alert", "Training Records"; third band labeled "Contractor Master Data" containing '
    '"Qualification File", "Personnel File", "Violation Ledger"; bottom band labeled "Sensing Layer" containing '
    '"Positioning Tag", "Camera", "Gas Detector", "Mobile Terminal".',
    "one solid upward arrow from each band to the band directly above it, three arrows in total, drawn at the center.")

# ===================== PAPER 4 =====================
add("p4_f1_externality.png", PAL4,
    "left-to-right mechanism diagram on one horizontal axis with three main nodes, one moderator ellipse above the "
    "axis, one moderator ellipse below the axis, and a curved feedback arrow under everything.",
    'leftmost rounded rectangle labeled "Unmanaged Smoking Behaviour"; center rounded rectangle labeled '
    '"Negative Externality: Secondhand Smoke and Litter"; rightmost rounded rectangle labeled "Public Environment '
    'Quality Loss"; the upper ellipse labeled "Facility Supply and Siting"; the lower ellipse labeled '
    '"Behavioural Nudge Design".',
    'a solid arrow from "Unmanaged Smoking Behaviour" to "Negative Externality: Secondhand Smoke and Litter" '
    'labeled "generates"; a solid arrow from that center node to "Public Environment Quality Loss" labeled '
    '"causes"; a dashed arrow from the upper ellipse pointing down onto the middle of the first solid arrow, '
    "indicating it weakens that path; a dashed arrow from the lower ellipse pointing up onto the middle of the same "
    "first solid arrow; a curved dashed arrow looping from the rightmost node back leftward to the leftmost node "
    'labeled "social norm feedback".')

add("p4_f2_boundary.png", PAL4,
    "a large rounded rectangle occupying most of the canvas divided by a horizontal dashed line into an upper "
    "region and a lower region, with three small boxes in the upper region and three small boxes in the lower region.",
    'the whole rectangle titled "Role Boundary under Tobacco Control Priority"; the upper region titled "Permitted"; '
    'its three boxes labeled "Facility Funding without Naming", "Litter Cleaning Support", "Non-brand Civility '
    'Reminders"; the lower region titled "Prohibited"; its three boxes labeled "Brand Marks and Advertising", '
    '"Sites near Minors", "Leading Health Policy Making"; a vertical strip on the far right labeled '
    '"Government and Venue Led".',
    "no arrows between the upper and lower boxes; a single horizontal dashed separator line runs across the middle "
    "of the rectangle; three short arrows point from the right vertical strip into the upper region only.")

add("p4_f3_polycentric.png", PAL4,
    "radial hub-and-spoke, one central hexagon with four rounded rectangles at the four corners of the canvas, and "
    "a dashed ring connecting the four corner boxes.",
    'the central hexagon labeled "Coordination Platform"; the top-left box labeled "Government Departments" with '
    'sub-caption "planning and rules"; the top-right box labeled "Venue Operators" with sub-caption "daily '
    'management"; the bottom-left box labeled "Tobacco Commercial Enterprise" with sub-caption "bounded support"; '
    'the bottom-right box labeled "Public and Social Organizations" with sub-caption "supervision and self-discipline".',
    "a solid double-headed arrow between the central hexagon and each of the four corner boxes; a dashed ring "
    "passing through all four corner boxes with small arrowheads indicating a continuous cycle.",
    "1024x1024")

add("p4_f4_nudge.png", PAL4,
    "a single top-down plan view of one designated smoking point drawn in the center, with five callout labels "
    "placed around it and connected by thin leader lines.",
    'the central object is a rounded open-sided shelter labeled "Designated Smoking Point"; callout 1 labeled '
    '"High-visibility Signage"; callout 2 labeled "Butt Bin within Two Steps"; callout 3 labeled "Windward '
    'Separation Distance"; callout 4 labeled "Ground Guiding Marks"; callout 5 labeled "Away from Entrances and '
    'Waiting Areas".',
    "one thin straight leader line from each callout label to the specific part of the shelter it refers to; no "
    "arrowheads on leader lines.")

add("p4_f5_pdca.png", PAL4,
    "a closed clockwise loop of four large rounded rectangles arranged in a square, with one small rectangle "
    "attached to the outside of each loop box.",
    'the four loop boxes labeled clockwise from the top-left "Plan: Siting Optimization", "Do: Facility and Nudge '
    'Deployment", "Check: Exposure and Litter Monitoring", "Act: Standard Revision"; the small attached boxes '
    'labeled respectively "Coverage Model", "Venue Agreement", "Difference-in-Differences Evaluation", '
    '"Guideline Update".',
    "solid clockwise arrows connecting the four loop boxes and closing the loop; one short dashed line from each "
    "loop box out to its own attached small box.",
    "1024x1024")

# ===================== PAPER 5 =====================
add("p5_f1_roadmap.png", PAL5,
    "a left-to-right technical roadmap with five sequential vertical stage columns of equal width, each column "
    "having a header bar and two stacked sub-boxes beneath it.",
    'column 1 header "Data Acquisition" with sub-boxes "DII 2010-2024", "Deduplication and Winsorization"; column 2 '
    'header "Label Construction" with sub-boxes "Entropy Weighting", "Natural Breaks Grading"; column 3 header '
    '"Model Building" with sub-boxes "Random Forest", "DBSCAN Tree Pruning"; column 4 header "Validity Testing" '
    'with sub-boxes "Leave-label-features-out", "Nested Cross Validation"; column 5 header "Application" with '
    'sub-boxes "Barrier Early Warning", "Freedom to Operate Screening".',
    "one thick horizontal arrow running along the top from column 1 through to column 5; a curved dashed feedback "
    'arrow along the bottom from column 4 back to column 2 labeled "Label Revision".')

add("p5_f2_model.png", PAL5,
    "left-to-right model structure diagram with four vertical stages, the second stage showing a fan of many small "
    "triangle icons, the third stage showing three grouped clusters of triangles, the fourth stage showing three "
    "single triangles.",
    'stage 1 labeled "Bootstrap Samples"; stage 2 labeled "Full Forest of Base Trees"; stage 3 labeled '
    '"Kappa Distance Clustering by DBSCAN"; stage 4 labeled "Pruned Sub-forest"; a small box at the far right '
    'labeled "Majority Vote Output"; a small discarded pile below stage 3 labeled "Noise Trees Removed".',
    "solid arrows from stage 1 to stage 2, stage 2 to stage 3, stage 3 to stage 4, and stage 4 to the far right "
    "box; one dashed arrow from stage 3 down to the discarded pile.")

add("p5_f3_circularity.png", PAL5,
    "the canvas split into a left panel and a right panel by a vertical solid divider, the left panel showing a "
    "circular loop of three boxes, the right panel showing a straight three-step chain.",
    'left panel titled "Circularity Problem"; its three loop boxes labeled "Four Indicators", "Entropy Weighted '
    'Label", "Model Features"; right panel titled "External Validity Design"; its three chain boxes labeled '
    '"Remove Label Indicators from Features", "Independent Value Proxies", "Expert Annotated Holdout".',
    "in the left panel, solid arrows form a closed circular loop through the three boxes returning to the first, "
    'with a small warning marker on the loop labeled "tautology"; in the right panel, solid arrows connect the '
    "three chain boxes strictly left to right.")

add("p5_f4_layering.png", PAL5,
    "a pyramid divided into four horizontal tiers, placed on the left half of the canvas, with four labeled "
    "callout boxes on the right half aligned to each tier.",
    'the pyramid tiers from top to bottom labeled "Frontier Cluster", "Core Cluster", "Transition Cluster", '
    '"Peripheral Cluster"; the four right callout boxes labeled respectively "Substrate Formulation", '
    '"Resistive Heating Element", "Extraction Process", "Housing and Assembly"; a vertical arrow along the far '
    'left of the pyramid pointing upward labeled "Value Density".',
    "one thin horizontal leader line from each pyramid tier to its own callout box on the right; no arrowheads on "
    "leader lines.")

add("p5_f5_application.png", PAL5,
    "a left-to-right pathway diagram, one shared source box on the left that splits at a solid circular junction "
    "node into three clearly separated parallel horizontal tracks, all three recombining into one outcome box on the right.",
    'the left source box labeled "High-value Patent Identification Model"; track I labeled "Pathway I" with one box '
    '"Overseas Barrier Early Warning"; track II labeled "Pathway II" with one box "Freedom to Operate Screening"; '
    'track III labeled "Pathway III" with one box "Illicit Product Feature Tracing"; the right outcome box labeled '
    '"Monopoly Administration Decision Support".',
    "one solid arrow from the source box to the circular junction node; one solid arrow from the junction node into "
    "each of the three track boxes; one solid arrow from each track box into the right outcome box.")

with open("/home/user/xixi/work/figures/prompts.json", "w", encoding="utf-8") as f:
    json.dump({"items": items}, f, ensure_ascii=False, indent=1)
print(len(items), "items written")
