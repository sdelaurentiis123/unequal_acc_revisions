#!/usr/bin/env python3
"""
Binary search for the minimum a_0 where q deviates significantly from unity
during the (e_0, q_0) = (0.2, 1.0) trajectory.

Same physics setup as run_q_evolution_to_LISA.py: full (a, e, q) integration
with Peters GW + Magda gas lookup. Vary a_0 and report q at LISA-band entry
for each.

Goal: characterize the a_0 dependence smoothly between 100 R_S (where q stays
at 1.0) and 1000 R_S (where q lands at ~0.985).
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

def edd(M):
    return 4 * math.pi * G * M * m_p / (c * 0.1 * sigma_T)

def peters_f(e):
    return (1 + (73/24)*e**2 + (37/96)*e**4) / (1 - e**2)**(7/2)

def adot_gw(M, q, a, e):
    return -64 * G**3 * M**3 * q * peters_f(e) / (5 * c**5 * a**3 * (1+q)**2)

def edot_gw(M, q, a, e):
    return -e * 304 * G**3 * M**3 * q * (1 + 121*e**2/304) / (
        15 * c**5 * a**4 * (1-e**2)**(5/2) * (1+q)**2)

def edot_gas(e, mdot_b, M):
    s = 0.0
    for j in range(len(ZRAKE_E)):
        p = 1.0
        for k in range(len(ZRAKE_E)):
            if k != j:
                p *= (e - ZRAKE_E[k]) / (ZRAKE_E[j] - ZRAKE_E[k])
        s += ZRAKE_DEDLOGM[j] * p
    return s * mdot_b / M

def qdot_gas(q, e, mdot_b, M):
    qr = round(q, 1); er = round(e, 1)
    if qr >= 1: qr = 1.0
    if qr < 0.1: qr = 0.1
    if er > 0.8: er = 0.8
    if er < 0: er = 0.0
    if er == 0.7:
        er = 0.8 if abs(0.8 - e) < abs(0.6 - e) else 0.6
    qbi = np.where(np.isclose(QBLIST, qr))[0]
    ebi = np.where(np.isclose(ECCLIST, er))[0]
    if len(qbi) == 0 or len(ebi) == 0:
        return 0.0
    return qdot_data[9 - qbi[0]][ebi[0]] * mdot_b / M

def integrate_one(M, a0_RS, mdot_factor, e0=0.2, q0=1.0):
    R_S = 2 * G * M / c**2
    a0 = a0_RS * R_S
    mdot_b = mdot_factor * edd(M)

    def rhs(a, y):
        e, q = y
        if q > 1.0: q = 1.0
        if q < 0.1: q = 0.1
        if e < 0:   e = 0.0
        if e > 0.79: e = 0.79
        da = -a * mdot_b / M + adot_gw(M, q, a, e)
        if abs(da) < 1e-100:
            return [0.0, 0.0]
        de = edot_gas(e, mdot_b, M) + edot_gw(M, q, a, e)
        dq = qdot_gas(q, e, mdot_b, M)
        return [de/da, dq/da]

    a_end = max(5 * R_S, 0.001 * a0)
    a_eval = np.geomspace(a0, a_end, 600)
    sol = solve_ivp(rhs, (a0, a_end), [e0, q0], t_eval=a_eval,
                    method='LSODA', rtol=1e-9, atol=1e-12)
    a_arr = sol.t
    q_arr = sol.y[1]
    f_gw = 2 * np.sqrt(G * M / a_arr**3) / (2 * math.pi)

    if f_gw[-1] >= 1e-4:
        idx = np.argmin(np.abs(f_gw - 1e-4))
        q_lisa = q_arr[idx]
    else:
        q_lisa = q_arr[-1]
    return q_lisa, q_arr[-1]

# Scan a_0 finely from 100 R_S to 1500 R_S
M = 1e7 * msol
mdot = 100  # M-dot factor

print("Mass = 10^7 M_sun, Mdot_b = 100 Mdot_Edd, (e_0, q_0) = (0.2, 1.0)")
print()
print(f"{'a_0/R_S':>9}  {'q_LISA':>9}  {'q_endpt':>9}  {'Δq from 1':>12}")
print(f"{'-'*9}  {'-'*9}  {'-'*9}  {'-'*12}")

a0_values = list(range(100, 1001, 50)) + [1100, 1200, 1500, 2000, 5000]
results = []
for a0 in a0_values:
    q_lisa, q_end = integrate_one(M, a0, mdot)
    delta_q = 1.0 - q_lisa
    results.append((a0, q_lisa, q_end, delta_q))
    print(f"{a0:>9}  {q_lisa:>9.5f}  {q_end:>9.5f}  {delta_q:>12.5f}")

# Find threshold: smallest a_0 where Δq > 0.001 (i.e., q drops below 0.999)
print()
print("Threshold analysis:")
for thresh in [0.001, 0.005, 0.01, 0.013]:
    crossings = [a0 for a0, qL, _, dq in results if dq > thresh]
    if crossings:
        a_crit = min(crossings)
        print(f"  smallest a_0 where Δq > {thresh:.4f}: {a_crit} R_S")
    else:
        print(f"  Δq never exceeds {thresh:.4f} in scan")

print()
# Also test sensitivity to (e_0, q_0): does (0.3, 1.0) follow the same pattern?
print("Repeat with (e_0, q_0) = (0.3, 1.0):")
print()
print(f"{'a_0/R_S':>9}  {'q_LISA':>9}  {'q_endpt':>9}  {'Δq from 1':>12}")
print(f"{'-'*9}  {'-'*9}  {'-'*9}  {'-'*12}")
for a0 in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500]:
    q_lisa, q_end = integrate_one(M, a0, mdot, e0=0.3)
    print(f"{a0:>9}  {q_lisa:>9.5f}  {q_end:>9.5f}  {1-q_lisa:>12.5f}")
