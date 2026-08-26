# -*- coding: utf-8 -*-
"""The bibliography, in APA 7 style, as Behavioral Sciences requires.

Behavioral Sciences uses author-date citations in the text and an
alphabetically ordered reference list, unlike the numbered style of the
engineering and sustainability titles. The rendering helpers below produce
both from a single structured entry, so an in-text citation and its reference
can never disagree.

Every entry was verified during preparation to the standard that its title,
journal, year and — critically — its author list were seen in a retrieved
record rather than recalled. Fields that could not be confirmed are omitted
rather than invented.
"""
from __future__ import annotations

# Each entry:
#   kind      article | book | chapter | report
#   authors   list of (surname, initials); initials None for an institution
#   year      int or str
#   title     already in APA sentence case
REFS: dict[str, dict] = {}


# ---------------------------------------------------------------------------
# rendering helpers
# ---------------------------------------------------------------------------
def sentence_case(t):
    return str(t).rstrip(". ")


def _name(a):
    surname, initials = a
    return surname if not initials else "%s, %s" % (surname, initials)


def author_list(ref):
    """The reference-list form: 'Surname, A. B., & Surname, C. D.'"""
    au = ref["authors"]
    if len(au) == 1:
        return _name(au[0])
    if len(au) == 2:
        return "%s, & %s" % (_name(au[0]), _name(au[1]))
    return "%s, & %s" % (", ".join(_name(a) for a in au[:-1]), _name(au[-1]))


def _label(ref, narrative=False):
    """The in-text form: 'Surname', 'A & B', or 'A et al.'

    Where two references of three or more authors would shorten to the same
    form, APA requires as many surnames as it takes to tell them apart, so the
    label grows to 'A, B, et al.' for both.
    """
    au = ref["authors"]
    joiner = " and " if narrative else " & "
    if len(au) == 1:
        return au[0][0]
    if len(au) == 2:
        return au[0][0] + joiner + au[1][0]
    n = max(1, _ambiguity().get(au[0][0], 1))
    if n >= len(au):
        head = ", ".join(a[0] for a in au[:-1])
        return head + "," + joiner + au[-1][0]
    if n == 1:
        return au[0][0] + " et al."
    return ", ".join(a[0] for a in au[:n]) + ", et al."


_AMBIG = None


def _ambiguity():
    """How many surnames each first author needs before the labels differ."""
    global _AMBIG
    if _AMBIG is None:
        by_first = {}
        for r in REFS.values():
            au = r["authors"]
            if len(au) >= 3:
                by_first.setdefault(au[0][0], set()).add(
                    tuple(a[0] for a in au))
        _AMBIG = {}
        for first, sets in by_first.items():
            n = 1
            while len(sets) > 1 and n < max(len(t) for t in sets):
                if len({t[:n] for t in sets}) == len(sets):
                    break
                n += 1
            _AMBIG[first] = n
    return _AMBIG


def render_citation(keys):
    """Render one citation marker.

    A key suffixed with ``_n`` is narrative: Author (Year). Otherwise the
    whole group is parenthetical and ordered alphabetically, as APA requires:
    (Author, Year; Other, Year). Works sharing an in-text label are collapsed
    onto that label with their years in order: (Author, Year, Year).
    """
    if len(keys) == 1 and keys[0].endswith("_n"):
        k = keys[0][:-2]
        r = REFS[k]
        return "%s (%s)" % (_label(r, narrative=True), r["year"])
    plain = [k[:-2] if k.endswith("_n") else k for k in keys]
    groups = {}
    for k in plain:
        r = REFS[k]
        groups.setdefault(_label(r), set()).add(str(r["year"]))
    parts = []
    for label, years in groups.items():
        yrs = sorted(years)
        parts.append(((label.lower(), yrs[0]),
                      "%s, %s" % (label, ", ".join(yrs))))
    parts.sort()
    return "(" + "; ".join(p[1] for p in parts) + ")"


def _sort_key(key):
    r = REFS[key]
    return (r["authors"][0][0].lower(),
            " ".join(a[0].lower() for a in r["authors"][1:]),
            str(r["year"]))


def alphabetical(keys):
    """The cited keys, ordered as the reference list requires."""
    seen, out = set(), []
    for k in keys:
        k = k[:-2] if k.endswith("_n") else k
        if k not in seen:
            seen.add(k)
            out.append(k)
    return sorted(out, key=_sort_key)


def add(key, **kw):
    assert key not in REFS, "duplicate reference key %s" % key
    kw.setdefault("kind", "article")
    REFS[key] = kw


# ---------------------------------------------------------------------------
# entries are added by the bibliography module
# ---------------------------------------------------------------------------
try:
    import bibliography  # noqa: F401  (populates REFS through add())
except ImportError:
    pass
