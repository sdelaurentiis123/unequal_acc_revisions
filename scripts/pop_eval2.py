#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 12:05:22 2024

@author: stanislavdelaurentiis
"""
import numpy as np
import pandas as pd
import pandas as pd

df = pd.read_csv('merger_data.txt', 
                 delim_whitespace=True,  # Use whitespace as delimiter
                 comment='#',            # Treat lines starting with # as comments
                 names=['ID_in', 'ID_out', 'q', 'm_tot', 'z'])
print(df)
print(df.columns)

print(df['q'])
df_reduc=df[df['q']>=0.1]
print(df_reduc)

q_points=df_reduc['q']


print(q_points)

import matplotlib.pyplot as plt

fig, ax=plt.subplots()
#ax.scatter(df_reduc['q'].to_numpy(),df_reduc['z'].to_numpy())
#density=True makes it a pdf
bin_edges = np.linspace(0.05, 1.05, 11)  # 12 edges for 11 bins

# Generate histogram with these bin edges
counts_q, bins, _ = ax.hist(
    df_reduc[(np.log10(df_reduc['m_tot']) > 6.5) & (np.log10(df_reduc['m_tot']) < 7.5)]['q'].to_numpy(),
    bins=bin_edges,
    color='red',
    zorder=float('inf'),
    density=True
)
ax.set_xlabel('q')
ax.set_ylabel('pdf')
fig.suptitle('illustris smbbh systems (all z)')
fig.savefig('illustris_tng_smbbh_q_pdf.pdf')


fig, ax=plt.subplots()

plt.figure()

plt.hist2d(np.log10(df_reduc['m_tot']), df_reduc['q'], bins=[np.array([6,7,8,9]), np.arange(0.1,1.05,0.1)], cmap='nipy_spectral', density=True)
plt.colorbar(label='Probability Density')  # Show color scale
plt.title('2D Probability Distribution (Separate Bins)')
plt.xlabel('m tot')
plt.ylabel('q')
plt.savefig('yoyo.pdf')
#plt.show()







import pandas as pd
import numpy as np

# Create DataFrame for both table \adot (g + a)
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

# Create DataFrame for grav table \adot  (g_r > a)
adot_grav = [
    [-8.88, -14.71, -5.51, 0.88, 3.45, 3.53, 2.57, 1.3],
    [-7.37, -8.68, -9.63, -0.75, 0.73, 2.59, 1.01, -0.88],
    [-5.23, -8.59, -12.52, -3.96, -4.19, -0.22, 2.54, 2.35],
    [-4.99, -7.76, -9.93, -7.38, -5.1, -0.65, 1.22, -0.77],
    [-4.67, -7.03, -5.63, -7.37, -5.78, -3.18, 0.66, -0.71],
    [-4.41, -7.03, -6.3, -7.62, -7.36, -6.0, -1.08, -2.14],
    [-4.27, -7.06, -6.53, -7.77, -9.31, -5.86, -1.22, -2.53],
    [-4.2, -7.21, -6.81, -8.09, -10.12, -2.89, -1.37, -2.4],
    [-4.16, -7.13, -7.23, -9.97, -10.56, -2.05, -1.38, -2.24],
    [-4.15, -7.19, -7.54, -10.59, -10.46, -2.27, -1.39, -2.18]
]

# Create indices and column names
qb_values = np.arange(0.1, 1.1, 0.1)
eb_values = [f'eb_{x:.1f}' for x in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]]

# Create the DataFrames
adot_both = pd.DataFrame(adot_both, index=qb_values, columns=eb_values)
adot_grav = pd.DataFrame(adot_grav, index=qb_values, columns=eb_values)

# Set index names
adot_both.index.name = 'qb'
adot_grav.index.name = 'qb'


##

# Create DataFrame for both table (ėb[M̄b/Mb], g + a)
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

# Create DataFrame for grav table (ėb[M̄b/Mb], gr > a)
edot_grav = [
    [0.0, 0.12, -7.74, -8.28, -8.12, -8.56, -8.88, -3.31],
    [0.0, 1.16, 4.83, -2.71, -2.23, -4.83, -3.38, -1.68],
    [0.0, 2.87, 8.4, 2.08, 4.65, -0.61, -1.56, -1.93],
    [0.0, 3.33, 4.27, 4.05, 3.69, 1.55, -0.98, -1.33],
    [-0.0, 3.59, 4.54, 5.38, 0.88, 0.23, -0.31, -0.82],
    [0.0, 4.1, 5.39, 6.57, 4.03, 0.87, -1.06, -0.69],
    [0.0, 4.41, 5.89, 7.37, 6.49, 2.2, -1.11, -0.27],
    [-0.0, 4.89, 6.2, 7.81, 7.58, 0.63, -0.66, -0.17],
    [-0.0, 4.8, 6.7, 9.5, 8.5, -0.04, -0.56, -0.3],
    [0.0, 4.98, 7.13, 10.53, 8.46, 0.23, -0.51, -0.39]
]

# Create indices and column names
qb_values = np.arange(0.1, 1.1, 0.1)
eb_values = [f'eb_{x:.1f}' for x in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]]

# Create the DataFrames
edot_both = pd.DataFrame(edot_both, index=qb_values, columns=eb_values)
edot_grav = pd.DataFrame(edot_grav, index=qb_values, columns=eb_values)

# Set index names
edot_both.index.name = 'qb'
edot_grav.index.name = 'qb'


import scipy
import math
import numpy as np
import matplotlib.pyplot as plt


from scipy.special import jv
from scipy import optimize
from scipy.integrate import solve_ivp
#cgs units
c=2.99792458e10
G=6.67430e-8
#G=1
#c=1
msol=1e33
mpc=3.086e24
z=1


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
def rs_func(mtot):
    return(2*G*(mtot)*(c**-2))
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





def adot_gas_func(m1, m2, a, e):
    q=min(m1/m2, m2/m1)
    
    mdot_m=100*eddington(m1+m2)/(m1+m2)
    df=adot_both
    # Get available eb values (strip 'eb_' prefix and convert to float)
    eb_vals = np.array([float(col.split('_')[1]) for col in df.columns])
    qb_vals = df.index.values
    
    # Find nearest values
    nearest_qb = qb_vals[np.abs(qb_vals - q).argmin()]
    nearest_eb = eb_vals[np.abs(eb_vals - e).argmin()]
    
    adot_a = df.loc[nearest_qb, f'eb_{nearest_eb:.1f}']
    if a<=5*rg:
        a=5*rg
    return(adot_a*a*mdot_m)
    
def edot_gas_func(m1, m2,a,e):
    q=min(m1/m2, m2/m1)

    mdot_m=100*eddington(m1+m2)/(m1+m2)
    df=edot_both
    # Get available eb values (strip 'eb_' prefix and convert to float)
    eb_vals = np.array([float(col.split('_')[1]) for col in df.columns])
    qb_vals = df.index.values
    
    # Find nearest values
    nearest_qb = qb_vals[np.abs(qb_vals - q).argmin()]
    nearest_eb = eb_vals[np.abs(eb_vals - e).argmin()]
    
    edot_e = df.loc[nearest_qb, f'eb_{nearest_eb:.1f}']
    return(edot_e*mdot_m)

def edot_both_func(m1, m2, a,e):
    print(f'''this is the edot val ! {edot_gw_func(m1, m2, a,e)+edot_gas_func(m1, m2, a,e)}''')
    return 1*(edot_gw_func(m1, m2, a,e)+edot_gas_func(m1, m2, a,e))#this is beign done to speed up calculations

def adot_both_func(m1, m2, a,e):
    return 1*(adot_gw_func(m1, m2, a,e)+adot_gas_func(m1, m2, a,e))

def pos_from_q_e(q,e):#from barycentric coords
    x_0=-1*(1 - (1/(1+q)))*(1+e)
    x_1=(1/(1+q))*(1+e)
   
    y_0=0
    y_1=0
    return([x_0, y_0, x_1, y_1])
def m_from_q(q):
    if q>1:
        print(f'''this is q {q}''')
        raise ValueError('q must be less than 1')
        
    m1=1/(1+q)
    m2=1-m1
    return(m1, m2)

# Binary total mass and component masses
M_total = 10**7 * msol  # Total mass in grams
rg=rs_func(M_total)



e_0, sigma_e = 0.5, 0.45  # Eccentricity
a_0, sigma_a = 500*rg, 100*rg  # Semi-major axis in rg

# Time span for integration (in s)
fid_a=1000*rg
t_span = (0, 1e5*(2*math.pi*np.sqrt(((fid_a)**3)/(G*M_total))))  # Evolve over 

# Number of binaries to simulate
n_binaries = int(100)


def qdot_func(m1, m2, a, e_init):
    """Rate of change of mass ratio, dependent on q and e."""
    data=np.load('/Users/stanislavdelaurentiis/roman_work/qdot_data_magda.npy')
    other_inds = np.where(data[0]<0)[0]
    data[0][other_inds]=0
    intermediate_inds =np.where(data[0]>0)[0]
    data[0][intermediate_inds]=-1*data[0][intermediate_inds]
    
    
    mdot_m=100*(eddington(m1+m2)/(m1+m2))
    data=data*mdot_m
    ecclist=np.array([0.0,0.1, 0.2,0.3,0.4,0.5,0.6,0.8])
    qblist=np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    
    q_init=np.minimum(m2/m1, m1/m2)
    q=round(q_init, 1)
    e=round(e_init, 1)
    if e==0.7:
        if np.abs(0.8-e_init)<np.abs(0.6-e_init):
            e=0.8
        else:
            e=0.6
    if e>0.8:
        e=0.8
    if e<0:
        e=0
    if q>=1:
        #print('yeah')
        q=1
    if q<0.1:
        q=0.1
    qbind=np.where(qblist==q)[0][0]
    ebind=np.where(ecclist==e)[0][0]
    print(f'''this is the qdot {data[9-qbind][ebind] }''')
    return 1*(data[9-qbind][ebind] )


# ODE system for each binary
def evolve_system(t, y):
    a, e, q = y
    if q<0.1:
        q=0.1
    if q>=1:
        #print('yeah')
        q=1
    if e>=0.8:
        e=0.8
    if e<=0:
        e=0
    if a<=500*rg:
        a=500*rg

    mprimary, msecondary=m_from_q(q)
    mprimary=mprimary*M_total
    msecondary=msecondary*M_total
    da = adot_both_func(mprimary, msecondary, a, e)
    de = edot_both_func(mprimary, msecondary, a, e)
    dq = qdot_func(mprimary, msecondary, a, e)
    print(f'''this is t {np.log10(t/(2*math.pi*np.sqrt(((fid_a)**3)/(G*M_total))))}''')
    print(f'''this is og a {a} e {e} q {q}''')
    print(f'''this is delta a {da} delta e {de} delta q {dq}''')
    return [da, de, dq]


counts_q=counts_q/np.sum(counts_q)
# Initialize binary population


initial_a = np.clip(np.random.normal(a_0, sigma_a, n_binaries), 10*rg, float('inf'))
initial_e = np.clip(np.random.normal(e_0, sigma_e, n_binaries), 0,1)


initial_a = np.full((n_binaries), fid_a)
initial_e = np.linspace(0,0.8,n_binaries)
initial_q = np.random.choice(np.arange(0.1,1.01,0.1), size=n_binaries, p=counts_q)

#=============================================================================
initial_a = np.random.uniform(400*rg, 450*rg, n_binaries)
initial_e = np.random.uniform(0.4, 0.5, n_binaries)
initial_q = np.random.choice(np.arange(0.1,1.01,0.1), size=n_binaries, p=counts_q)
#=============================================================================

#=============================================================================
initial_a = np.full((70), fid_a)
initial_e = np.tile(np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]), 10)
initial_q = np.repeat(np.arange(0.1, 1.01, 0.1), 7)

n_add_binaries= n_binaries-70
n_add_binaries=50
final_a=np.concatenate((initial_a,  np.full((n_add_binaries), fid_a)), axis=0)
final_e=np.concatenate((initial_e, np.random.uniform(0.4, 0.5, n_add_binaries)), axis=0)
final_q=np.concatenate((initial_q, np.random.choice(np.arange(0.1,1.01,0.1), size=n_add_binaries, p=counts_q)), axis=0)
#initial_q = np.random.choice(np.arange(0.1,1.01,0.1), size=n_binaries, p=counts_q)
#initial_q = np.linspace(0.1,1,n_binaries)
#initial_q=np.full((n_binaries), 1)
#=============================================================================

n_binaries=4
final_a=np.full((n_binaries), fid_a)
final_e=np.linspace(0,0.8,n_binaries)
final_e=np.array([0.2, 0.3, 0.8, 0.8])
final_q=np.array([1,1,1, 0.9])

tsteps=int(5e3)
# Storage for results
results_a = np.zeros((len(final_q), tsteps))
results_e = np.zeros((len(final_q), tsteps))
results_q = np.zeros((len(final_q), tsteps))


results_a=[]
results_q=[]
results_e=[]
# Time points to store results
times = np.linspace(t_span[0], t_span[1], tsteps)


# Evolve each binary
for i in range(len(final_q)):
    print(f'''this the i {i} binary with vals a={final_a[i]/rg}, e={final_e[i]}, q={final_q[i]}''')
    y0 = [final_a[i], final_e[i], final_q[i]]
    sol = solve_ivp(evolve_system, t_span, y0, t_eval=times, method='LSODA')#, rtol=1e-6)#,max_step=1e-10*t_span[1])#, rtol=1e-6)
    a_temp, e_temp, q_temp = sol.y
    #results_a[i] = a_temp
    #results_e[i] = e_temp
    #results_q[i] = q_temp
    
    results_a.append(a_temp)
    results_q.append(q_temp)
    results_e.append(e_temp)

# Plotting results for a single binary (example)

results_a=np.array(results_a)
results_q=np.array(results_q)
results_e=np.array(results_e)

results_a=results_a/rg
times=times/(2*math.pi*np.sqrt(((fid_a)**3)/(G*M_total)))



fig, ax=plt.subplots(1,3)
fig.set_figheight(10)
fig.set_figwidth(10)
ax[0].plot(times, results_a[0])
ax[0].set_xlabel('Time (fid orb)')
ax[0].set_ylabel('Semi-major axis (AU)')
ax[0].set_title('Evolution of a')


ax[1].plot(times, results_e[0])
ax[1].set_xlabel('Time (fid orb)')
ax[1].set_ylabel('Eccentricity')
ax[1].set_title('Evolution of e')


ax[2].plot(times, results_q[0])
ax[2].set_xlabel('Time (fid orb)')
ax[2].set_ylabel('Mass ratio q')
ax[2].set_title('Evolution of q')

fig.tight_layout()
#plt.show()
fig.savefig('asfjlk_new.pdf')
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib



colormap = plt.cm.nipy_spectral
colors = [colormap(i) for i in np.linspace(0, 1,len(times))]
fig, ax=plt.subplots(1,3)
fig.set_figheight(10)
fig.set_figwidth(20)
plottingsteps=100
for i in range(plottingsteps):
    
    scale=tsteps/plottingsteps
    ax[0].plot(np.sort(results_e[:, int(i*scale)]), 
                  [x for _, x in sorted(zip(results_e[:, int(i*scale)], results_q[:, int(i*scale)]), key=lambda pair: pair[0])]
                  , color=colors[int(i*scale)], alpha=0.5)
   
    
    ax[1].plot(np.sort(results_a[:, int(i*scale)]), 
               [x for _, x in sorted(zip(results_a[:, int(i*scale)], results_q[:, int(i*scale)]), key=lambda pair: pair[0])]
               , color=colors[int(i*scale)], alpha=0.5)

    
    
    ax[2].plot(np.sort(results_q[:, int(i*scale)]), 
               [x for _, x in sorted(zip(results_q[:, int(i*scale)], results_e[:, int(i*scale)]), key=lambda pair: pair[0])],
               color=colors[int(i*scale)], alpha=0.5)

    
ax[0].set_xlabel('e')
ax[0].set_ylabel('q')

ax[1].set_xlabel('a')
ax[1].set_ylabel('q')

ax[2].set_xlabel('q')
ax[2].set_ylabel('e')   
divider = make_axes_locatable(ax[2])
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar= plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=times[0], vmax=times[-1]), cmap='nipy_spectral'), cax=cax)
cbar.set_label('time')
fig.tight_layout()
fig.savefig('new_evol_yass.png')


fig, ax=plt.subplots()
ax.scatter(initial_a, initial_q)
fig.savefig('new_evol_full.png')


# =============================================================================
# fig, ax=plt.subplots()
# ax.plot(times, results_q[28])
# ax.set_xlabel('Time [orbits]')
# ax.set_ylabel('q')
# fig.suptitle(f'''e_0 = {results_e[28][0]: .2f}, q_0 = {results_q[28][0]}''')
# fig.savefig('new_evol.pdf')
# =============================================================================



fig, ax =plt.subplots(2,1)
fig.set_figheight(7)
fig.set_figwidth(5)

print(results_e)
print(np.shape(results_e))



sample_e= results_e[0].flatten()
sample_a= results_a[0].flatten()
sample_q1= results_q[0].flatten()
ax[0].plot(times, sample_e, color='blue', label=r'$q_{b,0}=1 \, , e_{b,0}=0.2$')
ax[1].plot(times, sample_q1, color='blue')
#ax[2].plot(times, sample_a, color='blue')

sample_e= results_e[1].flatten()
sample_a= results_a[1].flatten()
sample_q2= results_q[1].flatten()
ax[0].plot(times, sample_e, color='red', label=r'$q_{b,0}=1 \, , e_{b,0}=0.3$')
ax[1].plot(times, sample_q2, color='red')
#ax[2].plot(times, sample_a, color='red')


# =============================================================================
# sample_e= results_e[2].flatten()
# sample_a= results_a[2].flatten()
# sample_q= results_q[2].flatten()
# ax[0].plot(times, sample_e, color='green', label=r'$q_{b,0}=1 \, , e_{b,0}=0.8$')
# ax[1].plot(times, sample_q, color='green')
# ax[2].plot(times, sample_a, color='green')
# 
# sample_e_prime= results_e[3].flatten()
# sample_a_prime= results_a[3].flatten()
# sample_q_prime= results_q[3].flatten()
# ax[0].plot(times, sample_e_prime, color='purple', label=r'$q_{b,0}=0.9 \, , e_{b,0}=0.8$')
# ax[1].plot(times, sample_q_prime, color='purple')
# ax[2].plot(times, sample_a_prime, color='purple')
# =============================================================================



ax[0].set_ylabel(r'$e(t)$')
ax[1].set_ylabel(r'$q(t)$')
#ax[2].set_ylabel(r'$a(t) \, [R_S] $')
ax[-1].set_xlabel(r'$\tau$')

ax[0].legend()
#ax[2].plot(times, sample_q)
fig.tight_layout()
plt.savefig('evolution_plots.pdf')

#print()

print(f'''this is the final for one of them {sample_q1[-1]}''')
print(f'''this is the final for one of them {sample_q2[-1]}''')

sfd
#outcomes is the values you are choosing for, in this case it is q
sample_bbhs = np.random


# ok now we want to build a tool to actually evolve the population 
#given its 10% eddington (which i dont really beleive), but fuck it






