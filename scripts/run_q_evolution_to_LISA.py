#!/usr/bin/env python3
"""
Generate q_evolution_to_LISA.pdf for v3 paper DIFF 1.

Integrates (e, q) as functions of `a` (semi-major axis used as the independent
variable to avoid the t -> t_merge singularity in Peters' formulas). Combines
gas-driven and GW-driven contributions:

  de/da = (ė_gas + ė_GW) / (ȧ_gas + ȧ_GW)
  dq/da = q̇_gas / (ȧ_gas + ȧ_GW)

Initial conditions match v2 Fig 11: a_0 = 10^3 R_S, M_total = 10^7 M_sun,
M-dot_b = 100 * M-dot_Edd. Integrates from a_0 down to ~5 R_S (well into the
LISA band).

We DO NOT clamp q or e during integration — the integrator sees the raw RHS
and we observe the trajectory honestly. The qdot lookup table (Magda's grid)
has cell-edge effects since q is rounded to 0.1 increments; we surface these
in the resulting plots rather than smoothing them.

Outputs:
  q_evolution_to_LISA.pdf
  q_evolution_to_LISA_data.npz
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

# ---- Load and sign-correct the qdot lookup table -----
qdot_data = np.load(DATA)
# Match pop_eval2.py / peters_matthews_with_gas_effects.py:
# row 0 in the array == q_b = 1.0 (since data[9-qbind][...] is used)
zero_inds = np.where(qdot_data[0] < 0)[0]
qdot_data[0][zero_inds] = 0
flip_inds = np.where(qdot_data[0] > 0)[0]
qdot_data[0][flip_inds] = -qdot_data[0][flip_inds]
# After this: qdot_data[0] (the q_b=1 row) has sign-flipped negative values
# at (e=0.2) and (e=0.3) so q evolves DOWN from 1.0.

ECCLIST = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
QBLIST = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

# ---- Binary parameters -----
M_total = 1e7 * msol
R_S = 2 * G * M_total / c**2

def eddington_rate(M):
    eta = 0.1
    return 4 * math.pi * G * M * m_p / (c * eta * sigma_T)

MDOT_B = 100 * eddington_rate(M_total)  # 100 * M-dot_Edd

# ---- Peters formulas ----
def peters_f_e(e):
    return (1 + (73/24)*e**2 + (37/96)*e**4) / (1 - e**2)**(7/2)

def adot_gw(M, q, a, e):
    return -64 * G**3 * M**3 * q * peters_f_e(e) / (5 * c**5 * a**3 * (1+q)**2)

def edot_gw(M, q, a, e):
    return -e * 304 * G**3 * M**3 * q * (1 + 121*e**2/304) / (
        15 * c**5 * a**4 * (1-e**2)**(5/2) * (1+q)**2)

# ---- Gas-driven terms ----
def adot_gas(a):
    """ȧ_gas / a = -M-dot_b / M_b. Standard CBD inspiral scaling."""
    return -a * MDOT_B / M_total

ZRAKE_E = np.array([0.000, 0.080, 0.160, 0.375, 0.445, 0.550, 0.630, 0.750, 0.800])
ZRAKE_DEDLOGM = np.array([0.0, 0.0, 4.5, 4.0, 0.0, -3.0, -3.2, -2.7, -2.3])

def edot_gas(e):
    """Lagrange interpolation of Zrake+20 dė/dlogM data, * (M-dot/M)."""
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
    """Bilinear lookup with rounding (matches pop_eval2.py convention)."""
    q_r = round(q, 1); e_r = round(e, 1)
    if q_r >= 1: q_r = 1.0
    if q_r < 0.1: q_r = 0.1
    if e_r > 0.8: e_r = 0.8
    if e_r < 0: e_r = 0.0
    if e_r == 0.7:
        e_r = 0.8 if abs(0.8 - e) < abs(0.6 - e) else 0.6
    qb_idx = np.where(np.isclose(QBLIST, q_r))[0]
    eb_idx = np.where(np.isclose(ECCLIST, e_r))[0]
    if len(qb_idx) == 0 or len(eb_idx) == 0:
        return 0.0
    qdot_at_grid = qdot_data[9 - qb_idx[0]][eb_idx[0]]
    return qdot_at_grid * MDOT_B / M_total

# ---- ODE: integrate (e, q) as functions of `a` ----
# Independent variable: a (decreasing from a_0 to ~5 R_S).
# State: y = [e, q].
# de/da = (ė_gas + ė_GW) / (ȧ_gas + ȧ_GW)
# dq/da = q̇_gas / (ȧ_gas + ȧ_GW)
def evolve_in_a(a, y):
    e, q = y
    if q > 1.0: q = 1.0     # one-sided clamp: q can't exceed 1 by definition
    if q < 0.1: q = 0.1
    if e < 0:   e = 0.0
    if e > 0.79: e = 0.79

    da_total = adot_gas(a) + adot_gw(M_total, q, a, e)
    if abs(da_total) < 1e-100:
        return [0.0, 0.0]
    de_total = edot_gas(e) + edot_gw(M_total, q, a, e)
    dq = qdot_gas(q, e)
    return [de_total / da_total, dq / da_total]

def run_case(e0, q0, label):
    a0 = 1e3 * R_S
    a_end = 5 * R_S
    a_eval = np.geomspace(a0, a_end, 800)

    sol = solve_ivp(evolve_in_a, (a0, a_end), [e0, q0], t_eval=a_eval,
                    method='LSODA', rtol=1e-9, atol=1e-12)

    a_arr = sol.t
    e_arr = sol.y[0]
    q_arr = sol.y[1]

    # f_GW from Kepler's law
    f_orb = np.sqrt(G * M_total / a_arr**3) / (2 * math.pi)
    f_gw = 2 * f_orb

    print(f"  [{label}] a/R_S {a_arr[0]/R_S:.0f} -> {a_arr[-1]/R_S:.1f}; "
          f"e {e_arr[0]:.3f} -> {e_arr[-1]:.4f}; q {q_arr[0]:.4f} -> {q_arr[-1]:.4f}")
    print(f"             f_GW range: {f_gw[-1]:.2e} -> {f_gw[0]:.2e} Hz")
    return a_arr, e_arr, q_arr, f_gw

print(f"M_total = {M_total/msol:.0e} M_sun")
print(f"R_S = {R_S:.3e} cm; a_0 = 10^3 R_S = {1e3*R_S:.3e} cm")
print(f"M-dot_b = 100 * M-dot_Edd = {MDOT_B*3.156e7/msol:.3f} M_sun/yr")
print()

print("Case 1: (e_0, q_0) = (0.2, 1.0)")
a1, e1, q1, f1 = run_case(0.2, 1.0, "(0.2, 1.0)")
print()
print("Case 2: (e_0, q_0) = (0.3, 1.0)")
a2, e2, q2, f2 = run_case(0.3, 1.0, "(0.3, 1.0)")
print()

# Save data for inspection
np.savez(V3_DIR / "q_evolution_to_LISA_data.npz",
         a1=a1, e1=e1, q1=q1, f1=f1,
         a2=a2, e2=e2, q2=q2, f2=f2,
         R_S=R_S, M_total=M_total, MDOT_B=MDOT_B)

# Plot
LISA_LO = 1e-4
LISA_HI = 1e-1

fig, axes = plt.subplots(3, 1, figsize=(7, 8), sharex=True,
                         gridspec_kw={'hspace': 0.05})

ax = axes[0]
ax.loglog(f1, a1/R_S, color='blue', label=r'$(e_0, q_0) = (0.2, 1.0)$', lw=2)
ax.loglog(f2, a2/R_S, color='red', label=r'$(e_0, q_0) = (0.3, 1.0)$', lw=2)
ax.axvspan(LISA_LO, LISA_HI, alpha=0.18, color='gray',
           label='LISA band ($10^{-4}\\!-\\!10^{-1}$ Hz)')
ax.axhline(1e3, color='gray', ls=':', alpha=0.5, label=r'$a_0 = 10^3 R_S$')
ax.set_ylabel(r'$a / R_S$', fontsize=12)
ax.legend(loc='upper right', fontsize=9, framealpha=0.85)
ax.set_title(r'$(a, e, q)$ evolution from $a_0=10^3 R_S$ to $5 R_S$ '
             r'($M=10^7 M_\odot$, $\dot{M}_b = 100 \dot{M}_{\rm Edd}$)',
             fontsize=11)

ax = axes[1]
ax.semilogx(f1, e1, color='blue', lw=2)
ax.semilogx(f2, e2, color='red', lw=2)
ax.axvspan(LISA_LO, LISA_HI, alpha=0.18, color='gray')
ax.axhline(0.45, color='gray', ls=':', alpha=0.5, label=r'gas equil.\ $e=0.45$')
ax.axhline(0, color='gray', ls=(0, (1, 1)), alpha=0.5)
ax.set_ylabel(r'$e$', fontsize=12)
ax.set_ylim(-0.02, 0.55)
ax.legend(loc='upper right', fontsize=9, framealpha=0.85)

ax = axes[2]
ax.semilogx(f1, q1, color='blue', lw=2)
ax.semilogx(f2, q2, color='red', lw=2)
ax.axvspan(LISA_LO, LISA_HI, alpha=0.18, color='gray')
ax.axhline(1.0, color='black', alpha=0.4, label=r'$q=1$')
ax.set_ylabel(r'$q = M_2/M_1$', fontsize=12)
ax.set_xlabel(r'$f_{\rm GW}$ (Hz)', fontsize=12)
ax.set_ylim(0.97, 1.005)
ax.legend(loc='upper right', fontsize=9, framealpha=0.85)

plt.tight_layout()
out = V3_DIR / "q_evolution_to_LISA.pdf"
plt.savefig(out, bbox_inches='tight', dpi=150)
print(f"\nSaved: {out}")
print(f"Saved: {V3_DIR}/q_evolution_to_LISA_data.npz")
