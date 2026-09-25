# 2.0 launch giveaway

Three App Store promo codes, first come, first served. The home page shows a
band above the hero while codes are left; pressing **Claim a free copy** gives
that visitor the next code, and it is gone for everyone else. Once all three
are claimed the band disappears by itself.

Apple does not tell us when a code is redeemed, so "claimed" means handed out
here. The visitor's browser keeps the code it got (`ccx-giveaway` in local
storage, listed on `/cookies`).

| Piece | Where |
|---|---|
| Worker | `worker.js`, deployed as `coldcallx-giveaway` at https://coldcallx-giveaway.vadykk.workers.dev |
| Database | D1 `coldcallx-giveaway`, one table (`schema.sql`) |
| Band | `.gift` in `index.html` (markup and script) and `site.css` |

Commands below run from this folder with the calling worker's wrangler
(`../../coldcallerx/telnyx-api-worker/node_modules/.bin/wrangler`, or `npx wrangler`).

## Start it

In App Store Connect, open Cold Call X and generate three promo codes (they
expire four weeks after you make them), then:

```bash
wrangler d1 execute coldcallx-giveaway --remote --command "INSERT INTO codes (slot, code) VALUES (1,'CODE1'),(2,'CODE2'),(3,'CODE3')"
```

The band appears on the next page load.

## Check on it

```bash
curl https://coldcallx-giveaway.vadykk.workers.dev/status
wrangler d1 execute coldcallx-giveaway --remote --command "SELECT slot, claimed_at FROM codes"
```

## End it early

```bash
wrangler d1 execute coldcallx-giveaway --remote --command "DELETE FROM codes"
```

With no codes left the band stays hidden. To take it off the site for good,
delete the `.gift` band and its script from `index.html`, the `.gift` rules
from `site.css`, the `ccx-giveaway` row and the claim paragraph from
`/cookies`, and this folder; then `wrangler delete` the worker and
`wrangler d1 delete coldcallx-giveaway`.

## Test locally

```bash
wrangler d1 execute coldcallx-giveaway --local --file schema.sql
wrangler d1 execute coldcallx-giveaway --local --command "INSERT INTO codes (slot, code) VALUES (1,'TEST1'),(2,'TEST2'),(3,'TEST3')"
wrangler dev --local --port 8787
```

The page talks to `http://127.0.0.1:8787` whenever it is served from
127.0.0.1 or localhost.
