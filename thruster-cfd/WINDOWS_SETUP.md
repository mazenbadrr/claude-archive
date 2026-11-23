# Run the MSU-T76 CFD package on Windows (WSL2 + OpenFOAM)

OpenFOAM is Linux software; on Windows it runs inside **WSL2** (a built-in Ubuntu).
One-time setup is ~30–60 min. After that, each case is 2 commands.

---

## STEP 1 — Install WSL2 (Ubuntu)
Open **PowerShell as Administrator** and run:
```powershell
wsl --install -d Ubuntu
```
Reboot if it asks. When Ubuntu opens, create a username + password (remember them).
(If `wsl --install` says it's already installed, just open "Ubuntu" from the Start menu.)

## STEP 2 — Install OpenFOAM inside Ubuntu
In the **Ubuntu** window:
```bash
curl https://dl.openfoam.com/add-debian-repo.sh | sudo bash
sudo apt-get update
sudo apt-get install -y openfoam2312-default paraview
```
If the first line fails, use the Ubuntu-packaged build instead:
```bash
sudo apt-get update && sudo apt-get install -y openfoam paraview
```

## STEP 3 — Get the package into Ubuntu
You downloaded `MSU-T76_CFD_package.zip` from the chat to your Windows **Downloads**.
Pull it into Ubuntu and unzip (replace `YOURNAME` with your Windows user folder):
```bash
cd ~
cp /mnt/c/Users/YOURNAME/Downloads/MSU-T76_CFD_package.zip .
sudo apt-get install -y unzip && unzip MSU-T76_CFD_package.zip
cd cfd/openfoam
```

## STEP 4 — Turn on OpenFOAM, then run a case
```bash
source /usr/lib/openfoam/openfoam2312/etc/bashrc
./Allrun resin 2000
./Allrun pla 2000
cat results.csv
```
(For the Ubuntu-packaged build, step the source line is `source /usr/share/openfoam/etc/bashrc`
or just run `openfoam2312` / `openfoam` to enter the environment — whichever your install created.)

`results.csv` gives thrust, torque, KT, KQ, power for each run.
Run the whole 9-case matrix instead with: `./run_all.sh`

## STEP 5 — The CFD renders (pressure, velocity, streamlines)
Easiest: open the result in the ParaView GUI.
```bash
paraview case.foam &
```
In ParaView: click **Apply**, set the time to the last step, colour by **p** (pressure) or **U**
(velocity), add **Slice** and **Stream Tracer** filters. Or auto-generate the images:
```bash
pvbatch paraview/render.py case.foam out resin_2000
```
→ `out/pressure_blades_*.png`, `velocity_slice_*.png`, `streamlines_*.png`, `spin_*.mp4`.
Put resin + PLA side by side:
```bash
python3 scripts/compare_images.py out/pressure_blades_resin_2000.png out/pressure_blades_pla_2000.png out/compare_2000.png
```

---

## Notes
- First `./Allrun` is the slow one (it meshes). A case on a typical laptop (4–8 cores) is
  ~20–90 min depending on mesh size. Edit `system/snappyHexMeshDict` levels to trade speed/accuracy.
- Match `system/decomposeParDict` `numberOfSubdomains` to your core count (check with `nproc`).
- Change roughness only in `config/cfd_config.yaml`. Full guide: `README.md` in the package.
- Windows files are reachable from Ubuntu under `/mnt/c/...`, and your Ubuntu home is at
  `\\wsl$\Ubuntu\home\YOURNAME` from Windows Explorer.
