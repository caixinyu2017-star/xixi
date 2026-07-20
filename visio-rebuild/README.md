# Research-methodology flowchart — native Visio rebuild

A faithful, **natively editable** Microsoft Visio rebuild of the reference
research-methodology flowchart (cross-sectional survey → data collection →
narrative preprocessing → narrative analysis → psychometric & substantive
evaluation).

## Deliverable

| file | what it is |
|------|------------|
| **`research_methodology_flowchart.vsdx`** | the rebuild — a Visio 2013+ package of **native, editable shapes** (rectangles, connectors, text runs). Nothing is a flattened image. |
| `preview.png` | a raster preview of the diagram (for quick viewing / comparison). |

Open the `.vsdx` in Microsoft Visio; every box, arrow and text run can be
selected, moved, recoloured and re-typed.

## Design choices (per request)

- **Native shapes, not an embedded picture.** Each element is a real Visio
  `Shape` with geometry, fill/line formatting and a `Character` section.
- **Font: Microsoft YaHei, bold** (微软雅黑加粗) on every text run.
- **Larger type** than the source, kept proportionally close (labels ~17 pt,
  titles ~13.5–15 pt, body ~11.5 pt).
- Layout, colours, the dashed validation-criteria connector and the
  double-headed ↔ arrows between the four evaluation boxes mirror the original.

## How it is built

Everything is generated from one source of truth so the preview always
matches the `.vsdx`:

```
scene.py          # the diagram as data: BOXES + CONNS (image-pixel coords)
build_vsdx.py     # emits research_methodology_flowchart.vsdx from scene.py
make_preview.py   # emits preview.html from scene.py (screenshot -> preview.png)
assets/           # authentic Visio-authored document.xml + windows.xml
                  #   (DocumentSettings / StyleSheets / DocumentSheet / FaceNames,
                  #    with a Microsoft YaHei FaceName added) — reused verbatim so
                  #    the package matches what Visio itself writes.
```

Regenerate:

```bash
python3 build_vsdx.py        # -> research_methodology_flowchart.vsdx
python3 make_preview.py      # -> preview.html
# optional raster preview (headless Chromium):
chromium --headless --force-device-scale-factor=2 \
  --window-size=1400,1040 --screenshot=preview.png \
  "file://$PWD/preview.html"
```

To tweak the diagram, edit `scene.py` (text, coordinates, colours, connectors)
and re-run `build_vsdx.py`.

## Validation

- Package passes ZIP integrity and XML well-formedness on every part.
- Re-parsed with the `vsdx` reader library: 1 page, 39 native shapes, text
  round-trips correctly.
- Document-level parts (StyleSheets, DocumentSheet, FaceNames) are Visio's own,
  which maximises real-Visio openability.
