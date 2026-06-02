#!/usr/bin/env python3
"""
Sweep of (e, q) integrations starting at q_0 = 1.0 across multiple e_0.

For each e_0 in {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8} run the same coupled
gas + GW integration from a_0 = 10^3 R_S down to ~5 R_S. Plot all
trajectories together. Annotate which cells are "real drift" (raw q-dot
above the §3.2 noise floor) and which are "policy zero" (raw q-dot small
and negative, set to 0 in the lookup-table processing).

Mirrors run_q_evolution_to_LISA.py exactly except for the IC sweep.
"""
import math
import numpy as np
from pathlib import Path
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

G = 6.674e-8
c = 2.998e10
msol = 1.989e33
m_p = 1.6726e-24
sigma_T = 6.6524e-25

V3_DIR = Path(__file__).resolve().parent.parent
DATA = V3_DIR / "data" / "qdot_data_magda.npy"

qdot_data_raw = np.load(DATA).copy()           # untouched, for diagnostic
qdot_data = np.load(DATA).copy()               # with same policy as run_q_evolution_to_LISA
zero_inds = np.where(qdot_data[0] < 0)[0]
qdot_data[0][zero_inds] = 0
flip_inds = np.where(qdot_data[0] > 0)[0]
qdot_data[0][flip_inds] = -qdot_data[0][flip_inds]

ECCLIST = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
QBLIST = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

M_total = 1e7 * msol
R_S = 2 * G * M_total / c**2


def eddington_rate(M):
    eta = 0.1
    return 4 * math.pi * G * M * m_p / (c * eta * sigma_T)


MDOT_EDD = eddington_rate(M_total)
MDOT_B = MDOT_EDD   # default; overwritten in main loop below


def peters_f_e(e):
    return (1 + (73/24)*e**2 + (37/96)*e**4) / (1 - e**2)**(7/2)


def adot_gw(M, q, a, e):
    return -64 * G**3 * M**3 * q * peters_f_e(e) / (5 * c**5 * a**3 * (1+q)**2)


def edot_gw(M, q, a, e):
    return -e * 304 * G**3 * M**3 * q * (1 + 121*e**2/304) / (
        15 * c**5 * a**4 * (1-e**2)**(5/2) * (1+q)**2)


def adot_gas(a):
    return -a * MDOT_B / M_total


ZRAKE_E = np.array([0.000, 0.080, 0.160, 0.375, 0.445, 0.550, 0.630, 0.750, 0.800])
ZRAKE_DEDLOGM = np.array([0.0, 0.0, 4.5, 4.0, 0.0, -3.0, -3.2, -2.7, -2.3])


def edot_gas(e):
    mdot_over_m = MDOT_B / M_total
    result = 0.0
    for j in range(len(ZRAKE_E)):
        prod = 1.0
        for k in range(len(ZRAKE_E)):
            if k != j:
                prod *= (e - ZRAKE_E[k]) / (ZRAKE_E[j] - ZRAKE_E[k])
        result += ZRAKE_DEDLOGM[j] * prod
    return result * mdot_over_m


def qdot_gas(q, e):
    q_r = round(q, 1)
    e_r = round(e, 1)
    if q_r >= 1: q_r = 1.0
    if q_r < 0.1: q_r = 0.1
    if e_r > 0.8: e_r = 0.8
    if e_r < 0:   e_r = 0.0
    if e_r == 0.7:
        e_r = 0.8 if abs(0.8 - e) < abs(0.6 - e) else 0.6
    qb_idx = np.where(np.isclose(QBLIST, q_r))[0]
    eb_idx = np.where(np.isclose(ECCLIST, e_r))[0]
    if len(qb_idx) == 0 or len(eb_idx) == 0:
        return 0.0
    qdot_at_grid = qdot_data[9 - qb_idx[0]][eb_idx[0]]
    return qdot_at_grid * MDOT_B / M_total


def evolve_in_a(a, y):
    e, q = y
    if q > 1.0: q = 1.0
    if q < 0.1: q = 0.1
    if e < 0:   e = 0.0
    if e > 0.79: e = 0.79
    da_total = adot_gas(a) + adot_gw(M_total, q, a, e)
    if abs(da_total) < 1e-100:
        return [0.0, 0.0]
    de_total = edot_gas(e) + edot_gw(M_total, q, a, e)
    dq = qdot_gas(q, e)
    return [de_total / da_total, dq / da_total]


