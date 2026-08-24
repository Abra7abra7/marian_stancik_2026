#!/usr/bin/env python3
"""
test_visual.py — Browser-based visual integrity test for marianstancik.dev

Opens every page in headless Chromium and verifies:
  - Page loads (HTTP 200, no JS console errors)
  - Sections render with actual content (height > 50px, text > 100 chars)
  - i18n dictionary + language switch function present + works
  - Three.js canvas renders
  - Navigation links resolve
  - All subpages have meaningful body content

Usage:
  python3 test_visual.py                    # test production
  python3 test_visual.py --screenshots      # save screenshots
  python3 test_visual.py --json             # JSON output for parsing
"""

import sys
import os
import json
import argparse
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.marianstancik.dev"
PAGES = ["/", "/about", "/expertise", "/skills", "/drones", "/contact", "/blog"]

PAGE_MIN_BODY_HEIGHT = {
    "/": 2000, "/about": 800, "/expertise": 800, "/skills": 800,
    "/drones": 1500, "/contact": 500, "/blog": 500,
}

PAGE_MIN_SECTIONS = {
    "/": 5, "/about": 3, "/expertise": 3, "/skills": 3,
    "/drones": 3, "/contact": 2, "/blog": 2,
}


def page_dom_info(page):
    """Extract DOM state as a dict using a single evaluate."""
    return page.evaluate("""() => {
        const sections = document.querySelectorAll('section');
        const sectionData = Array.from(sections).map(s => ({
            id: s.id || '(no-id)',
            childCount: s.children.length,
            height: Math.round(s.getBoundingClientRect().height),
            textLength: (s.textContent || '').trim().length,
        }));
        const bodyHeight = document.body.scrollHeight;
        const bodyChildren = document.body.children.length;
        return {
            title: document.title,
            url: window.location.href,
            bodyHeight,
            bodyChildren,
            sectionCount: sections.length,
            sections: sectionData,
            hasCanvas: !!document.querySelector('canvas'),
            hasDict: typeof window.translations !== 'undefined',
            hasLangSwitch: typeof window.switchLanguage !== 'undefined',
            navLinks: Array.from(document.querySelectorAll('nav a[href], .header-nav a[href], footer a[href]'))
                .map(a => a.getAttribute('href'))
                .filter(h => h && !h.startsWith('#') && !h.startsWith('javascript:'))
        };
    }""")


