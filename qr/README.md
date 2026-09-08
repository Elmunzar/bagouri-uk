# QR codes

## What is here

| File | |
|---|---|
| `cards-hub.html` | **A4 sheet, 8 identical hub cards.** The clinic default. |
| `card.html` | A4 sheet, one card per guide (hub + 3 operations). |
| `prehab-hub.*` | Hub — `https://bagouri.uk/prehab/` |
| `prehab-hip.*` | `https://bagouri.uk/prehab/hip/` |
| `prehab-knee.*` | `https://bagouri.uk/prehab/knee/` |
| `prehab-hip-anterior.*` | `https://bagouri.uk/prehab/hip-muscle-sparing/` |

SVG for print, PNG for screen and for the card sheets. All generated at error
correction level H (~30% recoverable), so a code still scans when creased,
smudged or partly covered.

## Prefer the hub card

Handing a patient the wrong per-operation card shows them the wrong risks, the
wrong recovery expectations and the wrong exercises. The hub card cannot be
wrong: it asks the patient which operation they are waiting for.

Use the per-operation cards only where the workflow already knows the operation
with certainty — attached to a clinic letter after listing, not loose in a room.

## These codes are hard-bound to their URLs

Each code encodes an absolute `https://` URL. **If a guide's path ever changes,
every copy of that code — printed, displayed, or already in a patient's photo
roll — breaks silently.** A patient scanning an old card gets a 404, not a
redirect.

So: treat `/prehab/`, `/prehab/hip/`, `/prehab/knee/` and
`/prehab/hip-muscle-sparing/` as permanent URLs.

If a path genuinely must change, do **not** just regenerate the codes. Leave a
stub `index.html` at the old path that redirects, so codes already in the wild
keep working:

```html
<!doctype html>
<meta charset="utf-8">
<link rel="canonical" href="https://bagouri.uk/prehab/NEW-PATH/">
<meta http-equiv="refresh" content="0; url=https://bagouri.uk/prehab/NEW-PATH/">
<p>This page has moved to <a href="https://bagouri.uk/prehab/NEW-PATH/">its new address</a>.</p>
```

## Regenerating

Only needed if a URL changes or you want different colours or sizes.

```bash
pip install segno
```

```python
import segno
targets = {
  "prehab-hub":          "https://bagouri.uk/prehab/",
  "prehab-hip":          "https://bagouri.uk/prehab/hip/",
  "prehab-knee":         "https://bagouri.uk/prehab/knee/",
  "prehab-hip-anterior": "https://bagouri.uk/prehab/hip-muscle-sparing/",
}
for name, url in targets.items():
    q = segno.make(url, error='h')
    q.save(f"{name}.svg", scale=10, border=4, dark="#13264A")
    q.save(f"{name}.png", scale=14, border=4, dark="#13264A", light="#FFFFFF")
```

## Always verify after regenerating

Decode the image rather than trusting the generator, and check the target
actually serves over HTTPS:

```bash
curl -sI -o /dev/null -w "%{http_code}\n" https://bagouri.uk/prehab/
```

On macOS, decode with CoreImage (no extra dependencies):

```swift
import Foundation
import CoreImage
let ctx = CIContext()
let det = CIDetector(ofType: CIDetectorTypeQRCode, context: ctx,
                     options: [CIDetectorAccuracy: CIDetectorAccuracyHigh])!
for path in CommandLine.arguments.dropFirst() {
    guard let img = CIImage(contentsOf: URL(fileURLWithPath: path)) else { continue }
    let msgs = det.features(in: img).compactMap { ($0 as? CIQRCodeFeature)?.messageString }
    print("\((path as NSString).lastPathComponent): \(msgs.joined(separator: " | "))")
}
```

Then scan a real printed card with a real phone before any of it reaches a
patient. Digital verification does not prove ink on paper.
