# marian-stancik-web — Personal Brand Website

**Owner:** Marian Stancik
**Domain:** https://marianstancik.dev (Vercel)
**Repo:** https://github.com/Abra7abra7/marian_stancik_2026
**VPS:** 188.245.224.189 (Hetzner — Caddy + subscriber API)

---

## What is this?

Single-page personal brand website for Marian Stancik — AI Agent Developer, Product Manager at Delta Defence, Law student at PF UK, Drone pilot, CEO of ASCENTIA s.r.o.

The site presents his unique combination of three domains: AI & Autonomous Agents, Law & AI Compliance, and Drones & UAV Systems. It's optimized for both human visitors and AI/LLM crawlers (JSON-LD, llms.txt).

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Pure HTML5/CSS3/JS (no framework) | Speed, simplicity, no build step |
| **3D Background** | Three.js v0.160.0 (CDN) | Neural network particle system |
| **Hosting** | GitHub (source) → Vercel (deploy) | Free tier, auto-deploy from git push |
| **Lead Capture** | Python WSGI + SQLite + Caddy on VPS | Email subscription webhook |
| **Email** | AgentMail (marian_stancik@agentmail.to) | Inbox for leads & notifications |
| **AI Accessibility** | llms.txt + JSON-LD + robots.txt | AI/LLM crawler discovery |

---

## Project Structure

```
/root/marian-stancik-web/
├── index.html          ← Main website (single-page, 36 KB)
├── profile.jpg         ← Profile photo from X/Twitter (15 KB)
├── llms.txt            ← AI agent context file (content summary for LLMs)
├── robots.txt          ← SEO: allow all + sitemap reference
├── sitemap.xml         ← SEO: all pages for Google Search Console
├── AUDIT.md            ← Web quality audit report (generated)
└── .gitignore          ← Git exclusion rules
```

---

## Development Principles

### TDD (Test-Driven Development)
Every function/feature must have tests before implementation. This project uses:
- **HTML validity:** W3C validator before each deploy
- **Link checks:** All external links verified working
- **Form testing:** Endpoint returns correct HTTP codes
- **Performance budget:** <100 KB total, <2s LCP

### AGENTS.md Rule
Every directory-level project MUST have an AGENTS.md file in its root with:
- Project description and purpose
- Tech stack and architecture
- Structure and file map
- Development conventions
- Deployment instructions
- Pitfalls and known issues

### Git Conventions
- Branch: `master` (default)
- Commit messages: emoji prefix + description
- No secrets ever committed (API keys, tokens, passwords)
- `.gitignore` updated for each new dependency

---

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Visitor     │────▶│  Vercel CDN  │────▶│  GitHub Repo │
│  (browser)   │     │  (static)    │     │  (source)    │
└──────┬───────┘     └──────────────┘     └──────────────┘
       │
       ├────────────────────────────────────────────────┐
       │  Lead form POST                                │
       ▼                                                ▼
┌──────────────┐                                ┌──────────────┐
│  Caddy (VPS) │────▶│  Python WSGI  │────▶│  SQLite DB   │
│  188.245.224 │      │  :8701        │      │  leads.db     │
└──────────────┘      └──────────────┘      └──────────────┘
                                                    │
                                                    ▼
                                           ┌──────────────┐
                                           │  AgentMail    │
                                           │  (notify)     │
                                           └──────────────┘
```

### Sections (from top to bottom)

1. **Navigation** — Fixed top bar with MS monogram logo + nav links
2. **Hero** — Profile photo, name, tagline, role badges, social links
3. **About** — Bio paragraphs + stat cards (9+ agents, 3 domains, €2.6M insurance, etc.)
4. **Expertise** — 3-card grid (AI Agents, Law & AI Compliance, Drones & UAV)
5. **Projects** — 4 project cards with links + tech tags
6. **Blog Preview** — 3 featured blog posts (placeholder until blog engine)
7. **Lead Capture** — Email subscription form → VPS webhook → SQLite
8. **Connect** — Social media links grid
9. **Footer** — Copyright, ASCENTIA link, email, source

---

## Deployment

### Production (Vercel)
```bash
git push origin master
# Vercel auto-deploys from GitHub
# Domain: https://marianstancik.dev
```

### Lead Capture Backend (VPS)
```bash
systemctl status hermes-subscriber   # Check service health
systemctl restart hermes-subscriber  # Restart after code changes
# Endpoint: http://188.245.224.189/api/subscribe
# Caddy reverse proxies :80/api/subscribe → :8701
```

### Naming Convention
All files: lowercase, no spaces. Profile images: `profile.jpg`, `banner.jpg`.
.md files for iPhone: UTF-8 BOM (0xEF 0xBB 0xBF) required.

---

## SEO & AI Optimization

| Feature | File | Purpose |
|---------|------|---------|
| JSON-LD Person | Inline in index.html | Schema.org structured data for Google + AI |
| JSON-LD WebSite | Inline in index.html | Schema.org site metadata |
| llms.txt | `/llms.txt` | AI crawler context (LLM.txt standard) |
| robots.txt | `/robots.txt` | Search engine crawl rules |
| sitemap.xml | `/sitemap.xml` | Google Search Console |
| Open Graph | Meta tags | Social sharing previews |
| Twitter Cards | Meta tags | X/Twitter link previews |

### Brand Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Background | `#08080F` | Near-black background |
| Text | `#E8E8F0` | Primary text color |
| Bronze | `#CD7F32` | Accent — headings, highlights, hover states |
| Bronze Light | `#E8B86D` | Secondary accent |
| Subtext | `#8888A0` | Secondary text, descriptions |
| Card BG | `#151520` | Card backgrounds |

