#!/usr/bin/env python3
"""Read the solved forces and report thrust / torque / KT / KQ / power.
Handles both OpenFOAM force-output styles (force.dat+moment.dat, or forces.dat).

  python3 scripts/post.py --case . --material pla --rpm 2000
Appends a row to results.csv in the case directory.
"""
import argparse, pathlib, re, csv, sys

RHO = 998.2
D   = 0.076

def last_data_line(p):
    rows = [l for l in p.read_text().splitlines() if l.strip() and not l.lstrip().startswith("#")]
    return rows[-1] if rows else None

def nums(line):
    return [float(x) for x in re.sub(r'[()]', ' ', line).split()]

def read_force_moment(fdir):
    """Return (Fz_total, Mz_total) for one forces function-object directory."""
    fdir = pathlib.Path(fdir)
    times = sorted([d for d in fdir.iterdir() if d.is_dir()], key=lambda d: float(d.name))
    if not times: sys.exit(f"no time dirs in {fdir}")
    t = times[-1]
    if (t/"force.dat").exists():                      # ESI style
        f = nums(last_data_line(t/"force.dat"));  Fz = f[3]          # total force z
        m = nums(last_data_line(t/"moment.dat")); Mz = m[3]          # total moment z
    else:                                             # single forces.dat
        v = nums(last_data_line(t/"forces.dat"))
        # time, pressure(xyz), viscous(xyz), [porous(xyz)], then moments...
        Fz = v[3] + v[6]
        # moments begin after the force block (9 or 12 comps)
        off = 10 if len(v) >= 19 else 10
        Mz = v[off+2] + v[off+5]
    return Fz, Mz

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default=".")
    ap.add_argument("--material", required=True)
    ap.add_argument("--rpm", type=float, required=True)
    a = ap.parse_args()
    case = pathlib.Path(a.case); pp = case/"postProcessing"
    n = a.rpm/60.0

    Fz_p, Mz_p = read_force_moment(pp/"forces_propeller")
    try:
        Fz_d, _ = read_force_moment(pp/"forces_duct")
    except SystemExit:
        Fz_d = 0.0

    Mz_p = abs(Mz_p)          # report shaft-torque magnitude (sign = rotation dir only)
    T_total = Fz_p + Fz_d
    KT_tot  = T_total / (RHO*n**2*D**4)
    KT_prop = Fz_p   / (RHO*n**2*D**4)
    KQ      = Mz_p   / (RHO*n**2*D**5)
    P       = 2*3.141592653589793*n*Mz_p

    row = dict(material=a.material, rpm=int(a.rpm),
               thrust_N=round(T_total,3), thrust_prop_N=round(Fz_p,3),
               thrust_duct_N=round(Fz_d,3), torque_Nm=round(Mz_p,5),
               power_W=round(P,3), KT_total=round(KT_tot,4),
               KT_prop=round(KT_prop,4), KQ=round(KQ,5), tenKQ=round(10*KQ,4))
    print("[post]", row)
    out = case/"results.csv"
    new = not out.exists()
    with out.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(row));
        if new: w.writeheader()
        w.writerow(row)
    print("[post] appended to", out)

if __name__ == "__main__":
    main()
