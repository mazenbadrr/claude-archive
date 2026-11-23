#!/usr/bin/env python3
# Professional CFD renders from a solved case — run with ParaView's pvbatch:
#   pvbatch paraview/render.py <case.foam> <out_dir> <label>
# Produces: pressure_blades.png, velocity_slice.png, streamlines.png, spin.mp4
#
# ParaView's Python API shifts between versions; patch/region names below may
# need a tweak for your build (check reader.MeshRegions / .CellArrays).
import sys
from paraview.simple import *

casefoam = sys.argv[1] if len(sys.argv) > 1 else "case.foam"
outdir   = sys.argv[2] if len(sys.argv) > 2 else "."
label    = sys.argv[3] if len(sys.argv) > 3 else "case"

def newreader(regions):
    r = OpenFOAMReader(FileName=casefoam)
    try: r.SkipZeroTime = 0
    except Exception: pass
    r.CellArrays = ['U', 'p']
    r.MeshRegions = regions
    UpdatePipeline()
    return r

scene = GetAnimationScene(); scene.UpdateAnimationUsingDataTimeSteps(); scene.GoToLast()

# ---------- 1) pressure on the blades ----------
prop = newreader(['propeller'])
v = GetActiveViewOrCreate('RenderView'); v.ViewSize = [1400, 1050]; v.OrientationAxesVisibility = 0
d = Show(prop, v); ColorBy(d, ('CELLS', 'p')); d.RescaleTransferFunctionToDataRange(True, False)
pLUT = GetColorTransferFunction('p'); pLUT.ApplyPreset('Cool to Warm (Extended)', True)
sb = GetScalarBar(pLUT, v); sb.Title = 'p / rho  [m^2/s^2]'; sb.ComponentTitle = ''
v.ResetCamera(); v.CameraPosition = [0.16, 0.12, 0.09]; v.CameraFocalPoint = [0, 0, 0.01]
Render(); SaveScreenshot(f"{outdir}/pressure_blades_{label}.png", v, ImageResolution=[1400, 1050])

# spin animation of the blade pressure
cam = GetActiveCamera()
import os
os.makedirs(f"{outdir}/_frames_{label}", exist_ok=True)
for i in range(72):
    cam.Azimuth(5); Render()
    SaveScreenshot(f"{outdir}/_frames_{label}/f{i:03d}.png", v, ImageResolution=[1000, 820])
# stitch with ffmpeg if available
os.system(f"ffmpeg -y -framerate 20 -i {outdir}/_frames_{label}/f%03d.png "
          f"-pix_fmt yuv420p {outdir}/spin_{label}.mp4 >/dev/null 2>&1")

# ---------- 2) velocity slice + streamlines (water through the duct) ----------
Hide(d, v)
vol = newreader(['internalMesh'])
sl = Slice(Input=vol); sl.SliceType = 'Plane'
sl.SliceType.Origin = [0, 0, 0.01]; sl.SliceType.Normal = [0, 1, 0]
ds = Show(sl, v); ColorBy(ds, ('POINTS', 'U', 'Magnitude')); ds.RescaleTransferFunctionToDataRange(True, False)
GetColorTransferFunction('U').ApplyPreset('Turbo', True)
v.CameraPosition = [0, -0.5, 0.02]; v.CameraFocalPoint = [0, 0, 0.02]; v.CameraViewUp = [0, 0, 1]
Render(); SaveScreenshot(f"{outdir}/velocity_slice_{label}.png", v, ImageResolution=[1400, 1050])

st = StreamTracer(Input=vol, SeedType='High Resolution Line Source')
st.Vectors = ['POINTS', 'U']; st.MaximumStreamlineLength = 1.0
st.SeedType.Point1 = [-0.06, 0, -0.08]; st.SeedType.Point2 = [0.06, 0, -0.08]; st.SeedType.Resolution = 60
tube = Tube(Input=st); tube.Radius = 0.0007
dt = Show(tube, v); ColorBy(dt, ('POINTS', 'U', 'Magnitude'))
Render(); SaveScreenshot(f"{outdir}/streamlines_{label}.png", v, ImageResolution=[1400, 1050])
print("renders written to", outdir)
