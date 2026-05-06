#!/usr/bin/env python3
"""
Stress test for q evolution to LISA across binary parameters:
  - M_total: 10^5, 10^6, 10^7 M_sun
  - a_0:     10^2, 10^3, 10^4 R_S
  - Mdot_b:  1, 10, 100 Mdot_Edd

For each (M_total, a_0, Mdot_b), integrate (e, q) from a_0 down to 5 R_S
for the (e_0, q_0) = (0.2, 1.0) case. Report the q value at LISA-band entry
(f_GW = 1e-4 Hz) and at integration endpoint.

Goal: confirm that q-preservation is robust across parameter space, identify
where lookup-grid artifacts matter.
"""

import math
import numpy as np
from pathlib import Path
from scipy.integrate import solve_ivp

G = 6.674e-8
c = 2.998e10
msol = 1.989e33
m_p = 1.6726e-24
sigma_T = 6.6524e-25

V3_DIR = Path(__file__).resolve().parent.parent
DATA = V3_DIR / "data" / "qdot_data_magda.npy"

qdot_data = np.load(DATA)
zero_inds = np.where(qdot_data[0] < 0)[0]
qdot_data[0][zero_inds] = 0
flip_inds = np.where(qdot_data[0] > 0)[0]
qdot_data[0][flip_inds] = -qdot_data[0][flip_inds]

ECCLIST = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
QBLIST = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

ZRAKE_E = np.array([0.000, 0.080, 0.160, 0.375, 0.445, 0.550, 0.630, 0.750, 0.800])
ZRAKE_DEDLOGM = np.array([0.0, 0.0, 4.5, 4.0, 0.0, -3.0, -3.2, -2.7, -2.3])

def eddington_rate(M):
    eta = 0.1
    return 4 * math.pi * G * M * m_p / (c * eta * sigma_T)

def peters_f_e(e):
    return (1 + (73/24)*e**2 + (37/96)*e**4) / (1 - e**2)**(7/2)

def adot_gw(M, q, a, e):
    return -64 * G**3 * M**3 * q * peters_f_e(e) / (5 * c**5 * a**3 * (1+q)**2)

def edot_gw(M, q, a, e):
    return -e * 304 * G**3 * M**3 * q * (1 + 121*e**2/304) / (
        15 * c**5 * a**4 * (1-e**2)**(5/2) * (1+q)**2)

def adot_gas(a, mdot_b, m_total):
    return -a * mdot_b / m_total

def edot_gas(e, mdot_b, m_total):
    mdot_over_m = mdot_b / m_total
    result = 0.0
    for j in range(len(ZRAKE_E)):
        prod = 1.0
        for k in range(len(ZRAKE_E)):
            if k != j:
                prod *= (e - ZRAKE_E[k]) / (ZRAKE_E[j] - ZRAKE_E[k])
        result += ZRAKE_DEDLOGM[j] * prod
    return result * mdot_over_m

def qdot_gas(q, e, mdot_b, m_total):
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
    return qdot_at_grid * mdot_b / m_total

def run(M_total, a0_RS, mdot_factor, e0=0.2, q0=1.0):
    """Integrate one case. Returns (a, e, q, f_gw, q_at_LISA)."""
    R_S = 2 * G * M_total / c**2
    a0 = a0_RS * R_S
    mdot_b = mdot_factor * eddington_rate(M_total)

    def rhs(a, y):
        e, q = y
        if q > 1.0: q = 1.0
        if q < 0.1: q = 0.1
        if e < 0:   e = 0.0
        if e > 0.79: e = 0.79
        da = adot_gas(a, mdot_b, M_total) + adot_gw(M_total, q, a, e)
        if abs(da) < 1e-100:
            return [0.0, 0.0]
        de = edot_gas(e, mdot_b, M_total) + edot_gw(M_total, q, a, e)
        dq = qdot_gas(q, e, mdot_b, M_total)
        return [de/da, dq/da]

    a_end = max(5 * R_S, 0.001 * a0)  # don't go below 5 R_S
    a_eval = np.geomspace(a0, a_end, 600)
    sol = solve_ivp(rhs, (a0, a_end), [e0, q0], t_eval=a_eval,
                    method='LSODA', rtol=1e-9, atol=1e-12)
    a_arr = sol.t
    e_arr = sol.y[0]
    q_arr = sol.y[1]
    f_gw = 2 * np.sqrt(G * M_total / a_arr**3) / (2 * math.pi)

    # q at LISA band entry (f = 1e-4 Hz)
    if f_gw[-1] >= 1e-4:
        idx = np.argmin(np.abs(f_gw - 1e-4))
        q_lisa = q_arr[idx]
        e_lisa = e_arr[idx]
        a_lisa = a_arr[idx] / R_S
    else:
        q_lisa = float('nan'); e_lisa = float('nan'); a_lisa = float('nan')

    return {
        'M_total': M_total, 'a0_RS': a0_RS, 'mdot_factor': mdot_factor,
        'q_end': q_arr[-1], 'e_end': e_arr[-1], 'a_end_RS': a_arr[-1]/R_S,
        'f_end': f_gw[-1],
        'q_lisa': q_lisa, 'e_lisa': e_lisa, 'a_lisa_RS': a_lisa,
        'success': sol.success,
    }

# Run grid
masses_msol = [1e5, 1e6, 1e7]
a0_vals = [100, 1000, 10000]
mdot_factors = [1, 10, 100]

print(f"{'M_tot':>8} {'a_0/R_S':>9} {'Mdot':>5}  | {'q_LISA':>8} {'e_LISA':>8} {'a_LISA':>8}  | {'q_end':>8} {'e_end':>8} {'a_end':>8}  | {'f_end[Hz]':>10}")
print(f"{'-'*8} {'-'*9} {'-'*5}  | {'-'*8} {'-'*8} {'-'*8}  | {'-'*8} {'-'*8} {'-'*8}  | {'-'*10}")
results = []
for M in masses_msol:
    for a0 in a0_vals:
        for mdot in mdot_factors:
            r = run(M*msol, a0, mdot)
            results.append(r)
            qL = f"{r['q_lisa']:.4f}" if not np.isnan(r['q_lisa']) else " --- "
            eL = f"{r['e_lisa']:.4f}" if not np.isnan(r['e_lisa']) else " --- "
            aL = f"{r['a_lisa_RS']:.1f}" if not np.isnan(r['a_lisa_RS']) else " --- "
            print(f"{M:>8.0e} {a0:>9} {mdot:>5}  | {qL:>8} {eL:>8} {aL:>8}  | "
                  f"{r['q_end']:>8.4f} {r['e_end']:>8.4f} {r['a_end_RS']:>8.1f}  | {r['f_end']:>10.2e}")
