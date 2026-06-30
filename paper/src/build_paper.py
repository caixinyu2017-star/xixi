"""Assemble the full Biomimetics-style paper into a .docx."""
import docbuild, content_front, content_algo, content_results

OUT="/tmp/claude-0/-home-user-xixi/013086be-932a-56cd-b187-9ec3125f6bc6/scratchpad/MSSBOA_Biomimetics.docx"

P=docbuild.Paper()
content_front.front_matter(P)
content_front.abstract(P)
content_front.introduction(P)
e2=content_algo.section2(P)
content_algo.section3(P,e2)
content_results.section4(P)
content_results.section5(P)
content_results.section6(P)
content_results.backmatter(P)
content_results.appendix(P)
P.start_section(landscape=False)   # back to portrait for references
P.references()
P.save(OUT)

print("SAVED:",OUT)
print(f"equations={P.eqno}  figures={P.figno}  tables={P.tblno}  references={len(P.refs)}")
