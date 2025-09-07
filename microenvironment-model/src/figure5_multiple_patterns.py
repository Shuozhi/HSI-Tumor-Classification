
import os, numpy as np
from model import simulate_phi_rho

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTDIR, exist_ok=True)

params = dict(N=96, steps=430, dt=0.02, a=-0.38, b=1.0, c=1.0, gamma=1.1, K=1.0, D_rho=0.6)
seeds = [0, 1, 2, 3]
bins, raws = {}, {}
for idx, s in enumerate(seeds):
    snaps, phi, rho = simulate_phi_rho(seed=s, **params)
    bins[chr(ord('A')+idx)] = (phi > 0.0).astype(float)
    raws[chr(ord('A')+idx)] = phi

np.savez(os.path.join(OUTDIR, "figure5_patterns.npz"),
         A=bins['A'], B=bins['B'], C=bins['C'], D=bins['D'],
         A_raw=raws['A'], B_raw=raws['B'], C_raw=raws['C'], D_raw=raws['D'])
print("Saved:", os.path.join(OUTDIR, "figure5_patterns.npz"))
