#!/usr/bin/env python3
"""
Live (M_1, M_2) integration with the RAW q-dot lookup table.

Compared to run_q_evolution_to_LISA.py, this:

1. Tracks M_1 and M_2 as independent state variables.
2. Always queries the lookup with q_phys = min(M_1, M_2)/max(M_1, M_2) ∈ [0, 1].
3. Routes the "secondary" mass-accretion fraction to whichever of M_1, M_2 is
   currently the less massive. If the masses cross, the routing flips — i.e.,
   the simulation's "labelled secondary" identity is re-assigned to whichever
   BH is currently smaller. This is the live-tracking approach the §4.2
   caveats already mention as the proper structural fix.
4. Uses the RAW table values (no sign flip at q_b=1, no zeroing of small
   negatives).

If the raw value at (q_b=1, e_b=0.2) is +0.674, then in the live tracking the
"current less-massive" BH grows at f_less = (0.674 + 2)/4 = 0.668 of the
total accretion rate. Once it crosses the other BH, the labels flip and the
*new* less-massive BH grows faster. Net effect: q_phys saturates at or near 1
for the cells with positive raw q-dot, and drifts away from 1 for cells with
negative raw q-dot.

Output: q_evolution_live_q0_*.pdf
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

QDOT_RAW = np.load(DATA).copy()  # untouched

ECCLIST = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
QBLIST = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

M_total = 1e7 * msol
R_S = 2 * G * M_total / c**2


def eddington_rate(M):
    eta = 0.1
    return 4 * math.pi * G * M * m_p / (c * eta * sigma_T)


MDOT_EDD = eddington_rate(M_total)
MDOT_B = MDOT_EDD


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


def qdot_lookup_raw(q_phys, e):
    """Look up the raw q-dot value at the grid cell closest to (q_phys, e).

    q_phys is in [0, 1] (it is constructed as min/max). Returns the raw
    Magda q-dot in dimensionless Ṁ_b/M_b units.
    """
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
    return QDOT_RAW[9 - qb_idx[0]][eb_idx[0]]


def evolve_in_a_masses(a, y, mdot_b):
    """RHS for state y = [e, M_1, M_2] with a as the independent variable."""
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

    # GW terms (symmetric in M_1 <-> M_2)
    fe = peters_f_e(e)
    da_gw = -64 * G**3 * M_tot**3 * q_phys * fe / (5 * c**5 * a**3 * (1+q_phys)**2)
    de_gw = -e * 304 * G**3 * M_tot**3 * q_phys * (1 + 121*e**2/304) / (
        15 * c**5 * a**4 * (1-e**2)**(5/2) * (1+q_phys)**2)

    # Gas terms
    da_gas = -a * mdot_b / M_tot
    de_g = edot_gas(e, mdot_b, M_tot)

    # Routing total accretion to M_1, M_2 via the raw lookup at q_phys.
    # The lookup returns q-dot in units of Ṁ_b/M_b.
    # d(M_less/M_more)/dt = q_dot_lookup * Ṁ_b/M_b
    # f_less = Ṁ_less/Ṁ_b satisfies:
    #   f_less = (q_dot_lookup + q_phys(1+q_phys)) / (1+q_phys)^2
    q_dot = qdot_lookup_raw(q_phys, e)
    f_less = (q_dot + q_phys * (1 + q_phys)) / (1 + q_phys)**2
    # Clamp the fraction to [0, 1] just in case numerical edge cases push it
    f_less = max(0.0, min(1.0, f_less))
    Mdot_less = f_less * mdot_b
    Mdot_more = (1 - f_less) * mdot_b

    if sec_is_M2:
        Mdot_1 = Mdot_more
        Mdot_2 = Mdot_less
    else:
        Mdot_1 = Mdot_less
        Mdot_2 = Mdot_more

    da_tot = da_gas + da_gw
    if abs(da_tot) < 1e-100:
        return [0.0, 0.0, 0.0]
    de_tot = de_g + de_gw
    return [de_tot / da_tot, Mdot_1 / da_tot, Mdot_2 / da_tot]


def run_live(e0, q0, mdot_b_factor, a0_factor=1e4):
    mdot_b = mdot_b_factor * MDOT_EDD
    M_1_0 = M_total / (1 + q0)
    M_2_0 = q0 * M_1_0
    a0 = a0_factor * R_S
    a_end = 5 * R_S
    a_eval = np.geomspace(a0, a_end, 500)

    sol = solve_ivp(
        lambda a, y: evolve_in_a_masses(a, y, mdot_b),
        (a0, a_end), [e0, M_1_0, M_2_0], t_eval=a_eval,
        method='LSODA', rtol=1e-6, atol=1e-9)

    a_arr = sol.t
    e_arr = sol.y[0]
    M1_arr = sol.y[1]
    M2_arr = sol.y[2]
    # q reported as M_2/M_1 (can exceed 1)
    q_arr = M2_arr / M1_arr
    q_phys_arr = np.minimum(M1_arr, M2_arr) / np.maximum(M1_arr, M2_arr)

    f_orb = np.sqrt(G * (M1_arr + M2_arr) / a_arr**3) / (2 * math.pi)
    f_gw = 2 * f_orb
    return a_arr, e_arr, q_arr, q_phys_arr, f_gw, M1_arr, M2_arr


def sweep(q0, mdot_factor, label):
    E0_LIST = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
    print(f"\n--- q_0 = {q0}, M-dot_b = {mdot_factor:g} Edd, "
          f"a_0 = 10^4 R_S, RAW lookup, live (M_1, M_2) ---")
    print(f"{'e_0':>5}  {'raw qdot':>13}  {'q_final M2/M1':>15}  "
          f"{'q_phys_final':>13}  {'e_final':>9}")
    cases = []
    for e0 in E0_LIST:
        j = int(np.where(np.isclose(ECCLIST, e0))[0][0])
        raw_at_qb1 = QDOT_RAW[0][j]   # cell at q_b=1, e_b=e0
        a, e, q, qp, f, M1, M2 = run_live(e0, q0, mdot_factor)
        cases.append((e0, a, e, q, qp, f, M1, M2, raw_at_qb1))
        print(f"  {e0:.1f}  {raw_at_qb1:>+13.4f}  {q[-1]:>15.4f}  "
              f"{qp[-1]:>13.4f}  {e[-1]:>9.4f}")
    return cases


def make_plot(cases, q0_label, mdot_label, out_path, ylim_q):
    cmap = plt.cm.viridis
    colors = cmap(np.linspace(0.0, 0.9, len(cases)))
    LISA_LO, LISA_HI = 1e-4, 1e-1

    fig, axes = plt.subplots(3, 1, figsize=(8, 9), sharex=True,
                             gridspec_kw={'hspace': 0.06})

    ax = axes[0]
    for (e0, a, e, q, qp, f, M1, M2, raw), col in zip(cases, colors):
        ax.loglog(f, a/R_S, color=col, lw=1.8,
                  label=rf'$e_0={e0:.1f}$ (raw $\dot q$={raw:+.3f})')
    ax.axvspan(LISA_LO, LISA_HI, alpha=0.15, color='gray',
               label=r'LISA band')
    ax.set_ylabel(r'$a / R_S$', fontsize=12)
    ax.legend(loc='upper right', fontsize=7, framealpha=0.85, ncol=2)
    ax.set_title(rf'Live $(M_1, M_2)$ + RAW lookup: $q_0 = {q0_label}$, '
                 rf'$\dot{{M}}_b = {mdot_label}$, $a_0 = 10^4 R_S$',
                 fontsize=11)

    ax = axes[1]
    for (e0, a, e, q, qp, f, M1, M2, raw), col in zip(cases, colors):
        ax.semilogx(f, e, color=col, lw=1.8)
    ax.axvspan(LISA_LO, LISA_HI, alpha=0.15, color='gray')
    ax.axhline(0.45, color='gray', ls=':', alpha=0.5,
               label=r'gas equil.\ $e=0.45$')
    ax.set_ylabel(r'$e$', fontsize=12)
    ax.set_ylim(-0.02, 0.85)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.85)

    ax = axes[2]
    for (e0, a, e, q, qp, f, M1, M2, raw), col in zip(cases, colors):
        # show q_phys = min/max so reader sees the canonical [0,1] view
        ax.semilogx(f, qp, color=col, lw=1.8)
    ax.axvspan(LISA_LO, LISA_HI, alpha=0.15, color='gray')
    ax.axhline(1.0, color='black', alpha=0.4)
    ax.set_ylabel(r'$q_{\rm phys} = \min(M_1,M_2)/\max(M_1,M_2)$',
                  fontsize=11)
    ax.set_xlabel(r'$f_{\rm GW}$ (Hz)', fontsize=12)
    ax.set_ylim(*ylim_q)

    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close(fig)


# ============================================================
# Run the four cases the user cares about
# ============================================================
if __name__ == '__main__':
    print(f"M_total = {M_total/msol:.0e} M_sun")
    print(f"R_S = {R_S:.3e} cm; M_dot_Edd = {MDOT_EDD:.3e} g/s\n")

    # 1× Eddington, q0=1.0
    cases_q1_1edd = sweep(1.0, 1.0, '1Edd')
    make_plot(cases_q1_1edd, '1.0', r'1\,\dot M_{\rm Edd}',
              V3_DIR / "q_evolution_live_q0_1p0_1Edd.pdf",
              ylim_q=(0.85, 1.05))

    # 100× Eddington, q0=1.0
    cases_q1_100edd = sweep(1.0, 100.0, '100Edd')
    make_plot(cases_q1_100edd, '1.0', r'100\,\dot M_{\rm Edd}',
              V3_DIR / "q_evolution_live_q0_1p0_100Edd.pdf",
              ylim_q=(0.85, 1.05))

    # 1× Eddington, q0=0.6
    cases_q06_1edd = sweep(0.6, 1.0, '1Edd')
    make_plot(cases_q06_1edd, '0.6', r'1\,\dot M_{\rm Edd}',
              V3_DIR / "q_evolution_live_q0_0p6_1Edd.pdf",
              ylim_q=(0.55, 1.05))

    # 100× Eddington, q0=0.6
    cases_q06_100edd = sweep(0.6, 100.0, '100Edd')
    make_plot(cases_q06_100edd, '0.6', r'100\,\dot M_{\rm Edd}',
              V3_DIR / "q_evolution_live_q0_0p6_100Edd.pdf",
              ylim_q=(0.55, 1.05))

    for tag in ['q0_1p0_1Edd', 'q0_1p0_100Edd', 'q0_0p6_1Edd', 'q0_0p6_100Edd']:
        print(f"  Saved: q_evolution_live_{tag}.pdf")
