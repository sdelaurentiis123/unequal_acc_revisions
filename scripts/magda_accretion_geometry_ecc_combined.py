#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:12:57 2024

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


fig, ax =plt.subplots(10,8)
figalt, axalt =plt.subplots(10,8)

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


for qbind in range(len(qblist)):
    for ebind in range(len(ecclist)):
        ecc=ecclist[ebind]
        qb=qblist[qbind]
        if qb!=qb:
            continue
        else:
            yo=np.loadtxt('/Users/stanislavdelaurentiis/roman_work/magda_accretion_files/accretion_eb_'+str(ecc)+'_qb_'+str(qb)+'.txt')
            print('loading....'+'eb_'+str(ecc)+'_qb_'+str(qb))
            df=pd.DataFrame(yo)
            del yo
            df.columns=['time',
            'sinkid0', 'sinkid1',
            'mass0', 'mass1',
            'mass_in0', 'mass_in1',
            'px_0', 'py_0', 'pz_0',
            'px_1', 'py_1', 'pz_1',
            'x_0', 'y_0', 'z_0',
            'x_1', 'y_1', 'z_1']

            
            ax[0][ebind].set_title('eb_'+str(ecc)+'_qb_'+str(qb))
            time=(df['time'].to_numpy()[1:])/(2*math.pi)
            mdot0=(df['mass_in0'].to_numpy()[1:])/np.diff(df['time'].to_numpy())
            mdot1=(df['mass_in1'].to_numpy()[1:])/np.diff(df['time'].to_numpy())
            
            #would also be use doublechecking what the binary accretion looks like
            #if you assume mdot0 + mdot1 is
            # 10%eddington (at some time t, let's call it the end, could also be avg doesnt matter)
            # you effectively get a conversion from numerical to physical units
            # then you want to scale the numerical individual accretion rates to physial values
            # and then you want the eddington of that mass (in physical units)
            # thus you compare the numerical-->analytical and divide it by 
            # the eddington physical, see what it comes out to
           
            time, uniqueindex=np.unique(time,return_index=True)
            
            
            mdot0=mdot0[uniqueindex]
            mdot1=mdot1[uniqueindex]
            
            mass_in0=df['mass_in0'].to_numpy()[1:][uniqueindex] 
            # ok so mass_in is just instantaneous mass in (proved), hence this calculation of mdot is good
            mass_in1=df['mass_in1'].to_numpy()[1:][uniqueindex]
            

            indices=np.where((time[1:]>=time_start ) & (time[1:]<=time_end) )[0]
            
            
            def m_from_q(q):
                if q>1:
                    raise ValueError('q must be less than 1')
                m1=1/(1+q)
                m2=1-m1
                return(m1, m2)
            m0,m1=m_from_q(qb) #m0 is bigger
            m0_time=m0+np.cumsum(mass_in0)
            m1_time=m1+np.cumsum(mass_in1)
           
            qdot=(m1_time/m0_time)*( (mdot1/m1_time) - (mdot0/m0_time) )
            
            q=m1_time/m0_time
            qdot_slope, qdot_intercept=np.polyfit(time, q, 1)
            qdot_slope_matrix[9-qbind][ebind]=qdot_slope
            qdot_intercept_matrix[9-qbind][ebind]=qdot_intercept
            
            time0_new, mdot0_new = sliding_window_mass_summary(time, mass_in0, 10)
            time1_new, mdot1_new = sliding_window_mass_summary(time, mass_in1, 10)
            lambda_new=mdot0_new/mdot1_new
            
            msol=2e33
            
            num_phys_scale=(0.8*eddington(1e7*msol))/np.mean(mdot0_new+mdot1_new)
            mdot0_phys=mdot0_new*num_phys_scale
            mdot1_phys=mdot1_new*num_phys_scale
            mdot0_frac=mdot0_phys/eddington(m0*1e7*msol)
            mdot1_frac=mdot1_phys/eddington(m1*1e7*msol)
            
            
            indices=np.where((time0_new>=time_start ) & (time0_new<=time_end) )[0]
            
            
            ax[9-qbind][ebind].plot(time1_new[indices], lambda_new[indices], color='blue', alpha=0.5)
            lambda_new_fft.append(analyze_binary(time1_new, lambda_new, ecclist[ebind], qblist[qbind], 'lambda'))
            
            
            #axalt[9-qbind][ebind].plot(time1_new[indices], mdot1_frac[indices], color='red', label='secondary', alpha=0.5)
            #axalt[9-qbind][ebind].plot(time0_new[indices], mdot0_frac[indices], color='black', label='primary', alpha=0.5)
            
            
            axalt[9-qbind][ebind].plot(time1_new, mdot1_frac, color='red', label='secondary', alpha=0.5)
            axalt[9-qbind][ebind].plot(time0_new, mdot0_frac, color='black', label='primary', alpha=0.5)
            #axalt[9-qbind][ebind].plot(time1_new, mdot1_frac, color='red', label='secondary', alpha=0.5)
            #axalt[9-qbind][ebind].plot(time0_new, mdot1_frac / mdot0_frac, color='blue', label='primary', alpha=0.5)
            
            axalt[9-qbind][ebind].axhline(1, color='darkgray', ls='--', alpha=0.5)
            #fajdsflk
     
