# Working notes for this repository

## Figures

**Legends must never cover plot content.** If a legend would overlap any
series, marker, annotation or axis, place it *below* the figure (or below the
panel it belongs to) rather than inside the axes. In matplotlib:

```python
ax.legend(frameon=False, ncol=2, loc="upper center",
          bbox_to_anchor=(0.5, -0.30), borderaxespad=0.0)
```

then leave room with `fig.tight_layout(h_pad=...)`. This applies to every
figure in every paper in this repository, not only the one that prompted it.

**Schematic diagrams** (model structure, mechanism maps) use orthogonal
connectors only — horizontal and vertical segments joined at right angles, no
curved or diagonal arrows. Route connectors along dedicated lanes so that no
two ever cross and none passes through a box. Arrow labels sit clear of box
borders. Converging contributions are drawn as an explicit summation junction
(feeders → one spine → one arrow out), never as several arrows landing on the
same point.

## Manuscripts

- Every reported number is read at build time from the analysis output
  (`stats.json`, `calibrated.json`), so the text cannot drift from the
  computation.
- All symbols and display equations are native Word equation objects (OMML).
- References must be real and verifiable, weighted towards 2023–2026.
