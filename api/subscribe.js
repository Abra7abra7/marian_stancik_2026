// Vercel serverless function — Lead capture → AgentMail email
// Requires: AGENTMAIL_API_KEY env var set in Vercel project
// Target inbox: marian_stancik@agentmail.to (for now; creates vault leads via Hermes cron)

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', 'https://www.marianstancik.dev');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') return res.status(405).json({ status: 'error', message: 'POST only' });

  const { email, name, phone, message, company, source } = req.body || {};
  const cleanEmail = String(email || '').trim().toLowerCase();

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(cleanEmail))
    return res.status(400).json({ status: 'error', message: 'Invalid email address' });

  const apiKey = process.env.AGENTMAIL_API_KEY;
  if (!apiKey) {
    console.error('AGENTMAIL_API_KEY not configured');
    return res.status(500).json({ status: 'error', message: 'Server configuration error' });
  }

  const now = new Date().toISOString().split('T')[0];
  const subject = `[LEAD] ${name || cleanEmail} — ${source || 'web'}`;
  const text = [
    `${'─'.repeat(40)}`,
    `📥 NEW LEAD — marianstancik.dev`,
    `${'─'.repeat(40)}\n`,
    `Date:     ${now}`,
    `Source:   ${source || 'web'}`,
    `Email:    ${cleanEmail}`,
    name ? `Name:     ${name}` : null,
    phone ? `Phone:    ${phone}` : null,
    company ? `Company:  ${company}` : null,
    null,
    message ? `Message:\n${message}\n` : null,
    `Status:   new`,
    `${'─'.repeat(40)}`,
  ].filter(Boolean).join('\n');

  try {
    const INBOX = 'marian-hermes-agent@agentmail.to';
    const response = await sendAgentMail(apiKey, INBOX, [INBOX], subject, text);
    console.log('AgentMail sent:', response);

    // Also notify main inbox
    try {
      await sendAgentMail(apiKey, 'marian_stancik@agentmail.to', ['marian_stancik@agentmail.to'], `📬 New lead: ${name || cleanEmail}`, text);
    } catch (e2) {
      console.error('Secondary notification failed (non-fatal):', e2.message);
    }

    return res.status(200).json({ status: 'ok', email: cleanEmail });
  } catch (e) {
    console.error('AgentMail error:', e);
    return res.status(500).json({ status: 'error', message: 'Failed to send' });
  }
}

async function sendAgentMail(apiKey, inboxId, to, subject, text) {
  // JSON-RPC over SSE to AgentMail MCP endpoint
  const url = 'https://mcp.agentmail.to/mcp';
  const headers = {
    'x-api-key': apiKey,
    'Content-Type': 'application/json',
    'Accept': 'text/event-stream',
    'User-Agent': 'Mozilla/5.0 (compatible; HermesCRM/1.0)',
  };

  let sessionId = null;

  // Step 1: initialize
  const initReq = { jsonrpc: '2.0', id: '1', method: 'initialize', params: {
    protocolVersion: '0.1.0',
    capabilities: {},
    clientInfo: { name: 'hermes-crm-lead-capture', version: '1.0.0' }
  }};

  const initRes = await fetch(url, {
    method: 'POST', headers: { ...headers },
    body: JSON.stringify(initReq)
  });

  if (!initRes.ok) throw new Error(`Initialize HTTP ${initRes.status}`);
  const text = await initRes.text();
  
  // Parse SSE for session ID
  const sessionMatch = text.match(/Mcp-Session-Id:\s*(\S+)/i) || 
                       text.match(/["']sessionId["']\s*:\s*["']([^"']+)["']/);
  const sessionHeader = initRes.headers.get('Mcp-Session-Id');
  sessionId = sessionHeader || (sessionMatch ? sessionMatch[1] : null);

  // Step 2: send_message via fetch POST with JSON-RPC (not SSE)
  const msgReq = {
    jsonrpc: '2.0',
    id: '2',
    method: 'tools/call',
    params: {
      name: 'send_message',
      arguments: {
        inboxId: inboxId,
        to: to,
        subject: subject,
        text: text,
      }
    }
  };

  const msgHeaders = { ...headers, 'Content-Type': 'application/json' };
  if (sessionId) msgHeaders['Mcp-Session-Id'] = sessionId;

  const msgRes = await fetch(url, {
    method: 'POST', headers: msgHeaders,
    body: JSON.stringify(msgReq)
  });

  if (!msgRes.ok) throw new Error(`Send HTTP ${msgRes.status}`);
  const data = await msgRes.json();
  return data;
}
