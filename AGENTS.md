# marian-stancik-web — Personal Brand Website & Autonomous Engineering Hub

**Owner:** Marian Stancik  
**Domain:** https://marianstancik.dev (Production on Vercel)  
**Repo:** https://github.com/Abra7abra7/marian_stancik_dev_web  
**VPS:** 188.245.224.189 (Hetzner Cloud — Caddy + Python WSGI + Hermes Agent)  

---

## 1. Executive Overview

Personal brand and technical showcase website for Marian Stancik — AI Engineer, Defence Product Manager (confidential), Law scholar at PF UK, Drone pilot (EASA A1/A3, €2.6M insured), and CEO of ASCENTIA s.r.o.

Three core pillars:
1. **AI & Autonomous Agents:** Hermes Agent, MCP servers, cron-orchestrated 24/7 agents on Hetzner VPS
2. **Law & AI Compliance:** PF UK law — EU AI Act, GDPR, NIS2, legal-by-design
3. **UAV Systems:** Custom 1500g carbon quads, Pixhawk 6C + ArduPilot + Raspberry Pi 5 edge AI

---

## 2. ANONYMIZATION RULE (CRITICAL)

**Delta Defence is NEVER mentioned by name anywhere on the web.**  
Strict security requirement. Only "Defence Product Manager" and "Defence Industry" are used.

- ✅ Hero: "Defence Product Manager"
- ✅ About: "Defence Product Manager"  
- ✅ JSON-LD: `"name": "Defence Industry (confidential)"`
- ✅ SK: "Defence Product Manager"
- ✅ llms.txt, blog, all pages: no company name

---

## 3. Site Architecture — 6 podstránok

| Page | URL | Content |
|:-----|:----|:--------|
| **Home** | `/` | Hero + stats (19+ cron, 3 domains, 3+ yrs, €2.6M, 6 repos, 24/7) + blog preview + lead + connect |
| **About** | `/about` | Full bio — AI Eng, Defence PM, PF UK law, UAV builder — "Since 2023" |
| **Expertise** | `/expertise` | Three pillars with bronze SVG icons (gradient defs in all pages) |
| **Skills** | `/skills` | AI Engineering Skills Map — 4 categories × 5 items |
| **Drones** | `/drones` | FPV video + complete build specs (6 categories) + shopping list |
| **Contact** | `/contact` | Connect section with social links + email |
| **Blog** | `/blog` | Blog listing |

Vercel `cleanUrls: true` enables `/about` → `about.html` resolution.

---

## 4. SEO & Discovery

| Asset | URL | Status |
|:------|:----|:-------|
| Sitemap | `/sitemap.xml` | ✅ 11 URLs (pages + posts + rss) |
| RSS | `/rss.xml` | ✅ Created (3 posts) |
| llms.txt | `/llms.txt` | ✅ GEO, endpoints, pillars |
| llms-full.txt | `/llms-full.txt` | ✅ Full AI agent knowledge graph |
| IndexNow | API | ✅ Submitted for all pages |
| Google GSC | meta tag | ✅ G-HJ4MZ66NEY |
| JSON-LD | All pages | ✅ Person + WebPage schema |
| SVG gradient | All pages | ✅ bronzeGrad defs fix (expertise icons) |

---

## 5. Tech Stack & Services

| Layer | Technology |
|:------|:-----------|
| **Frontend** | HTML5 / CSS3 / Vanilla JS — zero build, responsive |
| **3D Background** | Three.js v0.160.0 (CDN importmap) — bronze neural constellation |
| **i18n** | Reactive JS dictionary (EN/SK) — localStorage persistence |
| **Blog** | Static HTML + `blog/posts.json` manifest |
| **Lead Capture** | Python WSGI (`leads.db` SQLite) + Caddy reverse proxy (`:8701`) |
| **Hosting** | Vercel (auto-deploy from `main` branch) |
| **Media** | Cloudflare R2 (`marian-stancik-media` bucket) |
| **Email** | AgentMail (`marian_stancik@agentmail.to`) |
| **Sync** | Syncthing → iPhone/Mac/PC |

