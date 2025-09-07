
import os, numpy as np
from model import simulate_phi_rho

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTDIR, exist_ok=True)

snaps, phi, rho = simulate_phi_rho(N=96, steps=400, dt=0.02, seed=2,
                                   a=-0.4, b=1.0, c=1.0, gamma=1.0, K=1.0, D_rho=0.6)
times = sorted(snaps.keys())
phi_t0 = snaps[times[0]]
phi_t1 = snaps[times[1]]
phi_t2 = snaps[times[2]]
phi_t3 = snaps[times[3]]

np.savez(os.path.join(OUTDIR, "figure3_snapshots.npz"),
         t_list=np.array(times), phi_t0=phi_t0, phi_t1=phi_t1, phi_t2=phi_t2, phi_t3=phi_t3)
print("Saved:", os.path.join(OUTDIR, "figure3_snapshots.npz"))
