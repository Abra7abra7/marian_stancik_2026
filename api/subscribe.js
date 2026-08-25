// Vercel serverless — Lead capture → jednoduchý email na marian_stancik@agentmail.to
export default async function handler(req, res) {
  try {
    res.setHeader('Access-Control-Allow-Origin', 'https://www.marianstancik.dev');
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

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
      return res.status(400).json({ error: 'Invalid email' });

    const now = new Date().toISOString().split('T')[0];
    const subject = `[LEAD] ${name || email} — ${source}`;
    const sep = '─'.repeat(40);
    const text = `${sep}\n📥 NEW LEAD — marianstancik.dev\n${sep}\n\nDate:   ${now}\nSource: ${source}\nEmail:  ${email}\n${name ? `Name:   ${name}\n` : ''}Status: new\n${sep}`;

    // Send via AgentMail MCP
    const url = 'https://mcp.agentmail.to/mcp';
    const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'User-Agent': 'Mozilla/5.0' };

    const initRes = await fetch(url, { method: 'POST', headers: { ...headers, 'x-api-key': apiKey }, body: JSON.stringify({ jsonrpc: '2.0', id: '1', method: 'initialize', params: { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'hermes-crm-lead', version: '1.0' } } }) });
    const initText = await initRes.text();
    const sid = initText.match(/"sessionId"\s*:\s*"([^"]+)"/)?.[1] || null;

    const msgHeaders = { ...headers, 'x-api-key': apiKey };
    if (sid) msgHeaders['Mcp-Session-Id'] = sid;

    const msgRes = await fetch(url, { method: 'POST', headers: msgHeaders, body: JSON.stringify({ jsonrpc: '2.0', id: '2', method: 'tools/call', params: { name: 'send_message', arguments: { inboxId: 'marian_stancik@agentmail.to', to: ['marian_stancik@agentmail.to'], subject, text } } }) });
    const msgText = await msgRes.text();

    if (msgText.includes('"isError":true')) throw new Error('AgentMail send failed');

    return res.status(200).json({ status: 'ok', email });
  } catch (e) {
    console.error('Error:', e.message);
    return res.status(500).json({ error: e.message });
  }
}