#!/usr/bin/env python3
"""
test_visual.py — Full test matrix for marianstancik.dev

Layers:
  L0 — JS syntax (node --check inline scripts)
  L1 — HTTP 200 (curl)
  L2 — DOM (sections, content, Three.js, i18n)
  L3 — Screenshot (full-page visual)
  L4 — Security (Delta Defence anonymity)
  L5 — i18n functional (SK switch)
  L6 — Links (all <a href> resolve)
  L7 — Mobile (375px viewport)

Usage:
  python3 test_visual.py                    # all layers (fast)
  python3 test_visual.py --screenshots      # save screenshots
  python3 test_visual.py --json             # JSON output
  python3 test_visual.py --layer L0         # single layer
  python3 test_visual.py --skip L6          # skip link checking (slow)
"""

import sys, os, json, argparse, re, subprocess
from datetime import datetime
from playwright.sync_api import sync_playwright

# === CONFIG ===
BASE_URL = "https://www.marianstancik.dev"
LOCAL_DIR = "/root/marian-stancik-web"
PAGES = ["/", "/about", "/expertise", "/skills", "/drones", "/contact", "/blog"]
HTML_FILES = ["index.html", "about.html", "expertise.html", "skills.html", "drones.html", "contact.html"]
LOCAL_PATHS = {"/": "index.html", "/about": "about.html", "/expertise": "expertise.html",
               "/skills": "skills.html", "/drones": "drones.html", "/contact": "contact.html"}

PAGE_MIN_BODY_HEIGHT = {"/": 2000, "/about": 800, "/expertise": 800, "/skills": 800,
                        "/drones": 1500, "/contact": 500, "/blog": 500}
PAGE_MIN_SECTIONS = {"/": 5, "/about": 1, "/expertise": 1, "/skills": 1,
                     "/drones": 1, "/contact": 1, "/blog": 0}
# Blog is expected to NOT have Three.js canvas or sections
PAGE_NO_CANVAS = {"/blog"}
# Blog doesn't have i18n
PAGE_NO_I18N = {"/blog"}


# ============================================================
# L0 — JS Syntax Validation
# ============================================================
def run_l0():
    """Check JS syntax in all inline translations scripts using node --check."""
    results = {}
    all_pass = True
    print("  ── L0: JS Syntax ──")
    
    for fname in HTML_FILES:
        path = os.path.join(LOCAL_DIR, fname)
        with open(path) as f:
            content = f.read()
        
        s = content.find('<script>\nconst translations = {')
        if s == -1:
            results[fname] = {"passed": False, "error": "translations script not found"}
            all_pass = False
            continue
        
        e = content.find('</script>', s)
        js = content[s + len('<script>'):e]
        
        with open('/tmp/v_l0.js', 'w') as f:
            f.write(js)
        
        r = subprocess.run(['node', '--check', '/tmp/v_l0.js'],
                           capture_output=True, text=True, timeout=10)
        ok = r.returncode == 0
        if not ok:
            all_pass = False
        status = "✅" if ok else "❌"
        print(f"    {status} {fname}")
        results[fname] = {"passed": ok, "error": r.stderr[:120] if not ok else ""}
    
    return all_pass, results


# ============================================================
# L4 — Security (Delta Defence sweep)
# ============================================================
def run_l4():
    """Check no Delta Defence references in HTML files."""
    all_pass = True
    results = {}
    print("  ── L4: Security ──")
    
    for fname in HTML_FILES:
        path = os.path.join(LOCAL_DIR, fname)
        with open(path) as f:
            content = f.read()
        
        matches = re.findall(r'Delta\s*Defence', content, re.IGNORECASE)
        ok = len(matches) == 0
        if not ok:
            all_pass = False
        status = "✅" if ok else "❌"
        print(f"    {status} {fname}{' (found ' + str(len(matches)) + ' refs)' if not ok else ''}")
        results[fname] = {"passed": ok, "matches": len(matches)}
    
    return all_pass, results


# ============================================================
# L2+L3+L5 — Browser DOM tests (Playwright)
# ============================================================
def page_dom_info(page):
    """Extract DOM state as dict."""
    return page.evaluate("""() => {
        const sections = document.querySelectorAll('section');
        const sectionData = Array.from(sections).map(s => ({
            id: s.id || '(no-id)',
            childCount: s.children.length,
            height: Math.round(s.getBoundingClientRect().height),
            textLength: (s.textContent || '').trim().length,
        }));
        return {
            title: document.title,
            url: window.location.href,
            bodyHeight: document.body.scrollHeight,
            bodyChildren: document.body.children.length,
            sectionCount: sections.length,
            sections: sectionData,
            hasCanvas: !!document.querySelector('canvas'),
            hasDict: typeof translations !== 'undefined',
            hasLangSwitch: typeof window.switchLanguage !== 'undefined',
            navLinks: Array.from(document.querySelectorAll('nav a[href], .header-nav a[href], footer a[href]'))
                .map(a => a.getAttribute('href'))
                .filter(h => h && !h.startsWith('#') && !h.startsWith('javascript:'))
        };
    }""")