---

## Performance Budget

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| HTML size | <40 KB | 36 KB | ✅ |
| Total page weight | <100 KB | ~50 KB | ✅ |
| LCP | <2.5s | ~1.2s | ✅ |
| CLS | <0.1 | ~0.02 | ✅ |
| INP | <200ms | ~50ms | ✅ |
| JavaScript | <150 KB | ~130 KB (Three.js CDN) | ✅ |
| External requests | <5 | 1 (Three.js CDN) | ✅ |

---

## Testing

### Manual checks before each deploy
```bash
# Check all links
grep -oP 'href="https?://[^"]*"' index.html | sort -u

# Check no broken forms  
grep -oP 'action="[^"]*"' index.html

# Check no secrets committed
grep -rn "api_key\|API_KEY\|secret\|token\|password" --include="*.html" --include="*.md"

# Validate HTML
curl -s -H "Content-Type: text/html" --data-binary @index.html "https://validator.w3.org/nu/?out=json"

# Check file sizes
find . -type f -name "*.html" -exec du -sh {} \;
```

### Form endpoint test
```bash
curl -s -X POST http://188.245.224.189/api/subscribe \
  -d "email=test@example.com"
# Expected: {"status": "ok", "email": "test@example.com"}
```

---

## Known Issues & Pitfalls

1. **HTTP form submission** — The lead form submits over HTTP (not HTTPS) because the VPS doesn't have a TLS domain. For production, set up a domain with Let's Encrypt on the VPS, or use a form service like Formspree.
2. **Three.js fallback** — If CDN is unreachable, the page still works (progressive enhancement). The 3D background is purely decorative.
3. **No blog engine yet** — Blog preview cards are static HTML. Need to implement a proper blog (Next.js/Hugo SSG).
4. **CSP restrictions** — CSP is set via meta tag. Some inline styles are blocked by strict CSP. Current config allows 'unsafe-inline' for styles.
5. **No analytics** — Plausible/Umami not yet installed. Consider adding once VPS is configured with a proper domain.
6. **profile.jpg** — JPEG format, 15 KB. Could be WebP for ~8 KB savings (affects LCP).

---

## Related Documents

| Document | Location |
|----------|----------|
| Brand strategy | `/opt/hermes-vault/01_OSOBNE/01_Profil/02-Brand-strategy.md` |
| Personal profile | `/opt/hermes-vault/01_OSOBNE/01_Profil/01-Marian-Stancik-profil.md` |
| Blog & Analytics plan | `/opt/hermes-vault/01_OSOBNE/01_Profil/03-Blog-Analytics-Strategy.md` |
| Web audit report | `./AUDIT.md` |
| Hermes coder profile | `/root/.hermes/profiles/coder/AGENTS.md` |

---

## Quick Commands

| Action | Command |
|--------|---------|
| Deploy | `git push origin master` |
| Test form | `curl -X POST http://188.245.224.189/api/subscribe -d "email=test@example.com"` |
| Check service | `systemctl status hermes-subscriber` |
| Restart service | `systemctl restart hermes-subscriber` |
| View logs | `journalctl -u hermes-subscriber -n 50 --no-pager` |
| Check leads | `sqlite3 /opt/hermes-vault/leads.db "SELECT * FROM leads ORDER BY subscribed_at DESC"` |
| Reload Caddy | `systemctl reload caddy` |
| Verify HTML | `curl -s -H "Content-Type: text/html" --data-binary @index.html "https://validator.w3.org/nu/?out=json"` |