asfdd
 
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
    axs.set_ylim(1e-2, 1e2)
    #axs.set_xlim(time_start,time_end)
    axs.set_xlim(0,1e4)
    axs.axhline(0.03, color='darkgray', ls='--')
    axs.axhline(1, color='darkgray', ls='--')
    


for i in range(10):
    axalt[9-i][0].set_ylabel(r'$\rm{q}_{\rm{b}}$: '+format(qblist[i],'.1f'))

    
 
for i in range(8):
    axalt[9][i].set_xlabel(r'$\rm{e}_{\rm{b}}$: '+format(ecclist[i],'.1f'))

figalt.set_figheight(20)
figalt.set_figwidth(21)             
figalt.tight_layout()

figalt.savefig('mdot1_mdot2_0.08edd_full_both.pdf')
nljkl



#fig.savefig('rmin0_rmin1_time_new.pdf')


import pickle
import matplotlib.pyplot as plt
import math
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib



#fig2, ax2=plt.subplots(10,8)
#figalt2, axalt2=plt.subplots(10,8)


exmeanlist_1=[]
eymeanlist_1=[]
e1_r_meanlist=[]

exmeanlist_2=[]
eymeanlist_2=[]
e2_r_meanlist=[]


alist_1=[]

emeanlist_1=[]
emeanlist_2=[]

efitmeanlist=[]
curlypifitmeanlist=[]

curlypimeanlist_1=[]
curlypimeanlist_2=[]

rm_meanlist_1=[]
rm_meanlist_2=[]

alist_2=[]
ecclist=[0.0,0.1, 0.2,0.3,0.4,0.5,0.6,0.8]
qblist=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]




