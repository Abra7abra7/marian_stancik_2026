# marian-stancik-web — Personal Brand Website & Engineering Hub

**Owner:** Marian Stancik  
**Domain:** https://marianstancik.dev (Vercel)  
**Repo:** https://github.com/Abra7abra7/marian_stancik_2026  
**VPS:** 188.245.224.189 (Hetzner — Caddy + subscriber API)  

---

## What is this?

Personal brand and technical showcase website for Marian Stancik — AI Agent Developer, Product Manager at Delta Defence, Law student at PF UK, Drone pilot (A1/A3), and CEO of ASCENTIA s.r.o.

The website demonstrates the synthesis of three core pillars:
1. **AI & Autonomous Agents** (Hermes Agent, cron-orchestrated 24/7 background agents, multi-agent systems).
2. **Law & AI Compliance** (EU AI Act, GDPR, NIS2, legal-by-design engineering).
3. **Drones & UAV Systems** (ArduPilot/PX4 custom UAVs, €2.6M insured, tactical mission planning).

The site is built with zero framework overhead (pure HTML5/CSS3/Vanilla JS), fully bilingual (EN/SK), equipped with a JSON-driven automated blog feed, and optimized for both human users and AI crawlers (Perplexity, ChatGPT, Claude, Gemini).

---

## Tech Stack & Architecture

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Pure HTML5 / CSS3 / Vanilla JS | Zero build step, maximum speed, instant loads |
| **3D Background** | Three.js v0.160.0 (CDN importmap) | Bronze neural network particle & node constellation |
| **Localization (i18n)** | Pure JS reactive dictionary (`translations`) | Live bilingual toggle (EN / SK) with `localStorage` persistence |
| **Blog System** | `blog/posts.json` manifest + standalone HTML | Hybrid SSG/Client hydration: static fallback + dynamic feed |
| **Icons & Branding** | Custom inline SVG vectors + bronze gradients | Sharp, responsive icons with glow hover micro-interactions |
| **Lead Capture** | Python WSGI (`leads.db` SQLite) + Caddy reverse proxy | Automated newsletter subscription endpoint (`:8701`) |
| **Notifications** | AgentMail (`marian_stancik@agentmail.to`) | Direct inbox for leads and system notifications |
| **AI / Search SEO** | `llms.txt` + JSON-LD (`Person`, `WebSite`, `BlogPosting`) + XML Sitemap | High-authority crawler indexing and AI agent discovery |

---

## Project Structure

```
/marian-stancik-web/
├── index.html                                    ← Main landing page (Bilingual, Three.js, Hero, About, Expertise, Projects, Blog Preview, Leads, Connect, Footer)
├── profile.jpg                                   ← Profile photo (Optimized JPEG, 15 KB)
├── favicon.svg                                   ← Bronze monogram SVG favicon
├── apple-touch-icon.svg                          ← Apple touch icon
├── llms.txt                                      ← AI crawler structured knowledge & direct article links
├── robots.txt                                    ← Search crawler directives + sitemap location
├── sitemap.xml                                   ← Full XML sitemap including all blog articles
├── AGENTS.md                                     ← Project architecture, conventions & agent documentation
├── AUDIT.md                                      ← Web quality, SEO & Lighthouse audit report
│
└── blog/
    ├── index.html                                ← Blog listing page (Bilingual EN/SK, dynamic post hydration from posts.json)
    ├── posts.json                                ← Single source of truth for all blog post metadata (EN & SK titles, excerpts, tags, URLs)
    └── posts/
        ├── 2026-08-22-building-digital-twin.html         ← Article 1: Autonomous Hermes agent posting 9x daily
        ├── 2026-08-20-ai-act-compliance.html             ← Article 2: Legal-by-design EU AI Act compliance guide
        └── 2026-08-17-autonomous-drone-missions.html     ← Article 3: Pixhawk, ArduPilot & Python UAV mission planning
```

---

## How the Bilingual Translation System (i18n) Works

1. **Client-Side Reactive Dictionary:**
   - All translatable strings are organized in a `translations` JavaScript object inside `index.html` (and localized `i18n` object in `blog/index.html`).
   - Supported languages: `en` (English - default) and `sk` (Slovak).
2. **State & Persistence:**
   - Selected language is persisted in the visitor's browser via `localStorage.getItem('ms_lang')`.
   - On page load, `applyTranslations()` immediately hydrates all DOM elements with the saved language preference.
3. **Instant DOM Updates (Zero Page Reload):**
   - Headings, body paragraphs, role descriptions, stat labels, project cards, and meta tags (`document.title`, `meta[name="description"]`, Open Graph locale) update dynamically via `textContent` and `innerHTML`.
   - Structural SVG icons inside buttons and badges remain preserved because translation target IDs are placed on specific inner text spans (e.g. `<span id="rolePm">...</span>`).
4. **Blog Grid Re-hydration:**
   - Calling `switchLanguage(lang)` immediately calls `loadDynamicPostsHome()`, which re-renders the blog cards with the appropriate language strings (`titleSk` / `excerptSk` / `displayDateSk` vs `title` / `excerpt` / `displayDate`).

---

## How the Blog Engine & Dynamic Feed Works

The blog uses a **hybrid architecture** combining instant static HTML rendering (for zero layout shift and offline indexing) with dynamic JSON hydration:

