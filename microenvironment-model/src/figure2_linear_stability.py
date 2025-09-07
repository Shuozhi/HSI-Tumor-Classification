
import os, numpy as np
from model import max_growth_rate_over_k

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTDIR, exist_ok=True)

a_vals = np.linspace(-1.0, 1.0, 81)
gamma_vals = np.linspace(0.25, 2.0, 71)
lambda_max = np.zeros((a_vals.size, gamma_vals.size))
k_star = np.zeros_like(lambda_max)

for i, a in enumerate(a_vals):
    for j, g in enumerate(gamma_vals):
        lam, kstar, ks, lamk = max_growth_rate_over_k(a=a, gamma=g, k_max=2.5, nk=256)
        lambda_max[i, j] = lam
        k_star[i, j] = kstar if lam > 0 else 0.0

np.savez(os.path.join(OUTDIR, "figure2_lambda_max.npz"),
         a_vals=a_vals, gamma_vals=gamma_vals, lambda_max=lambda_max, k_star=k_star)
print("Saved:", os.path.join(OUTDIR, "figure2_lambda_max.npz"))
