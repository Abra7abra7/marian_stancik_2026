#!/usr/bin/env python3
"""
Hermes Agent — Autonomous Blog Publishing CLI
Usage:
    python scripts/publish_post.py \
        --title "Edge AI on Raspberry Pi 5 with ArduPilot" \
        --title-sk "Edge AI na Raspberry Pi 5 s ArduPilotom" \
        --excerpt "Deploying neural computer vision models on custom UAVs for real-time target tracking." \
        --excerpt-sk "Nasadenie neurónových modelov počítačového videnia na UAV drony pre autonómne sledovanie cieľov." \
        --tags "Drones, Edge AI, Raspberry Pi 5, ArduPilot" \
        --read-time "5 min read" \
        --read-time-sk "5 min čítania" \
        --content-file "path/to/content.html" \
        [--push] [--dry-run]
"""

import os
import sys
import json
import argparse
import datetime
import re
import subprocess
from xml.etree import ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, 'blog', 'posts')
POSTS_JSON = os.path.join(BASE_DIR, 'blog', 'posts.json')
SITEMAP_XML = os.path.join(BASE_DIR, 'sitemap.xml')
LLMS_TXT = os.path.join(BASE_DIR, 'llms.txt')

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Marian Stancik</title>
<meta name="description" content="{excerpt}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="https://www.marianstancik.dev/blog/posts/{slug}.html">
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM Knowledge Graph">
<link rel="icon" type="image/svg+xml" href="../../favicon.svg">
<link rel="apple-touch-icon" href="../../apple-touch-icon.svg">
<meta name="theme-color" content="#08080F">

<!-- Open Graph -->
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:url" content="https://www.marianstancik.dev/blog/posts/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:image" content="https://www.marianstancik.dev/profile.webp">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="800">
<meta property="og:image:alt" content="{title}">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="sk_SK">
<meta property="og:site_name" content="Marian Stancik">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@marian_s_ai">
<meta name="twitter:creator" content="@marian_s_ai">
<meta name="twitter:image" content="https://www.marianstancik.dev/profile.webp">
<meta property="article:published_time" content="{date}">
<meta property="article:author" content="Marian Stancik">

<!-- JSON-LD BlogPosting -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{title}",
  "description": "{excerpt}",
  "datePublished": "{date}",
  "dateModified": "{date}",
  "author": {{
    "@type": "Person",
    "name": "Marian Stancik",
    "url": "https://www.marianstancik.dev"
  }},
  "publisher": {{
    "@type": "Person",
    "name": "Marian Stancik"
  }},
  "mainEntityOfPage": "https://www.marianstancik.dev/blog/posts/{slug}.html",
  "keywords": {tags_json}
}}
</script>

