/**
 * motion-scroll-reveal.tsx
 * Staggered scroll-reveal using Motion (framer-motion 12.x). Children fade/slide
 * up in sequence as they enter the viewport.  Stack: React + framer-motion.
 *   npm i framer-motion
 *
 * Honesty note: runnable skeleton, not a full app. JSX structure complete.
 *
 * Correctness points:
 *  - prefers-reduced-motion: Motion's useReducedMotion() hook. When true we
 *    render with NO transform/opacity animation (content visible immediately),
 *    honoring the OS setting without extra branches in markup.
 *  - cleanup: Motion + whileInViewport manage their own observers and tear them
 *    down on unmount; no manual listeners are added, so nothing leaks.
 *  - `once: true` so reveal fires a single time (no replay flicker on scroll-up).
 */
"use client";

import { motion, useReducedMotion, type Variants } from "framer-motion";

type Item = { id: string; title: string; body: string };

export interface ScrollRevealProps {
  items: Item[];
}

export default function ScrollReveal({ items }: ScrollRevealProps) {
  const reduce = useReducedMotion();

  const container: Variants = {
    hidden: {},
    show: { transition: { staggerChildren: reduce ? 0 : 0.12 } },
  };

  const child: Variants = reduce
    ? { hidden: { opacity: 1, y: 0 }, show: { opacity: 1, y: 0 } }
    : {
        hidden: { opacity: 0, y: 24 },
        show: {
          opacity: 1,
          y: 0,
          transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] },
        },
      };

  return (
    <motion.ul
      variants={container}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, amount: 0.3 }}
      style={{ listStyle: "none", padding: 0, display: "grid", gap: "1.5rem" }}
    >
      {items.map((it) => (
        <motion.li key={it.id} variants={child}>
          <h3>{it.title}</h3>
          <p>{it.body}</p>
        </motion.li>
      ))}
    </motion.ul>
  );
}
