// Vercel serverless function — Lead capture → AgentMail email
// Requires: AGENTMAIL_API_KEY env var set in Vercel project

export default async function handler(req, res) {
  try {
    // CORS
    res.setHeader('Access-Control-Allow-Origin', 'https://www.marianstancik.dev');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    if (req.method === 'OPTIONS') return res.status(200).end();
    if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

    const apiKey = process.env.AGENTMAIL_API_KEY;
    if (!apiKey) return res.status(500).json({ error: 'API key not configured' });

    // Parse body (form-encoded or JSON)
    let body = {};
    if (typeof req.body === 'object' && req.body !== null && !Array.isArray(req.body)) {
      body = req.body;
    } else if (req.headers['content-type']?.includes('application/json')) {
      try { body = JSON.parse(req.body); } catch { body = {}; }
    } else {
      const raw = typeof req.body === 'string' ? req.body : String(req.body || '');
      for (const pair of raw.split('&')) {
        const [k, v] = pair.split('=').map(s => decodeURIComponent(s.replace(/\+/g, ' ')));
        body[k] = v;
      }
    }

    const email = (body.email || '').trim().toLowerCase();
    const name = body.name || '';
    const source = body.source || 'web';

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
      return res.status(400).json({ error: 'Invalid email' });

    const now = new Date().toISOString().split('T')[0];
    const subject = `[LEAD] ${name || email} — ${source}`;
    const separator = '─'.repeat(40);
    const text = `${separator}\n📥 NEW LEAD — marianstancik.dev\n${separator}\n\nDate:     ${now}\nSource:   ${source}\nEmail:    ${email}\n${name ? `Name:     ${name}\n` : ''}Status:   new\n${separator}`;

    await sendLeadToAgentMail(apiKey, email, name, source, subject, text);
    return res.status(200).json({ status: 'ok', email });

  } catch (e) {
    console.error('Handler error:', e.message);
    return res.status(500).json({ error: e.message });
  }
}

async function sendLeadToAgentMail(apiKey, email, name, source, subject, text) {
  const INBOX = 'marian-hermes-agent@agentmail.to';
  const url = 'https://mcp.agentmail.to/mcp';
  const headers = { 'x-api-key': apiKey, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (compatible; HermesCRM/1.0)' };

  // 1. Initialize session
  const initRes = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify({ jsonrpc: '2.0', id: '1', method: 'initialize', params: { protocolVersion: '0.1.0', capabilities: {}, clientInfo: { name: 'hermes-crm-lead', version: '1.0' } } })
  });

  let sessionId = null;
  const initText = await initRes.text();
  const sseMatch = initText.match(/"sessionId"\s*:\s*"([^"]+)"/);
  sessionId = sseMatch ? sseMatch[1] : null;

  // 2. Send message
  const msgRes = await fetch(url, {
    method: 'POST',
    headers: { ...headers, 'Accept': 'application/json', ...(sessionId ? { 'Mcp-Session-Id': sessionId } : {}) },
    body: JSON.stringify({
      jsonrpc: '2.0', id: '2', method: 'tools/call',
      params: { name: 'send_message', arguments: { inboxId: INBOX, to: [INBOX], subject, text } }
    })
  });

  const msgText = await msgRes.text();
  if (!msgRes.ok) throw new Error(`AgentMail HTTP ${msgRes.status}: ${msgText.slice(0, 200)}`);

  // Try to parse JSON from SSE events (data: {...})
  if (msgText.includes('"isError":true')) throw new Error('AgentMail send failed: ' + msgText.slice(0, 200));
  console.log('Lead sent to AgentMail');
}