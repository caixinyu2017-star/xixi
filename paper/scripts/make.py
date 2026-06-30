#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Single entry point so build_doc is one shared module instance (avoids the
__main__ double-import that splits the citation registry)."""
import build_doc
from china_refs import CHINA_REFS as CR
build_doc.CHINA_REFS.update(CR)
from prose import write_prose

if __name__ == "__main__":
    missing = build_doc.build(write_prose)
    # warn on any TEMP / unresolved china refs still present
    allrefs = dict(build_doc.REF_DB); allrefs.update(build_doc.CHINA_REFS)
    temp = [k for k in build_doc.CITE.order if str(allrefs.get(k, "")).startswith("[TEMP]")]
    if temp:
        print("TEMP refs still present (replace before shipping):", temp)
