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
| **CSS** | External `/css/main.css` — shared, cached across all pages |
| **JS (i18n)** | External `/js/i18n.js` — translations + helpers, loaded at body bottom |
| **JS (Three.js)** | External `/js/three-bg.js` — deferred ES module |
| **Images** | WebP primary (`profile.webp`) with JPEG fallback, `fetchpriority="high"` on LCP |
| **CDN Preconnect** | `css/main.css`, `js/i18n.js`, `js/three-bg.js` are on Vercel origin; Three.js CDN and Google Fonts have `<link rel="preconnect">` hints |
| **3D Background** | Three.js v0.160.0 (CDN importmap) — bronze neural constellation |
| **i18n** | Reactive JS dictionary (EN/SK) — localStorage persistence |
| **Blog** | Static HTML + `blog/posts.json` manifest |
| **Lead Capture** | Python WSGI (`leads.db` SQLite) + Caddy reverse proxy (`:8701`) |
| **Hosting** | Vercel (auto-deploy from `main` branch) |
| **Media** | Cloudflare R2 (`marian-stancik-media` bucket) |
| **Email** | AgentMail (`marian_stancik@agentmail.to`) |
| **Sync** | Syncthing → iPhone/Mac/PC |

---

## 6. Coding Agent — OpenCode

**Preferovaný externý kódovací agent:** OpenCode (`/root/.local/bin/opencode`)

| Property | Value |
|:---------|:-------|
| **CLI** | `/root/.local/bin/opencode` |
| **Provider** | OpenRouter (kľúč v `/root/.hermes/auth.json`) |
| **Model** | `openrouter/deepseek/deepseek-v4-flash` |
| **Auth** | Export `OPENROUTER_API_KEY` z `auth.json` do env |
| **Workdir** | `/root/marian-stancik-web` |
| **Short tasks** | `terminal("opencode run --model ... 'prompt'")` |
| **Long tasks** | `execute_code` s `subprocess.run` (vyhne sa quoting problémom) |
| **Repo req** | Vyžaduje git repo |

```python
# Reliable pattern:
import subprocess
env = {'OPENROUTER_API_KEY': key, 'PATH': '/root/.local/bin:/usr/bin:/bin:/usr/local/bin:/root/.hermes/node/bin'}
result = subprocess.run(['/root/.local/bin/opencode', 'run', '--model', 'openrouter/deepseek/deepseek-v4-flash', 'task'],
    capture_output=True, text=True, timeout=120, env=env, cwd='/root/marian-stancik-web')
```

---

## 7. i18n — Language Switching (EN/SK)

**Architektúra:** Inline JS dictionary (`const translations = {en: {...}, sk: {...}}`) v každom HTML.

**Kritický detail:** Každý element je individuálne null-safe:
```javascript
var _e = document.getElementById('X'); if(_e) _e.textContent = d.Y;
```
Ak element neexistuje (napr. `skipLinkText` na home page), je preskočený — ostatné preklady bežia ďalej.

**Prepínanie:** `switchLanguage(lang)` → nastaví `currentLang`, uloží do `localStorage('ms_lang')`, zavolá `applyTranslations()` a `loadDynamicPostsHome()`.

---

## 8. Footer Links Status

| Link | Status | Detail |
|:-----|:-------|:-------|
| Prime Agent Masterclass | ⏳ | "(coming soon)" — no link |
| ASCENTIA s.r.o. | ⏳ | "(coming soon)" — no link (domain not purchased) |
| Open Source | ✅ | GitHub profile |
| Blog | ✅ | `/blog` |
| Social (X, YT, GH, LI) | ✅ | All working |

---

## 9. About Text — Key Changes

- **"Since 2023"** — added to first paragraph (replaced old intro)
- **University paragraph removed** — no "90 years" or "90-ročnou" anywhere
- **Defence Product Manager** — now includes legal-by-design under EU AI Act/GDPR/NIS2
- **Drone paragraph** — concise (1500g, Pixhawk, RPi 5, €2.6M)
- **CEO paragraph** — concise ("AI-first company running 24/7")
- **Stats** — Open Source Repos (6) + 24/7 Agent Runtime (replaced PF UK tradition)
- All changes synced to both inline HTML and i18n EN/SK dictionaries

---

## 10. Drones Page — Complete Build Specs

6 categories of build specifications + complete shopping list:

