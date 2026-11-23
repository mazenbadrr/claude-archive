# MSU-T76 ducted thruster — OpenFOAM CFD package (SLA vs FDM roughness)

Steady **MRF RANS** (simpleFoam, k-ω SST, incompressible) of the bollard (J=0) ducted
thruster, set up to compare the two print finishes through **equivalent sand-grain
roughness kₛ**. Authored to run on a capable workstation/HPC — **not** a 4-core cloud box.

> ⚠️ **Authored & syntax-checked, NOT yet run.** No OpenFOAM was available where this was
> built, so you must do a first test run and expect to tune mesh levels / residuals. Every
> file is standard OpenFOAM; the physics choices are documented inline.

## 0. Prerequisites
- **OpenFOAM** v2212/v2312 (ESI, `openfoam.com`) — or Foundation `openfoam.org` v11/12 (the
  `surfaceFeatures`/`surfaceFeatureExtract` fallback in `Allrun` covers both).
- **Python 3** (standard library only — scripts have no external deps).
- **ParaView** (`pvbatch`) for the renders. `ffmpeg` for the spin animation (optional).
- Source the environment first, e.g. `source /usr/lib/openfoam/openfoam2312/etc/bashrc`.

## 1. What's here
```
config/cfd_config.yaml     <- SINGLE source of truth: kₛ (10/80/0 µm), rpm, fluid, duct
geometry/                  prop.stl (D=76 mm, verified), duct.stl (nominal 19A, 1 mm gap)
constant/                  transportProperties, turbulenceProperties, MRFProperties, triSurface/
0.orig/                    U p k omega nut   (roughness enters in nut: nutkRoughWallFunction)
system/                    blockMesh, snappyHexMesh (+ MRF cellZone), schemes, solution, forces
scripts/set_case.py        writes kₛ + omega from the config into the case
scripts/post.py            forces -> thrust, torque, KT, KQ, power  (results.csv)
Allrun / Allclean          run / clean ONE case:  ./Allrun <material> <rpm>
run_all.sh                 all 9 cases (resin/pla/smooth × 1500/1750/2000) -> results_all.csv
paraview/render.py         pvbatch: pressure-on-blades, velocity slice, streamlines, spin.mp4
```

## 2. Run one case
```bash
source <openfoam>/etc/bashrc
./Allrun resin 2000      # material = smooth | resin | pla ;  rpm
cat results.csv          # thrust_N, torque_Nm, KT, KQ, power_W ...
```
`Allrun` meshes (blockMesh → snappyHexMesh, building the MRF `rotatingZone`), writes the
roughness + rotation via `set_case.py`, solves, then `post.py` writes `results.csv`.

## 3. Run the full comparison (9 cases)
```bash
./run_all.sh             # writes runs/<mat>_<rpm>/ and results_all.csv
```

## 4. The renders you asked for
After a case finishes (creates `case.foam`):
```bash
pvbatch paraview/render.py runs/resin_2000/case.foam  out/  resin_2000
pvbatch paraview/render.py runs/pla_2000/case.foam    out/  pla_2000
```
→ `pressure_blades_*.png`, `velocity_slice_*.png`, `streamlines_*.png`, `spin_*.mp4`.
Put the resin + pla `pressure_blades` side by side for the comparison figure:
```bash
python3 scripts/compare_images.py out/pressure_blades_resin_2000.png \
        out/pressure_blades_pla_2000.png out/compare_pressure_2000.png
```

## 5. Change the roughness (your measured values)
Edit **only** `config/cfd_config.yaml` → `roughness:` (metres). Convert your measured Ra to
equivalent sand-grain kₛ (a common first estimate is kₛ ≈ 5.9·Ra; a flow-measured kₛ is
better). `set_case.py` writes it into `0/nut` (propeller `nutkRoughWallFunction.Ks`).

## 6. Drop in the REAL duct
`geometry/duct.stl` is a **nominal 19A** annulus (inner Ø78 mm → 1 mm tip gap). To use the
true duct: export just the duct solid from `MSU-T76_demo_rig_RevB_assembly.step` as an STL in
**metres**, aligned so the propeller axis is **+z** with the prop centred at the origin
(prop spans z=0→0.02 m). Replace `geometry/duct.stl` and `constant/triSurface/duct.stl`, set
`duct.inner_dia_m`/`tip_gap_m` in the config, and check the `rotatingZone` cylinder radius in
`system/snappyHexMeshDict` still sits in the gap (between tip 38 mm and the duct inner wall).

## 7. Reading the results
- **thrust_N** = axial force (propeller + duct).  **torque_Nm**, **power_W** = shaft.
- **KT** = T/(ρ n² D⁴), **KQ** = Q/(ρ n² D⁵), with n = rpm/60, D = 0.076 m, ρ = 998.2.
- Compare **resin vs pla** at each rpm: expect ~equal thrust, higher torque/power for PLA.
- Cavitation check: `postProcessing/minMaxP` min p → Cp_min; compare to σ from submergence.
- Check **y⁺** (`postProcessing/yPlus`) is in 30–300 for the wall functions; refine layers if not.

## 8. Known limitations / tuning
- Mesh levels in `snappyHexMeshDict` are a sensible start (~2–6 M cells); do a mesh-independence
  check before quoting final numbers.
- Steady MRF gives the time-averaged load — correct for bollard KT/KQ. For unsteady wake detail
  use a sliding-mesh (AMI) transient run (`pimpleFoam`) later.
- The transitional-roughness regime (kₛ⁺≈20 for PLA) is where k-ω SST rough wall functions are
  least certain — treat the SLA-vs-PLA Δ as indicative and validate against the bollard test.
- `0/k`, `0/omega` seeds are modest; if convergence stalls, lower relaxation or ramp.

Baseline analytical predictions (Track A) for sanity: ~11.4 / 15.5 / 20.2 N at 1500/1750/2000 rpm.
