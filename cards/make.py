#!/usr/bin/env python3
"""
Generates the personal card sheet, the vCard, and the vCard QR.

    pip install segno
    python3 make.py

Outputs, all into this directory:
    bagouri.vcf        vCard 3.0 - the file to email or AirDrop
    vcard-qr.svg/.png  QR encoding that vCard - scan to save the contact
    cards.html         A4 sheet, 10 personal cards, open and print at 100%

The card's own QR points at the prehabilitation hub, NOT at the vCard: a card
handed to a patient in clinic exists to get them to their guide. The vCard QR
is the separate artefact, for colleagues and referrers.
"""

import html
import pathlib

import segno

# ---------------------------------------------------------------------------
# EDIT THIS BLOCK. Anything left as None prints as a visible amber placeholder
# on the card, so it cannot reach a printer unnoticed.
# ---------------------------------------------------------------------------
CONFIG = {
    "given_name":  "Elmunzar",
    "family_name": "Bagouri",
    # As it should print, e.g. "Mr Elmunzar Bagouri" - title matters for surgeons.
    "display_name": "Mr Elmunzar Bagouri",
    # e.g. "MBBS, FRCS (Tr&Orth)"
    "post_nominals": "MBBS, CCT, MBA, FRCS (Tr&Orth)",
    # e.g. "Consultant Orthopaedic Surgeon"
    "job_title": "Consultant Trauma and Lower Limb Arthroplasty Surgeon",
    # e.g. "Hip and knee replacement"
    "subspecialty": None,
    # e.g. ["Mid Yorkshire Teaching NHS Trust", "Spire Methley Park Hospital"]
    "hospitals": None,

    # Known and confirmed.
    "secretary_name": "Evy Sennett",
    "secretary_tel":  "01924 543584",
    "private_tel":    "01977 518518",   # Spire Methley Park - the PRIVATE route
    "email":          "enquiries@bagouri.uk",
    "website":        "bagouri.uk",
    "prehab_url":     "https://bagouri.uk/prehab/",
}

HERE = pathlib.Path(__file__).parent
NAVY, TEAL = "#13264A", "#0E7C7B"


def field(key):
    """A confirmed value, or a marked placeholder."""
    v = CONFIG.get(key)
    return v if v else f"[{key.replace('_', ' ')}]"


def missing():
    return [k for k, v in CONFIG.items() if v is None]


# ---------------------------------------------------------------------------
# vCard 3.0 - the format Contacts, Outlook and Android all import cleanly.
# ---------------------------------------------------------------------------
def build_vcard():
    org = "; ".join(CONFIG["hospitals"]) if CONFIG["hospitals"] else "[hospitals]"
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{CONFIG['family_name']};{CONFIG['given_name']};;;",
        f"FN:{field('display_name')}",
        f"TITLE:{field('job_title')}",
        f"ORG:{org}",
        # Two work numbers save as indistinguishable entries unless labelled.
        # PREF marks the NHS secretary as the default; X-ABLabel names each one
        # in Apple Contacts, and the NOTE repeats both for everything else.
        f"TEL;TYPE=WORK,VOICE;PREF=1:{CONFIG['secretary_tel']}",
        f"item1.TEL;TYPE=WORK,VOICE:{CONFIG['private_tel']}",
        "item1.X-ABLabel:Private - Spire Methley Park",
        f"EMAIL;TYPE=WORK,INTERNET:{CONFIG['email']}",
        f"URL:https://{CONFIG['website']}",
        (f"NOTE:NHS patients - secretary ({CONFIG['secretary_name']}) {CONFIG['secretary_tel']}. "
         f"Private patients - Spire Methley Park {CONFIG['private_tel']}. "
         f"Prehabilitation guides for patients: {CONFIG['prehab_url']}"),
        "END:VCARD",
    ]
    # vCard requires CRLF line endings; some Android importers reject LF-only.
    return "\r\n".join(lines) + "\r\n"


