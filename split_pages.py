#!/usr/bin/env python3
import os

H = '/root/marian-stancik-web'

with open(f'{H}/index.html', 'r') as f:
    html = f.read()

def extract(start_tag, end_tag):
    """Extract content between two markers (including start, excluding end)."""
    s = html.find(start_tag)
    e = html.find(end_tag, s) if end_tag else len(html)
    return html[s:e] if s >= 0 else ''

def page_base():
    """Common boilerplate (head, css, nav, three, footer, js)."""
    css = html[html.find('/* ===== RESET'):html.find('</style>')+8]
    three = html[html.find('<script type="importmap">'):]
    # Truncate three.js at the i18n script
    three = three[:three.find('<!-- i18n Dictionary')]
    
    nav = '''<nav aria-label="Main navigation">
  <div class="nav-container">
    <a href="/" class="nav-logo" aria-label="Marian Stancik home">
      <div class="ms-logo" aria-hidden="true">MS</div>
      <span class="nav-logo-text">Marian <span>Stancik</span></span>
    </a>
    <div class="nav-right">
      <div class="lang-switcher" aria-label="Language selector">
        <button class="lang-btn active" id="btnEn" onclick="switchLanguage(\'en\')">EN</button>
        <button class="lang-btn" id="btnSk" onclick="switchLanguage(\'sk\')">SK</button>
      </div>
      <button class="mobile-toggle" aria-label="Toggle menu" aria-expanded="false">☰</button>
      <div class="nav-links">
        <a href="/" class="nav-link">Home</a>
        <a href="/about" class="nav-link" id="navAbout">About</a>
        <a href="/expertise" class="nav-link" id="navExpertise">Expertise</a>
        <a href="/skills" class="nav-link">Skills</a>
        <a href="/drones" class="nav-link">Drones</a>
        <a href="/blog" class="nav-link" id="navBlog">Blog</a>
        <a href="/contact" class="nav-link nav-cta" id="navContact">✦ Contact</a>
      </div>
    </div>
  </div>
</nav>'''

    footer_end = html[html.find('<!-- Footer -->'):]
    footer_end = footer_end[:footer_end.find('<!-- Three.js')]
    
    i18n = html[html.find('<!-- i18n Dictionary'):]
    i18n = i18n[:i18n.find('</script>')+9]
    
    return css, nav, footer_end, three, i18n

css, nav, footer_end, three, i18n = page_base()

# Fix nav labels in i18n
old_vals = {'navAbout: "About"', 'navExpertise: "Expertise"', 'navBlog: "Blog"', 'navContact: "✦ Contact"'}
# Add nav items for new pages
sk_skills = '''    navBlog: "Blog",
    navContact: "✦ Contact",'''

# Extract the full translations from source for each page
translations_start = html.find('const translations = {')
translations_end = html.find('// Mobile menu toggle')
translations = html[translations_start:translations_end]
# Remove the old applyTranslations function up to but not including // Mobile menu toggle
mobile_menu_start = html.find('// Mobile menu toggle')
mobile_menu = html[mobile_menu_start:]
mobile_menu = mobile_menu[:mobile_menu.find('// Lead form submit')]

common_js = translations + '\n' + mobile_menu

def make_page(title, desc, og_desc, body, suffix):
    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="AI Engineer, AI Engineering, autonomous AI agents, Hermes Agent, MCP, production AI systems">
