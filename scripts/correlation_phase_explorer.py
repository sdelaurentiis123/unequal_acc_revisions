#!/usr/bin/env python3 -u
"""
Toy-model exploration of what NEGATIVE vs POSITIVE cross-correlation
between λ(t) and r_i(t) actually means, and where the sign comes from.

Premise: both λ(t) and r_i(t) are periodic at the cavity-precession
beat period τ_cav. In the simplest model each is sinusoidal in some
phase φ(t), but the phase of λ relative to r_i can be anything — and
which phase you get controls the sign of the cross-correlation.

Cases explored:
  A. r_i and λ exactly anti-phase   (δ = π)        → C_peak = −1 at τ=0
  B. r_i and λ exactly in phase     (δ = 0)        → C_peak = +1 at τ=0
  C. quarter-phase shifted          (δ = π/2)      → C(0)=0, C_peak ≈ ±1 at τ = ±T/4
  D. delayed reaction via gas flow  (δ = ω·τ_lag)  → C_peak at τ = τ_lag, sign depends
  E. opposite-side cavity-lump      (lambda peaks when r_i is large)
                                                   → C_peak = +1 at τ=0 (POSITIVE!)
  F. additive noise added to (B)    → |C_peak| < 1 but sign preserved

What this shows:
  - C(λ, r_2) positive does NOT necessarily contradict the "wall feeds
    the nearer BH" picture; it depends on whether the gas response at
    BH_2 is to the *near* cavity edge (anti-phase → negative C) or to
    the *opposite-side lump* (in-phase → positive C).
  - τ_peak ≠ 0 with large |C| implies a delayed reaction — the gas
    needs travel time. The sign of τ_peak says who leads whom.

Output: numerics_audit/correlation_phase_toy.pdf
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import zscore

sys.stdout.reconfigure(line_buffering=True)

V3 = Path(__file__).resolve().parent.parent
OUT = V3 / "numerics_audit"
OUT.mkdir(exist_ok=True)


def lag_corr(x, y, max_lag):
    n = len(x)
    lags = np.arange(-max_lag, max_lag + 1)
    out = np.zeros_like(lags, dtype=float)
    for i, k in enumerate(lags):
        if k < 0:
            a, b = x[-k:], y[:n + k]
        elif k > 0:
            a, b = x[:n - k], y[k:]
        else:
            a, b = x, y
        if a.std() > 0 and b.std() > 0:
            out[i] = np.corrcoef(a, b)[0, 1]
    return lags, out


# Time array — 70 cycles of a baseline period T=100
t = np.linspace(0, 7000, 7000)
T = 100.0
omega = 2 * np.pi / T

# We'll plot 6 cases in a 3x2 grid:
cases = [
    ('A: anti-phase (δ=π) — naive "wall feeds near BH"', lambda: (
        np.cos(omega * t),
        -np.cos(omega * t),
    )),
    ('B: in-phase (δ=0) — opposite-side lump or "lag = T/2 mod period"', lambda: (
        np.cos(omega * t),
        np.cos(omega * t),
    )),
    ('C: quarter phase (δ=π/2) — derivative coupling', lambda: (
        np.cos(omega * t),
        np.cos(omega * t - np.pi / 2),
    )),
    ('D: delayed reaction τ_lag=25 (= T/4)', lambda: (
        np.cos(omega * t),
        np.cos(omega * (t - 25)),
    )),
    ('E: delayed reaction τ_lag=15 + opposite sign', lambda: (
        np.cos(omega * t),
        -np.cos(omega * (t - 15)),
    )),
    ('F: in-phase + noise (SNR=2)', lambda: (
        np.cos(omega * t) + 0.5 * np.random.RandomState(1).randn(len(t)),
        np.cos(omega * t) + 0.5 * np.random.RandomState(2).randn(len(t)),
    )),
]

MAX_LAG = 80   # in samples; sample step is 1 time-unit -> ±80 units (~0.8 period)

fig, axes = plt.subplots(3, 4, figsize=(20, 10))
print(f"{'case':<55s}  {'C(0)':>7}  {'peakC':>7}  {'tau_peak':>9}")
print("=" * 85)
for row, (title, gen) in enumerate(cases[:3]):
    x, y = gen()
    x_z = zscore(x)
    y_z = zscore(y)
    lags, c = lag_corr(x_z, y_z, MAX_LAG)
    i_abs = np.argmax(np.abs(c))
    peak_c, tau_peak, c0 = c[i_abs], lags[i_abs], c[len(c) // 2]
    print(f"{title:<55s}  {c0:+7.3f}  {peak_c:+7.3f}  {tau_peak:+9.0f}")

    # Time-series panel
    ax = axes[row, 0]
    ax.plot(t[:400], x[:400], 'b-', lw=1.0, label=r'$\lambda(t)$ (proxy)')
    ax.plot(t[:400], y[:400], 'r-', lw=1.0, label=r'$r_i(t)$ (proxy)')
    ax.set_title(title, fontsize=9)
    ax.set_xlabel('t'); ax.set_ylabel('signal')
    if row == 0:
        ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # C(τ) panel
    ax = axes[row, 1]
    ax.plot(lags, c, 'k-', lw=1.4)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.axvline(tau_peak, color='red', lw=0.6, ls='--', alpha=0.7)
    ax.set_title(f'$C(0)={c0:+.2f}$, $C_{{\\rm peak}}={peak_c:+.2f}$ @ $\\tau_{{\\rm peak}}={tau_peak:+d}$', fontsize=10)
    ax.set_xlabel(r'lag $\tau$ (samples)'); ax.set_ylabel(r'$C(\tau)$')
    ax.set_ylim(-1.1, 1.1)
    ax.grid(alpha=0.3)

for row, (title, gen) in enumerate(cases[3:]):
    x, y = gen()
    x_z = zscore(x)
    y_z = zscore(y)
    lags, c = lag_corr(x_z, y_z, MAX_LAG)
    i_abs = np.argmax(np.abs(c))
    peak_c, tau_peak, c0 = c[i_abs], lags[i_abs], c[len(c) // 2]
    print(f"{title:<55s}  {c0:+7.3f}  {peak_c:+7.3f}  {tau_peak:+9.0f}")

    ax = axes[row, 2]
    ax.plot(t[:400], x[:400], 'b-', lw=1.0, label=r'$\lambda(t)$ (proxy)')
    ax.plot(t[:400], y[:400], 'r-', lw=1.0, label=r'$r_i(t)$ (proxy)')
    ax.set_title(title, fontsize=9)
    ax.set_xlabel('t'); ax.set_ylabel('signal')
    ax.grid(alpha=0.3)

    ax = axes[row, 3]
    ax.plot(lags, c, 'k-', lw=1.4)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.axvline(tau_peak, color='red', lw=0.6, ls='--', alpha=0.7)
    ax.set_title(f'$C(0)={c0:+.2f}$, $C_{{\\rm peak}}={peak_c:+.2f}$ @ $\\tau_{{\\rm peak}}={tau_peak:+d}$', fontsize=10)
    ax.set_xlabel(r'lag $\tau$ (samples)'); ax.set_ylabel(r'$C(\tau)$')
    ax.set_ylim(-1.1, 1.1)
    ax.grid(alpha=0.3)

fig.suptitle(r'Toy model: phase-shift signatures in C(τ) between λ(t) proxy and $r_i$(t) proxy. '
             'Period T = 100.', fontsize=12, y=1.00)
plt.tight_layout()
out_path = OUT / "correlation_phase_toy.pdf"
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"\nSaved {out_path}")

# ---------------------------------------------------------------
# Key takeaway table for the email/email-Zoltan-back content
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("Cheat sheet for interpreting the data:")
print("=" * 70)
print("""
  C(τ_peak) = +1, τ_peak = 0   → λ and r_i co-move identically.
                                  Possible: opposite-side cavity lump
                                  drives accretion; OR shared phase
                                  modulation (cavity precesses, both
                                  metrics track it the same way).

  C(τ_peak) = −1, τ_peak = 0   → λ and r_i mirror images.
                                  This is the naive "wall feeds nearer
                                  BH" prediction.

  C(τ_peak) = +1, τ_peak > 0   → r_i lags λ by τ_peak — "λ moves first,
                                  geometry responds later."
                                  Or: gas accretes BH_i, depleting that
                                  side of the cavity; cavity expands
                                  near BH_i a viscous time later.

  C(τ_peak) = +1, τ_peak < 0   → λ lags r_i by |τ_peak| — "geometry
                                  changes first, gas responds after a
                                  viscous time." This IS the gas-travel
                                  picture, but with SAME sign (opposite-
                                  side feeding) rather than wall-feeds-
                                  nearest-BH.

  |C(τ_peak)| < 0.3            → no clean phase relationship; multiple
                                  mechanisms compete.
""")
