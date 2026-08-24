#!/usr/bin/env python3
"""Add AI Skills section, Drone Showcase section, CSS, and i18n"""
import re

with open('/root/marian-stancik-web/index.html', 'r') as f:
    html = f.read()

# === CSS — insert before ANIMATIONS ===
skills_css = """
/* ===== AI ENGINEERING SKILLS ===== */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 36px;
}
.skill-category {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 28px 24px;
  transition: all 0.3s;
}
.skill-category:hover {
  border-color: rgba(205,127,50,0.3);
  background: rgba(205,127,50,0.04);
  transform: translateY(-2px);
}
.skill-icon { margin-bottom: 16px; }
.skill-category h3 {
  font-size: 1.05rem;
  font-weight: 600;
  color: #F0F0F5;
  margin-bottom: 14px;
}
.skill-category ul { list-style: none; padding: 0; }
.skill-category li {
  font-size: 0.85rem;
  color: #8888A0;
  padding: 4px 0 4px 16px;
  position: relative;
}
.skill-category li::before {
  content: '';
  position: absolute;
  left: 0; top: 11px;
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #CD7F32;
  opacity: 0.5;
}
.drone-videos {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-top: 36px;
}
.drone-video-card {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px;
  overflow: hidden;
  transition: all 0.3s;
}
.drone-video-card:hover {
  border-color: rgba(205,127,50,0.3);
  transform: translateY(-3px);
}
.drone-video-card video {
  display: block;
  width: 100%;
  height: auto;
}
.drone-video-caption {
  font-size: 0.78rem;
  color: #8888A0;
  padding: 12px 16px 14px;
  text-align: center;
}
.drone-specs {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 28px;
}
.spec-item {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 10px;
  padding: 14px 16px;
  text-align: center;
}
.spec-key {
  display: block;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #CD7F32;
  margin-bottom: 6px;
}
.spec-val {
  display: block;
  font-size: 0.82rem;
  color: #C8C8D4;
}
@media (max-width: 800px) {
  .skills-grid { grid-template-columns: 1fr; }
  .drone-videos { grid-template-columns: 1fr; }
  .drone-specs { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 500px) {
  .drone-specs { grid-template-columns: 1fr; }
}
"""
# CSS is before first script or before "ANIMATIONS"
html = html.replace(
    '/* ===== SOCIAL ICONS ===== */',
    skills_css + '\n/* ===== SOCIAL ICONS ===== */'
)

# === HTML sections — insert after expertise section </section> ===
# Find the closing </section> of expertise (3rd section)
skills_html = """
<!-- === AI ENGINEERING SKILLS === -->
<section id="ai-skills" aria-label="AI Engineering skills map">
  <div class="container">
    <div class="section-label fade-in" id="skillsLabel">✦ AI Engineering Skills</div>
    <h2 class="fade-in" id="skillsHeading">Skills &amp; capabilities.</h2>
    <p class="section-intro fade-in" id="skillsIntro">
      Full-stack AI engineering — from LLM foundations to production deployment of autonomous agent systems.
    </p>
    <div class="skills-grid fade-in">
      <div class="skill-category">
        <div class="skill-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#CD7F32" stroke-width="1.8"><path d="M12 3v12M5 10l7-7 7 7M5 21h14"/></svg></div>
        <h3 id="sk1Title">Build &amp; Deploy AI Applications</h3>
        <ul id="sk1List">
          <li>Autonomous multi-agent systems (Hermes Agent)</li>
          <li>Model Context Protocol (MCP) servers</li>
          <li>Production 24/7 agent runtime on VPS</li>
          <li>Telegram / WhatsApp command &amp; control</li>
        </ul>
      </div>
      <div class="skill-category">
        <div class="skill-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#CD7F32" stroke-width="1.8"><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/></svg></div>
        <h3 id="sk2Title">Software Engineering</h3>
        <ul id="sk2List">
          <li>Python, TypeScript, Go</li>
          <li>HTML5 / CSS3 / Vanilla JS (zero framework)</li>
          <li>CI/CD, GitOps, Vercel deploy</li>
          <li>Infrastructure: Hetzner, Caddy, Syncthing</li>
        </ul>
      </div>
      <div class="skill-category">
        <div class="skill-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#CD7F32" stroke-width="1.8"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><circle cx="12" cy="12" r="3"/></svg></div>
        <h3 id="sk3Title">LLM &amp; Agentive Systems</h3>
        <ul id="sk3List">
          <li>LLM foundations &amp; model grounding</li>
          <li>Multi-agent architectures</li>
          <li>Evaluation-driven development</li>
          <li>Context persistence &amp; checkpoint recovery</li>
        </ul>
      </div>
      <div class="skill-category">
        <div class="skill-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#CD7F32" stroke-width="1.8"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg></div>
        <h3 id="sk4Title">Production Operations</h3>
        <ul id="sk4List">
          <li>19+ cron-orchestrated background agents</li>
          <li>AgentMail automation &amp; lead capture</li>
          <li>System monitoring &amp; watchdogs</li>
          <li>Secure-by-design infrastructure</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- === DRONE SHOWCASE === -->
<section id="drone-showcase" aria-label="Drone build and UAV video showcase">
  <div class="container">
    <div class="section-label fade-in" id="droneLabel">✦ UAV Systems</div>
    <h2 class="fade-in" id="droneHeading">Built. Flown. Programmed.</h2>
    <p class="section-intro fade-in" id="droneIntro">
      1500g custom carbon quad with ArduPilot, Pixhawk 6C, Raspberry Pi 5 edge AI. EASA A1/A3 certified, €2.6M insured.
    </p>
    <div class="drone-videos fade-in">
      <div class="drone-video-card">
        <video controls preload="metadata" poster width="100%" height="auto">
          <source src="https://pub-6f8a7e36d1e74f6c8b8a3f2c5d4e7b12.r2.dev/drone/2026-08-24_fpv-okuliare-10.mp4" type="video/mp4">
        </video>
        <p class="drone-video-caption" id="dCap1">FPV flight &mdash; autonomous waypoint navigation testing</p>
      </div>
      <div class="drone-video-card">
        <video controls preload="metadata" poster width="100%" height="auto">
          <source src="https://pub-6f8a7e36d1e74f6c8b8a3f2c5d4e7b12.r2.dev/drone/2026-08-24_fpv-okuliare-11.mp4" type="video/mp4">
        </video>
        <p class="drone-video-caption" id="dCap2">Hand-built 1500g carbon quad &mdash; maiden flight</p>
      </div>
      <div class="drone-video-card">
        <video controls preload="metadata" poster width="100%" height="auto">
          <source src="https://pub-6f8a7e36d1e74f6c8b8a3f2c5d4e7b12.r2.dev/drone/2026-08-24_fpv-okuliare-21.mp4" type="video/mp4">
        </video>
        <p class="drone-video-caption" id="dCap3">ArduPilot mission planning &mdash; automated multi-waypoint</p>
      </div>
    </div>
    <div class="drone-specs fade-in">
      <div class="spec-item"><span class="spec-key">Frame</span><span class="spec-val">1500g custom carbon quad</span></div>
      <div class="spec-item"><span class="spec-key">Flight Controller</span><span class="spec-val">Pixhawk 6C + ArduPilot Copter</span></div>
      <div class="spec-item"><span class="spec-key">Edge AI</span><span class="spec-val">Raspberry Pi 5 onboard computer</span></div>
      <div class="spec-item"><span class="spec-key">Software</span><span class="spec-val">QGroundControl, Mission Planner, MAVLink</span></div>
      <div class="spec-item"><span class="spec-key">Certification</span><span class="spec-val">EASA A1/A3, Coverdrone €2.6M insured</span></div>
      <div class="spec-item"><span class="spec-key">Goal</span><span class="spec-val">Program &amp; operate autonomous UAV systems</span></div>
    </div>
  </div>
</section>

"""
# Insert after 3rd </section> closing (expertise section)
html = html.replace(
    '<!-- === PROJECTS === -->',
    skills_html + '\n<!-- === PROJECTS === -->'
)

