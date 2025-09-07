
import os, numpy as np
from model import dispersion_relation

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTDIR, exist_ok=True)

ks = np.linspace(0.0, 2.5, 256)
gamma_list = [0.5, 0.9, 1.2, 1.6]
a_fixed = -0.4
L = []
for g in gamma_list:
    lam_plus, lam_minus = dispersion_relation(ks, a=a_fixed, gamma=g, K=1.0, D_rho=0.6, c=1.0)
    L.append(np.real(lam_plus))
lambdas_plus = np.array(L)

np.savez(os.path.join(OUTDIR, "supp_s1_dispersion.npz"),
         ks=ks, lambdas_plus=lambdas_plus, gamma_list=np.array(gamma_list), a_fixed=a_fixed)
print("Saved:", os.path.join(OUTDIR, "supp_s1_dispersion.npz"))