<meta name="author" content="Marian Stancik">
<link rel="canonical" href="https://www.marianstancik.dev{suffix}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.svg">
<meta name="theme-color" content="#08080F">
<meta property="og:title" content="Marian Stancik — {title.split('—')[1].strip() if '—' in title else title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="https://www.marianstancik.dev{suffix}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://www.marianstancik.dev/profile.jpg">
<meta property="og:site_name" content="Marian Stancik">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@marian_s_ai">
<meta name="twitter:creator" content="@marian_s_ai">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' https://*.r2.cloudflarestorage.com; connect-src 'self' https://cdn.jsdelivr.net http://188.245.224.189; font-src 'self'">
</head>
'''

    page = f'''{head}
{css}
</head>
<body>
<canvas id="three-canvas"></canvas>
<div class="content" id="main-content">
{nav}
{body}
{footer_end}
</div>
{three}
<script>
{common_js}
</script>
</body>
</html>'''
    return page

# === BUILD PAGES ===

# HOME
home_body = extract('<!-- === HERO === -->', '<!-- === ABOUT === -->')
# Add stats
about_stats = extract('<div class="stats', '</section>')
home_body += about_stats + '</div></section>\n'
home_body += extract('<!-- === BLOG PREVIEW === -->', '<!-- === LEAD CAPTURE === -->')
home_body += extract('<!-- === LEAD CAPTURE === -->', '<!-- === CONNECT === -->')
home_body += extract('<!-- === CONNECT === -->', '<!-- Footer -->')

P = {}
P['index.html'] = make_page(
    'Marian Stancik — AI Engineer | Defence Product Manager | Law | Drones',
    'Marian Stancik is an AI Engineer building autonomous agent systems and production AI infrastructure. Defence Product Manager, PF UK law student, UAV systems builder.',
    'AI Engineer building autonomous agent systems. Defence Product Manager. PF UK law. UAV builder.',
    home_body, ''
)

# ABOUT
about_body = extract('<!-- === ABOUT === -->', '<!-- === EXPERTISE === -->')
P['about.html'] = make_page(
    'Marian Stancik — About | AI Engineer, Defence PM, PF UK Law, UAV',
    'About Marian Stancik — AI Engineer, Defence Product Manager, PF UK law student (3rd year), UAV builder.',
    'About — AI Engineer, Defence PM, PF UK law, UAV builder.',
    about_body, '/about'
)

# EXPERTISE
exp_body = extract('<!-- === EXPERTISE === -->', '<!-- === AI ENGINEERING SKILLS === -->')
P['expertise.html'] = make_page(
    'Marian Stancik — Expertise | AI Engineering, Law, Drones',
    'Three pillars: AI Engineering & Autonomous Agents, Law & AI Compliance (PF UK), UAV Systems & Drone Programming.',
    'Three pillars of expertise — AI Engineering, Law & AI Compliance, UAV Systems.',
    exp_body, '/expertise'
)

# SKILLS
skills_body = extract('<!-- === AI ENGINEERING SKILLS === -->', '<!-- === DRONE SHOWCASE === -->')
P['skills.html'] = make_page(
    'Marian Stancik — AI Engineering Skills | Agent Systems, MCP, Production',
    'Full-stack AI engineering: autonomous multi-agent systems, MCP, LLM & agentive systems, production operations.',
    'AI Engineering Skills Map — Build, Deploy, Operate autonomous agent systems.',
    skills_body, '/skills'
)

# DRONES
drone_body = extract('<!-- === DRONE SHOWCASE === -->', '<!-- === PROJECTS === -->')
P['drones.html'] = make_page(
    'Marian Stancik — UAV Systems & Drone Programming | ArduPilot, Pixhawk',
    '1500g custom quad with ArduPilot, Pixhawk 6C, Raspberry Pi 5 edge AI. EASA A1/A3, €2.6M insured. FPV showcase.',
    'Custom UAV systems, ArduPilot programming, FPV flight video.',
    drone_body, '/drones'
)

# CONTACT
contact_body = extract('<!-- === CONNECT === -->', '<!-- Footer -->')
P['contact.html'] = make_page(
    'Marian Stancik — Contact | Connect, Email, Social',
    'Connect with Marian Stancik — AI Engineer, Defence PM, PF UK law, UAV builder. X/Twitter, LinkedIn, GitHub.',
    'Contact — follow the build, read the blog, reach out.',
    contact_body, '/contact'
)

# WRITE
os.chdir(H)
for fname, content in P.items():
    with open(fname, 'w') as f:
        f.write(content)
    print(f"✅ {fname} ({len(content)} chars)")

print(f"\nGenerated {len(P)} pages")