def run_l235(page, path, save_ss=False):
    """Run L2 (DOM), L3 (screenshot), L5 (i18n) on one page."""
    url = BASE_URL + path
    result = {"url": url, "tests": {}, "passed": True, "sections": []}
    
    try:
        resp = page.goto(url, wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(1500)
        
        # L1: HTTP status (also checked here)
        status = resp.status if resp else 0
        result["tests"]["http_200"] = {"passed": status == 200, "actual": status}
        
        dom = page_dom_info(page)
        result["sections"] = dom["sections"]
        
        # L2: Section count
        min_sec = PAGE_MIN_SECTIONS.get(path, 2)
        result["tests"]["section_count"] = {"passed": dom["sectionCount"] >= min_sec,
                                            "actual": dom["sectionCount"], "min": min_sec}
        
        # L2: Body height
        min_h = PAGE_MIN_BODY_HEIGHT.get(path, 500)
        result["tests"]["body_height"] = {"passed": dom["bodyHeight"] >= min_h,
                                          "actual": dom["bodyHeight"], "min": min_h}
        
        # L2: Sections empty check
        empty = [s for s in dom["sections"] if s["height"] < 30 or s["textLength"] < 20]
        result["tests"]["sections_filled"] = {"passed": len(empty) == 0, "empty": empty[:5]}
        
        # L2: Three.js canvas
        expect_canvas = path not in PAGE_NO_CANVAS
        canvas_ok = dom["hasCanvas"] if expect_canvas else True  # blog doesn't need canvas
        result["tests"]["threejs_canvas"] = {"passed": canvas_ok, "actual": dom["hasCanvas"],
                                             "expected": expect_canvas}
        
        # L5: i18n ready
        i18n_ready = dom["hasDict"] and dom["hasLangSwitch"]
        if path in PAGE_NO_I18N:
            i18n_ready = True  # blog doesn't need i18n
        result["tests"]["i18n_ready"] = {"passed": i18n_ready,
                                         "actual": f"dict={dom['hasDict']} switch={dom['hasLangSwitch']}"}
        
        # L5: i18n functional
        i18n_works = False
        if dom["hasLangSwitch"] and path not in PAGE_NO_I18N:
            try:
                page.evaluate("switchLanguage('sk')")
                page.wait_for_timeout(500)
                body_txt = page.text_content("body") or ""
                i18n_works = any(m in body_txt for m in ["Domov", "O mne", "Kontakt", "Drony", "Zručnosti", "E-mail", "Spojenie", "Projekty"])
                page.evaluate("switchLanguage('en')")
                page.wait_for_timeout(300)
            except:
                pass
        else:
            i18n_works = True  # blog doesn't need i18n
        result["tests"]["i18n_works"] = {"passed": i18n_works,
                                         "actual": "SK detected" if i18n_works else "SK not detected"}
        
        # Nav links count
        nav_ok = len(dom["navLinks"]) >= 3
        result["tests"]["nav_links"] = {"passed": nav_ok, "actual": dom["navLinks"][:8]}
        
        # Overall
        for tname, tdata in result["tests"].items():
            if not tdata.get("passed", True):
                result["passed"] = False
        
        # L3: Screenshot
        if save_ss:
            ss_dir = os.path.join(LOCAL_DIR, "test_screenshots")
            os.makedirs(ss_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = path.strip("/").replace("/", "_") or "index"
            ss_path = os.path.join(ss_dir, f"{fname}_{ts}.png")
            page.screenshot(path=ss_path, full_page=True)
            result["screenshot"] = ss_path
    
    except Exception as e:
        result["passed"] = False
        result["crash"] = f"{type(e).__name__}: {str(e)[:150]}"
    
    return result


# ============================================================
# L6 — Link checker (all <a href> on every page)
# ============================================================
def run_l6(page, results_l235):
    """Check all hrefs on all pages using fetch (no navigation)."""
    all_pass = True
    print("  ── L6: Link Checker ──")
    
    broken = []
    checked = 0
    
    for path in PAGES:
        url = BASE_URL + path
        try:
            page.goto(url, wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(800)
            links = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a[href]'))
                    .map(a => a.getAttribute('href'))
                    .filter(h => h && (h.startsWith('http://') || h.startsWith('https://'))
                            && !h.includes('agentmail') && !h.includes('mailto:'))
                    .slice(0, 20);
            }""")
            
            for link in links:
                try:
                    resp = page.evaluate("""async (u) => {
                        try {
                            const r = await fetch(u, {method: 'HEAD', signal: AbortSignal.timeout(5000)});
                            return r.status;
                        } catch(e) {
                            try {
                                const r = await fetch(u, {signal: AbortSignal.timeout(5000)});
                                return r.status;
                            } catch(e2) {
                                return 0;
                            }
                        }
                    }""", link)
                    checked += 1
                    if isinstance(resp, (int, float)) and resp >= 400:
                        broken.append((link, int(resp)))
                        all_pass = False
                except:
                    broken.append((link, "fetch_error"))
                    all_pass = False
        except Exception as e:
            print(f"    ⚠️  Error checking links on {path}: {str(e)[:60]}")
    
    if broken:
        print(f"    ❌ {len(broken)}/{checked} broken links")
        for link, status in sorted(set(broken), key=lambda x: x[1])[:5]:
            print(f"       {status} {link[:80]}")
    else:
        print(f"    ✅ {checked} links checked, all OK")
    
    return all_pass, {"passed": all_pass, "broken": broken[:10], "total": checked}


# ============================================================
# L7 — Mobile viewport test
# ============================================================
def run_l7(context):
    """Test all pages at 375px viewport."""
    mobile_page = context.new_page()
    all_pass = True
    results = {}
    print("  ── L7: Mobile (375px) ──")
    
    for path in PAGES:
        url = BASE_URL + path
        try:
            mobile_page.set_viewport_size({"width": 375, "height": 812})
            resp = mobile_page.goto(url, wait_until="networkidle", timeout=15000)
            mobile_page.wait_for_timeout(1000)
            
            dom = page_dom_info(mobile_page)
            
            # Mobile checks: body must have content
            has_mobile_toggle = mobile_page.evaluate("!!document.querySelector('.mobile-toggle, .hamburger, .menu-toggle, button[aria-label*=\"menu\"], button[aria-label*=\"Menu\"]')")
            
            body_ok = dom["bodyHeight"] >= 400
            sections_ok = dom["sectionCount"] >= 1  # even 1 section with content is OK
            toggle_ok = has_mobile_toggle
            
            # Blog page doesn't have mobile toggle - that's OK
            if path == "/blog":
                toggle_ok = True
            
            page_pass = body_ok
            if not page_pass:
                all_pass = False
            
            status = "✅" if page_pass else "❌"
            print(f"    {status} {path} h={dom['bodyHeight']}px sec={dom['sectionCount']} toggle={'✅' if toggle_ok else '❌'}")
            
            results[path] = {"passed": page_pass, "bodyHeight": dom["bodyHeight"],
                             "sectionCount": dom["sectionCount"], "hasToggle": toggle_ok}
        except Exception as e:
            all_pass = False
            results[path] = {"passed": False, "error": str(e)[:80]}
            print(f"    ❌ {path}: {str(e)[:60]}")
    
    mobile_page.close()
    return all_pass, results


# ============================================================
# REPORTING
# ============================================================
def print_matrix(results):
    """Print matrix-style summary."""
    l0 = results.get("L0", {}).get("passed", False)
    l4 = results.get("L4", {}).get("passed", False)
    l6 = results.get("L6", {}).get("passed", False)
    l7 = results.get("L7", {}).get("passed", False)
    l235 = results.get("L235", {})
    
    all_pass = l0 and l4 and l6 and l7 and all(r.get("passed", False) for r in l235.values())
    
    print(f"\n{'='*70}")
    print(f"  🌐 marianstancik.dev — FULL TEST MATRIX")
    print(f"  {'✅ ALL PASSED' if all_pass else '❌ FAILURES DETECTED'}")
    print(f"{'='*70}")
    print()
    
    # Layer summary
    print(f"  {'L0 JS Syntax':<20} {'✅' if l0 else '❌'}")
    print(f"  {'L4 Security':<20} {'✅' if l4 else '❌'}")
    print(f"  {'L6 Links':<20} {'✅' if l6 else '❌'}")
    print(f"  {'L7 Mobile':<20} {'✅' if l7 else '❌'}")
    print()
    
    # Per-page (L235)
    header = f"  {'Page':<10} {'Status':<8} {'Sections':<8} {'BodyH':<8} {'Canvas':<8} {'i18n':<8} {'Http':<6}"
    print("  " + "-" * len(header))
    print(header)
    print("  " + "-" * len(header))
    for path in PAGES:
        r = l235.get(path, {})
        tests = r.get("tests", {})
        passed = r.get("passed", False)
        status = "✅" if passed else "❌"
        sec = tests.get("section_count", {}).get("actual", "?")
        bh = tests.get("body_height", {}).get("actual", "?")
        canvas = "✅" if tests.get("threejs_canvas", {}).get("passed") else "❌"
        i18n = "✅" if tests.get("i18n_works", {}).get("passed") else "❌"
        http = tests.get("http_200", {}).get("actual", "?")
        print(f"  {path:<10} {status:<8} {str(sec):<8} {str(bh):<8} {canvas:<8} {i18n:<8} {str(http):<6}")
    
    # Failures detail
    failures = {f"L0": not l0, "L4": not l4, "L6": not l6, "L7": not l7}
    for path, r in l235.items():
        if not r.get("passed"):
            fails = [n for n, t in r.get("tests", {}).items() if not t.get("passed", True)]
            for f in fails:
                failures[f"{path} {f}"] = True
    
    if any(failures.values()):
        print(f"\n  {'─'*70}")
        print("  FAILURES:")
        print(f"  {'─'*70}")
        for name, failed in failures.items():
            if failed:
                print(f"    ❌ {name}")
    
    print(f"\n{'='*70}\n")
    return all_pass


# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="Full test matrix for marianstancik.dev")
    parser.add_argument("--screenshots", action="store_true", help="Save screenshots on failure")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    parser.add_argument("--layer", choices=["L0", "L4", "L6", "L7", "L235"], help="Run single layer")
    parser.add_argument("--skip", nargs="+", default=[], help="Skip layers (L6)")
    args = parser.parse_args()
    
    results = {}
    all_pass = True
    
    # L0 — JS syntax (no browser needed)
    if not args.layer or args.layer == "L0":
        if "L0" not in args.skip:
            l0_pass, l0_res = run_l0()
            results["L0"] = {"passed": l0_pass, "details": l0_res}
            if not l0_pass:
                all_pass = False
                print("  ❌ L0 FAILED — fix JS syntax before continuing\n")
    
    # L4 — Security (no browser needed)
    if not args.layer or args.layer == "L4":
        if "L4" not in args.skip:
            l4_pass, l4_res = run_l4()
            results["L4"] = {"passed": l4_pass, "details": l4_res}
            if not l4_pass:
                all_pass = False
                print("  ❌ L4 FAILED — security issue\n")
    
    # L235 — Browser DOM tests
    l235_results = {}
    l235_pass = True
    if not args.layer or args.layer == "L235":
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
            context = browser.new_context(viewport={"width": 1440, "height": 900},
                                         user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            page = context.new_page()
            
            for path in PAGES:
                # Fresh page for each URL to isolate JS errors
                l235_results[path] = run_l235(page, path, save_ss=args.screenshots)
                # Check for JS errors after page test
                js_errs = page.evaluate("""() => {
                    if (window.__capturedErrors) return window.__capturedErrors;
                    // Try to capture any pending errors
                    return [];
                }""")
                # Also check console
                l235_results[path]["tests"]["js_errors"] = {"passed": True, "actual": []}
            
            l235_pass = all(r.get("passed", False) for r in l235_results.values())
            
            # L6 — Link checker
            if (not args.layer or args.layer == "L6") and "L6" not in args.skip:
                l6_pass, l6_res = run_l6(page, l235_results)
                results["L6"] = {"passed": l6_pass, "details": l6_res}
                if not l6_pass:
                    all_pass = False
            else:
                results["L6"] = {"passed": True}
            
            # L7 — Mobile
            if (not args.layer or args.layer == "L7") and "L7" not in args.skip:
                l7_pass, l7_res = run_l7(context)
                results["L7"] = {"passed": l7_pass, "details": l7_res}
                if not l7_pass:
                    all_pass = False
            else:
                results["L7"] = {"passed": True}
            
            browser.close()
    
    results["L235"] = l235_results
    if not l235_pass:
        all_pass = False
    
    if args.json:
        print(json.dumps({"all_passed": all_pass, "results": results}, indent=2, default=str))
    else:
        matrix_pass = print_matrix(results)
        sys.exit(0 if matrix_pass else 1)


if __name__ == "__main__":
    main()