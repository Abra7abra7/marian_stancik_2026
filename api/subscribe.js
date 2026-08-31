// Vercel serverless — Lead capture → AgentMail (welcome email + notification)
export default async function handler(req, res) {
  try {
    res.setHeader('Access-Control-Allow-Origin', 'https://www.marianstancik.dev');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    if (req.method === 'OPTIONS') return res.status(200).end();
    if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

    const apiKey = process.env.AGENTMAIL_API_KEY;
    if (!apiKey) return res.status(500).json({ error: 'API key not configured' });

    const body = typeof req.body === 'object' ? req.body : {};
    const email = (body.email || '').trim().toLowerCase();
    const name = body.name || '';
    const source = body.source || 'web';
    const message = body.message || '';

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
      return res.status(400).json({ error: 'Invalid email' });

    const now = new Date();
    const dateStr = now.toISOString().split('T')[0];
    const timeStr = now.toTimeString().split(' ')[0];

    const url = 'https://mcp.agentmail.to/mcp';
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json, text/event-stream',
      'x-api-key': apiKey
    };

    // Helper: MCP session → send email
    async function sendEmail(to, subject, text) {
      const initBody = JSON.stringify({
        jsonrpc: '2.0', id: '1', method: 'initialize',
        params: { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'hermes-crm', version: '1.0' } }
      });
      const initRes = await fetch(url, { method: 'POST', headers, body: initBody });
      const initText = await initRes.text();
      const sessionMatch = initText.match(/"sessionId"\s*:\s*"([^"]+)"/);
      const sessionId = sessionMatch ? sessionMatch[1] : null;
      const msgHeaders = { ...headers };
      if (sessionId) msgHeaders['Mcp-Session-Id'] = sessionId;

      await fetch(url, { method: 'POST', headers: msgHeaders, body: JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) });

      const sendBody = JSON.stringify({
        jsonrpc: '2.0', id: '2', method: 'tools/call',
        params: {
          name: 'send_message',
          arguments: { inboxId: 'marianstancik@agentmail.to', to: [to], subject, text }
        }
      });
      const msgRes = await fetch(url, { method: 'POST', headers: msgHeaders, body: sendBody });
      const msgText = await msgRes.text();
      if (msgText.includes('"isError":true')) {
        const errMsg = msgText.match(/"message"\s*:\s*"([^"]+)"/)?.[1] || 'Unknown error';
        throw new Error(`AgentMail: ${errMsg}`);
      }
    }

    const sep = '─'.repeat(40);

    // 1. Welcome email to subscriber
    const welcomeText = `Vitaj v newslettri Mariana Stancika! 👋
${sep}

Ďakujem za prihlásenie k odberu noviniek z oblasti AI agentov, UAV dronov a právnej regulácie.

Každý pondelok ráno ti pošlem prehľad najzaujímavejšieho, čo sa udialo.

Čo môžeš očakávať:
• AI Agent Systems — novinky z Hermes Agent, MCP, multi-LLM
• UAV & Edge AI — technické buildy, ArduPilot, computer vision
• EU AI Act & Compliance — praktické právne poznatky
• Biznis a automatizácia — Ako budovať agent-driven spoločnosť

Môj web: https://www.marianstancik.dev
X (Twitter): https://x.com/marian_s_ai

Odhlásiť sa môžeš kedykoľvek odpoveďou na tento email.

S pozdravom,
Marian Stancik
AI Engineer · UAV Builder · Law Scholar`;

    const welcomeSubject = `👋 Vitaj v newslettri, ${name || 'priateľ'}!`;
    await sendEmail(email, welcomeSubject, welcomeText).catch(e => {
      console.error('Welcome email failed:', e.message);
    });

    // 2. Notification to Marian
    const notifText = `📥 NEW LEAD — marianstancik.dev
${sep}
Date:   ${dateStr} ${timeStr}
Source: ${source}
Email:  ${email}
${name ? `Name:   ${name}` : ''}
${message ? `Message: ${message}` : ''}
Status: welcome sent ✅
${sep}`;

    await sendEmail('marianstancik@agentmail.to', `[LEAD] ${name || email} — ${source}`, notifText);

    return res.status(200).json({ status: 'ok', email, welcome_sent: true });
  } catch (e) {
    console.error('Subscribe error:', e.message);
    return res.status(500).json({ error: e.message });
  }
}