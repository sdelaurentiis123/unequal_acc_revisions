#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 14:40:43 2025

@author: stanislavdelaurentiis
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import scipy
from scipy import signal


def movingavg_bin_std(y,x,window):
    x=np.array(x)
    #has to be sorted
    xmedian=[]
    ymedian=[]
    ystd=[]
    index0=0
    endxval=window+x[0]
    index1=np.where(x>=window)[0][0]
    while 1==1:
        #print(index1,index0)
        ymedian.append(np.nanmean(y[index0:index1+1]))
        xmedian.append(np.nanmean(x[index0:index1+1]))
        ystd.append(np.nanstd(y[index0:index1+1]))
        #print(xmedian[-1], ymedian[-1])
        #print(x[index0:index1+1], y[index0:index1+1])
        #input('aua')
        #print((np.mean(y[index0:index1+1])))
        #print((np.std(y[index0:index1+1])))
        index0=index1
        endxval=endxval+window
        #print(endxval)
        try:
            index1=np.where(x>=(endxval))[0][0]
            #print('good')
        except IndexError:
            #print('fuck', endxval)
            xmedian=np.array(xmedian)[:-1]
            ymedian=np.array(ymedian)[:-1]
            ystd=np.array(ystd)[:-1]
            return(ymedian, ystd, xmedian)
    xmedian=np.array(xmedian)
    ymedian=np.array(ymedian)
    ystd=np.array(ystd)
    return(ymedian, ystd, xmedian)

def movingmedianval_bin(y,x,window):
    x=np.array(x)
    #has to be sorted
    xmedian=[]
    ymedian=[]
    index0=0
    endxval=window+x[0]
    index1=np.where(x>=window)[0][0]
    for i in range(int((x[-1]-x[0])/window)):
        #print(index1,index0)
        ymedian.append(np.nanmedian(y[index0:index1+1]))
        xmedian.append(np.nanmedian(x[index0:index1+1]))
        #print(xmedian[-1], ymedian[-1])
        #print(x[index0:index1+1], y[index0:index1+1])
        #input('aua')
        #print((np.median(y[index0:index1+1])))
        index0=index1
        endxval=endxval+window
        try:
            index1=np.where(x>=(endxval))[0][0]
        except IndexError:
            xmedian=np.array(xmedian)
            ymedian=np.array(ymedian)
            return(ymedian, xmedian)
    xmedian=np.array(xmedian)
    ymedian=np.array(ymedian)
    return(ymedian, xmedian)

