# MSU-T76 ducted thruster — print-material (roughness) CFD study

Comparing two 3D-print finishes of the **same** propeller for the MSU-T76 ducted underwater
thruster, at bollard (J=0), at 1500 / 1750 / 2000 rpm:
- **A — SLA resin** (smooth, kₛ ≈ 10 µm)
- **B — FDM PLA** (rough layer lines, kₛ ≈ 80 µm)

Same geometry → the only flow difference is **surface roughness**. Headline result: **thrust is
≈equal; the rough PLA costs more torque/power** (lower efficiency). At equal *input power* the
smooth resin makes ~5% more thrust. _(IEGR 790, Morgan State — paper due 2026-12-03.)_

## Folders
| Path | What |
|---|---|
| `config/cfd_config.yaml` | **Single source of truth** — kₛ, rpm, fluid, propeller, duct |
| `trackA/` | Analytical prediction (ITTC-78): methods, `comparison_onepager.pdf/png`, graphs, `predictions_trackA.csv` |
| `renders/` | Propeller geometry render + rotation video; `compare_friction.png` (SLA vs FDM blade friction) |
| `flow/` | Actuator-disk slipstream colour field + `flow_through.mp4` (illustrative, not RANS) |
| `openfoam/` | **Full OpenFOAM + ParaView CFD package** — see its own `README.md` |
| `WINDOWS_SETUP.md` | How to run the OpenFOAM package on Windows (WSL2) |

## Status
- ✅ Geometry verified (prop D=76 mm, watertight), analytical comparison + figures done.
- ✅ OpenFOAM case authored & the Python plumbing verified (config→case, forces→KT/KQ).
- ⏳ **Not yet solved** — run `openfoam/` on a capable machine (your PC via WSL2, or the MSU cluster).

## Honesty notes (for the paper)
- `trackA` numbers are **analytical** (ITTC-78, fully-rough upper bound) — preliminary.
- `flow/` and `renders/compare_friction` are **engineering estimates, NOT RANS CFD** — labeled as such.
- Real solved pressure/velocity renders come from running `openfoam/`.
- The duct here is a **nominal 19A** (1 mm tip gap) — replace with the real duct from the RevB STEP.
- Series coefficients KT₀/KQ₀ in the config are nominal — verify against Oosterveld/Carlton.
