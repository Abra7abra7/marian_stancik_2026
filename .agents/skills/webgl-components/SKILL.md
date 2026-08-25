---
name: webgl-components
description: Build small, always-on WebGL visuals (identity avatars, ambient orbs, glass and iridescent surfaces, animated textures) that ship inside a normal web app UI without wrecking performance, accessibility, SSR, or layout.
---

# WebGL Visual Components & Resilience

## 1. Zero-Jank & Battery Optimization
- Disconnect render loop or cap framerate when the tab is hidden (`document.hidden` or `visibilitychange`).
- Do not render off-screen canvases: use `IntersectionObserver` to pause Three.js animation when the canvas is scrolled out of view.

## 2. Robust Hardware Caveat & Fallback
- Always pass `failIfMajorPerformanceCaveat: true` to prevent CPU software-rasterizer lag on machines with disabled hardware acceleration.
- Provide a clean CSS gradient fallback if WebGL fails or context is lost.

## 3. Reduced Motion
- Listen to `@media (prefers-reduced-motion: reduce)`: render a single high-quality static frame and never start the continuous rotation loop.
