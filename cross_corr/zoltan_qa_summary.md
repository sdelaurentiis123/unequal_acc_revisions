# Cross-correlation Q&A for Zoltan

## Q1. Normalization

YES, standard Pearson form. `np.corrcoef` after explicit z-score in `scripts/cross_correlation_sweep.py:79`. Confirmed by range check: peak_C in [-0.941, +0.998].

## Q2. Negative correlations

- λ ≡ Ṁ₂/Ṁ₁ and r_i is BH-i-to-cavity-wall distance.
- Negative C(λ, r_2) means: small r_2 (BH-2 near wall) ↔ large λ (Ṁ₂ wins). Exactly the cavity-distance prediction.
- Negative is the *expected* sign for the cavity-distance picture; positive C(λ, r_2) would be the surprise.

For λ↔r_1: 41/80 cells have C<0, median signed C = -0.11.
For λ↔r_2: 36/80 cells have C<0, median signed C = +0.10.

## Q3. τ_peak vs gas travel timescale

Reference timescales:
- BH orbital transit ~ r/v_orb ≈ 0.24 τ_b (below 10 τ_b cadence)
- Viscous (h/r=0.1, α=0.1) ~ 100 τ_b
- Viscous (h/r=0.05, α=0.1) ~ 400 τ_b

**lambda-rmin1**: τ_peak range [-990, +960] τ_b, median |τ_peak| = 115 τ_b.
**lambda-rmin2**: τ_peak range [-960, +950] τ_b, median |τ_peak| = 100 τ_b.
**rmin1-rmin2**: τ_peak range [-950, +510] τ_b, median |τ_peak| = 35 τ_b.
