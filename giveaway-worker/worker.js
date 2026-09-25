// The 2.0 launch giveaway: three App Store promo codes, first come, first
// served. Each code goes to exactly one visitor: the claim is a single D1
// UPDATE, so two people pressing Claim at the same moment can never receive
// the same code. The site shows its giveaway band only while /status says
// codes are left.
//
// Nothing about the visitor is stored. The per-IP rate limit (one claim a
// minute) lives in Cloudflare's memory, not in the database, and only stops a
// script from taking every code in one burst.

const ORIGINS = ['https://coldcallx.app', 'http://127.0.0.1:4417'];

export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);
    const origin = request.headers.get('Origin');
    const cors = {
      'Access-Control-Allow-Origin': ORIGINS.includes(origin) ? origin : ORIGINS[0],
      'Vary': 'Origin',
      'Cache-Control': 'no-store',
    };
    const json = (body, status = 200) =>
      new Response(JSON.stringify(body), { status, headers: { ...cors, 'Content-Type': 'application/json' } });

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: { ...cors, 'Access-Control-Allow-Methods': 'GET, POST', 'Access-Control-Max-Age': '86400' } });
    }

    if (pathname === '/status' && request.method === 'GET') {
      const row = await env.DB.prepare('SELECT COUNT(*) AS total, SUM(claimed_at IS NULL) AS left FROM codes').first();
      return json({ total: row.total, left: row.left ?? 0 });
    }

    if (pathname === '/claim' && request.method === 'POST') {
      if (!ORIGINS.includes(origin)) return json({ error: 'origin' }, 403);
      const { success } = await env.CLAIMS.limit({ key: request.headers.get('CF-Connecting-IP') || 'unknown' });
      if (!success) return json({ error: 'slow_down' }, 429);

      const won = await env.DB.prepare(
        `UPDATE codes SET claimed_at = ?1
         WHERE slot = (SELECT slot FROM codes WHERE claimed_at IS NULL ORDER BY slot LIMIT 1)
         RETURNING code`,
      ).bind(new Date().toISOString()).first();
      const row = await env.DB.prepare('SELECT COUNT(*) AS total, SUM(claimed_at IS NULL) AS left FROM codes').first();
      if (!won) return json({ total: row.total, left: 0 }, 410);
      return json({ code: won.code, total: row.total, left: row.left ?? 0 });
    }

    return json({ error: 'not_found' }, 404);
  },
};
