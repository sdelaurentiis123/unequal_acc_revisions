#!/usr/bin/env python3 -u
"""
Periodic-phase analysis with a fixed physical anchor.

Problem the previous cross-correlation analysis had: τ_peak is only
defined modulo the precession period T. Reporting raw τ_peak values
across cells with different T's mixes physics with numerics.

Fix: for each sim, measure the precession period T directly, then
express the (r_i trough → λ peak) lag as a phase angle φ ∈ [0°, 360°).

Convention (cavity-distance anchored):
  lag = t(λ peak) − t(preceding r_i trough)
  φ   = lag / T × 360°
  φ small  ↔  trough → peak with quick response (cavity-distance picture)
  φ near 180°  ↔  trough and peak ~half-cycle apart
  φ approaching 360°  ↔  trough comes ~just AFTER λ peak (eating-then-retreat)

Procedure per sim:
  1. Smooth λ(t), r_1(t), r_2(t) lightly (Gaussian, σ = 1 snapshot).
  2. Compute T from the FFT of r_2(t) (dominant non-zero frequency).
     Cross-check against T from λ(t).
  3. Find λ peaks and r_i troughs via scipy.signal.find_peaks.
  4. For each λ peak, find the most recent preceding r_i trough.
     Wrap into [0, T) if needed.
  5. Take median lag across matched events → φ_i (median, in degrees).

Outputs:
  cross_corr/phase_anchor_summary.csv
  numerics_audit/phase_anchor_heatmaps.pdf
  numerics_audit/phase_anchor_distribution.pdf
"""
import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

V3 = Path(__file__).resolve().parent.parent
OUT_FIG = V3 / "numerics_audit"
OUT_CSV = V3 / "cross_corr"
DATA = '/Users/stanislavdelaurentiis/roman_work/metrics_data'

T_CUT = 3000.0       # τ_b — discard transient
DT_TAU = 10.0        # snapshot cadence
SMOOTH_SIGMA = 1.0   # snapshots — light smoothing
PEAK_PROM = 0.5      # in z-scored units
PEAK_DIST = 5        # snapshots = 50 τ_b min separation

ECC = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
QB  = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def load_sim(eb, qb):
    with open(f'{DATA}/data_eb_{eb}_qb_{qb}', 'rb') as f:
        d = pickle.load(f)
    keys = ['time', 'mdot1', 'mdot2', 'rmin1', 'rmin2']
    n = min(len(d[k]) for k in keys)
    arr = {k: np.asarray(d[k])[:n] for k in keys}
    keep = arr['time'] >= T_CUT
    m1 = arr['mdot1'][keep]; m2 = arr['mdot2'][keep]
    lam = m2 / np.where(m1 != 0, m1, np.nan)
    fin = np.isfinite(lam)
    lam[~fin] = np.nanmedian(lam[fin]) if fin.any() else 0.0
    return arr['time'][keep], lam, arr['rmin1'][keep], arr['rmin2'][keep]


def dominant_period(signal, dt):
    """Return the dominant period (in τ_b) of the signal via FFT,
    excluding DC and frequencies below the noise floor.

    Returns (T_dom, S_peak/S_mean) where the second is a peak-strength
    metric for confidence."""
    n = len(signal)
    sig = signal - signal.mean()
    win = np.hanning(n)
    spec = np.abs(np.fft.rfft(sig * win))
    freqs = np.fft.rfftfreq(n, d=dt)
    # Exclude DC and very-low frequencies that just track the window
    # (anything with period > n*dt/2)
    fmin = 2 / (n * dt)
    mask = freqs > fmin
    if not mask.any():
        return np.nan, 0.0
    spec_m = spec[mask]
    freqs_m = freqs[mask]
    i_peak = int(np.argmax(spec_m))
    if spec_m[i_peak] <= 0:
        return np.nan, 0.0
    T = 1.0 / freqs_m[i_peak]
    confidence = float(spec_m[i_peak] / np.median(spec_m))
    return T, confidence


def match_trough_to_peak(t_lam_peaks, t_trough_events, T):
    """For each λ peak, find the most recent r-trough PRECEDING it.
    Return list of lags (peak_time - trough_time) in τ_b.

    Lags should be in [0, T) if the signals are well-paired."""
    if len(t_lam_peaks) == 0 or len(t_trough_events) == 0:
        return np.array([])
    t_trough_events = np.sort(t_trough_events)
    lags = []
    for tp in t_lam_peaks:
        before = t_trough_events[t_trough_events < tp]
        if len(before) == 0:
            continue
        prev = before[-1]
        lag = tp - prev
        # If gap is more than ~1.5 periods, no preceding trough was found
        # in a reasonable window — skip
        if lag > 1.5 * T:
            continue
        lags.append(lag)
    return np.array(lags)


