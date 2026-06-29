/**
 * gsap-horizontal-pan.tsx
 * Horizontal scroll gallery: vertical scroll drives a horizontal translate of
 * a wide track, pinned in the viewport.  Stack: React + GSAP 3.15 + ScrollTrigger.
 *
 * Honesty note: runnable skeleton, not a full app. JSX structure complete.
 *
 * Correctness points:
 *  - prefers-reduced-motion: when reduced, we DON'T pin/scrub. Instead we let
 *    the track scroll horizontally with native overflow-x (still fully usable
 *    via trackpad/keyboard), so we never trap or hijack the user's scroll.
 *  - cleanup: gsap.context + ctx.revert() on unmount.
 *  - the horizontal distance is computed from real measured widths, recomputed
 *    on ScrollTrigger.refresh() (handled automatically on resize).
 */
"use client";

import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

type Panel = { id: string; label: string };

export interface HorizontalPanProps {
  panels: Panel[];
}

export default function HorizontalPan({ panels }: HorizontalPanProps) {
  const root = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce || !root.current || !track.current) return; // native overflow fallback

    const ctx = gsap.context(() => {
      const el = track.current!;
      gsap.to(el, {
        x: () => -(el.scrollWidth - window.innerWidth),
        ease: "none",
        scrollTrigger: {
          trigger: root.current!,
          start: "top top",
          end: () => "+=" + (el.scrollWidth - window.innerWidth),
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true, // recompute distance on resize
        },
      });
    }, root);

    return () => ctx.revert();
  }, [panels.length]);

  return (
    <div ref={root} style={{ overflow: "hidden" }}>
      <div
        ref={track}
        style={{
          display: "flex",
          gap: "2rem",
          // fallback: if reduced-motion, this allows native horizontal scroll
          overflowX: "auto",
          willChange: "transform",
        }}
      >
        {panels.map((p) => (
          <article
            key={p.id}
            style={{ flex: "0 0 80vw", minHeight: "70vh", display: "grid", placeItems: "center" }}
          >
            <h2>{p.label}</h2>
          </article>
        ))}
      </div>
    </div>
  );
}
