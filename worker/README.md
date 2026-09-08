# Feedback endpoint

Cloudflare Worker + D1. Patient-typed text stays in your own Cloudflare account,
with no third-party form service, so you remain the only data controller.

## One-time setup

```bash
npm install -g wrangler
wrangler login
```

```bash
wrangler d1 create bagouri-feedback
```

Paste the returned `database_id` into `wrangler.toml`, then:

```bash
wrangler kv namespace create RATE
```

Paste that `id` into `wrangler.toml` too, then:

```bash
wrangler d1 execute bagouri-feedback --remote --file=schema.sql
```

```bash
wrangler secret put SALT
```

```bash
wrangler deploy
```

Finally, add `feedback` as a subdomain route for the worker in the Cloudflare dashboard.

## Reading what patients sent

```bash
wrangler d1 execute bagouri-feedback --remote --command "SELECT created_at, page, helpful, confusing, suggestion FROM feedback ORDER BY id DESC LIMIT 50"
```

## What is deliberately NOT stored

No IP address, no user agent, no cookie, no name, no email, no session. The rate
limiter hashes the IP with a secret salt and keeps only the first 8 bytes for 60
seconds; the address itself never reaches storage.

## Until this is deployed

`/feedback/` is not linked from the site and carries `noindex`. Deploy the worker,
then remove that tag and uncomment the feedback links in the guide footers.