def analyze_sim(eb, qb):
    try:
        t, lam, r1, r2 = load_sim(eb, qb)
    except FileNotFoundError:
        return None
    n = len(t)
    if n < 50:
        return None

    # Smooth
    lam_s = gaussian_filter1d(lam, sigma=SMOOTH_SIGMA)
    r1_s = gaussian_filter1d(r1, sigma=SMOOTH_SIGMA)
    r2_s = gaussian_filter1d(r2, sigma=SMOOTH_SIGMA)

    # z-score for peak-prominence threshold
    def zsafe(x):
        s = x.std()
        return (x - x.mean()) / s if s > 0 else x - x.mean()
    lam_z = zsafe(lam_s); r1_z = zsafe(r1_s); r2_z = zsafe(r2_s)

    # Dominant period from r_2 (proxy for cavity precession)
    T_r2, conf_r2 = dominant_period(r2_s, dt=DT_TAU)
    T_lam, conf_lam = dominant_period(lam_s, dt=DT_TAU)
    # Use r_2's period as canonical, with sanity bound — reject the
    # whole-window FFT artifact (~2300 τ_b for a 7000 τ_b window).
    T_BOUND = 1500.0
    if np.isfinite(T_r2) and 0 < T_r2 < T_BOUND:
        T = T_r2
    elif np.isfinite(T_lam) and 0 < T_lam < T_BOUND:
        T = T_lam
    else:
        T = T_r2  # fall back to whatever we have

    # Find λ peaks and r_i troughs.
    # Anchor: TROUGH for both r_1 and r_2 — gives mirror-image signs
    # for the two pairs when r_1, r_2 are anti-phase.
    # Try the nominal prominence first, then a relaxed fallback for
    # quiet sims that have no peaks at PEAK_PROM = 0.5.
    def _find_peaks(sig, sign=+1):
        for prom in (PEAK_PROM, 0.2, 0.1):
            p, _ = find_peaks(sign * sig, prominence=prom, distance=PEAK_DIST)
            if len(p) >= 3:
                return p
        return p  # whatever we got
    lam_peaks = _find_peaks(lam_z, +1)
    r1_anchors = _find_peaks(r1_z, -1)
    r2_anchors = _find_peaks(r2_z, -1)

    t_lam_peaks = t[lam_peaks]
    t_r1_troughs = t[r1_anchors]
    t_r2_troughs = t[r2_anchors]

    if not np.isfinite(T) or T <= 0 or len(t_lam_peaks) < 3:
        return dict(
            eb=eb, qb=qb,
            T_r2=T_r2, conf_r2=conf_r2,
            T_lam=T_lam, conf_lam=conf_lam,
            n_lam_peaks=len(lam_peaks),
            n_r1_troughs=len(r1_anchors),
            n_r2_troughs=len(r2_anchors),
            phi_r1=np.nan, phi_r2=np.nan,
            lag_r1=np.nan, lag_r2=np.nan,
            n_matches_r1=0, n_matches_r2=0,
        )

    # Compute lags
    lags_r1 = match_trough_to_peak(t_lam_peaks, t_r1_troughs, T)
    lags_r2 = match_trough_to_peak(t_lam_peaks, t_r2_troughs, T)

    lag_r1 = float(np.median(lags_r1)) if len(lags_r1) else np.nan
    lag_r2 = float(np.median(lags_r2)) if len(lags_r2) else np.nan
    phi_r1 = (lag_r1 / T * 360.0) if np.isfinite(lag_r1) else np.nan
    phi_r2 = (lag_r2 / T * 360.0) if np.isfinite(lag_r2) else np.nan

    return dict(
        eb=eb, qb=qb,
        T_r2=T_r2, conf_r2=conf_r2,
        T_lam=T_lam, conf_lam=conf_lam,
        n_lam_peaks=len(lam_peaks),
        n_r1_troughs=len(r1_anchors),
        n_r2_troughs=len(r2_anchors),
        phi_r1=phi_r1, phi_r2=phi_r2,
        lag_r1=lag_r1, lag_r2=lag_r2,
        n_matches_r1=len(lags_r1),
        n_matches_r2=len(lags_r2),
    )


