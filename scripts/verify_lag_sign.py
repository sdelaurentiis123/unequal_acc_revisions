#!/usr/bin/env python3 -u
"""
Sanity check: who actually leads whom in (0.6, 1.0)?

Approach:
  1. Load λ(t) and r_2(t) for (e_b, q_b) = (0.6, 1.0)
  2. Smooth each lightly to suppress noise
  3. Find peaks of each
  4. For each λ peak, find the nearest r_2 peak. Average the time differences.
     If λ peaks consistently EARLIER than the nearest r_2 peak → λ leads.
     If λ peaks consistently LATER → r_2 leads.
  5. Run the cross-correlation on the same data and confirm the lag-sign convention
     agrees with the peak-time difference.
  6. Also do this by ANTI-peaks (troughs) of r_2 — since r_2 small = "BH-2 close
     to wall", the troughs of r_2 are the cavity-distance "close" events.

Plot:
  - Long time-series window with λ peaks (blue ▼) and r_2 peaks (green ▲) marked
  - Cross-correlation curve with τ_peak annotated
  - Histogram of per-peak time differences vs the cross-correlation τ_peak
"""
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d
from scipy.stats import zscore

sys.stdout.reconfigure(line_buffering=True)

V3 = Path(__file__).resolve().parent.parent
DATA = '/Users/stanislavdelaurentiis/roman_work/metrics_data'
T_CUT = 3000.0
DT_TAU = 10.0
MAX_LAG = 20   # ±200 τ_b
EB, QB = 0.6, 1.0

# --- load ---
with open(f'{DATA}/data_eb_{EB}_qb_{QB}', 'rb') as f:
    d = pickle.load(f)
keys = ['time', 'mdot1', 'mdot2', 'rmin1', 'rmin2']
n = min(len(d[k]) for k in keys)
t_all = np.asarray(d['time'])[:n]
keep = t_all >= T_CUT
t = t_all[keep]
m1 = np.asarray(d['mdot1'])[:n][keep]
m2 = np.asarray(d['mdot2'])[:n][keep]
r1 = np.asarray(d['rmin1'])[:n][keep]
r2 = np.asarray(d['rmin2'])[:n][keep]
lam = m2 / np.where(m1 != 0, m1, np.nan)
fin = np.isfinite(lam)
lam[~fin] = np.nanmedian(lam[fin])

print(f"(e_b, q_b) = ({EB}, {QB})")
print(f"  n snapshots after cut: {len(t)}")
print(f"  t range: {t[0]:.0f} to {t[-1]:.0f} τ_b")
print(f"  λ mean = {lam.mean():.3f}, std = {lam.std():.3f}")
print(f"  r_2 mean = {r2.mean():.3f}, std = {r2.std():.3f}")
print()

# Smooth to suppress noise but keep the precession-period oscillations
SIGMA = 1.5  # snapshots; mild smoothing
lam_s = gaussian_filter1d(lam, sigma=SIGMA)
r2_s = gaussian_filter1d(r2, sigma=SIGMA)

# --- peaks ---
PROM = 0.5   # in units of std after z-score
distance = 5  # min 50 τ_b between peaks
lam_z = zscore(lam_s)
r2_z = zscore(r2_s)

lam_peaks, _ = find_peaks(lam_z, prominence=PROM, distance=distance)
r2_peaks, _  = find_peaks(r2_z,  prominence=PROM, distance=distance)
r2_troughs, _ = find_peaks(-r2_z, prominence=PROM, distance=distance)

print(f"  λ peaks found: {len(lam_peaks)}")
print(f"  r_2 peaks found: {len(r2_peaks)}")
print(f"  r_2 troughs found: {len(r2_troughs)}")
print()

# For each λ peak, find the nearest r_2 peak and r_2 trough
# Time difference: t(r_2 event) - t(λ peak).
#   Positive → r_2 event happens AFTER λ peak (λ leads).
#   Negative → r_2 event happens BEFORE λ peak (r_2 leads).
lam_peak_times = t[lam_peaks]
r2_peak_times = t[r2_peaks]
r2_trough_times = t[r2_troughs]

dt_to_r2_peak = []
dt_to_r2_trough = []
for tp in lam_peak_times:
    if len(r2_peak_times) > 0:
        i = int(np.argmin(np.abs(r2_peak_times - tp)))
        dt_to_r2_peak.append(r2_peak_times[i] - tp)
    if len(r2_trough_times) > 0:
        i = int(np.argmin(np.abs(r2_trough_times - tp)))
        dt_to_r2_trough.append(r2_trough_times[i] - tp)

dt_to_r2_peak = np.array(dt_to_r2_peak)
dt_to_r2_trough = np.array(dt_to_r2_trough)

print(f"  Avg time(r_2 peak)   - time(λ peak):   "
      f"{dt_to_r2_peak.mean():+.0f} ± {dt_to_r2_peak.std():.0f} τ_b")
