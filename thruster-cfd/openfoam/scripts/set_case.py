#!/usr/bin/env python3
"""Write the roughness (Ks) and rotation (omega) into an OpenFOAM case
from the single config file.  No external deps.

  python3 scripts/set_case.py --case . --material pla --rpm 2000 \
          --config config/cfd_config.yaml

material: smooth | resin|sla | pla|fdm   (maps to ks in the config)
"""
import argparse, re, math, pathlib, sys

MAP = {"smooth":"smooth", "resin":"A_SLA", "sla":"A_SLA",
       "pla":"B_FDM", "fdm":"B_FDM"}

def load_roughness(cfg):
    txt = pathlib.Path(cfg).read_text()
    ks = {}
    for key in ("smooth", "A_SLA", "B_FDM"):
        m = re.search(rf'^\s*{key}:\s*([0-9.eE+-]+)', txt, re.M)
        if m: ks[key] = float(m.group(1))
    return ks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default=".")
    ap.add_argument("--material", required=True)
    ap.add_argument("--rpm", type=float, required=True)
    ap.add_argument("--config", default="config/cfd_config.yaml")
    a = ap.parse_args()
    case = pathlib.Path(a.case)

    mat = MAP.get(a.material.lower())
    if mat is None:
        sys.exit(f"unknown material '{a.material}'  (use smooth|resin|pla)")
    ks = load_roughness(case/a.config)[mat]
    omega = 2*math.pi*a.rpm/60.0

    # 1) propeller Ks in 0/nut  (line carries the  'set by set_case.py'  marker)
    nut = case/"0"/"nut"
    t = nut.read_text()
    t = re.sub(r'(Ks\s+uniform\s+)[0-9.eE+-]+(;\s*//\s*<-- set by set_case\.py)',
               rf'\g<1>{ks:.6e}\g<2>', t)
    nut.write_text(t)

    # 2) omega in constant/MRFProperties
    mrf = case/"constant"/"MRFProperties"
    t = mrf.read_text()
    t = re.sub(r'(omega\s+)[0-9.eE+-]+(;)', rf'\g<1>{omega:.5f}\g<2>', t)
    mrf.write_text(t)

    print(f"[set_case] material={a.material} -> ks={ks*1e6:.1f} um ({ks:.3e} m); "
          f"rpm={a.rpm:.0f} -> omega={omega:.4f} rad/s")

if __name__ == "__main__":
    main()