for qbind in range(len(qblist)):
    for ebind in range(len(ecclist)):
        #all the sim snapshot data is when the binary is at apocenter....
        picklefile = open('/Users/stanislavdelaurentiis/roman_work/magda_new_cavity_data/'+'qb_'+str(qblist[qbind])+'_e_'+str(ecclist[ebind])+'_ellipses_0.3meanmaxsig_1_1000', 'rb')  
        data = pickle.load(picklefile)
        ecc_fit=np.array(data['e1'])
        curlypi_fit=np.array(data['theta1'])
        
        e_fit_mean=np.mean(ecc_fit[100:])
        curlypi_fit_mean=np.mean(curlypi_fit[100:])
        efitmeanlist.append(e_fit_mean)
        curlypifitmeanlist.append(curlypi_fit_mean)
        qb=qblist[qbind]
        eb=ecclist[ebind]
        if qb!=qb:
            continue
        
        picklefile = open('/Users/stanislavdelaurentiis/roman_work/magda_new_cavity_data/qb_'+str(qblist[qbind])+'_e_'+str(ecclist[ebind])+'_fourier_0.3meanmaxsig_1_1000', 'rb')  
        data = pickle.load(picklefile)
        
        
        N=np.array(data['N'])
        
        rm0=np.array(data['r0'])
        am0=np.array(data['a0'])
        
        rm1=np.array(data['r1'])
        rm2=np.array(data['r2'])
        am1=np.array(data['a1'])
        am2=np.array(data['a2'])
        time=np.array(data['filename1']).astype('float')
        time=time*10
        
        rm3=np.array(data['r3'])
        am3=np.array(data['a3'])
        
        rm4=np.array(data['r4'])
        am4=np.array(data['a4'])
        
        rm5=np.array(data['r5'])
        am5=np.array(data['a5'])
        
        rm6=np.array(data['r6'])
        am6=np.array(data['a6'])
        
        rm7=np.array(data['r7'])
        am7=np.array(data['a7'])
        
        rm8=np.array(data['r8'])
        am8=np.array(data['a8'])
        
        rm9=np.array(data['r9'])
        am9=np.array(data['a9'])
        
        rm10=np.array(data['r10'])
        am10=np.array(data['a10'])
        
        #but we need to solve a rootfinder.....
        #look back to old zoltan equations see how we did this....
        def ellipse_func(theta):
            #have to make sure that time and theta are spanning different dimensions so that we can get time
            rvals=(   rm0/N + (rm1/N)*np.cos((1*theta)-am1) + (rm2/N)*np.cos((2*theta)-am2)
             +(rm3/N)*np.cos(3*theta-am3) + (rm4/N)*np.cos(4*theta-am4)
             + (rm5/N)*np.cos(5*theta-am5) + (rm6/N)*np.cos(6*theta-am6)
             + (rm7/N)*np.cos(7*theta-am7) + (rm8/N)*np.cos(8*theta-am8)
             + (rm9/N)*np.cos(9*theta-am9) + (rm10/N)*np.cos(10*theta-am10)
            )
            xvals=rvals*np.cos(theta)
            yvals=rvals*np.sin(theta)
            return(xvals, yvals)
        def ellipse_func2(theta, 
                          rm0init, rm1init, 
                          rm2init, rm3init, 
                          rm4init, rm5init, 
                          rm6init, rm7init,
                          rm8init, rm9init, 
                          rm10init,
                          Ninit, 
                          am1init, am2init,
                          am3init, am4init,
                          am5init, am6init,
                          am7init, am8init,
                          am9init, am10init):
            #have to make sure that time and theta are spanning different dimensions so that we can get time
            rvals=(   rm0init/Ninit + (rm1init/Ninit)*np.cos((1*theta)-am1init) + (rm2init/Ninit)*np.cos((2*theta)-am2init)
             +(rm3init/Ninit)*np.cos(3*theta-am3init) + (rm4init/Ninit)*np.cos(4*theta-am4init)
             + (rm5init/Ninit)*np.cos(5*theta-am5init) + (rm6init/Ninit)*np.cos(6*theta-am6init)
             + (rm7init/Ninit)*np.cos(7*theta-am7init) + (rm8init/Ninit)*np.cos(8*theta-am8init)
             + (rm9init/Ninit)*np.cos(9*theta-am9init) + (rm10init/Ninit)*np.cos(10*theta-am10init)
            )
            
            return(rvals)
        
        
        def pos_from_q_e(q,e):#from barycentric coords
            x_0=-1*(1 - (1/(1+q)))*(1+e)
            x_1=(1/(1+q))*(1+e)
           
            y_0=0
            y_1=0
            return([x_0, y_0, x_1, y_1])
        def m_from_q(q):
            if q>1:
                raise ValueError('q must be less than 1')
            m1=1/(1+q)
            m2=1-m1
            return(m1, m2)
        def hill_radii(m0, m1, r01):
            rhill0=r01*np.sqrt(m0/(3*(m0+m1)))
            rhill1=r01*np.sqrt(m1/(3*(m0+m1)))
            return(rhill0, rhill1)
        def circle(r,x0, y0):
            theta=np.arange(-1*math.pi, math.pi, 0.01)
            return([r*np.cos(theta) +x0, r*np.sin(theta) + y0])
        def circle2(r,x0, y0, phi):
            rout=np.sqrt((r*np.sin(phi)+x0)**2 + (r*np.cos(phi)+y0)**2)
            return(rout)
            
        
        rmin0_sink_list=[]
        rmin1_sink_list=[]
        
        x_0, y_0, x_1, y_1=pos_from_q_e(qblist[qbind], ecclist[ebind])
        #print(x_0, x_1, np.abs(x_0-x_1))
        m0, m1=m_from_q(qblist[qbind])
        
        rhill0, rhill1=hill_radii(m0, m1, np.abs(x_1-x_0))
        
        theta=np.arange(-1*math.pi, 1*math.pi, 0.001)
        theta=np.reshape(theta, (len(theta),1))
        x_ellipse, y_ellipse=ellipse_func(theta)
        
        
        r_ellipse_sink0=((x_0-x_ellipse)**2 + (y_0-y_ellipse)**2)
        r_ellipse_sink1=((x_1-x_ellipse)**2 + (y_1-y_ellipse)**2)
        
        print(f'''m0 is {m0}; rhill0 is {rhill0}; m1 is {m1}; rhill1 is {rhill1}''')
        
        rmin0_sink=np.min(r_ellipse_sink0, axis=0)-rhill0
        rmin1_sink=np.min(r_ellipse_sink1, axis=0)-rhill1
        
        
        indices=np.where((time>=time_start ) & (time<=time_end) )[0]
        axtmp=ax[9-qbind][ebind].twinx()
        axtmp.plot(time[indices], rmin0_sink[indices], color='black')
        axtmp.plot(time[indices], rmin1_sink[indices], color='red')
        
        axtmp2=axalt[9-qbind][ebind].twinx()
        axtmp2.plot(time[indices], rmin0_sink[indices], color='black', ls='--')
        axtmp2.plot(time[indices], rmin1_sink[indices], color='red', ls='--')
        
        rmin0_sink_fft.append(analyze_binary(time, rmin0_sink, ecclist[ebind], qblist[qbind], 'rmin0'))
        rmin1_sink_fft.append(analyze_binary(time, rmin1_sink, ecclist[ebind], qblist[qbind], 'rmin1'))
        
        
        axtmp.set_xlim(time_start, time_end)
        axtmp2.set_xlim(time_start, time_end)
        
        axtmp.set_yscale('linear')
        axtmp.set_ylim(0,6)
        axtmp2.set_yscale('linear')
        axtmp2.set_ylim(0,6)
        #afsjlk
        continue
        print('we messed up here...')

    
for axs in ax.flatten():
    pass
    #axs.set_ylim(0.2,2)
    #axs.axhline(1, color='black', ls='--', alpha=0.5)
    #axs.set_xlim(0,10000)
    #axs.set_yscale('linear')
    #axs.set_yscale('log')
    #axs.set_ylim(-0.1, 2.5)
    #axs.set_ylim(1e-1, 2.5)
    


