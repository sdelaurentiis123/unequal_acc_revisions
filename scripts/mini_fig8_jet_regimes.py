#!/usr/bin/env python3
"""
Mini Fig 8 panels per Zoltan #6: jet-regime classification heatmap at multiple
Mdot_b values, showing how the regime boundaries shift.

For each (q_b, e_b) cell, classify into one of:
  - none (neither BH crosses 1.1 Mdot_Edd sustained)
  - single-jet (one BH sustainedly above 1.1 Mdot_Edd, other not)
  - dual-jet (both BHs simultaneously above 1.1 Mdot_Edd for >50 tau)
  - flickering-jet (both BHs cross threshold but in alternating fashion)

Sweep Mdot_b in {0.01, 0.1, 1, 10} Mdot_Edd. Output: 4-panel heatmap, NOT
time-series (per Zoltan: 'without all the curves and labels').

Accretion file format (from magda_accretion_files/accretion_eb_X_qb_Y.txt,
columns per magda_accretion_actual_fixed.py):
  time  sinkid0  sinkid1  mass0  mass1  mass_in0  mass_in1  ...
  [time = simulation time, /2pi -> orbits]
  [mass_in0, mass_in1 = mass accreted at this step by each BH]
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from pathlib import Path

V3_DIR = Path(__file__).resolve().parent.parent
ACC_DIR = V3_DIR / "data" / "magda_accretion_files"

qblist = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ecclist = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]

THRESHOLD = 1.1  # in M-dot_Edd (per BH)
DURATION_TAU = 50

def edd_per_M(M):
    """Eddington rate / M (per unit mass)."""
    G = 6.67430e-8; c = 3.0e10; sigma_T = 6.6524e-25; m_p = 1.6726e-24
    return (4 * math.pi * G * m_p) / (0.1 * sigma_T * c)  # M-independent rate per unit mass

def classify(qb, eb, mdot_factor):
    """Classify the (q_b, e_b) sim under the assumption Mdot_b = mdot_factor * Mdot_Edd_total.

    The accretion file gives mass_in per timestep in simulation units (M_bin)
    over time in units (2pi tau). Convert to M-dot in M_bin/tau, then rescale
    so that <M-dot_b> = mdot_factor * Mdot_Edd_total (relative to binary M).
    Then check threshold 1.1 * Mdot_Edd_per_BH for each BH.
    """
    fname = ACC_DIR / f"accretion_eb_{eb}_qb_{qb}.txt"
    if not fname.exists():
        return -1
    try:
        d = np.loadtxt(fname, usecols=(0, 5, 6))
    except Exception as ex:
        print(f"  load failed for ({qb}, {eb}): {ex}")
        return -1

    t_raw = d[:, 0]
    mi0 = d[:, 1]
    mi1 = d[:, 2]
    if len(t_raw) < 50:
        return -1

    # time -> tau_b (orbital units)
    t = t_raw / (2 * math.pi)

    # mdot per BH in sim units (M_bin / tau)
    dt = np.diff(t)
    mdot0 = mi0[1:] / dt
    mdot1 = mi1[1:] / dt
    t_mid = t[1:]

    # Cut early instability (first 3000 tau)
    cut = t_mid > 3000
    if cut.sum() < 50:
        return -1
    t_mid = t_mid[cut]; mdot0 = mdot0[cut]; mdot1 = mdot1[cut]

    # Sim-units total mean
    sim_mean_mb = (mdot0 + mdot1).mean()
    if sim_mean_mb <= 0:
        return -1

    # In sim units, M_bin = 1, so mdot in units of M_bin/tau.
    # Rescale: total Mdot_b in physical units = mdot_factor * Mdot_Edd(M_bin).
    # Mdot_Edd(M_bin) per unit binary mass = edd_per_M (constant)
    # We classify each BH against 1.1 Mdot_Edd of THAT BH.
    # Mdot_Edd(BH) = (M_BH/M_bin) * Mdot_Edd(M_bin) = (m_frac) * edd_per_M * M_bin
    # In sim units (M_bin=1): Mdot_Edd_per_BH(sim) = m_frac * mdot_factor / sim_mean_mb (after rescale)
    # Actually simpler: scale mdot to "Eddington-of-each-BH" ratio.
    # mdot0 / Mdot_Edd_BH0 = mdot0 / (m0_frac * Mdot_Edd_total)
    # In sim units, Mdot_Edd_total scales such that mean(mdot0+mdot1) -> mdot_factor * Mdot_Edd_total
    # i.e. mean(mdot0+mdot1)_sim corresponds to mdot_factor * Mdot_Edd_total in physical units
    # So Mdot_Edd_total (sim) = mean(mdot0+mdot1)_sim / mdot_factor
    # Mdot_Edd_per_BH_i (sim) = m_i_frac * Mdot_Edd_total (sim)
    # mdot_i / Mdot_Edd_per_BH_i = mdot_i / (m_i_frac * sim_mean_mb / mdot_factor)
    #                            = mdot_factor * mdot_i / (m_i_frac * sim_mean_mb)

    m0_frac = 1.0 / (1 + qb)  # primary mass fraction
    m1_frac = qb / (1 + qb)   # secondary mass fraction

    mdot0_in_edd = mdot_factor * mdot0 / (m0_frac * sim_mean_mb)
    mdot1_in_edd = mdot_factor * mdot1 / (m1_frac * sim_mean_mb)

    above_0 = mdot0_in_edd > THRESHOLD
    above_1 = mdot1_in_edd > THRESHOLD
    above_both = above_0 & above_1

    median_dt = np.median(np.diff(t_mid))
    samples_per_50 = max(1, int(DURATION_TAU / median_dt))

    def has_run(mask, n):
        if not mask.any():
            return False
        cur = 0; max_run = 0
        for v in mask:
            if v: cur += 1
            else:
                max_run = max(max_run, cur); cur = 0
        max_run = max(max_run, cur)
        return max_run >= n

    sus_0 = has_run(above_0, samples_per_50)
    sus_1 = has_run(above_1, samples_per_50)
    sus_both = has_run(above_both, samples_per_50)

    if not sus_0 and not sus_1:
        return 0  # none
    if sus_both:
        return 2  # dual
    if sus_0 and sus_1:
        # Both crossed sustainedly but never simultaneously -> flickering
        return 3
    return 1  # single

# ============================================================
# Run classification grid for each Mdot_b factor
# ============================================================

mdot_factors = [0.01, 0.1, 1.0, 10.0]
results = {}

for mf in mdot_factors:
    grid = np.full((len(qblist), len(ecclist)), -1, dtype=int)
    for i, qb in enumerate(qblist):
        for j, eb in enumerate(ecclist):
            grid[i, j] = classify(qb, eb, mf)
    results[mf] = grid
    counts = {0: (grid==0).sum(), 1: (grid==1).sum(), 2: (grid==2).sum(),
              3: (grid==3).sum(), -1: (grid==-1).sum()}
    print(f"Mdot_b = {mf:6.2f} Mdot_Edd: none={counts[0]:>2} single={counts[1]:>2} "
          f"dual={counts[2]:>2} flickering={counts[3]:>2} missing={counts[-1]:>2}")

# ============================================================
# Plot 4-panel mini-tapestry
# ============================================================

colors = ['lightgray', 'white', 'tab:blue', 'tab:purple', 'tab:green']
cmap = ListedColormap(colors)
bounds = [-1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

fig, axes = plt.subplots(1, 4, figsize=(13, 3.6), sharey=True)
for ax, mf in zip(axes, mdot_factors):
    ax.imshow(results[mf], cmap=cmap, norm=norm, aspect='auto', origin='lower',
              extent=[min(ecclist), max(ecclist), 0, max(qblist)])
    ax.set_title(rf'$\dot{{M}}_b = {mf:g} \, \dot{{M}}_{{\rm Edd}}$', fontsize=11)
    ax.set_xlabel(r'$e_b$', fontsize=11)

axes[0].set_ylabel(r'$q_b$', fontsize=11)

legend_handles = [
    Patch(facecolor='white', edgecolor='black', label='no jet'),
    Patch(facecolor='tab:blue',   label='single'),
    Patch(facecolor='tab:purple', label='dual'),
    Patch(facecolor='tab:green',  label='flickering'),
]
fig.legend(handles=legend_handles, loc='lower center', ncol=4, fontsize=10,
           bbox_to_anchor=(0.5, -0.02))

plt.tight_layout(rect=[0, 0.05, 1, 1])
out = V3_DIR / "mini_fig8_jet_regimes.pdf"
plt.savefig(out, bbox_inches='tight', dpi=150)
print(f"\nSaved {out}")
