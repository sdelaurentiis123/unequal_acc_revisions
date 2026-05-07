#!/usr/bin/env python3
"""
Mini-Fig 8 (jet-regime time-series at multiple Mdot_b) for Zoltan #6.

Two side-by-side 10x8 time-series grids identical in style to the
existing Fig 8, one at Mdot_b = 0.5 Mdot_Edd and one at Mdot_b = 5 Mdot_Edd.
Each cell:
  - black curve: primary's per-Eddington accretion rate
  - red curve:   secondary's per-Eddington accretion rate
  - dashed gray: 1.0 Mdot_Edd_BH threshold line
  - background colored by jet-regime classifier (no eb_idx hack, no overrides):
      blue   = single
      purple = dual
      green  = flickering
      white  = no jet

Classifier matches existing accretion_eddington.py loose criterion
(line 605-614) MINUS the eb_idx in {4,7} hand-painting:
  single:     n_secondary > 1 at >=1 points in [7500, 9500]
  flickering: n_secondary > 1 at >=2 points AND n_primary > 1.1 at >50 points
  dual:       n_simul > 50 points
"""

import math
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

V3_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path("/Users/stanislavdelaurentiis/roman_work/metrics_data_new")

qblist = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ecclist = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]

MSOL = 2e33
M_BIN = 1e7 * MSOL
TIME_START = 7500
TIME_END = 9500

# Mdot_b values to render (left panel, right panel)
MDOT_FACTORS = [0.5, 5.0]

REGIME_COLORS = {
    'none':       (1.0, 1.0, 1.0, 0.0),       # white (transparent)
    'single':     (0.0, 0.0, 1.0, 0.18),       # blue
    'dual':       (0.5, 0.0, 0.5, 0.22),       # purple
    'flickering': (0.0, 0.7, 0.0, 0.22),       # green
}

def eddington(M, epsilon=0.1):
    G = 6.67430e-8; c = 3.0e10; sigma_T = 6.6524e-25; m_p = 1.6726e-24
    return (4 * math.pi * G * M * m_p) / (epsilon * sigma_T * c)

def load_sim(qb, eb):
    fname = DATA_DIR / f"data_eb_{eb}_qb_{qb}"
    if not fname.exists():
        return None
    with open(fname, 'rb') as f:
        d = pickle.load(f)
    t = np.asarray(d['time_mdot'])
    mp = np.asarray(d['mdot1'])  # primary
    ms = np.asarray(d['mdot2'])  # secondary
    return t, mp, ms

def classify(mdot_p_frac_window, mdot_s_frac_window):
    n_s = int((mdot_s_frac_window > 1).sum())
    n_p = int((mdot_p_frac_window > 1.1).sum())
    n_simul = int(((mdot_s_frac_window > 1) & (mdot_p_frac_window > 1.1)).sum())
    regime = 'none'
    if n_s > 0:
        regime = 'single'
    if n_s > 1 and n_p > 50:
        regime = 'flickering'
    if n_simul > 50:
        regime = 'dual'
    return regime

def compute_panel(qb, eb, mdot_factor):
    """Return (t_window, mp_frac_window, ms_frac_window, regime) or None."""
    sim = load_sim(qb, eb)
    if sim is None:
        return None
    t, mp_full, ms_full = sim
    sim_mean = (mp_full + ms_full).mean()
    if sim_mean <= 0:
        return None
    scale = mdot_factor * 2 * eddington(M_BIN) / sim_mean
    mp_phys = mp_full * scale
    ms_phys = ms_full * scale
    m_p = (1.0 / (1 + qb)) * M_BIN
    m_s = (qb / (1 + qb)) * M_BIN
    mp_frac = mp_phys / eddington(m_p)
    ms_frac = ms_phys / eddington(m_s)
    mask = (t >= TIME_START) & (t <= TIME_END)
    t_w = t[mask]; mp_w = mp_frac[mask]; ms_w = ms_frac[mask]
    regime = classify(mp_w, ms_w)
    return t_w, mp_w, ms_w, regime

# ============================================================
# Render: 1 figure, 2 side-by-side panels each a 10x8 time-series grid
# ============================================================

NROWS = len(qblist)  # 10
NCOLS = len(ecclist) # 8

fig = plt.figure(figsize=(16.5, 10.5))
outer = fig.add_gridspec(1, 2, left=0.06, right=0.99, bottom=0.08, top=0.94, wspace=0.07)

YLIM = (3e-3, 3e2)  # padded so tick labels don't crush at panel boundaries
TIME_LABEL_TICKS = [8000, 9000]

regime_counts = {mf: {'none':0,'single':0,'dual':0,'flickering':0} for mf in MDOT_FACTORS}

for panel_idx, mf in enumerate(MDOT_FACTORS):
    inner = outer[panel_idx].subgridspec(NROWS, NCOLS, hspace=0, wspace=0)

    # Top centered title for this panel
    title_ax = fig.add_subplot(outer[panel_idx])
    title_ax.set_title(rf'$\dot{{M}}_b = {mf:g}\,\dot{{M}}_{{\rm Edd}}$',
                       fontsize=15, pad=14)
    title_ax.set_axis_off()

    for i, qb in enumerate(qblist[::-1]):  # i=0 is qb=1.0 at top
        for j, eb in enumerate(ecclist):
            ax = fig.add_subplot(inner[i, j])
            res = compute_panel(qb, eb, mf)
            if res is None:
                ax.set_facecolor('lightgray')
            else:
                t_w, mp_w, ms_w, regime = res
                regime_counts[mf][regime] += 1
                ax.plot(t_w, mp_w, color='black', lw=0.5, alpha=0.85)
                ax.plot(t_w, ms_w, color='red',   lw=0.5, alpha=0.85)
                ax.axhline(1.0, color='gray', ls='--', lw=0.5, alpha=0.6)
                ax.set_facecolor(REGIME_COLORS[regime])

            ax.set_yscale('log')
            ax.set_ylim(*YLIM)
            ax.set_xlim(TIME_START, TIME_END)

            # Only outer rows/cols get visible ticks/labels
            ax.tick_params(axis='both', which='both',
                           bottom=(i == NROWS - 1), top=False,
                           left=(panel_idx == 0 and j == 0), right=False,
                           labelbottom=(i == NROWS - 1),
                           labelleft=(panel_idx == 0 and j == 0),
                           labelsize=8, length=2)
            if i == NROWS - 1:
                ax.set_xticks(TIME_LABEL_TICKS)
                ax.set_xticklabels([str(v) for v in TIME_LABEL_TICKS])
                ax.set_xlabel(rf'$e_b$={eb:.1f}', fontsize=10, labelpad=3)
            else:
                ax.set_xticks([])
            if panel_idx == 0 and j == 0:
                ax.set_ylabel(rf'$q_b$={qb:.1f}', fontsize=10, labelpad=3)


# Print classifier counts for sanity check
for mf in MDOT_FACTORS:
    c = regime_counts[mf]
    print(f"Mdot_b = {mf:.2f} Mdot_Edd: none={c['none']:>2} single={c['single']:>2} "
          f"dual={c['dual']:>2} flickering={c['flickering']:>2}")

out = V3_DIR / "mini_fig8_jet_regimes.pdf"
plt.savefig(out, bbox_inches='tight', dpi=140)
print(f"\nSaved {out}")
