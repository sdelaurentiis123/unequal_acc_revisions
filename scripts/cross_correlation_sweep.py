#!/usr/bin/env python3
"""
Lagged cross-correlation C(tau) between the headline metrics across the full
(e_b, q_b) suite.

For each sim:
- Builds the time-series: lambda = mdot2/mdot1, mdot1, mdot2, rmin1, rmin2,
  alpha1, alpha2, mass_disk1, mass_disk2.
- Applies the paper's 3000 tau_b transient cut.
- z-scores each series.
- Computes the lagged Pearson cross-correlation C_{XY}(tau) over lags
  +/- MAX_LAG snapshots (snapshot cadence = 10 tau_b).
- Reports peak |C|, the lag at the peak (in tau_b), and zero-lag C.

Outputs:
- cross_corr/sweep_summary.csv: one row per (e_b, q_b, pair) with metrics.
- cross_corr/headline_panel.pdf: C(tau) curves for two representative sims
  comparing the key pairs.
"""
import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore

DATA = '/Users/stanislavdelaurentiis/roman_work/metrics_data'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'cross_corr')
os.makedirs(OUT, exist_ok=True)

ECC = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
QB = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
T_CUT = 3000.0           # tau_b — discard transient (matches paper)
MAX_LAG = 20             # in snapshots; snapshot cadence = 10 tau_b -> +/- 200 tau_b
                         # Covers orbital up to viscous timescales without picking
                         # up spurious matches at multi-precession-period lags
                         # (cavity precession period ~350 tau_b in clean cells).
DT_TAU = 10.0            # snapshot cadence in tau_b

METRICS = ['lambda', 'mdot1', 'mdot2', 'rmin1', 'rmin2',
           'alpha1', 'alpha2', 'mass_disk1', 'mass_disk2']

# Headline pairs we care about for the paper
PAIRS = [
    ('lambda', 'rmin1'),
    ('lambda', 'rmin2'),
    ('lambda', 'mdot1'),
    ('lambda', 'mdot2'),
    ('rmin1', 'rmin2'),
    ('mdot1', 'mdot2'),
    ('mdot1', 'rmin1'),
    ('mdot1', 'rmin2'),
    ('mdot2', 'rmin1'),
    ('mdot2', 'rmin2'),
    ('lambda', 'alpha1'),
    ('lambda', 'alpha2'),
    ('lambda', 'mass_disk1'),
    ('lambda', 'mass_disk2'),
]


def lag_corr(x, y, max_lag):
    """Pearson cross-correlation as a function of integer lag in [-max_lag, max_lag].

    Sign convention: positive lag means y is delayed relative to x
    (i.e., x leads y by `lag` snapshots if the peak is at positive lag).
    """
    n = len(x)
    lags = np.arange(-max_lag, max_lag + 1)
    out = np.zeros_like(lags, dtype=float)
    for i, k in enumerate(lags):
        if k < 0:
            a = x[-k:]
            b = y[:n + k]
        elif k > 0:
            a = x[:n - k]
            b = y[k:]
        else:
            a, b = x, y
        if len(a) > 2 and a.std() > 0 and b.std() > 0:
            out[i] = np.corrcoef(a, b)[0, 1]
        else:
            out[i] = np.nan
    return lags, out


def load_sim(eb, qb):
    path = os.path.join(DATA, f'data_eb_{eb}_qb_{qb}')
    with open(path, 'rb') as f:
        d = pickle.load(f)
    keys = ['time', 'mdot1', 'mdot2', 'rmin1', 'rmin2',
            'alpha1', 'alpha2', 'mass_disk1', 'mass_disk2']
    # A handful of sims have ragged arrays; clip everything to the common length
    n = min(len(d[k]) for k in keys)
    arr = {k: np.asarray(d[k])[:n] for k in keys}
    t = arr['time']
    keep = t >= T_CUT
    m1 = arr['mdot1'][keep]
    series = {
        'lambda': arr['mdot2'][keep] / np.where(m1 != 0, m1, np.nan),
        'mdot1': m1,
        'mdot2': arr['mdot2'][keep],
        'rmin1': arr['rmin1'][keep],
        'rmin2': arr['rmin2'][keep],
        'alpha1': arr['alpha1'][keep],
        'alpha2': arr['alpha2'][keep],
        'mass_disk1': arr['mass_disk1'][keep],
        'mass_disk2': arr['mass_disk2'][keep],
    }
    # Drop NaNs from the lambda construction by replacing with the per-series median
    for k, v in series.items():
        m = np.isfinite(v)
        if not m.all():
            v[~m] = np.nanmedian(v[m]) if m.any() else 0.0
        series[k] = v
    return series