##
exmeanlist_1=[]
eymeanlist_1=[]
e1_r_meanlist=[]

exmeanlist_2=[]
eymeanlist_2=[]
e2_r_meanlist=[]


alist_1=[]

emeanlist_1=[]
emeanlist_2=[]

efitmeanlist=[]
curlypifitmeanlist=[]

curlypimeanlist_1=[]
curlypimeanlist_2=[]

rm_meanlist_1=[]
rm_meanlist_2=[]

alist_2=[]
ecclist=[0.0,0.1, 0.2,0.3,0.4,0.5,0.6,0.8]
qblist=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
#fig, ax =plt.subplots(10,8)
for qbind in range(len(qblist)):
    for ebind in range(len(ecclist)):
        try:
          picklefile = open('/Users/stanislavdelaurentiis/roman_work/'+'qb_'+str(qblist[qbind])+'_e_'+str(ecclist[ebind])+'_ellipses_0.3meanmaxsig_1_1000', 'rb')  
          data = pickle.load(picklefile)
          ecc_fit=np.array(data['e1'])
          curlypi_fit=np.array(data['theta1'])
          
          e_fit_mean=np.mean(ecc_fit[100:])
          curlypi_fit_mean=np.mean(curlypi_fit[100:])
          efitmeanlist.append(e_fit_mean)
          curlypifitmeanlist.append(curlypi_fit_mean)
          
        except FileNotFoundError:
          continue
        
        
        picklefile = open('/Users/stanislavdelaurentiis/roman_work/qb_'+str(qblist[qbind])+'_e_'+str(ecclist[ebind])+'_fourier_0.3meanmaxsig_1_1000', 'rb')  
        data = pickle.load(picklefile)
        
        N=np.array(data['N'])
        
        rm0=np.array(data['r0'])
        am0=np.array(data['a0'])
        
        rm1=np.array(data['r1'])
        rm2=np.array(data['r2'])
        am1=np.array(data['a1'])
        am2=np.array(data['a2'])
        time=np.array(data['filename1']).astype('float')
        
        
        rm3=np.array(data['r3'])
        am3=np.array(data['a3'])
        
        rm4=np.array(data['r4'])
        am4=np.array(data['a4'])
        
        rm5=np.array(data['r5'])
        am5=np.array(data['a5'])
        
        rm6=np.array(data['r6'])
        am6=np.array(data['a6'])
        
        rm7=np.array(data['r7'])
        am7=np.array(data['a7'])
        
        rm8=np.array(data['r8'])
        am8=np.array(data['a8'])
        
        rm9=np.array(data['r9'])
        am9=np.array(data['a9'])
        
        rm10=np.array(data['r10'])
        am10=np.array(data['a10'])
        
    

        
        #this is for m=1
        amplitude=(rm1/N)
        baseline=rm0/N
        
        rmin=baseline-amplitude
        rmax=baseline+amplitude
        a=0.5*(rmin+rmax)
        alist_1.append(np.mean(a[100:]))
        e_1=1-(rmin/a)
        ex_1=e_1*np.cos(am1)
        ey_1=e_1*np.sin(am1)
        
        e_1=e_1.flatten()
        ex_1=ex_1.flatten()
        ey_1=ey_1.flatten()
        
        a_1=a
        
        #this is for m=2
        amplitude=(rm2/N)
        baseline=rm0/N
        rmax=baseline+amplitude
        rmin=baseline-amplitude
        a=rmax
        b=rmin
        alist_2.append(np.mean(a[100:]))
        e_2=np.sqrt(1-b**2/a**2)
        ex_2=e_2*np.cos(am2).flatten()
        ey_2=e_2*np.sin(am2).flatten()
        
        e_2=e_2.flatten()
        ex_2=ex_2.flatten()
        ey_2=ey_2.flatten()
        
        time=time*10
        inidces_of_interest=np.where((time>=6000) & (time<=7000))
        
        
        #if np.mean(rm1[100:])>=1.1*np.mean(rm2[100:]):
        axtmp_new=ax[9-qbind][ebind].twinx()
        
        
        axtmp_new.plot(time[inidces_of_interest], e_1[inidces_of_interest], color='green', zorder=float('inf'), alpha=0.5)
        
        
        
        axtmp_newnew=ax[9-qbind][ebind].twinx()
        axtmp_newnew.plot(time[inidces_of_interest], a_1[inidces_of_interest], color='purple', zorder=float('inf'), alpha=0.5)
        
        
        e1_fft.append(analyze_binary(time, e_1, ecclist[ebind], qblist[qbind], 'e1'))
        a1_fft.append(analyze_binary(time, a_1, ecclist[ebind], qblist[qbind], 'a1'))
        
        
##






fig.set_figheight(20)
fig.set_figwidth(21)             
fig.tight_layout()

fig.savefig(f'''combined_rmin_hill_ecc_a_lambda_lores_{time_start}_{time_end}.pdf''')






