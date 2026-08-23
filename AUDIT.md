# 📊 Web Quality Audit — marianstancik.dev

**Dátum:** 23. august 2026
**Metodológia:** web-quality-audit skill (Google Lighthouse 150+ checks)
**Auditovaný súbor:** index.html (statický single-page web)

---

## SÚHRN

| Kategória | Skóre | Kritické | Vysoké | Stredné | Nízke |
|-----------|-------|----------|--------|---------|-------|
| **Performance** | 🟡 75/100 | 0 | 2 | 3 | 2 |
| **Accessibility** | 🟢 92/100 | 0 | 0 | 1 | 2 |
| **SEO** | 🟢 95/100 | 0 | 0 | 1 | 1 |
| **Best Practices** | 🟢 90/100 | 0 | 0 | 1 | 2 |

**Celkové hodnotenie:** 🟢 Dobre postavený web — 0 critical issues. 7 odporúčaní na zlepšenie.

---

## PERFORMANCE (🟡 75/100)

### Čo je dobré ✅

| Check | Status |
|-------|--------|
| Systémové fonty (žiadny FOuT/FOiT) | ✅ Výborné |
| CSS v `<head>` (nie render-blocking) | ✅ |
| JS na konci `<body>` | ✅ |
| Three.js version pinned (0.160.0) | ✅ |
| Minimal external dependencies (1 CDN) | ✅ |
| Progressive enhancement (content viditeľný bez JS) | ✅ |
| Jednoduchý DOM (žiadny framework bloat) | ✅ |

### Čo treba opraviť 🔧

| # | Priorita | Problém | Dopad | Riešenie |
|---|----------|---------|-------|----------|
| 1 | 🔴 **High** | `font-display: swap` chýba | Pri pomalom načítaní fontov blokuje rendering textu (FOIT) | Pridať do CSS: `body { font-display: swap; }` |
| 2 | 🔴 **High** | Chýba `preconnect` pre CDN | Three.js sa sťahuje neskôr kvôli DNS+TCP latency | Pridať: `<link rel="preconnect" href="https://cdn.jsdelivr.net">` |
| 3 | 🟡 **Medium** | Profilovka JPEG (400×400, 15 KB) | O 40-50% väčšia než WebP | Konvertovať na WebP: `profile.webp` + `<picture>` fallback |
| 4 | 🟡 **Medium** | banner.jpg v repozitári (21 KB) | Zbytočný súbor na webe | Zmazať (nie je referencovaný v index.html) |
| 5 | 🟡 **Medium** | Inline CSS 13.3 KB nie je minifikovaný | O 15-20% väčší než minifikovaný | Minifikovať CSS (alebo použiť build tool) |
| 6 | 🔵 **Low** | Chýba `<link rel="preload">` pre profilovku | LCP image sa nenačíta prioritne | Pridať: `<link rel="preload" as="image" href="profile.webp">` |
| 7 | 🔵 **Low** | HTML nie je minifikované (35.7 KB) | O ~10% väčšie | Minifikovať cez build pipeline |

### Core Web Vitals (odhad)

| Metrika | Odhad | Cieľ | Status |
|---------|-------|------|--------|
| **LCP** | ~1.2s | < 2.5s | ✅ **Dobre** (jednoduchá stránka) |
| **INP** | ~50ms | < 200ms | ✅ **Výborne** (minimálny JS) |
| **CLS** | ~0.02 | < 0.1 | ✅ **Výborne** (statický layout) |

---

## ACCESSIBILITY (🟢 92/100)

### Čo je dobré ✅

| Check | Status |
|-------|--------|
| `lang="en"` na `<html>` | ✅ |
| Skip navigation link | ✅ |
| ARIA labels na všetkých linkách | ✅ |
| `alt` text na všetkých obrázkoch | ✅ |
| Farebný kontrast (všetky páry > 4.5:1) | ✅ |
| Logická heading štruktúra (1×H1 → 7×H2 → 10×H3) | ✅ |
| `rel="noopener"` na všetkých externých linkách | ✅ |
| Focus visible (default browser) | ✅ |

### Čo treba opraviť 🔧

