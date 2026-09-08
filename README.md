# bagouri.uk

Patient information site. Plain static HTML — no build step, no framework, no tracking.

    /                          landing
    /prehab/                   hub: the three guides (QR code target)
      /prehab/hip/
      /prehab/knee/            draft, noindex — awaiting the knee document
      /prehab/hip-muscle-sparing/
    /feedback/                 noindex + unlinked until worker/ is deployed
    /admin/                    working documents, not patient-facing
    /qr/                       QR codes + printable A4 card sheet
    /worker/                   Cloudflare Worker + D1 for the feedback form

## Editing

Edit the HTML directly, on github.com or locally. Pushing to `main` redeploys within a minute.

## Local preview

    python3 -m http.server 8090

## Content notes

- Exercise content and videos are credited to Versus Arthritis (now arthritis-uk.org).
- Guides carry a "Last reviewed" date in the footer. Update it whenever the clinical
  content changes.
