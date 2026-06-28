#!/usr/bin/env python3 -u
"""
Rigorous audit of the q̇-evolution numerics as currently implemented in
scripts/q_evolution_live_masses.py. NO FIXES applied here — this script
only characterizes the current behavior so we can decide what to change.

Designed to be FAST (a few seconds total) — no full population sweeps.
Each test is isolated and prints progress.

Tests:
  T1. Lookup-policy comparison (no ODE) — current nearest-round vs
      round-down vs bilinear vs cubic spline.
  T2. f_less clamp activation map (no ODE).
  T3. q₀ convergence test — ONE e₀, four q₀ values, one Ṁ_bin, one
      lookup policy. Quick 4-trajectory plot, current production lookup.
  T4. Ṁ_bin convergence — ONE case, three Ṁ_bin values, time-rescale
      check.
  T5. Peters f(e) blowup vs clamp (no ODE).
  T6. Zrake polynomial extrapolation (no ODE).
  T7. ODE tolerance sensitivity — ONE case at three rtol values.

Outputs to v3/numerics_audit/.
"""
import sys
import math
import time
import numpy as np
from pathlib import Path
from scipy.integrate import solve_ivp
from scipy.interpolate import RegularGridInterpolator, CubicSpline
import matplotlib.pyplot as plt

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

G = 6.674e-8
c = 2.998e10
msol = 1.989e33
m_p = 1.6726e-24
sigma_T = 6.6524e-25

V3_DIR = Path(__file__).resolve().parent.parent
OUT = V3_DIR / "numerics_audit"
OUT.mkdir(exist_ok=True)
DATA = V3_DIR / "data" / "qdot_data_magda.npy"

QDOT_RAW = np.load(DATA).copy()
ECCLIST = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
QBLIST = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
QDOT_TABLE = QDOT_RAW[::-1, :]            # row 0 -> q_b=0.1, row 9 -> q_b=1.0

M_total = 1e7 * msol
R_S = 2 * G * M_total / c**2


def eddington_rate(M):
    return 4 * math.pi * G * M * m_p / (c * 0.1 * sigma_T)


MDOT_EDD = eddington_rate(M_total)


def peters_f_e(e):
    return (1 + (73/24)*e**2 + (37/96)*e**4) / (1 - e**2)**(7/2)


ZRAKE_E = np.array([0.000, 0.080, 0.160, 0.375, 0.445, 0.550, 0.630, 0.750, 0.800])
ZRAKE_DEDLOGM = np.array([0.0, 0.0, 4.5, 4.0, 0.0, -3.0, -3.2, -2.7, -2.3])


def edot_gas_over_mdot_M(e):
    result = 0.0
    for j in range(len(ZRAKE_E)):
        prod = 1.0
        for k in range(len(ZRAKE_E)):
            if k != j:
                prod *= (e - ZRAKE_E[k]) / (ZRAKE_E[j] - ZRAKE_E[k])
        result += ZRAKE_DEDLOGM[j] * prod
    return result


# ============================================================
# Lookup policies
# ============================================================

def lookup_nearest_round(q_phys, e):
    q_r = round(q_phys, 1)
    e_r = round(e, 1)
    if q_r >= 1: q_r = 1.0
    if q_r < 0.1: q_r = 0.1
    if e_r > 0.8: e_r = 0.8
    if e_r < 0: e_r = 0.0
    if e_r == 0.7:
        e_r = 0.8 if abs(0.8 - e) < abs(0.6 - e) else 0.6
    qb_idx = np.where(np.isclose(QBLIST, q_r))[0][0]
    eb_idx = np.where(np.isclose(ECCLIST, e_r))[0][0]
    return QDOT_TABLE[qb_idx, eb_idx]


def lookup_round_down(q_phys, e):
    q_phys = min(max(q_phys, 0.1), 1.0)
    e = min(max(e, 0.0), 0.8)
    qb_idx = max(0, np.searchsorted(QBLIST, q_phys, side='right') - 1)
    eb_idx = int(np.argmin(np.abs(ECCLIST - e)))
    return QDOT_TABLE[qb_idx, eb_idx]


_bilin = RegularGridInterpolator(
    (QBLIST, ECCLIST), QDOT_TABLE,
    bounds_error=False, fill_value=None, method='linear'
)


def lookup_bilinear(q_phys, e):
    q_phys = min(max(q_phys, 0.1), 1.0)
    e = min(max(e, 0.0), 0.8)
    return float(_bilin([[q_phys, e]])[0])


_q_splines = [CubicSpline(QBLIST, QDOT_TABLE[:, j], bc_type='natural') for j in range(len(ECCLIST))]


