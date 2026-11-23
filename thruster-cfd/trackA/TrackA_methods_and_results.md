# Track A — Analytical bollard-pull prediction (MSU-T76 ducted thruster)

**Status:** preliminary estimate, *not* CFD. Purpose: give comparison numbers now, a
fallback before the Dec 3 deadline, and a physical frame for the CFD/test. All inputs live in
`config/cfd_config.yaml` (one file — replace defaults with your measured values).

## 1. Geometry verification (from your STL — PASS)
`MSU-T76_D2_propeller_PD0.6_quote-light.stl`

| Quantity | Spec | Measured | |
|---|---|---|---|
| Bounding box | ~76×76×20 mm | 75.997 × 75.998 × 20.000 mm | ✅ units = mm |
| Volume | ≈7,788 mm³ | 7,788.39 mm³ | ✅ |
| Tip diameter | 76 mm | 76.00 mm (R_tip 38.00) | ✅ |
| Watertight | yes | yes, 1 body, winding-consistent | ✅ |
| Topology | — | genus 1 → shaft bore Ø5.2 mm | ✅ expected |
| Orientation | shaft axis | already on +Z, centred X/Y, Z 0→20 | ✅ no re-orient |

Notes: this is the *quote-light* (decimated, 68k-tri) export — dimensionally perfect but use the
STEP from `MSU-T76_demo_rig_RevB_package.zip` for the final mesh. **Tip clearance not yet
checked** — needs the duct geometry.

## 2. Method
- Thrust `T = KT · ρ n² D⁴`, torque `Q = KQ · ρ n² D⁵`, power `P = 2π n Q`, with `n` in rev/s.
- Baseline `KT_total0`, `KQ0` = Ka 4-70 / 19A nozzle, P/D 0.6, at J=0 (**nominal — verify vs
  Oosterveld 1970 / Carlton**).
- Roughness effect via **ITTC-1978** propeller correction at 0.75R:
  `ΔC_D = (2+4·t/c)·(1.89+1.62·log₁₀(c/kₛ))^−2.5`,
  `ΔKT = −0.3·(P/D)·(cZ/D)·ΔC_D`, `ΔKQ = +0.25·(cZ/D)·ΔC_D`.
- Roughness-Reynolds `kₛ⁺ = kₛ·u_τ/ν`, `u_τ = V₀.₇R·√(C_f/2)`, `C_f` = ITTC smooth line.
  Regime: `kₛ⁺<5` smooth · `5–70` transitional · `>70` fully rough.

## 3. Results

**Roughness regime (robust, geometry-based):**

| Prop | kₛ | kₛ⁺ (1500→2000 rpm) | Regime |
|---|---|---|---|
| A — SLA resin | 10 µm | 2.7 → 3.4 | hydraulically **smooth** |
| B — FDM PLA | 80 µm | 21 → 27 | **transitional** |

**Absolute prediction (nominal KT₀=0.55, KQ₀=0.048 — verify):**

| rpm | Thrust ≈ | Torque A | Torque B | Power A→B | Re₀.₇R | σ_tip |
|---|---|---|---|---|---|---|
| 1500 | 11.4 N | 83.8 mN·m | 89.6 mN·m | 13.2→14.1 W | 1.09e5 | 5.7 |
| 1750 | 15.5 N | 114 mN·m | 122 mN·m | 20.9→22.3 W | 1.27e5 | 4.2 |
| 2000 | 20.2 N | 149 mN·m | 159 mN·m | 31.2→33.4 W | 1.45e5 | 3.2 |

(Full machine-readable table: `predictions_trackA.csv`.)

## 4. Interpretation (what to put in the paper)
1. **Print method shows up in torque, not thrust.** Thrust differs <0.5% between A and B;
   the roughness penalty is a friction effect → it raises torque and lowers efficiency.
2. **SLA ≈ hydraulically smooth; FDM = transitional.** This is the central result: at these
   rpm the 10 µm SLA surface barely perturbs the flow, while the 80 µm FDM surface does.
3. **Magnitude is uncertain by design.** ITTC-78 is a *fully-rough* correlation, so its ~+7%
   torque penalty (B vs A) is an **upper bound** — the true transitional-regime value is smaller.
   Pinning it needs a transitional roughness wall-function in CFD **and** your bollard test. The
   difficulty of predicting the transitional regime is itself a paper-worthy point.
4. **Cavitation not excluded at 2000 rpm** (σ_tip=3.2). Report −Cp_min from CFD against this.
5. **Transitional blade Reynolds** (~1e5) → consider a transition-sensitive turbulence model.

## 5. Caveats / to refine
- `KT_total0`, `KQ0`: replace nominal values with the actual Ka4-70/19A series data.
- `chord_075R`, `t/c`: estimated from EAR; refine from the CAD (weak effect, but do it).
- Tip-gap unknown until duct CAD arrives — and tip gap strongly sets ducted thrust.
- Ra→kₛ conversion for your prints should come from a measurement, not the 10/80 µm defaults.
