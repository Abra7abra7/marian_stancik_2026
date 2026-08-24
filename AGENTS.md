# marian-stancik-web — Personal Brand Website & Autonomous Engineering Hub

**Owner:** Marian Stancik  
**Domain:** https://marianstancik.dev (Production on Vercel)  
**Repo:** https://github.com/Abra7abra7/marian_stancik_dev_web  
**VPS:** 188.245.224.189 (Hetzner Cloud — Caddy + Python WSGI + Hermes Agent)  

---

## 1. Executive Overview

Personal brand and technical showcase website for Marian Stancik — AI Agent Developer, Product Manager at Delta Defence a.s., Law student at PF UK, Drone pilot (EASA A1/A3, €2.6M insured), and CEO of ASCENTIA s.r.o.

The website demonstrates the synergy of three core pillars:
1. **AI & Autonomous Agents:** Hermes Agent, custom MCP servers, cron-orchestrated 24/7 background agents on European Hetzner Cloud VPS, Telegram & WhatsApp C2.
2. **Law & AI Compliance:** Faculty of Law, Comenius University in Bratislava (PF UK — 90+ years tradition, clinical legal education). Specialized in EU AI Act, GDPR, NIS2, and Legal-by-Design software architectures.
3. **Drones & UAV Systems:** Delta Defence tactical UAV engineering, custom hand-soldered 1500g carbon quads, Pixhawk 6C + ArduPilot, QGroundControl, Mission Planner, and onboard Raspberry Pi 5 edge AI neural companion guidance.

---

## 2. Tech Stack & Architecture

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Pure HTML5 / CSS3 / Vanilla JS | Zero build overhead, sub-second load, 100% responsive |
| **3D Background** | Three.js v0.160.0 (CDN importmap) | Bronze neural constellation particle & node network |
| **Localization (i18n)** | Reactive JS dictionary (`translations`) | Live bilingual toggle (EN / SK) with `localStorage` persistence |
| **Blog System** | `blog/posts.json` manifest + HTML | Hybrid SSG/Client hydration: static fallback + dynamic feed |
| **Branding & Icons** | Custom inline SVG vectors + bronze gradients | Sharp, scalable icons with glow hover micro-interactions |
| **Lead Capture** | Python WSGI (`leads.db` SQLite) + Caddy reverse proxy | Automated newsletter & lead subscription endpoint (`:8701`) |
| **Notifications** | AgentMail (`marian_stancik@agentmail.to`) | Direct inbox for leads and system notifications |
| **AI & Search SEO** | `llms.txt` + JSON-LD (`Person`, `WebSite`, `BlogPosting`) + Sitemap | High-authority crawler indexing and AI agent discovery |

---

## 3. Git & Deployment Architecture (GitOps)

### Primary Branch Convention: `main`
> [!IMPORTANT]
> **Vercel production deployments are triggered from the `main` branch.**  
> Always keep `main` and `master` in sync.

```bash
# Push directly to production:
git push origin main
git push origin main:master
```

### Hetzner VPS Synchronization (Hermes Agent Working Tree)
To ensure Hermes Agent on the Hetzner VPS never pushes outdated files:
```bash
cd /opt/hermes-vault/marian_stancik_dev_web   # (or VPS repo path)
git fetch origin main
git reset --hard origin/main
```

---

## 4. Automated Blog Publishing Pipeline (`scripts/publish_post.py`)

Hermes Agent publishes new articles autonomously using the CLI tool with built-in `git pull --rebase` protection:

```bash
python scripts/publish_post.py \
  --title "Article Title in English" \
  --title-sk "Názov článku v slovenčine" \
  --excerpt "Short English summary for meta tags and feed." \
  --excerpt-sk "Krátky slovenský popis pre meta tagy a feed." \
  --tags "AI Agents, Drones, Compliance" \
  --read-time "5 min read" \
  --read-time-sk "5 min čítania" \
  --content-file "path/to/content.html" \
  --push
```

### What the Pipeline Does Automatically:
1. **Pulls Latest Code:** Automatically executes `git pull origin main --rebase` before modifying files.
2. **Generates HTML Article:** Creates `blog/posts/YYYY-MM-DD-slug.html` with full Open Graph, Twitter Cards, and `BlogPosting` JSON-LD schema.
3. **Updates Manifest:** Prepends the new entry into `blog/posts.json`.
4. **Updates AI Knowledge Graph:** Appends new article endpoint into `llms.txt`.
5. **Git Commit & Push:** Pushes commit `📝 auto(blog): publish YYYY-MM-DD-slug` to `origin/main`.
6. **Vercel Auto-Deploy:** Website rebuilds and publishes the article live within ~15 seconds.

---

## 5. Critical Convention: Explicit Relative Paths

> [!IMPORTANT]
> **Never use directory-only links (e.g. `blog/`, `../`, `../../`) or root-absolute paths starting with `/` in internal links.**

- **Why:** In browser disk mode (`file:///C:/Users/.../index.html`), clicking `blog/` or `../` opens Chrome's folder directory view instead of the HTML page.
- **Rule:** Always use explicit `.html` relative paths:
  - From `index.html` ➔ `blog/index.html`, `blog/posts/slug.html`, `blog/posts.json`, `favicon.svg`
  - From `blog/index.html` ➔ `../index.html`, `posts/slug.html`, `posts.json`, `../favicon.svg`
  - From `blog/posts/*.html` ➔ `../../index.html`, `../index.html`, `../../favicon.svg`

---

## 6. Official Social Media Channels

All social links are standardized across `index.html`, `llms.txt`, and metadata:
- **𝕏 / Twitter:** [`https://x.com/marian_s_ai`](https://x.com/marian_s_ai) (`@marian_s_ai`)
- **YouTube:** [`https://www.youtube.com/@marian_ai`](https://www.youtube.com/@marian_ai) (`@marian_ai`)
- **Facebook:** [`https://www.facebook.com/profile.php?id=100089785398619`](https://www.facebook.com/profile.php?id=100089785398619)
- **Threads:** [`https://www.threads.com/`](https://www.threads.com/)
- **LinkedIn:** [`https://www.linkedin.com/in/marian-stancik-924b41298/`](https://www.linkedin.com/in/marian-stancik-924b41298/)
- **Instagram:** [`https://www.instagram.com/marian_stancik`](https://www.instagram.com/marian_stancik)
- **GitHub:** [`https://github.com/Abra7abra7`](https://github.com/Abra7abra7)
- **Email:** `marian_stancik@agentmail.to`
- **ASCENTIA:** [`https://ascentia.sk`](https://ascentia.sk)

---

## 7. Lead Capture & CRM Workflow

1. **Lead Submission:** Frontend submits `POST /api/subscribe` to Hetzner VPS (`http://188.245.224.189/api/subscribe`).
2. **Reverse Proxy & WSGI:** Caddy proxies requests to Python daemon `:8701`.
3. **Database:** Records stored in `/opt/hermes-vault/leads.db` (SQLite).
4. **Hermes C2 Integration:** Hermes Agent monitors `leads.db`, alerts via Telegram/WhatsApp, and can trigger automated AgentMail sequences.
5. **Zero-Loss Fallback:** If offline or blocked by browser mixed-content policy, form falls back to pre-filled `mailto:marian_stancik@agentmail.to`.

---

## 8. Verification & Quality Commands

```bash
# Verify all relative links across the website:
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
console.log('✅ Link verification passed.');
"

# Test blog publisher CLI dry run:
python scripts/publish_post.py --title "Test Title" --title-sk "Test Názov" --excerpt "Test excerpt" --excerpt-sk "Test popis" --dry-run
```