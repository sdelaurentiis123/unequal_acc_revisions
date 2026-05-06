#!/usr/bin/env python3
"""
Regen Fig 2 (sigma_lambda heatmap) with viridis perceptually-uniform colormap
(per Zoltan annotation 5.1, "recolor #1") and Fig 3 (<lambda> line plot) with
gray-shaded preferential-to-secondary region (per DIFF 26 / annotation 5.2).
"""
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pathlib import Path

V3_DIR = Path(__file__).resolve().parent.parent
DATA = V3_DIR / "data" / "metrics_data"

qblist = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ecclist = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]

# ---- Fig 2: sigma_lambda heatmap ----

lambda_stds = np.zeros((len(qblist), len(ecclist)))
for i, qb in enumerate(qblist):
    for j, eb in enumerate(ecclist):
        with open(DATA / f"data_eb_{eb}_qb_{qb}", 'rb') as f:
            d = pickle.load(f)
        lam = d['mdot2'] / d['mdot1']
        lam = lam[250:]
        lambda_stds[i, j] = np.std(lam)

fig, ax = plt.subplots(figsize=(8, 6))
c = ax.imshow(lambda_stds, aspect='auto', origin='lower',
              cmap='viridis',
              extent=[min(ecclist), max(ecclist), 0, max(qblist)])

ecclist_mod = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
qblist_mod = np.array(qblist) - 0.05
ax.set_xticks(np.array(ecclist_mod) + (ecclist_mod[1] - ecclist_mod[0]) / 2)
ax.set_yticks(qblist_mod)
ax.set_xticklabels(ecclist)
ax.set_yticklabels(qblist)

for i in range(len(qblist)):
    for j in range(len(ecclist)):
        v = lambda_stds[i, j]
        ax.text((np.array(ecclist_mod) + (ecclist_mod[1] - ecclist_mod[0]) / 2)[j],
                qblist_mod[i],
                f"{v:.2f}",
                ha="center", va="center",
                color="white" if v < lambda_stds.max()*0.5 else "black",
                fontsize=8)

cbar = plt.colorbar(c, ax=ax)
cbar.set_label(r"$\sigma_{\lambda}$", fontsize=12)
ax.set_xlabel(r"$e_b$", fontsize=12)
ax.set_ylabel(r"$q_b$", fontsize=12)
plt.tight_layout()
fig.savefig(V3_DIR / "lambda_std_colormap.pdf")
plt.close(fig)
print(f"Saved {V3_DIR / 'lambda_std_colormap.pdf'} (viridis colormap, range "
      f"{lambda_stds.min():.3f}-{lambda_stds.max():.3f})")

# ---- Fig 3: <lambda> vs q_b lines, with gray shading for lambda > 1 ----

fig, ax = plt.subplots(figsize=(7, 5))
colors = cm.coolwarm(np.linspace(0, 1, len(ecclist) + 1))

for ebind, eb in enumerate(ecclist):
    lams = []; lams_std = []
    for qb in qblist:
        with open(DATA / f"data_eb_{eb}_qb_{qb}", 'rb') as f:
            d = pickle.load(f)
        lam_full = d['mdot2'] / d['mdot1']
        meds = [np.median(lam_full[250+idx:]) for idx in np.arange(0, 105, 5)]
        lams.append(np.mean(meds))
        lams_std.append(np.std(meds) / len(meds))
    color_idx = ebind + 1 if eb == 0.8 else ebind
    ax.plot(qblist, lams, color=colors[color_idx], marker='*',
            label=rf"$e_b = {eb}$")
    ax.errorbar(qblist, lams, yerr=lams_std, color=colors[color_idx], ls='none')

# Gray-shade preferential-to-secondary region (lambda > 1)
ymin, ymax = ax.get_ylim()
ax.axhspan(1.0, max(ymax, 12), alpha=0.13, color='gray', zorder=-1)
ax.text(0.05, 0.93, 'preferential to secondary',
        transform=ax.transAxes, fontsize=10, color='gray',
        verticalalignment='top')

ax.axhline(1.0, color='gray', ls='-', alpha=0.4, lw=0.8)

# Siwek+23a power law q_b^-0.9 reference
qb_ref = np.linspace(0.1, 1.0, 50)
ax.plot(qb_ref, qb_ref**(-0.9), 'g--', alpha=0.6, label=r'$q_b^{-0.9}$ (S23a)')

ax.set_xlabel(r"$q_b$", fontsize=12)
ax.set_ylabel(r"$\langle \lambda \rangle$", fontsize=12)
ax.set_xlim(0.05, 1.05)
ax.set_ylim(0, max(ymax, 12))
ax.legend(loc='upper right', fontsize=8, framealpha=0.85, ncol=2)
plt.tight_layout()
fig.savefig(V3_DIR / "magda_fig2.pdf")
plt.close(fig)
print(f"Saved {V3_DIR / 'magda_fig2.pdf'} (with gray-shading for lambda > 1)")