print(f"  Median time(r_2 peak)- time(λ peak):   {np.median(dt_to_r2_peak):+.0f} τ_b")
print(f"  Avg time(r_2 trough) - time(λ peak):   "
      f"{dt_to_r2_trough.mean():+.0f} ± {dt_to_r2_trough.std():.0f} τ_b")
print(f"  Median time(r_2 trough)-time(λ peak):  {np.median(dt_to_r2_trough):+.0f} τ_b")
print()
print("  positive → r_2 event AFTER λ peak → λ leads")
print("  negative → r_2 event BEFORE λ peak → r_2 leads")
print()

# --- cross-correlation for comparison ---
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

lags, c2 = lag_corr(lam_z, r2_z, MAX_LAG)
i_peak = int(np.argmax(np.abs(c2)))
print(f"  Cross-correlation peak: τ_peak = {lags[i_peak] * DT_TAU:+.0f} τ_b, "
      f"C_peak = {c2[i_peak]:+.3f}, C(0) = {c2[len(c2)//2]:+.3f}")

# Convention reminder:
# At k > 0 in lag_corr: corr(x[i], y[i+k]).
# Peak at k > 0 means corr(x(t), y(t+k)) is max, i.e., y(t+k) is most like x(t).
# y(t+k) resembling x(t) means x's pattern at time t shows up in y at time t+k → x leads y by k.

print()
print("  Convention check:")
print(f"  - if τ_peak = +50, that's corr(λ(t), r_2(t+50)) max → λ(t) predicts r_2(t+50)")
print(f"    → λ pattern shows up in r_2 50 τ_b LATER → λ leads r_2")
print()
print(f"  Direct measurement says: median offset = {np.median(dt_to_r2_peak):+.0f} τ_b")
print(f"  Cross-correlation says:  τ_peak     = {lags[i_peak] * DT_TAU:+.0f} τ_b")
agreement = "AGREE" if np.sign(np.median(dt_to_r2_peak)) == np.sign(lags[i_peak] * DT_TAU) else "DISAGREE"
print(f"  Sign agreement: {agreement}")


# --- plot ---
fig, axes = plt.subplots(2, 1, figsize=(15, 8))

# Show a window covering several precession cycles
T_SHOW_START = t[0]
T_SHOW_END = t[0] + 2000  # 2000 τ_b = ~5-6 precession cycles
mask = (t >= T_SHOW_START) & (t <= T_SHOW_END)

ax = axes[0]
ax.plot(t[mask], lam_z[mask], 'b-', lw=1.2, label=r'$\lambda(t)$ (z)')
ax.plot(t[mask], r2_z[mask], 'g-', lw=1.2, label=r'$r_2(t)$ (z)')

# Mark λ peaks
for p in lam_peaks:
    if T_SHOW_START <= t[p] <= T_SHOW_END:
        ax.axvline(t[p], color='blue', alpha=0.3, lw=0.5)
        ax.plot(t[p], lam_z[p], 'bv', markersize=8)

# Mark r_2 peaks
for p in r2_peaks:
    if T_SHOW_START <= t[p] <= T_SHOW_END:
        ax.axvline(t[p], color='green', alpha=0.3, lw=0.5, ls='--')
        ax.plot(t[p], r2_z[p], 'g^', markersize=8)

# Mark r_2 troughs
for p in r2_troughs:
    if T_SHOW_START <= t[p] <= T_SHOW_END:
        ax.plot(t[p], r2_z[p], 'gs', markersize=8, markerfacecolor='lightgreen')

ax.set_xlabel(r'$t\ [\tau_b]$', fontsize=12)
ax.set_ylabel('z-scored signal', fontsize=12)
ax.set_title(rf'$(e_b, q_b) = ({EB}, {QB})$ — '
             r'$\lambda$ (blue ▼ = peak) vs $r_2$ (green ▲ = peak, ◾ = trough)',
             fontsize=11)
ax.legend(loc='upper right', fontsize=10)
ax.axhline(0, color='gray', lw=0.4)
ax.grid(alpha=0.3)

ax = axes[1]
ax.plot(lags * DT_TAU, c2, 'k-', lw=1.5)
ax.axvline(lags[i_peak] * DT_TAU, color='red', ls='--',
           label=rf'$\tau_{{\rm peak}}={lags[i_peak]*DT_TAU:+.0f}\,\tau_b$')
ax.axvline(0, color='gray', lw=0.5)
ax.axhline(0, color='gray', lw=0.5)
ax.axvline(np.median(dt_to_r2_peak), color='green', ls=':',
           label=rf'direct peak-time offset = {np.median(dt_to_r2_peak):+.0f}$\,\tau_b$')
ax.set_xlabel(r'lag $\tau\ [\tau_b]$', fontsize=12)
ax.set_ylabel(r'$C(\tau)$', fontsize=12)
ax.set_title(rf'Cross-correlation $C(\lambda, r_2)(\tau)$  —  search $\pm 200\,\tau_b$',
             fontsize=11)
ax.legend(fontsize=10)
ax.grid(alpha=0.3)

plt.tight_layout()
out = V3 / "numerics_audit" / "verify_lag_sign.pdf"
plt.savefig(out, bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"\nSaved {out}")