def lookup_spline_q(q_phys, e):
    q_phys = min(max(q_phys, 0.1), 1.0)
    e = min(max(e, 0.0), 0.8)
    eb_idx = int(np.argmin(np.abs(ECCLIST - e)))
    return float(_q_splines[eb_idx](q_phys))


# ============================================================
# T1. Lookup-policy comparison (NO ODE — should be < 1 second)
# ============================================================
t0 = time.time()
print("=" * 70)
print("T1: lookup-policy comparison (no ODE)", flush=True)
print("=" * 70)
fig, axes = plt.subplots(2, 4, figsize=(20, 8), sharex=True, sharey=True)
q_fine = np.linspace(0.1, 1.0, 200)
ecols = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
for ax, ec in zip(axes.flatten(), ecols):
    nearest = np.array([lookup_nearest_round(qq, ec) for qq in q_fine])
    rdn = np.array([lookup_round_down(qq, ec) for qq in q_fine])
    bil = np.array([lookup_bilinear(qq, ec) for qq in q_fine])
    spl = np.array([lookup_spline_q(qq, ec) for qq in q_fine])
    ec_idx = int(np.argmin(np.abs(ECCLIST - ec)))
    ax.plot(q_fine, nearest, 'k-', lw=1.0, alpha=0.4, label='nearest-round (current)')
    ax.plot(q_fine, rdn, 'b-', lw=1.0, alpha=0.6, label='round-down')
    ax.plot(q_fine, bil, 'g-', lw=1.5, label='bilinear')
    ax.plot(q_fine, spl, 'm--', lw=1.2, alpha=0.7, label='cubic spline')
    ax.scatter(QBLIST, QDOT_TABLE[:, ec_idx], color='red', zorder=5, s=30, label='data')
    ax.set_title(rf'$e_b={ec}$', fontsize=11)
    ax.axhline(0, color='gray', lw=0.5)
    ax.grid(True, alpha=0.3)
axes[0, 0].set_ylabel(r'$\dot q\ [\dot M_b / M_b]$', fontsize=12)
axes[1, 0].set_ylabel(r'$\dot q\ [\dot M_b / M_b]$', fontsize=12)
for j in range(4):
    axes[1, j].set_xlabel(r'$q_{\rm phys}$', fontsize=12)
axes[0, 0].legend(loc='upper right', fontsize=8, framealpha=0.9)
fig.suptitle('T1: lookup policy comparison at fixed $e_b$', fontsize=13, y=0.99)
plt.tight_layout()
plt.savefig(OUT / "T1_lookup_policies.pdf", bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"  at q_phys = 0.95, four policies give:", flush=True)
for ec in [0.0, 0.1, 0.2, 0.3, 0.4]:
    v = (lookup_nearest_round(0.95, ec), lookup_round_down(0.95, ec),
         lookup_bilinear(0.95, ec), lookup_spline_q(0.95, ec))
    print(f"    e_b={ec}: nearest={v[0]:+.3f}  round-down={v[1]:+.3f}  "
          f"bilinear={v[2]:+.3f}  spline={v[3]:+.3f}", flush=True)
print(f"  T1 took {time.time()-t0:.2f}s", flush=True)

# ============================================================
# T2. f_less clamp activation map
# ============================================================
t0 = time.time()
print("\n" + "=" * 70)
print("T2: f_less = (q̇ + q(1+q))/(1+q)^2 clamp map", flush=True)
print("=" * 70)
f_less_map = np.zeros_like(QDOT_TABLE)
for i, qb in enumerate(QBLIST):
    for j, eb in enumerate(ECCLIST):
        q_dot = QDOT_TABLE[i, j]
        f_less_map[i, j] = (q_dot + qb*(1 + qb)) / (1 + qb)**2

n_clamp = int(np.sum((f_less_map < 0) | (f_less_map > 1)))
print(f"  cells outside [0,1]: {n_clamp} / {f_less_map.size}", flush=True)
print(f"  min(f_less)={f_less_map.min():+.4f}, max(f_less)={f_less_map.max():+.4f}", flush=True)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(f_less_map, origin='lower', aspect='auto',
               extent=[-0.05, 0.85, 0.05, 1.05], cmap='RdBu_r', vmin=0, vmax=1)
plt.colorbar(im, label=r'$f_{\rm less}$ (clamped to [0,1] in prod)')
for i, qb in enumerate(QBLIST):
    for j, eb in enumerate(ECCLIST):
        v = f_less_map[i, j]
        flag = '!' if (v < 0 or v > 1) else ''
        ax.text(eb, qb, f"{v:+.2f}{flag}", ha='center', va='center', fontsize=7,
                color='white' if 0.3 < v < 0.7 else 'black')