# Run
print("Running phase-anchor analysis across the 80-sim suite...")
rows = []
for qb in QB:
    for eb in ECC:
        r = analyze_sim(eb, qb)
        if r is not None:
            rows.append(r)
df = pd.DataFrame(rows)
df.to_csv(OUT_CSV / "phase_anchor_summary.csv", index=False)
print(f"\nWrote {OUT_CSV / 'phase_anchor_summary.csv'} ({len(df)} rows)\n")

# Summarize
print("Period from r_2 FFT — distribution:")
print(f"  median T_r2: {df.T_r2.median():.0f} τ_b")
print(f"  IQR:         {df.T_r2.quantile(0.25):.0f} – {df.T_r2.quantile(0.75):.0f} τ_b")
print(f"  min, max:    {df.T_r2.min():.0f}, {df.T_r2.max():.0f} τ_b")
print()
high_conf = df[df.conf_r2 > 5]   # peak >5× median spectral power
print(f"High-confidence period (peak-to-median spectral ratio > 5): "
      f"{len(high_conf)}/{len(df)} cells")
print(f"  these have median T_r2 = {high_conf.T_r2.median():.0f} τ_b")
print()

print("=" * 70)
print("Phase (r_2 trough → λ peak) — distribution")
print("Convention: φ ∈ [0°, 360°), 0° = trough and peak coincide,")
print("            small φ = cavity-distance quick response")
print("=" * 70)
ok = df[df.phi_r2.notna()]
print(f"  cells with valid φ_r2: {len(ok)}/{len(df)}")
print(f"  φ_r2 distribution: median={ok.phi_r2.median():.0f}°, "
      f"IQR=[{ok.phi_r2.quantile(0.25):.0f}, {ok.phi_r2.quantile(0.75):.0f}]°")
print()
print("  φ_r2 binned:")
bins = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
hist, _ = np.histogram(ok.phi_r2, bins=bins)
for h, lo, hi in zip(hist, bins[:-1], bins[1:]):
    bar = '#' * h
    print(f"    [{lo:3d}°, {hi:3d}°): {h:2d} {bar}")
print()


# ----------------- visualization -----------------
def e_edges(values):
    e = np.zeros(len(values) + 1)
    e[0] = values[0] - (values[1] - values[0]) / 2
    e[-1] = values[-1] + (values[-1] - values[-2]) / 2
    for i in range(1, len(values)):
        e[i] = (values[i-1] + values[i]) / 2
    return e


def q_edges(values):
    e = np.zeros(len(values) + 1)
    e[0] = values[0] - 0.05
    e[-1] = values[-1] + 0.05
    for i in range(1, len(values)):
        e[i] = (values[i-1] + values[i]) / 2
    return e


e_e = e_edges(ECC); q_e = q_edges(QB)


def build_grid(field):
    g = np.full((len(QB), len(ECC)), np.nan)
    for _, r in df.iterrows():
        try:
            i = QB.index(r['qb'])
            j = ECC.index(r['eb'])
            g[i, j] = r[field]
        except (ValueError, KeyError):
            pass
    return g


# Read clean-cell flags from sweep_summary so we can mark them
sweep = pd.read_csv(OUT_CSV / "sweep_summary.csv")

def clean_cells(pair):
    sub = sweep[sweep.pair == pair]
    cells = set()
    for _, r in sub.iterrows():
        if abs(r.peak_C) >= 0.7:
            cells.add((r.eb, r.qb))
    return cells

clean_r1 = clean_cells('lambda-rmin1')
clean_r2 = clean_cells('lambda-rmin2')


# Panel: φ_r1 and φ_r2 heatmaps — wrap to (-180°, +180°] to match tau_peak_panel
def _wrap_pm_pi_deg(phi_deg):
    return ((phi_deg + 180) % 360) - 180


