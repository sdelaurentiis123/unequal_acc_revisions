#!/usr/bin/env python3
"""
qdot(t) panel grid for the full simulation suite.

For each (e_b, q_b) sim, compute the instantaneous q-dot time series

    qdot(t) = (M_2(t)/M_1(t)) * (Mdot_2(t)/M_2(t) - Mdot_1(t)/M_1(t))

(matching scripts/magda_accretion_actual_fixed.py:323 — this is d/dt of
q = M_2/M_1 including the cumulative mass change in the denominator).

Cumulative masses are constructed from the input accretion-rate time series
starting from m_1(0) = 1/(1+q_b), m_2(0) = q_b/(1+q_b).

Output: qdot_full_panels.pdf  (10 rows of q_b, 8 cols of e_b)
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

V3_DIR = Path(__file__).resolve().parent.parent
DATA = '/Users/stanislavdelaurentiis/roman_work/metrics_data'

ECCLIST = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
QBLIST = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
T_START = 0
T_END = 10000

fig, ax = plt.subplots(10, 8, sharex=True, sharey=True,
                       figsize=(20, 22),
                       gridspec_kw={'hspace': 0.0, 'wspace': 0.0})

for qbind, qb in enumerate(QBLIST):
    for ebind, eb in enumerate(ECCLIST):
        try:
            with open(f'{DATA}/data_eb_{eb}_qb_{qb}', 'rb') as f:
                d = pickle.load(f)
        except FileNotFoundError:
            continue

        # arrays may be ragged across keys — clip to common length
        keys = ['time', 'mdot1', 'mdot2']
        n = min(len(d[k]) for k in keys)
        t = np.asarray(d['time'])[:n]
        mdot1 = np.asarray(d['mdot1'])[:n]
        mdot2 = np.asarray(d['mdot2'])[:n]

        # Cumulative masses (in units where M_b(t=0) = 1) — needed for q(t)
        m1_0 = 1.0 / (1.0 + qb)
        m2_0 = qb / (1.0 + qb)
        dt = np.diff(t, prepend=t[0])
        m1_t = m1_0 + np.cumsum(mdot1 * dt)
        m2_t = m2_0 + np.cumsum(mdot2 * dt)
        m1_t = np.where(m1_t > 0, m1_t, m1_0)
        m2_t = np.where(m2_t > 0, m2_t, m2_0)

        # Paper Eq 1: q̇ (in Ṁ_b/M_b units) = (1+q)(λ-q)/(1+λ)
        # — already dimensionless by convention.
        with np.errstate(divide='ignore', invalid='ignore'):
            q_t = m2_t / m1_t
            lam_t = mdot2 / np.where(mdot1 != 0, mdot1, np.nan)
            qdot_norm = (1 + q_t) * (lam_t - q_t) / (1 + lam_t)

        a = ax[9 - qbind][ebind]
        a.plot(t, qdot_norm, color='black', lw=0.6, alpha=0.85)
        a.axhline(0, color='gray', ls='--', lw=0.5, alpha=0.6)

# Symmetric linear y-limits across the grid so signs are readable
for axs in ax.flatten():
    axs.set_ylim(-3, 3)
    axs.set_xlim(T_START, T_END)

LABEL_FS = 16
for i in range(10):
    ax[9 - i][0].set_ylabel(rf'$q_b={QBLIST[i]:.1f}$', fontsize=LABEL_FS)
for j in range(8):
    ax[9][j].set_xlabel(rf'$e_b={ECCLIST[j]:.1f}$', fontsize=LABEL_FS)

fig.suptitle(r'$\dot{q}(t) = (1+q)(\lambda-q)/(1+\lambda)$ in '
             r'$\dot{M}_b/M_b$ units (paper Eq.\ 1), '
             r'linear y-axis $\pm 3$, time in $\tau_b$',
             fontsize=14, y=0.905)

out = V3_DIR / "qdot_full_panels.pdf"
plt.savefig(out, bbox_inches='tight', dpi=120)
print(f"Wrote {out}")
