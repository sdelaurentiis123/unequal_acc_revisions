#!/usr/bin/env python3
"""
Two diagnostic integrations:

(A) Raw integration: q_0 = 1.0, varying e_0, using the qdot lookup table
    AS-IS (no sign flip, no clamping of negatives to zero). Demonstrates
    why the §4.2 policy is needed: with raw signs, qdot at (q_b=1, e_b=0.2)
    is positive, which would push q upward past 1 (impossible by the
    M_2/M_1 <= 1 convention).

(B) Sub-1 integration: q_0 = 0.6, varying e_0. Does the binary reach
    q = 1? Probes the "preferential accretion drives toward equal mass"
    picture across the full (e_b, q_b) lookup.

Also reports the gas-GW crossover semi-major axis at each Ṁ_b.
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

qdot_raw = np.load(DATA).copy()   # NO policy applied — used in (A)
qdot_policy = np.load(DATA).copy()
zero_inds = np.where(qdot_policy[0] < 0)[0]
qdot_policy[0][zero_inds] = 0
flip_inds = np.where(qdot_policy[0] > 0)[0]
qdot_policy[0][flip_inds] = -qdot_policy[0][flip_inds]

ECCLIST = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
QBLIST = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

M_total = 1e7 * msol
R_S = 2 * G * M_total / c**2


def eddington_rate(M):
    eta = 0.1
    return 4 * math.pi * G * M * m_p / (c * eta * sigma_T)


MDOT_EDD = eddington_rate(M_total)
MDOT_B = MDOT_EDD       # overwritten per case
QDOT_TABLE = qdot_policy  # overwritten per case ('raw' or 'policy')


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
    if q_r > 1: q_r = 1.0
    if q_r < 0.1: q_r = 0.1
    if e_r > 0.8: e_r = 0.8
    if e_r < 0:   e_r = 0.0
    if e_r == 0.7:
        e_r = 0.8 if abs(0.8 - e) < abs(0.6 - e) else 0.6
    qb_idx = np.where(np.isclose(QBLIST, q_r))[0]
    eb_idx = np.where(np.isclose(ECCLIST, e_r))[0]
    if len(qb_idx) == 0 or len(eb_idx) == 0:
        return 0.0
    qdot_at_grid = QDOT_TABLE[9 - qb_idx[0]][eb_idx[0]]
    return qdot_at_grid * MDOT_B / M_total


def evolve_in_a(a, y):
    e, q = y
    if q > 1.0: q = 1.0
    if q < 0.05: q = 0.05
    if e < 0:   e = 0.0
    if e > 0.79: e = 0.79
    da_total = adot_gas(a) + adot_gw(M_total, q, a, e)
    if abs(da_total) < 1e-100:
        return [0.0, 0.0]
    de_total = edot_gas(e) + edot_gw(M_total, q, a, e)
    dq = qdot_gas(q, e)
    return [de_total / da_total, dq / da_total]


def run_case(e0, q0, a0_factor=1e3):
    a0 = a0_factor * R_S
    a_end = 5 * R_S
    a_eval = np.geomspace(a0, a_end, 500)
    sol = solve_ivp(evolve_in_a, (a0, a_end), [e0, q0], t_eval=a_eval,
                    method='LSODA', rtol=1e-6, atol=1e-9)
    a_arr = sol.t
    e_arr = sol.y[0]
    q_arr = sol.y[1]
    f_orb = np.sqrt(G * M_total / a_arr**3) / (2 * math.pi)
    f_gw = 2 * f_orb
    return a_arr, e_arr, q_arr, f_gw


def crossover_a(M, q, e, mdot_b):
    """Solve |a_dot_gas| = |a_dot_GW| analytically for a."""
    fe = peters_f_e(e)
    # a * mdot_b/M = 64 G^3 M^3 q f(e) / (5 c^5 a^3 (1+q)^2)
    rhs = 64 * G**3 * M**3 * q * fe / (5 * c**5 * (1 + q)**2 * mdot_b / M)
    a4 = rhs
    return a4**0.25


# ============================================================
# (A) Raw integration: q_0 = 1.0
# ============================================================
LISA_LO, LISA_HI = 1e-4, 1e-1
E0_LIST = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]

print(f"M_total = {M_total/msol:.0e} M_sun;  M_dot_Edd = {MDOT_EDD:.3e} g/s")
print()
print("======= (A) RAW q-dot table, q_0 = 1.0, M-dot_b = 1 Edd =======")
print("Using the lookup table values directly with NO sign flip, NO clamping.")
print()
MDOT_B = MDOT_EDD
QDOT_TABLE = qdot_raw
cases_A = []
print(f"{'e_0':>5}  {'raw qdot':>10}  {'q_final':>9}  {'e_final':>9}")
for e0 in E0_LIST:
    j = int(np.where(np.isclose(ECCLIST, e0))[0][0])
    raw = qdot_raw[0][j]
    a, e, q, f = run_case(e0, 1.0)
    cases_A.append((e0, a, e, q, f, raw))
    print(f"  {e0:.1f}  {raw:>+10.4f}  {q[-1]:>9.4f}  {e[-1]:>9.4f}")
print()

# ============================================================
# (B) Sub-1 integration: q_0 = 0.6, policy table (raw row 0 doesn't
# matter here since q starts away from 1). Now at a_0 = 10^5 R_S so
# we actually start in the gas-dominated regime at 1 M_dot_Edd.
# ============================================================
print("======= (B) q_0 = 0.6, M-dot_b = 1 Edd, a_0 = 10^5 R_S =======")
print()
MDOT_B = MDOT_EDD
QDOT_TABLE = qdot_policy
cases_B = []
print(f"{'e_0':>5}  {'qdot[q_b=0.6, e_b]':>20}  {'q_final':>9}  {'e_final':>9}")
for e0 in E0_LIST:
    qb_row = 9 - int(np.where(np.isclose(QBLIST, 0.6))[0][0])  # row 4
    j = int(np.where(np.isclose(ECCLIST, e0))[0][0])
    qdot_local = qdot_policy[qb_row][j]
    a, e, q, f = run_case(e0, 0.6, a0_factor=1e4)
    cases_B.append((e0, a, e, q, f, qdot_local))
    print(f"  {e0:.1f}  {qdot_local:>+20.4f}  {q[-1]:>9.4f}  {e[-1]:>9.4f}")
print()

# ============================================================
# (B_raw) q_0 = 0.6 with RAW table (no policy on q_b=1 row)
# Shows what happens when we let the integrator hit the q_b=1
# boundary without sign-flipping or zeroing.
# ============================================================
print("======= (B_raw) q_0 = 0.6, RAW q-dot table, M-dot_b = 1 Edd, a_0 = 10^4 R_S =======")
print()
MDOT_B = MDOT_EDD
QDOT_TABLE = qdot_raw
cases_Braw = []
print(f"{'e_0':>5}  {'raw row0 q-dot':>15}  "
      f"{'q_b=0.6 row q-dot':>18}  {'q_final':>9}  {'e_final':>9}")
for e0 in E0_LIST:
    j = int(np.where(np.isclose(ECCLIST, e0))[0][0])
    qd_top = qdot_raw[0][j]
    qd_06 = qdot_raw[9 - int(np.where(np.isclose(QBLIST, 0.6))[0][0])][j]
    a, e, q, f = run_case(e0, 0.6, a0_factor=1e4)
    cases_Braw.append((e0, a, e, q, f, qd_top))
    print(f"  {e0:.1f}  {qd_top:>+15.4f}  {qd_06:>+18.4f}  "
          f"{q[-1]:>9.4f}  {e[-1]:>9.4f}")
print()

# ============================================================
# (B2) q_0 = 1.0 at a_0 = 10^5 R_S, 1 M-dot_Edd — same a_0 as (B)
# so q_0=1 and q_0=0.6 are directly comparable.
# ============================================================
print("======= (B2) q_0 = 1.0, M-dot_b = 1 Edd, a_0 = 10^5 R_S =======")
print()
MDOT_B = MDOT_EDD
QDOT_TABLE = qdot_policy
cases_B2 = []
print(f"{'e_0':>5}  {'used qdot':>10}  {'q_final':>9}  {'e_final':>9}")
for e0 in E0_LIST:
    j = int(np.where(np.isclose(ECCLIST, e0))[0][0])
    used = qdot_policy[0][j]
    a, e, q, f = run_case(e0, 1.0, a0_factor=1e4)
    cases_B2.append((e0, a, e, q, f, used))
    print(f"  {e0:.1f}  {used:>+10.4f}  {q[-1]:>9.4f}  {e[-1]:>9.4f}")
print()

# ============================================================
# (C) Diagnostic: gas-GW crossover semi-major axis
# ============================================================
print("======= (C) Gas-GW crossover semi-major axis a_x =======")
print("Solving |a_dot_gas| = |a_dot_GW| for a, at q=1, e=0.2.")
print()
for factor in [1.0, 10.0, 100.0]:
    ax = crossover_a(M_total, 1.0, 0.2, factor * MDOT_EDD)
    print(f"  M-dot_b = {factor:>5g} M_dot_Edd:  a_x = {ax/R_S:>8.1f} R_S "
          f"(gas dominates for a > a_x, GW dominates for a < a_x)")
print(f"  Integration window: 5 R_S to 10^3 R_S")
print()


# ============================================================
# Plots
# ============================================================
def make_panel(cases, q0_label, mdot_label, out_path, ylim_q):
    cmap = plt.cm.viridis
    colors = cmap(np.linspace(0.0, 0.9, len(cases)))

    fig, axes = plt.subplots(3, 1, figsize=(8, 9), sharex=True,
                             gridspec_kw={'hspace': 0.06})

    ax = axes[0]
    for (e0, a, e, q, f, qd), col in zip(cases, colors):
        ax.loglog(f, a/R_S, color=col, lw=1.8,
                  label=rf'$e_0={e0:.1f}$ ($\dot q$={qd:+.3f})')
    ax.axvspan(LISA_LO, LISA_HI, alpha=0.15, color='gray',
               label=r'LISA band')
    ax.set_ylabel(r'$a / R_S$', fontsize=12)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.85, ncol=2)
    ax.set_title(rf'$q_0 = {q0_label}$, $\dot{{M}}_b = {mdot_label}$, '
                 rf'$M=10^7 M_\odot$, $a_0=10^3 R_S$', fontsize=11)

    ax = axes[1]
    for (e0, a, e, q, f, qd), col in zip(cases, colors):
        ax.semilogx(f, e, color=col, lw=1.8)
    ax.axvspan(LISA_LO, LISA_HI, alpha=0.15, color='gray')
    ax.axhline(0.45, color='gray', ls=':', alpha=0.5,
               label=r'gas equil.\ $e=0.45$')
    ax.set_ylabel(r'$e$', fontsize=12)
    ax.set_ylim(-0.02, 0.85)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.85)

    ax = axes[2]
    for (e0, a, e, q, f, qd), col in zip(cases, colors):
        ax.semilogx(f, q, color=col, lw=1.8)
    ax.axvspan(LISA_LO, LISA_HI, alpha=0.15, color='gray')
    ax.axhline(1.0, color='black', alpha=0.4)
    ax.set_ylabel(r'$q = M_2/M_1$', fontsize=12)
    ax.set_xlabel(r'$f_{\rm GW}$ (Hz)', fontsize=12)
    ax.set_ylim(*ylim_q)

    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close(fig)


make_panel(cases_A, '1.0', r'1\,\dot M_{\rm Edd}',
           V3_DIR / "q_evolution_raw_q0_1.pdf",
           ylim_q=(0.85, 1.06))
print(f"Saved: {V3_DIR}/q_evolution_raw_q0_1.pdf")

make_panel(cases_B, '0.6', r'1\,\dot M_{\rm Edd}\ (a_0=10^4 R_S)',
           V3_DIR / "q_evolution_q0_0p6_wide.pdf",
           ylim_q=(0.55, 1.06))
print(f"Saved: {V3_DIR}/q_evolution_q0_0p6_wide.pdf")

make_panel(cases_B2, '1.0', r'1\,\dot M_{\rm Edd}\ (a_0=10^4 R_S)',
           V3_DIR / "q_evolution_q0_1p0_wide.pdf",
           ylim_q=(0.85, 1.06))
print(f"Saved: {V3_DIR}/q_evolution_q0_1p0_wide.pdf")

make_panel(cases_Braw, '0.6', r'1\,\dot M_{\rm Edd},\ \mathrm{RAW\ table}',
           V3_DIR / "q_evolution_q0_0p6_raw.pdf",
           ylim_q=(0.55, 1.06))
print(f"Saved: {V3_DIR}/q_evolution_q0_0p6_raw.pdf")
