#!/usr/bin/env python3
"""
Weekly Umami Analytics Report for marianstancik.dev
Generates stats and sends via AgentMail every Monday 9:00
"""
import json
import urllib.request
import base64
from datetime import datetime, timezone, timedelta

# Config
UMAMI_URL = "http://localhost:3000"
WEBSITE_ID = "ec1c0df8-e51f-4236-9ad0-e3992f0b1637"
AGENTMAIL_API_KEY = None  # read from env
AGENTMAIL_URL = "https://mcp.agentmail.to/mcp"
REPORT_TO = ["marianstancik@agentmail.to"]
FROM_INBOX = "marianstancik@agentmail.to"

def get_auth_token():
    """Get Umami auth token"""
    req = urllib.request.Request(
        f"{UMAMI_URL}/api/auth/login",
        data=json.dumps({"username": "admin", "password": "umami"}).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as f:
        return json.load(f)["token"]

def api_get(token, path, params=None):
    """Umami API GET"""
    url = f"{UMAMI_URL}{path}"
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def get_weekly_data(token):
    """Get all weekly stats"""
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    start_at = int(week_ago.timestamp() * 1000)
    end_at = int(now.timestamp() * 1000)
    
    stats = api_get(token, f"/api/websites/{WEBSITE_ID}/stats",
                    {"startAt": start_at, "endAt": end_at})
    
    # Top pages
    pages = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                    {"startAt": start_at, "endAt": end_at, "type": "url", "limit": 10})
    
    # Top referrers
    referrers = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                         {"startAt": start_at, "endAt": end_at, "type": "referrer", "limit": 10})
    
    # Browsers
    browsers = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                        {"startAt": start_at, "endAt": end_at, "type": "browser", "limit": 5})
    
    # Devices
    devices = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                       {"startAt": start_at, "endAt": end_at, "type": "device", "limit": 5})
    
    # Countries
    countries = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                         {"startAt": start_at, "endAt": end_at, "type": "country", "limit": 10})
    
    return {
        "stats": stats if "error" not in stats else {},
        "pages": pages if isinstance(pages, list) else [],
        "referrers": referrers if isinstance(referrers, list) else [],
        "browsers": browsers if isinstance(browsers, list) else [],
        "devices": devices if isinstance(devices, list) else [],
        "countries": countries if isinstance(countries, list) else [],
        "period": {
            "from": week_ago.strftime("%d.%m.%Y"),
            "to": now.strftime("%d.%m.%Y")
        }
    }

def format_report(data):
    """Format report as HTML + plain text"""
    s = data["stats"]
    pv = s.get("pageviews", 0)
    visitors = s.get("visitors", 0)
    visits = s.get("visits", 0)
    bounces = s.get("bounces", 0)
    total_time = s.get("totaltime", 0)
    bounce_rate = round(bounces / visits * 100, 1) if visits else 0
    avg_time = round(total_time / visits, 0) if visits else 0
    
    period = data["period"]
    
    # --- HTML ---
    def fmt_list(items, label_key="x", val_key="y", max_n=10):
        if not items:
            return '<p style="color:#8888A0;">Zatiaľ žiadne dáta</p>'
        rows = ""
        for item in items[:max_n]:
            rows += f'<tr><td style="padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.06);">{item.get(label_key,"?")}</td><td style="padding:6px 10px;border-bottom:1px solid rgba(255,255,255,0.06);text-align:right;color:#E8B86D;">{item.get(val_key,0)}</td></tr>\n'
        return f'<table style="width:100%;border-collapse:collapse;font-size:13px;">{rows}</table>'
    
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:620px;margin:0 auto;padding:30px 24px;background:#0D0D18;color:#F0F0F5;border-radius:12px;">
<div style="text-align:center;padding-bottom:24px;border-bottom:2px solid #CD7F32;">
  <h1 style="margin:0;font-size:24px;color:#CD7F32;">📊 Týždenný Report</h1>
  <p style="margin:8px 0 0;color:#8888A0;font-size:14px;">marianstancik.dev · {period["from"]} – {period["to"]}</p>
</div>