ax.set_xlabel(r'$e_b$', fontsize=12)
ax.set_ylabel(r'$q_b$', fontsize=12)
ax.set_title(r'T2: $f_{\rm less}$ map (! = clamp would bite)', fontsize=11)
plt.tight_layout()
plt.savefig(OUT / "T2_fless_clamp_map.pdf", bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"  T2 took {time.time()-t0:.2f}s", flush=True)


# ============================================================
# T5. Peters f(e) clamp (no ODE)
# ============================================================
t0 = time.time()
print("\n" + "=" * 70)
print("T5: Peters f(e) blowup vs e=0.79 clamp", flush=True)
print("=" * 70)
print(f"  f(0.79) = {peters_f_e(0.79):.3e}", flush=True)
print(f"  f(0.85) = {peters_f_e(0.85):.3e}", flush=True)
print(f"  f(0.95) = {peters_f_e(0.95):.3e}", flush=True)
e_fine = np.linspace(0, 0.95, 300)
fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(e_fine, peters_f_e(e_fine), 'b-')
ax.axvline(0.79, color='red', ls='--', alpha=0.7, label='production clamp')
ax.axvline(0.8, color='gray', ls=':', alpha=0.5, label='max e in Magda table')
ax.set_xlabel(r'$e$')
ax.set_ylabel(r'$f(e)$')
ax.set_title('T5: Peters f(e)')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "T5_peters_clamp.pdf", bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"  T5 took {time.time()-t0:.2f}s", flush=True)


# ============================================================
# T6. Zrake polynomial extrapolation (no ODE)
# ============================================================
t0 = time.time()
print("\n" + "=" * 70)
print("T6: Zrake polynomial — extrapolation past data range?", flush=True)
print("=" * 70)
for et in [0.05, 0.45, 0.79, 0.85, 0.90, 0.95]:
    note = " (EXTRAP)" if et > 0.8 else ""
    print(f"  de/dlnM(e={et:.2f}) = {edot_gas_over_mdot_M(et):+.2f}{note}", flush=True)
e_test = np.linspace(0, 0.95, 300)
edot_vals = np.array([edot_gas_over_mdot_M(ee) for ee in e_test])
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(e_test, edot_vals, 'b-', label='Lagrange polynomial')
ax.scatter(ZRAKE_E, ZRAKE_DEDLOGM, color='red', zorder=5, s=50, label='Zrake data')
ax.axvline(0.8, color='gray', ls=':', alpha=0.5, label='max data e')
ax.axhline(0, color='gray', lw=0.4)
ax.set_xlabel('e'); ax.set_ylabel(r'$de/d\ln M$')
ax.set_title('T6: Zrake gas-driven eccentricity rate')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / "T6_zrake_extrap.pdf", bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"  T6 took {time.time()-t0:.2f}s", flush=True)


# ============================================================
# ODE integration (used in T3, T4, T7)
# Limited step count + timeout to prevent runaway.
# ============================================================
def evolve(a, y, mdot_b, lookup_fn):
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
    e_c = max(0.0, min(0.79, e))

    fe = peters_f_e(e_c)
    da_gw = -64 * G**3 * M_tot**3 * q_phys * fe / (5 * c**5 * a**3 * (1+q_phys)**2)
    de_gw = -e_c * 304 * G**3 * M_tot**3 * q_phys * (1 + 121*e_c**2/304) / (
        15 * c**5 * a**4 * (1-e_c**2)**(5/2) * (1+q_phys)**2)
    da_gas = -a * mdot_b / M_tot
    de_g = edot_gas_over_mdot_M(e_c) * mdot_b / M_tot

    q_dot = lookup_fn(q_phys, e_c)
    f_less = (q_dot + q_phys*(1+q_phys)) / (1+q_phys)**2
    f_less_clamped = max(0.0, min(1.0, f_less))
    Mdot_less = f_less_clamped * mdot_b
    Mdot_more = (1 - f_less_clamped) * mdot_b
    if sec_is_M2:
        Mdot_1, Mdot_2 = Mdot_more, Mdot_less
    else:
        Mdot_1, Mdot_2 = Mdot_less, Mdot_more

    da_tot = da_gas + da_gw
    if abs(da_tot) < 1e-100:
        return [0.0, 0.0, 0.0]
    de_tot = de_g + de_gw
    return [de_tot / da_tot, Mdot_1 / da_tot, Mdot_2 / da_tot]