def main():
    rows = []
    for qb in QB:
        for eb in ECC:
            try:
                s = load_sim(eb, qb)
            except FileNotFoundError:
                continue
            # z-score each series so correlations are comparable across metrics
            z = {k: zscore(v, nan_policy='omit') for k, v in s.items()}
            for a, b in PAIRS:
                lags, c = lag_corr(z[a], z[b], MAX_LAG)
                # peak signed correlation (allow negative-correlation peaks)
                i_abs = int(np.nanargmax(np.abs(c)))
                peak_c = float(c[i_abs])
                peak_lag_tau = float(lags[i_abs] * DT_TAU)
                zero_c = float(c[len(c) // 2])
                rows.append({
                    'eb': eb, 'qb': qb, 'pair': f'{a}-{b}',
                    'peak_C': peak_c,
                    'peak_lag_tau_b': peak_lag_tau,
                    'C_at_zero_lag': zero_c,
                })
    df = pd.DataFrame(rows)
    summary_csv = os.path.join(OUT, 'sweep_summary.csv')
    df.to_csv(summary_csv, index=False)
    print(f'Wrote {summary_csv} ({len(df)} rows)')

    # Headline aggregate stats
    print('\n--- Mean(|peak C|) across the suite, by pair ---')
    g = df.groupby('pair').agg(
        mean_abs_peak=('peak_C', lambda x: np.mean(np.abs(x))),
        median_abs_peak=('peak_C', lambda x: np.median(np.abs(x))),
        median_peak_lag=('peak_lag_tau_b', 'median'),
        median_zero_lag=('C_at_zero_lag', 'median'),
    )
    print(g.sort_values('mean_abs_peak', ascending=False).to_string(
        float_format='%.3f'))

    # Headline panel: two representative sims, side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    headline_pairs = [('lambda', 'rmin1'), ('lambda', 'mdot1'),
                      ('lambda', 'mdot2'), ('rmin1', 'rmin2')]
    colors = ['C0', 'C1', 'C2', 'C3']
    for ax, (eb, qb), title in zip(
            axes,
            [(0.6, 1.0), (0.4, 0.7)],
            ['Clean period: $(e_b,q_b)=(0.6, 1.0)$',
             'Messy: $(e_b,q_b)=(0.4, 0.7)$']):
        s = load_sim(eb, qb)
        z = {k: zscore(v) for k, v in s.items()}
        for col, (a, b) in zip(colors, headline_pairs):
            lags, c = lag_corr(z[a], z[b], MAX_LAG)
            ax.plot(lags * DT_TAU, c, color=col, lw=1.4,
                    label=f'{a} vs {b}')
        ax.axhline(0, color='k', lw=0.5, alpha=0.5)
        ax.axvline(0, color='k', lw=0.5, alpha=0.5)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel(r'Lag $[\tau_b]$', fontsize=11)
        ax.set_xlim(-MAX_LAG * DT_TAU, MAX_LAG * DT_TAU)
    axes[0].set_ylabel(r'Cross-correlation $C(\tau)$', fontsize=11)
    axes[1].legend(loc='lower right', fontsize=9, framealpha=0.9)
    plt.tight_layout()
    panel = os.path.join(OUT, 'headline_panel.pdf')
    plt.savefig(panel, bbox_inches='tight')
    print(f'\nWrote {panel}')


if __name__ == '__main__':
    main()
