#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:11:59 2025

@author: stanislavdelaurentiis
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math


def eddington(M, epsilon=0.1):
    """
    Calculate the Eddington accretion rate for a black hole in CGS units.
    
    Parameters:
    M (float): Mass of the black hole in grams.
    epsilon (float): Radiative efficiency (default is 0.1).
    
    Returns:
    float: Eddington accretion rate in g/s.
    """
    # Constants in CGS units
    G = 6.67430e-8       # Gravitational constant in cm^3 g^-1 s^-2
    c = 3.0e10           # Speed of light in cm/s
    sigma_T = 6.6524e-25 # Thomson scattering cross-section in cm^2
    m_p = 1.6726e-24     # Proton mass in g
    
    # Eddington accretion rate formula
    M_dot_edd = (4 * math.pi * G * M * m_p) / (epsilon * sigma_T * c)
    
    return M_dot_edd

#f = open('qdot_data_magda.npy', 'rb')
data=np.load('/Users/stanislavdelaurentiis/roman_work/qdot_data_magda.npy')
#data=np.abs(data)
msol=1.99e33
m1 = 1e7*msol
m2 = 1e7*msol
mdot_m=1*(eddington(m1+m2)/(m1+m2))
data2=data*mdot_m

fig, ax = plt.subplots(figsize=(6,6),)

# Create the imshow plot
im = ax.imshow(data, cmap='magma',
               vmin=1e-3,
               vmax=1)

# Create tick positions and labels for x-axis (qb from 1 to 0.1)
qb_values = np.arange(1, 0, -0.1)  # Creates array [1.0, 0.9, ..., 0.1]
ax.set_yticks(np.arange(len(qb_values)))
ax.set_yticklabels([f'{x:.1f}' for x in qb_values])

# Create tick positions and labels for y-axis (0 to 0.8, skip 0.7)
x_values = np.array([x/10 for x in range(0, 9) if x != 7])  # Creates [0, 0.1, ..., 0.6, 0.8]
ax.set_xticks(np.arange(len(x_values)))
ax.set_xticklabels([f'{x:.1f}' for x in x_values])

# Add annotations for each cell
#log_data = np.log10(np.abs(data))
for i in range(len(qb_values)):
    for j in range(len(x_values)):
        text = ax.text(j, i, f'{data[i,j]:.3f}',
                      ha='center', va='center',
                      #color='white' if data[i,j] < -0.375 else 'black')
                      color='white' if data[i,j] < 0.45 else 'black')

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar= plt.colorbar(im, cax=cax)
# Add colorbar and label
#cbar = fig.colorbar(im, ax=ax)
cbar.set_label(r'$\langle \dot{q} \rangle$ [$\dot{M}_b / M_b$]')


# Add axis labels if desired
ax.set_ylabel(r'$q_b$')
ax.set_xlabel(r'$e_b$')
fig.tight_layout()
fig.savefig('qdot_heatmap_new.pdf')
asdf
fig, ax = plt.subplots(figsize=(6,6),)
# Create the imshow plot
im = ax.imshow(np.log10(np.abs(data2)), cmap='viridis',
               vmin=-16,
               vmax=-15)

# Create tick positions and labels for x-axis (qb from 1 to 0.1)
qb_values = np.arange(1, 0, -0.1)  # Creates array [1.0, 0.9, ..., 0.1]
ax.set_yticks(np.arange(len(qb_values)))
ax.set_yticklabels([f'{x:.1f}' for x in qb_values])

# Create tick positions and labels for y-axis (0 to 0.8, skip 0.7)
x_values = np.array([x/10 for x in range(0, 9) if x != 7])  # Creates [0, 0.1, ..., 0.6, 0.8]
ax.set_xticks(np.arange(len(x_values)))
ax.set_xticklabels([f'{x:.1f}' for x in x_values])

# Add annotations for each cell
log_data = np.log10(np.abs(data2))
for i in range(len(qb_values)):
    for j in range(len(x_values)):
        text = ax.text(j, i, f'{log_data[i,j]:.2f}',
                      ha='center', va='center',
                      color='white' if log_data[i,j] < -0.375 else 'black')

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar= plt.colorbar(im, cax=cax)
# Add colorbar and label
#cbar = fig.colorbar(im, ax=ax)
cbar.set_label(r'log($\langle \dot{q} \rangle$) [$$]')


# Add axis labels if desired
ax.set_ylabel(r'$q_b$')
ax.set_xlabel(r'$e_b$')


fig.tight_layout()
fig.savefig('qdot_heatmap_1e7_1edd.pdf')




#cgs units
c=2.99792458e10
G=6.67430e-8
#G=1
#c=1
msol=1e33
mpc=3.086e24


#
#d=zc/h0 h0=70.8 km/s/mpc
