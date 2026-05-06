#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:16:42 2025

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
fig, ax = plt.subplots(3,2,figsize=(6, 6))
colors = cm.nipy_spectral(np.linspace(0, 1, len(ecclist)+1))  # Choose a colormap




#e_b=0.5, q_b=0.8
#e_b=0.2, q_b=0.1
#e_b=0.6, q_b=0.6

sim_param_list = [(0.5,0.8), (0.8,1.0), (0.2,0.1), (0.8,0.3), (0.4,0.7), (0.5,0.7)]

i=0
j=0
start_time=5000
end_time=10000
for eb, qb in sim_param_list:#zip ([0.5, 0.6, 0.8, 0.4, 0.2,], [0.8, 1.0, 0.8, 0.7 ,0.1 ,]):
    print(eb, qb)


    pickle_file_path = f"/Users/stanislavdelaurentiis/roman_work/metrics_data/data_eb_{eb}_qb_{qb}"
    with open(pickle_file_path, 'rb') as f:
        cucumber_file = pickle.load(f)
    time=cucumber_file['time']
    lambda_full=cucumber_file['mdot2'] / cucumber_file['mdot1'] #this is now secondary over primary...
    rmin1= cucumber_file['rmin1'] #primary
    rmin2 = cucumber_file['rmin2'] # secondary
    indices=np.where((time>=start_time) & (time<=end_time))[0]
    #ax[i][j].plot(time[indices], lambda_full[indices], color='black', alpha=0.8)
    ax[i][j].plot(time[indices], cucumber_file['mdot2'][indices], color='green', alpha=0.8)
    ax[i][j].plot(time[indices], cucumber_file['mdot1'][indices], color='purple', alpha=0.8)
    ax[i][j].set_yscale('log')
    #ax[i][j].set_ylim(1/10,10)
    ax[i][j].set_title(rf'''$e_b$ = {eb}, $q_b$ = {qb}''')
    twinax= ax[i][j].twinx()
    twinax.plot(time[indices], rmin1[indices], color='blue', alpha=0.8)
    twinax.plot(time[indices], rmin2[indices], color='red', alpha=0.8)
    twinax.set_ylim(0,5.5)
    if j==0:
        ax[i][j].set_ylabel(r'$\lambda$')
    if j==1:
        twinax.set_ylabel(r'$r_1 \, , r_2 \, [a]$')
    if i==2:
        ax[i][j].set_xlabel(r'Time $[\tau]$')
    
    if i==2:
        j=1
        i=0
        continue
    i=i+1
    
fig.tight_layout()
fig.savefig('proof_of_lambda_r_not_causal.pdf')
    