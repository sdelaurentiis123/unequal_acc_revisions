#!/usr/bin/env python3
"""
Companion FFT figure for Fig 6 (Zoltan broad comment #4b).

For two representative sims that exhibit non-trivial lambda(t) behavior
(upper-right and middle-right panels of Fig 6: (e_b, q_b) = (0.8, 0.3)
and (0.4, 0.7)), shows time-series of lambda, r_1, r_2 alongside their
power spectra (normalized rFFT amplitudes vs period).

The post-3000 tau_b window is used (matches the paper's analysis cut),
giving N=700 points at the 10 tau_b snapshot cadence.

Output: fourier_panels_fig6.pdf
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt

# Sims Zoltan flagged: upper-right and middle-right of Fig 6
sim_list = [(0.8, 0.3), (0.4, 0.7)]
T_CUT = 3000  # transient cut (matches paper)

fig, axes = plt.subplots(2, 2, figsize=(12, 6.5),
                         gridspec_kw={'hspace': 0.35, 'wspace': 0.45})

PERIOD_MIN, PERIOD_MAX = 20, 5000  # tau_b — display window for periodogram

for row, (eb, qb) in enumerate(sim_list):
    pickle_file = f"/Users/stanislavdelaurentiis/roman_work/metrics_data/data_eb_{eb}_qb_{qb}"
    with open(pickle_file, 'rb') as f:
        d = pickle.load(f)

    time = d['time']
    lam = d['mdot2'] / d['mdot1']
    r1 = d['rmin1']
    r2 = d['rmin2']

    # Apply 3000 tau_b transient cut
    keep = time >= T_CUT
    t = time[keep]
    lam = lam[keep]
    r1 = r1[keep]
    r2 = r2[keep]

    dt = np.median(np.diff(t))  # ~10 tau_b
    N = len(t)
    print(f"({eb}, {qb}): N={N}, dt={dt:.2f} tau_b, span {t[0]:.0f}-{t[-1]:.0f}")

    # ---- Left col: time series ----
    ax = axes[row][0]
    ax.plot(t, lam, color='black', alpha=0.85, lw=0.9)
    ax.set_yscale('log')
    ax.set_ylim(1e-1, 1e1)
    ax.set_ylabel(r'$\lambda$', fontsize=13)
    ax.text(0.02, 0.96, rf'$e_b={eb},\ q_b={qb}$',
            transform=ax.transAxes, ha='left', va='top', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.2',
                      facecolor='white', edgecolor='gray', alpha=0.9))

    twinax = ax.twinx()
    twinax.plot(t, r1, color='blue', alpha=0.7, lw=0.9)
    twinax.plot(t, r2, color='red', alpha=0.7, lw=0.9)
    twinax.set_ylim(0, 5)
    twinax.set_ylabel(r'$r_1, r_2 \, [a]$', fontsize=13)

    if row == 1:
        ax.set_xlabel(r'Time $[\tau_b]$', fontsize=13)
    ax.set_xlim(t[0], t[-1])

    # ---- Right col: power spectra (normalized rFFT amplitudes vs period) ----
    ax = axes[row][1]

    def power_spectrum(signal):
        """Match paper's convention: rFFT amplitudes normalized by sum."""
        sig = signal - np.mean(signal)
        amp = np.abs(np.fft.rfft(sig))
        amp[0] = 0.0
        if amp.sum() > 0:
            amp /= amp.sum()
        freqs = np.fft.rfftfreq(N, d=dt)
        with np.errstate(divide='ignore'):
            periods = 1.0 / freqs
        return periods, amp

    P_lam, A_lam = power_spectrum(lam)
    P_r1, A_r1 = power_spectrum(r1)
    P_r2, A_r2 = power_spectrum(r2)

    ax.plot(P_lam, A_lam, color='black', lw=1.4, label=r'$\lambda$')
    ax.plot(P_r1, A_r1, color='blue', lw=1.0, alpha=0.8, label=r'$r_1$')
    ax.plot(P_r2, A_r2, color='red', lw=1.0, alpha=0.8, label=r'$r_2$')

    ax.axhline(0.05, color='gray', linestyle=':', alpha=0.5, lw=0.8)
    ax.text(PERIOD_MIN * 1.5, 0.052, 'threshold = 0.05',
            ha='left', va='bottom', fontsize=8, color='gray')

    # Mark dominant peak (above threshold) for each
    for periods, amp, color in [(P_lam, A_lam, 'black'),
                                  (P_r1, A_r1, 'blue'),
                                  (P_r2, A_r2, 'red')]:
        mask = (periods >= PERIOD_MIN) & (periods <= PERIOD_MAX) & (amp > 0.05)
        if mask.any():
            i = np.argmax(amp * mask)
            ax.axvline(periods[i], color=color, alpha=0.3, lw=0.8, linestyle='--')
            ax.text(periods[i] * 1.05, amp[i],
                    rf'$\tau={periods[i]:.0f}\,\tau_b$',
                    color=color, fontsize=8, va='bottom')

    ax.set_xscale('log')
    ax.set_xlim(PERIOD_MIN, PERIOD_MAX)
    ax.set_ylim(0, max(A_lam[1:].max(), A_r1[1:].max(), A_r2[1:].max()) * 1.15)
    ax.set_ylabel('Normalized amplitude', fontsize=12)
    if row == 1:
        ax.set_xlabel(r'Period $[\tau_b]$', fontsize=13)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.85)

out = 'fourier_panels_fig6.pdf'
plt.savefig(out, bbox_inches='tight', dpi=150)
print(f"Wrote {out}")
