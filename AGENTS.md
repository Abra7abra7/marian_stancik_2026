# marian-stancik-web — Personal Brand Website & Autonomous Engineering Hub

**Owner:** Marian Stancik  
**Domain:** https://marianstancik.dev (Production on Vercel)  
**Repo:** https://github.com/Abra7abra7/marian_stancik_dev_web  
**VPS:** 188.245.224.189 (Hetzner Cloud — Caddy + Python WSGI + Hermes Agent)  

---

## 1. Executive Overview

Personal brand and technical showcase website for Marian Stancik — AI Engineer, CEO @ ASCENTIA, Drone pilot (EASA A1/A3, €2.6M insured).

Two core pillars:
1. **AI & Autonomous Agents:** Hermes Agent, MCP servers, cron-orchestrated 24/7 agents on Hetzner VPS
2. **UAV Systems:** Custom 1500g carbon quads, Pixhawk 6C + ArduPilot + Raspberry Pi 5 edge AI

---

## 2. ANONYMIZATION RULE (CRITICAL — ZERO TOLERANCE)

**Delta Defence is NEVER mentioned by name anywhere on the web.**  
Strict security requirement. Only "Defence Product Manager" and "Defence Industry" are used.

- ✅ Hero: "Defence Product Manager"
- ✅ About: "Defence Product Manager"  
- ✅ JSON-LD: `"name": "Defence Industry (confidential)"`
- ✅ SK: "Defence Product Manager"
- ✅ `llms.txt`, `llms-full.txt`, blog, AUDIT.md, all pages: **ZERO** company name references

---

## 3. Site Architecture — 6 Podstránok + Blog

| Page | URL | Content & Purpose |
|:-----|:----|:------------------|
| **Home** | `/` | Hero + stats (19+ cron, 3 domains, 3+ yrs, €2.6M, 6 repos, 24/7) + blog preview + lead + connect |
| **About** | `/about` | Full bio — AI Eng, Defence PM, PF UK law, UAV builder — "Since 2023" |
| **Expertise** | `/expertise` | Three pillars with bronze SVG icons (`#bronzeGrad` defs in all pages) |
| **Skills** | `/skills` | Full-stack AI Engineering Skills Map — 4 categories × 5 items |
| **Drones** | `/drones` | FPV video + complete build specs (6 categories) + shopping list |
| **Contact** | `/contact` | Connect section with social links + AgentMail direct inbox |
| **Blog** | `/blog` | Static blog listing + standalone articles in `/blog/posts/` |

Vercel `cleanUrls: true` enables `/about` → `about.html` resolution.

---

## 4. Design System & Tokens (`html-generator` Standards)