#n_peaks=5
e1_df=pd.DataFrame(e1_fft)
# =============================================================================
# e1_df_freqs = pd.DataFrame(e1_df['top_freqs'].to_list(), columns=[f'freq_{i+1}' for i in range(n_peaks)])
# e1_df_phases = pd.DataFrame(e1_df['top_phases'].to_list(), columns=[f'phase_{i+1}' for i in range(n_peaks)])
# # Merge the frequency and phase DataFrames with the original DataFrame
# e1_df = pd.concat([e1_df[['e_b', 'q_b']], e1_df_freqs, e1_df_phases], axis=1)
# 
# =============================================================================


a1_df=pd.DataFrame(a1_fft)
# =============================================================================
# a1_df_freqs = pd.DataFrame(a1_df['top_freqs'].to_list(), columns=[f'freq_{i+1}' for i in range(n_peaks)])
# a1_df_phases = pd.DataFrame(a1_df['top_phases'].to_list(), columns=[f'phase_{i+1}' for i in range(n_peaks)])
# 
# # Merge the frequency and phase DataFrames with the original DataFrame
# a1_df = pd.concat([a1_df[['e_b', 'q_b']], a1_df_freqs, a1_df_phases], axis=1)
# 
# 
# =============================================================================

rmin0_sink_df=pd.DataFrame(rmin0_sink_fft)
# =============================================================================
# rmin0_sink_df_freqs = pd.DataFrame(rmin0_sink_df['top_freqs'].to_list(), columns=[f'freq_{i+1}' for i in range(n_peaks)])
# rmin0_df_phases = pd.DataFrame(rmin0_df['top_phases'].to_list(), columns=[f'phase_{i+1}' for i in range(n_peaks)])
# 
# # Merge the frequency and phase DataFrames with the original DataFrame
# rmin0_df = pd.concat([rmin0_df[['e_b', 'q_b']], rmin0_df_freqs, rmin0_df_phases], axis=1)
# =============================================================================



rmin1_sink_df=pd.DataFrame(rmin1_sink_fft)
# =============================================================================
# df_freqs = pd.DataFrame(df['top_freqs'].to_list(), columns=[f'freq_{i+1}' for i in range(n_peaks)])
# df_phases = pd.DataFrame(df['top_phases'].to_list(), columns=[f'phase_{i+1}' for i in range(n_peaks)])
# 
# # Merge the frequency and phase DataFrames with the original DataFrame
# df = pd.concat([df[['e_b', 'q_b']], df_freqs, df_phases], axis=1)
# 
# 
# =============================================================================

lambda_new_df=pd.DataFrame(lambda_new_fft)
# =============================================================================
# df_freqs = pd.DataFrame(df['top_freqs'].to_list(), columns=[f'freq_{i+1}' for i in range(n_peaks)])
# df_phases = pd.DataFrame(df['top_phases'].to_list(), columns=[f'phase_{i+1}' for i in range(n_peaks)])
# 
# # Merge the frequency and phase DataFrames with the original DataFrame
# df = pd.concat([df[['e_b', 'q_b']], df_freqs, df_phases], axis=1)
# =============================================================================




#


figalt.set_figheight(20)
figalt.set_figwidth(21)             
figalt.tight_layout()

figalt.savefig('combined_rmin_mdot.pdf')
#fig.savefig('rmin0_rmin1_time_new.pdf')

        

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plotterr(df, n_peaks=3, save_prefix="plot"):
    """
    Plots 2D heatmaps of frequencies and phases in q and e space from a DataFrame 
    where frequency and phase data are stored as lists.

    Parameters:
    - df: DataFrame containing `q_b`, `e_b`, and lists of frequencies, phases, and power.
    - n_peaks: Number of top peaks to plot.
    - save_prefix: Prefix for saving the plots.

    Returns:
    - None (saves the plots).
    """
    # Initialize lists to store exploded data
    exploded_data = []

    # Explode the lists of top_freqs, top_phases, and top_power into individual rows
    for _, row in df.iterrows():
        for i in range(min(len(row['top_freqs']), n_peaks)):
            exploded_data.append({
                'e_b': row['e_b'],
                'q_b': row['q_b'],
                'freq': np.flip(row['top_freqs'])[i],
                'phase': np.flip(row['top_phases'])[i],
                'power': np.flip(row['top_power'])[i]
            })

    # Create an exploded DataFrame
    exploded_df = pd.DataFrame(exploded_data)

    # Loop through the number of peaks
    for i in range(1, n_peaks + 1):
        # Filter for the current peak
        peak_df = exploded_df.groupby(['e_b', 'q_b']).nth(i - 1).reset_index()

        # Pivot data for heatmap plotting
        freq_pivot = peak_df.pivot(index="q_b", columns="e_b", values="freq")
        phase_pivot = peak_df.pivot(index="q_b", columns="e_b", values="phase")
        
        freq_pivot = freq_pivot.sort_index(ascending=False)
        phase_pivot = phase_pivot.sort_index(ascending=False)

        # Frequency heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(1/freq_pivot, cmap="viridis", annot=True, fmt=".2f", cbar_kws={'label': 'Frequency (Hz)'}, ax=ax)
        ax.set_title(f"Top-{i} Frequency in q-e Space")
        ax.set_xlabel("e Eccentricity")
        ax.set_ylabel("q (Mass ratio)")
        plt.tight_layout()
        plt.savefig(f"{save_prefix}_freq_{i}.pdf")
        plt.close()

        # Phase heatmap
        fig, ax=plt.subplots()
        sns.heatmap(phase_pivot, cmap="coolwarm", annot=True, fmt=".2f", cbar_kws={'label': 'Phase (radians)'})
        ax.set_title(f"Top-{i} Phase in q-e Space")
        ax.set_xlabel("e Eccentricity")
        ax.set_ylabel("q (Mass ratio)")
        fig.tight_layout()
        fig.savefig(f"{save_prefix}_phase_{i}.pdf")
        plt.close()

    print(f"Plots saved with prefix: {save_prefix}")
    
