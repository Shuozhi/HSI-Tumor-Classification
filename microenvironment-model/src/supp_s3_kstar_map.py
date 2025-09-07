
import os, numpy as np
from model import max_growth_rate_over_k

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTDIR, exist_ok=True)

a_vals = np.linspace(-1.0, 1.0, 81)
gamma_vals = np.linspace(0.25, 2.0, 71)
k_star = np.zeros((a_vals.size, gamma_vals.size))

for i, a in enumerate(a_vals):
    for j, g in enumerate(gamma_vals):
        lam, kstar, ks, lamk = max_growth_rate_over_k(a=a, gamma=g, k_max=2.5, nk=256)
        k_star[i, j] = kstar if lam > 0 else 0.0

dka = np.gradient(k_star, a_vals, axis=0)
dkg = np.gradient(k_star, gamma_vals, axis=1)

np.savez(os.path.join(OUTDIR, "supp_s3_kstar_map.npz"),
         a_vals=a_vals, gamma_vals=gamma_vals, k_star=k_star, dka=dka, dkg=dkg)
print("Saved:", os.path.join(OUTDIR, "supp_s3_kstar_map.npz"))
