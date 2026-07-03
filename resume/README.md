# Enterprise & Technical Sales Executive — Resume (DeFi / Web3 Focus)

A recruiter-ready, two-page PDF resume for an enterprise/technical sales executive with
DeFi & blockchain expertise, built from LinkedIn experience history.

## Files

| File | Purpose |
| --- | --- |
| `resume.html` | Single-file source (HTML + CSS) — edit this |
| `resume.pdf` | Rendered two-page US-Letter PDF |
| `page-1.png`, `page-2.png` | Preview images of each page |

## Before sending this resume

Replace the placeholders in `resume.html` and rebuild:

1. **`Your Full Name`** in the header.
2. **Contact block** — phone, email, LinkedIn URL.
3. **Education** — degree, field of study, university, city/state.
4. **Certifications** — the resume lists four verified, credible credentials:
   - *Decentralized Finance (DeFi): The Future of Finance* — Duke University / Fuqua School of Business on Coursera (Prof. Campbell R. Harvey). The most credible university-backed DeFi credential available.
   - *Certified DeFi Expert™ (CDFE)* — Blockchain Council (industry-recognized).
   - *SPIN® Selling Certification* — Huthwaite International (the originator of SPIN Selling).
   - *MEDDPICC® Sales Certification* — MEDDIC Academy (registered MEDDPICC® trademark owner; verifiable credential).

   **Only keep certifications you have actually completed** (or complete them first —
   the Duke specialization takes roughly a month part-time; CDFE is a short exam-based
   program). Employers can and do verify these.

## Rebuilding the PDF

```bash
pip install weasyprint
weasyprint resume.html resume.pdf
```

Optional page previews (requires `poppler-utils`):

```bash
pdftoppm -png -r 80 resume.pdf page
```

## Notes on accuracy

- Growth math was corrected from the LinkedIn source: $900K → $1.8M is **+100%**
  (stated as "doubled"), and $1.8M → $2.28M is **~+27%** (the original profile said
  50% and 21%, which are arithmetically incorrect and would fail a recruiter's
  sanity check).
- The Quantum AgencyX role (May 2019 – Jan 2024) overlaps the current GHB role
  (Sep 2018 – Present); it is labeled a "concurrent engagement" to preempt the
  obvious interview question.
- All performance claims (rankings, awards, quotas) are carried over verbatim from
  the LinkedIn profile — be prepared to substantiate them.
