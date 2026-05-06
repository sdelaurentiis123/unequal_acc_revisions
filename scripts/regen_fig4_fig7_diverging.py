#!/usr/bin/env python3
"""
Regenerate Fig 4 (lambda_mean_colormap.pdf) and Fig 7 (qdot_heatmap_new.pdf)
with diverging colormaps per Zoltan #3.

Fig 4: <lambda> centered at lambda=1 (preferential to secondary above, primary below).
Fig 7: <qdot> centered at qdot=0 (positive = q increasing toward 1, negative = away).

Both use 'seismic' colormap with TwoSlopeNorm.
"""

import numpy as np
import math
import pickle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path

V3_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = V3_DIR / "data"

qblist = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ecclist = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]

# ============================================================
# Fig 4: <lambda> diverging at lambda=1
# ============================================================

lambda_vals = np.zeros((len(qblist), len(ecclist)))
for i, qb in enumerate(qblist):
    for j, eb in enumerate(ecclist):
        path = DATA_DIR / "metrics_data" / f"data_eb_{eb}_qb_{qb}"
        with open(path, 'rb') as f:
            d = pickle.load(f)
        lam_full = d['mdot2'] / d['mdot1']
        meds = [np.median(lam_full[250+idx:]) for idx in np.arange(0, 105, 5)]
        lambda_vals[i, j] = np.mean(meds)

fig, ax = plt.subplots(figsize=(8, 6))
norm = mcolors.TwoSlopeNorm(vmin=lambda_vals.min(), vcenter=1.0, vmax=lambda_vals.max())
c = ax.imshow(
    lambda_vals,
    aspect="auto",
    origin="lower",
    cmap="seismic",   # red = preferential to secondary, blue = preferential to primary
    norm=norm,
    extent=[min(ecclist), max(ecclist), 0, max(qblist)],
)

ecclist_mod = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
qblist_mod = np.array(qblist) - 0.05
ax.set_xticks(np.array(ecclist_mod) + (ecclist_mod[1] - ecclist_mod[0]) / 2)
ax.set_yticks(qblist_mod)
ax.set_xticklabels(ecclist)
ax.set_yticklabels(qblist)

# In-cell value labels (black text on light cells, white on saturated)
for i in range(len(qblist)):
    for j in range(len(ecclist)):
        v = lambda_vals[i, j]
        # Heuristic: text color flips on light vs dark cells
        text_color = "black" if 0.7 < v < 2.0 else "white"
        ax.text(
            (np.array(ecclist_mod) + (ecclist_mod[1] - ecclist_mod[0]) / 2)[j],
            qblist_mod[i],
            f"{v:.2f}",
            ha="center", va="center", color=text_color, fontsize=8
        )

cbar = plt.colorbar(c, ax=ax)
cbar.set_label(r"$\langle \lambda \rangle$ (centered at $\lambda=1$)", fontsize=12)
ax.set_xlabel(r"$e_b$", fontsize=12)
ax.set_ylabel(r"$q_b$", fontsize=12)
plt.tight_layout()
fig.savefig(V3_DIR / "lambda_mean_colormap.pdf")
plt.close(fig)
print(f"Saved {V3_DIR / 'lambda_mean_colormap.pdf'}")
print(f"  lambda_vals range: {lambda_vals.min():.2f} to {lambda_vals.max():.2f}")
print(f"  Cells with <lambda> < 1 (preferential to primary): "
      f"{(lambda_vals < 1).sum()} / {lambda_vals.size}")

# ============================================================
# Fig 7: <qdot> diverging at qdot=0
# ============================================================

def eddington(M):
    G = 6.67430e-8; c = 3.0e10; sigma_T = 6.6524e-25; m_p = 1.6726e-24
    return (4 * math.pi * G * M * m_p) / (0.1 * sigma_T * c)

qdot = np.load(DATA_DIR / "qdot_data_magda.npy")
msol = 1.99e33
M = 2 * 1e7 * msol  # binary total
mdot_per_M = eddington(M) / M
qdot_scaled = qdot * mdot_per_M

print(f"  qdot_scaled range: {qdot_scaled.min():.2e} to {qdot_scaled.max():.2e}")

fig, ax = plt.subplots(figsize=(6, 6))
# Note: qdot_data_magda.npy is shape (10, 8) with rows from qb=1 to qb=0.1 (top to bottom)
# We want qb=0.1 at bottom, so flip
qdot_disp = qdot_scaled  # array is already arranged with row 0 = q=1 (top), row 9 = q=0.1 (bottom)
# imshow with origin='lower' means row 0 plotted at the bottom
# So we want to flip rows so qb=0.1 is at the bottom of the image
qdot_disp_flipped = qdot_disp[::-1]

vmax = max(abs(qdot_scaled.min()), abs(qdot_scaled.max()))
norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)
im = ax.imshow(
    qdot_disp_flipped,
    cmap='seismic',
    norm=norm,
    aspect="auto",
    origin="lower",
    extent=[min(ecclist), max(ecclist), 0, max(qblist)],
)
ax.set_xticks(np.array(ecclist_mod) + (ecclist_mod[1] - ecclist_mod[0]) / 2)
ax.set_yticks(qblist_mod)
ax.set_xticklabels(ecclist)
ax.set_yticklabels(qblist)

# Cell labels
for i in range(len(qblist)):
    for j in range(len(ecclist)):
        v = qdot_disp_flipped[i, j]
        text_color = "black" if abs(v) < 0.3*vmax else "white"
        ax.text(
            (np.array(ecclist_mod) + (ecclist_mod[1] - ecclist_mod[0]) / 2)[j],
            qblist_mod[i],
            f"{v:.2e}",
            ha="center", va="center", color=text_color, fontsize=6
        )

cbar = plt.colorbar(im, ax=ax)
cbar.set_label(r"$\langle \dot{q} \rangle$ ($\dot{M}_b / M_b$ units, centered at 0)", fontsize=10)
ax.set_xlabel(r"$e_b$", fontsize=12)
ax.set_ylabel(r"$q_b$", fontsize=12)
plt.tight_layout()
fig.savefig(V3_DIR / "qdot_heatmap_new.pdf")
plt.close(fig)
print(f"Saved {V3_DIR / 'qdot_heatmap_new.pdf'}")
