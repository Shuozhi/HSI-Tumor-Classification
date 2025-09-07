
import os, numpy as np
from model import simulate_phi_rho

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTDIR, exist_ok=True)

snaps, phi, rho = simulate_phi_rho(N=96, steps=450, dt=0.02, seed=5,
                                   a=-0.35, b=1.0, c=1.0, gamma=1.2, K=1.0, D_rho=0.6)

phi_final = phi.copy()
binary_mask = (phi_final > 0.0).astype(float)

np.savez(os.path.join(OUTDIR, "figure4_pattern.npz"),
         phi_final=phi_final, binary_mask=binary_mask)
print("Saved:", os.path.join(OUTDIR, "figure4_pattern.npz"))
