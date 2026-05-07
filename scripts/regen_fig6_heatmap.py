#!/usr/bin/env python3
"""
Standalone regen for Fig 6 (rmin_lambda_peak_ratio._paper_ready.pdf).

Hardcodes the period-ratio matrix read off the existing v3 PDF (the
heatmap data is small, 10x8, so this avoids re-running the full
magda_accretion_geometry_ecc_combined.py pipeline). Identical data
and color scaling as before, only larger fonts on axes / ticks /
cell labels / colorbar.
"""

import numpy as np
import matplotlib.pyplot as plt

ecclist = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
qblist  = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

NaN = np.nan
# Rows: top=q=1.0, bottom=q=0.1 (matches original orientation).
new_map = np.array([
    [NaN, 1.00, NaN, NaN, NaN,  1.00, 1.00, 0.86],  # q=1.0
    [NaN, 1.00, NaN, NaN, NaN,  1.00, 1.00, 1.00],  # q=0.9
    [NaN, 1.00, NaN, NaN, NaN,  1.00, 1.00, 0.97],  # q=0.8
    [NaN, 1.00, NaN, NaN, NaN,  NaN,  1.00, 1.00],  # q=0.7
    [NaN, 1.00, NaN, NaN, 0.93, NaN,  1.00, 1.00],  # q=0.6
    [NaN, 1.00, NaN, NaN, NaN,  NaN,  NaN,  1.00],  # q=0.5
    [NaN, 1.00, NaN, NaN, NaN,  NaN,  NaN,  1.00],  # q=0.4
    [NaN, 0.53, NaN, NaN, NaN,  NaN,  NaN,  1.71],  # q=0.3
    [NaN, 1.00, NaN, NaN, NaN,  NaN,  NaN,  NaN],   # q=0.2
    [NaN, NaN,  NaN, NaN, NaN,  NaN,  NaN,  NaN],   # q=0.1
])

fig, ax = plt.subplots(figsize=(8, 10))
c = ax.imshow(new_map, cmap='magma', vmin=0.3, vmax=3, aspect='auto')

cbar = fig.colorbar(c, ax=ax)
cbar.set_label(r'$\tau_{\lambda} / \tau_{r_{1}}$', fontsize=20)
cbar.ax.tick_params(labelsize=15)

ax.set_ylabel(r'$q_b$', fontsize=22)
ax.set_xlabel(r'$e_b$', fontsize=22)
ax.set_xticks(np.arange(len(ecclist)))
ax.set_xticklabels([f'{e:.1f}' for e in ecclist], fontsize=15)
ax.set_yticks(np.arange(len(qblist)))
ax.set_yticklabels([f'{q:.1f}' for q in np.flip(qblist)], fontsize=15)

for i in range(new_map.shape[0]):
    for j in range(new_map.shape[1]):
        v = new_map[i, j]
        if not np.isnan(v):
            ax.text(j, i, f'{v:.2f}', ha='center', va='center',
                    color='white', fontsize=15)

plt.tight_layout()
fig.savefig('rmin_lambda_peak_ratio._paper_ready.pdf')
print('Wrote rmin_lambda_peak_ratio._paper_ready.pdf')
