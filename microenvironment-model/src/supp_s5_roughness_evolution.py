
import os, numpy as np
from model import simulate_phi_rho, front_roughness

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTDIR, exist_ok=True)

N=96; steps=420; dt=0.02
snaps, phi_final, rho_final = simulate_phi_rho(N=N, steps=steps, dt=dt, seed=11,
                                               a=-0.36, b=1.0, c=1.0, gamma=1.15, K=1.0, D_rho=0.6)

tlist = sorted(snaps.keys())
wlist = []
for t in tlist:
    phi_t = snaps[t]
    binary = (phi_t > 0.0).astype(float)
    wlist.append(front_roughness(binary))

np.savez(os.path.join(OUTDIR, "supp_s5_roughness_evolution.npz"),
         tlist=np.array(tlist), wlist=np.array(wlist))
print("Saved:", os.path.join(OUTDIR, "supp_s5_roughness_evolution.npz"))