<style>
*, *::before, *::after {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: #08080F;
  color: #E8E8F0;
  line-height: 1.8;
  -webkit-font-smoothing: antialiased;
}}
.container {{ max-width: 720px; margin: 0 auto; padding: 0 24px; }}
nav {{
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  background: rgba(8,8,15,0.85);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 100;
}}
.nav-inner {{ max-width: 720px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }}
.nav-inner a {{ color: #8888A0; text-decoration: none; font-size: 0.85rem; transition: color 0.3s; }}
.nav-inner a:hover {{ color: #CD7F32; }}
.post-header {{ padding: 60px 0 32px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 36px; }}
.badge {{
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #CD7F32;
  background: rgba(205,127,50,0.08);
  border: 1px solid rgba(205,127,50,0.2);
  padding: 4px 14px;
  border-radius: 100px;
  margin-bottom: 14px;
}}
h1 {{ font-size: clamp(1.8rem, 4vw, 2.5rem); font-weight: 700; color: #F0F0F5; line-height: 1.25; letter-spacing: -0.02em; margin-bottom: 16px; }}
.post-meta {{ display: flex; gap: 12px; color: #666680; font-size: 0.8rem; align-items: center; }}
.post-content {{ font-size: 1rem; color: #B0B0C8; }}
.post-content p + p {{ margin-top: 18px; }}
.post-content h2 {{ font-size: 1.35rem; font-weight: 600; color: #F0F0F5; margin: 40px 0 14px; letter-spacing: -0.01em; }}
.post-content h3 {{ font-size: 1.1rem; font-weight: 600; color: #E8B86D; margin: 28px 0 10px; }}
.post-content ul, .post-content ol {{ margin: 16px 0 16px 24px; }}
.post-content li {{ margin-bottom: 8px; }}
.post-content strong {{ color: #F0F0F5; }}
.post-content pre {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 20px; overflow-x: auto; margin: 20px 0; }}
.post-content pre code {{ font-family: monospace; font-size: 0.85rem; color: #E8B86D; }}
.callout {{ background: rgba(205,127,50,0.06); border-left: 3px solid #CD7F32; border-radius: 0 8px 8px 0; padding: 16px 20px; margin: 24px 0; color: #E8E8F0; }}
footer {{ text-align: center; padding: 36px 24px; color: #555570; font-size: 0.75rem; border-top: 1px solid rgba(255,255,255,0.04); margin-top: 60px; }}
footer a {{ color: #8888A0; text-decoration: none; }}
footer a:hover {{ color: #CD7F32; }}
</style>
</head>
<body>
<nav>
<div class="nav-inner">
<a href="../../index.html">← Marian Stancik</a>
<a href="../index.html">All Posts</a>
</div>
</nav>
<div class="container">
<article class="post-header">
<div class="badge">{primary_tag}</div>
<h1>{title}</h1>
<div class="post-meta">
<span>{display_date}</span>
<span>·</span>
<span>{read_time}</span>
<span>·</span>
<span>By Marian Stancik</span>
</div>
</article>

<div class="post-content">
{content}
</div>
</div>

<footer>
<p>© {year} <a href="https://ascentia.sk" target="_blank">ASCENTIA s.r.o.</a> — <a href="../../index.html">www.marianstancik.dev</a></p>
</footer>
</body>
</html>
"""

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'[\s-]+', '-', text).strip('-')

def main():
    parser = argparse.ArgumentParser(description="Hermes Agent Automated Blog Publisher")
    parser.add_argument('--title', required=True, help="Article title (English)")
    parser.add_argument('--title-sk', required=True, help="Article title (Slovak)")
    parser.add_argument('--excerpt', required=True, help="Article excerpt (English)")
    parser.add_argument('--excerpt-sk', required=True, help="Article excerpt (Slovak)")
    parser.add_argument('--tags', default="AI Agents, Tech", help="Comma-separated tags")
    parser.add_argument('--read-time', default="4 min read", help="Read time EN")
    parser.add_argument('--read-time-sk', default="4 min čítania", help="Read time SK")
    parser.add_argument('--content-file', help="Path to HTML/MD content snippet")
    parser.add_argument('--content-html', help="Raw HTML content string")
    parser.add_argument('--date', help="Publish date YYYY-MM-DD (defaults to today)")
    parser.add_argument('--push', action='store_true', help="Automatically git commit and push to main")
    parser.add_argument('--dry-run', action='store_true', help="Simulate run without writing files")

    args = parser.parse_args()

    # Dates
    pub_date = args.date or datetime.date.today().strftime('%Y-%m-%d')
    dt = datetime.datetime.strptime(pub_date, '%Y-%m-%d')
    display_date = dt.strftime('%B %d, %Y')
    
    # Slovak month mapping
    sk_months = {
        1: 'január', 2: 'február', 3: 'marec', 4: 'apríl',
        5: 'máj', 6: 'jún', 7: 'júl', 8: 'august',
        9: 'september', 10: 'október', 11: 'november', 12: 'december'
    }
    display_date_sk = f"{dt.day}. {sk_months[dt.month]} {dt.year}"
    year = str(dt.year)

    # Slug & Paths
    title_slug = slugify(args.title)
    slug = f"{pub_date}-{title_slug}"
    html_filename = f"{slug}.html"
    html_filepath = os.path.join(POSTS_DIR, html_filename)
    relative_url = f"blog/posts/{html_filename}"
    blog_url = f"posts/{html_filename}"

    tags = [t.strip() for t in args.tags.split(',') if t.strip()]
    primary_tag = tags[0] if tags else "AI & Technology"

    # Content
    content = ""
    if args.content_file and os.path.exists(args.content_file):
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    elif args.content_html:
        content = args.content_html
    else:
        content = f"<p><strong>{args.excerpt}</strong></p><p>Full technical analysis and implementation details coming in this series.</p>"

    # Render HTML Article
    html_out = HTML_TEMPLATE.format(
        title=args.title,
        excerpt=args.excerpt,
        slug=slug,
        date=pub_date,
        display_date=display_date,
        read_time=args.read_time,
        primary_tag=primary_tag,
        tags_json=json.dumps(tags),
        content=content,
        year=year
    )

    new_post_entry = {
        "slug": slug,
        "url": relative_url,
        "blogUrl": blog_url,
        "date": pub_date,
        "displayDate": display_date,
        "displayDateSk": display_date_sk,
        "title": args.title,
        "titleSk": args.title_sk,
        "excerpt": args.excerpt,
        "excerptSk": args.excerpt_sk,
        "tags": tags,
        "readTime": args.read_time,
        "readTimeSk": args.read_time_sk
    }

    print(f"[*] Preparing article: {slug}")
    print(f"    - Title (EN): {args.title}")
    print(f"    - Title (SK): {args.title_sk}")
    print(f"    - Target file: {html_filepath}")

    if args.dry_run:
        print("[!] DRY RUN mode — no files written.")
        print(f"JSON preview:\n{json.dumps(new_post_entry, indent=2, ensure_ascii=False)}")
        return

    if args.push and not args.dry_run:
        print("[*] Pulling latest changes from origin/main before publishing...")
        try:
            subprocess.run(["git", "pull", "origin", "main", "--rebase"], cwd=BASE_DIR, check=True)
        except Exception as e:
            print(f"[!] Warning: git pull failed: {e}")

    # 1. Write HTML article file
    with open(html_filepath, 'w', encoding='utf-8') as f:
        f.write(html_out)
    print(f"[+] Created article: {html_filepath}")

    # 2. Update blog/posts.json
    posts = []
    if os.path.exists(POSTS_JSON):
        with open(POSTS_JSON, 'r', encoding='utf-8') as f:
            try:
                posts = json.load(f)
            except Exception:
                posts = []
    
    # Filter out existing if re-publishing same slug
    posts = [p for p in posts if p.get('slug') != slug]
    posts.insert(0, new_post_entry)

    with open(POSTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f"[+] Updated manifest: {POSTS_JSON} ({len(posts)} total posts)")

    # 3. Update llms.txt
    if os.path.exists(LLMS_TXT):
        with open(LLMS_TXT, 'r', encoding='utf-8') as f:
            llms_content = f.read()
        
        article_link = f"https://www.marianstancik.dev/{relative_url}"
        if article_link not in llms_content:
            new_item = f"\n- **{args.title}:** {article_link} (Topics: {', '.join(tags)})\n"
            # Append before Links section or at end
            if "## Links & Social Channels" in llms_content:
                llms_content = llms_content.replace("## Links & Social Channels", f"{new_item}\n## Links & Social Channels")
            else:
                llms_content += new_item
            with open(LLMS_TXT, 'w', encoding='utf-8') as f:
                f.write(llms_content)
            print(f"[+] Updated llms.txt knowledge graph")

    # 4. Optional Git Commit & Push
    if args.push:
        print("[*] Executing git push to main...")
        subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
        commit_msg = f"📝 auto(blog): publish {slug}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, check=True)
        print(f"[✅] Published and deployed live to: https://www.marianstancik.dev/{relative_url}")
    else:
        print("[ℹ] Files written locally. Run 'git push origin main' when ready.")

if __name__ == '__main__':
    main()