def run(e0, q0, mdot_factor, lookup_fn, a0_factor=1e4, rtol=1e-5, atol=1e-8, max_step=None, label=''):
    mdot_b = mdot_factor * MDOT_EDD
    M_1_0 = M_total / (1 + q0)
    M_2_0 = q0 * M_1_0
    a0 = a0_factor * R_S
    a_end = 5 * R_S
    a_eval = np.geomspace(a0, a_end, 300)
    t_start = time.time()
    sol = solve_ivp(lambda a, y: evolve(a, y, mdot_b, lookup_fn),
                    (a0, a_end), [e0, M_1_0, M_2_0], t_eval=a_eval,
                    method='LSODA', rtol=rtol, atol=atol,
                    max_step=max_step if max_step else np.inf)
    elapsed = time.time() - t_start
    a_arr = sol.t
    e_arr = sol.y[0]
    M1, M2 = sol.y[1], sol.y[2]
    qp = np.minimum(M1, M2) / np.maximum(M1, M2)
    print(f"    {label}: done in {elapsed:.1f}s, success={sol.success}, "
          f"q_final={qp[-1]:.4f}, e_final={e_arr[-1]:.4f}, n_eval={sol.t.size}",
          flush=True)
    return a_arr, e_arr, qp


# ============================================================
# T3. q₀ convergence (FAST — 4 trajectories at one e₀)
# ============================================================
t0 = time.time()
print("\n" + "=" * 70)
print("T3: q₀ convergence at e₀=0.2 (4 trajectories, current production lookup)", flush=True)
print("=" * 70)
fig, ax = plt.subplots(figsize=(9, 5))
Q0_LIST = [0.3, 0.6, 0.9, 1.0]
for q0 in Q0_LIST:
    a, e, qp = run(0.2, q0, 100.0, lookup_nearest_round, label=f'q0={q0}')
    ax.semilogx(a/R_S, qp, lw=1.8, label=rf'$q_0={q0}$')
ax.invert_xaxis()
ax.axhline(1.0, color='gray', lw=0.5)
ax.axhline(0.95, color='red', ls=':', lw=0.7, alpha=0.6, label='q=0.95 grid line')
ax.set_xlabel(r'$a/R_S$ (decreasing)')
ax.set_ylabel(r'$q_{\rm phys}$')
ax.set_xlim(1e4, 5)
ax.legend(loc='lower left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_title(r'T3: q-evolution from different $q_0$, $e_0=0.2$, $\dot M_b=100$ Edd, current lookup')
plt.tight_layout()
plt.savefig(OUT / "T3_q0_convergence.pdf", bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"  T3 took {time.time()-t0:.2f}s", flush=True)


# ============================================================
# T4. Ṁ_bin convergence (one case, 3 Ṁ_bin)
# ============================================================
t0 = time.time()
print("\n" + "=" * 70)
print("T4: Ṁ_bin convergence — same case at three Ṁ_bin", flush=True)
print("=" * 70)
fig, ax = plt.subplots(figsize=(9, 5))
for mdot in [1.0, 10.0, 100.0]:
    a, e, qp = run(0.2, 0.6, mdot, lookup_nearest_round, label=f'mdot={mdot} Edd')
    ax.semilogx(a/R_S, qp, lw=1.6, label=rf'$\dot M_b={mdot:g}$ Edd')
ax.invert_xaxis()
ax.set_xlabel(r'$a/R_S$ (decreasing)')
ax.set_ylabel(r'$q_{\rm phys}$')
ax.set_xlim(1e4, 5)
ax.legend(); ax.grid(True, alpha=0.3)
ax.set_title(r'T4: $\dot M_b$ invariance check — $e_0=0.2, q_0=0.6$, current lookup')
plt.tight_layout()
plt.savefig(OUT / "T4_mdot_convergence.pdf", bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"  T4 took {time.time()-t0:.2f}s", flush=True)


# ============================================================
# T7. Integrator tolerance sensitivity
# ============================================================
t0 = time.time()
print("\n" + "=" * 70)
print("T7: integrator rtol sensitivity (same case at 3 tolerances)", flush=True)
print("=" * 70)
fig, ax = plt.subplots(figsize=(9, 5))
RTOLS = [1e-4, 1e-6, 1e-9]
for rt in RTOLS:
    a, e, qp = run(0.2, 0.6, 100.0, lookup_nearest_round,
                   rtol=rt, atol=rt*1e-3, label=f'rtol={rt:.0e}')
    ax.semilogx(a/R_S, qp, lw=1.5, label=f'rtol={rt:.0e}, q_f={qp[-1]:.5f}')
ax.invert_xaxis()
ax.set_xlabel(r'$a/R_S$ (decreasing)')
ax.set_ylabel(r'$q_{\rm phys}$')
ax.set_xlim(1e4, 5)
ax.legend(); ax.grid(True, alpha=0.3)
ax.set_title(r'T7: rtol sensitivity — $e_0=0.2, q_0=0.6, \dot M_b=100$ Edd')
plt.tight_layout()
plt.savefig(OUT / "T7_tolerance.pdf", bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"  T7 took {time.time()-t0:.2f}s", flush=True)


print("\n" + "=" * 70)
print(f"DONE. Outputs in {OUT}", flush=True)
print("=" * 70)