def plotterr(df, n_peaks=3, save_prefix="plot"):
    """
    Plots 2D heatmaps of frequencies and phases in q and e space from a DataFrame 
    where frequency and phase data are stored as lists.

    Parameters:
    - df: DataFrame containing `q_b`, `e_b`, and lists of frequencies, phases, and power.
    - n_peaks: Number of top peaks to plot.
    - save_prefix: Prefix for saving the plots.

    Returns:
    - None (saves the plots).
    """
    # Initialize lists to store exploded data
    exploded_data = []

    # Explode the lists of top_freqs, top_phases, and top_power into individual rows
    for _, row in df.iterrows():
        for i in range(min(len(row['top_freqs']), n_peaks)):
            exploded_data.append({
                'e_b': row['e_b'],
                'q_b': row['q_b'],
                'freq': np.flip(row['top_freqs'])[i],
                'phase': np.flip(row['top_phases'])[i],
                'power': np.flip(row['top_power'])[i]
            })

    # Create an exploded DataFrame
    exploded_df = pd.DataFrame(exploded_data)

    # List of q and e values as per the user's request
    q_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # 10 unique q values
    e_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]  # 8 unique e values

    # Create a complete grid of q and e values
    complete_index = pd.MultiIndex.from_product([q_values, e_values], names=['q_b', 'e_b'])

    # Loop through the number of peaks
    for i in range(1, n_peaks + 1):
        # Filter for the current peak
        peak_df = exploded_df.groupby(['e_b', 'q_b']).nth(i - 1).reset_index()

        # Pivot data for heatmap plotting (swap e_b and q_b for desired orientation)
        freq_pivot = peak_df.pivot(index="q_b", columns="e_b", values="freq")  # q on y-axis, e on x-axis
        phase_pivot = peak_df.pivot(index="q_b", columns="e_b", values="phase")  # q on y-axis, e on x-axis

        # Reindex to include all q and e combinations, filling missing values with NaN
        freq_pivot = freq_pivot.reindex(q_values[::-1], axis=0, fill_value=np.nan)  # Highest q at the top (reverse q_values)
        freq_pivot = freq_pivot.reindex(e_values, axis=1, fill_value=np.nan)  # Ensure e on x-axis
        phase_pivot = phase_pivot.reindex(q_values[::-1], axis=0, fill_value=np.nan)  # Highest q at the top
        phase_pivot = phase_pivot.reindex(e_values, axis=1, fill_value=np.nan)

        
        

        # Frequency heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(1/freq_pivot, cmap="viridis", annot=True, fmt=".2f", cbar_kws={'label': 'Frequency (Hz)'}, ax=ax)
        ax.set_title(f"Top-{i} Frequency in q-e Space")
        ax.set_ylabel("q (Mass Ratio)")  # q on the y-axis
        ax.set_xlabel("e (Eccentricity)")  # e on the x-axis
        plt.tight_layout()
        plt.savefig(f"{save_prefix}_freq_{i}.pdf")
        plt.close()

        # Phase heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(phase_pivot, cmap="coolwarm", annot=True, fmt=".2f", cbar_kws={'label': 'Phase (radians)'}, ax=ax)
        ax.set_title(f"Top-{i} Phase in q-e Space")
        ax.set_ylabel("q (Mass Ratio)")  # q on the y-axis
        ax.set_xlabel("e (Eccentricity)")  # e on the x-axis
        fig.tight_layout()
        fig.savefig(f"{save_prefix}_phase_{i}.pdf")
        plt.close()

    print(f"Plots saved with prefix: {save_prefix}")
    


plotterr(lambda_new_df, save_prefix='lambda')
plotterr(rmin1_sink_df, save_prefix='rmin1_sink')
plotterr(rmin0_sink_df, save_prefix='rmin0_sink')

plotterr(e1_df, save_prefix='e1')

