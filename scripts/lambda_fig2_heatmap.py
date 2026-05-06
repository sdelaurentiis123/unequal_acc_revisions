#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 16:59:08 2025

@author: stanislavdelaurentiis
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle

# Define lists of qb and eb values
qblist = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ecclist = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]

# Initialize an empty 2D array to store lambda values
lambda_vals = np.zeros((len(qblist), len(ecclist)))

# Populate the lambda_vals array
for i, qb in enumerate(qblist):
    for j, eb in enumerate(ecclist):
        pickle_file_path = f"/Users/stanislavdelaurentiis/roman_work/metrics_data/data_eb_{eb}_qb_{qb}"
        with open(pickle_file_path, 'rb') as f:
            cucumber_file = pickle.load(f)
        lambda_full=cucumber_file['mdot2'] / cucumber_file['mdot1']
        lambd_tmp_medians=[]
        for idx in np.arange(0,105, 5):
            lambd_tmp_medians.append(np.median(lambda_full[250+idx:]))
        lambda_val = np.mean(lambd_tmp_medians)
        lambda_vals[i, j] = lambda_val

# Create a heatmap
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the heatmap
c = ax.imshow(
    lambda_vals,
    aspect="auto",
    origin="lower",
    cmap="magma",
    extent=[min(ecclist), max(ecclist), 0, max(qblist)],
    vmin=1,
    vmax=7
)



# Set ticks at the center of boxes
ecclist_mod = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
qblist_mod = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])-0.05
ax.set_xticks(np.array(ecclist_mod) + (ecclist_mod[1] - ecclist_mod[0]) / 2)


ax.set_yticks(qblist_mod)
ax.set_xticklabels(ecclist)
ax.set_yticklabels(qblist)

for i in range(len(qblist)):
    for j in range(len(ecclist)):
        ax.text(
            (np.array(ecclist_mod) + (ecclist_mod[1] - ecclist_mod[0]) / 2)[j], qblist_mod[i], f"{lambda_vals[i, j]:.2f}",
            ha="center", va="center", color="white" if lambda_vals[i, j]<4 else "black", fontsize=8
        )


# Add colorbar
cbar = plt.colorbar(c, ax=ax)
cbar.set_label(r"$\langle \lambda \rangle$", fontsize=12)

# Add labels and title
ax.set_xlabel(r"$e_b$", fontsize=12)
ax.set_ylabel(r"$q_b$", fontsize=12)


# Show the plot
plt.tight_layout()
plt.show()
fig.savefig('lambda_mean_colormap.pdf')



import numpy as np
import matplotlib.pyplot as plt
import pickle

# Define lists of qb and eb values
qblist = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
ecclist = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]

# Initialize an empty 2D array to store lambda values
lambda_stds = np.zeros((len(qblist), len(ecclist)))

# Populate the lambda_vals array
for i, qb in enumerate(qblist):
    for j, eb in enumerate(ecclist):
        pickle_file_path = f"/Users/stanislavdelaurentiis/roman_work/metrics_data/data_eb_{eb}_qb_{qb}"
        with open(pickle_file_path, 'rb') as f:
            cucumber_file = pickle.load(f)
        lambda_full=cucumber_file['mdot2'] / cucumber_file['mdot1']
        lambda_full=lambda_full[250:]
        
        lambda_stds[i, j] = np.max(lambda_full)-np.min(lambda_full)#/np.mean(lambda_full)
        lambda_stds[i, j] = np.std(lambda_full)

# Create a heatmap
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the heatmap
c = ax.imshow(
    lambda_stds,
    aspect="auto",
    origin="lower",
    cmap="magma",
    extent=[min(ecclist), max(ecclist), 0, max(qblist)],
)




# Add colorbar
cbar = plt.colorbar(c, ax=ax)
cbar.set_label(r"$\sigma_{\lambda}$", fontsize=12)



ax.set_xticks(np.array(ecclist_mod) + (ecclist_mod[1] - ecclist_mod[0]) / 2)
ax.set_yticks(qblist_mod)
ax.set_xticklabels(ecclist)
ax.set_yticklabels(qblist)

for i in range(len(qblist)):
    for j in range(len(ecclist)):
        ax.text(
            (np.array(ecclist_mod) + (ecclist_mod[1] - ecclist_mod[0]) / 2)[j], qblist_mod[i], f"{lambda_stds[i, j]:.2f}",
            ha="center", va="center", color="white" if lambda_stds[i, j] < 0.8*float(c.norm.vmax) else "black", fontsize=8
        )




# Add labels and title
ax.set_xlabel(r"$e_b$", fontsize=12)
ax.set_ylabel(r"$q_b$", fontsize=12)


# Show the plot
plt.tight_layout()
plt.show()
fig.savefig('lambda_std_colormap.pdf')