# === i18n applyTranslations entries ===
# Insert JS translation calls inside applyTranslations function
insert_js = """  document.getElementById('skillsLabel').textContent = d.skillsLabel;
  document.getElementById('skillsHeading').textContent = d.skillsHeading;
  document.getElementById('skillsIntro').textContent = d.skillsIntro;
  document.getElementById('droneLabel').textContent = d.droneLabel;
  document.getElementById('droneHeading').textContent = d.droneHeading;
  document.getElementById('droneIntro').textContent = d.droneIntro;
  document.getElementById('dCap1').textContent = d.dCap1;
  document.getElementById('dCap2').textContent = d.dCap2;
  document.getElementById('dCap3').textContent = d.dCap3;
"""

html = html.replace(
    "document.getElementById('exp3Desc').textContent = d.exp3Desc;",
    "document.getElementById('exp3Desc').textContent = d.exp3Desc;\n" + insert_js
)

# === SK translations ===
# Insert SK translations after heroEmail in sk section
sk_skills = """    skillsLabel: \"✦ AI Engineering Skills\",
    skillsHeading: \"Zručnosti &amp; schopnosti.\",
    skillsIntro: \"Full-stack AI inžinierstvo — od LLM základov po produkčné nasadenie autonómnych agentov.\",
    sk1Title: \"Build &amp; Deploy AI aplikácie\",
    sk2Title: \"Softvérové inžinierstvo\",
    sk3Title: \"LLM &amp; Agentívne systémy\",
    sk4Title: \"Produkčná prevádzka\",
    droneLabel: \"✦ UAV Systémy\",
    droneHeading: \"Postavené. Odlietané. Naprogramované.\",
    droneIntro: \"1500g custom carbon quad s ArduPilot, Pixhawk 6C, Raspberry Pi 5 edge AI. EASA A1/A3, €2,6M poistené.\",
    dCap1: \"FPV let — test autonómneho navigovania\",
    dCap2: \"Ručne postavený 1500g carbon quad — prvý let\",
    dCap3: \"ArduPilot plánovanie misií — automatické waypointy\",
    """

# Find in SK section — only second occurrence of heroEmail
sk_pos = html.rfind('heroEmail: "E-mail"')
if sk_pos > 0:
    # Insert after this line
    next_nl = html.find('\n', sk_pos)
    html = html[:next_nl+1] + sk_skills + html[next_nl+1:]

with open('/root/marian-stancik-web/index.html', 'w') as f:
    f.write(html)

print(f"✅ Skills + Drone sections added")
print(f"File size: {len(html)} chars")
print(f"Has skills section: {'<!-- === AI ENGINEERING SKILLS === -->' in html}")
print(f"Has drone section: {'drone-showcase' in html}")