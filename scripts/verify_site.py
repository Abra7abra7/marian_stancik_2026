#!/usr/bin/env python3
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    pages = [
        'index.html',
        'about.html',
        'expertise.html',
        'skills.html',
        'drones.html',
        'contact.html',
        'blog/index.html'
    ]

    print("========================================")
    print(" 1. SECURITY & ANONYMIZATION (L4 SWEEP)")
    print("========================================")
    found_sec = False
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith(('.html', '.md', '.js', '.txt', '.json', '.xml')) and file not in ['AGENTS.md', 'test_visual.py', 'verify_site.py']:
                p = os.path.join(root, file)
                with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = re.findall(r'Delta\s*Defence', content, re.IGNORECASE)
                    if matches:
                        print(f"❌ Security violation in {p}: {matches}")
                        found_sec = True
    if not found_sec:
        print("✅ L4 Security Sweep passed (0 forbidden company names found)")

    print("\n========================================")
    print(" 2. JS SYNTAX CHECK (L0)")
    print("========================================")
    for js_file in ['js/i18n.js', 'js/three-bg.js']:
        if os.path.exists(js_file):
            r = subprocess.run(['node', '--check', js_file], capture_output=True, text=True)
            if r.returncode == 0:
                print(f"✅ {js_file}: Syntax OK")
            else:
                print(f"❌ {js_file}: Syntax error:\n{r.stderr}")

    print("\n========================================")
    print(" 3. HTML META & LINK INTEGRITY CHECK")
    print("========================================")
    all_pages_ok = True
    for p in pages:
        if not os.path.exists(p):
            print(f"❌ Missing page file: {p}")
            all_pages_ok = False
            continue
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        errors = []
        if 'OG_<title>' in c or 'OG_<meta' in c:
            errors.append('Found malformed OG_ tags')
        if 'https://www.marianstancik.devabout' in c or 'https://www.marianstancik.devexpertise' in c:
            errors.append('Found malformed URL in JSON-LD')
        if 'href="blog/index.html"' in c:
            errors.append('Found relative blog/index.html link')
        if 'class="skip-link"' not in c and p != 'blog/index.html':
            errors.append('Missing skip-link')
        if 'rel="alternate" type="text/plain" href="/llms.txt"' not in c:
            errors.append('Missing llms.txt discovery link')

        if errors:
            print(f"❌ {p}: {errors}")
            all_pages_ok = False
        else:
            print(f"✅ {p}: All checks passed")

    print("\n========================================")
    print(" 4. DESIGN TOKENS & CSS VALIDATION")
    print("========================================")
    with open('css/main.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    if ':root' in css_content and '--color-primary' in css_content and '--font-body' in css_content:
        print("✅ css/main.css: :root Design Tokens present")
    else:
        print("❌ css/main.css: Missing :root tokens")

    print("\n========================================")
    print(" 5. AI CRAWLERS IN ROBOTS.TXT")
    print("========================================")
    with open('robots.txt', 'r', encoding='utf-8') as f:
        robots = f.read()
    if 'GPTBot' in robots and 'ClaudeBot' in robots and 'PerplexityBot' in robots:
        print("✅ robots.txt: AI bots explicitly allowed & indexed")
    else:
        print("❌ robots.txt: Missing AI bot directives")

if __name__ == '__main__':
    main()
