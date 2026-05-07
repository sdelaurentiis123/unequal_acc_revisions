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
    for start_index in range(len(time)):
        end_time = time[start_index] + window_size
        
        # Find the end index for the current window
        end_index = np.searchsorted(time, end_time, side='right') - 1
        
        # Check if we have enough points in the current window
        if end_index >= start_index:
            # Calculate total mass
            total_mass = np.sum(mass[start_index:end_index + 1])
            
            # Average derivative defined as total mass divided by the window size
            avg_derivative = total_mass / window_size
            
            # Append results (start_time, end_time, total_mass, avg_derivative, evaluated_time)
            evaluated_time = (time[start_index] + time[end_index]) / 2  # Midpoint of the window
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



qdot_slope_matrix=np.ones((10,8))
qdot_intercept_matrix=np.ones((10,8))

lambda_med_matrix=np.zeros((10,8))
lambda_mean_matrix=np.zeros((10,8))


ecclist=[0.0,0.1, 0.2,0.3,0.4,0.5,0.6,0.8]
qblist=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

i=0
fig, ax =plt.subplots(10,8, sharex=True, sharey=True,
                       gridspec_kw={'hspace': 0.0, 'wspace': 0.0})
figalt, axalt =plt.subplots(10,8, sharex=True, sharey=True,
                       gridspec_kw={'hspace': 0.0, 'wspace': 0.0})

fig1, ax1 =plt.subplots(10,8, sharex=True, sharey=True,
                       gridspec_kw={'hspace': 0.0, 'wspace': 0.0})
fig1alt, ax1alt =plt.subplots(10,8, sharex=True, sharey=True,
                       gridspec_kw={'hspace': 0.0, 'wspace': 0.0})

time_start_list=np.array([5800, 8000, 9000])
time_end_list=time_start_list+300

time_start_list=np.array([0])
time_end_list=time_start_list+10000

