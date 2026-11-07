# claude-archive

A complete transfer of Mazen's work out of Claude (Cowork/desktop, claude.ai Projects, Artifacts) and
the connected Google Drive and Notion sources, captured as standalone files so nothing depends on a
Claude session staying alive. Everything here is a faithful copy; where a copy is imperfect or a file
could not be retrieved cleanly, it is called out below.

_Last updated: 2026-11-07_

## What's in here

| Folder | Contents | Count |
|---|---|---|
| `artifacts/` | Every Claude Artifact, saved as standalone HTML | 22 |
| `drive/` | Google Drive files (DURIP fs-CARS package + related) | 27 |
| `notion/` | Inventory of Notion content (see privacy note) | — |

---

## `artifacts/` — 22 Claude Artifacts

Each is a self-contained `.html` file; open in any browser.

### `rocketry/` (7) — Dr. Bussari rocketry lab mentoring
- `rocketry-mentoring-plan-nov2026-apr2027.html`
- `rocket-aerospace-mentoring-plan-cevien-thomas.html`
- `day1-welcome-to-the-rocket-lab.html`
- `day2-research-quest-newtons-laws-thrust.html`
- `sensor-engineer-lab.html`
- `rocket-sensor-scope-lab.html`
- `thrust-data-to-flight.html`

### `thrusters/` (4) — MSU-T76 additively-manufactured underwater thruster
- `msu-t76-two-propeller-bollard-experiment.html`
- `msu-t76-demo-rig-simulation-plan.html`
- `lake-clifton-test-pad.html`
- `background-lit-review-am-underwater-thruster.html` — **⚠ essentially empty** (title + byline only; the source document was never filled in)

### `proposals-qd/` (7) — Quick-disconnect hardware, ACCD/ONR, fs-CARS status
- `qd-rp1-100-release-sequence.html`
- `qd-rp1-100-release-sequence-v2.html`
- `qd-rp1-200-simple-kit.html`
- `work-summary-quick-disconnects-proposals.html`
- `accd-onr-application-field-guide.html`
- `fs-cars-accd-proposal-status.html`
- `army-report-test-stand-delay-inputs.html`

### `certs-coursework/` (4) — Certifications & coursework
- `solidworks-browser-exams-post.html`
- `draftsight-certification-poster.html`
- `soap-pump-challenge-poster.html`
- `hw3-ai-in-project-management-seminar-report.html`

**Fidelity note:** a few artifacts exported from Claude Docs/Slides reference images or slide assets
that were hosted as Claude service blobs; those won't render offline, but their alt text is preserved
in the HTML.

---

## `drive/` — Google Drive (27 files)

Mirror of the DURIP FY27 fs-CARS submission package and related documents, owned by
`mabad5@morgan.edu`. Every file here was verified byte-for-byte against Drive metadata.

### `durip-fscars/` — the submission package
- **`1 · Grants.gov PDFs/`** — 5 final grants-package PDFs (Technical Proposal, References Field 9,
  Facilities Field 10, Budget Justification, Budget Sheet)
- **`2 · Budget and quote tracker/`** — `DURIP_fsCARS_Budget_v4.xlsx`, `DURIP_FY27_Quote_Status_2026-11-03.pdf`
- **`3 · Vendor quotes/`** — 9 vendor quotes (LightConversion, Tibidabo, Zaber, BNC, Newport/MKS,
  Gentec, Crystran, OptiGrate)
- **`4 · Drawings and vendor-request files/`** — HEPA enclosure drawing, gas-panel schematic,
  spectrograph web-form text
- **`13 · DURIP FY27 — fs-CARS System — Full Proposal — v4.1.pdf`** — compiled full proposal
- **`final-pdfs/`** — a convenience copy of the 5 owned grants-package deliverables (identical bytes
  to the files in `1 · Grants.gov PDFs/`; kept as a "final deliverables" set)

### `other/`
- `Army_Report_Test_Stand_Delay_Inputs.pdf`
- `PWS-LC-FND-001_Rev3_Structural_Engineering_Services.pdf`

### ⚠ Two Drive files could not be transferred cleanly
These were **not** committed (a corrupt copy is worse than a clean gap). Their content is not lost —
it is reflected in files already archived here. To retrieve the originals, re-download by Drive ID in a
session where the download tool writes large results to disk, then `base64 -d`.

| File | Drive ID | Where its content already lives |
|---|---|---|
| `MSU_DURIP_fsCARS_Project_Abstract.pdf` | `1cGPZJQhgvnMtVT84p0tzeXEYVedxzGDV` | Abstract text appears in the full proposal (`13 · …v4.1.pdf`) and the grants package |
| `DURIP_Quote_Status_2026-11-04.xlsx` | `1gqbtOIkhUqJFbUrGTbDMVPPkoKwJM96J` | Same figures in `DURIP_FY27_Quote_Status_2026-11-03.pdf` and `DURIP_fsCARS_Budget_v4.xlsx` |

---

## `notion/` — inventory only (privacy)

`notion/README.md` is an **inventory** of what was in Notion, not a full copy. Sensitive personal
items found in Notion — government-issued IDs (driver's licenses) and a bank credit-card record —
were **deliberately not copied** into this repository, even though it is private. Retrieve those
directly from Notion if needed.

---

## Notes on this archive
- **DURIP is DoD grant material.** Treat the `drive/durip-fscars/` contents as potentially sensitive
  (distribution-limited) and share accordingly.
- Filenames use readable names and a middot (`·`) separator in the Drive folder names; these are valid
  and render correctly on GitHub.
- This archive is a snapshot. Ongoing work now lives in the separate `lab-vault` workspace.
