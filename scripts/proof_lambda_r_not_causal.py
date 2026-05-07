#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig 6 (proof_of_lambda_r_not_causal). Same data as v2 (lambda on left,
r_1 / r_2 on right). Only change vs v2 is the panel concatenation per
Zoltan annotation 7.1: sharex/sharey + hspace=wspace=0; inner ticks
suppressed.
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(3, 2, figsize=(7.0, 6.5),
                       sharex=True, sharey=True,
                       gridspec_kw={'hspace': 0.0, 'wspace': 0.0})

sim_param_list = [(0.5, 0.8), (0.8, 0.3),
                  (0.8, 1.0), (0.4, 0.7),
                  (0.2, 0.1), (0.5, 0.7)]

start_time = 5000
end_time = 10000

twin_axes = [[None, None] for _ in range(3)]

for idx, (eb, qb) in enumerate(sim_param_list):
    i = idx // 2
    j = idx % 2
    print(eb, qb)

    pickle_file_path = f"/Users/stanislavdelaurentiis/roman_work/metrics_data/data_eb_{eb}_qb_{qb}"
    with open(pickle_file_path, 'rb') as f:
        cucumber_file = pickle.load(f)
    time = cucumber_file['time']
    lambda_full = cucumber_file['mdot2'] / cucumber_file['mdot1']  # secondary / primary
    rmin1 = cucumber_file['rmin1']
    rmin2 = cucumber_file['rmin2']
    indices = np.where((time >= start_time) & (time <= end_time))[0]

    ax[i][j].plot(time[indices], lambda_full[indices], color='black', alpha=0.8)
    ax[i][j].set_yscale('log')
    ax[i][j].set_ylim(3e-2, 3e1)  # padding so 10^-1 / 10^1 ticks don't crush at panel boundaries

    ax[i][j].text(0.03, 0.97, rf'$e_b$={eb}, $q_b$={qb}',
                  transform=ax[i][j].transAxes,
                  ha='left', va='top', fontsize=9,
                  bbox=dict(boxstyle='round,pad=0.15',
                            facecolor='white', edgecolor='gray', alpha=0.9))

    twinax = ax[i][j].twinx()
    twinax.plot(time[indices], rmin1[indices], color='blue', alpha=0.8)
    twinax.plot(time[indices], rmin2[indices], color='red', alpha=0.8)
    twinax.set_ylim(-0.4, 5.6)  # padding so 0 / 5 ticks don't crush
    twin_axes[i][j] = twinax

for i in range(3):
    for j in range(2):
        if j == 0:
            ax[i][j].set_ylabel(r'$\lambda$')
        else:
            ax[i][j].tick_params(labelleft=False)
        if j == 1:
            twin_axes[i][j].set_ylabel(r'$r_1, r_2 \, [a]$')
        else:
            twin_axes[i][j].tick_params(labelright=False)
        if i == 2:
            ax[i][j].set_xlabel(r'Time $[\tau_b]$')

fig.savefig('proof_of_lambda_r_not_causal.pdf', bbox_inches='tight')
print("Wrote proof_of_lambda_r_not_causal.pdf")