def main():
    vcf = build_vcard()
    (HERE / "bagouri.vcf").write_text(vcf, encoding="utf-8")

    # Error correction M, not H: a vCard carries far more data than a URL, and H
    # would push the code dense enough to be slow to scan at card size.
    q = segno.make(vcf, error="m")
    q.save(HERE / "vcard-qr.svg", scale=10, border=4, dark=NAVY)
    q.save(HERE / "vcard-qr.png", scale=14, border=4, dark=NAVY, light="#FFFFFF")

    ph = ' style="background:#FEF6EC;border:1px dashed #C08A3E;padding:0 3px"'

    def esc(v, key):
        val = field(key)
        marked = CONFIG.get(key) is None
        return f"<span{ph}>{html.escape(val)}</span>" if marked else html.escape(val)

    if CONFIG["hospitals"]:
        hospitals_html = html.escape(" · ".join(CONFIG["hospitals"]))
    else:
        hospitals_html = f'<span{ph}>[hospitals]</span>'

    card = f"""    <div class="card">
      <div class="who">
        <p class="name">{esc(None, 'display_name')}<span class="pn">{esc(None, 'post_nominals')}</span></p>
        <p class="role">{esc(None, 'job_title')}</p>
        <p class="sub">{esc(None, 'subspecialty')}</p>
        <p class="hosp">{hospitals_html}</p>
        <p class="lines">
          <span>{html.escape(CONFIG['secretary_name'])} &middot; {html.escape(CONFIG['secretary_tel'])}</span>
          <span>Private &middot; {html.escape(CONFIG['private_tel'])}</span>
          <span>{html.escape(CONFIG['email'])}</span>
        </p>
      </div>
      <div class="scan">
        <img src="../qr/prehab-hub.svg" alt="QR code to bagouri.uk/prehab">
        <p class="cap">Preparing for surgery</p>
        <p class="web">{html.escape(CONFIG['website'])}/prehab</p>
      </div>
    </div>"""

    doc = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Personal cards - 10 per A4</title>
<style>
  *{{box-sizing:border-box}}
  body{{margin:0;background:#EEF1F6;
       font:12px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:#16202E}}
  .sheet{{width:210mm;height:297mm;margin:0 auto;background:#fff;padding:11mm 20mm;
          display:grid;grid-template-columns:85mm 85mm;grid-auto-rows:55mm;
          justify-content:center;align-content:start}}
  .card{{width:85mm;height:55mm;border:.4pt dashed #B6C0CE;padding:5mm;
         display:flex;gap:3.5mm;align-items:center;overflow:hidden}}
  .who{{flex:1;min-width:0}}
  .name{{margin:0;font-size:11pt;font-weight:700;color:{NAVY};line-height:1.15}}
  .pn{{display:block;font-size:7.5pt;font-weight:600;color:#4A5568;margin-top:.6mm}}
  .role{{margin:1.4mm 0 0;font-size:8pt;font-weight:600;color:{TEAL}}}
  .sub{{margin:.4mm 0 0;font-size:7.5pt;color:#4A5568}}
  .hosp{{margin:1.6mm 0 0;font-size:7pt;color:#4A5568;line-height:1.3}}
  .lines{{margin:2.2mm 0 0;font-size:7pt;color:#16202E;line-height:1.45}}
  .lines span{{display:block}}
  .scan{{width:24mm;text-align:center;flex:none}}
  .scan img{{width:24mm;height:24mm;display:block}}
  .cap{{margin:1mm 0 0;font-size:6pt;letter-spacing:.06em;text-transform:uppercase;color:{TEAL};font-weight:700}}
  .web{{margin:.4mm 0 0;font-size:6.5pt;font-weight:700;color:{NAVY}}}
  @media print{{
    body{{background:#fff}}
    .sheet{{margin:0}}
    @page{{size:A4;margin:0}}
  }}
</style>
</head>
<body>
<div class="sheet">
{chr(10).join([card] * 10)}
</div>
</body>
</html>
"""
    (HERE / "cards.html").write_text(doc, encoding="utf-8")

    print(f"bagouri.vcf      {len(vcf)} bytes")
    print(f"vcard-qr.svg/png QR version {q.version}, error correction M")
    print("cards.html       10 cards per A4")
    m = missing()
    print(f"\nSTILL PLACEHOLDER ({len(m)}): {', '.join(m)}" if m
          else "\nAll fields confirmed - safe to print.")


if __name__ == "__main__":
    main()
