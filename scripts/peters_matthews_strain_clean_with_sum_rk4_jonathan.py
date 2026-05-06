#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 13:17:59 2024

@author: stanislavdelaurentiis
"""
import scipy
import math
import numpy as np
import matplotlib.pyplot as plt
import LISA as li

from scipy.special import jv
from scipy import optimize
#cgs units
c=2.99792458e10
G=6.67430e-8
#G=1
#c=1
msol=1e33
mpc=3.086e24


linestyles=['dotted','--', '-.', ]
alphalist=[0.9,0.7,0.5]

#
#d=zc/h0 h0=70.8 km/s/mpc
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

def rs_func(m1,m2):
    return(2*G*(m1+m2)*(c**-2))
def d_from_z(z):
    val = z*(3e5/70.8)
    val =val*mpc
    return(val)



def chirp_mass(m1,m2):
    q=max(m2/m1, m1/m2)
    m=m1+m2
    val=m*(q**(3/5))*((1+q)**(-6/5))
    return(val)
def chirp_massalt(m1,m2):
    eta=(m1*m2)/((m1+m2)**2)
    m=m1+m2
    val=m*(eta**(3/5))
    return(val)
def g(n,e):
    val=((n**4)/32)*(
                        ( jv(n-2,n*e) -(2*e*jv(n-1, n*e)) +(2/n)*(jv(n, n*e))  
                         + (2*e*jv(n+1, n*e)) - jv(n+2, n*e) )**2
                        +(1-(e**2))*( jv(n-2,n*e)- (2*jv(n,n*e)) + jv(n+2, n*e) )**2
                        +(4/(3*(n**2)))*( (jv(n,n*e))**2 )
        )
    return(val)
    
    
def F(e):
    top=1 + ((73/24)*(e**2)) +((37/96)*e**4)
    bot= (1-(e**2))**(7/2)
    val=top/bot
    return(val)

def f_from_fr(fr,z):
    return(fr/(1+z))


def peters_f_e(ecc):
     val=( 1+ ( (73/24)* (ecc**2)) + ( (37/96)* (ecc**4)) )
     bot=( (1-(ecc**2))**(3.5))
     #print('e', ecc)
     #print('bot', bot)
     val=val/bot
     return(val)
 
def t_p_og(m1,m2,a,e):
    a=np.array(list(a))
    e=np.array(list(e))
    if len(a)==1 and len(e)!=1:
        a=np.full(len(e),a[0])
        #print(a)
    if len(e)==1 and len(a)!=1:
        e=np.full(len(a),e[0])
        #print('yeah',e)
    
    
    q=m2/m1
    if q>1:
        raise Exception('m1 has to be < m2')
    M=m1+m2
    top=5*(c**5)*((1+q)**2)*(a**4)
    bot=256*(G**3)*(M**3)*q*peters_f_e(e)
    val=top/bot
    return(val)




def strain_harmonic(f_orb, n,e, z, m1,m2):
    f=f_from_fr(f_orb*n,z)
    prefact=1/(math.pi*d_from_z(z))
    dedf_top=((G*chirp_massalt(m1,m2))**(5/3))*((2/n)**(2/3))*g(n,e)
    dedf_bot=3*(math.pi**(1/3))*((f)**(4/3))*((1+z)**1/3)*F(e)
    dedf=dedf_top/dedf_bot
    dedf=dedf*(4/(c**2))
    val=prefact*np.sqrt(dedf)
    return(val,f)


def strain_harmonicnew(f_orb, n,e, z, m1,m2):
    f=f_from_fr(f_orb*n,z)
    prefact=1/(math.pi*d_from_z(z))
    dedf_top=((G*chirp_massalt(m1,m2))**(5/3))*((2/n)**(2/3))*g(n,e)
    dedf_bot=3*(math.pi**(1/3))*((f)**(4/3))*((1+z)**1/3)*F(e)
    dedf=dedf_top/dedf_bot
    dedf=dedf*(4*G/(c**2))
    val=prefact*np.sqrt(dedf)
    return(val,f)

#this is coming from huerta and barack combined
#huerta eq 20
#barack eq 46
def strainharmonic_newest(f_orb, n, e, z, m1, m2):
    f=f_from_fr(f_orb*n,z)
    dedf_top=((G*chirp_massalt(m1,m2))**(5/3))*((2/n)**(2/3))*g(n,e)*(math.pi**(2/3))
    dedf_bot=3*((f)**(1/3))*((1+z)**1/3)*F(e)*(c**3)
    dedf=dedf_top/dedf_bot
    prefact=1/(math.pi*(d_from_z(z)/(1+z)))
    val=prefact*np.sqrt(2*dedf)
    return(val,f)

def strain_harmonicalt(f_orb, n,e, z, m1,m2):
    f=f_from_fr(f_orb*n,z)
    val=2*np.sqrt(32/5)*((G*chirp_massalt(m1,m2))**(5/3))*((2*math.pi*f_orb)**(2/3))*np.sqrt(g(n,e))*(1+z)*((n*d_from_z(z))**-1)
    val=val*(c**-4)
    return(val,f)

def strain_harmonicalt2(f_orb, n,e, z, m1,m2):
    f=f_from_fr(f_orb*n,z)
    #val=
    val=2*np.sqrt(32/5)*((G*chirp_massalt(m1,m2))**(5/3))*((2*math.pi*f_orb)**(2/3))*np.sqrt(g(n,e))*(1+z)*((n*d_from_z(z))**-1)
    val=val/c**3
    return(val,f)

def a_from_f(f,n, m1,m2):
    fr=(f*(1+z))
    fr=fr*2*math.pi#to getit to be angular velocity omega
    return((G*(m1+m2)*(fr**-2))**(1/3))


def p_oms(f):
    val=((1.5e-11)**2)*(1+ ((2e-6/f)**4))
    return(val)
def p_acc(f):
    val = ((3e-15)**2)*(1+ ((0.4e-6/f)**2))*(1+ ((f/8e-6)**4))
    return(val)

def lisa_sensitivity(f):
    f_star=19.09#*1e-3
    L=2.5*1e6
    val = (10/(3*(L**2)))*(
        p_oms(f) + 2*(1+(np.cos(f/f_star)**2))*(p_acc(f)/((2*math.pi*f)**4) )
        ) *(1 + (6/10)*((f/f_star)**2) ) 
    return(val)

def tq_sensitivity(f):
    f_star=0.28#hz
    L=np.sqrt(3)*1e5*1e3
    pxtq=(1e-12)**2 #m hz
    #pxtq=pxtq*1e-3 #mhz to hz
    
    patq=(1e-15)**2 #mhz
    #patq=patq*1e-3
    
    val = (10/(L**2))*(
        pxtq +  ((4*patq)/((2*math.pi*f)**4))*(1 + (1e-4/f)))*(1 + (6/10)*((f/f_star)**2) ) 
    return(val)

#this is coming from huerta and barack combined
#huerta eq 20
#barack eq 46
def strain_harmonic(f_orb, n, e, z, m1, m2):
    f=f_from_fr(f_orb,z)
    dedf_top=((G*chirp_massalt(m1,m2))**(5/3))*((2/n)**(2/3))*g(n,e)*(math.pi**(2/3))
    dedf_bot=3*((f)**(1/3))*((1+z)**(1/3))*F(e)*(c**3)
    dedf=dedf_top/dedf_bot
    prefact=1/(math.pi*(d_from_z(z)))
    val=prefact*np.sqrt(2*dedf)
    val=val
    return(val,f)

def strain_harmonic_sum(f_orb,ninit, e, z, m1, m2):
    f=f_from_fr(f_orb,z)
    dedf_top=((G*chirp_massalt(m1,m2))**(5/3))*(math.pi**(2/3))
    dedf_bot=3*((f)**(1/3))*((1+z)**(1/3))*(c**3)
    sum_term=0
    for n in np.arange(1, 16,1):
        sum_term=sum_term + (((2/n)**(2/3))*g(n,e) * (F(e)**-1))
        print('n', n, 'this',(((2/n)**(2/3))*g(n,e) * (F(e)**-1)),  'sum', sum_term)
    
    dedf=dedf_top/dedf_bot
    dedf=dedf*sum_term
    
    prefact=1/(math.pi*(d_from_z(z)))
    val=prefact*np.sqrt(2*dedf)
    val=val
    return(val,f)

#def strainharmonic(f_orb,e, z, m1, m2):
#        f_orb=np.reshape(f_orb,(len(f_orb),1))
#        n=np.reshape(np.arange(1,51,1),(1,len(np.arange(1,51,1))))
#        e=np.array(e)
#        e=np.reshape(e,(len(e),1))
#        m1=np.array(m1)
#        m2=np.array(m2)
#        z=np.array(z)
#        f=f_from_fr(f_orb*n,z)
#        dedf_top=((G*chirp_massalt(m1,m2))**(5/3))*((2/n)**(2/3))*g(n,e)*(math.pi**(2/3))
#        dedf_bot=3*((f)**(1/3))*((1+z)**1/3)*F(e)*(c**3)
#        dedf=dedf_top/dedf_bot
#       prefact=1/(math.pi*(d_from_z(z)))
#        val=prefact*np.sqrt(2*dedf)
#        #summ.append(val)
#        return(np.sum(val, axis=1),np.sum(f,axis=1)/np.sum(n, axis=1))



def adot_gw_func(m1,m2,a,e):
    #a=np.array(list(a))
    #e=np.array(list(e))
    #if len(a)==1 and len(e)!=1:
    #    a=np.full(len(e),a[0])
    #if len(e)==1 and len(a)!=1:
    #    e=np.full(len(a),e[0])
        
    M=m1+m2
    q=m2/m1
    if q>1:
        raise Exception('m1 has to be < m2')
    top=-64*(G**3)*(M**3)*q*peters_f_e(e)
    bot=5*(c**5)*(a**3)*( (1+q)**2 )
    val=top/bot
    return(val)

def edot_gw_func(m1,m2,a,e):
    #a=np.array(list(a))
    #e=np.array(list(e))
    #if len(a)==1 and len(e)!=1:
    #    a=np.full(len(e),a[0])
    #if len(e)==1 and len(a)!=1:
    #    e=np.full(len(a),e[0])
        
    M=m1+m2
    q=m2/m1
    if q>1:
        raise Exception('m1 has to be < m2')
        
        
    top=-1*e*304*(G**3)*(M**3)*q*( 1+ ((121/304)*(e**2)) )
    bot=15*(c**5)*(a**4)*( (1-(e**2))**2.5 )*( (1+q)**2)
    
    val=top/bot
    return(val)

def func_gw(a, e):
    return(edot_gw_func(mprimary,msecondary,a,e)/adot_gw_func(mprimary,msecondary,a,e))

def adot_gas_func(a, e):
    mdot_m=eddington(mprimary+msecondary)/(mprimary+msecondary)
    return(-1*a*mdot_m)
def edot_gas_func(a,e):
    mdot_m=eddington(mprimary+msecondary)/(mprimary+msecondary)

# Data from the table
    ej_values = [0.000, 0.080, 0.160, 0.375, 0.445, 0.550, 0.630, 0.750, 0.800]
    dedlogm_values = [0.0, 0.0, 4.5, 4.0, 0.0, -3.0, -3.2, -2.7, -2.3]
    
    # Function to calculate the product term
    def product_term(j, e):
        product = 1
        for k in range(len(ej_values)):
            if k != j:
                product *= (e - ej_values[k]) / (ej_values[j] - ej_values[k])
        return product
    
    # Calculate the sum
    result = sum(dedlogm_values[j] * product_term(j, e) for j in range(len(ej_values)))
    result=result*mdot_m
    return result

def edot_both_func(m1, m2, a,e):
    return edot_gw_func(m1, m2, a,e)+edot_gas_func(a,e)

def adot_both_func(m1, m2, a,e):
    return adot_gw_func(m1, m2, a,e)+adot_gas_func(a,e)

def func_gas(a,e):
    return(edot_gas_func(a,e)/adot_gas_func(a,e))


def func_both(a, e):
    adot_both=adot_gas_func(a,e)+adot_gw_func(mprimary, msecondary, a,e)
    edot_both=edot_gas_func(a,e)+edot_gw_func(mprimary, msecondary, a,e)
    return(edot_both/adot_both)



# Define the RK4 method for a first-order differential equation dy/dx = f(y, x)
# here y is e, x is a
def rk4(func, y0, x0, x_end, h):
    f=func
    # Number of steps
    N = (int((x_end - x0) / h))
    
    # Arrays to store x and y values
    x_values = np.zeros(N+1)
    y_values = np.zeros(N+1)
    
    # Initial conditions
    x_values[0] = x0
    y_values[0] = y0
    
    # Runge-Kutta iteration
    for i in range(N):
        print
        x = x_values[i]
        y = y_values[i]
        
        k1 = h * f(x,y)
        k2 = h * f(x + h/2, y + k1/2)
        k3 = h * f(x + h/2, y + k2/2)
        k4 = h * f( x + h, y + k3)
        
        # Update y and x
        y_values[i+1] = y + (k1 + 2*k2 + 2*k3 + k4) / 6
        x_values[i+1] = x + h
        
    return x_values, y_values






mprimary=0.5e5*msol
msecondary=0.5e5*msol
rs=rs_func(mprimary, msecondary)

fig, ax=plt.subplots(1,1)
ax.plot(np.arange(0,0.8,0.01),edot_gas_func(300*rs, np.arange(0,0.8,0.01)), color='blue')#/np.arange(0,0.8,0.01))
ax.axhline(0, color='black', ls='--', alpha=0.1)
ax.set_ylabel(r'$\frac{de}{dt}$')
ax.set_xlabel(r'$e$')

ax.plot(np.arange(0,0.8,0.01),edot_gw_func(mprimary, msecondary, 300*rs, np.arange(0,0.8,0.01)), color='red')#/np.arange(0,0.8,0.01))
#ax[1].axhline(0, color='black', ls='--', alpha=0.1)
#ax[1].set_ylabel(r'$\frac{de}{dt}$')

#ax.plot(np.arange(0,0.8,0.01),edot_gw_func(300*rs, np.arange(0,0.8,0.01)), color='green')#/np.arange(0,0.8,0.01))
#ax[2].axhline(0, color='black', ls='--', alpha=0.1)
#ax[2].set_ylabel(r'$\frac{de}{dlogM}$')
#ax.set_xlabel(r'$e$')

fig.savefig('de_dt_tests.pdf')





def f_from_a(a):
    f=(1/(2*math.pi))*(np.sqrt(G*(mprimary+msecondary)*(a**-3)))
    return(f/(1+z))



def decoupling_radius_nu(a, e, nu):
    """ Calculate the decoupling radius using the merger timescale of an eccentric binary. """
    # Calculate the merger timescale
    T_P = t_p_og(mprimary, msecondary, a, e)
    
    # Calculate the decoupling radius using T_P = T_nu
    r_d = np.sqrt(T_P * nu)
    
    return r_d



z=1
fig, ax=plt.subplots(3,5)
e0list=[0.1, 0.445, 0.7]
a0list=[300*rs, 3000*rs, 5000*rs, 8000*rs, 10000*rs]




for i in range(len(e0list)):
    for j in range(len(a0list)):
        e0=e0list[i]
        a0=a0list[j]
        
        aout_gw, eout_gw=rk4(func_gw, e0, a0, 1*rs, -1*0.1*rs)
        f_gw=f_from_a(aout_gw)
        
        aout_gas, eout_gas=rk4(func_gas, e0, a0, 1*rs, -1*0.1*rs)
        f_gas=f_from_a(aout_gas)
        
        aout_both, eout_both=rk4(func_both, e0, a0, 1*rs, -1*0.1*rs)
        f_both=f_from_a(aout_both)
        
        
        ax[2-i][j].plot(f_gw, eout_gw, color='red', alpha=0.5, label='gws', ls='dotted')
        ax[2-i][j].plot(f_gas, eout_gas, color='blue', alpha=0.5, label='zrake+20 gas', ls='--')
        ax[2-i][j].plot(f_both, eout_both, color='purple', alpha=0.5, label='gas + gw', ls='-.')
        
        ax[2-i][j].set_xscale('log')
        ax[2-i][j].set_yscale('log')
        ax[2-i][j].set_xlim(1e-9, 1e-2)
        ax[2-i][j].set_ylim(1e-5, 1)
        a0str= format(a0/rs, '.0f')
        if j==0:
            ax[2-i][j].set_ylabel(fr"$e_0$ = { e0 }")
        if i==0:
            ax[2-i][j].set_xlabel(fr"$a_0$ = { a0str } $R_S$")
        
fig.set_figheight(10)
fig.set_figwidth(18)
fig.savefig('test_jonathan.pdf')
afsjlk





flist=np.reshape(10**np.linspace(-8, 0,500),(500,1))
n_try=np.reshape(np.array([1,2,3,4,5,6]),(1,6))
fig, ax=plt.subplots()
for i in range(np.shape(n_try)[1]):
    ax.plot(strain_harmonic(flist, n_try,0, 3, 0.5e7*msol,0.5e7*msol)[1],strain_harmonic(flist, n_try,0,3, 0.5e7*msol,0.5e7*msol)[0],alpha=[1,0.7,0.5, 0.2, 0.3,0.4][i], color='black')
ax.plot(strain_harmonic_sum(flist,n_try, 0, 3, 0.5e7*msol,0.5e7*msol)[1],strain_harmonic(flist, n_try,0,3, 0.5e7*msol,0.5e7*msol)[0],alpha=1, color='red')

ax.set_yscale('log')
ax.set_xscale('log')
#ax.set_ylim(3e-22,3e-15)
ax.set_xlim(1e-5,1e-1)
fig.tight_layout()
fig.savefig('developer.pdf')


##############
##############

alphalinelist=np.array([1,0.5,0.3])
alphalist=alphalinelist
#nlist=np.reshape(np.array([1,2,3,4]),(1,4))
nlist=np.reshape(np.array([2]),(1,1))
markerlist=['^','s', '*']
linestylelist=['dashed', 'dotted', '-.']

###########
##########


fig, ax=plt.subplots(2,2)
fig.set_figheight(5.5)
fig.set_figwidth(5.7)
#fig.set_figheight(6.7)
#fig.set_figwidth(6.7)
for axxx in ax.flatten():
    axxx.tick_params(top=True, bottom=True, left=True, right=True)
    axxx.set_xscale('log')
    

    
##################
##################
z=1
##################
##################
    
ax[0][0].tick_params(labelbottom=False, top=False)
flist=np.reshape(10**np.linspace(-8, 0,500),(500,1))
lisa = li.LISA() 


Sn = lisa.Sn(flist)
ax[0][0].plot(flist, np.sqrt(flist*Sn), color='darkblue', label=r'LISA $\sqrt{S_{n}f}$', zorder=-1*float('inf'))

#ax[0][0].plot(flist, np.sqrt(flist*lisa_sensitivity(flist)), color='purple', label=r'LISA $\sqrt{S_{n}f}$')
ax[0][0].plot(flist, np.sqrt(flist*tq_sensitivity(flist)), color='purple', label=r'TQ $\sqrt{S_{n}f}$', zorder=-1*float('inf'), lw=0.8)



ax[0][0].plot(0,0, ls='--', color='black', label=r'$a_0 =120R_S$')
ax[0][0].plot(0,0, ls='dotted', color='black', label=r'$a_0 =300R_S$')
ax[0][0].plot(0,0, ls='dashdot', color='black', label=r'$a_0 =800R_S$')
ax[0][0].legend(loc='upper right')


ax[0][1].scatter(0,0, marker='o', color='black', label=r'$e=0.25$')
ax[0][1].plot(0,0, ls='--', color='black', label=r'$a_0 =80R_S$')
ax[0][1].plot(0,0, ls='dotted', color='black', label=r'$a_0 =250R_S$')
ax[0][1].plot(0,0, ls='dashdot', color='black', label=r'$a_0 =550R_S$')
ax[0][1].legend()



ax[1][1].scatter(0,0, marker='^', color='black', label=r'$\tau_{\rm{GW}}=10\rm{yr}$')
ax[1][1].scatter(0,0, marker='s', color='black', label=r'$\tau_{\rm{GW}}=1 \rm{yr}$')
ax[1][1].scatter(0,0, marker='*', color='black', label=r'$\tau_{\rm{GW}}=7 \rm{d}$')
ax[1][1].legend()

ax[1][0].plot(0,0, ls='-', color='black', alpha=1, label=r'$e_0 = 0.45$')
ax[1][0].plot(0,0, ls='-', color='black', alpha=0.5, label=r'$e_0 = 0.7$')

ax[1][0].legend()
###############
###############
#1e7msol, z=1
###############
###############

ax[1][0].axhline(0.25, color='darkgray', ls=(0, (1, 1)), zorder=-1e5)
ax[1][1].axhline(0.25, color='darkgray', ls=(0, (1, 1)), zorder=-1e5)

ax[1][0].axhline(10**(-1.5), color='darkgray', ls='dashdot', zorder=-1e5)
ax[1][1].axhline(10**(-1.5), color='darkgray', ls='dashdot',zorder=-1e5)


colorinstance='saddlebrown'
mprimary=(0.5e7)*msol
msecondary=(0.5e7)*msol

alist=np.array([120])*rs_func(mprimary,msecondary)
for i in range(len(alist)):
    a=alist[i]
    f0=np.sqrt(G*(mprimary+msecondary)*(a**-3))/(2*math.pi)
    fmin=np.sqrt(G*(mprimary+msecondary)*((3*rs_func(mprimary,msecondary))**-3))/(2*math.pi)
    #flist_in=np.reshape(10**np.linspace(np.log10(f0), np.log10(fmin),100), 
                        #(len(10**np.linspace(np.log10(f0), np.log10(fmin),100)),1))
    e0=0.45
    strainlist=[]
    flistactual=[]
    eoutlist=[]
    #y1 is a
    #y2 is e
    t_vals, a_vals, e_vals = rk4_singleq(func_gw, e0, a, )



    
    
    
    for forb in flist_in:
        if e0==0:
            eoutt=0
            val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
            valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
            strainlist.append(val[0])
            flistactual.append(valfreq[0])
            eoutlist.append(eoutt)
            continue
        def e_root(e):
            #print(e)
            val0=(forb/f0)
            val1=(( (1-(e0**2))/(1-(e**2)) )*( (e/e0)**(12/19) )*( ( ( 1+((121/304)*(e**2)) )/( 1+((121/304)*(e0**2)) ) )**(870/2299)))**-1.5
            
            return(np.abs(val0-val1))
    
        eoutt=scipy.optimize.minimize_scalar(e_root, bounds=(0,1-1e-10),method='bounded', options={'xtol':1e-20}).x
        eoutlist.append(eoutt)
    
        val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
        valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
    
        strainlist.append(val[0])
        flistactual.append(valfreq[0])
        
    strainlist=np.array(strainlist)
    flistactual=np.array(flistactual)
    
    flistactual=np.reshape(flistactual, (len(flistactual), 1))
    strainlist=np.reshape(strainlist, (len(strainlist), 1))
    
    eoutlist=np.array(eoutlist)
    eoutlist=np.reshape(eoutlist, (len(eoutlist)))
    ax[1][0].plot(flistactual, eoutlist, color=colorinstance, ls=linestylelist[i])
    
    e_cutoff_min=0.25
    index_e_cuttoff_min=np.where(eoutlist<=e_cutoff_min)[0][0]
    
    for j in range(np.shape(nlist)[1]):
        t_peters_list=z*t_p_og(mprimary,msecondary,a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary), eoutlist)/(3600*24)
        index_month=np.where(t_peters_list<=10*365)[0][0]
        index_week=np.where(t_peters_list<=365)[0][0]
        index_day=np.where(t_peters_list<=7)[0][0]
        a_cutoff_min=20
        index_a_cuttoff_min=np.where( (a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary)/rs_func(mprimary, msecondary))<=a_cutoff_min)[0][0]
        #ax[0][0].scatter(flistactual[:,j][index_a_cuttoff_min], strainlist[:,j][index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
        if j==0:#this is the choice for which harmonic we are plotting the e of
            if index_month!=0: 
                ax[1][0].scatter(flistactual[:,j][index_month], eoutlist[index_month],color=colorinstance, marker=markerlist[0])
            if index_week!=0: 
                ax[1][0].scatter(flistactual[:,j][index_week], eoutlist[index_week], color=colorinstance, alpha=1, marker=markerlist[1])
            ax[1][0].scatter(flistactual[:,j][index_day], eoutlist[index_day], color=colorinstance, alpha=1, marker=markerlist[2])
            #ax[1][0].scatter(flistactual[:,j][index_a_cuttoff_min], eoutlist[index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
        ax[0][0].plot(flistactual[:,j],strainlist[:,j], color=colorinstance, ls=linestylelist[i], alpha=1)
        
        
        #ax[0][0].scatter(flistactual[:,j][index_month], strainlist[:,j][index_month], color=colorinstance, alpha=1, marker=markerlist[0])
        #ax[0][0].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=1, marker=markerlist[1])
        #ax[0][0].scatter(flistactual[:,j][index_day], strainlist[:,j][index_day], color=colorinstance, alpha=1, marker=markerlist[2])
        
        ax[0][0].scatter(flistactual[:,j][index_e_cuttoff_min], strainlist[:,j][index_e_cuttoff_min], color=colorinstance, alpha=1, marker='o')
        if index_week!=0: 
            ax[0][0].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=1, marker='s' )
        
        

###############
###############
#1e6msol, z=1
###############
###############

colorinstance='red'
mprimary=(0.5e6)*msol
msecondary=(0.5e6)*msol

alist=np.array([120,300])*rs_func(mprimary,msecondary)
for i in range(len(alist)):
    a=alist[i]
    f0=np.sqrt(G*(mprimary+msecondary)*(a**-3))/(2*math.pi)
    fmin=np.sqrt(G*(mprimary+msecondary)*((3*rs_func(mprimary,msecondary))**-3))/(2*math.pi)
    flist_in=np.reshape(10**np.linspace(np.log10(f0), np.log10(fmin),100), 
                        (len(10**np.linspace(np.log10(f0), np.log10(fmin),100)),1))
    e0list=[0.45,0.7]
    for e0iter in range(len(e0list)) :
        e0=e0list[e0iter]
        strainlist=[]
        flistactual=[]
        eoutlist=[]
        for forb in flist_in:
            if e0==0:
                eoutt=0
                val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
                valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
                strainlist.append(val[0])
                flistactual.append(valfreq[0])
                eoutlist.append(eoutt)
                continue
            def e_root(e):
                #print(e)
                val0=(forb/f0)
                val1=(( (1-(e0**2))/(1-(e**2)) )*( (e/e0)**(12/19) )*( ( ( 1+((121/304)*(e**2)) )/( 1+((121/304)*(e0**2)) ) )**(870/2299)))**-1.5
                
                return(np.abs(val0-val1))
        
            eoutt=scipy.optimize.minimize_scalar(e_root, bounds=(0,1-1e-10),method='bounded', options={'xtol':1e-20}).x
            eoutlist.append(eoutt)
        
            val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
            valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
        
            strainlist.append(val[0])
            flistactual.append(valfreq[0])
            
        strainlist=np.array(strainlist)
        flistactual=np.array(flistactual)
        
        flistactual=np.reshape(flistactual, (len(flistactual), 1))
        strainlist=np.reshape(strainlist, (len(strainlist), 1))
        
        eoutlist=np.array(eoutlist)
        eoutlist=np.reshape(eoutlist, (len(eoutlist)))
        ax[1][0].plot(flistactual[:,0], eoutlist, color=colorinstance, ls=linestylelist[i], alpha=alphalinelist[e0iter])
        e_cutoff_min=0.25
        index_e_cuttoff_min=np.where(eoutlist<=e_cutoff_min)[0][0]
        
        for j in range(np.shape(nlist)[1]):
            
            t_peters_list=z*t_p_og(mprimary,msecondary,a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary), eoutlist)/(3600*24)
            index_month=np.where(t_peters_list<=365*10)[0][0]
            index_week=np.where(t_peters_list<=365)[0][0]
            index_day=np.where(t_peters_list<=7)[0][0]
            #ax[0][0].scatter(flistactual[:,j][index_month], strainlist[:,j][index_month], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[0])
            #ax[0][0].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[1])
            #ax[0][0].scatter(flistactual[:,j][index_day], strainlist[:,j][index_day], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[2])
            
            
            
            a_cutoff_min=20
            index_a_cuttoff_min=np.where( (a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary)/rs_func(mprimary, msecondary))<=a_cutoff_min)[0][0]
            #ax[0][0].scatter(flistactual[:,j][index_a_cuttoff_min], strainlist[:,j][index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
            if j==0:#this is the choice for which harmonic we are plotting the e of
                if index_month!=0: 
                    ax[1][0].scatter(flistactual[:,j][index_month], eoutlist[index_month],color=colorinstance, alpha=alphalinelist[e0iter], marker=markerlist[0])
                if index_week!=0: 
                    ax[1][0].scatter(flistactual[:,j][index_week], eoutlist[index_week], color=colorinstance, alpha=alphalinelist[e0iter], marker=markerlist[1])
                ax[1][0].scatter(flistactual[:,j][index_day], eoutlist[index_day], color=colorinstance, alpha=alphalinelist[e0iter], marker=markerlist[2])
                #ax[1][0].scatter(flistactual[:,j][index_a_cuttoff_min], eoutlist[index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
            
            ax[0][0].plot(flistactual[:,j],strainlist[:,j], color=colorinstance, ls=linestylelist[i], alpha=alphalinelist[e0iter])
            ax[0][0].scatter(flistactual[:,j][index_e_cuttoff_min], strainlist[:,j][index_e_cuttoff_min], color=colorinstance, alpha=alphalinelist[e0iter], marker='o')
            if index_week!=0: 
                ax[0][0].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=alphalinelist[e0iter], marker='s' )
            
            
###############
###############
#1e5msol, z=1
###############
###############

colorinstance='green'
mprimary=(0.5e5)*msol
msecondary=(0.5e5)*msol

alist=np.array([120,300, 800])*rs_func(mprimary,msecondary)
for i in range(len(alist)):
    if i==0:
        continue
    a=alist[i]
    f0=np.sqrt(G*(mprimary+msecondary)*(a**-3))/(2*math.pi)
    fmin=np.sqrt(G*(mprimary+msecondary)*((3*rs_func(mprimary,msecondary))**-3))/(2*math.pi)
    flist_in=np.reshape(10**np.linspace(np.log10(f0), np.log10(fmin),100), 
                        (len(10**np.linspace(np.log10(f0), np.log10(fmin),100)),1))
    e0list=[0.45,0.7]
    for e0iter in range(len(e0list)) :
        e0=e0list[e0iter]
        strainlist=[]
        flistactual=[]
        eoutlist=[]
        for forb in flist_in:
            if e0==0:
                eoutt=0
                val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
                valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
                strainlist.append(val[0])
                flistactual.append(valfreq[0])
                eoutlist.append(eoutt)
                continue
            def e_root(e):
                #print(e)
                val0=(forb/f0)
                val1=(( (1-(e0**2))/(1-(e**2)) )*( (e/e0)**(12/19) )*( ( ( 1+((121/304)*(e**2)) )/( 1+((121/304)*(e0**2)) ) )**(870/2299)))**-1.5
                
                return(np.abs(val0-val1))
        
            eoutt=scipy.optimize.minimize_scalar(e_root, bounds=(0,1-1e-10),method='bounded', options={'xtol':1e-20}).x
            eoutlist.append(eoutt)
        
            val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
            valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
        
            strainlist.append(val[0])
            flistactual.append(valfreq[0])
            
        strainlist=np.array(strainlist)
        flistactual=np.array(flistactual)
        
        flistactual=np.reshape(flistactual, (len(flistactual), 1))
        strainlist=np.reshape(strainlist, (len(strainlist), 1))
        
        eoutlist=np.array(eoutlist)
        eoutlist=np.reshape(eoutlist, (len(eoutlist)))
        ax[1][0].plot(flistactual[:,0], eoutlist, color=colorinstance, ls=linestylelist[i], alpha=alphalinelist[e0iter])
        
        e_cutoff_min=0.25
        index_e_cuttoff_min=np.where(eoutlist<=e_cutoff_min)[0][0]
    
        for j in range(np.shape(nlist)[1]):
            
            t_peters_list=z*t_p_og(mprimary,msecondary,a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary), eoutlist)/(3600*24)
            index_month=np.where(t_peters_list<=365*10)[0][0]
            index_week=np.where(t_peters_list<=365)[0][0]
            index_day=np.where(t_peters_list<=7)[0][0]
            #if index_month!=0:
            #    ax[0][0].scatter(flistactual[:,j][index_month], strainlist[:,j][index_month], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[0])
            #if index_week!=0:
            #    ax[0][0].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[1])
            #ax[0][0].scatter(flistactual[:,j][index_day], strainlist[:,j][index_day], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[2])
            
            
            
            a_cutoff_min=20
            index_a_cuttoff_min=np.where( (a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary)/rs_func(mprimary, msecondary))<=a_cutoff_min)[0][0]
            #ax[0][0].scatter(flistactual[:,j][index_a_cuttoff_min], strainlist[:,j][index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
            if j==0:#this is the choice for which harmonic we are plotting the e of
                if index_month!=0:    
                    ax[1][0].scatter(flistactual[:,j][index_month], eoutlist[index_month],color=colorinstance,alpha=alphalinelist[e0iter], marker=markerlist[0])
                if index_week!=0:
                    ax[1][0].scatter(flistactual[:,j][index_week], eoutlist[index_week], color=colorinstance, alpha=alphalinelist[e0iter], marker=markerlist[1])
                ax[1][0].scatter(flistactual[:,j][index_day], eoutlist[index_day], color=colorinstance, alpha=alphalinelist[e0iter], marker=markerlist[2])
                #ax[1][0].scatter(flistactual[:,j][index_a_cuttoff_min], eoutlist[index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
                
            
            ax[0][0].scatter(flistactual[:,j][index_e_cuttoff_min], strainlist[:,j][index_e_cuttoff_min], color=colorinstance, alpha=alphalinelist[e0iter], marker='o')
            ax[0][0].plot(flistactual[:,j],strainlist[:,j], color=colorinstance, ls=linestylelist[i], alpha=alphalinelist[e0iter])
            if index_week!=0: 
                ax[0][0].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=alphalinelist[e0iter], marker='s' )
            

ax[0][0].set_ylim(5e-22,1e-15)
ax[0][0].set_xlim(5e-6,5e-1)
ax[0][0].set_xscale('log')
ax[0][0].set_yscale('log')

ax[1][0].set_xlim(5e-6,5e-1)
ax[1][0].set_ylim(1e-3,5)
ax[1][0].set_xscale('log')
ax[1][0].set_yscale('log')



##########################
##########################
##########################
##########################
#WE ARE NOW GOING TO Z=3
##########################
##########################
##########################
##########################


##################
##################
z=3
##################
##################
    
ax[0][1].tick_params(labelbottom=False, top=False)
flist=np.reshape(10**np.linspace(-8, 0,500),(500,1))
lisa = li.LISA() 
Sn = lisa.Sn(flist)
ax[0][1].plot(flist, np.sqrt(flist*Sn), color='darkblue', label=r'LISA $\sqrt{S_{n}f}$', zorder=-1*float('inf'))
ax[0][1].plot(flist, np.sqrt(flist*tq_sensitivity(flist)), color='purple', label=r'TQ $\sqrt{S_{n}f}$', zorder=-1*float('inf'), lw=0.8)


###############
###############
#1e7msol, z=3
###############
###############
colorinstance='saddlebrown'
mprimary=(0.5e7)*msol
msecondary=(0.5e7)*msol

alist=np.array([80])*rs_func(mprimary,msecondary)
for i in range(len(alist)):
    a=alist[i]
    f0=np.sqrt(G*(mprimary+msecondary)*(a**-3))/(2*math.pi)
    fmin=np.sqrt(G*(mprimary+msecondary)*((3*rs_func(mprimary,msecondary))**-3))/(2*math.pi)
    flist_in=np.reshape(10**np.linspace(np.log10(f0), np.log10(fmin),100), 
                        (len(10**np.linspace(np.log10(f0), np.log10(fmin),100)),1))
    e0=0.45
    strainlist=[]
    flistactual=[]
    eoutlist=[]
    for forb in flist_in:
        if e0==0:
            eoutt=0
            val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
            valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
            strainlist.append(val[0])
            flistactual.append(valfreq[0])
            eoutlist.append(eoutt)
            continue
        def e_root(e):
            #print(e)
            val0=(forb/f0)
            val1=(( (1-(e0**2))/(1-(e**2)) )*( (e/e0)**(12/19) )*( ( ( 1+((121/304)*(e**2)) )/( 1+((121/304)*(e0**2)) ) )**(870/2299)))**-1.5
            
            return(np.abs(val0-val1))
    
        eoutt=scipy.optimize.minimize_scalar(e_root, bounds=(0,1-1e-10),method='bounded', options={'xtol':1e-20}).x
        eoutlist.append(eoutt)
    
        val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
        valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
    
        strainlist.append(val[0])
        flistactual.append(valfreq[0])
        
    strainlist=np.array(strainlist)
    flistactual=np.array(flistactual)
    
    flistactual=np.reshape(flistactual, (len(flistactual), 1))
    strainlist=np.reshape(strainlist, (len(strainlist), 1))
    
    eoutlist=np.array(eoutlist)
    eoutlist=np.reshape(eoutlist, (len(eoutlist)))
    ax[1][1].plot(flistactual[:,0], eoutlist, color=colorinstance, ls=linestylelist[i])
    
    e_cutoff_min=0.25
    index_e_cuttoff_min=np.where(eoutlist<=e_cutoff_min)[0][0]

    
    for j in range(np.shape(nlist)[1]):
        
        t_peters_list=z*t_p_og(mprimary,msecondary,a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary), eoutlist)/(3600*24)
        index_month=np.where(t_peters_list<=365*10)[0][0]
        index_week=np.where(t_peters_list<=365)[0][0]
        index_day=np.where(t_peters_list<=7)[0][0]
        #ax[0][1].scatter(flistactual[:,j][index_month], strainlist[:,j][index_month], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[0])
        #ax[0][1].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[1])
        #ax[0][1].scatter(flistactual[:,j][index_day], strainlist[:,j][index_day], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[2])
        
        
        
        a_cutoff_min=20
        index_a_cuttoff_min=np.where( (a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary)/rs_func(mprimary, msecondary))<=a_cutoff_min)[0][0]
        #ax[0][1].scatter(flistactual[:,j][index_a_cuttoff_min], strainlist[:,j][index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
        if j==0:#this is the choice for which harmonic we are plotting the e of
            if index_month!=0: 
                ax[1][1].scatter(flistactual[:,j][index_month], eoutlist[index_month],color=colorinstance, alpha=1, marker=markerlist[0])
            if index_week!=0:
                ax[1][1].scatter(flistactual[:,j][index_week], eoutlist[index_week], color=colorinstance, alpha=1, marker=markerlist[1])
            ax[1][1].scatter(flistactual[:,j][index_day], eoutlist[index_day], color=colorinstance, alpha=1, marker=markerlist[2])
            #ax[1][1].scatter(flistactual[:,j][index_a_cuttoff_min], eoutlist[index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
            
        ax[0][1].plot(flistactual[:,j],strainlist[:,j], color=colorinstance, ls=linestylelist[i], alpha=1)
        ax[0][1].scatter(flistactual[:,j][index_e_cuttoff_min], strainlist[:,j][index_e_cuttoff_min], color=colorinstance, alpha=1, marker='o')
        if index_week!=0: 
            ax[0][1].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=1, marker='s' )
        
        
###############
###############
#1e6msol, z=3
###############
###############

colorinstance='red'
mprimary=(0.5e6)*msol
msecondary=(0.5e6)*msol

alist=np.array([80,250])*rs_func(mprimary,msecondary)
for i in range(len(alist)):
    a=alist[i]
    f0=np.sqrt(G*(mprimary+msecondary)*(a**-3))/(2*math.pi)
    fmin=np.sqrt(G*(mprimary+msecondary)*((3*rs_func(mprimary,msecondary))**-3))/(2*math.pi)
    flist_in=np.reshape(10**np.linspace(np.log10(f0), np.log10(fmin),100), 
                        (len(10**np.linspace(np.log10(f0), np.log10(fmin),100)),1))
    e0list=[0.45,0.7]
    for e0iter in range(len(e0list)) :
        e0=e0list[e0iter]
        strainlist=[]
        flistactual=[]
        eoutlist=[]
        for forb in flist_in:
            if e0==0:
                eoutt=0
                val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
                valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
                strainlist.append(val[0])
                flistactual.append(valfreq[0])
                eoutlist.append(eoutt)
                continue
            def e_root(e):
                #print(e)
                val0=(forb/f0)
                val1=(( (1-(e0**2))/(1-(e**2)) )*( (e/e0)**(12/19) )*( ( ( 1+((121/304)*(e**2)) )/( 1+((121/304)*(e0**2)) ) )**(870/2299)))**-1.5
                
                return(np.abs(val0-val1))
        
            eoutt=scipy.optimize.minimize_scalar(e_root, bounds=(0,1-1e-10),method='bounded', options={'xtol':1e-20}).x
            eoutlist.append(eoutt)
        
            val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
            valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
        
            strainlist.append(val[0])
            flistactual.append(valfreq[0])
            
        strainlist=np.array(strainlist)
        flistactual=np.array(flistactual)
        
        flistactual=np.reshape(flistactual, (len(flistactual), 1))
        strainlist=np.reshape(strainlist, (len(strainlist), 1))
        
        eoutlist=np.array(eoutlist)
        eoutlist=np.reshape(eoutlist, (len(eoutlist)))
        ax[1][1].plot(flistactual[:,0], eoutlist, color=colorinstance, ls=linestylelist[i], alpha=alphalinelist[e0iter])
        
        
        e_cutoff_min=0.25
        index_e_cuttoff_min=np.where(eoutlist<=e_cutoff_min)[0][0]
    
        
        for j in range(np.shape(nlist)[1]):
            
            t_peters_list=z*t_p_og(mprimary,msecondary,a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary), eoutlist)/(3600*24)
            index_month=np.where(t_peters_list<=365*10)[0][0]
            index_week=np.where(t_peters_list<=365)[0][0]
            index_day=np.where(t_peters_list<=7)[0][0]
            #ax[0][1].scatter(flistactual[:,j][index_month], strainlist[:,j][index_month], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[0])
            #ax[0][1].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[1])
            #ax[0][1].scatter(flistactual[:,j][index_day], strainlist[:,j][index_day], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[2])
            
            
           
            
            
            
            a_cutoff_min=20
            index_a_cuttoff_min=np.where( (a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary)/rs_func(mprimary, msecondary))<=a_cutoff_min)[0][0]
            #ax[0][1].scatter(flistactual[:,j][index_a_cuttoff_min], strainlist[:,j][index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
            
            if j==0:#this is the choice for which harmonic we are plotting the e of
                if index_month!=0: 
                    ax[1][1].scatter(flistactual[:,j][index_month], eoutlist[index_month],color=colorinstance, alpha=alphalinelist[e0iter], marker=markerlist[0])
                if index_week!=0: 
                    ax[1][1].scatter(flistactual[:,j][index_week], eoutlist[index_week], color=colorinstance, alpha=alphalinelist[e0iter], marker=markerlist[1])
                ax[1][1].scatter(flistactual[:,j][index_day], eoutlist[index_day], color=colorinstance,  alpha=alphalinelist[e0iter], marker=markerlist[2])
                #ax[1][1].scatter(flistactual[:,j][index_a_cuttoff_min], eoutlist[index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
                
        ax[0][1].plot(flistactual[:,j],strainlist[:,j], color=colorinstance, ls=linestylelist[i], alpha=alphalinelist[e0iter])
        ax[0][1].scatter(flistactual[:,j][index_e_cuttoff_min], strainlist[:,j][index_e_cuttoff_min], color=colorinstance, alpha=alphalinelist[e0iter], marker='o')
        if index_week!=0: 
            ax[0][1].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=alphalinelist[e0iter], marker='s' )
        
###############
###############
#1e5msol, z=3
###############
###############

colorinstance='green'
mprimary=(0.5e5)*msol
msecondary=(0.5e5)*msol

alist=np.array([80,250,550])*rs_func(mprimary,msecondary)
for i in range(len(alist)):
    if i==0:
        continue
    a=alist[i]
    f0=np.sqrt(G*(mprimary+msecondary)*(a**-3))/(2*math.pi)
    fmin=np.sqrt(G*(mprimary+msecondary)*((3*rs_func(mprimary,msecondary))**-3))/(2*math.pi)
    flist_in=np.reshape(10**np.linspace(np.log10(f0), np.log10(fmin),100), 
                        (len(10**np.linspace(np.log10(f0), np.log10(fmin),100)),1))
    e0list=[0.45,0.7]
    for e0iter in range(len(e0list)) :
        e0=e0list[e0iter]
        strainlist=[]
        flistactual=[]
        eoutlist=[]
        for forb in flist_in:
            if e0==0:
                eoutt=0
                val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
                valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
                strainlist.append(val[0])
                flistactual.append(valfreq[0])
                eoutlist.append(eoutt)
                continue
            def e_root(e):
                #print(e)
                val0=(forb/f0)
                val1=(( (1-(e0**2))/(1-(e**2)) )*( (e/e0)**(12/19) )*( ( ( 1+((121/304)*(e**2)) )/( 1+((121/304)*(e0**2)) ) )**(870/2299)))**-1.5
                
                return(np.abs(val0-val1))
        
            eoutt=scipy.optimize.minimize_scalar(e_root, bounds=(0,1-1e-10),method='bounded', options={'xtol':1e-20}).x
            eoutlist.append(eoutt)
        
            val=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[0]
            valfreq=strain_harmonic_sum(forb, nlist, eoutt, z, mprimary,msecondary)[1]
        
            strainlist.append(val[0])
            flistactual.append(valfreq[0])
            
        strainlist=np.array(strainlist)
        flistactual=np.array(flistactual)
        
        flistactual=np.reshape(flistactual, (len(flistactual), 1))
        strainlist=np.reshape(strainlist, (len(strainlist), 1))
        
        eoutlist=np.array(eoutlist)
        eoutlist=np.reshape(eoutlist, (len(eoutlist)))
        ax[1][1].plot(flistactual[:,0], eoutlist, color=colorinstance, ls=linestylelist[i], alpha=alphalinelist[e0iter])
      
        
        e_cutoff_min=0.25
        index_e_cuttoff_min=np.where(eoutlist<=e_cutoff_min)[0][0]
    
        
        for j in range(np.shape(nlist)[1]):
            
            t_peters_list=z*t_p_og(mprimary,msecondary,a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary), eoutlist)/(3600*24)
            index_month=np.where(t_peters_list<=365*10)[0][0]
            index_week=np.where(t_peters_list<=365)[0][0]
            index_day=np.where(t_peters_list<=7)[0][0]
            #if index_month!=0:
            #    ax[0][1].scatter(flistactual[:,j][index_month], strainlist[:,j][index_month], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[0])
            #if index_week!=0:
            #    ax[0][1].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[1])
            #ax[0][1].scatter(flistactual[:,j][index_day], strainlist[:,j][index_day], color=colorinstance, alpha=alphalinelist[j], marker=markerlist[2])
            
            
            
            a_cutoff_min=20
            index_a_cuttoff_min=np.where( (a_from_f(flistactual[:,j],nlist[:,j], mprimary, msecondary)/rs_func(mprimary, msecondary))<=a_cutoff_min)[0][0]
            #ax[0][1].scatter(flistactual[:,j][index_a_cuttoff_min], strainlist[:,j][index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
            if j==0:#this is the choice for which harmonic we are plotting the e of
                if index_month!=0:
                    ax[1][1].scatter(flistactual[:,j][index_month], eoutlist[index_month],color=colorinstance, alpha=alphalinelist[e0iter], marker=markerlist[0])
                if index_week!=0:
                    ax[1][1].scatter(flistactual[:,j][index_week], eoutlist[index_week], color=colorinstance,  alpha=alphalinelist[e0iter], marker=markerlist[1])
                ax[1][1].scatter(flistactual[:,j][index_day], eoutlist[index_day], color=colorinstance, alpha=alphalinelist[e0iter], marker=markerlist[2])
                #ax[1][1].scatter(flistactual[:,j][index_a_cuttoff_min], eoutlist[index_a_cuttoff_min], color=colorinstance, alpha=alphalinelist[j], marker='d')
                
            ax[0][1].plot(flistactual[:,j],strainlist[:,j], color=colorinstance, ls=linestylelist[i], alpha=alphalinelist[e0iter])
            ax[0][1].scatter(flistactual[:,j][index_e_cuttoff_min], strainlist[:,j][index_e_cuttoff_min], color=colorinstance, alpha=alphalinelist[e0iter], marker='o')
            if index_week!=0: 
                ax[0][1].scatter(flistactual[:,j][index_week], strainlist[:,j][index_week], color=colorinstance, alpha=alphalinelist[e0iter], marker='s' )
            
            
   
    
ax[0][1].set_ylim(5e-22,1e-15)
ax[0][1].set_xlim(5e-6,5e-1)
ax[0][1].set_xscale('log')
ax[0][1].set_yscale('log')

ax[1][1].set_xlim(5e-6,5e-1)
ax[1][1].set_ylim(1e-3,5)
ax[1][1].set_xscale('log')
ax[1][1].set_yscale('log')


ax[0][0].set_ylabel(r'Characteristic Strain h$_c$(f)')
ax[1][0].set_xlabel(r'Observed Frequency (f) [Hz]')
ax[1][1].set_xlabel(r'Observed Frequency (f) [Hz]')
ax[1][0].set_ylabel('e')

ax[0][0].set_title(r'$Z=1$')
ax[0][1].set_title(r'$Z=3$')

for i in range(2):
    for j in range(2):
        ax[i][j].tick_params(top=True, bottom=True, left=True, right=True)
        if i==0:
            ax[i][j].tick_params(labelbottom=False)
        if j==1:
            ax[i][j].tick_params(labelleft=False)


ax[0][0].tick_params(top=False)
ax[0][1].tick_params(top=False, right=False)
ax[1][1].tick_params(right=False)
fig.tight_layout()
fig.subplots_adjust(wspace=0, hspace=0)    

#msfdkjsdlf
fig.savefig('strain_calcs_closetofinal_with_sum.pdf')
sdfmslk
def e_root(e):
    #print(e)
    #val0=(forb/f0)
    val1=(( (1-(e0**2))/(1-(e**2)) )*( (e/e0)**(12/19) )*( ( ( 1+((121/304)*(e**2)) )/( 1+((121/304)*(e0**2)) ) )**(870/2299)))**-1.5
    
    #return(np.abs(val0-val1))
