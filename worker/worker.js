/**
 * bagouri.uk feedback endpoint.
 *
 * Design constraints, deliberately:
 *   - stores no IP address, no user agent, no cookie, no name, no email
 *   - accepts only the four known fields, each length-capped
 *   - CORS restricted to the site origin
 *   - honeypot + per-minute rate limit to keep bots out
 */
const ORIGIN = 'https://bagouri.uk';
const MAX = 1500;

const cors = {
  'Access-Control-Allow-Origin': ORIGIN,
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400',
};

// Cap the length and strip control characters.
const clean = (v) => String(v ?? '').slice(0, MAX).replace(/[\x00-\x1F\x7F]/g, '').trim();

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: cors });
    if (request.headers.get('Origin') !== ORIGIN) return new Response('Forbidden', { status: 403, headers: cors });

    let body;
    try { body = await request.json(); } catch { return new Response('Bad request', { status: 400, headers: cors }); }

    // Honeypot: accept silently, so the bot learns nothing.
    if (clean(body.website)) return new Response('{"ok":true}', { status: 200, headers: cors });

    // Rate limit on a salted, truncated hash of the IP. The address itself is never stored.
    if (env.RATE) {
      const ip = request.headers.get('CF-Connecting-IP') || '';
      const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(ip + (env.SALT || 'bagouri')));
      const key = 'rl:' + [...new Uint8Array(digest)].slice(0, 8).map((b) => b.toString(16).padStart(2, '0')).join('');
      if (await env.RATE.get(key)) return new Response('Too many requests', { status: 429, headers: cors });
      await env.RATE.put(key, '1', { expirationTtl: 60 });
    }

    const row = {
      page: clean(body.page).slice(0, 40) || 'general',
      helpful: ['yes', 'partly', 'no'].includes(body.helpful) ? body.helpful : '',
      confusing: clean(body.confusing),
      suggestion: clean(body.suggestion),
    };
    if (!row.helpful && !row.confusing && !row.suggestion) {
      return new Response('Empty', { status: 400, headers: cors });
    }

    await env.DB.prepare(
      'INSERT INTO feedback (created_at, page, helpful, confusing, suggestion) VALUES (?, ?, ?, ?, ?)'
    ).bind(new Date().toISOString(), row.page, row.helpful, row.confusing, row.suggestion).run();

    return new Response('{"ok":true}', { status: 200, headers: { ...cors, 'Content-Type': 'application/json' } });
  },
};