1. **Frame & Motors** — GEPRC Mark4-8, iFlight XING2 2809, HQprop, GNB battery
2. **Electronics & FC** — Skystars H7 Dual Gyro, Radiomaster XR1, FlyfishRC GPS
3. **AI & Autopilot** — Raspberry Pi 5 8GB, Camera 3, BEC, servo release mechanism
4. **FPV System** — Caddx Ratel 2, Axisflying Smurfs VTX, Skyzone Cobra X
5. **Ground Control** — RadioMaster Pocket, Samsung 35E, iSDT charger
6. **Tools & Assembly** — 19 items (soldering station, wire, flux, multimeter, etc.)

---

## 11. Lead CRM

- **Database:** `/opt/hermes-vault/leads.db` (SQLite) — extended schema (name, phone, message, company, contact_status)
- **Web form** → Python WSGI on VPS (`:8701`) → leads.db
- **Vault mirror:** `/opt/hermes-vault/05_INBOX/leads/` — per-lead .md files with BOM
- **Status taxonomy:** new → contacted → meeting → proposal → negotiation → won | lost
- **Auto-monitor:** `lead-monitor.py` — checks DB → creates vault lead files

---

## 12. Git & Deployment

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

## 13. Test Matrix (MANDATORY before every push)

| Vrstva | Nástroj | Čo testuje | Rýchlosť |
|:-------|:--------|:-----------|:---------|
| **L0 — Syntax** | `node --check` | JS syntax v inline scriptoch | <1s |
| **L1 — HTTP** | `curl` | HTTP 200, hlavičky, SEO meta | ~2s |
| **L2 — DOM** | Playwright | Počet sekcií, výška, Three.js, i18n | ~30s |
| **L3 — Screenshot** | Playwright | Full-page vizuálna kontrola | ~10s |
| **L4 — Security** | `grep` | Delta Defence, secrets v HTML | ~1s |
| **L5 — i18n** | Playwright | SK prepnutie, kľúče nie sú prázdne | ~5s |
| **L6 — Links** | Playwright | Všetky `<a href>` vracajú 200 | ~15s |
| **L7 — Mobile** | Playwright 375px | Responzívny layout, menu | ~15s |

**One command to run all:**
```bash
python3 test_visual.py
```

### Per-page thresholds

| Check | Threshold | Fail example |
|:------|:----------|:-------------|
| bodyHeight | > 500px (subpages), > 2000px (/) | Prázdna = ~100px |
| sectionCount | > 2 (subpages), > 5 (/) | Iba 1 sekcia |
| section height | každá > 50px | Empty section |
| section text | každá > 100 chars | Empty content |
| Three.js | `<canvas>` exists | Blog page ✅ intentionally no canvas |
| i18n ready | `translations` + `switchLanguage` | Broken JS object |
| i18n works | SK text detected | "Kontakt" / "Spojenie" in DOM |
| JS errors (console) | 0 | SyntaxError |
| L0 syntax | `node --check` exit 0 | Missing comma, extra brace |

## 14. Workflow (MANDATORY — every single change)

```bash
# Step 1: Pull latest
git pull --rebase origin main

# Step 2: Make changes (patch tool ONLY — never cat write_file on HTML)

# Step 3: L0 — JS syntax validation
python3 -c "
import subprocess
pages = ['index.html','about.html','expertise.html','skills.html','drones.html','contact.html']
for p in pages:
    c = open(p).read()
    s = c.find('<script>\\nconst translations = {')
    if s>-1:
        e = c.find('</script>', s)
        js = c[s+len('<script>'):e]
        open('/tmp/v.js','w').write(js)
        r = subprocess.run(['node','--check','/tmp/v.js'], capture_output=True, text=True, timeout=10)
        print(f\"{'✅' if r.returncode==0 else '❌'} {p}: {'ok' if r.returncode==0 else r.stderr[:80]}\")
"

# Step 4: L4 — Security sweep
grep -rn 'Delta Defence' . --include="*.html" 2>/dev/null && echo "❌ FAIL" || echo "✅ Delta Defence not found"

# Step 5: L1+L2+L5+L6+L7 — Browser test (30s)
python3 test_visual.py

# Step 6: Only if ALL pass — deploy
git add -A
git commit -m "..."
git push origin main
git push origin main:master

# Step 7: Verify live
sleep 20 && python3 test_visual.py
```