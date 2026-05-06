#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 16:16:00 2025

@author: stanislavdelaurentiis
"""



import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Initialize data
ecclist = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
qblist = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# Set up the figure and colormap
fig, ax = plt.subplots(figsize=(6, 4))
colors = cm.coolwarm(np.linspace(0, 1, len(ecclist)+1))  # Choose a colormap

# Loop through eccentricities (e_b) and calculate lambda_val for each q_b
for ebind, eb in enumerate(ecclist):
    lambda_vals = []  # Store lambda values for the current e_b
    lambda_stds = []  # Store lambda stds for the current e_b
    for qb in qblist:
        pickle_file_path = f"/Users/stanislavdelaurentiis/roman_work/metrics_data/data_eb_{eb}_qb_{qb}"
        with open(pickle_file_path, 'rb') as f:
            cucumber_file = pickle.load(f)
        lambda_full=cucumber_file['mdot2'] / cucumber_file['mdot1']
        lambd_tmp_medians=[]
        for idx in np.arange(0,105, 5):
            lambd_tmp_medians.append(np.median(lambda_full[250+idx:]))
        lambda_val = np.mean(lambd_tmp_medians)
        lambda_std = np.std(lambd_tmp_medians)/len(lambd_tmp_medians)
        #print()
        lambda_vals.append(lambda_val)
        lambda_stds.append(lambda_std)
        
    # Plot the line for the current e_b
    if eb==0.8:
        ax.plot(qblist, lambda_vals, color=colors[ebind+1], marker='*')
        ax.errorbar(qblist, lambda_vals, yerr=lambda_stds, color=colors[ebind+1], ls='none')
    else:
        ax.plot(qblist, lambda_vals, color=colors[ebind], marker='*')
        ax.errorbar(qblist, lambda_vals, yerr=lambda_stds, color=colors[ebind], ls='none')

# Add labels, legend, and colorbar
ax.set_xlabel(r"$q_b$", fontsize=14)
ax.set_ylabel(r"$\lambda$", fontsize=14)
ax.set_xscale('log')
ax.set_yscale('log')

magda_hypothesis = lambda x: x**(-0.9)

ax.plot(np.linspace(0.1, 1, 500), magda_hypothesis(np.linspace(0.1, 1, 500)), ls='--', color='darkgreen', alpha=1.0, label=r'$q_b^{-0.9}$')
ax.legend()

#plt.grid()

# Add a colorbar to represent e_b values
sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=plt.Normalize(vmin=min(ecclist), vmax=max(ecclist)))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label(r"$e_b$", fontsize=14)

# Show the plot
plt.tight_layout()
plt.show()
fig.savefig('magda_fig2.pdf')
