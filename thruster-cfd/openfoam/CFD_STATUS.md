# CFD status & what to tune next

## Where it stands (verified 2026-11-23, OpenFOAM 2312 on Windows/WSL2, 32 cores)
- ✅ **Pipeline runs end to end:** blockMesh → snappyHexMesh (prop + duct + MRF
  `rotatingZone`) → MRF `simpleFoam` → forces → `post.py` → `results.csv`.
- ✅ A first resin run produced a *plausible* result (~7.9 N, KT≈0.21) on the coarse mesh.
- ❌ **Not converged / not trustworthy yet:** repeat/clean runs **diverge** — thrust blows up to
  10³–10⁶ N, KT to huge negatives. First-order upwind + heavy under-relaxation (U=0.3) did **not**
  stabilize it. The steady MRF solve on this coarse mesh is numerically unstable.

## Most likely causes (in priority order)
1. **Mesh quality near the blades.** Coarse snappy, no boundary layers → skewed/`highAspect`
   cells on the thin blade edges. Check `checkMesh` (max non-orthogonality, skewness). This alone
   commonly causes divergence.
2. **Open far-field BCs.** `totalPressure` + `pressureInletOutletVelocity` on *all six* faces lets
   pressure drift and permits unstable recirculation at the "outlet". Prefer a **cylindrical
   domain** with a defined far inlet (low turbulence) and a single pressure **outlet**, or move the
   boundaries further out.
3. **No flow initialization.** Start from a `potentialFoam` solution (needs a `potentialFlow`
   sub-dict in `fvSolution` and a `Phi` solver) so `simpleFoam` doesn't start from a dead field.
4. **Turbulence startup.** `k`/`omega` seeds are rough; consider bounding (`limitFields`) and/or
   ramping `omega` (run a few hundred iters at lower rpm, then raise).
5. **Near-wall / rough wall functions.** Verify `y+` is in 30–300 for `nutkRoughWallFunction`;
   add 3–5 prism layers and re-check.

## Recommended path to a converged result
1. `checkMesh` and fix the worst cells first (add layers, raise `resolveFeatureAngle`, improve
   `meshQualityControls`).
2. Add `potentialFoam` initialization.
3. Switch to a cylindrical domain with inlet/outlet BCs.
4. Run with `simpleFoam`, **monitor residuals live** (`foamMonitor -l postProcessing/residuals/0/solverInfo.dat`
   or ParaView) — tune relaxation until residuals fall ~3–4 orders.
5. Mesh-independence study, then trust the numbers. Validate against the **bollard test**.
6. Only then quote KT/KQ and the SLA-vs-FDM delta.

Best done by someone who can watch residuals iterate (a CFD-savvy labmate, or on the MSU cluster)
— not through one-command round trips.

## For the Dec 3 paper (realistic)
- **Quantitative results:** the analytical prediction (`../trackA/`) + the **physical bollard test**.
- **CFD section:** methodology/setup + qualitative flow figures (`../flow/`, `../renders/`), clearly
  labeled; converged CFD + validation as **future work**.
- This is a legitimate, defensible Master's structure.
