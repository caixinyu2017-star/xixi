/**
 * gsap-sticky-stack.tsx
 * Sticky "stacking cards" scroll effect: cards pin and overlap as you scroll.
 * Stack: React 18/19 + GSAP 3.15 + ScrollTrigger.  npm i gsap
 *
 * Honesty note: this is a runnable skeleton, not a full app. Drop into a
 * Next.js client component or Vite + React project. JSX structure is complete;
 * `node --check` does not parse TSX, so structural correctness is the contract.
 *
 * Key correctness points implemented here:
 *  - prefers-reduced-motion: motion is gated; with reduced motion we skip
 *    pinning + scrubbing and just show the cards statically (no jank, no harm).
 *  - cleanup: gsap.context() scopes every tween/ScrollTrigger to this component;
 *    ctx.revert() in the effect cleanup kills them on unmount (no leaks, no
 *    duplicate triggers on Fast Refresh / re-render).
 *  - SSR-safe: all GSAP work runs inside useLayoutEffect (client only).
 */
"use client";

import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

type Card = { id: string; title: string; body: string };

export interface StickyStackProps {
  cards: Card[];
}

export default function StickyStack({ cards }: StickyStackProps) {
  const root = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce || !root.current) return; // static fallback, no animation

    const ctx = gsap.context(() => {
      const panels = gsap.utils.toArray<HTMLElement>(".stack-card");
      panels.forEach((panel, i) => {
        if (i === panels.length - 1) return; // last card stays put
        gsap.to(panel, {
          scale: 0.92,
          autoAlpha: 0.5,
          ease: "none",
          scrollTrigger: {
            trigger: panel,
            start: "top top",
            end: "+=100%",
            pin: true,
            pinSpacing: false,
            scrub: true,
          },
        });
      });
    }, root);

    return () => ctx.revert(); // kills tweens + ScrollTriggers, restores DOM
  }, [cards.length]);

  return (
    <div ref={root}>
      {cards.map((c) => (
        <section
          key={c.id}
          className="stack-card"
          style={{
            position: "sticky",
            top: 0,
            minHeight: "100vh",
            display: "grid",
            placeItems: "center",
          }}
        >
          <div>
            <h2>{c.title}</h2>
            <p>{c.body}</p>
          </div>
        </section>
      ))}
    </div>
  );
}