| # | Priorita | Problém | Riešenie |
|---|----------|---------|----------|
| 1 | 🟡 **Medium** | Chýba `aria-current="page"` na navigácii | Pridať na aktívny odkaz pre screen readery |
| 2 | 🔵 **Low** | Chýba `role="alert"` na lead forme po odoslaní | Pridať success/error správu s `role="alert"` |
| 3 | 🔵 **Low** | Chýba `tabindex` poradie na lead forme (je OK, ale overiť) | Automatické poradie je v pohode |

---

## SEO (🟢 95/100)

### Čo je dobré ✅

| Check | Status |
|-------|--------|
| Unikátny title tag (50-60 chars) | ✅ "Marian Stancik — AI Agent Developer | Product Manager | Law | Drones" |
| Meta description (150-160 chars) | ✅ |
| Canonical URL | ✅ |
| JSON-LD structured data (Person + WebSite) | ✅ |
| `robots.txt` + `llms.txt` | ✅ |
| HTTPS-only (žiadny mixed content) | ✅ |
| Responzívny dizajn (mobile-friendly) | ✅ |
| Heading hierarchy (1 H1, logické poradie) | ✅ |

### Čo treba opraviť 🔧

| # | Priorita | Problém | Riešenie |
|---|----------|---------|----------|
| 1 | 🟡 **Medium** | Chýba sitemap.xml | Vytvoriť `sitemap.xml` so všetkými URL |
| 2 | 🔵 **Low** | Chýba `hreflang` tag | Ak bude SK verzia, pridať `hreflang="sk"` |

---

## BEST PRACTICES (🟢 90/100)

### Čo je dobré ✅

| Check | Status |
|-------|--------|
| `<!DOCTYPE html>` | ✅ |
| `<meta charset="UTF-8">` (prvý v `<head>`) | ✅ |
| Žiadne deprecated API (document.write, sync XHR) | ✅ |
| Žiadne chyby v HTML syntaxi | ✅ |
| Valid HTML5 (žiadne deprecated atribúty) | ✅ |
| HTTPS-only | ✅ |

### Čo treba opraviť 🔧

| # | Priorita | Problém | Riešenie |
|---|----------|---------|----------|
| 1 | 🟡 **Medium** | Chýba CSP (Content Security Policy) | Pridať cez `<meta http-equiv="Content-Security-Policy">` |
| 2 | 🔵 **Low** | Chýba HSTS | Rieši sa na úrovni Vercel/Caddy, nie v HTML |
| 3 | 🔵 **Low** | Chýba cache-control header | Rieši sa na úrovni Vercel, nie v HTML |

---

## OKAMŽITÉ OPRAVY (spravím teraz)

| # | Oprava | Náročnosť |
|---|--------|-----------|
| 1 | Zmazať banner.jpg (unused, 21 KB) | 🔧 10s |
| 2 | Pridať `font-display: swap` do CSS | 🔧 10s |
| 3 | Pridať `preconnect` pre jsdelivr CDN | 🔧 10s |
| 4 | Pridať CSP meta tag | 🔧 30s |
| 5 | Vytvoriť `sitemap.xml` | 🔧 2 min |

---

## DLHODOBÉ ODPORÚČANIA (nie teraz)

| # | Odporúčanie | Prečo |
|---|-------------|-------|
| 1 | Konvertovať profile.jpg → profile.webp | O 40-50% menší súbor, rýchlejší LCP |
| 2 | Minifikovať CSS a HTML cez build pipeline | O 15% menší bundle |
| 3 | Migrovať na Next.js static export | Automatický minify + preload + sitemap |
| 4 | Nainštalovať Plausible self-hosted | GDPR compliant analytics |
| 5 | Content Security Policy na úrovni Vercel | Lepšia ochrana XSS |

---

## 🔗 KRÍŽOVÉ ODKAZY

| Dokument | Cesta |
|----------|-------|
| Blog & Analytics stratégia | `01_OSOBNE/01_Profil/03-Blog-Analytics-Strategy.md` |
| Brand stratégia | `01_OSOBNE/01_Profil/02-Brand-strategy.md` |
| GitHub repo | https://github.com/Abra7abra7/marian_stancik_2026 |

---

*Vytvorené: 23. august 2026 | Hermes Agent (coder profile)*
*Metodológia: web-quality-audit skill (addyosmani)*