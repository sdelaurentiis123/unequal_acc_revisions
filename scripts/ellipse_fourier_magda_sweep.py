#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:13:36 2024

@author: stanislavdelaurentiis
"""

import pickle
import matplotlib.pyplot as plt
import math
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable


f=open('saving_peaks.txt', 'w+')
f.close()
ecclist=[0.0,0.1, 0.2,0.3,0.4,0.5,0.6,0.8]
qblist=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

e_master_save=[]
a_master_save=[]
for ebind in range(len(ecclist)):
    for qbind in range(len(qblist)):
        try:
          picklefile = open('/Users/stanislavdelaurentiis/roman_work/'+'qb_'+str(qblist[qbind])+'_e_'+str(ecclist[ebind])+'_ellipses_0.3meanmaxsig_1_1000', 'rb')  
        except FileNotFoundError:
          continue
        
        picklefile = open('/Users/stanislavdelaurentiis/roman_work/'+'qb_'+str(qblist[qbind])+'_e_'+str(ecclist[ebind])+'_ellipses_0.3meanmaxsig_1_1000', 'rb')  
        data = pickle.load(picklefile)
        
        xcenter=np.array(data['x1'])
        ycenter=np.array(data['y1'])
        a=np.array(data['a1'])
        b=np.array(data['b1'])
        ecc=np.array(data['e1'])
        theta=np.array(data['theta1'])
        #theta[np.where(theta>=0.75*math.pi)[0]]=(math.pi)-theta[np.where(theta>=0.75*math.pi)[0]]
        
        xcom=np.array(data['x_com'])
        ycom=np.array(data['y_com'])
        
        #so the foci are along the semi-major axis, we know the angle for that
        #so what you do is you take center of the ellipse and then you take a*e 
        #(which is foucs length) and then you mulitply it against sin(theta_c) and cos(theta_c) and there you get deltay and deltax respectively
        focallength=a*ecc
        f_xpos=xcenter+focallength*np.cos(theta)
        f_ypos=ycenter+focallength*np.sin(theta)
        f_xneg=xcenter-focallength*np.cos(theta)
        f_yneg=ycenter-focallength*np.sin(theta)
        
        time=np.array(data['filename1']).astype('float')
        time=time
        fig, ax=plt.subplots(2,1)
        fig.set_figheight(20)
        fig.set_figwidth(30)
        ax[0].plot(time, ecc, marker='x', color='blue')
        ax[1].plot(time, theta/math.pi, marker='x', color='blue')
        ax[0].set_ylabel(r'e')
        ax[1].set_ylabel(r'$\theta_{\rm{C}}$')
        ax[1].set_xlabel(r'Time/10')
        fig.tight_layout()
        #fig.savefig('e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'ellipses_5_22.pdf')
        plt.close(fig)
        
        fig, ax=plt.subplots(4,1)
        fig.set_figheight(20)
        fig.set_figwidth(30)
        ax[0].plot(time, np.abs(f_xpos), marker='x', color='blue')
        ax[0].plot(time, f_ypos, marker='x', color='red')
        ax[0].plot(time, np.sqrt(f_xpos**2 + f_ypos**2) , marker='x', color='green')
        
        ax[1].plot(time, np.abs(f_xneg), marker='x', color='blue')
        ax[1].plot(time, f_yneg, marker='x', color='red')
        ax[1].plot(time, np.sqrt(f_xneg**2 + f_yneg**2) , marker='x', color='green')
        
        ax[2].plot(time, np.minimum(np.sqrt(f_xpos**2 + f_ypos**2), np.sqrt(f_xneg**2 + f_yneg**2)), marker='x', color='green')
        
        ax[3].plot(time, xcenter, marker='x', color='blue')
        ax[3].plot(time, ycenter, marker='x', color='red')
        ax[3].plot(time, np.sqrt(xcenter**2 + ycenter**2) , marker='x', color='green')
        
        ax[0].set_ylabel(r'pos foc.')
        ax[1].set_ylabel(r'neg foc.')
        ax[2].set_ylabel(r'min foc.')
        ax[3].set_ylabel(r'center.')
        #ax[1].set_ylabel(r'$\theta_{\rm{C}}$')
        #ax[1].set_xlabel(r'Time/10')
        fig.tight_layout()
        #fig.savefig('e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'ellipses_focallength_final.pdf')
        plt.close(fig)
    
        
        
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
        a1=0.5*(rmin+rmax)
        a1=a1.flatten()
        e_1=1-(rmin/a)
        ex_1=e_1*np.cos(am1)
        ey_1=e_1*np.sin(am1)
        
        e_1=e_1.flatten()
        ex_1=ex_1.flatten()
        ey_1=ey_1.flatten()
        
        
        #this is for m=2
        amplitude=(rm2/N)
        baseline=rm0/N
        rmax=baseline+amplitude
        rmin=baseline-amplitude
        a2=rmax.flatten()
        b2=rmin.flatten()
        e_2=np.sqrt(1-b**2/a**2)
        ex_2=e_2*np.cos(am2).flatten()
        ey_2=e_2*np.sin(am2).flatten()
        
        e_2=e_2.flatten()
        ex_2=ex_2.flatten()
        ey_2=ey_2.flatten()
        
        fig, ax=plt.subplots(2,1)
        fig.set_figheight(20)
        fig.set_figwidth(30)
        ax[0].plot(time, rm1, color='blue', marker='x', label=r'$m=1$')
        ax[0].plot(time, rm2, color='red', marker='x', label=r'$m=2$')
        
        ax[1].plot(time, am1, color='blue', marker='x', label=r'$m=1$')
        ax[1].plot(time, am2, color='red', marker='x', label=r'$m=2$')
        ax[0].legend()
        ax[0].set_ylabel(r'mag')
        ax[1].set_ylabel(r'phase')
        ax[1].set_xlabel(r'Time/10')
        fig.tight_layout()
        #fig.savefig('e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'final_fourieronly.pdf')
        plt.close(fig)
        
        fig, ax=plt.subplots(9,1)
        fig.set_figheight(20)
        fig.set_figwidth(30)
        startindex=0
        ax[0].plot(time[startindex:], ecc[startindex:], marker='.', color='black')
        ax[1].plot(time[startindex:], theta[startindex:]/math.pi, marker='.', color='black')
        
        ax[2].plot(time[startindex:], a[startindex:], marker='.', color='black')
        
        ax[3].plot(time[startindex:], np.minimum(np.sqrt(f_xpos**2 + f_ypos**2), np.sqrt(f_xneg**2 + f_yneg**2))[startindex:], marker='.', color='green',label='ellipse focus')
        ax[3].plot(time[startindex:], np.sqrt(xcenter**2 + ycenter**2)[startindex:] , marker='.', color='red', label='ellipse center')
        
        ax[4].plot(time[startindex:], np.minimum(np.sqrt((f_xpos-xcom)**2 + (f_ypos-ycom)**2), np.sqrt((f_xneg-xcom)**2 + (f_yneg-ycom)**2))[startindex:], marker='.', color='green',label='ellipse focus')
        ax[4].plot(time[startindex:], np.sqrt((xcenter-xcom)**2 + (ycenter-ycom)**2)[startindex:] , marker='.', color='red', label='ellipse center')
        
        ax[5].plot(time[startindex:],xcom[startindex:], marker='.', color='blue', label='xcom')
        ax[5].plot(time[startindex:],ycom[startindex:], marker='.', color='black', label='ycom')
        ax[5].plot(time[startindex:],np.sqrt(xcom[startindex:]**2 + ycom[startindex:]**2), marker='.', color='purple', label='rcom')
        ax[5].set_ylim(-1.5,1.5)
        ax[5].axhline(0, color='darkgray', ls='--', alpha=0.5)
        
        ax[6].plot(time[startindex:],xcenter[startindex:], marker='.', color='blue', label='xcenter')
        ax[6].plot(time[startindex:],ycenter[startindex:], marker='.', color='black', label='ycenter')
        ax[6].plot(time[startindex:],np.sqrt(xcenter[startindex:]**2 + ycenter[startindex:]**2), marker='.', color='purple', label='rcenter')
        ax[6].axhline(0, color='darkgray', ls='--', alpha=0.5)
        ax[6].set_ylim(-1.5,1.5)
        
        ax[7].plot(time[startindex:], rm1[startindex:], color='blue', marker='.', label=r'$m=1$')
        ax[7].plot(time[startindex:], rm2[startindex:], color='red', marker='.', label=r'$m=2$')
        #ax[7].plot(time[startindex:], rm3[startindex:], color='green', marker='.', label=r'$m=3$')
        #ax[7].plot(time[startindex:], rm4[startindex:], color='purple', marker='.', label=r'$m=4$')
        #ax[7].plot(time[startindex:], rm5[startindex:], color='black', marker='.', label=r'$m=5$')
        #ax[7].plot(time[startindex:], rm6[startindex:], color='saddlebrown', marker='.', label=r'$m=6$')
        #ax[7].plot(time[startindex:], rm7[startindex:], color='violet',alpha=0.5, marker='.', label=r'$m=7$')
        #ax[7].plot(time[startindex:], rm8[startindex:], color='darkgray', alpha=0.5, marker='.', label=r'$m=8$')
        #ax[7].plot(time[startindex:], rm9[startindex:], color='pink', alpha=0.5, marker='.', label=r'$m=9$')
        #ax[7].plot(time[startindex:], rm10[startindex:], color='limegreen', alpha=0.5, marker='.', label=r'$m=10$')
        
        
        
        ax[8].plot(time[startindex:], am1[startindex:]/math.pi, color='blue', marker='.', label=r'$m=1$')
        ax[8].plot(time[startindex:], am2[startindex:]/math.pi, color='red', marker='.', label=r'$m=2$')
        #ax[8].plot(time[startindex:], am3[startindex:]/math.pi, color='green', marker='.', label=r'$m=3$')
        #ax[8].plot(time[startindex:], am4[startindex:]/math.pi, color='purple', marker='.', label=r'$m=4$')
        #ax[8].plot(time[startindex:], am5[startindex:]/math.pi, color='black', marker='.', label=r'$m=5$')
        #ax[8].plot(time[startindex:], am6[startindex:]/math.pi, color='saddlebrown', marker='.', label=r'$m=6$')
        #ax[8].plot(time[startindex:], am7[startindex:]/math.pi, color='violet',alpha=0.5, marker='.', label=r'$m=7$')
        #ax[8].plot(time[startindex:], am8[startindex:]/math.pi, color='darkgray', alpha=0.5, marker='.', label=r'$m=8$')
        #ax[8].plot(time[startindex:], am9[startindex:]/math.pi, color='pink', alpha=0.5, marker='.', label=r'$m=9$')
        #ax[8].plot(time[startindex:], am10[startindex:]/math.pi, color='limegreen', alpha=0.5, marker='.', label=r'$m=10$')
        
        ax[7].legend()
        ax[6].legend()
        ax[5].legend()
        ax[3].legend()
        ax[4].legend()
        ax[8].legend()
        ax[0].set_ylabel('e')
        ax[1].set_ylabel(r'$\theta_{C}/\pi$')
        ax[2].set_ylabel('a (semi-major)')
        ax[3].set_ylabel('distance/a (bary)')
        ax[4].set_ylabel('distance/a (com)')
        ax[5].set_ylabel('distance/a')
        ax[6].set_ylabel('distance/a (com)')
        ax[7].set_ylabel(r'mag')
        ax[8].set_ylabel(r'phase/$\pi$')
        ax[8].set_xlabel(r'Time/10')
        fig.tight_layout()
        fig.savefig('sweep_timeseries/'+'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'full_fourier_ellipse_final.pdf')
        plt.close()
        
        
        fig, ax=plt.subplots(4,2)
        fig.set_figheight(6)
        fig.set_figwidth(12)
        
        ax[0][0].plot(time[startindex:]*10, ecc[startindex:], marker='.', color='black')
        ax[1][0].plot(time[startindex:]*10, theta[startindex:]/math.pi, marker='.', color='black')
        
        ax[2][0].plot(time[startindex:]*10, a[startindex:], marker='.', color='black')
        
        
        ax[3][0].plot(time[startindex:]*10, rm1[startindex:]/N, color='blue', marker='.', label=r'$m=1$')
        ax[3][0].plot(time[startindex:]*10, rm2[startindex:]/N, color='red', marker='.', label=r'$m=2$')
        #ax[7].plot(time[startindex:], rm3[startindex:], color='green', marker='.', label=r'$m=3$')
        #ax[7].plot(time[startindex:], rm4[startindex:], color='purple', marker='.', label=r'$m=4$')
        #ax[7].plot(time[startindex:], rm5[startindex:], color='black', marker='.', label=r'$m=5$')
        #ax[7].plot(time[startindex:], rm6[startindex:], color='saddlebrown', marker='.', label=r'$m=6$')
        #ax[7].plot(time[startindex:], rm7[startindex:], color='violet',alpha=0.5, marker='.', label=r'$m=7$')
        #ax[7].plot(time[startindex:], rm8[startindex:], color='darkgray', alpha=0.5, marker='.', label=r'$m=8$')
        #ax[7].plot(time[startindex:], rm9[startindex:], color='pink', alpha=0.5, marker='.', label=r'$m=9$')
        #ax[7].plot(time[startindex:], rm10[startindex:], color='limegreen', alpha=0.5, marker='.', label=r'$m=10$')
        
        ax[0][1].plot(time[startindex:]*10, e_1[startindex:], color='blue', marker='.', label=r'$m=1$')
        ax[1][1].plot(time[startindex:]*10, e_2[startindex:], color='red', marker='.', label=r'$m=2$')
        
        ax[2][1].plot(time[startindex:]*10, am1[startindex:]/math.pi, color='blue', marker='.', label=r'$m=1$')
        ax[3][1].plot(time[startindex:]*10, am2[startindex:]/math.pi, color='red', marker='.', label=r'$m=2$')
        #ax[8].plot(time[startindex:], am3[startindex:]/math.pi, color='green', marker='.', label=r'$m=3$')
        #ax[8].plot(time[startindex:], am4[startindex:]/math.pi, color='purple', marker='.', label=r'$m=4$')
        #ax[8].plot(time[startindex:], am5[startindex:]/math.pi, color='black', marker='.', label=r'$m=5$')
        #ax[8].plot(time[startindex:], am6[startindex:]/math.pi, color='saddlebrown', marker='.', label=r'$m=6$')
        #ax[8].plot(time[startindex:], am7[startindex:]/math.pi, color='violet',alpha=0.5, marker='.', label=r'$m=7$')
        #ax[8].plot(time[startindex:], am8[startindex:]/math.pi, color='darkgray', alpha=0.5, marker='.', label=r'$m=8$')
        #ax[8].plot(time[startindex:], am9[startindex:]/math.pi, color='pink', alpha=0.5, marker='.', label=r'$m=9$')
        #ax[8].plot(time[startindex:], am10[startindex:]/math.pi, color='limegreen', alpha=0.5, marker='.', label=r'$m=10$')
        


        ax[0][0].set_ylabel(r'$e_{\rm{fit}}$')
        ax[1][0].set_ylabel(r'$\varpi_{\rm{fit}}/ \pi$')
        ax[2][0].set_ylabel(r'$a_{\rm{fit}}$')
        
        ax[3][0].set_ylabel(r'$|\hat{r}_{m}|$')
        
        ax[0][1].set_ylabel(r'$e_{m=1}$')
        ax[1][1].set_ylabel(r'$e_{m=2}$')
        
        ax[2][1].set_ylabel(r'$\hat{\phi}_{m=1} / \pi$')
        ax[3][1].set_ylabel(r'$\hat{\phi}_{m=2} / \pi$')
        
        
        ax[3][0].set_xlabel(r'$\tau_{\rm{b}}$')
        ax[3][1].set_xlabel(r'$\tau_{\rm{b}}$')
        fig.tight_layout()
        fig.savefig('sweep_timeseries_alternative/'+'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'full_fourier_ellipse_final.pdf')
        plt.close()
        
        fig, ax = plt.subplots(2,2)
        fig.set_figheight(8)
        fig.set_figwidth(13)
        
        
        ax[0][0].plot(time[startindex:]*10, e_1[startindex:], color='blue', marker='.', label=r'$m=1$')
        ax[0][1].plot(time[startindex:]*10, e_2[startindex:], color='red', marker='.', label=r'$m=2$')
        
        ax[1][0].plot(time[startindex:]*10, a1[startindex:], color='blue', marker='.', label=r'$m=1$')
        ax[1][1].plot(time[startindex:]*10, a2[startindex:], color='red', marker='.', label=r'$m=2$')
        fig.tight_layout()
        
        fig.savefig('timeseries_alt_funk/'+'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'timeseries.pdf')
        
        e_master_save.append(np.mean(e_1[startindex:]))
        a_master_save.append(np.mean(a1[startindex:]))
        continue
        
a_grid=np.reshape(np.array(a_master_save).flatten(), (8,10)).T
e_grid=np.reshape(np.array(e_master_save).flatten(), (8,10)).T

fig, ax =plt.subplots()
cax=ax.imshow(a_grid, aspect='auto', origin='lower', cmap='viridis', extent=[ecclist[0], ecclist[-1],qblist[0], qblist[-1]])
yticks = np.linspace(qblist[0]+0.05, qblist[-1]-0.05, num=10)  #  ticks on the x-axis (e)
xticks = np.linspace(ecclist[0]+0.05, ecclist[-1]-0.05, num=8)
ax.set_xticks(xticks)
ax.set_yticks(yticks)

# Set the tick labels at the appropriate positions
ax.set_xticklabels([f'{e:.1f}' for e in ecclist])  # Custom x-tick labels
ax.set_yticklabels([f'{q:.1f}' for q in qblist])  # Custom y-tick labels
ax.set_xlabel(r'e$_{\rm{b}}$')
ax.set_ylabel(r'a$_{\rm{b}}$')

fig.colorbar(cax, label=r'a$_{\rm{cav}}$ [a$_{\rm{b}}$]')
#fig.set_constrained_layout(True)
fig.tight_layout()
fig.savefig('a_cavity_heatmap.pdf')
fig, ax =plt.subplots()
cax=ax.imshow(e_grid, aspect='auto', origin='lower', cmap='viridis', extent=[ecclist[0], ecclist[-1],qblist[0], qblist[-1]])
ax.set_xticks(xticks)
ax.set_yticks(yticks)
ax.set_xlabel(r'$e_b$')
ax.set_ylabel(r'$q_b$')

# Set the tick labels at the appropriate positions
ax.set_xticklabels([f'{e:.1f}' for e in ecclist])  # Custom x-tick labels
ax.set_yticklabels([f'{q:.1f}' for q in qblist])  # Custom y-tick labels
fig.colorbar(cax,label=r'e$_{\rm{cav}}$')
#fig.set_constrained_layout(True)
fig.tight_layout()
fig.savefig('e_m1_cavity_heatmap.pdf')


fig, ax =plt.subplots(2,1)#, constrained_layout=True)
fig.set_figheight(8)
fig.set_figwidth(8)
im=ax[0].imshow(a_grid, aspect='auto', origin='lower', cmap='viridis', extent=[ecclist[0], ecclist[-1],qblist[0], qblist[-1]])
divider = make_axes_locatable(ax[0])
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar= plt.colorbar(im, cax=cax)
cbar.set_label(label=r'a$_{\rm{cav}}$ [a$_{\rm{b}}$]')

yticks = np.linspace(qblist[0]+0.05, qblist[-1]-0.05, num=10)  #  ticks on the x-axis (e)
xticks = np.linspace(ecclist[0]+0.05, ecclist[-1]-0.05, num=8)
ax[0].set_xticks(xticks)
ax[0].set_yticks(yticks)

ax[1].set_xticks(xticks)
ax[1].set_yticks(yticks)

# Set the tick labels at the appropriate positions
ax[1].set_xticklabels([f'{e:.1f}' for e in ecclist])  # Custom x-tick labels
ax[1].set_yticklabels([f'{q:.1f}' for q in qblist])  # Custom y-tick labels

ax[0].set_xticklabels([f'{e:.1f}' for e in ecclist])  # Custom x-tick labels
ax[0].set_yticklabels([f'{q:.1f}' for q in qblist])  # Custom y-tick labels

ax[1].set_xlabel(r'e$_{\rm{b}}$')
ax[0].set_ylabel(r'q$_{\rm{b}}$')
ax[1].set_ylabel(r'q$_{\rm{b}}$')


im=ax[1].imshow(e_grid, aspect='auto', origin='lower', cmap='viridis', extent=[ecclist[0], ecclist[-1],qblist[0], qblist[-1]])
divider = make_axes_locatable(ax[1])
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar= plt.colorbar(im, cax=cax)
cbar.set_label(label=r'e$_{\rm{cav}}$')
#fig.colorbar(cax,label=r'e$_{\rm{cav}}$')
#fig.set_constrained_layout(True)
#fig.tight_layout()

np.save('cavity_a_m1_data.npy', a_grid)
np.save('cavity_e_m1_data.npy', e_grid)
fig.savefig('a_e_cavity_heatmap_joint.pdf', bbox_inches='tight')
asdjfkl

if 1==1:
        
        startindex=800
        
        fig, ax = plt.subplots()
        fig.set_figheight(4)
        fig.set_figwidth(6)
        ax.plot(time[startindex:]*10, theta[startindex:]/math.pi, marker='.', color='black', label='LLS')
        ax.plot(time[startindex:]*10, am1[startindex:]/math.pi, color='blue', marker='*', label=r'Fourier ($m=1$)')
        ax.legend(loc='lower right')
        ax.set_ylim(-1.1, 1.1)
        ax.set_xlabel(r'Time [$\tau_{\rm{b}}$]')
        ax.set_ylabel(r'$\varpi / \pi$')
        #ax.plot(time[startindex:]*10, am2[startindex:]/math.pi, color='red', marker='.', label=r'$m=2$')
        fig.tight_layout()
        plt.savefig('eb_0_qb_0.1_varpi_comp.pdf')
        asf
        
        
    
        import scipy
        import scipy.signal
        from scipy.signal import lombscargle
        from astropy.timeseries import LombScargle as lombscargle
        infreqs=10**np.arange(-1.99,0,0.001)
        fig, ax=plt.subplots(11,1)
        fig.set_figheight(20)
        fig.set_figwidth(30)
        startindex=0
        rcenter=np.sqrt(xcenter**2 + ycenter**2)
        rcom=np.sqrt(xcom[startindex:]**2 + ycom[startindex:]**2)
        
        foc_bary=np.minimum(np.sqrt(f_xpos**2 + f_ypos**2), np.sqrt(f_xneg**2 + f_yneg**2))
        center_bary=np.sqrt(xcenter**2 + ycenter**2)
        
        center_com=np.sqrt((xcenter-xcom)**2 + (ycenter-ycom)**2)
        foc_com=np.minimum(np.sqrt((f_xpos-xcom)**2 + (f_ypos-ycom)**2), np.sqrt((f_xneg-xcom)**2 + (f_yneg-ycom)**2))
        
        
        
    # =============================================================================
    #     eccpg=lombscargle(time[startindex:], ecc[startindex:], freqs=infreqs, normalize=True)
    #     thetapg=lombscargle(time[startindex:], theta[startindex:], freqs=infreqs, normalize=True)
    #     apg=lombscargle(time[startindex:], a[startindex:], freqs=infreqs, normalize=True)
    #     foc_barypg=lombscargle(time[startindex:], np.minimum(np.sqrt(f_xpos**2 + f_ypos**2), np.sqrt(f_xneg**2 + f_yneg**2))[startindex:], freqs=infreqs, normalize=True)
    #     center_barypg=lombscargle(time[startindex:], np.sqrt(xcenter**2 + ycenter**2)[startindex:], freqs=infreqs, normalize=True)
    #     foc_compg=lombscargle(time[startindex:], np.minimum(np.sqrt((f_xpos-xcom)**2 + (f_ypos-ycom)**2), np.sqrt((f_xneg-xcom)**2 + (f_yneg-ycom)**2))[startindex:], freqs=infreqs, normalize=True)
    #     center_compg=lombscargle(time[startindex:], np.sqrt((xcenter-xcom)**2 + (ycenter-ycom)**2)[startindex:], freqs=infreqs, normalize=True)
    #     xcompg=lombscargle(time[startindex:], xcom[startindex:], freqs=infreqs, normalize=True)
    #     ycompg=lombscargle(time[startindex:], ycom[startindex:], freqs=infreqs, normalize=True)
    #     rcompg=lombscargle(time[startindex:], np.sqrt(xcom[startindex:]**2 + ycom[startindex:]**2), freqs=infreqs, normalize=True)
    #     xcenterpg=lombscargle(time[startindex:], xcenter[startindex:], freqs=infreqs, normalize=True)
    #     ycenterpg=lombscargle(time[startindex:], ycenter[startindex:], freqs=infreqs, normalize=True)
    #     rcenterpg=lombscargle(time[startindex:], np.sqrt(xcenter[startindex:]**2 + ycenter[startindex:]**2), freqs=infreqs, normalize=True)
    #     rm1pg=lombscargle(time[startindex:], rm1[startindex:], freqs=infreqs, normalize=True)
    #     rm2pg=lombscargle(time[startindex:], rm2[startindex:], freqs=infreqs, normalize=True)
    #     am1pg=lombscargle(time[startindex:], am1[startindex:], freqs=infreqs, normalize=True)
    #     am2pg=lombscargle(time[startindex:], am2[startindex:], freqs=infreqs, normalize=True)
    # =============================================================================
        
        
        eccfreqs,eccpg=lombscargle(time[startindex:], ecc[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        thetafreqs, thetapg=lombscargle(time[startindex:], theta[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        afreqs,apg=lombscargle(time[startindex:], a[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        foc_baryfreqs, foc_barypg=lombscargle(time[startindex:], np.minimum(np.sqrt(f_xpos**2 + f_ypos**2), np.sqrt(f_xneg**2 + f_yneg**2))[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        center_baryfreqs, center_barypg=lombscargle(time[startindex:], np.sqrt(xcenter**2 + ycenter**2)[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        foc_comfreqs, foc_compg=lombscargle(time[startindex:], np.minimum(np.sqrt((f_xpos-xcom)**2 + (f_ypos-ycom)**2), np.sqrt((f_xneg-xcom)**2 + (f_yneg-ycom)**2))[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        center_comfreqs, center_compg=lombscargle(time[startindex:], np.sqrt((xcenter-xcom)**2 + (ycenter-ycom)**2)[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        xcomfreqs, xcompg=lombscargle(time[startindex:], xcom[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        ycomfreqs, ycompg=lombscargle(time[startindex:], ycom[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        rcomfreqs, rcompg=lombscargle(time[startindex:], np.sqrt(xcom[startindex:]**2 + ycom[startindex:]**2)).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        xcenterfreqs, xcenterpg=lombscargle(time[startindex:], xcenter[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        ycenterfreqs, ycenterpg=lombscargle(time[startindex:], ycenter[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        rcenterfreqs, rcenterpg=lombscargle(time[startindex:], np.sqrt(xcenter[startindex:]**2 + ycenter[startindex:]**2)).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        rm1freqs, rm1pg=lombscargle(time[startindex:], rm1[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        rm2freqs, rm2pg=lombscargle(time[startindex:], rm2[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        am1freqs, am1pg=lombscargle(time[startindex:], am1[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        am2freqs, am2pg=lombscargle(time[startindex:], am2[startindex:]).autopower(minimum_frequency=infreqs[0],maximum_frequency=infreqs[-1])
        
        ax[0].plot(10*(1)/eccfreqs, eccpg , label='e_c')
        ax[1].plot(10*(1)/thetafreqs, thetapg, label='theta_c')
        ax[2].plot(10*(1)/afreqs, apg, label='a')
        
        
        ax[3].plot(10*(1)/foc_baryfreqs, foc_barypg, color='red', label='min foci (bary)')
        ax[3].plot(10*(1)/center_baryfreqs, center_barypg, color='blue', label='cav center (bary)')
        
        ax[4].plot(10*(1)/foc_comfreqs, foc_compg, color='red', label='min foci (com)')
        ax[4].plot(10*(1)/center_comfreqs, center_compg, color='blue', label='cav center (com)')
       
        
        ax[5].plot(10*(1)/xcomfreqs, xcompg, color='blue', label='xcom')
        ax[5].plot(10*(1)/ycomfreqs, ycompg, color='black', label='ycom')
        ax[5].plot(10*(1)/rcomfreqs, rcompg, color='purple', label='rcom')
        
        
        ax[6].plot(10*(1)/xcenterfreqs, xcenterpg, color='blue', label='xcenter')
        ax[6].plot(10*(1)/ycenterfreqs, ycenterpg, color='black', label='ycenter')
        ax[6].plot(10*(1)/rcenterfreqs, rcenterpg, color='purple', label='rcenter')
        
        
        
        
        ax[7].plot(10*(1)/rm1freqs, rm1pg, label='mag m=1')
        
        ax[8].plot(10*(1)/rm2freqs, rm2pg, label='mag m=2')
        
        
        ax[9].plot(10*(1)/am1freqs, am1pg, label='phase m=1')
        
        ax[10].plot(10*(1)/am2freqs, am2pg, label='phase m=2')
        
        for axs in ax:
            axs.set_xscale('log')
            axs.legend()
            #axs.axvline(50,color='black', alpha=0.5, ls='--')
            #axs.set_ylim(0,1)
            #axs.axvline(30,color='black', alpha=0.5, ls='--')
        
        fig.tight_layout()
        fig.savefig('sweep_periodograms/'+'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'lombscargle_fourier_cavs.pdf')
        plt.close(fig)
        
        
        from scipy.fft import fft, fftfreq
        
       
# =============================================================================
#         fig, ax=plt.subplots(2,2)
#         N=600
#         T=1/800
#         x = np.linspace(0.0, N*T, N, endpoint=False)
#         y = np.sin(10.0 * 2.0*np.pi*x) + 0.5*np.sin(100.0 * 2.0*np.pi*x)
#         yf=fft(y)[1:len(y)//2]
#         xf=fftfreq(N,T)[1:len(y)//2]
#         ax[0][0].plot(xf, (2/len(yf))*np.abs(yf), color='blue')
#         ax[1][0].plot((2*math.pi)/(xf), (2/len(yf))*np.abs(yf), color='blue')
#         ax[0][1].plot(x,y, color='blue')
#         ax[1][1].plot(np.arange(len(yf))+1, (2/len(yf))*np.abs(yf), color='blue')
#         ax[0][0].set_xscale('log')
#         ax[1][0].set_xscale('log')
#         fig.savefig('fft_pure_sinwave_test.pdf')
#         
# =============================================================================
        N=len(ecc)
        T=10
        xf = fftfreq(N, T)[1:N//2]
        
        eccpg = fft(ecc)[1:N//2]
        thetapg = fft(theta)[1:N//2]
        apg = fft(a)[1:N//2]
        
        foc_barypg = fft(foc_bary)[1:N//2]
        center_barypg=fft(center_bary)[1:N//2]
        
        foc_compg=fft(foc_com)[1:N//2]
        center_compg=fft(center_com)[1:N//2]
        
        xcompg=fft(xcom)[1:N//2]
        ycompg=fft(ycom)[1:N//2]
        rcompg=fft(rcom)[1:N//2]
        
        xcenterpg=fft(xcenter)[1:N//2]
        ycenterpg=fft(ycenter)[1:N//2]
        rcenterpg=fft(rcenter)[1:N//2]
        
        rm1pg=fft(rm1)[1:N//2]
        am1pg=fft(am1)[1:N//2]
        rm2pg=fft(rm2)[1:N//2]
        am2pg=fft(am2)[1:N//2]
        
        
        fig, ax=plt.subplots(11,1)
        fig.set_figheight(20)
        fig.set_figwidth(30)
        ax[0].plot((1)/(xf), (2/N)*np.abs(eccpg) , label='e_c')
        ax[1].plot((1)/(xf), (2/N)*np.abs(thetapg), label='theta_c')
        ax[2].plot((1)/(xf), (2/N)*np.abs(apg), label='a')
        
        
        ax[3].plot((1)/(xf), (2/N)*np.abs(foc_barypg), color='red', label='min foci (bary)')
        ax[3].plot((1)/(xf), (2/N)*np.abs(center_barypg), color='blue', label='cav center (bary)')
        
        ax[4].plot((1)/(xf), (2/N)*np.abs(foc_compg), color='red', label='min foci (com)')
        ax[4].plot((1)/(xf), (2/N)*np.abs(center_compg), color='blue', label='cav center (com)')
       
        
        ax[5].plot((1)/(xf), (2/N)*np.abs(xcompg), color='blue', label='xcom')
        ax[5].plot((1)/(xf), (2/N)*np.abs(ycompg), color='black', label='ycom')
        ax[5].plot((1)/(xf), (2/N)*np.abs(rcompg), color='purple', label='rcom')
        
        
        ax[6].plot((1)/(xf), (2/N)*np.abs(xcenterpg), color='blue', label='xcenter')
        ax[6].plot((1)/(xf), (2/N)*np.abs(ycenterpg), color='black', label='ycenter')
        ax[6].plot((1)/(xf), (2/N)*np.abs(rcenterpg), color='purple', label='rcenter')
        
        
        
        
        ax[7].plot((1)/(xf), (2/N)*np.abs(rm1pg), label='mag m=1')
        
        ax[8].plot((1)/(xf), (2/N)*np.abs(rm2pg), label='mag m=2')
        
        
        ax[9].plot((1)/(xf), (2/N)*np.abs(am1pg), label='phase m=1')
        
        ax[10].plot((1)/(xf), (2/N)*np.abs(am2pg), label='phase m=2')
        
        
        from statsmodels.nonparametric.smoothers_lowess import lowess
        eccpg_lowess_x=lowess((2/N)*np.abs(eccpg), 1/(xf), frac=0.01)[:,0]
        eccpg_lowess_y=lowess((2/N)*np.abs(eccpg), 1/(xf), frac=0.01)[:,1]
        
        thetapg_lowess_x=lowess((2/N)*np.abs(thetapg), 1/(xf), frac=0.01)[:,0]
        thetapg_lowess_y=lowess((2/N)*np.abs(thetapg), 1/(xf), frac=0.01)[:,1]
        
        apg_lowess_x=lowess((2/N)*np.abs(apg), 1/(xf), frac=0.01)[:,0]
        apg_lowess_y=lowess((2/N)*np.abs(apg), 1/(xf), frac=0.01)[:,1]
        
        #foc_barypg_lowess_x=lowess((2/N)*np.abs(foc_barypg), 1/(xf), frac=0.01)[:,0]
        #foc_barypg_lowess_y=lowess((2/N)*np.abs(foc_barypg), 1/(xf), frac=0.01)[:,1]
        
        rm1pg_lowess_x=lowess((2/N)*np.abs(rm1pg), 1/(xf), frac=0.01)[:,0]
        rm1pg_lowess_y=lowess((2/N)*np.abs(rm1pg), 1/(xf), frac=0.01)[:,1]
        
        rm2pg_lowess_x=lowess((2/N)*np.abs(rm2pg), 1/(xf), frac=0.01)[:,0]
        rm2pg_lowess_y=lowess((2/N)*np.abs(rm2pg), 1/(xf), frac=0.01)[:,1]
        
        am1pg_lowess_x=lowess((2/N)*np.abs(am1pg), 1/(xf), frac=0.01)[:,0]
        am1pg_lowess_y=lowess((2/N)*np.abs(am1pg), 1/(xf), frac=0.01)[:,1]
        
        am2pg_lowess_x=lowess((2/N)*np.abs(am2pg), 1/(xf), frac=0.01)[:,0]
        am2pg_lowess_y=lowess((2/N)*np.abs(am2pg), 1/(xf), frac=0.01)[:,1]
        
        
        ax[0].plot(eccpg_lowess_x,eccpg_lowess_y, color='black', ls='--')
        ax[1].plot(thetapg_lowess_x,thetapg_lowess_y, color='black', ls='--')
        ax[2].plot(apg_lowess_x,apg_lowess_y, color='black', ls='--')
        #ax[3].plot(foc_barypg_lowess_x,foc_barypg_lowess_x, color='black', ls='--')
        
        ax[7].plot(rm1pg_lowess_x,rm1pg_lowess_y, color='black', ls='--')
        ax[8].plot(rm2pg_lowess_x,rm2pg_lowess_y, color='black', ls='--')
        ax[9].plot(am1pg_lowess_x,am1pg_lowess_y, color='black', ls='--')
        ax[10].plot(am2pg_lowess_x,am2pg_lowess_y, color='black', ls='--')
        
        
        
        for axs in ax:
            axs.set_xscale('log')
            axs.legend()
            #axs.axvline(50,color='black', alpha=0.5, ls='--')
            #axs.set_ylim(0,1)
            #axs.axvline(30,color='black', alpha=0.5, ls='--')
        
        fig.tight_layout()
        fig.savefig('sweep_fft/'+'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'fft_cavs.pdf')
        plt.close(fig)
        
        
        
         
        
        
        def localmax(array):
            indices=np.where(np.diff(np.sign(np.diff(array)))==-2)[0]+1
            return(indices)
    
        print('THIS IS '+'e'+str(ecclist[ebind])+' qb '+str(qblist[qbind])+'!!')
        
        f=open('saving_peaks.txt', 'a+')
        f.write(('THIS IS '+'e'+str(ecclist[ebind])+' qb '+str(qblist[qbind])+'!!'+'\n'))
        
        print(' Max ecc', eccpg_lowess_x[np.where(np.nanmax(eccpg_lowess_y)==eccpg_lowess_y)[0]][0], np.nanmax(eccpg_lowess_y))
        f.write(' Max ecc; Period:'+format(eccpg_lowess_x[np.where(np.nanmax(eccpg_lowess_y)==eccpg_lowess_y)[0]][0], '.4f')+'; Power: '+format(np.nanmax(eccpg_lowess_y),'.4f')+'\n')
        
        print(' Max theta', thetapg_lowess_x[np.where(np.nanmax(thetapg_lowess_y)==thetapg_lowess_y)[0]][0], np.nanmax(thetapg_lowess_y))
        f.write(' Max theta; Period:'+format(thetapg_lowess_x[np.where(np.nanmax(thetapg_lowess_y)==thetapg_lowess_y)[0]][0], '.4f')+'; Power: '+format(np.nanmax(thetapg_lowess_y),'.4f')+'\n')
        
        print(' Max a', apg_lowess_x[np.where(np.nanmax(apg_lowess_y)==apg_lowess_y)[0]][0], np.nanmax(apg_lowess_y))
        f.write(' Max a; Period:'+format(apg_lowess_x[np.where(np.nanmax(apg_lowess_y)==apg_lowess_y)[0]][0], '.4f')+'; Power: '+format(np.nanmax(apg_lowess_y),'.4f')+'\n')
        
        print(' Max rm1', rm1pg_lowess_x[np.where(np.nanmax(rm1pg_lowess_y)==rm1pg_lowess_y)[0]][0], np.nanmax(rm1pg_lowess_y))
        f.write(' Max rm1; Period:'+format(rm1pg_lowess_x[np.where(np.nanmax(rm1pg_lowess_y)==rm1pg_lowess_y)[0]][0], '.4f')+'; Power: '+format(np.nanmax(rm1pg_lowess_y),'.4f')+'\n')
        
        print(' Max rm2', rm2pg_lowess_x[np.where(np.nanmax(rm2pg_lowess_y)==rm2pg_lowess_y)[0]][0], np.nanmax(rm2pg_lowess_y))
        f.write(' Max rm2; Period:'+format(rm2pg_lowess_x[np.where(np.nanmax(rm2pg_lowess_y)==rm2pg_lowess_y)[0]][0], '.4f')+'; Power: '+format(np.nanmax(rm2pg_lowess_y),'.4f')+'\n')
        
        
        print(' Max am1', am1pg_lowess_x[np.where(np.nanmax(am1pg_lowess_y)==am1pg_lowess_y)[0]][0], np.nanmax(am1pg_lowess_y))
        f.write(' Max am1; Period:'+format(am1pg_lowess_x[np.where(np.nanmax(am1pg_lowess_y)==am1pg_lowess_y)[0]][0], '.4f')+'; Power: '+format(np.nanmax(am1pg_lowess_y),'.4f')+'\n')
        
        
        print(' Max am2', am2pg_lowess_x[np.where(np.nanmax(am2pg_lowess_y)==am2pg_lowess_y)[0]][0], np.nanmax(am2pg_lowess_y))
        f.write(' Max am2; Period:'+format(am2pg_lowess_x[np.where(np.nanmax(am2pg_lowess_y)==am2pg_lowess_y)[0]][0], '.4f')+'; Power: '+format(np.nanmax(am2pg_lowess_y),'.4f')+'\n')
        
        

        f.write('\n\n')
        f.close()
            
        ecc=ecc.reshape(1,len(ecc))
        theta=theta.reshape(1,len(theta))
        a=a.reshape(1,len(a))
        
        foc_com=foc_com.reshape(1, len(foc_com))
        center_com=center_com.reshape(1, len(center_com))
        rcom=rcom.reshape(1,len(rcom))
        
        foc_bary=foc_bary.reshape(1, len(foc_bary))
        center_bary=center_bary.reshape(1, len(center_bary))
        rcenter=rcenter.reshape(1,len(rcenter))
        
        rm1=rm1.reshape(1,len(rm1))
        rm2=rm2.reshape(1,len(rm2))
        am1=am1.reshape(1,len(am1))
        am2=am2.reshape(1,len(am2))
    
        
    
       
        print('\n')
        
        fig, ax=plt.subplots()
        fig.set_figheight(15)
        fig.set_figwidth(15)
        ticknames=np.array(['ecc','theta', 'a', 'foc_bary','center_com', 'rcom', 'rm1', 'rm2',' am1', 'am2'])
        alldata=np.concatenate((ecc,theta, a, foc_com, center_com, rcom, rm1, rm2, am1, am2))
        corrcoeff_matrix=np.corrcoef(alldata, alldata)
        corrcoeff_matrix=corrcoeff_matrix[0:10,0:10]
        for i in range(10):
            for j in range(10):
                if j>i:
                    corrcoeff_matrix[i,j]=0
        im=ax.imshow(corrcoeff_matrix, cmap='bwr',vmin=-1,vmax=1)
        ax.set_xticks(np.arange(0,10,1))
        ax.set_yticks(np.arange(0,10,1))
        ax.set_xticklabels(ticknames)
        ax.set_yticklabels(ticknames)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar= plt.colorbar(im, cax=cax)
        cbar.set_label(label='correlation')
        fig.tight_layout()
        fig.savefig('sweep_corr/'+'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'correlation_matrix.pdf')
        
        import corner
        import matplotlib.cm as cm
        import matplotlib
        cmap = plt.cm.bwr
        fig=corner.corner(alldata.T)
        ax = np.array(fig.axes).reshape((10, 10))
        norm = matplotlib.colors.Normalize( vmin=-1, vmax=1, clip=True)
        for i in range(10):
            ax[i][0].set_ylabel(ticknames[i])
            for j in range(10):
                ax[9][j].set_xlabel(ticknames[j])
                if j<=i:
                    im=ax[i][j].set_facecolor(cmap(norm(corrcoeff_matrix[i][j])))
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm) 
        sm.set_array([]) 
        fig.colorbar(sm, ax=ax.ravel().tolist()) 
        fig.savefig('sweep_corner/' +'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'cornerplots.pdf')
        
        
        plt.close(fig)
        
        #this is for m=1
        amplitude=(rm1/N)
        baseline=rm0/N
        rmin=baseline-amplitude
        rmax=baseline+amplitude
        a=0.5*(rmin+rmax)
        e_1=1-(rmin/a)
        ex_1=e_1*np.cos(am1)
        ey_1=e_1*np.sin(am1)
        
        e_1=e_1.flatten()
        ex_1=ex_1.flatten()
        ey_1=ey_1.flatten()
        
        
        #this is for m=2
        amplitude=(rm2/N)
        baseline=rm0/N
        rmax=baseline+amplitude
        rmin=baseline-amplitude
        a=rmax
        b=rmin
        e_2=np.sqrt(1-b**2/a**2)
        ex_2=e_2*np.cos(am2).flatten()
        ey_2=e_2*np.sin(am2).flatten()
        
        e_2=e_2.flatten()
        ex_2=ex_2.flatten()
        ey_2=ey_2.flatten()
        
        fig, ax=plt.subplots()
        fig.set_figheight(10)
        fig.set_figwidth(10)
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        colormap = plt.cm.nipy_spectral
        colors = [colormap(i) for i in np.linspace(0, 1,len(time))]
        ax.scatter(ex_1, ey_1, color=colors, alpha=0.8)
        ax.axhline(0, ls='--',color='black')
        ax.axvline(0, ls='--',color='black')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar= plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=time[0], vmax=time[-1]*10), cmap='nipy_spectral'), cax=cax)
        cbar.set_label('Time')
        ax.set_xlabel('ex')
        ax.set_ylabel('ey')
        fig.savefig('sweep_ex_ey/'+'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'ex_ey_m1.pdf')
        plt.close(fig)
        
        fig, ax=plt.subplots()
        fig.set_figheight(10)
        fig.set_figwidth(10)
        colormap = plt.cm.nipy_spectral
        colors = [colormap(i) for i in np.linspace(0, 1,len(time))]
        ax.scatter(ex_2, ey_2, color=colors, alpha=0.8)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar= plt.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=time[0], vmax=time[-1]*10), cmap='nipy_spectral'), cax=cax)
        cbar.set_label('Time')
        ax.set_xlabel('ex')
        ax.set_ylabel('ey')
        ax.axhline(0, ls='--',color='black')
        ax.axvline(0, ls='--',color='black')
        fig.savefig('sweep_ex_ey/'+'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'ex_ey_m2.pdf')
        plt.close(fig)
        
        fig, ax=plt.subplots(3,1)
        fig.set_figheight(10)
        fig.set_figwidth(20)
        ax[0].plot(time, ex_1, marker='x')
        ax[1].plot(time, ey_1, marker='x')
        ax[2].plot(time, e_1, marker='x')
        ax[0].set_ylabel('ex')
        ax[1].set_ylabel('ey')
        ax[2].set_ylabel('e')
        ax[2].set_xlabel('time')
        fig.tight_layout()
        fig.savefig('sweep_ex_ey/'+'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'ex_ey_m1_unraveled.pdf')
        plt.close(fig)
        
        fig, ax=plt.subplots(3,1)
        fig.set_figheight(10)
        fig.set_figwidth(20)
        ax[0].plot(time, ex_2, marker='x')
        ax[1].plot(time, ey_2, marker='x')
        ax[2].plot(time, e_2, marker='x')
        ax[0].set_ylabel('ex')
        ax[1].set_ylabel('ey')
        ax[2].set_ylabel('e')
        ax[2].set_xlabel('time')
        fig.tight_layout()
        fig.savefig('sweep_ex_ey/'+'e'+str(ecclist[ebind])+'_qb_'+str(qblist[qbind])+'_'+'ex_ey_m2_unraveled.pdf')
        plt.close(fig)
        
        
        
        
        
        
        
        
        
        
        #fig, ax=plt.subplots()
        
        
        #there seems to be a correlation going on here between timings 
        #(could be tied back to earlier work about lopsidedness of the cavities)
        
        #also get the correlation functions going comparing cavity parameters (a,e,theta) to am1 rm1 ( and am2 rm2)
        
        #also should make a q_b e_b plot with scatter pints 
        