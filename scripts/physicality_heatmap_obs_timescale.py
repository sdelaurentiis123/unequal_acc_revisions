#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 18:36:53 2023

@author: stanislavdelaurentiis
"""
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
import scipy
from scipy import optimize
c=2.99792458e8
G=6.6725985e-11
msun=1.989e30



def t_visc(r,mdot, sigma):
    r0=r/2
    try:
        val = 2*math.pi*((r0**2)*sigma)
        val=val/mdot
        
    except ZeroDivisionError:
        val=float('inf')
    return(
        val
        )

eadotdict={0:1.76,
           0.1:-0.95, 
           0.2:-1.31, 
           0.3:-4.79, 
           0.4:-6.1,
           0.5:0.6, 
           0.6:0.38,
           0.8:-2.74}

eadotdict={0:-4.15,
           0.1:-7.19, 
           0.2:-7.54, 
           0.3:-10.59, 
           0.4:-10.46,
           0.5:-2.27, 
           0.6:-1.39,
           0.8:-2.18}




def mdot(sigma, nu):
    return(
        3*math.pi*sigma*nu
        )
def mdot_edd(mtot):
    ledd=1.26e38*(mtot/msun)#this is in cgs (ie ergs/s)
    ledd=ledd*1e-7 #now in joules/s
    return(ledd/(0.1*(c**2)))


def torb_kep_func(a,mtotal):
    top=2*math.pi
    bot=np.sqrt(G*mtotal*(a**-3))
    val=top/bot
    return(val)

def t_visc_alt(e, mdot, mtot):
    adot_a=np.interp(e, list(eadotdict.keys()), list(eadotdict.values()))
    mdot=mdot*mdot_edd(mtot)
    val=np.abs(adot_a)*(mdot/mtot)
    val=1/val
    return(val)

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



def GR_ORB(m1, m2, a, e):
    a=np.array(list(a))
    e=np.array(list(e))
    if len(a)==1 and len(e)!=1:
        a=np.full(len(e),a[0])
    if len(e)==1 and len(a)!=1:
        e=np.full(len(a),e[0])

    def epsilon_finder(a_in, mtot):
        #print('epsilon_finder', G, mtot, c)
        return(
            G*mtot*(c**-2)*(a_in**-1)
            )
    
    def j_finder(e_r):
        return(
            1-(e_r**2)
            )
    
    def eta_finder(m1,m2):
        return(
        (m1*m2)/((m1+m2)**2)
        )
    
    
    
    M=m1+m2
    
    epsilon=epsilon_finder(a, M)
    j=j_finder(e)
    eta=eta_finder(m1,m2)
    
    def nfunc(epsilon, eta, j, mtot):
        #print('nfunc', epsilon, eta, j, mtot)
        return(
                ((epsilon**1.5)*(c**3)*((G*mtot)**-1))*(
                    1
                    +((epsilon/8)*(-15+eta))
                    +((epsilon**2)/128)*(
                        555
                        +(30*eta)
                        +(11*(eta**2))
                        +(192*(-5+(2*eta))*(j**-0.5))
                        )
                    )
            )
    
    def Phifunc(epsilon, eta, j):
        #print('yo, its PHI')
        return(
            2*math.pi*(
                1
                +((3*epsilon)/j)
                +((epsilon**2)/4)*(
                    ((3/j)*(-5 + (2*eta)))
                    -((15/(j**2))*(-7 + (2*eta)))
                    )
                )
            )
    def torb_kep_func(a,mtotal):
        top=2*math.pi
        bot=np.sqrt(G*mtotal*(a**-3))
        val=top/bot
        return(val)
    
    torb_kep=torb_kep_func(a,M)
    n=nfunc(epsilon, eta, j, M)
    #print(n)
    Phi=Phifunc(epsilon, eta, j)
    #print(Phi)
    torb_prec=np.abs((2*math.pi)/n)
    #print('torb_prec',torb_prec)
    prec_angle_deg=(Phi-(2*math.pi))*(180/math.pi)
    tprec_pi=(360/prec_angle_deg)*torb_prec*0.5
    tprec_pi_kep_orbs=(360/prec_angle_deg)*(torb_prec/torb_kep)*0.5
    return(tprec_pi, Phi, tprec_pi_kep_orbs, torb_prec)


def adot_func(m1,m2,a,e):
    a=np.array(list(a))
    e=np.array(list(e))
    if len(a)==1 and len(e)!=1:
        a=np.full(len(e),a[0])
    if len(e)==1 and len(a)!=1:
        e=np.full(len(a),e[0])
        
    M=m1+m2
    q=m2/m1
    if q>1:
        raise Exception('m1 has to be < m2')
    top=-64*(G**3)*(M**3)*q*peters_f_e(e)
    bot=5*(c**5)*(a**3)*( (1+q)**2 )
    val=top/bot
    return(val)

def edot_func(m1,m2,a,e):
    a=np.array(list(a))
    e=np.array(list(e))
    if len(a)==1 and len(e)!=1:
        a=np.full(len(e),a[0])
    if len(e)==1 and len(a)!=1:
        e=np.full(len(a),e[0])
        
    M=m1+m2
    q=m2/m1
    if q>1:
        raise Exception('m1 has to be < m2')
        
        
    top=-1*e*304*(G**3)*(M**3)*q*( 1+ ((121/304)*(e**2)) )
    bot=15*(c**5)*(a**4)*( (1-(e**2))**2.5 )*( (1+q)**2)
    
    val=top/bot
    return(val)

def gwtscale(m1,m2,a,e):
    return(a/adot_func(m1,m2,a,e))
    


def haiman09_30b(alpha=0.3, mdot=0.1, mass=1e7*msun, betagw_v=0.1):
    alpha=alpha/0.3
    mdot=mdot/0.1
    mass=mass/(1e7*msun)
    return(
        1e3*(
        0.222*(alpha**(-4/13))*(mdot**(-2/13))*(mass**(1/13))*(betagw_v**(5/13))
        )
        )

def haiman09_29b(alpha=0.3, mdot=0.1, mass=1e7*msun, betagw_s=1):
    alpha=alpha/0.3
    mdot=mdot/0.1
    mass=mass/(1e7*msun)
    return(
        1e3*(
        0.470*(alpha**(-4/25))*(mdot**(-1/5))*(mass**(-2/25))*(betagw_s**(8/25))
        )
        )

def haiman09_30b_ecc(e=0, alpha=0.1, mdot=10, mass=1e7*msun, betagw_v=0.1):
    alpha=alpha/0.3
    mdot=mdot/0.1
    mass=mass/(1e7*msun)
    return(
        1e3*(
        0.222*(alpha**(-4/13))*(mdot**(-2/13))*(mass**(1/13))*(betagw_v**(5/13))
        )
        *(peters_f_e(e)**(5/13))
        )

def haiman09_30a_ecc(e=0, alpha=0.3, mdot=1, mass=1e7*msun, betagw_v=1):
    alpha=alpha/0.3
    mdot=mdot
    mass=mass/(1e7*msun)
    return(
        1e3*(
        0.202*(alpha**(-2))*(mdot**(-4))*(betagw_v**(2))
        )
        *(peters_f_e(e)**(2))
        )

def haiman09_29b_ecc(e=0, alpha=0.3, mdot=0.1, mass=1e7*msun, betagw_s=1):
    alpha=alpha/0.3
    mdot=mdot/0.1
    mass=mass/(1e7*msun)
    return(
        1e3*(
        0.470*(alpha**(-4/25))*(mdot**(-1/5))*(mass**(-2/25))*(betagw_s**(8/25))
        )
        *(peters_f_e(e)**(8/25))
        )







#a_in=2.8710694592451814e-05*(2/3)*(pc)
#e_in=0.45

def rg_func(m1,m2):
       return( 2*G*(m1+m2)*(c**-2) )



def torb_kep_func(a,mtotal):
    top=2*math.pi
    bot=np.sqrt(G*mtotal*(a**-3))
    val=top/bot
    return(val)


#print(rootvals0.x)

#quit

#print('0','log', np.log10(rootvals0.x), 'si')
#print('0','log', np.log10(rootvals0.x*(1e4)), 'cgs')
#quit

#def root1(x):
#    if x<=0:
#        return(float('inf'))
#    return(  np.abs (mdot(x, rootvals0.x) -(1e-3*edd)) )
    
#rootvals1=scipy.optimize.minimize_scalar(root1, options={'xtol':1e-20})
#print('log', np.log10(rootvals1.x), 'si')
#print('log', np.log10(rootvals1.x*0.1), 'cgs')
#quit


fig, ax=plt.subplots(3,2)
fig.set_figheight(10)
fig.set_figwidth(10)
for axs in ax.flatten():
    axs.tick_params(bottom=True, top=True, left=True, right=False, labelleft=True, labelbottom=False)



massbinarylist=[0.5e7*msun, 0.5e6*msun,0.5e5*msun]
#zlist=[1,3]
zlist=[1,10]
for j in range(len(zlist)):
    for i in range(len(massbinarylist)):
        

        z=zlist[j]
        m1=massbinarylist[i]
        m2=massbinarylist[i]
        rg=rg_func(m1,m2)
        
        
        alist=np.arange(5,1300.5,1)
        alist=alist*rg
        alist=np.flip(alist)
        
        elist=np.arange(0.001,0.92,0.002)
        
        
        matrixtorb=np.zeros((len(alist), len(elist)))#a is rows, e is columns (with the lowest ecc being towards the left, 
                                                       #and the highest a being at the top)
        matrixtpeters=np.zeros((len(alist), len(elist)))#a is rows, e is columns
        matrixtboth=np.zeros((len(alist), len(elist)))#a is rows, e is columns #tpeters divded by tprec
        
        matrixdelta_a=np.zeros((len(alist), len(elist)))#a is rows, e is columns 
        matrixdelta_e=np.zeros((len(alist), len(elist)))#a is rows, e is columns
        
        
        
        #these are lists to be populated with coordinate values that leave tprec_signal(system years) <10
        #and have peters to signal ratios of greater than 30

        dictphysical_obs={}
        dictphysicaldec_ecc_alt1={}
        dictphysicaldec_ecc_alt2={}



        for eiterr in range(len(elist)):
            e=[]
            e.append(elist[eiterr])
            #print(elist[i])
            torb_seconds=torb_kep_func(alist, m1+m2)*(1+z)
            #tprec_kep_orbs=GR_ORB(m1,m2, alist, e)[2]
            #torbgr=GR_ORB(m1,m2, alist, e)[3]*(1+z)
            tpeters_seconds=t_p_og(m1,m2, alist, e)*(1+z)
            
            adot=adot_func(m1,m2, alist,e)
            edot=edot_func(m1,m2, alist,e)
            
            
            #print(GR_ORB(m1,m2, alist, e))
            #print(t_p_og(m1,m2, alist, e))
            
            matrixtorb[:,eiterr]=torb_seconds
            matrixtpeters[:,eiterr]=tpeters_seconds
            #matrixtboth[:,eiterr]=tpeters_seconds/tprec_seconds
            
            
            matrixdelta_a[:,eiterr]=(adot*300*10*torb_seconds)/rg #has to be divided by rs since everything here is in rs
            matrixdelta_e[:,eiterr]=edot*300*10*torb_seconds
            
            indexlist_obs=np.where(  (np.array((300*torb_seconds)/(3600*24*365))<10) &((np.array(tpeters_seconds)/(3600*24*365))>1e2))[0]
            #indexlistdec_ecc_alt1=np.where( (np.array(tpeters_seconds/tprec_seconds)>100) & (np.array(tprec_seconds/(3600*24*365))<2) &((np.array(tpeters_seconds)/(3600*24*365))>5e2))[0]
            #indexlistdec_ecc_alt2=np.where( (np.array(tpeters_seconds/tprec_seconds)>100) & (np.array(tprec_seconds/(3600*24*365))<2) &((np.array(tpeters_seconds)/(3600*24*365))>1e3))[0]
            
            if len(indexlist_obs)>0:
                dictphysical_obs[elist[eiterr]]=alist[indexlist_obs]/rg
                
            #if len(indexlistdec_ecc_alt1)>0:
                #dictphysicaldec_ecc_alt1[elist[eiterr]]=alist[indexlistdec_ecc_alt1]/rg
                
            #if len(indexlistdec_ecc_alt2)>0:
                #dictphysicaldec_ecc_alt2[elist[eiterr]]=alist[indexlistdec_ecc_alt2]/rg
                
            

        
        xticksmap=[]
        xticklabelsmap=[]
        numdec=2
        stepsize=0.1
        for iterr in np.arange(0, elist[-1]+(0.002*stepsize), stepsize):
            if float(format(iterr,'.'+str(numdec)+'f'))==0:
                continue
                xticksmap.append(0)
                xticklabelsmap.append(format(0,'.'+str(numdec)+'f'))
                
            xticksmap.append(iterr)
            xticklabelsmap.append(format(iterr,'.'+str(numdec)+'f'))
        
        yticksmap=[]
        yticklabelsmap=[]
        stepsize=100
        numdec=0
        for iterr in np.arange(alist[-1],alist[0]+(0.5*stepsize*rg), stepsize*rg):
            if float(format(iterr,'.'+str(numdec)+'f'))==0:
                yticksmap.append(0)
                yticklabelsmap.append(format(0,'.'+str(numdec)+'f'))
                continue
            yticksmap.append(iterr/rg)
            yticklabelsmap.append(format(iterr/rg,'.'+str(numdec)+'f'))
        
            
        
        
        
        cm = ax[i][j].imshow(
                np.log10((300*matrixtorb)/(3600*24*365)),
                origin="upper",
                cmap="jet",
                aspect='auto',
                extent=(elist[0],elist[-1],alist[-1]/rg,alist[0]/rg),
                interpolation='None',
                vmin=-2 + 0.1,
                vmax=2 - 0.1
                #vmax=4
                
            )
        print('this is torb')
        print(m1/msun, m2/msun, alist, alist/rg, z)
        print(torb_kep_func(m1+m2, alist)*(1+z))
        #print(matrixtorb/(3600*24*365))
       
        if j==0:
            if i==0:
                ax[i][j].set_ylabel(r'$a$ $[R_S]$')#' $\left(  M_{\rm{Bin}} = 10^{7} M_{\odot}  \right)$')
                
            if i==1:
                ax[i][j].set_ylabel(r'$a$ $[R_S]$')#' $\left(  M_{\rm{Bin}} = 10^{6} M_{\odot}  \right)$')
            if i==2:
                ax[i][j].set_ylabel(r'$a$ $[R_S]$')#' $\left(  M_{\rm{Bin}} = 10^{5} M_{\odot}  \right)$')
        if j==1:
            divider = make_axes_locatable(ax[i][j])
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cbar1= plt.colorbar(cm, cax=cax)
            if i==0:
                cbar1.set_label(label=r'$log\left( \tau_{\rm{f}} \  [\rm{yrs}]  \right)$  ')
            if i==1:
                cbar1.set_label(label=r'$log\left( \tau_{\rm{f}} \  [\rm{yrs}] \right)$')#'  $\left(  M_{\rm{Bin}} = 10^{6} M_{\odot}  \right)$')
            if i==2:
                cbar1.set_label(label=r'$log\left( \tau_{\rm{f}} \  [\rm{yrs}] \right)$ ')#' $\left(  M_{\rm{Bin}} = 10^{5} M_{\odot}  \right)$')
            ax[i][j].tick_params(labelleft=False)
        
        
        if i==2:
            ax[i][j].tick_params(labelbottom=True)
            ax[i][j].set_xlabel(r'$e$')
        
        
        
        
        
        
        
        
        yspace=int(0.075*len(alist))
        xspace=int(0.075*len(elist))
        
        #ax[2].arrow(0.1,50,0.1,1,color='green')
        
                        
        
        ephysical_obs=list(dictphysical_obs.keys())
        #ephysicaldec_ecc_alt1=list(dictphysicaldec_ecc_alt1.keys())
        #ephysicaldec_ecc_alt2=list(dictphysicaldec_ecc_alt2.keys())
                        
        
        
        plote=[]
        plotmaxa=[]
        plotmina=[]
        for iterr in range(len(ephysical_obs)):   
            plote.append(ephysical_obs[iterr])
            plotmaxa.append(max(np.array(dictphysical_obs[ephysical_obs[iterr]])))
            plotmina.append(min(np.array(dictphysical_obs[ephysical_obs[iterr]])))
        
        ax[i][j].plot(plote, plotmaxa, color='black', lw=2, alpha=0.5, ls='-')#, label=r'$T_{\rm{}}>10^{2}$ yrs')
        ax[i][j].plot(plote, plotmina, color='black', lw=2, alpha=0.5, ls='-')
        
# =============================================================================
#         plote=[]
#         plotmaxa=[]
#         plotmina=[]
#         for iterr in range(len(ephysicaldec_ecc_alt1)):   
#             plote.append(ephysicaldec_ecc_alt1[iterr])
#             plotmaxa.append(max(np.array(dictphysicaldec_ecc_alt1[ephysicaldec_ecc_alt1[iterr]])))
#             plotmina.append(min(np.array(dictphysicaldec_ecc_alt1[ephysicaldec_ecc_alt1[iterr]])))
#         
#         ax[i][j].plot(plote, plotmaxa, color='black', lw=2, alpha=0.5, ls='--', label=r'$T_{\rm{GW}}> 5 \cdot 10^{2}$ yrs')
#         ax[i][j].plot(plote, plotmina, color='black', lw=2, alpha=0.5, ls='--')
#         
#         plote=[]
#         plotmaxa=[]
#         plotmina=[]
#         for iterr in range(len(ephysicaldec_ecc_alt2)):   
#             plote.append(ephysicaldec_ecc_alt2[iterr])
#             plotmaxa.append(max(np.array(dictphysicaldec_ecc_alt2[ephysicaldec_ecc_alt2[iterr]])))
#             plotmina.append(min(np.array(dictphysicaldec_ecc_alt2[ephysicaldec_ecc_alt2[iterr]])))
#         
#         ax[i][j].plot(plote, plotmaxa, color='black', lw=2, alpha=0.5, ls='dotted', label=r'$T_{\rm{GW}}>10^{3}$ yrs')
#         ax[i][j].plot(plote, plotmina, color='black', lw=2, alpha=0.5, ls='dotted')
#         
#         
# =============================================================================
        
        
        for iterri in range(len(elist)):
            if iterri%xspace==0:
                for iterrj in range(len(alist)):
                    if iterrj%yspace==0:
                        ax[i][j].arrow(x=elist[iterri],y=alist[iterrj]/rg, 
                                           dx=matrixdelta_e[iterrj,iterri], 
                                           dy=matrixdelta_a[iterrj,iterri], 
                                           color='darkgray',
                                           length_includes_head=True,
                                           head_starts_at_zero=True,
                                           head_width=0.003,head_length=0.003, width=0.0001
                                           )
        ax[i][j].set_ylim(alist[-1]/rg, alist[0]/rg)
        ax[i][j].set_xlim(elist[0], elist[-1])
        
        
        
        ax[i][j].set_xticks(xticksmap)
        ax[i][j].set_xticklabels(xticklabelsmap)
        ax[i][j].set_yticks(yticksmap)
        ax[i][j].set_yticklabels(yticklabelsmap)
        
        
        #ax[i][j].axvline(0.25, color='white', ls='dashdot')
        if i==0:
            ax[i][j].tick_params(top=False)
            #ax[i][j].vlines(x=0.25,  color='black', ls='-', ymin=60, ymax=150)


    


#ax[0].set_ylim(0,300)

ax[0][0].set_title(r'$Z=1$')
ax[0][1].set_title(r'$Z=10$')

#ax[0][1].legend(loc='upper right', framealpha=1)

ax[0][0].annotate(r'$  M_{\rm{bin}} = 10^{7} M_{\odot} $', xy=(0.3,1200), color='white', zorder=float('inf'),size=15)
ax[1][0].annotate(r'$  M_{\rm{bin}} = 10^{6} M_{\odot} $', xy=(0.3,1200), color='white', zorder=float('inf'),size=15)
ax[2][0].annotate(r'$  M_{\rm{bin}} = 10^{5} M_{\odot} $', xy=(0.3,1200), color='white', zorder=float('inf'),size=15)
#ax[0][0].annotate(r'$  M_{\rm{bin}} = 10^{7} M_{\odot} $', xy=(0.3,1150), color='white', zorder=float('inf'),size=20)


fig.tight_layout()
fig.subplots_adjust(hspace=0.0)
fig.subplots_adjust(wspace=0.0)
#
fig.savefig('new_obs_heatmap_new_big.pdf')
    


