# Visio rebuild — career-narrative study methodology flowchart

Native, fully editable **Visio** reconstruction of the reference methodology
diagram (5-stage research pipeline: Sample → Data collection → Narrative
preprocessing → Narrative analysis → Psychometric & substantive evaluation).

## Deliverable

- **`method_flowchart.vsdx`** — the Visio drawing. Open and edit it directly in
  Microsoft Visio.

### Key properties

- **Native editable shapes**, not an embedded picture. Every box, arrow, label
  and connector is a real Visio `Shape` with its own geometry and text runs, so
  you can move, restyle, retype or recolour anything.
- **No raster/image parts** in the package (verified — the `.vsdx` contains only
  XML parts, zero `media/` entries).
- **Fonts:** all text uses **Microsoft YaHei (微软雅黑), bold**, at deliberately
  large point sizes, kept close to the reference (row labels 15.5 pt, box titles
  13–16.5 pt, bullets 11.5–12.5 pt).
- Single custom landscape page (14.56 × 11.2 in) laid out to mirror the
  reference proportions.

## How it is built

Layout and rendering share one source of truth so what you preview is exactly
what ships:

| file | role |
| --- | --- |
| `layout.py` | the single layout spec (all shapes, positions, text, colours, sizes) in design-pixel space |
| `build_vsdx.py` | serialises the spec into the `.vsdx` OPC package (this is the deliverable generator) |
| `preview.py` | renders `preview.png` from the **same** spec for visual QA |
| `preview.png` | raster preview of the diagram |

Regenerate:

```bash
python3 build_vsdx.py     # -> method_flowchart.vsdx
python3 preview.py        # -> preview.png  (needs matplotlib; QA only)
```

Editing the diagram programmatically: change coordinates/text in `layout.py`
and re-run both commands.

## Notes

- The preview uses a substitute sans font, so in `preview.png` the round bullet
  glyph is drawn as `-` and text is regular weight; the actual `.vsdx` uses
  Microsoft YaHei bold with proper `•` bullets.
- The reference image was not committed; the layout was transcribed from it.
