---
name: better-ui
description: Design engineering principles for making interfaces feel polished. Use when building UI components, implementing animations or hover states, or doing any visual detail work. Triggers on UI polish, "feels off", stagger animations, enter animations, theme switch transitions, border radius, optical alignment, image outlines, box shadows, icons, icon stroke weight, motion restraint.
---

# UI Polish & Design Engineering

Polish comes from a pile of small details that compound. This skill is the reference for which are worth having and what values they take.

## 1. Concentric Border Radius
- **Formula:** Outer radius = inner radius + padding.
- Mismatched radii on nested elements is the most common reason an interface looks unrefined.

## 2. Optical over Geometric Alignment
- When geometric centering looks off, align optically. Buttons with icons, arrows, and asymmetric icons need a manual nudge (1-2px padding tweak).

## 3. Shadows for Elevation, Borders for Structure
- Where a border exists only to create depth, prefer layered transparent `box-shadow` values.
- Keep subtle borders only to communicate structure (dividers, cards, focus rings).

## 4. Scale on Press
- A `scale(0.96)` on button click/active state gives instant tactile physical feedback.
- Always use `0.96` (values below 0.95 feel exaggerated).

## 5. Contextual Icon Animations & SVG States
- Icons use `currentColor` and take hover/active states from CSS color and opacity.
- Outline is the default variant; fill or glow marks the active state.
- Match icon stroke weight (`1.5px` to `2px`) to the optical weight of adjacent text.

## 6. Transition Discipline
- Never use `transition: all`. Always specify exact properties: `transition: transform 0.2s cubic-bezier(0.2, 0, 0, 1), opacity 0.2s ease, border-color 0.2s ease`.
