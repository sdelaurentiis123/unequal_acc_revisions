#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig 6 (proof_of_lambda_r_not_causal). Panels concatenated (touching) per
Zoltan annotation 7.1. Inner ticks/labels suppressed; outer labels only.
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

ecclist = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
qblist = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

fig, ax = plt.subplots(3, 2, figsize=(7.0, 6.5),
                       sharex=True, sharey=True,
                       gridspec_kw={'hspace': 0.0, 'wspace': 0.0})

sim_param_list = [(0.5, 0.8), (0.8, 1.0),
                  (0.2, 0.1), (0.8, 0.3),
                  (0.4, 0.7), (0.5, 0.7)]

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
    rmin1 = cucumber_file['rmin1']
    rmin2 = cucumber_file['rmin2']
    indices = np.where((time >= start_time) & (time <= end_time))[0]

    ax[i][j].plot(time[indices], cucumber_file['mdot2'][indices], color='green', alpha=0.8)
    ax[i][j].plot(time[indices], cucumber_file['mdot1'][indices], color='purple', alpha=0.8)
    ax[i][j].set_yscale('log')

    ax[i][j].text(0.97, 0.92, rf'$e_b$={eb}, $q_b$={qb}',
                  transform=ax[i][j].transAxes,
                  ha='right', va='top', fontsize=10,
                  bbox=dict(boxstyle='round,pad=0.2',
                            facecolor='white', edgecolor='gray', alpha=0.85))

    twinax = ax[i][j].twinx()
    twinax.plot(time[indices], rmin1[indices], color='blue', alpha=0.8)
    twinax.plot(time[indices], rmin2[indices], color='red', alpha=0.8)
    twinax.set_ylim(0, 5.5)
    twin_axes[i][j] = twinax

# share twinx scale across all panels (already same ylim) and suppress inner labels
for i in range(3):
    for j in range(2):
        # left-axis (lambda) label only on left column
        if j == 0:
            ax[i][j].set_ylabel(r'$\dot{M}_1, \dot{M}_2$')
        else:
            ax[i][j].tick_params(labelleft=False)
        # right-axis (r) label only on right column
        if j == 1:
            twin_axes[i][j].set_ylabel(r'$r_1, r_2 \, [a]$')
        else:
            twin_axes[i][j].tick_params(labelright=False)
        # x-label only on bottom row
        if i == 2:
            ax[i][j].set_xlabel(r'Time $[\tau_b]$')

fig.savefig('proof_of_lambda_r_not_causal.pdf', bbox_inches='tight')
print("Wrote proof_of_lambda_r_not_causal.pdf")
