"""Academic-English pass over the submitted text.

The manuscript narrates completed work in the present tense ("MSSBOA is
compared with...", "three variants are constructed", "the Friedman test is
performed").  English scientific convention is the past tense for what was
done and the present tense for what a table, figure or equation shows, for
symbol definitions and for interpretation.  This module makes that
distinction consistently.

Only whole clauses whose subject is an action performed by the authors are
converted.  Sentences of the form "Table 6 reports...", "where x denotes...",
"the greedy selection guarantees..." are deliberately left in the present.
"""
import re

# ---------------------------------------------------------------- methods
# (pattern, replacement) applied to body text, longest first
METHODS_PAST = [
    ('is comprehensively examined', 'was comprehensively examined'),
    ('is compared with the basic SBOA', 'was compared with the basic SBOA'),
    ('MSSBOA is compared with', 'MSSBOA was compared with'),
    ('MSSBOA is applied to', 'MSSBOA was applied to'),
    ('MSSBOA is then applied to', 'MSSBOA was then applied to'),
    ('is successfully applied to', 'was successfully applied to'),
    ('A grid search is conducted', 'A grid search was conducted'),
    ('the Friedman test is performed', 'the Friedman test was performed'),
    ('the Nemenyi post-hoc test is applied', 'the Nemenyi post-hoc test was applied'),
    ('the Wilcoxon rank-sum test is conducted', 'the Wilcoxon rank-sum test was conducted'),
    ('three variants of MSSBOA are constructed', 'three variants of MSSBOA were constructed'),
    ('are independently run 30 times', 'were run 30 times independently'),
    ('is independently run 30 times', 'was run 30 times independently'),
    ('Each algorithm is independently run', 'Each algorithm was run independently'),
    ('the best value, mean value and standard deviation are recorded',
     'the best value, the mean value and the standard deviation were recorded'),
    ('the maximum number of function evaluations is used',
     'the maximum number of function evaluations was used'),
    ('the dimensions are set to', 'the dimensions were set to'),
    ('The search range is', 'The search range was'),
    ('is searched from', 'was varied from'),
    ('Palettes of', 'Palettes of'),
    ('colors are optimized', 'colours were optimized'),
    ('are considered, covering', 'were considered, covering'),
    ('are formulated as continuous optimization problems and solved by',
     'were formulated as continuous optimization problems and solved by'),
    ('a hue diversity term is introduced', 'a hue-diversity term is introduced'),
    ('All experiments were conducted on a workstation',
     'All experiments were carried out on a workstation'),
]

# ------------------------------------------------------- register and style
STYLE = [
    # American -> British spelling, to match the rest of the revision
    ('color-harmony', 'colour-harmony'),
    ('color harmony', 'colour harmony'),
    ('Color-harmony', 'Colour-harmony'),
    ('color palette', 'colour palette'),
    ('color model', 'colour model'),
    ('color space', 'colour space'),
    ('colors', 'colours'),
    ('color design', 'colour design'),
    ('Color Harmonization', 'Color Harmonization'),      # reference title
    # wordiness and register
    ('In order to ', 'To '),
    ('a large number of ', 'many '),
    ('It is worth noting that ', 'Notably, '),
    ('can be seen that', 'shows that'),
    ('so as to better serve', 'to better serve'),
    ('and thus generates', 'and therefore generates'),
    ('Owing to their flexibility', 'Because they are flexible'),
    # hedging: an unqualified causal claim becomes a measured one
    ('which confirms that every strategy is effective',
     'which indicates that each strategy contributes'),
]

SKIP_PREFIX = ('where ', 'Table ', 'Figure ', 'Algorithm ')


def polish_paragraph(text):
    """Return the polished text, or None when nothing changes."""
    if not text or text.startswith(SKIP_PREFIX):
        return None
    out = text
    for a, b in METHODS_PAST:
        out = out.replace(a, b)
    for a, b in STYLE:
        out = out.replace(a, b)
    # "is set to X" inside a methods sentence -> "was set to X"
    out = re.sub(r'\bcriterion and set to\b', 'criterion and was set to', out)
    return out if out != text else None


def polish_document(doc, color, body_styles=('MDPI_3.1_text', 'MDPI_3.2_text_no_indent')):
    """Apply the pass to body paragraphs; returns the number of runs changed."""
    from docx_edit import COLORS
    n = 0
    for p in doc.paragraphs:
        style = p.style.name if p.style else ''
        if not any(style.startswith(s[:12]) for s in body_styles):
            continue
        for r in p.runs:
            if not r.text.strip() or r.font.strike:
                continue
            new = polish_paragraph(r.text)
            if new:
                r.text = new
                if r.font.color is None or r.font.color.type is None:
                    r.font.color.rgb = COLORS[color]
                n += 1
    return n