All pages adhere to the **`html-generator`** skill & design system token conventions defined in [`css/main.css`](file:///css/main.css):

### Color Tokens (Bronze Neural Theme)
- `--color-bg: #08080F;` (Deep dark canvas)
- `--color-bg-secondary: #0D0D18;` (Elevated surface)
- `--color-bg-card: rgba(18, 18, 30, 0.65);` (Glassmorphic card)
- `--color-primary: #CD7F32;` (Metallic Bronze)
- `--color-accent: #E8B86D;` (Gold / Amber Accent)
- `--color-glow: rgba(205, 127, 50, 0.2);` (Ambient glow)
- `--color-border: rgba(255, 255, 255, 0.06);`
- `--color-border-hover: rgba(205, 127, 50, 0.35);`

### Spacing & Layout Tokens
- `--space-xs: 4px;` | `--space-sm: 8px;` | `--space-md: 16px;` | `--space-lg: 24px;` | `--space-xl: 48px;` | `--space-2xl: 90px;`
- `--radius-sm: 6px;` | `--radius-md: 12px;` | `--radius-lg: 18px;` | `--radius-full: 9999px;`
- `--min-tap-target: 44px;` (Touch accessibility)

### Rules for HTML & CSS
1. **No external CSS frameworks:** No Tailwind, Bootstrap, or Foundation. Pure Vanilla CSS only.
2. **Root-relative paths:** Always use `/about`, `/expertise`, `/skills`, `/drones`, `/contact`, `/blog` (never relative `blog/index.html` on subpages).
3. **Accessibility (WCAG AA):**
   - Every page MUST contain `<a href="#main-content" class="skip-link">Skip to main content</a>`.
   - Single `<h1>` per page, hierarchical `<h2>` and `<h3>`.
   - Descriptive `aria-label` on all icon links and buttons.
4. **Active Nav State:** The current page's navigation link must have class `active` (e.g. `<a href="/about" class="nav-link active">`).

---

## 5. SEO & AI Agent Discovery (GEO / LLMO)

| Asset | URL / Target | Function & Status |
|:------|:-------------|:-------------------|
| **llms.txt** | `/llms.txt` | ✅ Machine-readable knowledge graph for Perplexity, ChatGPT, Claude |
| **llms-full.txt** | `/llms-full.txt` | ✅ Full deep-context graph of agent architectures & UAV specs |
| **Autodiscovery Tag** | `<link rel="alternate" type="text/plain" href="/llms.txt">` | ✅ Included in `<head>` of all HTML pages |
| **robots.txt** | `/robots.txt` | ✅ Explicitly allows `GPTBot`, `ClaudeBot`, `PerplexityBot`, `anthropic-ai`, `CCBot`, `Google-Extended`, `Applebot-Extended` |
| **Sitemap** | `/sitemap.xml` | ✅ Synchronized URLs (11 endpoints) |
| **RSS Feed** | `/rss.xml` | ✅ Valid XML RSS feed |
| **JSON-LD Schema** | All pages | ✅ Schema.org `Person`, `WebSite`, `AboutPage`, `CollectionPage`, `ContactPage` |
| **Google GSC** | meta tag | ✅ `G-HJ4MZ66NEY` |

---

## 6. Tech Stack & Architecture

| Layer | Technology | Details |
|:------|:-----------|:--------|
| **Frontend** | HTML5 / CSS3 / Vanilla JS | Zero-build, instant load, Lighthouse 100 target |
| **CSS** | `/css/main.css` | Centralized styles, `:root` design tokens, cached across pages |
| **JS (i18n)** | `/js/i18n.js` | Reactive EN/SK switcher, localStorage persistence, null-safe DOM binding |
| **JS (Three.js)** | `/js/three-bg.js` | Bronze neural constellation (deferred ES module) |
| **3D Background** | Three.js v0.160.0 | Importmap CDN: `https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js` |
| **Lead Capture** | Python WSGI | VPS `:8701` → SQLite `leads.db` + fallback `mailto:` |
| **Hosting** | Vercel | Auto-deploy on push to `main` branch (`cleanUrls: true`) |
| **Media CDN** | Cloudflare R2 | `marian-stancik-media` bucket |

---

## 7. i18n — Language Switching Protocol (EN/SK)

- **Storage:** Inline dictionary in `js/i18n.js` (`const translations = {en: {...}, sk: {...}}`).
- **Null-Safety Requirement:** All DOM updates MUST be null-safe:
  ```javascript
  var _e = document.getElementById('X'); if(_e) _e.textContent = d.Y;
  ```
- **Switching mechanism:** `switchLanguage(lang)` saves to `localStorage('ms_lang')` and triggers `applyTranslations()`.
- **New elements:** When adding new text to any HTML page, define an ID and register keys in both `en` and `sk` in `js/i18n.js`.

---

## 8. Test Matrix & Automated Verification

### Test Layers

| Layer | Tool | Scope | Speed |
|:------|:-----|:------|:------|
| **L0 — Syntax** | `node --check` | JS syntax in `js/i18n.js` and `js/three-bg.js` | <1s |
| **L1 — Security** | `re.findall` | Anonymization sweep (Delta Defence 0 occurrences) | <1s |
| **L2 — HTML Integrity** | Python script | No malformed `OG_` tags, valid JSON-LD URLs, root-relative links | <1s |
| **L3 — Design Tokens** | Python script | `:root` custom properties validated in `css/main.css` | <1s |
| **L4 — AI Discovery** | Python script | `llms.txt` tags in `<head>`, AI bot rules in `robots.txt` | <1s |
| **L5 — Browser & DOM** | Playwright (`test_visual.py`) | Mobile 375px viewport, Three.js `<canvas>`, visual screenshots | ~30s |

### Single Command Local Verification
Run the cross-platform test script before every commit:
```bash
python scripts/verify_site.py
```

---

## 9. Rules for Future Work (MANDATORY)

1. **🔒 Strict Anonymization:** Never mention confidential defense companies by name anywhere.
2. **⚡ Zero Build / Vanilla Only:** Do not introduce bundlers (Webpack, Vite, Tailwind CLI) into production runtime unless explicitly requested.
3. **🎨 Design Token Usage:** All colors and spacing must use `var(--color-...)` and `var(--space-...)` from `css/main.css`.
4. **🔗 Root-Relative Links:** Internal links must start with `/` (e.g. `/about`, `/blog`, `/contact`), never relative `blog/index.html` on subpages.
5. **♿ Accessibility First:** Keep `.skip-link`, semantic landmarks (`<main>`, `<nav>`, `<footer>`), and valid `aria-label` tags.
6. **🤖 Keep AI Metadata Synced:** When adding pages or updating capabilities, update `llms.txt`, `llms-full.txt`, `sitemap.xml`, and JSON-LD schemas.
7. **🌍 Dual i18n Keys:** Every new text element must have translations for both English and Slovak.

---

## 10. Standard Development Workflow

```bash
# Step 1: Pull latest changes
git pull --rebase origin main

# Step 2: Make edits to HTML / CSS / JS / Markdown

# Step 3: Run local verification script
python scripts/verify_site.py

# Step 4: Verify JS syntax
node --check js/i18n.js
node --check js/three-bg.js

# Step 5: Deploy (only when all checks pass)
git add -A
git commit -m "feat: [describe change]"
git push origin main

# Step 6: Verify production deployment on https://marianstancik.dev
```