for timeindex in range(len(time_start_list)):
    time_start=time_start_list[timeindex]
    time_end=time_end_list[timeindex]
    for qbind in range(len(qblist)):
        for ebind in range(len(ecclist)):
            ecc=ecclist[ebind]
            qb=qblist[qbind]
            
            try:
                #if ecc==0.8 and qb==0.1:
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

                
                #ax[0][ebind].set_title('eb_'+str(ecc)+'_qb_'+str(qb))
                time=(df['time'].to_numpy()[1:])/(2*math.pi)
                mdot0=(df['mass_in0'].to_numpy()[1:])/np.diff(df['time'].to_numpy())
                mdot1=(df['mass_in1'].to_numpy()[1:])/np.diff(df['time'].to_numpy())
                
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
                

                
                
                

                
                time0_new, mdot0_new = sliding_window_mass_summary(time, mass_in0, 10)
                time1_new, mdot1_new = sliding_window_mass_summary(time, mass_in1, 10)
                # sfjslk  -- NameError breakpoint disabled for fig 5 regen
                
                ########

                import numpy as np

                def sliding_window_average(time, data, window_size):
                    """
                    Computes the sliding window average over a given window size in time units with non-overlapping windows.
                    
                    Parameters:
                    time (array-like): Input time values.
                    data (array-like): Input data values.
                    window_size (float): Size of the sliding window in time units.
                    
                    Returns:
                    tuple of np.ndarray: Two arrays, one for new times and one for averaged values.
                    """
                    if window_size <= 0:
                        raise ValueError("Window size must be positive")
                    
                    times = []
                    averages = []
                    start_idx = 0
                    
                    while start_idx < len(time):
                        end_idx = np.searchsorted(time, time[start_idx] + window_size, side='right')
                        if end_idx > len(time):
                            break
                        
                        window_time = time[start_idx:end_idx]
                        window_data = data[start_idx:end_idx]
                        
                        if len(window_data) > 0:
                            times.append(np.nanmean(window_time))
                            averages.append(np.nanmean(window_data))
                        
                        start_idx = end_idx
                    
                    return np.array(times), np.array(averages)
                
                def apply_savitzky_golay(data, window_length, polyorder):
                    from scipy.signal import savgol_filter
                    """
                    Applies the Savitzky-Golay filter for smoothing.
                    
                    Parameters:
                    data (array-like): Input data values.
                    window_length (int): The length of the filter window (must be odd and > polyorder).
                    polyorder (int): The order of the polynomial used to fit the samples.
                    
                    Returns:
                    np.ndarray: Smoothed data.
                    """
                    if window_length % 2 == 0:
                        raise ValueError("Window length must be an odd number")
                    if window_length <= polyorder:
                        raise ValueError("Window length must be greater than polyorder")
                    
                    return savgol_filter(data, window_length, polyorder)




                figtmp, axtmp = plt.subplots(3,1)
                time_old, lambda_old_avg = sliding_window_average(time, mdot0/mdot1, 10)
                #time_old, mdot1_old_avg = sliding_window_average(time, mdot1, 10)
                
                
                axtmp[0].plot(mdot0_new/mdot1_new)
                axtmp[1].plot(lambda_old_avg, color='red')
                axtmp[0].set_yscale('log')
                axtmp[1].set_yscale('log')
                #axtmp[1].set_ylim(0,5)
                
                
                figtmp.tight_layout()
                figtmp.savefig('averaging_mdot_method_comp.pdf')
                #asfdjlk
                #############
                
                lambda_new=mdot0_new/mdot1_new
                
                
                q_t_select=np.interp(time0_new, time, q, left=None, right=None)
                lambda_new_calc=1/lambda_new
                
                
                qdot_magdacalc= (1+q_t_select)*(lambda_new_calc-q_t_select)*((1+lambda_new_calc)**-1)
                
                
                qdot_slope_matrix[9-qbind][ebind]=np.mean(qdot_magdacalc[300:])
                #amplitude_of_qdot = 0.5 * (np.max(qdot_magdacalc[300:]) +np.min(qdot_magdacalc[300:]))
                
                #qdot_slope_matrix[9-qbind][ebind]=
                #qdot_intercept_matrix[9-qbind][ebind]=0
                
                ax[9-qbind][ebind].plot(time1_new, lambda_new_calc, color='black', alpha=0.5)
                #ax[9-qbind][ebind].plot(time[indices], q[indices],color='red', label='secondary', alpha=0.5)
                
                index_new_new=np.where(time1_new>2000)[0][0]
                lambda_mean_matrix[9-qbind][ebind]=np.mean(lambda_new[index_new_new])
                lambda_med_matrix[9-qbind][ebind]=np.median(lambda_new[index_new_new])
                
               
                axalt[9-qbind][ebind].plot(time[indices], q[indices]-qb, color='blue', alpha=0.5)
                
                #ax1[9-qbind][ebind].plot(time[indices], qdot[indices], color='black', alpha=0.5)
                
                #figtmp, axtmp=plt.subplots()
                #axtmp.plot(time0_new, qdot_magdacalc)
                #figtmp.savefig(f'''/Users/stanislavdelaurentiis/roman_work/qdot_dir/q_{qblist[qbind]}_e_{ecclist[ebind]}.pdf''')
                
                
                #fjaskldf
                continue
            
            except OSError:
                continue
    
    #commented out on 03/03 to make to not fuck with the larger plot
    #np.save('lambda_mean_data', lambda_mean_matrix)
    #np.save('lambda_med_data', lambda_med_matrix)
    
    #np.save('qdot_data_magda', qdot_slope_matrix)
    
    
    for axs in ax.flatten():
        axs.set_ylim(3e-2, 3e1)  # padding so 10^-1 and 10^1 tick labels don't crush at panel boundaries
        axs.set_yscale('log')
        axs.set_xlim(time_start,time_end)
        

        
    
    for axs in axalt.flatten():
        axs.set_ylim(-3e-2,3e-2)
        axs.set_xlim(time_start,time_end)
    

    LABEL_FS = 16
    TICK_FS = 11
    for i in range(10):
        ax[9-i][0].set_ylabel(r'$q_b$ = '+format(qblist[i],'.1f'), fontsize=LABEL_FS)
        axalt[9-i][0].set_ylabel(r'$q_b$ = '+format(qblist[i],'.1f'), fontsize=LABEL_FS)
        ax1[9-i][0].set_ylabel(r'$q_b$ = '+format(qblist[i],'.1f'), fontsize=LABEL_FS)
        ax1alt[9-i][0].set_ylabel(r'$q_b$ = '+format(qblist[i],'.1f'), fontsize=LABEL_FS)


    for i in range(8):
        ax[9][i].set_xlabel(r'$e_b$ = '+format(ecclist[i],'.1f'), fontsize=LABEL_FS)
        axalt[9][i].set_xlabel(r'$e_b$ = '+format(ecclist[i],'.1f'), fontsize=LABEL_FS)
        ax1alt[9][i].set_xlabel(r'$e_b$ = '+format(ecclist[i],'.1f'), fontsize=LABEL_FS)
        ax1[9][i].set_xlabel(r'$e_b$ = '+format(ecclist[i],'.1f'), fontsize=LABEL_FS)

    # Bigger tick labels on the visible (outer) panels
    for axs in ax.flatten():
        axs.tick_params(labelsize=TICK_FS)



    fig.set_figheight(20)
    fig.set_figwidth(16)

    fig.savefig('lambda_fixed_magda_ratio_'+str(time_start) + '_'+str(time_end)+'.pdf')
    plt.close(fig)
    import sys; sys.exit(0)
    
    
    
    
    afdjskl
    
    figalt.set_figheight(20)
    figalt.set_figwidth(21)             
    figalt.tight_layout()
    
    figalt.savefig('q_'+str(time_start) + '_'+str(time_end)+'.pdf')
    plt.close(figalt)
    
    
    for axs in ax1.flatten():
        axs.set_yscale('linear')
        axs.set_ylim(-1e-6,1e-6)

    fig1.set_figheight(20)
    fig1.set_figwidth(21)             
    fig1.tight_layout()
    
    fig1.savefig('qdot_fixed_'+str(time_start) + '_'+str(time_end)+'.pdf')
    plt.close(fig1)
    
    
    
    np.save('qdot_data_magda', qdot_slope_matrix)
    #np.save('qdot_intercept_data', qdot_intercept_matrix)
    
    
    asfdjl
    
    for axs in ax1.flatten():
        axs.set_yscale('linear')
        axs.set_ylim(-1e-6,1e-6)
    for axs in ax1alt.flatten():
        axs.set_yscale('linear')
        axs.set_ylim(-1e-6,1e-6)
    
    fig1.set_figheight(20)
    fig1.set_figwidth(21)             
    fig1.tight_layout()
    
    fig1.savefig('qdot_raw'+str(time_start) + '_'+str(time_end)+'.pdf')
    plt.close(fig1)
    
    
    fig1alt.set_figheight(20)
    fig1alt.set_figwidth(21)             
    fig1alt.tight_layout()
    
    fig1alt.savefig('qdot_smoothed'+str(time_start) + '_'+str(time_end)+'.pdf')
    plt.close(fig1alt)
    
    
    
    