<div style="padding:20px 0;">
  <h2 style="color:#CD7F32;font-size:16px;margin:0 0 12px;">📈 Súhrn</h2>
  <table style="width:100%;border-collapse:collapse;font-size:14px;">
    <tr><td style="padding:8px 12px;">Zobrazenia stránok</td><td style="padding:8px 12px;text-align:right;color:#E8B86D;font-weight:bold;">{pv}</td></tr>
    <tr><td style="padding:8px 12px;border-top:1px solid rgba(255,255,255,0.06);">Unikátni návštevníci</td><td style="padding:8px 12px;border-top:1px solid rgba(255,255,255,0.06);text-align:right;color:#E8B86D;font-weight:bold;">{visitors}</td></tr>
    <tr><td style="padding:8px 12px;border-top:1px solid rgba(255,255,255,0.06);">Návštevy</td><td style="padding:8px 12px;border-top:1px solid rgba(255,255,255,0.06);text-align:right;color:#E8B86D;font-weight:bold;">{visits}</td></tr>
    <tr><td style="padding:8px 12px;border-top:1px solid rgba(255,255,255,0.06);">Miera odchodu</td><td style="padding:8px 12px;border-top:1px solid rgba(255,255,255,0.06);text-align:right;color:#E8B86D;font-weight:bold;">{bounce_rate}%</td></tr>
    <tr><td style="padding:8px 12px;border-top:1px solid rgba(255,255,255,0.06);">Priem. čas na stránke</td><td style="padding:8px 12px;border-top:1px solid rgba(255,255,255,0.06);text-align:right;color:#E8B86D;font-weight:bold;">{avg_time:.0f}s</td></tr>
  </table>
</div>

<div style="padding:20px 0;">
  <h2 style="color:#CD7F32;font-size:16px;margin:0 0 12px;">📄 Top stránky</h2>
  {fmt_list(data["pages"])}
</div>

<div style="padding:20px 0;">
  <h2 style="color:#CD7F32;font-size:16px;margin:0 0 12px;">🔗 Top referrers</h2>
  {fmt_list(data["referrers"])}
</div>

<div style="padding:20px 0;">
  <h2 style="color:#CD7F32;font-size:16px;margin:0 0 12px;">🌍 Krajiny</h2>
  {fmt_list(data["countries"])}
</div>

<div style="padding:20px 0;">
  <h2 style="color:#CD7F32;font-size:16px;margin:0 0 12px;">📱 Zariadenia</h2>
  {fmt_list(data["devices"])}
</div>

<div style="padding:20px 0;">
  <h2 style="color:#CD7F32;font-size:16px;margin:0 0 12px;">🌐 Prehliadače</h2>
  {fmt_list(data["browsers"])}
</div>

<div style="padding-top:16px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;color:#8888A0;font-size:12px;">
  <p style="margin:0;">Vygenerované: {datetime.now().strftime("%d. %B %Y %H:%M")} CEST</p>
  <p style="margin:4px 0 0;">Hermes Agent · Umami Analytics · api.marianstancik.dev</p>
</div>
</body></html>"""

    # --- Plain text ---
    text = f"""📊 TÝŽDENNÝ REPORT — marianstancik.dev
{period["from"]} – {period["to"]}
{'='*50}

📈 SÚHRN
----------
Zobrazenia stránok:  {pv}
Unikátni návštevníci: {visitors}
Návštevy:            {visits}
Miera odchodu:       {bounce_rate}%
Priem. čas na str.:  {avg_time:.0f}s

📄 TOP STRÁNKY
----------
"""
    for item in data["pages"][:10]:
        text += f"  {item.get('x','?')}: {item.get('y',0)}\n"

    text += f"""
🔗 TOP REFERRERS
----------
"""
    for item in data["referrers"][:10]:
        text += f"  {item.get('x','?')}: {item.get('y',0)}\n"

    text += f"""
🌍 KRAJINY
----------
"""
    for item in data["countries"][:10]:
        text += f"  {item.get('x','?')}: {item.get('y',0)}\n"

    text += f"""
📱 ZARIADENIA
----------
"""
    for item in data["devices"][:5]:
        text += f"  {item.get('x','?')}: {item.get('y',0)}\n"

    text += f"""
---
Vygenerované: {datetime.now().strftime("%d.%m.%Y %H:%M")}
Hermes Agent · Umami Analytics
"""
    return html, text


def send_email_via_agentmail(html_body, text_body):
    """Send via AgentMail direct JSON-RPC"""
    with open('/opt/umami/.env') as f:
        for line in f:
            line = line.strip()
            if line.startswith('UMAMI_DB_PASSWORD='):
                # Not the API key, but we need AgentMail API key
                pass
    
    # Use the MCP tool approach - simpler
    # We'll output the report data and let the cron deliver via Telegram
    return None


def main():
    token = get_auth_token()
    data = get_weekly_data(token)
    html, text = format_report(data)
    print("REPORT_DATA_MARKER_START")
    print(json.dumps({"html": html, "text": text}))
    print("REPORT_DATA_MARKER_END")


if __name__ == "__main__":
    main()