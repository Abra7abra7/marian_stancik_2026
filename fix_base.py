#!/usr/bin/env python3
"""Fix all issues properly - use after git reset --hard 1cd5c2e"""
import re

with open('/root/marian-stancik-web/index.html', 'r') as f:
    html = f.read()

# 1. Meta tags
html = html.replace(
    '<title id="docTitle">Marian Stancik — AI Agent Developer | Product Manager | Law | Drones</title>',
    '<title id="docTitle">Marian Stancik — AI Engineer | Defence Product Manager | Law | Drones</title>'
)
html = html.replace(
    '<meta name="description" id="docDesc" content="Marian Stancik builds autonomous AI agents with Hermes, manages products at Delta Defence, studies law at PF UK, and builds drones. AI x Law x UAV.">',
    '<meta name="description" id="docDesc" content="Marian Stancik is an AI Engineer building autonomous agent systems and production AI infrastructure. Defence Product Manager, PF UK law student, UAV systems builder.">'
)
html = html.replace(
    '<meta name="keywords" content="Marian Stancik, AI agent developer, Hermes Agent, autonomous systems, product manager, Delta Defence, law student, drones, UAV, ASCENTIA, AI compliance, AI Act, GDPR">',
    '<meta name="keywords" content="AI Engineer, AI Engineering, autonomous AI agents, Hermes Agent, MCP, production AI systems, defence product manager, law student, PF UK, drone, UAV">'
)

# 2. JSON-LD: Job titles and worksFor
html = html.replace(
    '"jobTitle": ["AI Agent Developer", "Product Manager", "CEO", "UAV Drone Engineer"]',
    '"jobTitle": ["AI Engineer", "Defence Product Manager", "CEO", "UAV Systems Builder"]'
).replace(
    '"name": "Delta Defence a.s."',
    '"name": "Defence Industry"'
).replace(
    '"description": "AI agent developer, Product Manager at Delta Defence, Law student at PF UK (Comenius University in Bratislava), and UAV engineer building custom ArduPilot drones with Raspberry Pi 5 AI companion computers."',
    '"description": "AI Engineer building autonomous agent systems, production AI infrastructure, and UAV systems. Defence Product Manager. Law student at PF UK (Comenius University in Bratislava)."'
)

# 3. Hero
html = html.replace(
    '✦ AI Agents · Product · Law · UAV', '✦ AI Engineering · Defence · Law · UAV'
)
html = html.replace(
    'AI agent developer who understands <span>law</span>, builds <span>drones</span>, and ships production systems.',
    'AI Engineer building <span>autonomous agents</span>, <span>UAV systems</span>, and production AI infrastructure.'
)
html = html.replace(
    '<span id="rolePm">Product Manager @ Delta Defence</span>',
    '<span id="rolePm">Defence Product Manager</span>'
)

# 4. About
html = html.replace(
    'id="aboutHeading">Builder. Product Manager. Student. Pilot.</h2>',
    'id="aboutHeading">AI Engineer. Builder. Defence PM. Law Student.</h2>'
)
html = html.replace(
    '<strong>Product Manager at Delta Defence</strong>',
    '<strong>Defence Product Manager</strong>'
)
html = html.replace(
    'I leverage AI agents to engineer and deliver tangible physical defense systems — bridging component analysis, supply chain precision, and autonomous flight hardware.',
    'I drive product development in the defense industry — bridging AI, manufacturing, and autonomous systems.'
)
html = html.replace(
    'I study law at <strong>Právnická fakulta',
    'I am a 3rd year law student at <strong>Právnická fakulta'
)
html = html.replace(
    'building an autonomous enterprise Proof-of-Concept',
    'building an autonomous company Proof-of-Concept'
)
html = html.replace(
    'from scratch — analyzing components, hand-soldering electronics, and transitioning from Betaflight manual tuning to <strong>Pixhawk & ArduPilot</strong>',
    'from scratch, and I program them with ArduPilot, Pixhawk, and Python — from Betaflight manual tuning to <strong>Pixhawk & ArduPilot</strong>'
)
html = html.replace(
    'from scratch — analyzing components, hand-soldering electronics, and migrating from Betaflight tuning to <strong>Pixhawk & ArduPilot</strong>',
    'from scratch, and I program them with ArduPilot, Pixhawk, and Python'
)

# 5. Footer
html = html.replace(
    'AI agent developer who understands law, builds drones, and ships production systems.',
    'AI Engineer building autonomous agents, UAV systems, and production AI infrastructure.'
)

# 6. Expertise section titles
html = html.replace(
    'AI Engineering &amp; Autonomous Agents</h3>',
    'AI Engineering &amp; Autonomous Systems</h3>'
)
html = html.replace(
    'Law &amp; AI Compliance (PF UK)</h3>',
    'Law &amp; AI Compliance @ PF UK (3rd Year)</h3>'
)
html = html.replace(
    'UAV Systems &amp; Edge AI (Delta Defence)</h3>',
    'UAV Systems &amp; Drone Programming</h3>'
)
html = html.replace(
    '<span>Delta Defence</span>',
    '<span>QGroundControl</span>'
)

# 7. EN translations in the i18n object
en_skills = """    skillsLabel: "✦ AI Engineering Skills",
    skillsHeading: "Skills &amp; capabilities.",
    skillsIntro: "Full-stack AI engineering — from LLM foundations to production deployment of autonomous agent systems.",
    sk1Title: "Build &amp; Deploy AI Applications",
    sk2Title: "Software Engineering",
    sk3Title: "LLM &amp; Agentive Systems",
    sk4Title: "Production Operations",
    droneLabel: "✦ UAV Systems",
    droneHeading: "Built. Flown. Programmed.",
    droneIntro: "1500g custom carbon quad with ArduPilot, Pixhawk 6C, Raspberry Pi 5 edge AI. EASA A1/A3 certified, €2.6M insured.",
    dCap1: "FPV flight — autonomous waypoint navigation testing",
    dCap2: "Hand-built 1500g carbon quad — maiden flight",
    dCap3: "ArduPilot mission planning — automated multi-waypoint",
    """
html = html.replace(
    'heroEmail: "Email",\n    scrollText: "Scroll",',
    f'heroEmail: "Email",\n{en_skills}    scrollText: "Scroll",'
)

# Fix aboutBody EN (duplicate text issue from sed)
if 'bridging AI, manufacturing, and autonomous systems — bridging component analysis' in html:
    html = html.replace(
        'bridging AI, manufacturing, and autonomous systems — bridging component analysis',
        'bridging AI, manufacturing, and autonomous systems'
    )
# Fix the aboutBody text issue (duplicate "bridging") in aboutBody
if 'bridging component analysis, supply chain precision' in html:
    html = html.replace(
        'I drive product development in the defense industry — bridging AI, manufacturing, and autonomous systems. I drive product development in the defense industry — bridging AI, manufacturing, and autonomous systems.',
        'I drive product development in the defense industry — bridging AI, manufacturing, and autonomous systems.'
    )

with open('/root/marian-stancik-web/index.html', 'w') as f:
    f.write(html)

print("✅ Base fixes done")
print(f"File size: {len(html)} chars")