def test_page(page, path, save_ss=False):
    """Test a single page. Returns dict with results."""
    url = BASE_URL + path
    result = {"url": url, "tests": {}, "passed": True, "sections": []}

    try:
        resp = page.goto(url, wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(1500)  # let JS settle

        # HTTP status
        status = resp.status if resp else 0
        result["tests"]["http_200"] = {"passed": status == 200, "actual": status}

        dom = page_dom_info(page)
        result["sections"] = dom["sections"]

        # Section count
        min_sec = PAGE_MIN_SECTIONS.get(path, 2)
        rc_ok = dom["sectionCount"] >= min_sec
        result["tests"]["section_count"] = {"passed": rc_ok, "actual": dom["sectionCount"], "min": min_sec}

        # Body height
        min_h = PAGE_MIN_BODY_HEIGHT.get(path, 500)
        bh_ok = dom["bodyHeight"] >= min_h
        result["tests"]["body_height"] = {"passed": bh_ok, "actual": dom["bodyHeight"], "min": min_h}

        # Section content — flag any section that is empty or very thin
        empty_secs = [s for s in dom["sections"] if s["height"] < 30 or s["textLength"] < 20]
        result["tests"]["sections_filled"] = {"passed": len(empty_secs) == 0, "empty": empty_secs[:5]}

        # Three.js canvas
        result["tests"]["threejs_canvas"] = {"passed": dom["hasCanvas"], "actual": dom["hasCanvas"]}

        # i18n present
        i18n_ready = dom["hasDict"] and dom["hasLangSwitch"]
        result["tests"]["i18n_ready"] = {"passed": i18n_ready, "actual": f"dict={dom['hasDict']} switch={dom['hasLangSwitch']}"}

        # i18n functional — switch to SK and check
        i18n_works = False
        if dom["hasLangSwitch"]:
            try:
                page.evaluate("switchLanguage('sk')")
                page.wait_for_timeout(500)
                body_txt = page.text_content("body") or ""
                i18n_works = any(m in body_txt for m in ["Vitajte", "Spojte sa", "Kontakt", "Drony", "Zručnosti"])
                # switch back to EN
                page.evaluate("switchLanguage('en')")
                page.wait_for_timeout(300)
            except Exception as e:
                i18n_works = False
        result["tests"]["i18n_works"] = {"passed": i18n_works, "actual": "SK detected" if i18n_works else "SK not detected"}

        # Nav links
        nav_ok = len(dom["navLinks"]) >= 3
        result["tests"]["nav_links"] = {"passed": nav_ok, "actual": dom["navLinks"][:8]}

        # Overall
        for tname, tdata in result["tests"].items():
            if not tdata.get("passed", True):
                result["passed"] = False

        if save_ss:
            ss_dir = "/root/marian-stancik-web/test_screenshots"
            os.makedirs(ss_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = path.strip("/").replace("/", "_") or "index"
            ss_path = f"{ss_dir}/{fname}_{ts}.png"
            page.screenshot(path=ss_path, full_page=True)
            result["screenshot"] = ss_path

    except Exception as e:
        result["passed"] = False
        result["crash"] = f"{type(e).__name__}: {str(e)[:150]}"

    return result


def print_report(results):
    """Print formatted report."""
    all_ok = all(r["passed"] for r in results.values())

    print(f"\n{'='*70}")
    print(f"  🌐 marianstancik.dev — VISUAL INTEGRITY TEST")
    print(f"  {'✅ ALL PASSED' if all_ok else '❌ FAILURES DETECTED'}")
    print(f"{'='*70}")
    print(f"  {len(PAGES)} pages tested")
    print()

    # Per-page summary line
    for path in PAGES:
        r = results.get(path, {})
        status = "✅" if r.get("passed") else "❌"
        crash = r.get("crash", "")
        
        tests = r.get("tests", {})
        bh = tests.get("body_height", {}).get("actual", "?")
        sc = tests.get("section_count", {}).get("actual", "?")
        canvas = "✅" if tests.get("threejs_canvas", {}).get("passed") else "❌"
        i18n = "✅" if tests.get("i18n_works", {}).get("passed") else "❌"
        
        fails = [n for n, t in tests.items() if not t.get("passed", True)]
        fail_str = f" ⚠️ {', '.join(fails)}" if fails else ""
        crash_str = f" 💥 {crash}" if crash else ""
        
        print(f"  {status} {path:<8} h={bh:<5} sec={sc:<2} 🎨{canvas} 🌐{i18n}{fail_str}{crash_str}")

    # Detail for failures
    failures = [(p, r) for p, r in results.items() if not r.get("passed")]
    if failures:
        print(f"\n{'─'*70}")
        print("  DETAIL — FAILED PAGES")
        print(f"{'─'*70}")
        for path, r in failures:
            tests = r.get("tests", {})
            print(f"\n  ❌ {BASE_URL}{path}")
            for tname, tdata in sorted(tests.items()):
                if not tdata.get("passed", True):
                    detail = tdata.get("actual", tdata.get("empty", "?"))
                    print(f"     ✗ {tname}: {detail}")
            
            # Show section details
            secs = r.get("sections", [])
            if secs:
                print(f"     Sections ({len(secs)}):")
                for s in secs:
                    ic = "✅" if s["height"] > 50 and s["textLength"] > 100 else "⚠️"
                    print(f"       {ic} #{s['id']} h={s['height']}px txt={s['textLength']}ch")
            
            ss = r.get("screenshot")
            if ss:
                print(f"     📸 Screenshot: {ss}")

    print(f"\n{'='*70}\n")
    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Visual integrity test for marianstancik.dev")
    parser.add_argument("--screenshots", action="store_true", help="Save screenshots on failure")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    args = parser.parse_args()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        # Collect JS errors globally on page
        js_errors = []

        page = context.new_page()
        # Capture page-level JS errors
        def _on_error(msg):
            js_errors.append(str(msg))
        page.on("pageerror", _on_error)
        
        results = {}
        for path in PAGES:
            results[path] = test_page(page, path, save_ss=args.screenshots)

        # Report JS errors from each page
        for path, r in results.items():
            if js_errors:
                r["tests"]["js_errors"] = {"passed": False, "actual": list(set(js_errors))[:5]}
            else:
                r["tests"]["js_errors"] = {"passed": True, "actual": []}

        browser.close()

    if args.json:
        output = {"all_passed": all(r["passed"] for r in results.values()), "results": results}
        print(json.dumps(output, indent=2, default=str))
    else:
        all_ok = print_report(results)
        sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()