
import os, numpy as np
from model import dispersion_relation, simulate_phi_rho, radial_structure_factor

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTDIR, exist_ok=True)

ks = np.linspace(0.0, 2.5, 256)
lam_plus, lam_minus = dispersion_relation(ks, a=-0.35, gamma=1.2, K=1.0, D_rho=0.6, c=1.0)
lambda_example = np.real(lam_plus)

snaps, phi, rho = simulate_phi_rho(N=96, steps=450, dt=0.02, seed=7,
                                   a=-0.35, b=1.0, c=1.0, gamma=1.2, K=1.0, D_rho=0.6)
kbins, Sk = radial_structure_factor(phi)

np.savez(os.path.join(OUTDIR, "supp_s2_dispersion_Sk.npz"),
         ks=ks, lambda_example=lambda_example, kbins=kbins, Sk=Sk)
print("Saved:", os.path.join(OUTDIR, "supp_s2_dispersion_Sk.npz"))