def table_maker(df, n_peaks=3, save_prefix="plot"):
    """
    Plots 2D heatmaps of frequencies and phases in q and e space from a DataFrame 
    where frequency and phase data are stored as lists.

    Parameters:
    - df: DataFrame containing `q_b`, `e_b`, and lists of frequencies, phases, and power.
    - n_peaks: Number of top peaks to plot.
    - save_prefix: Prefix for saving the plots.

    Returns:
    - None (saves the plots).
    """
    # Initialize lists to store exploded data
    exploded_data = []

    # Explode the lists of top_freqs, top_phases, and top_power into individual rows
    for _, row in df.iterrows():
        for i in range(min(len(row['top_freqs']), n_peaks)):
            exploded_data.append({
                'e_b': row['e_b'],
                'q_b': row['q_b'],
                'freq': np.flip(row['top_freqs'])[i],
                'phase': np.flip(row['top_phases'])[i],
                'power': np.flip(row['top_power'])[i]
            })

    # Create an exploded DataFrame
    exploded_df = pd.DataFrame(exploded_data)

    # List of q and e values as per the user's request
    q_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # 10 unique q values
    e_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]  # 8 unique e values

    # Create a complete grid of q and e values
    complete_index = pd.MultiIndex.from_product([q_values, e_values], names=['q_b', 'e_b'])

    # Loop through the number of peaks
    i=1
    if 1==1:
        # Filter for the current peak
        peak_df = exploded_df.groupby(['e_b', 'q_b']).nth(i - 1).reset_index()

        # Pivot data for heatmap plotting (swap e_b and q_b for desired orientation)
        freq_pivot = peak_df.pivot(index="q_b", columns="e_b", values="freq")  # q on y-axis, e on x-axis
        phase_pivot = peak_df.pivot(index="q_b", columns="e_b", values="phase")  # q on y-axis, e on x-axis

        # Reindex to include all q and e combinations, filling missing values with NaN
        freq_pivot = freq_pivot.reindex(q_values[::-1], axis=0, fill_value=np.nan)  # Highest q at the top (reverse q_values)
        freq_pivot = freq_pivot.reindex(e_values, axis=1, fill_value=np.nan)  # Ensure e on x-axis
        phase_pivot = phase_pivot.reindex(q_values[::-1], axis=0, fill_value=np.nan)  # Highest q at the top
        phase_pivot = phase_pivot.reindex(e_values, axis=1, fill_value=np.nan)

        
    return(1/freq_pivot, phase_pivot)


lambda_tau, lambda_phase = table_maker(lambda_new_df)
rmin1_tau, rmin1_phase = table_maker(rmin1_sink_df)
rmin0_tau, rmin0_phase = table_maker(rmin0_sink_df)
e1_tau, e1_phase = table_maker(e1_df)




import numpy as np
import matplotlib.pyplot as plt

# Compute the heatmap data
new_map = np.where(
    np.isnan(lambda_tau.to_numpy() / rmin1_tau.to_numpy()), 
    lambda_tau.to_numpy() / rmin0_tau.to_numpy(), 
    lambda_tau.to_numpy() / rmin1_tau.to_numpy()
)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 10))

# Plot the heatmap using imshow
c = ax.imshow(new_map, cmap="magma", vmin=0.3, vmax=3, aspect="auto")

# Add colorbar
cbar = fig.colorbar(c, ax=ax)
cbar.set_label(r'$\tau_{\lambda} / \tau_{r_{1}}$')

# Set axis labels and ticks
ax.set_ylabel(r"$q_b$")  # q on the y-axis
ax.set_xlabel(r"$e_b$")  # e on the x-axis
ax.set_xticks(np.arange(len(ecclist)))  # Set tick positions
ax.set_xticklabels(ecclist)  # Set tick labels
ax.set_yticks(np.arange(len(qblist)))  
ax.set_yticklabels(np.flip(qblist))  

# Annotate each cell with the corresponding value
for i in range(new_map.shape[0]):
    for j in range(new_map.shape[1]):
        ax.text(j, i, f"{new_map[i, j]:.2f}", ha='center', va='center', color='white')

# Adjust layout and save figure
plt.tight_layout()
fig.savefig('rmin_lambda_peak_ratio._paper_ready.pdf')
plt.show()



########
asdfjlk



fig, ax =plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(8)
sns.heatmap(rmin0_tau.to_numpy()/rmin1_tau.to_numpy(), cmap="viridis", annot=True, fmt=".2f", 
            cbar_kws={'label': r'$\tau_{r0} / \tau_{r1}$  '}, ax=ax,
            xticklabels=ecclist, yticklabels=np.flip(qblist),
            vmin=0.3,
            vmax=3,)
ax.set_ylabel("q (Mass Ratio)")  # q on the y-axis
ax.set_xlabel("e (Eccentricity)")  # e on the x-axis
plt.tight_layout()
fig.savefig('rmin1_rmin0_peak_ratio.pdf')

fig, ax =plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(8)
sns.heatmap(lambda_tau.to_numpy()/rmin1_tau.to_numpy(), cmap="viridis", annot=True, fmt=".2f", 
            cbar_kws={'label': r'$\tau_{\lambda} / \tau_{r1}$  '}, ax=ax,
            xticklabels=ecclist, yticklabels=np.flip(qblist),
            vmin=0.3,
            vmax=3,)
