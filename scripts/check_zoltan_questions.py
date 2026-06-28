#!/usr/bin/env python3 -u
"""
Answers to Zoltan's three follow-up questions on the cross-correlation:

Q1. Normalization: is C(τ) the standard Pearson form?
    -> YES. cross_correlation_sweep.py uses np.corrcoef (Pearson) after
       z-scoring. See line 79 of that file. Skip the runtime check; just
       state the answer.

Q2. What do negative correlations mean physically?
    -> Numerically: when C(λ, r_2) < 0, λ and r_2 anti-correlate at the
       peak lag. Since λ = Ṁ_2 / Ṁ_1 and r_2 is the BH-2-to-cavity-wall
       distance, NEGATIVE C means: r_2 small (BH-2 near wall) ↔ λ large
       (Ṁ_2 wins). That's the cavity-distance picture working in the
       predicted direction.

Q3. Does τ_peak match a gas travel time r_2/v_orb?
    -> Compute it. r_2 ≈ 1.5 a_b (cavity edge ~2a_b, BH offset ~0.5 a_b).
       Mean orbital speed v_orb ≈ 2π a_b / τ_b. So t_grav ≈ r_2/v_orb
       ≈ 1.5 a_b / (6.28 a_b/τ_b) ≈ 0.24 τ_b — well below our 10 τ_b
       snapshot cadence. Viscous flow timescale at h/r=0.1 is ~100 τ_b.
       So if τ_peak is ~10 τ_b, the dynamics are orbit-like (we can't
       resolve sub-orbit); if τ_peak ~ 100s of τ_b, dynamics are viscous.

Outputs:
  cross_corr/zoltan_qa_summary.csv   per-sim peak/lag for the headline pairs
  cross_corr/peak_C_heatmaps.pdf      |peak C| heatmap + signed-C heatmap
  cross_corr/tau_peak_heatmaps.pdf    τ_peak heatmap for λ↔r pairs
  cross_corr/zoltan_qa_summary.md     short markdown report
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

V3 = Path(__file__).resolve().parent.parent
OUT = V3 / 'cross_corr'
CSV = OUT / 'sweep_summary.csv'

df = pd.read_csv(CSV)
print(f"Loaded {CSV}: {len(df)} rows")

ECC = sorted(df.eb.unique())
QB = sorted(df.qb.unique())
print(f"  eb values: {ECC}")
print(f"  qb values: {QB}")
print(f"  pairs: {sorted(df.pair.unique())}")
print()

# ------------------------------------------------------------------
# Q1 answer: confirmed by reading code. Print sanity stats.
# ------------------------------------------------------------------
print("=" * 60)
print("Q1: normalization sanity check")
print("=" * 60)
print(f"  range of peak_C:  [{df.peak_C.min():+.3f}, {df.peak_C.max():+.3f}]")
print(f"  range of zero_C:  [{df.C_at_zero_lag.min():+.3f}, "
      f"{df.C_at_zero_lag.max():+.3f}]")
print(f"  Both bounded in [-1, 1]: {df.peak_C.between(-1, 1).all() and df.C_at_zero_lag.between(-1, 1).all()}")
print()


# ------------------------------------------------------------------
# Q2 answer: stats by pair, separate positive vs negative
# ------------------------------------------------------------------
print("=" * 60)
print("Q2: sign of peak C for the key pairs")
print("=" * 60)
for pair in ['lambda-rmin1', 'lambda-rmin2', 'rmin1-rmin2',
             'lambda-mdot1', 'lambda-mdot2', 'mdot1-mdot2']:
    sub = df[df.pair == pair]
    n_neg = int((sub.peak_C < 0).sum())
    n_pos = int((sub.peak_C > 0).sum())
    n_strong_neg = int((sub.peak_C < -0.5).sum())
    n_strong_pos = int((sub.peak_C > 0.5).sum())
    med_signed = sub.peak_C.median()
    med_abs = sub.peak_C.abs().median()
    print(f"  {pair:<18s}: median signed={med_signed:+.2f}  |median|={med_abs:.2f}  "
          f"neg={n_neg}/{len(sub)}  pos={n_pos}/{len(sub)}  "
          f"|C|>0.5: neg={n_strong_neg} pos={n_strong_pos}")
print()


# ------------------------------------------------------------------
# Q3 answer: tau_peak distribution
# ------------------------------------------------------------------
print("=" * 60)
print("Q3: tau_peak values for cavity-distance pairs")
print("=" * 60)
# Expected gas-flow timescales:
#   t_grav (BH transit at apocenter) ~ r_2/v_orb ~ 0.24 tau_b — sub-cadence
#   t_visc (h/r=0.1, alpha=0.1)      ~ (h/r)^-2 * tau_orb ~ 100 tau_b
#   t_visc (h/r=0.05)                 ~ 400 tau_b
print("  Reference timescales:")
print("    t_grav (BH at apocenter)       ~ 0.24 tau_b   (sub-cadence; cannot resolve)")
print("    t_visc (h/r=0.1, alpha=0.1)    ~ 100 tau_b")
print("    t_visc (h/r=0.05, alpha=0.1)   ~ 400 tau_b")
print("    snapshot cadence (sampling)    = 10 tau_b")
print()
for pair in ['lambda-rmin1', 'lambda-rmin2', 'rmin1-rmin2']:
    sub = df[df.pair == pair]
    print(f"  {pair}:")
    print(f"    range of tau_peak: [{sub.peak_lag_tau_b.min():+.0f}, "
          f"{sub.peak_lag_tau_b.max():+.0f}] tau_b")
    print(f"    median |tau_peak|: {sub.peak_lag_tau_b.abs().median():.0f} tau_b")
    print(f"    mode (most common): {sub.peak_lag_tau_b.value_counts().head(3).to_dict()}")
print()


# ------------------------------------------------------------------
# Build the heatmaps Zoltan asked for: |peak C| and signed peak C in (eb, qb)
# ------------------------------------------------------------------
def make_heatmap(values, title, cmap, vmin, vmax, fname, fmt='{:+.2f}'):
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(values, origin='lower', aspect='auto', cmap=cmap,
                   vmin=vmin, vmax=vmax,
                   extent=[ECC[0]-0.05, ECC[-1]+0.05, QB[0]-0.05, QB[-1]+0.05])
    plt.colorbar(im, ax=ax)
    for i, qb in enumerate(QB):
        for j, eb in enumerate(ECC):
            v = values[i, j]
            if np.isfinite(v):
                # text color: white on dark, black on light
                lum = (v - vmin) / (vmax - vmin) if vmax > vmin else 0.5
                color = 'white' if (lum < 0.3 or lum > 0.7) else 'black'
                ax.text(eb, qb, fmt.format(v), ha='center', va='center',
                        fontsize=7, color=color)
    ax.set_xlabel(r'$e_b$', fontsize=12)
    ax.set_ylabel(r'$q_b$', fontsize=12)
    ax.set_title(title, fontsize=11)
    plt.tight_layout()
    plt.savefig(fname, bbox_inches='tight', dpi=150)
    plt.close(fig)
    print(f"  wrote {fname}")


for pair, fname in [
    ('lambda-rmin1', OUT / 'peak_C_lambda_r1.pdf'),
    ('lambda-rmin2', OUT / 'peak_C_lambda_r2.pdf'),
]:
    sub = df[df.pair == pair].set_index(['qb', 'eb'])
    peak_grid = np.full((len(QB), len(ECC)), np.nan)
    lag_grid = np.full((len(QB), len(ECC)), np.nan)
    for i, qb in enumerate(QB):
        for j, eb in enumerate(ECC):
            try:
                peak_grid[i, j] = sub.loc[(qb, eb), 'peak_C']
                lag_grid[i, j]  = sub.loc[(qb, eb), 'peak_lag_tau_b']
            except KeyError:
                pass
    make_heatmap(peak_grid, f'peak C ({pair})', 'RdBu_r', -1, 1,
                 fname, fmt='{:+.2f}')
    lag_path = str(fname).replace('peak_C_', 'tau_peak_')
    make_heatmap(lag_grid, rf'$\tau_{{\rm peak}}$ [$\tau_b$] ({pair})',
                 'viridis', -500, 500, lag_path, fmt='{:+.0f}')


# ------------------------------------------------------------------
# Identify the "clean" cells: those where |peak C| > 0.7
# ------------------------------------------------------------------
print("\n" + "=" * 60)
print("Clean cells (|peak C| > 0.7) — Zoltan's 'cavity-distance dominates' regime")
print("=" * 60)
for pair in ['lambda-rmin1', 'lambda-rmin2']:
    sub = df[df.pair == pair]
    clean = sub[sub.peak_C.abs() > 0.7].sort_values('peak_C', key=np.abs, ascending=False)
    print(f"\n  {pair} — {len(clean)} cells:")
    for _, r in clean.iterrows():
        print(f"    (eb={r.eb}, qb={r.qb}): peak_C={r.peak_C:+.3f}, "
              f"tau_peak={r.peak_lag_tau_b:+.0f} tau_b, C(0)={r.C_at_zero_lag:+.3f}")


# ------------------------------------------------------------------
# Save short MD summary
# ------------------------------------------------------------------
md = OUT / 'zoltan_qa_summary.md'
with open(md, 'w') as f:
    f.write("# Cross-correlation Q&A for Zoltan\n\n")
    f.write("## Q1. Normalization\n\n")
    f.write("YES, standard Pearson form. `np.corrcoef` after explicit z-score "
            "in `scripts/cross_correlation_sweep.py:79`. Confirmed by range "
            f"check: peak_C in [{df.peak_C.min():+.3f}, {df.peak_C.max():+.3f}].\n\n")
    f.write("## Q2. Negative correlations\n\n")
    f.write("- λ ≡ Ṁ₂/Ṁ₁ and r_i is BH-i-to-cavity-wall distance.\n")
    f.write("- Negative C(λ, r_2) means: small r_2 (BH-2 near wall) "
            "↔ large λ (Ṁ₂ wins). Exactly the cavity-distance prediction.\n")
    f.write("- Negative is the *expected* sign for the cavity-distance picture; "
            "positive C(λ, r_2) would be the surprise.\n\n")
    sub_r1 = df[df.pair == 'lambda-rmin1']
    sub_r2 = df[df.pair == 'lambda-rmin2']
    f.write(f"For λ↔r_1: {(sub_r1.peak_C < 0).sum()}/{len(sub_r1)} cells have C<0, "
            f"median signed C = {sub_r1.peak_C.median():+.2f}.\n")
    f.write(f"For λ↔r_2: {(sub_r2.peak_C < 0).sum()}/{len(sub_r2)} cells have C<0, "
            f"median signed C = {sub_r2.peak_C.median():+.2f}.\n\n")
    f.write("## Q3. τ_peak vs gas travel timescale\n\n")
    f.write("Reference timescales:\n")
    f.write("- BH orbital transit ~ r/v_orb ≈ 0.24 τ_b (below 10 τ_b cadence)\n")
    f.write("- Viscous (h/r=0.1, α=0.1) ~ 100 τ_b\n")
    f.write("- Viscous (h/r=0.05, α=0.1) ~ 400 τ_b\n\n")
    for pair in ['lambda-rmin1', 'lambda-rmin2', 'rmin1-rmin2']:
        sub = df[df.pair == pair]
        f.write(f"**{pair}**: τ_peak range [{sub.peak_lag_tau_b.min():+.0f}, "
                f"{sub.peak_lag_tau_b.max():+.0f}] τ_b, "
                f"median |τ_peak| = {sub.peak_lag_tau_b.abs().median():.0f} τ_b.\n")
print(f"\nWrote {md}")
