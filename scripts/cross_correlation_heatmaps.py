#!/usr/bin/env python3
"""
Cross-correlation heatmaps across the (e_b, q_b) suite.

One panel per metric pair. Each panel shows the *signed peak* cross-
correlation C(tau) value for that pair across the simulation grid, on a
diverging colormap centered at 0. Reads sweep_summary.csv produced by
cross_correlation_sweep.py.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'cross_corr')
SUMMARY = os.path.join(OUT, 'sweep_summary.csv')

ECC = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
QB = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

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

LABEL = {
    'lambda': r'\lambda',
    'rmin1': 'r_1', 'rmin2': 'r_2',
    'mdot1': r'\dot{M}_1', 'mdot2': r'\dot{M}_2',
    'alpha1': r'\alpha_1', 'alpha2': r'\alpha_2',
    'mass_disk1': r'M_{\rm d,1}', 'mass_disk2': r'M_{\rm d,2}',
}


def build_grid(df, pair, field='peak_C'):
    a, b = pair
    sub = df[df['pair'] == f'{a}-{b}']
    g = np.full((len(QB), len(ECC)), np.nan)
    for _, r in sub.iterrows():
        i = QB.index(r['qb'])
        j = ECC.index(r['eb'])
        g[i, j] = r[field]
    return g


def _draw_grid(df, field, signed, title, out_path):
    """Draw a 2x7 panel grid of heatmaps for the 14 PAIRS."""
    fig, axes = plt.subplots(2, 7, figsize=(22, 8),
                             gridspec_kw={'wspace': 0.28, 'hspace': 0.4})
    if signed:
        norm = mcolors.TwoSlopeNorm(vmin=-1.0, vcenter=0.0, vmax=1.0)
        cmap = 'seismic'
    else:
        norm = mcolors.Normalize(vmin=0.0, vmax=1.0)
        cmap = 'viridis'

    last_im = None
    for ax, (a, b) in zip(axes.flatten(), PAIRS):
        g = build_grid(df, (a, b), field=field)
        plotg = g if signed else np.abs(g)
        last_im = ax.imshow(plotg, origin='lower', cmap=cmap, norm=norm,
                            aspect='auto')
        ax.set_xticks(range(len(ECC)))
        ax.set_xticklabels([f'{x:.1f}' for x in ECC], fontsize=7)
        ax.set_yticks(range(len(QB)))
        ax.set_yticklabels([f'{y:.1f}' for y in QB], fontsize=7)
        ax.set_title(rf'${LABEL[a]}$ vs ${LABEL[b]}$', fontsize=10)
        ax.set_xlabel(r'$e_b$', fontsize=9)
        ax.set_ylabel(r'$q_b$', fontsize=9)
        for i in range(len(QB)):
            for j in range(len(ECC)):
                v = g[i, j]
                if not np.isfinite(v):
                    continue
                if signed:
                    color = 'white' if abs(v) > 0.55 else 'black'
                    txt = f'{v:.2f}'
                else:
                    color = 'black' if abs(v) > 0.6 else 'white'
                    txt = f'{abs(v):.2f}'
                ax.text(j, i, txt, ha='center', va='center', fontsize=5.5,
                        color=color)

    cbar = fig.colorbar(last_im, ax=axes, location='right', shrink=0.75,
                        pad=0.02)
    if signed and field == 'peak_C':
        cbar.set_label(r'Signed peak cross-correlation $C(\tau_{\rm peak})$',
                       fontsize=11)
    elif signed and field == 'C_at_zero_lag':
        cbar.set_label(r'Zero-lag cross-correlation $C(0)$', fontsize=11)
    elif field == 'peak_C':
        cbar.set_label(r'$|C(\tau_{\rm peak})|$', fontsize=11)
    else:
        cbar.set_label(r'$|C(0)|$', fontsize=11)
    fig.suptitle(title, fontsize=12, y=1.0)
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close(fig)
    print(f'Wrote {out_path}')


def main():
    df = pd.read_csv(SUMMARY)

    _draw_grid(
        df, field='peak_C', signed=True,
        title=r'Lagged cross-correlations across the $(e_b, q_b)$ suite '
              r'(snapshot cadence $10\,\tau_b$, $|\tau| \leq 1000\,\tau_b$)',
        out_path=os.path.join(OUT, 'cross_corr_heatmaps.pdf'))

    _draw_grid(
        df, field='peak_C', signed=False,
        title=r'Magnitude of lagged cross-correlations across the '
              r'$(e_b, q_b)$ suite',
        out_path=os.path.join(OUT, 'cross_corr_heatmaps_magnitude.pdf'))

    _draw_grid(
        df, field='C_at_zero_lag', signed=True,
        title=r'Zero-lag (no shift) cross-correlations across the '
              r'$(e_b, q_b)$ suite',
        out_path=os.path.join(OUT, 'cross_corr_heatmaps_zerolag.pdf'))

    _draw_grid(
        df, field='C_at_zero_lag', signed=False,
        title=r'Magnitude of zero-lag cross-correlations across the '
              r'$(e_b, q_b)$ suite',
        out_path=os.path.join(OUT,
                              'cross_corr_heatmaps_zerolag_magnitude.pdf'))


if __name__ == '__main__':
    main()