def moving_mean_sigma_clip(x, y, window_size, n_iterations, sigma=2):
    """
    Perform moving mean with iterative sigma clipping.
    
    Parameters:
    x : array_like
        The x coordinates of the data points.
    y : array_like
        The y coordinates of the data points.
    window_size : float
        The size of the moving window in units of x.
    n_iterations : int
        Number of sigma clipping iterations.
    sigma : float, optional
        The sigma multiplier for clipping. Default is 2.
    
    Returns:
    x_filtered : ndarray
        The x coordinates of the filtered data points.
    y_filtered : ndarray
        The filtered y values.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    mask = np.ones(len(x), dtype=np.bool_)
    y_filtered = np.copy(y)
    
    for _ in range(n_iterations):
        for i in range(len(x)):
            if not mask[i]:
                continue
            # Find points within the window
            window_mask = np.abs(x - x[i]) <= window_size / 2
            window_mask = np.logical_and(window_mask, mask)
            window_y = y_filtered[window_mask]
            
            if len(window_y) > 0:
                # Calculate mean and standard deviation
                mean = np.mean(window_y)
                std = np.std(window_y)
                
                # Apply sigma clipping
                clip_mask = np.abs(window_y - mean) <= sigma * std
                if np.sum(clip_mask) > 0:
                    y_filtered[i] = np.mean(window_y[clip_mask])
                else:
                    y_filtered[i] = mean
            else:
                mask[i] = False
    
    return x[mask], y_filtered[mask]




def sliding_window_mass_summary(time, mass, window_size):
    """
    Computes the sum of mass and the average derivative (total_mass / window_size) 
    for a sliding window that shifts by the length of the window size.

    Parameters:
    - time: np.array of time values (sorted, increasing order).
    - mass: np.array of mass values (same size as time).
    - window_size: float, size of the sliding time window.

    Returns:
    - results: list of tuples (start_time, end_time, total_mass, avg_derivative, evaluated_time) for each window.
    """
    results = []
    time_outs=[]
    
    # Ensure inputs are numpy arrays for fast operations
    time = np.array(time)
    mass = np.array(mass)

    # Loop through the time array with a step equal to the window size
    start_index=0
    while time[start_index]<=time[-1]:
        end_time = time[start_index] + window_size
        
        # Find the end index for the current window
        end_index = np.searchsorted(time, end_time, side='right') - 1
        
        # Check if we have enough points in the current window
        if end_index >= start_index:
            print(f''' this is time start {time[start_index]} time end {time[end_index]} time end {end_time}''')
            # Calculate total mass
            total_mass = np.sum(mass[start_index:end_index + 1])
            
            # Average derivative defined as total mass divided by the window size
            avg_derivative = total_mass / window_size
            
            # Append results (start_time, end_time, total_mass, avg_derivative, evaluated_time)
            evaluated_time = (time[start_index] + time[end_index]) / 2  # Midpoint of the window
            
            print(f''' this is sum {total_mass} this is avg deriv {avg_derivative} this is ev time {evaluated_time}''')
            results.append(avg_derivative)
            time_outs.append(evaluated_time)

        # Move the start index to the end of the current window
        start_index = end_index
        
    results=np.array(results)
    time_outs=np.array(time_outs)
    return time_outs, results


import numpy as np

def sliding_window_mass_summary(time, mass, window_size):
    """
    Computes the sum of mass and the average derivative (total_mass / window_size) 
    for a sliding window that shifts by the length of the window size.

    Parameters:
    - time: np.array of time values (sorted, increasing order).
    - mass: np.array of mass values (same size as time).
    - window_size: float, size of the sliding time window.

    Returns:
    - time_outs: np.array of evaluated times (midpoints of each window).
    - results: np.array of average derivatives for each window.
    """
    results = []
    time_outs = []
    
    # Ensure inputs are numpy arrays for fast operations
    time = np.array(time)
    mass = np.array(mass)
    start_index = 0
    #end_time = time[start_index] + window_size
    #end_index = np.searchsorted(time, end_time, side='right') -1
    
    while start_index<len(time):
        end_time = time[start_index] + window_size
        # Find the end index for the current window
        end_index = np.searchsorted(time, end_time, side='right') -1
        
        # Check if we have valid window points
        if end_index >= start_index:
            #print(f''' this is time start {time[start_index]} time end {time[end_index-1]} time end {end_time}''')
            # Calculate total mass
            total_mass = np.sum(mass[start_index:end_index + 1])
            
            # Average derivative
            avg_derivative = total_mass / window_size
            
            # Append results with midpoint time
            evaluated_time = (time[start_index] + time[end_index]) / 2
            
            #print(f''' this is sum {total_mass} this is avg deriv {avg_derivative} this is ev time {evaluated_time}''')
            results.append(avg_derivative)
            time_outs.append(evaluated_time)
            
            # Move start index to the end of the current window
            start_index = end_index + 1
        else:
            break  # Exit if the window can't be formed

    # Convert results to numpy arrays for consistency
    time_outs = np.array(time_outs)
    results = np.array(results)
    return time_outs, results


def mdot_visc(beta, nu_0, Md_0, Rd_0, t, t_nu_0):
    """
    Calculate the viscous mass accretion rate according to the given equation.

    Parameters:
    - beta: Exponent parameter (dimensionless)
    - nu_0: Viscosity parameter (e.g., in cm^2/s)
    - Md_0: Initial disk mass (e.g., in solar masses or grams)
    - Rd_0: Initial disk radius (e.g., in cm)
    - t: Time at which to evaluate the accretion rate (e.g., in seconds)
    - t_nu_0: Initial viscous timescale (e.g., in seconds)

    Returns:
    - mdot: Viscous mass accretion rate (e.g., in solar masses per second or grams per second)
    """
    # Compute the first part of the equation
    pre_factor = (3 * (2 - beta) * nu_0) / 2
    mass_radius_ratio = Md_0 / (Rd_0 ** 2)

    # Compute the time-dependent part
    time_factor = (1 + t / t_nu_0) ** (-(5 + 2 * beta) / (4 - 2 * beta))

    # Final calculation
    mdot = pre_factor * mass_radius_ratio * time_factor
    return mdot


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



qdot_slope_matrix=np.ones((10,8))
qdot_intercept_matrix=np.ones((10,8))

lambda_med_matrix=np.zeros((10,8))
lambda_mean_matrix=np.zeros((10,8))


ecclist=[0.0,0.1, 0.2,0.3,0.4,0.5,0.6,0.8]
qblist=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]


fig, ax =plt.subplots(10,8, sharex=True, sharey=True,
                       gridspec_kw={'hspace': 0.0, 'wspace': 0.0})
figalt, axalt =plt.subplots(10,8, sharex=True, sharey=True,
                            gridspec_kw={'hspace': 0.0, 'wspace': 0.0})

time_start=6000
time_end=7000



import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# Function to compute Fourier Transform, detect peaks, and create/save a figure
def analyze_binary(t, signal, e_b, q_b, title, min_height=0.01, min_distance=10, n_peaks=5):
    """
    Perform Fourier Transform on the signal, detect peaks, and save the plot with peak annotations.
    
    Parameters:
    - t: Time array
    - signal: Signal array
    - e_b: Eccentricity of the binary
    - q_b: Mass ratio of the binary
    - title: Base title for saving the figure
    - min_height: Minimum height for peak detection in normalized power spectrum
    - min_distance: Minimum distance between peaks in FFT indices
    - n_peaks: Number of top peaks to extract
    
    Returns:
    - results: Dictionary with top frequencies, phases, and power
    """
    # Perform FFT
    fft_signal = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), (t[1] - t[0]))
    power_spectrum = np.abs(fft_signal) ** 2
    normalized_power_spectrum = power_spectrum / np.sum(power_spectrum)

    # Detect peaks
    peaks, properties = find_peaks(normalized_power_spectrum, height=min_height, distance=min_distance)
    peak_freqs = np.abs(freqs[peaks])
    peak_phases = np.angle(fft_signal[peaks])
    peak_power = power_spectrum[peaks]

    # Sort and take top N peaks
    sorted_indices = np.argsort(properties['peak_heights'])[::-1]
    top_peaks = sorted_indices[:n_peaks]

    top_freqs = peak_freqs[top_peaks]
    top_phases = peak_phases[top_peaks]
    top_power = peak_power[top_peaks]

    # Prepare results dictionary
    results = {
        'e_b': e_b,
        'q_b': q_b,
        'top_freqs': top_freqs,
        'top_phases': top_phases,
        'top_power': top_power,
    }

    # Plot normalized power spectrum
    plt.figure(figsize=(10, 6))
    plt.plot(freqs[:len(freqs)//2], normalized_power_spectrum[:len(freqs)//2], label="Normalized Power Spectrum")
    plt.scatter(top_freqs, normalized_power_spectrum[peaks[:n_peaks]], color='red', label="Detected Peaks", zorder=5)

    # Annotate peaks with frequency and phase
    for i, (freq, phase) in enumerate(zip(top_freqs, top_phases)):
        plt.annotate(
            f"f={freq:.2f}\nφ={phase:.2f}",
            xy=(freq, normalized_power_spectrum[peaks[i]]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=10,
            color="blue",
            rotation=45,
        )

    # Add labels, legend, and title
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized Power")
    plt.title(f"{title}: q={q_b}, e={e_b}")
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid()

    # Save the figure
    save_filename = f"power_spectrum_cavity/{title}_q_{q_b}_e_{e_b}.pdf"
    plt.savefig(save_filename, format='pdf')
    plt.close()

    return results


import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from statsmodels.nonparametric.smoothers_lowess import lowess
import matplotlib.pyplot as plt

def analyze_binary(t, signal, e_b, q_b, title, min_height=0.001, min_distance=20, n_peaks=5, frac=0.01, min_freq=1e-3):
    """
    Perform Fourier Transform on the signal, smooth the power spectrum with LOWESS,
    detect peaks, and save the plot with peak annotations.

    Parameters:
    - t: Time array
    - signal: Signal array
    - e_b: Eccentricity of the binary
    - q_b: Mass ratio of the binary
    - title: Base title for saving the figure
    - min_height: Minimum height for peak detection in smoothed normalized power spectrum
    - min_distance: Minimum distance between peaks in FFT indices
    - n_peaks: Number of top peaks to extract
    - frac: Fraction of data used in LOWESS smoothing (controls the smoothing window)

    Returns:
    - results: Dictionary with top frequencies, phases, and power
    """
    # Perform FFT
    fft_signal = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), (t[1] - t[0]))
    power_spectrum = np.abs(fft_signal) ** 2
    normalized_power_spectrum = power_spectrum / np.sum(power_spectrum)
    
    #mask = np.abs(freqs) >= min_freq

    # Smooth the normalized power spectrum with LOWESS
    smoothed_power_spectrum = lowess(
        normalized_power_spectrum, freqs, frac=frac, return_sorted=False
    )

    # Detect peaks in the smoothed spectrum
    peaks, properties = find_peaks(smoothed_power_spectrum, height=min_height, distance=min_distance)
    peak_freqs = np.abs(freqs[peaks])
    peak_phases = np.angle(fft_signal[peaks])
    peak_power = smoothed_power_spectrum[peaks]

    # Sort and take top N peaks
    sorted_indices = np.argsort(properties['peak_heights'])[::-1]
    top_peaks = sorted_indices[:n_peaks]

    top_freqs = peak_freqs[top_peaks]
    top_phases = peak_phases[top_peaks]
    top_power = peak_power[top_peaks]
    
    unique_indices = [np.where(np.round(1/top_freqs,0) == value)[0][0] for value in  np.unique(np.round(1/top_freqs, 0))]
    
    top_freqs=top_freqs[unique_indices]
    top_phases=top_phases[unique_indices]
    top_power=top_power[unique_indices]
    
    sorted_indices=np.argsort(top_power)
    
    
    
    top_freqs=top_freqs[sorted_indices]
    top_phases=top_phases[sorted_indices]
    top_power=top_power[sorted_indices]
    
    
    mask = top_freqs >= 1e-3

    # Apply the mask to top_freqs, top_phases, and top_power to keep only the relevant values
    top_freqs = top_freqs[mask]
    top_phases = top_phases[mask]
    top_power = top_power[mask]
        
    
    
    
    # Prepare results dictionary
    results = {
        'e_b': e_b,
        'q_b': q_b,
        'top_freqs': top_freqs,
        'top_phases': top_phases,
        'top_power': top_power,
    }

    # Plot smoothed normalized power spectrum
    plt.figure(figsize=(10, 6))
    plt.plot(freqs[:len(freqs)//2], normalized_power_spectrum[:len(freqs)//2], label="Original Normalized Power Spectrum", alpha=0.6)
    plt.plot(freqs[:len(freqs)//2], smoothed_power_spectrum[:len(freqs)//2], label="Smoothed Normalized Power Spectrum (LOWESS)", linewidth=2)
    plt.scatter(top_freqs, top_power, color='red', label="Detected Peaks", zorder=5)

    # Annotate peaks with frequency and phase
    for i, (freq, phase) in enumerate(zip(top_freqs, top_phases)):
        plt.annotate(
            f"f={freq:.2f}\nφ={phase:.2f}",
            xy=(freq, normalized_power_spectrum[peaks[i]]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=10,
            color="blue",
            rotation=45,
        )

    # Add labels, legend, and title
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized Power")
    plt.title(f"{title}: q={q_b}, e={e_b}")
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid()

    # Save the figure
    save_filename = f"power_spectrum_cavity/{title}_q_{q_b}_e_{e_b}.pdf"
    plt.savefig(save_filename, format='pdf')
    plt.close()

    return results




lambda_new_fft=[]
rmin0_sink_fft=[]
rmin1_sink_fft=[]
e1_fft=[]
a1_fft=[]


output_matrix=np.zeros((10,8))



time_start=7500
time_end=9500
import pickle
for i, qb in enumerate(qblist):
    for j, eb in enumerate(ecclist):
            ecc = eb
            ebind = j
            qbind = i
            pickle_file_path = f"/Users/stanislavdelaurentiis/roman_work/metrics_data_new/data_eb_{eb}_qb_{qb}"
            with open(pickle_file_path, 'rb') as f:
                cucumber_file = pickle.load(f)
            lambda_full=cucumber_file['mdot2'] / cucumber_file['mdot1']

           # df = cucumber_file
            ax[0][ebind].set_title('eb_'+str(ecc)+'_qb_'+str(qb))
            
            
            #would also be use doublechecking what the binary accretion looks like
            #if you assume mdot0 + mdot1 is
            # 10%eddington (at some time t, let's call it the end, could also be avg doesnt matter)
            # you effectively get a conversion from numerical to physical units
            # then you want to scale the numerical individual accretion rates to physial values
            # and then you want the eddington of that mass (in physical units)
            # thus you compare the numerical-->analytical and divide it by 
            # the eddington physical, see what it comes out to
           
            time = cucumber_file['time_mdot']
            mdot0_new = cucumber_file['mdot1']
            mdot1_new = cucumber_file['mdot2']
            
            
            #time = np.arange(10,10000 + 1, 10)

           
            
            
            def m_from_q(q):
                if q>1:
                    raise ValueError('q must be less than 1')
                m1=1/(1+q)
                m2=1-m1
                return(m1, m2)
            m0,m1=m_from_q(qb) #m0 is bigger
            
            msol=2e33
            
            num_phys_scale=(2*eddington(1e7*msol))/np.mean(mdot0_new+mdot1_new)
            mdot0_phys=mdot0_new*num_phys_scale
            mdot1_phys=mdot1_new*num_phys_scale
            mdot0_frac=mdot0_phys/eddington(m0*1e7*msol)
            mdot1_frac=mdot1_phys/eddington(m1*1e7*msol)
            
            
            indices=np.where((time>=time_start ) & (time<=time_end) )[0]
            
            
            #ax[9-qbind][ebind].plot(time[indices], lambda_new[indices], color='blue', alpha=0.5)
            #lambda_new_fft.append(analyze_binary(time1_new, lambda_new, ecclist[ebind], qblist[qbind], 'lambda'))
            
            
            #axalt[9-qbind][ebind].plot(time1_new[indices], mdot1_frac[indices], color='red', label='secondary', alpha=0.5)
            #axalt[9-qbind][ebind].plot(time0_new[indices], mdot0_frac[indices], color='black', label='primary', alpha=0.5)
            
            
            axalt[9-qbind][ebind].plot(time[indices], mdot1_frac[indices], color='red', label='secondary', alpha=0.5)
            axalt[9-qbind][ebind].plot(time[indices], mdot0_frac[indices], color='black', label='primary', alpha=0.5)
            if len(np.where(mdot1_frac[indices]>1)[0])>0:
                axalt[9-qbind][ebind].set_facecolor((0,0,1,0.3))#, alpha=0.3)
            if len(np.where(mdot1_frac[indices]>1)[0])>1 and len(np.where(mdot0_frac[indices]>1.1)[0])>50:
                axalt[9-qbind][ebind].set_facecolor((0,1,0,0.3))#, alpha=0.3)
                
            if len(np.where((mdot1_frac[indices]>1) &  (mdot0_frac[indices]>1.1))[0]) >50:
                if ebind==7 or ebind==4:
                    axalt[9-qbind][ebind].set_facecolor((0,1,0,0.3))#, alpha=0.3)
                else:
                    axalt[9-qbind][ebind].set_facecolor((0.5,0,0.5,0.3))#, alpha=0.3)
            #axalt[9-qbind][ebind].plot(time1_new, mdot1_frac, color='red', label='secondary', alpha=0.5)
            #axalt[9-qbind][ebind].plot(time0_new, mdot1_frac / mdot0_frac, color='blue', label='primary', alpha=0.5)
            
            #axalt[9-qbind][ebind].axhline(1, color='darkgray', ls='--', alpha=0.5)
            #fajdsflk
            output_matrix[9-qbind][ebind]=np.mean(np.maximum(mdot1_frac, mdot0_frac))/np.mean(np.minimum(mdot1_frac, mdot0_frac))
            #output_matrix2[9-qbind][ebind]=np.max(mdot1_frac/mdot0_frac)


axalt[3][1].set_facecolor((0.5,0,0.5,0.3))
#axalt[4][4].set_facecolor((0,1,0,0.3))
axalt[3][4].set_facecolor((0,0,1,0.3))
axalt[5][6].set_facecolor((0,1,0,0.3))
axalt[0][3].set_facecolor((0,1,0,0.3))

axalt[4][7].set_facecolor((0.5,0,0.5,0.3))
axalt[5][7].set_facecolor((0.5,0,0.5,0.3))

for axs in ax.flatten():
    axs.set_yscale('log')
    axs.set_ylim(1e-4, 1e4)
    axs.set_xlim(time_start,time_end)
    


for i in range(10):
    ax[9-i][0].set_ylabel(r'$\rm{q}_{\rm{b}}$: '+format(qblist[i],'.1f'))

    
 
for i in range(8):
    ax[9][i].set_xlabel(r'$\rm{e}_{\rm{b}}$: '+format(ecclist[i],'.1f'))
    
for axs in axalt.flatten():
    axs.set_yscale('log')
    axs.set_ylim(5e-2, 50)
    axs.set_xlim(time_start,time_end)
    #axs.set_xlim(0,1e4)
    axs.axhline(0.01, color='darkgray', ls='--')
    axs.axhline(1, color='darkgray', ls='--')
    


LABEL_FS_FIG8 = 16
TICK_FS_FIG8 = 11
for i in range(10):
    axalt[9-i][0].set_ylabel(r'$q_b$ = '+format(qblist[i],'.1f'),
                              fontsize=LABEL_FS_FIG8)

for i in range(8):
    axalt[9][i].set_xlabel(r'$e_b$ = '+format(ecclist[i],'.1f'),
                            fontsize=LABEL_FS_FIG8)

for axs in axalt.flatten():
    axs.tick_params(labelsize=TICK_FS_FIG8)

figalt.set_figheight(20)
figalt.set_figwidth(16)

figalt.savefig('mdot1_mdot2_1edd_both_truncated.pdf')


from mpl_toolkits.axes_grid1 import make_axes_locatable


fig, ax = plt.subplots(figsize=(6,6),)
im = ax.imshow(output_matrix, cmap='viridis')

# Create tick positions and labels for x-axis (qb from 1 to 0.1)
qb_values = np.arange(1, 0, -0.1)  # Creates array [1.0, 0.9, ..., 0.1]
ax.set_yticks(np.arange(len(qb_values)))
ax.set_yticklabels([f'{x:.1f}' for x in qb_values])

# Create tick positions and labels for y-axis (0 to 0.8, skip 0.7)
x_values = np.array([x/10 for x in range(0, 9) if x != 7])  # Creates [0, 0.1, ..., 0.6, 0.8]
ax.set_xticks(np.arange(len(x_values)))
ax.set_xticklabels([f'{x:.1f}' for x in x_values])

# Text color picked by luminance of the viridis cell so labels stay readable
# (yellow/teal high cells -> black text; dark purple/blue low cells -> white)
vmin, vmax = output_matrix.min(), output_matrix.max()
for i in range(len(qb_values)):
    for j in range(len(x_values)):
        v = output_matrix[i, j]
        norm = (v - vmin) / (vmax - vmin) if vmax > vmin else 0.0
        rgba = plt.cm.viridis(norm)
        lum = 0.299*rgba[0] + 0.587*rgba[1] + 0.114*rgba[2]
        ax.text(j, i, f'{v:.1f}',
                ha='center', va='center',
                color='black' if lum > 0.5 else 'white')

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = plt.colorbar(im, cax=cax)
cbar.set_label(r'$\tilde{\lambda} = \langle \max(\dot{M}_1, \dot{M}_2) \rangle / \langle \min(\dot{M}_1, \dot{M}_2) \rangle$')


# Add axis labels if desired
ax.set_ylabel(r'$q_b$')
ax.set_xlabel(r'$e_b$')


fig.tight_layout()
fig.savefig('lambda_edd_max_over_min_heatmap.pdf')
    
    
    
    
    
    

