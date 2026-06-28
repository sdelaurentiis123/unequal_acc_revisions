#!/usr/bin/env python3 -u
"""
τ_peak heatmaps for λ↔r_1 and λ↔r_2 — final clean version.

Uses STANDARDIZED phase φ from the (r_i trough → λ peak) anchor.
Trough used for BOTH r_1 and r_2 (so the two panels are mirror images
when r_1 and r_2 are anti-phase).

Both numbers shown in each cell are derived from the SAME source:
  - φ                = standardized phase in (-π, +π]
  - τ (in τ_b)       = φ · T / (2π)  — the trough-to-peak lag, NOT the
                       cross-corr argmax (those would be inconsistent
                       with φ for negative-C_peak cells)

Falls back to T_lam (λ's FFT period) if T_r2 is missing/extreme.

Visual:
  - Uniform-square cells (imshow + aspect='equal')
  - All 80 cells filled
  - Lime outline: |C_peak| ≥ 0.7 (clean cross-correlation regime)

Output: numerics_audit/tau_peak_panel.pdf
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

V3 = Path(__file__).resolve().parent.parent
OUT = V3 / "numerics_audit"
SWEEP = V3 / "cross_corr" / "sweep_summary.csv"
PHASE = V3 / "cross_corr" / "phase_anchor_summary.csv"

sweep = pd.read_csv(SWEEP)
phase = pd.read_csv(PHASE)

ECC = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
QB  = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def wrap_pm_pi_deg(phi_deg):
    return ((phi_deg + 180) % 360) - 180


# Build the panel
fig, axes = plt.subplots(1, 2, figsize=(17, 9))

for ax, sweep_pair, phase_field, label in zip(
        axes,
        ['lambda-rmin1', 'lambda-rmin2'],
        ['phi_r1', 'phi_r2'],
        [r'$\lambda$ vs $r_1$', r'$\lambda$ vs $r_2$']):

    sweep_sub = sweep[sweep.pair == sweep_pair].set_index(['qb', 'eb'])
    phi_grid_rad = np.full((len(QB), len(ECC)), np.nan)
    tau_grid     = np.full((len(QB), len(ECC)), np.nan)
    peak_grid    = np.full((len(QB), len(ECC)), np.nan)

    for i, qb in enumerate(QB):
        for j, eb in enumerate(ECC):
            try:
                pc = float(sweep_sub.loc[(qb, eb), 'peak_C'])
                phi_row = phase[(phase.eb == eb) & (phase.qb == qb)]
                if phi_row.empty:
                    continue
                phi_deg = float(phi_row[phase_field].iloc[0])
                # Fall back to T_lam if T_r2 isn't usable
                T = float(phi_row['T_r2'].iloc[0])
                if not np.isfinite(T) or T <= 0 or T > 1500:
                    T = float(phi_row['T_lam'].iloc[0])
                peak_grid[i, j] = pc
                if np.isfinite(phi_deg) and np.isfinite(T) and T > 0:
                    phi_signed_deg = wrap_pm_pi_deg(phi_deg)
                    phi_grid_rad[i, j] = np.radians(phi_signed_deg)
                    # τ from φ — same physical lag, in τ_b
                    tau_grid[i, j] = phi_signed_deg / 360.0 * T
            except KeyError:
                pass

    im = ax.imshow(phi_grid_rad, cmap='twilight_shifted',
                   vmin=-np.pi, vmax=np.pi, aspect='equal',
                   origin='lower', interpolation='nearest')

    for i, qb in enumerate(QB):
        for j, eb in enumerate(ECC):
            phi = phi_grid_rad[i, j]
            tau = tau_grid[i, j]
            pc  = peak_grid[i, j]
            if np.isfinite(phi):
                norm = (phi + np.pi) / (2 * np.pi)
                color = 'white' if (0.15 < norm < 0.4 or 0.65 < norm < 0.9) else 'black'
                ax.text(j, i,
                        f"{phi/np.pi:+.2f}π\n{int(tau):+d} τ_b",
                        ha='center', va='center',
                        fontsize=8.5, color=color, weight='bold',
                        linespacing=0.9)
            else:
                # Cell with no period data — paint it neutral and mark
                ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1,
                                       facecolor='lightgray', edgecolor='none',
                                       zorder=1))
                ax.text(j, i, '—', ha='center', va='center',
                        fontsize=12, color='dimgray', weight='bold', zorder=2)
            if np.isfinite(pc) and abs(pc) >= 0.7:
                ax.add_patch(Rectangle((j - 0.45, i - 0.45), 0.9, 0.9,
                                       fill=False, edgecolor='lime', lw=2.2,
                                       zorder=3))

    cbar = plt.colorbar(im, ax=ax, label=r'standardized $\phi$  (rad)',
                        ticks=[-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
                        fraction=0.045, pad=0.04)
    cbar.ax.set_yticklabels([r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
    ax.set_xticks(range(len(ECC)))
    ax.set_xticklabels([f'{e:.1f}' for e in ECC], fontsize=11)
    ax.set_yticks(range(len(QB)))
    ax.set_yticklabels([f'{q:.1f}' for q in QB], fontsize=11)
    ax.set_xlabel(r'$e_b$', fontsize=13)
    ax.set_ylabel(r'$q_b$', fontsize=13)
    ax.set_title(label + r'   —   text: $\phi$ / $\tau_{\rm peak}$', fontsize=12)
    ax.set_xlim(-0.5, len(ECC) - 0.5)
    ax.set_ylim(-0.5, len(QB) - 0.5)

fig.suptitle(
    r'Standardized phase $\phi$ from ($r_i$ trough $\to$ $\lambda$ peak), wrapped to $(-\pi, +\pi]$.   '
    r'Lime outline: $|C_{\rm peak}| \geq 0.7$.',
    fontsize=11, y=0.98)
plt.tight_layout()
out = OUT / "tau_peak_panel.pdf"
plt.savefig(out, bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"Saved {out}")

# Summary
print()
for sweep_pair, phase_field, label in [
        ('lambda-rmin1', 'phi_r1', 'λ↔r₁'),
        ('lambda-rmin2', 'phi_r2', 'λ↔r₂')]:
    sweep_sub = sweep[sweep.pair == sweep_pair][['eb', 'qb', 'peak_C', 'peak_lag_tau_b']]
    merged = sweep_sub.merge(phase[['eb', 'qb', phase_field]], on=['eb', 'qb'])
    merged['phi_signed_deg'] = wrap_pm_pi_deg(merged[phase_field])
    merged['phi_signed_pi']  = merged['phi_signed_deg'] / 180
    clean = merged[merged.peak_C.abs() >= 0.7]
    print(f"{label}: {len(clean)} clean cells")
    print(f"  median signed φ = {clean.phi_signed_pi.median():+.2f}π = "
          f"{clean.phi_signed_deg.median():+.0f}°")