```
┌─────────────────────────────────────────────────────────────┐
│                      blog/posts.json                         │
│   (Single source of truth: URLs, dates, tags, EN/SK texts)   │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│          index.html          │ │       blog/index.html        │
│   `loadDynamicPostsHome()`   │ │     `loadDynamicPosts()`     │
│  Fetches JSON & renders top  │ │  Fetches JSON & renders all  │
│  3 articles in active lang   │ │  articles with active lang   │
└──────────────────────────────┘ └──────────────────────────────┘
               │                              │
               └──────────────┬───────────────┘
                              ▼
        ┌───────────────────────────────────────────┐
        │        blog/posts/[slug].html             │
        │   Standalone, SEO-optimized articles      │
        │   with JSON-LD `BlogPosting` metadata     │
        └───────────────────────────────────────────┘
```

### 1. `blog/posts.json` Schema
Each entry in `posts.json` contains:
```json
{
  "id": "building-digital-twin",
  "url": "blog/posts/2026-08-22-building-digital-twin.html",
  "urlFromBlog": "posts/2026-08-22-building-digital-twin.html",
  "date": "2026-08-22",
  "displayDate": "August 22, 2026",
  "displayDateSk": "22. august 2026",
  "readTime": "4 min read",
  "readTimeSk": "4 min čítania",
  "title": "Building a Digital Twin That Posts 9x Daily",
  "titleSk": "Ako postaviť Digital Twin, ktorý publikuje 9x denne",
  "excerpt": "How I built an autonomous AI agent with Hermes...",
  "excerptSk": "Ako som postavil autonómneho AI agenta cez Hermes...",
  "tags": ["AI Agents", "Hermes", "Automation"]
}
```

### 2. Autonomous Publishing Pipeline (Hermes Agent)
- To publish a new article automatically:
  1. Generate the standalone article HTML file in `blog/posts/YYYY-MM-DD-slug.html` using the existing template structure with JSON-LD schema.
  2. Prepend the new metadata entry into `blog/posts.json`.
  3. Append the new URL into `sitemap.xml` and `llms.txt`.
  4. Git commit and push to `master` (Vercel automatically builds and deploys within seconds).

---

## Critical Convention: Relative Paths (`file:///` & Web Compatibility)

> [!IMPORTANT]
> **Never use root-absolute paths starting with `/` (e.g. `/blog/` or `/blog/posts/...`) in internal links or fetch requests.**

- **Why:** On Windows and local testing, opening HTML files directly from disk (`file:///C:/Users/mstancik/.../index.html`) causes root-absolute links `/blog/` to resolve to `file:///C:/blog/` (which fails).
- **Rule:** Always use strictly relative paths:
  - From `index.html` ➔ `blog/`, `blog/posts/slug.html`, `blog/posts.json`, `favicon.svg`
  - From `blog/index.html` ➔ `../`, `posts/slug.html`, `posts.json`, `../favicon.svg`
  - From `blog/posts/*.html` ➔ `../../`, `../`, `../../favicon.svg`

---

## Design System & Iconography

- **Theme:** Sleek dark-mode aesthetic (`#08080F`) with polished bronze metallic accents (`#CD7F32` and `#E8B86D`).
- **Icons:** All emojis and generic icons have been replaced with sharp, inline SVG vectors:
  - **Socials:** Official vector geometries for 𝕏, GitHub, LinkedIn, Instagram, Email, and Blog.
  - **Role Badges:** Mini vector icons for defense radar, scales of justice, UAV drone, and corporate crest.
  - **Expertise Cards:** Custom vector icons with linear bronze gradient strokes (`#bronzeGrad`).
  - **Project Cards:** Dedicated branded iconography with `.card-icon-wrap` containers that feature glow transitions on hover.

---

## Lead Capture & Backend

- **Endpoint:** `http://188.245.224.189/api/subscribe` (Caddy reverse proxy on Hetzner VPS to Python WSGI daemon `:8701`).
- **Database:** SQLite at `/opt/hermes-vault/leads.db`.
- **Fallback:** If the API endpoint is unreachable or blocked by browser mixed-content restrictions, the form seamlessly opens a pre-filled `mailto:` client window to ensure no lead is ever lost.

---

## Testing & Verification

### Link & Integrity Verification Script
Run the automated integrity verification script to ensure 100% relative path resolution:
```bash
node -e "
const fs = require('fs'), path = require('path');
function check(file, dir) {
  const c = fs.readFileSync(file, 'utf8');
  for (const m of c.matchAll(/href=\"([^\"]+)\"/g)) {
    const h = m[1];
    if (h.startsWith('http') || h.startsWith('#') || h.startsWith('mailto:')) continue;
    const target = h.endsWith('/') ? h + 'index.html' : h;
    const exists = fs.existsSync(path.resolve(dir, target));
    if (!exists && !h.includes('${')) console.error('Broken link:', file, '->', h);
  }
}
check('index.html', '.');
check('blog/index.html', 'blog');
fs.readdirSync('blog/posts').forEach(p => check(path.join('blog/posts', p), 'blog/posts'));
console.log('Link verification complete.');
"
```

### Git Deploy Command
```bash
git add .
git commit -m "✨ feat: update website architecture, i18n, blog feed, and branding"
git push origin master
# Vercel deploys automatically to https://marianstancik.dev
```