---

## 6. Footer Links Status

| Link | Status | Detail |
|:-----|:-------|:-------|
| Prime Agent Masterclass | ⏳ | "(coming soon)" — no link |
| ASCENTIA s.r.o. | ⏳ | "(coming soon)" — no link (domain not purchased) |
| Open Source | ✅ | GitHub profile |
| Blog | ✅ | `/blog` |
| Social (X, YT, GH, LI) | ✅ | All working |

---

## 7. About Text — Key Changes

- **"Since 2023"** — added to first paragraph (replaced old intro)
- **University paragraph removed** — no "90 years" or "90-ročnou" anywhere
- **Defence Product Manager** — now includes legal-by-design under EU AI Act/GDPR/NIS2
- **Drone paragraph** — concise (1500g, Pixhawk, RPi 5, €2.6M)
- **CEO paragraph** — concise ("AI-first company running 24/7")
- **Stats** — Open Source Repos (6) + 24/7 Agent Runtime (replaced PF UK tradition)
- All changes synced to both inline HTML and i18n EN/SK dictionaries

---

## 8. Drones Page — Complete Build Specs

6 categories of build specifications + complete shopping list:

1. **Frame & Motors** — GEPRC Mark4-8, iFlight XING2 2809, HQprop, GNB battery
2. **Electronics & FC** — Skystars H7 Dual Gyro, Radiomaster XR1, FlyfishRC GPS
3. **AI & Autopilot** — Raspberry Pi 5 8GB, Camera 3, BEC, servo release mechanism
4. **FPV System** — Caddx Ratel 2, Axisflying Smurfs VTX, Skyzone Cobra X
5. **Ground Control** — RadioMaster Pocket, Samsung 35E, iSDT charger
6. **Tools & Assembly** — 19 items (soldering station, wire, flux, multimeter, etc.)

---

## 9. Lead CRM

- **Database:** `/opt/hermes-vault/leads.db` (SQLite) — extended schema (name, phone, message, company, contact_status)
- **Web form** → Python WSGI on VPS (`:8701`) → leads.db
- **Vault mirror:** `/opt/hermes-vault/05_INBOX/leads/` — per-lead .md files with BOM
- **Status taxonomy:** new → contacted → meeting → proposal → negotiation → won | lost
- **Auto-monitor:** `lead-monitor.py` — checks DB → creates vault lead files

---

## 10. Git & Deployment

### Branches
- **`main`** — Vercel production trigger
- **`master`** — synced to `main` on every push

### Workflow
```bash
git pull --rebase origin main   # Always before work
git add -A && git commit -m "..."
git push origin main            # Triggers Vercel deploy
git push origin main:master     # Sync branches
```

### IndexNow
```bash
# After URL changes:
curl -X POST https://api.indexnow.org/indexnow \
  -H "Content-Type: application/json" \
  -d '{"host":"www.marianstancik.dev","key":"60f8a34d7b694a3d8eacc8642d372787","urlList":["https://www.marianstancik.dev/","https://www.marianstancik.dev/about",...]}'
```

---

## 11. Verification Commands

```bash
# HTTP 200 check for all pages
for url in / /about /expertise /skills /drones /contact /blog; do
  curl -s -o /dev/null -w "%{http_code}" "https://www.marianstancik.dev${url}"
done

# Delta Defence sweep
grep -rn 'Delta Defence' . --include="*.html" --include="*.md" --include="*.txt" 2>/dev/null

# 90 years sweep
grep -rn '90 years\|90-ročn' . --include="*.html" 2>/dev/null

# SEO meta
curl -s https://www.marianstancik.dev/about | grep -E '<title>|<meta name="description"|<link rel="canonical"|<script type="application/ld\+json"'
```