def run_case(e0, q0):
    a0 = 1e3 * R_S
    a_end = 5 * R_S
    a_eval = np.geomspace(a0, a_end, 800)
    sol = solve_ivp(evolve_in_a, (a0, a_end), [e0, q0], t_eval=a_eval,
                    method='LSODA', rtol=1e-9, atol=1e-12)
    a_arr = sol.t
    e_arr = sol.y[0]
    q_arr = sol.y[1]
    f_orb = np.sqrt(G * M_total / a_arr**3) / (2 * math.pi)
    f_gw = 2 * f_orb
    return a_arr, e_arr, q_arr, f_gw


# --- Sweep ---
E0_LIST = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
MDOT_B_VARIANTS = [(1.0, '1Edd'), (100.0, '100Edd')]


def build_plot(cases, mdot_label, out_path):
    LISA_LO, LISA_HI = 1e-4, 1e-1
    cmap = plt.cm.viridis
    colors = cmap(np.linspace(0.0, 0.9, len(E0_LIST)))

    fig, axes = plt.subplots(3, 1, figsize=(8, 9), sharex=True,
                             gridspec_kw={'hspace': 0.06})

    ax = axes[0]
    for (e0, a, e, q, f, raw, used), col in zip(cases, colors):
        real = abs(raw) > 0.05
        style = '-' if real else (0, (4, 2))
        ax.loglog(f, a/R_S, color=col, lw=1.8, ls=style,
                  label=rf'$e_0={e0:.1f}$ (raw $\dot q$={raw:+.3f})')
    ax.axvspan(LISA_LO, LISA_HI, alpha=0.15, color='gray',
               label=r'LISA band')
    ax.axhline(1e3, color='gray', ls=':', alpha=0.5)
    ax.set_ylabel(r'$a / R_S$', fontsize=12)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.85, ncol=2)
    ax.set_title(rf'$(a, e, q)$ evolution from $a_0=10^3 R_S$, $q_0 = 1.0$, '
                 rf'$\dot{{M}}_b = {mdot_label}$, $M=10^7 M_\odot$',
                 fontsize=11)

    ax = axes[1]
    for (e0, a, e, q, f, raw, used), col in zip(cases, colors):
        real = abs(raw) > 0.05
        style = '-' if real else (0, (4, 2))
        ax.semilogx(f, e, color=col, lw=1.8, ls=style)
    ax.axvspan(LISA_LO, LISA_HI, alpha=0.15, color='gray')
    ax.axhline(0.45, color='gray', ls=':', alpha=0.5,
               label=r'gas equil.\ $e=0.45$')
    ax.set_ylabel(r'$e$', fontsize=12)
    ax.set_ylim(-0.02, 0.85)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.85)

    ax = axes[2]
    for (e0, a, e, q, f, raw, used), col in zip(cases, colors):
        real = abs(raw) > 0.05
        style = '-' if real else (0, (4, 2))
        ax.semilogx(f, q, color=col, lw=1.8, ls=style)
    ax.axvspan(LISA_LO, LISA_HI, alpha=0.15, color='gray')
    ax.axhline(1.0, color='black', alpha=0.4)
    ax.set_ylabel(r'$q = M_2/M_1$', fontsize=12)
    ax.set_xlabel(r'$f_{\rm GW}$ (Hz)', fontsize=12)
    ax.set_ylim(0.97, 1.005)

    ax.text(0.02, 0.04,
            'solid: real drift (raw $|\\dot q|>0.05$)\n'
            'dashed: lookup-table value zeroed by policy at $q_b=1$',
            transform=ax.transAxes, fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='gray', alpha=0.85))

    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close(fig)


for factor, tag in MDOT_B_VARIANTS:
    MDOT_B = factor * MDOT_EDD
    cases = []
    print(f"=== M-dot_b = {factor:g} * M-dot_Edd ===")
    print(f"{'e_0':>5}  {'raw qdot[0]':>13}  {'used qdot':>11}  "
          f"{'q_final':>9}  {'e_final':>9}")
    for e0 in E0_LIST:
        j = int(np.where(np.isclose(ECCLIST, e0))[0][0])
        raw = qdot_data_raw[0][j]
        used = qdot_data[0][j]
        a, e, q, f = run_case(e0, 1.0)
        cases.append((e0, a, e, q, f, raw, used))
        print(f"  {e0:.1f}  {raw:>+13.4f}  {used:>+11.4f}  "
              f"{q[-1]:>9.4f}  {e[-1]:>9.4f}")
    out = V3_DIR / f"q_evolution_sweep_q0_1_{tag}.pdf"
    build_plot(cases, tag.replace('Edd', r'\,\dot M_{\rm Edd}'), out)
    print(f"Saved: {out}\n")
