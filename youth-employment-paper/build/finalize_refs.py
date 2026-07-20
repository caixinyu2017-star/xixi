# -*- coding: utf-8 -*-
"""Assemble refs.py from a hand-curated mapping of citation-key -> list of real ref dicts.
Numbers references by first appearance across the manuscript (MDPI style)."""
import re
import content as C


def build(KEY_REFS):
    # order of key first-appearance
    order = []
    for b in C.BLOCKS:
        if b[0] in ('p', 'hyp'):
            text = b[1] if b[0] == 'p' else b[2]
            for k in re.findall(r'\[\[([a-z0-9\-]+)\]\]', text):
                if k not in order:
                    order.append(k)
    # sanity: every key must have refs
    missing = [k for k in order if k not in KEY_REFS or not KEY_REFS[k]]
    if missing:
        raise SystemExit("Missing refs for keys: %s" % missing)

    num_by_doi = {}
    references = []
    CIT = {}

    def keyof(ref):
        return (ref.get('doi') or ref.get('title', '')).lower().strip()

    for k in order:
        nums = []
        for ref in KEY_REFS[k]:
            dk = keyof(ref)
            if dk not in num_by_doi:
                num = len(references) + 1
                num_by_doi[dk] = num
                references.append(ref)
            nums.append(num_by_doi[dk])
        CIT[k] = nums
    return CIT, references


def write_refs_py(CIT, references, path):
    lines = ["# -*- coding: utf-8 -*-", '"""Auto-generated real references (MDPI format)."""', ""]
    lines.append("CIT = {")
    for k, v in CIT.items():
        lines.append(f"    {k!r}: {v},")
    lines.append("}")
    lines.append("")
    lines.append("REFERENCES = [")
    for r in references:
        d = {kk: r.get(kk, '') for kk in ('authors', 'title', 'journal_abbrev',
                                          'journal_full', 'year', 'volume', 'issue', 'pages', 'doi')}
        lines.append("    " + repr(d) + ",")
    lines.append("]")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("Wrote %s with %d references, %d citation keys" % (path, len(references), len(CIT)))


if __name__ == "__main__":
    import ref_pool  # provides KEY_REFS
    CIT, references = build(ref_pool.KEY_REFS)
    write_refs_py(CIT, references,
                  "/tmp/claude-0/-home-user-xixi/7cc0eeef-b56d-5a7e-a38b-98d920654675/scratchpad/refs.py")