fig, axes = plt.subplots(1, 2, figsize=(17, 7))
for ax, field, label, clean in zip(axes,
                                    ['phi_r1', 'phi_r2'],
                                    [r'$\phi$  ($r_1$ trough $\to$ $\lambda$ peak)',
                                     r'$\phi$  ($r_2$ trough $\to$ $\lambda$ peak)'],
                                    [clean_r1, clean_r2]):
    g_raw = build_grid(field)
    # wrap each cell to (-180, +180]
    g = np.where(np.isfinite(g_raw), _wrap_pm_pi_deg(g_raw), np.nan)
    pcm = ax.pcolormesh(e_e, q_e, g, cmap='twilight_shifted',
                        vmin=-180, vmax=180, shading='flat')
    plt.colorbar(pcm, ax=ax, label=r'$\phi$  [deg]',
                 ticks=[-180, -90, 0, 90, 180])
    for i, qb in enumerate(QB):
        for j, eb in enumerate(ECC):
            v = g[i, j]
            if not np.isfinite(v):
                continue
            # text color cycle for twilight_shifted readability
            norm = (v + 180) / 360
            color = 'white' if (0.15 < norm < 0.4 or 0.65 < norm < 0.9) else 'black'
            ax.text(eb, qb, f"{v:+.0f}°", ha='center', va='center',
                    fontsize=8, color=color, weight='bold')
            if (eb, qb) in clean:
                ax.add_patch(Rectangle(
                    (e_e[j] + 0.003, q_e[i] + 0.003),
                    e_e[j+1] - e_e[j] - 0.006,
                    q_e[i+1] - q_e[i] - 0.006,
                    fill=False, edgecolor='lime', lw=2.0))
    ax.set_xticks(ECC); ax.set_xticklabels([f'{e:.1f}' for e in ECC], fontsize=10)
    ax.set_yticks(QB); ax.set_yticklabels([f'{q:.1f}' for q in QB], fontsize=10)
    ax.set_xlim(e_e[0], e_e[-1]); ax.set_ylim(q_e[0], q_e[-1])
    ax.set_xlabel(r'$e_b$', fontsize=12)
    ax.set_ylabel(r'$q_b$', fontsize=12)
    ax.set_title(label, fontsize=11)

fig.suptitle(r'Phase anchor: $\phi$ = (lag from $r_i$ trough to $\lambda$ peak) / $T$ × 360°, wrapped to $(-180°, +180°]$.'
             '\n'
             r'$\phi$ small $+$ → cavity-distance quick response.  '
             r'$\phi \to \pm180°$  → half-cycle from trough.  '
             r'Opposite-sign panels → $r_1$, $r_2$ approximately anti-phase.',
             fontsize=10, y=1.02)
plt.tight_layout()
out_path = OUT_FIG / "phase_anchor_heatmaps.pdf"
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"Saved {out_path}")


# Panel: distribution histograms
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
all_phi_r2 = df.phi_r2.dropna()
clean_phi_r2 = df[df.apply(lambda r: (r.eb, r.qb) in clean_r2, axis=1)].phi_r2.dropna()
ax.hist(all_phi_r2, bins=np.linspace(0, 360, 19), color='gray', edgecolor='black',
        alpha=0.6, label=f'all {len(all_phi_r2)} cells')
ax.hist(clean_phi_r2, bins=np.linspace(0, 360, 19), color='lime', edgecolor='black',
        alpha=0.6, label=f'clean λ↔r₂: {len(clean_phi_r2)} cells')
ax.set_xlabel(r'$\phi$  ($r_2$ trough $\to$ $\lambda$ peak)  [deg]')
ax.set_ylabel('count')
ax.set_title(r'Distribution of $\phi_{r_2}$')
ax.set_xticks([0, 60, 120, 180, 240, 300, 360])
ax.axvline(0, color='red', lw=0.5)
ax.axvline(180, color='gray', lw=0.5)
ax.legend(); ax.grid(alpha=0.3)

ax = axes[1]
# Period distribution
all_T = df.T_r2.dropna()
clean_T = df[df.apply(lambda r: (r.eb, r.qb) in clean_r2, axis=1)].T_r2.dropna()
ax.hist(all_T, bins=20, color='gray', edgecolor='black', alpha=0.6,
        label=f'all {len(all_T)} cells')
ax.hist(clean_T, bins=np.linspace(50, 800, 20), color='lime', edgecolor='black',
        alpha=0.6, label=f'clean λ↔r₂: {len(clean_T)} cells')
ax.set_xlabel(r'$T_{r_2}$  [τ_b]  (dominant period from FFT)')
ax.set_ylabel('count')
ax.set_title(r'Distribution of measured precession period')
ax.legend(); ax.grid(alpha=0.3)

plt.tight_layout()
out_path2 = OUT_FIG / "phase_anchor_distribution.pdf"
plt.savefig(out_path2, bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"Saved {out_path2}")
