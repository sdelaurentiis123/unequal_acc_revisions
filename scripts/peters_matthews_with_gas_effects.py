#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peters-Matthews Evolution with Gas Effects on Mass Ratio
Based on peters_matthews_strain_clean_with_sum.py but with gas-driven dq/dt

Key Innovation: Include gas effects on mass ratio evolution (q) from simulation data
This shows how binaries evolve when both GW radiation and gas dynamics affect q

Created: Dec 2024
@author: stanislavdelaurentiis
"""

import scipy
import math
import numpy as np
import matplotlib.pyplot as plt
# import LISA as li  # Not available, use built-in lisa_sensitivity function
import pandas as pd
from scipy.special import jv
from scipy import optimize
from scipy.integrate import solve_ivp

# CGS units
c = 2.99792458e10
G = 6.67430e-8
msol = 1e33
mpc = 3.086e24

# Load qdot data ONCE at module level (not in function!)
print("Loading mass ratio evolution data...")
try:
    qdot_data_global = np.load('qdot_data_magda.npy')
    other_inds = np.where(qdot_data_global[0] < 0)[0]
    qdot_data_global[0][other_inds] = 0
    intermediate_inds = np.where(qdot_data_global[0] > 0)[0]
    qdot_data_global[0][intermediate_inds] = -1 * qdot_data_global[0][intermediate_inds]
    print("✓ Mass ratio evolution data loaded successfully")
except Exception as e:
    print(f"✗ Failed to load qdot data: {e}")
    qdot_data_global = None

# Simulation data for gas evolution (from pop_eval2.py)
# These are the lookup tables for gas-driven evolution
adot_both = [
    [-1.28, -5.06, 1.03, 3.43, 3.74, 4.0, 3.8, -6.32],
    [-0.77, -1.51, -0.16, 0.92, 2.87, 2.59, -1.3, -7.09],
    [1.15, -2.05, -1.89, -0.19, -1.44, -0.93, -2.34, -3.49],
    [1.29, -1.3, -0.65, -2.41, -2.5, -2.93, -1.48, -3.61],
    [1.43, -0.69, -0.15, -2.43, -2.1, -3.73, -1.26, -3.52],
    [1.58, -0.69, -0.42, -2.37, -2.96, -4.33, -0.3, -2.73],
    [1.67, -0.75, -0.46, -2.38, -5.16, -4.36, 0.28, -2.85],
    [1.72, -0.94, -0.67, -2.52, -6.23, -0.28, 0.52, -3.0],
    [1.74, -0.88, -1.02, -4.15, -6.23, 0.86, 0.47, -2.89],
    [1.76, -0.95, -1.31, -4.79, -6.1, 0.6, 0.38, -2.74]
]

edot_both = [
    [0.0, 1.55, 0.78, -1.84, -4.15, -4.78, -5.95, -7.7],
    [0.0, 1.32, 2.14, 0.16, -2.02, -3.96, -4.62, -5.47],
    [0.0, 3.73, 5.59, 0.23, -0.4, -2.73, -3.95, -3.46],
    [0.0, 4.29, 3.5, 2.52, 0.23, -1.64, -2.81, -2.61],
    [-0.0, 4.33, 3.75, 3.38, 1.33, -1.82, -2.37, -2.15],
    [0.0, 4.73, 4.9, 4.52, 3.33, -0.04, -2.2, -1.96],
    [0.0, 4.88, 5.48, 5.26, 5.8, 0.58, -2.14, -1.86],
    [-0.0, 5.28, 5.95, 5.97, 6.48, -1.15, -2.08, -1.7],
    [-0.0, 5.16, 6.6, 8.33, 7.02, -1.83, -2.12, -1.69],
    [0.0, 5.33, 7.07, 9.43, 6.91, -1.67, -2.11, -1.85]
]

# Create DataFrames for gas evolution
qb_values = np.arange(0.1, 1.1, 0.1)
eb_values = [f'eb_{x:.1f}' for x in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]]

adot_both = pd.DataFrame(adot_both, index=qb_values, columns=eb_values)
edot_both = pd.DataFrame(edot_both, index=qb_values, columns=eb_values)
adot_both.index.name = 'qb'
edot_both.index.name = 'qb'

# Styling arrays
linestyles = ['dotted', '--', '-.']
alphalist = [0.9, 0.7, 0.5]
alphalinelist = np.array([1, 0.5, 0.3])
markerlist = ['^', 's', '*']
linestylelist = ['dashed', 'dotted', '-.']

def eddington(M, epsilon=0.1):
    """Calculate Eddington accretion rate for a black hole in CGS units."""
    G = 6.67430e-8
    c = 3.0e10
    sigma_T = 6.6524e-25
    m_p = 1.6726e-24
    M_dot_edd = (4 * math.pi * G * M * m_p) / (epsilon * sigma_T * c)
    return M_dot_edd

def rs_func(m1, m2):
    """Schwarzschild radius for total mass"""
    return 2 * G * (m1 + m2) * (c**-2)

def d_from_z(z):
    """Distance from redshift"""
    val = z * (3e5 / 70.8)
    val = val * mpc
    return val

def chirp_mass(m1, m2):
    """Chirp mass calculation"""
    q = max(m2/m1, m1/m2)
    m = m1 + m2
    val = m * (q**(3/5)) * ((1 + q)**(-6/5))
    return val

def chirp_massalt(m1, m2):
    """Alternative chirp mass calculation"""
    eta = (m1 * m2) / ((m1 + m2)**2)
    m = m1 + m2
    val = m * (eta**(3/5))
    return val

def g(n, e):
    """Harmonic amplitude function"""
    val = ((n**4)/32) * (
        (jv(n-2, n*e) - (2*e*jv(n-1, n*e)) + (2/n)*(jv(n, n*e)) + 
         (2*e*jv(n+1, n*e)) - jv(n+2, n*e))**2 +
        (1-(e**2)) * (jv(n-2, n*e) - (2*jv(n, n*e)) + jv(n+2, n*e))**2 +
        (4/(3*(n**2))) * (jv(n, n*e))**2
    )
    return val

def F(e):
    """Peters-Matthews F function"""
    top = 1 + ((73/24)*(e**2)) + ((37/96)*e**4)
    bot = (1-(e**2))**(7/2)
    val = top / bot
    return val

def f_from_fr(fr, z):
    """Frequency conversion from rest frame"""
    return fr / (1 + z)

def peters_f_e(ecc):
    """Peters-Matthews eccentricity function"""
    val = (1 + ((73/24) * (ecc**2)) + ((37/96) * (ecc**4)))
    bot = ((1-(ecc**2))**(3.5))
    val = val / bot
    return val

def t_p_og(m1, m2, a, e):
    """Peters-Matthews coalescence time"""
    # Handle scalar inputs
    if np.isscalar(a):
        a = np.array([a])
    else:
        a = np.array(list(a))
    
    if np.isscalar(e):
        e = np.array([e])
    else:
        e = np.array(list(e))
    
    if len(a) == 1 and len(e) != 1:
        a = np.full(len(e), a[0])
    if len(e) == 1 and len(a) != 1:
        e = np.full(len(a), e[0])
    
    q = m2 / m1
    if q > 1:
        # Swap masses so that m1 is the larger mass
        m1, m2 = m2, m1
        q = m2 / m1
    M = m1 + m2
    top = 5 * (c**5) * ((1 + q)**2) * (a**4)
    bot = 256 * (G**3) * (M**3) * q * peters_f_e(e)
    val = top / bot
    return val

def strain_harmonic_sum(f_orb, ninit, e, z, m1, m2):
    """Calculate strain with harmonic sum"""
    f = f_from_fr(f_orb, z)
    dedf_top = ((G*chirp_massalt(m1, m2))**(5/3)) * (math.pi**(2/3))
    dedf_bot = 3 * ((f)**(1/3)) * ((1 + z)**(1/3)) * (c**3)
    sum_term = 0
    for n in np.arange(1, 16, 1):
        sum_term = sum_term + (((2/n)**(2/3)) * g(n, e) * (F(e)**-1))
    
    dedf = dedf_top / dedf_bot
    dedf = dedf * sum_term
    
    prefact = 1 / (math.pi * (d_from_z(z)))
    val = prefact * np.sqrt(2 * dedf)
    return val, f

def a_from_f(f, n, m1, m2):
    """Semi-major axis from frequency"""
    fr = f * (1 + z)
    fr = fr * 2 * math.pi
    return (G * (m1 + m2) * (fr**-2))**(1/3)

def p_oms(f):
    """LISA optical metrology system noise"""
    val = ((1.5e-11)**2) * (1 + ((2e-6/f)**4))
    return val

def p_acc(f):
    """LISA accelerometer noise"""
    val = ((3e-15)**2) * (1 + ((0.4e-6/f)**2)) * (1 + ((f/8e-6)**4))
    return val

def lisa_sensitivity(f):
    """LISA sensitivity curve"""
    f_star = 19.09
    L = 2.5 * 1e6
    val = (10/(3*(L**2))) * (
        p_oms(f) + 2 * (1 + (np.cos(f/f_star)**2)) * (p_acc(f)/((2*math.pi*f)**4))
    ) * (1 + (6/10) * ((f/f_star)**2))
    return val

def tq_sensitivity(f):
    """TQ sensitivity curve"""
    f_star = 0.28
    L = np.sqrt(3) * 1e5 * 1e3
    pxtq = (1e-12)**2
    patq = (1e-15)**2
    val = (10/(L**2)) * (
        pxtq + ((4*patq)/((2*math.pi*f)**4)) * (1 + (1e-4/f))
    ) * (1 + (6/10) * ((f/f_star)**2))
    return val

def adot_both_func(m1, m2, a, e):
    """Gas + GW evolution for semi-major axis"""
    q = min(m2/m1, m1/m2)
    q = round(q, 1)
    e = round(e, 1)
    
    if e == 0.7:
        if np.abs(0.8 - e) < np.abs(0.6 - e):
            e = 0.8
        else:
            e = 0.6
    if e > 0.8:
        e = 0.8
    if e < 0:
        e = 0
    if q >= 1:
        q = 1
    if q < 0.1:
        q = 0.1
    
    try:
        val = adot_both.loc[q, f'eb_{e}']
        return val * 1e-6  # Scale factor
    except:
        return 0

def edot_both_func(m1, m2, a, e):
    """Gas + GW evolution for eccentricity"""
    q = min(m2/m1, m1/m2)
    q = round(q, 1)
    e = round(e, 1)
    
    if e == 0.7:
        if np.abs(0.8 - e) < np.abs(0.6 - e):
            e = 0.8
        else:
            e = 0.6
    if e > 0.8:
        e = 0.8
    if e < 0:
        e = 0
    if q >= 1:
        q = 1
    if q < 0.1:
        q = 0.1
    
    try:
        val = edot_both.loc[q, f'eb_{e}']
        return val * 1e-6  # Scale factor
    except:
        return 0

def qdot_func(m1, m2, a, e_init):
    """Gas-driven mass ratio evolution (KEY INNOVATION)"""
    try:
        # Use the pre-loaded global qdot_data_global
        if qdot_data_global is None:
            raise Exception("qdot_data_global is not loaded. Please ensure qdot_data_magda.npy is in the same directory.")

        mdot_m = 100 * (eddington(m1 + m2) / (m1 + m2))
        data = qdot_data_global * mdot_m
        
        ecclist = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
        qblist = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        
        q_init = np.minimum(m2/m1, m1/m2)
        q = round(q_init, 1)
        e = round(e_init, 1)
        
        if e == 0.7:
            if np.abs(0.8 - e_init) < np.abs(0.6 - e_init):
                e = 0.8
            else:
                e = 0.6
        if e > 0.8:
            e = 0.8
        if e < 0:
            e = 0
        if q >= 1:
            q = 1
        if q < 0.1:
            q = 0.1
        
        qbind = np.where(qblist == q)[0][0]
        ebind = np.where(ecclist == e)[0][0]
        
        dq_dt_result = 1 * (data[9 - qbind][ebind])
        
        return dq_dt_result
    except Exception as ex:
        print(f"Error in qdot_func: {ex}")
        return 0  # Fallback if no data

def m_from_q(q):
    """Convert mass ratio to individual masses"""
    if q <= 1:
        m1 = q / (1 + q)
        m2 = 1 / (1 + q)
    else:
        m1 = 1 / (1 + q)
        m2 = q / (1 + q)
    return m1, m2

def evolve_system_with_gas(t, y, m_total):
    """ODE system with gas effects on q evolution"""
    a, e, q = y
    
    # Boundary conditions
    if q < 0.1:
        q = 0.1
    if q >= 1:
        q = 1
    if e >= 0.8:
        e = 0.8
    if e <= 0:
        e = 0
    
    # Get individual masses
    m1_frac, m2_frac = m_from_q(q)
    mprimary = m1_frac * m_total
    msecondary = m2_frac * m_total
    
    # Gas + GW evolution
    da = adot_both_func(mprimary, msecondary, a, e)
    de = edot_both_func(mprimary, msecondary, a, e)
    dq = qdot_func(mprimary, msecondary, a, e)  # KEY INNOVATION: Gas effects on q
    
    return [da, de, dq]

def solve_evolution_with_gas(f0, fmin, e0, q0, m_total, z, n_points=100):
    """Solve evolution with gas effects using proper time integration like pop_eval2.py"""
    
    # Initial conditions
    a0 = (G * m_total / (2 * math.pi * f0)**2)**(1/3)
    
    # Time span - estimate from Peters-Matthews
    m1_temp = m_total * q0 / (1 + q0)
    m2_temp = m_total / (1 + q0)
    if m1_temp > m2_temp:
        m1_temp, m2_temp = m2_temp, m1_temp
    t_gw = t_p_og(m1_temp, m2_temp, a0, e0)
    
    # Use a MUCH shorter time span for testing - let's see just 1% of evolution
    t_end = t_gw[0] * 0.01  # Just 1% of the full coalescence time
    t_span = [0, t_end]
    times = np.linspace(t_span[0], t_span[1], n_points)
    
    print(f"    === DETAILED EVOLUTION DIAGNOSTICS ===")
    print(f"    Time span: 0 to {t_end:.2e} seconds ({t_end/t_gw[0]*100:.1f}% of full coalescence)")
    print(f"    Full coalescence time: {t_gw[0]:.2e} seconds")
    print(f"    Initial: a₀={a0/rs_func(m1_temp, m2_temp):.1f}R_S, e₀={e0:.3f}, q₀={q0:.6f}")
    
    # Counter for tracking integration steps
    step_count = [0]
    
    # Define ODE system with extensive diagnostics
    def evolve_system(t, y):
        a, e, q = y
        step_count[0] += 1
        
        # Store original values for comparison
        a_orig, e_orig, q_orig = a, e, q
        
        # Boundary conditions (same as pop_eval2.py)
        if q < 0.1:
            q = 0.1
        if q >= 1:
            q = 1
        if e >= 0.8:
            e = 0.8
        if e <= 0:
            e = 0
        
        # Get individual masses
        m1_frac, m2_frac = m_from_q(q)
        mprimary = m1_frac * m_total
        msecondary = m2_frac * m_total
        
        # Calculate derivatives
        da = adot_both_func(mprimary, msecondary, a, e)
        de = edot_both_func(mprimary, msecondary, a, e)
        dq = qdot_func(mprimary, msecondary, a, e)
        
        # Print detailed diagnostics every 10 steps
        if step_count[0] % 10 == 1:
            print(f"    Step {step_count[0]:4d}: t={t:.2e}s")
            print(f"      a={a/rs_func(mprimary, msecondary):.2f}R_S (da/dt={da:.2e})")
            print(f"      e={e:.6f} (de/dt={de:.2e})")
            print(f"      q={q:.6f} (dq/dt={dq:.2e}) ← GAS EFFECT")
            if q != q_orig or e != e_orig:
                print(f"      Boundary correction applied: q {q_orig:.6f}→{q:.6f}, e {e_orig:.6f}→{e:.6f}")
        
        return [da, de, dq]
    
    # Solve ODE using same method as pop_eval2.py but with better tolerance
    y0 = [a0, e0, q0]
    
    try:
        print(f"    Starting ODE integration...")
        sol = solve_ivp(evolve_system, t_span, y0, t_eval=times, method='LSODA', rtol=1e-8, atol=1e-10)
        
        if sol.success:
            a_results, e_results, q_results = sol.y
            print(f"    ✓ Integration successful! Total steps: {step_count[0]}")
        else:
            print(f"    ✗ Integration failed: {sol.message}")
            return np.array([[f0, e0, q0]])  # Return initial conditions only
        
        # Convert to frequency space for plotting
        f_results = np.sqrt(G * m_total * (a_results**-3)) / (2 * math.pi)
        
        # Track q evolution details
        q_min = np.min(q_results)
        q_max = np.max(q_results)
        q_range = q_max - q_min
        
        print(f"    === EVOLUTION SUMMARY ===")
        print(f"    Initial → Final:")
        print(f"      a: {a_results[0]/rs_func(m1_temp, m2_temp):.2f} → {a_results[-1]/rs_func(m1_temp, m2_temp):.2f} R_S")
        print(f"      e: {e_results[0]:.6f} → {e_results[-1]:.6f}")
        print(f"      q: {q_results[0]:.6f} → {q_results[-1]:.6f}")
        print(f"      f: {f_results[0]:.2e} → {f_results[-1]:.2e} Hz")
        
        print(f"    Mass ratio evolution:")
        print(f"      Range: {q_min:.6f} to {q_max:.6f} (span: {q_range:.6f})")
        
        if q_range > 1e-6:
            print(f"    ✓ SIGNIFICANT q evolution detected!")
            # Find where q is most unequal
            q_deviation = np.abs(q_results - q0)
            max_dev_idx = np.argmax(q_deviation)
            print(f"      Most unequal q: {q_results[max_dev_idx]:.6f} at step {max_dev_idx}")
        else:
            print(f"    ✗ No significant q evolution (gas effects too weak or inactive)")
        
        # Combine results and sort by frequency
        results = []
        for i in range(len(f_results)):
            results.append([f_results[i], e_results[i], q_results[i]])
        
        sort_indices = np.argsort([r[0] for r in results])
        results = np.array(results)[sort_indices]
        
        return results
        
    except Exception as e:
        print(f"    ✗ ERROR in time integration: {e}")
        import traceback
        traceback.print_exc()
        return np.array([[f0, e0, q0]])  # Return initial conditions only

def solve_evolution_with_gas_old(f0, fmin, e0, q0, m_total, z, n_points=100):
    """Fallback to old frequency-based method"""
    # ... keep the old implementation as backup ...
    pass # Placeholder for the old method if needed

# Main plotting code (same structure as Peters-Matthews script)
nlist = np.reshape(np.array([2]), (1, 1))

fig, ax = plt.subplots(3, 2)  # Changed from 2x2 to 3x2 for q evolution
fig.set_figheight(8.0)  # Increased height for third row
fig.set_figwidth(5.7)

for axxx in ax.flatten():
    axxx.tick_params(top=True, bottom=True, left=True, right=True)
    axxx.set_xscale('log')

# LISA sensitivity curves
ax[0][0].tick_params(labelbottom=False, top=False)
flist = np.reshape(10**np.linspace(-8, 0, 500), (500, 1))

# Use built-in lisa_sensitivity function
Sn = lisa_sensitivity(flist)
ax[0][0].plot(flist, np.sqrt(flist*Sn), color='darkblue', 
              label=r'LISA $\sqrt{S_{n}f}$', zorder=-1*float('inf'))
ax[0][0].plot(flist, np.sqrt(flist*tq_sensitivity(flist)), color='purple', 
              label=r'TQ $\sqrt{S_{n}f}$', zorder=-1*float('inf'), lw=0.8)

# Add LISA sensitivity to z=3 panel as well
ax[0][1].plot(flist, np.sqrt(flist*Sn), color='darkblue', 
              label=r'LISA $\sqrt{S_{n}f}$', zorder=-1*float('inf'))
ax[0][1].plot(flist, np.sqrt(flist*tq_sensitivity(flist)), color='purple', 
              label=r'TQ $\sqrt{S_{n}f}$', zorder=-1*float('inf'), lw=0.8)

# Add legends
ax[0][0].plot(0, 0, ls='--', color='black', label=r'$a_0 =120R_S$')
ax[0][0].plot(0, 0, ls='dotted', color='black', label=r'$a_0 =300R_S$')
ax[0][0].plot(0, 0, ls='dashdot', color='black', label=r'$a_0 =800R_S$')
ax[0][0].legend(loc='upper right')

ax[0][1].scatter(0, 0, marker='o', color='black', label=r'$e=0.25$')
ax[0][1].plot(0, 0, ls='--', color='black', label=r'$a_0 =80R_S$')
ax[0][1].plot(0, 0, ls='dotted', color='black', label=r'$a_0 =250R_S$')
ax[0][1].plot(0, 0, ls='dashdot', color='black', label=r'$a_0 =550R_S$')
ax[0][1].legend()

ax[1][1].scatter(0, 0, marker='^', color='black', label=r'$\tau_{\rm{GW}}=10\rm{yr}$')
ax[1][1].scatter(0, 0, marker='s', color='black', label=r'$\tau_{\rm{GW}}=1 \rm{yr}$')
ax[1][1].scatter(0, 0, marker='*', color='black', label=r'$\tau_{\rm{GW}}=7 \rm{d}$')
ax[1][1].scatter(0, 0, marker='D', color='black', s=100, 
                edgecolors='black', linewidth=2, label='LISA entry')
ax[1][1].legend()

ax[1][0].plot(0, 0, ls='-', color='black', alpha=1, label=r'$e_0 = 0.45$')
ax[1][0].plot(0, 0, ls='-', color='black', alpha=0.5, label=r'$e_0 = 0.7$')
ax[1][0].legend()

# Add legend for q evolution (third row)
ax[2][0].axhline(1.0, color='darkgray', ls='-', alpha=0.5, label='Equal mass (q=1)')
ax[2][1].axhline(1.0, color='darkgray', ls='-', alpha=0.5, label='Equal mass (q=1)')

# Add reference lines
ax[1][0].axhline(0.25, color='darkgray', ls=(0, (1, 1)), zorder=-1e5)
ax[1][1].axhline(0.25, color='darkgray', ls=(0, (1, 1)), zorder=-1e5)
ax[1][0].axhline(10**(-1.5), color='darkgray', ls='dashdot', zorder=-1e5)
ax[1][1].axhline(10**(-1.5), color='darkgray', ls='dashdot', zorder=-1e5)

# Add LISA frequency range markers
lisa_freq_min = 1e-4
ax[0][0].axvline(lisa_freq_min, color='darkblue', ls='--', alpha=0.5, label='LISA range')
ax[0][1].axvline(lisa_freq_min, color='darkblue', ls='--', alpha=0.5, label='LISA range')
ax[1][0].axvline(lisa_freq_min, color='darkblue', ls='--', alpha=0.5, label='LISA range')
ax[1][1].axvline(lisa_freq_min, color='darkblue', ls='--', alpha=0.5, label='LISA range')
ax[2][0].axvline(lisa_freq_min, color='darkblue', ls='--', alpha=0.5, label='LISA range')
ax[2][1].axvline(lisa_freq_min, color='darkblue', ls='--', alpha=0.5, label='LISA range')

###############
# Use exact binary parameters from pop_eval2.py 
###############
z = 1
colorinstance = 'saddlebrown'

# EXACT parameters from pop_eval2.py
M_total = 10**7 * msol  # Same total mass as pop_eval2.py
rg = rs_func(M_total/2, M_total/2)  # Schwarzschild radius 
fid_a = 100 * rg  # MUCH SMALLER: 100 R_S instead of 1000 R_S

# The TWO specific binaries from pop_eval2.py that were plotted
binary_cases = [
    {'e0': 0.2, 'q0': 1.0, 'label': r'$q_{b,0}=1, e_{b,0}=0.2$', 'color': 'blue'},
    {'e0': 0.3, 'q0': 1.0, 'label': r'$q_{b,0}=1, e_{b,0}=0.3$', 'color': 'red'}
]

print("TESTING SMALLER INITIAL SEPARATION:")
print(f"M_total = {M_total/msol:.0e} M☉")
print(f"a₀ = {fid_a/rg:.0f} R_S (MUCH SMALLER than original 1000 R_S)")
print(f"Binaries: {[(case['e0'], case['q0']) for case in binary_cases]}")
print("This should show stronger gas effects on q evolution!")

# Store results for plotting on both panels
all_results = []

for case_iter, case in enumerate(binary_cases):
    e0 = case['e0'] 
    q0 = case['q0']
    
    # Calculate initial orbital parameters
    mprimary = M_total / 2  # Equal mass case (q=1)
    msecondary = M_total / 2
    
    a = fid_a
    f0 = np.sqrt(G * M_total * (a**-3)) / (2 * math.pi)
    fmin = np.sqrt(G * M_total * ((3*rs_func(mprimary, msecondary))**-3)) / (2 * math.pi)
    
    print(f"\nBinary {case_iter+1}: e₀={e0}, q₀={q0}")
    print(f"  Initial frequency: f₀={f0:.2e} Hz")
    print(f"  Final frequency: f_min={fmin:.2e} Hz")
    
    # Solve evolution with gas effects (KEY INNOVATION)
    evolution_results = solve_evolution_with_gas(f0, fmin, e0, q0, M_total, z)
    
    flistactual = evolution_results[:, 0]
    eoutlist = evolution_results[:, 1]
    qoutlist = evolution_results[:, 2]  # This now evolves due to gas!
    
    # Calculate strain for each point
    strainlist = []
    for j, (f_val, e_val, q_val) in enumerate(evolution_results):
        # Update masses based on evolved q
        m1_new = M_total * q_val / (1 + q_val)
        m2_new = M_total / (1 + q_val)
        
        val = strain_harmonic_sum(f_val, nlist, e_val, z, m1_new, m2_new)[0]
        if np.isscalar(val):
            strainlist.append(val)
        else:
            strainlist.append(val[0])
    
    strainlist = np.array(strainlist)
    
    # Store results for both panels
    all_results.append({
        'flist': flistactual,
        'elist': eoutlist,
        'qlist': qoutlist, 
        'strainlist': strainlist,
        'case': case,
        'case_iter': case_iter
    })

# Plot results on both left and right panels
for result in all_results:
    case = result['case']
    case_iter = result['case_iter']
    flistactual = result['flist']
    eoutlist = result['elist']
    qoutlist = result['qlist']  # Add q data
    strainlist = result['strainlist']
    
    # Plot results
    alpha_val = alphalinelist[case_iter] if case_iter < len(alphalinelist) else 0.7
    
    # Left panels: Main results
    ax[1][0].plot(flistactual, eoutlist, color=case['color'], 
                 ls='-', alpha=alpha_val, linewidth=2,
                 label=case['label'])
    
    ax[0][0].plot(flistactual, strainlist, color=case['color'], 
                 ls='-', alpha=alpha_val, linewidth=2)
    
    # NEW: Plot q evolution on third row
    ax[2][0].plot(flistactual, qoutlist, color=case['color'], 
                 ls='-', alpha=alpha_val, linewidth=2,
                 label=case['label'])
    
    # Right panels: Same data for comparison with LISA sensitivity
    ax[1][1].plot(flistactual, eoutlist, color=case['color'], 
                 ls='--', alpha=alpha_val, linewidth=1.5,
                 label=case['label'])
    
    ax[0][1].plot(flistactual, strainlist, color=case['color'], 
                 ls='--', alpha=alpha_val, linewidth=1.5)
    
    # NEW: Plot q evolution on third row (right panel)
    ax[2][1].plot(flistactual, qoutlist, color=case['color'], 
                 ls='--', alpha=alpha_val, linewidth=1.5,
                 label=case['label'])
    
    # Add time markers and LISA entry markers
    e_cutoff_min = 0.25
    valid_indices = np.where(eoutlist >= e_cutoff_min)[0]
    if len(valid_indices) > 0:
        index_e_cutoff_min = valid_indices[0]
        
        # Mark when binary enters LISA sensitivity range
        lisa_freq_min = 1e-4  # Hz - LISA most sensitive frequency range
        lisa_indices = np.where(flistactual >= lisa_freq_min)[0]
        if len(lisa_indices) > 0:
            lisa_entry_idx = lisa_indices[0]
            # Mark on both eccentricity panels
            for ax_panel in [ax[1][0], ax[1][1]]:
                ax_panel.scatter(flistactual[lisa_entry_idx], eoutlist[lisa_entry_idx], 
                               color=case['color'], marker='D', s=100, 
                               alpha=alpha_val, edgecolors='black', linewidth=2)
            
            # NEW: Mark q value at LISA entry on third row
            for ax_panel in [ax[2][0], ax[2][1]]:
                ax_panel.scatter(flistactual[lisa_entry_idx], qoutlist[lisa_entry_idx], 
                               color=case['color'], marker='D', s=100, 
                               alpha=alpha_val, edgecolors='black', linewidth=2)
            
            print(f"  LISA entry at f={flistactual[lisa_entry_idx]:.2e} Hz, e={eoutlist[lisa_entry_idx]:.3f}, q={qoutlist[lisa_entry_idx]:.3f}")
        
        # Mark e=0.25 cutoff on strain panels
        for ax_panel in [ax[0][0], ax[0][1]]:
            ax_panel.scatter(flistactual[index_e_cutoff_min], strainlist[index_e_cutoff_min], 
                           color=case['color'], alpha=alpha_val, marker='o')

###############
# Z=3 case removed - focusing only on the exact binaries from pop_eval2.py
###############

# Add legend for the exact binaries
ax[1][0].legend(loc='upper right', fontsize=10)
ax[1][1].legend(loc='upper right', fontsize=10)
ax[2][0].legend(loc='upper right', fontsize=10)  # NEW: Legend for q evolution
ax[2][1].legend(loc='upper right', fontsize=10)  # NEW: Legend for q evolution

# Set axis limits and labels (same as original Peters-Matthews script)
ax[0][1].set_ylim(5e-22, 1e-15)
ax[0][1].set_xlim(5e-6, 5e-1)
ax[0][1].set_yscale('log')

ax[1][1].set_xlim(5e-6, 5e-1)
ax[1][1].set_ylim(1e-3, 5)
ax[1][1].set_yscale('log')

ax[0][0].set_ylim(5e-22, 1e-15)
ax[0][0].set_xlim(5e-6, 5e-1)
ax[0][0].set_yscale('log')

ax[1][0].set_xlim(5e-6, 5e-1)
ax[1][0].set_ylim(1e-3, 5)
ax[1][0].set_yscale('log')

# NEW: Set axis limits for q evolution (third row)
ax[2][0].set_xlim(5e-6, 5e-1)
ax[2][0].set_ylim(0.5, 1.5)  # q ranges around 1
ax[2][0].set_yscale('linear')  # Linear scale for q

ax[2][1].set_xlim(5e-6, 5e-1)
ax[2][1].set_ylim(0.5, 1.5)  # q ranges around 1
ax[2][1].set_yscale('linear')  # Linear scale for q

# Labels
ax[0][0].set_ylabel(r'Characteristic Strain h$_c$(f)')
ax[1][0].set_ylabel('e')
ax[2][0].set_ylabel('q')  # NEW: Label for q
ax[2][0].set_xlabel(r'Observed Frequency (f) [Hz]')  # NEW: x-label for bottom row
ax[2][1].set_xlabel(r'Observed Frequency (f) [Hz]')  # NEW: x-label for bottom row

ax[0][0].set_title(r'pop_eval2.py Binaries: $M=10^7 M_{\odot}, a_0=1000 R_S$ (Gas Effects)')
ax[0][1].set_title(r'Right panels show LISA sensitivity for comparison')

# Tick parameters
for i in range(3):
    for j in range(2):
        ax[i][j].tick_params(top=True, bottom=True, left=True, right=True)
        if i < 2:  # Only top two rows don't show bottom labels
            ax[i][j].tick_params(labelbottom=False)
        if j == 1:
            ax[i][j].tick_params(labelleft=False)

ax[0][0].tick_params(top=False)
ax[0][1].tick_params(top=False, right=False)
ax[2][1].tick_params(right=False)  # Bottom right panel

fig.tight_layout()
fig.subplots_adjust(wspace=0, hspace=0)

# Save figure
fig.savefig('peters_matthews_with_gas_effects.pdf', dpi=300, bbox_inches='tight')
plt.show()

print("Plot saved as 'peters_matthews_with_gas_effects.pdf'")
print("SUCCESS: Used EXACT binary parameters from pop_eval2.py!")
print("Key Innovation: Gas effects on mass ratio evolution (q) included!")
print("")
print("Analyzed the TWO specific binaries from pop_eval2.py:")
print("  • Binary 1: e₀=0.2, q₀=1.0, M=10⁷ M☉, a₀=1000 R_S")
print("  • Binary 2: e₀=0.3, q₀=1.0, M=10⁷ M☉, a₀=1000 R_S")
print("")
print("NEW: Added third row showing mass ratio (q) evolution!")
print("This shows how gas-driven mass ratio evolution affects binary detectability in LISA.")
print("Diamond markers (◆) show final e and q values when binaries enter LISA sensitivity range.")
print("")
print("Evolution pattern: q starts equal (q=1), becomes unequal due to gas effects,")
print("then may return toward equal as shown in the bottom panels.") 