
import os, numpy as np
from model import radial_structure_factor

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTDIR, exist_ok=True)

data = np.load(os.path.join(OUTDIR, "figure3_snapshots.npz"))
phi_t3 = data["phi_t3"]
kbins, Sk = radial_structure_factor(phi_t3)

np.savez(os.path.join(OUTDIR, "supp_s4_Sk_from_fig3.npz"), kbins=kbins, Sk=Sk)
print("Saved:", os.path.join(OUTDIR, "supp_s4_Sk_from_fig3.npz"))
