#!/usr/bin/env python3
"""
Population q-evolution with a modified q-dot table:

  - q_b = 1 row: q̇ = -|raw|  (every cell now drives q AWAY from 1)
  - q_b < 1 rows: unchanged from raw (q̇ > 0 drives q TOWARD 1)

Integrates a sweep of (q_0, e_0) initial conditions to see where the
binary population converges. Uses live (M_1, M_2) tracking so the
q ≤ 1 convention is respected by construction.

Output:
  q_evolution_population_modified_table.npz
  q_evolution_population_modified.pdf
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

# ---- Modified lookup table ----
# q_b = 1 row: every cell becomes -|raw|.  Negatives stay negative
# (with same magnitude), positives flip sign. No noise-floor zeroing.
qdot_table = np.load(DATA).copy()
qdot_table[0] = -np.abs(qdot_table[0])

ECCLIST = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
QBLIST = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

print("Modified q-dot table (q_b = 1 row only, in Ṁ_b/M_b units):")
for j, e in enumerate(ECCLIST):
    print(f"  e_b={e:.1f}: q̇_mod = {qdot_table[0, j]:+.4f}")
print()

M_total = 1e7 * msol
R_S = 2 * G * M_total / c**2


def eddington_rate(M):
    eta = 0.1
    return 4 * math.pi * G * M * m_p / (c * eta * sigma_T)


MDOT_EDD = eddington_rate(M_total)


def peters_f_e(e):
    return (1 + (73/24)*e**2 + (37/96)*e**4) / (1 - e**2)**(7/2)


ZRAKE_E = np.array([0.000, 0.080, 0.160, 0.375, 0.445, 0.550, 0.630, 0.750, 0.800])
ZRAKE_DEDLOGM = np.array([0.0, 0.0, 4.5, 4.0, 0.0, -3.0, -3.2, -2.7, -2.3])


def edot_gas(e, mdot_b, M):
    mdot_over_m = mdot_b / M
    result = 0.0
    for j in range(len(ZRAKE_E)):
        prod = 1.0
        for k in range(len(ZRAKE_E)):
            if k != j:
                prod *= (e - ZRAKE_E[k]) / (ZRAKE_E[j] - ZRAKE_E[k])
        result += ZRAKE_DEDLOGM[j] * prod
    return result * mdot_over_m


def qdot_lookup(q_phys, e):
    """Returns the modified-table q̇ in Ṁ_b/M_b units at the nearest grid cell."""
    q_r = round(q_phys, 1)
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
    return qdot_table[9 - qb_idx[0]][eb_idx[0]]


def rhs(a, y, mdot_b):
    """RHS for state y = [e, M_1, M_2]. Independent variable: a."""
    e, M_1, M_2 = y
    if M_1 <= 0 or M_2 <= 0:
        return [0.0, 0.0, 0.0]

    M_tot = M_1 + M_2
    if M_2 <= M_1:
        M_less, M_more = M_2, M_1
        sec_is_M2 = True
    else:
        M_less, M_more = M_1, M_2
        sec_is_M2 = False
    q_phys = M_less / M_more

    if e < 0:   e = 0.0
    if e > 0.79: e = 0.79

    fe = peters_f_e(e)
    da_gw = -64 * G**3 * M_tot**3 * q_phys * fe / (5 * c**5 * a**3 * (1+q_phys)**2)
    de_gw = -e * 304 * G**3 * M_tot**3 * q_phys * (1 + 121*e**2/304) / (
        15 * c**5 * a**4 * (1-e**2)**(5/2) * (1+q_phys)**2)
    da_gas = -a * mdot_b / M_tot
    de_g = edot_gas(e, mdot_b, M_tot)

    q_dot = qdot_lookup(q_phys, e)
    f_less = (q_dot + q_phys * (1 + q_phys)) / (1 + q_phys)**2
    f_less = max(0.0, min(1.0, f_less))
    Mdot_less = f_less * mdot_b
    Mdot_more = (1 - f_less) * mdot_b
    if sec_is_M2:
        Mdot_1, Mdot_2 = Mdot_more, Mdot_less
    else:
        Mdot_1, Mdot_2 = Mdot_less, Mdot_more

    da_tot = da_gas + da_gw
    if abs(da_tot) < 1e-100:
        return [0.0, 0.0, 0.0]
    de_tot = de_g + de_gw
    return [de_tot / da_tot, Mdot_1 / da_tot, Mdot_2 / da_tot]


def run_case(e0, q0, mdot_factor=100.0, a0_factor=1e4):
    mdot_b = mdot_factor * MDOT_EDD
    M_1_0 = M_total / (1 + q0)
    M_2_0 = q0 * M_1_0
    a0 = a0_factor * R_S
    a_end = 5 * R_S
    a_eval = np.geomspace(a0, a_end, 500)
    sol = solve_ivp(
        lambda a, y: rhs(a, y, mdot_b),
        (a0, a_end), [e0, M_1_0, M_2_0], t_eval=a_eval,
        method='LSODA', rtol=1e-6, atol=1e-9)
    a_arr = sol.t
    e_arr = sol.y[0]
    M1_arr = sol.y[1]; M2_arr = sol.y[2]
    q_phys = np.minimum(M1_arr, M2_arr) / np.maximum(M1_arr, M2_arr)
    f_orb = np.sqrt(G * (M1_arr + M2_arr) / a_arr**3) / (2 * math.pi)
    f_gw = 2 * f_orb
    return a_arr, e_arr, q_phys, f_gw


def sweep(q0, mdot_factor):
    cases = []
    for e0 in ECCLIST:
        a, e, q, f = run_case(e0, q0, mdot_factor=mdot_factor)
        cases.append((e0, a, e, q, f))
    return cases


print("Running population sweep at M_dot_b = 100 M_dot_Edd, a_0 = 10^4 R_S")
print()
Q0_LIST = [0.3, 0.6, 0.9, 1.0]

results = {}
for q0 in Q0_LIST:
    print(f"--- q_0 = {q0} ---")
    print(f"{'e_0':>5}  {'q_phys_final':>13}  {'e_final':>9}")
    cases = sweep(q0, mdot_factor=100.0)
    results[q0] = cases
    for (e0, a, e, q, f) in cases:
        print(f"  {e0:.1f}  {q[-1]:>13.4f}  {e[-1]:>9.4f}")
    print()


# Plot all initial conditions in one figure
fig, axes = plt.subplots(len(Q0_LIST), 1, figsize=(9, 11), sharex=True,
                         gridspec_kw={'hspace': 0.06})
LISA_LO, LISA_HI = 1e-4, 1e-1
cmap = plt.cm.viridis
colors = cmap(np.linspace(0.0, 0.9, len(ECCLIST)))

for ax, q0 in zip(axes, Q0_LIST):
    for (e0, a, e, q, f), col in zip(results[q0], colors):
        ax.semilogx(f, q, color=col, lw=1.8,
                    label=rf'$e_0={e0:.1f}$' if q0 == Q0_LIST[0] else None)
    ax.axvspan(LISA_LO, LISA_HI, alpha=0.15, color='gray',
               label='LISA band' if q0 == Q0_LIST[0] else None)
    ax.axhline(1.0, color='black', alpha=0.4, lw=0.8)
    ax.axhline(0.95, color='red', ls=':', alpha=0.6, lw=1.0,
               label=r'$q = 0.95$ grid boundary' if q0 == Q0_LIST[0] else None)
    ax.set_ylabel(rf'$q_{{\rm phys}}$ ($q_0={q0:.1f}$)', fontsize=11)
    ax.set_ylim(0.25, 1.05)
    ax.grid(True, alpha=0.2)

axes[0].legend(loc='lower right', fontsize=8, framealpha=0.9, ncol=3)
axes[0].set_title(r'Modified lookup ($q_b = 1$ row $\to -|\dot q_{\rm raw}|$): '
                  r'population $q$-evolution across $(e_0, q_0)$',
                  fontsize=11)
axes[-1].set_xlabel(r'$f_{\rm GW}$ (Hz)', fontsize=12)

plt.tight_layout()
out = V3_DIR / "q_evolution_population_modified.pdf"
plt.savefig(out, bbox_inches='tight', dpi=150)
print(f"Saved: {out}")