ax.set_ylabel("q (Mass Ratio)")  # q on the y-axis
ax.set_xlabel("e (Eccentricity)")  # e on the x-axis
plt.tight_layout()
fig.savefig('rmin1_lambda_peak_ratio.pdf')

fig, ax =plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(8)
sns.heatmap(lambda_tau.to_numpy()/rmin0_tau.to_numpy(), cmap="viridis", annot=True, fmt=".2f", 
            cbar_kws={'label': r'$\tau_{\lambda} / \tau_{r0}$  '}, ax=ax,
            xticklabels=ecclist, yticklabels=np.flip(qblist),
            vmin=0.3,
            vmax=3,)
            
ax.set_ylabel("q (Mass Ratio)")  # q on the y-axis
ax.set_xlabel("e (Eccentricity)")  # e on the x-axis
plt.tight_layout()
fig.savefig('rmin0_lambda_peak_ratio.pdf')
    
fig, ax =plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(8)
sns.heatmap(lambda_tau.to_numpy()/e1_tau.to_numpy(), cmap="viridis", 
            annot=True, fmt=".2f", cbar_kws={'label': r'$\tau_{\lambda} / \tau_{e}$  '  }, ax=ax,
            xticklabels=ecclist, yticklabels=np.flip(qblist),
            vmin=0.3,
            vmax=3,)
ax.set_ylabel("q (Mass Ratio)")  # q on the y-axis
ax.set_xlabel("e (Eccentricity)")  # e on the x-axis
plt.tight_layout()
fig.savefig('e1_lambda_peak_ratio.pdf')



fig, ax =plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(8)
ins=np.abs(lambda_phase.to_numpy()-e1_phase.to_numpy())
ins[ins >= math.pi] = 2*math.pi - ins[ins >= math.pi]
print(ins)
sns.heatmap(ins/math.pi, cmap="bwr", annot=True, fmt=".2f", 
            cbar_kws={'label': r'$ \left( \phi_{\lambda} - \phi_{e} \right)/\pi $'}, ax=ax,
            xticklabels=ecclist, yticklabels=np.flip(qblist),
            vmin=0, 
            vmax=1)
ax.set_ylabel("q (Mass Ratio)")  # q on the y-axis
ax.set_xlabel("e (Eccentricity)")  # e on the x-axis
plt.tight_layout()
fig.savefig('e1_lambda_phase_diff.pdf')

fig, ax =plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(8)
ins=np.abs(lambda_phase.to_numpy()-rmin1_phase.to_numpy())
ins[ins >= math.pi] = 2*math.pi - ins[ins >= math.pi]
print(ins)
sns.heatmap(ins/math.pi, cmap="bwr", 
            annot=True, fmt=".2f", cbar_kws={'label': r'$ \left( \phi_{\lambda} - \phi_{r1} \right)/\pi $'}, ax=ax,
            xticklabels=ecclist, yticklabels=np.flip(qblist),
            vmin=0, 
            vmax=1)
ax.set_ylabel("q (Mass Ratio)")  # q on the y-axis
ax.set_xlabel("e (Eccentricity)")  # e on the x-axis
plt.tight_layout()
fig.savefig('rmin1_lambda_phase_diff.pdf')

fig, ax =plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(8)
ins=np.abs(lambda_phase.to_numpy()-rmin0_phase.to_numpy())
ins[ins >= math.pi] = 2*math.pi - ins[ins >= math.pi]
print(ins)
sns.heatmap(ins/math.pi, cmap="bwr", annot=True, fmt=".2f",
            cbar_kws={'label': r'$ \left( \phi_{\lambda} - \phi_{r0} \right)/\pi $'}, ax=ax,
            xticklabels=ecclist, yticklabels=np.flip(qblist),
            vmin=0, 
            vmax=1)
ax.set_ylabel("q (Mass Ratio)")  # q on the y-axis
ax.set_xlabel("e (Eccentricity)")  # e on the x-axis
plt.tight_layout()
fig.savefig('rmin0_lambda_phase_diff.pdf')

fig, ax =plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(8)
ins=np.abs(rmin1_phase.to_numpy()-rmin0_phase.to_numpy())
ins[ins >= math.pi] = 2*math.pi - ins[ins >= math.pi]
print(ins)
sns.heatmap(ins/math.pi, cmap="bwr",
            annot=True, fmt=".2f", cbar_kws={'label': r'$\left( \phi_{r1} - \phi_{r0} \right)/\pi $'}, ax=ax,
            xticklabels=ecclist, yticklabels=np.flip(qblist),
            vmin=0, 
            vmax=1)
ax.set_ylabel("q (Mass Ratio)")  # q on the y-axis
ax.set_xlabel("e (Eccentricity)")  # e on the x-axis
plt.tight_layout()
fig.savefig('rmin0_rmin1_phase_diff.pdf')


