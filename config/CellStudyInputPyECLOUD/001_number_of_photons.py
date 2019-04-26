from __future__ import division, print_function
import os
import argparse

import numpy as np
#from scipy.constants import e, epsilon_0, h, hbar
import matplotlib.pyplot as plt

import LHCMeasurementTools.mystyle as ms
#~ from RcParams import init_pyplot
#~ init_pyplot()
plt.close('all')
import n_photons
from n_photons import lhc_bending_radius, copper_work_function_eV

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Output file', type=str)
parser.add_argument('--noshow', help='Do not call plt.show.', action='store_true')
args = parser.parse_args()


def set_title(sp, *arg, **kwargs):
    if args.o:
        pass
    else:
       sp.set_title(*arg, fontsize=12, **kwargs)

beam_energies = np.array([450, 3500, 6500, 7000, 11.5e3])*1e9

fig = ms.figure('Photons per m')

sp = plt.subplot(2,2,1)
set_title(sp, r'$N_\gamma > W_{Cu}$ per m bend')
sp.set_xlabel('Energy [TeV]')
sp.set_ylabel(r'$N_\gamma (E>W_{Cu})$')
ms.sciy()
sp.grid(True)

xx = np.linspace(1, 12e3, 1e3)*1e9
yy = n_photons.n_photons_meter(xx, lhc_bending_radius, copper_work_function_eV)
sp.plot(xx/1e12, yy,'.', label='4.6')
spt = sp.twinx()
spt.set_yticks([])

sp2 = plt.subplot(2,2,2)
set_title(sp2,'Ratio of photons above work function')
sp2.set_xlabel('Energy [TeV]')
sp2.set_ylabel('Ratio')
sp2.grid(True)
yy2 = n_photons.n_photons_meter(xx, lhc_bending_radius, 0.)
ratio = yy/yy2
sp2.plot(xx/1e12, ratio, '.', color='black')

for energy, color in zip(beam_energies,['b','g','r', 'c', 'm']):
    this_ratio = np.interp(energy, xx, ratio)
    label = '%.2f' % this_ratio
    sp2.axvline(energy/1e12, ls='--', label=label, color=color)
    this_n_photons = np.interp(energy, xx, yy)
    label = '%.2f' % (this_n_photons*1e2)
    spt.axvline(energy/1e12, ls='--', label=label, color=color)
sp2.legend(loc='upper left', bbox_to_anchor=(1,1), title=r'$N_\gamma (E>W_{Cu}) / N_\gamma$')

#xx2 = np.loadtxt(os.path.dirname(os.path.abspath(__file__))+'/nphotons_giovanni.csv', delimiter=',')
#sp.plot(xx2[:,0]/1e3, xx2[:,1],'.', label='4.4 (GR)')
#sp.legend(loc='upper left', bbox_to_anchor=(1,1), title='$W_{Cu}$ [eV]')
spt.legend(loc='upper left', bbox_to_anchor=(1,1), title='$N_\gamma$ [1e-2]')

sp = plt.subplot(2,2,3)
set_title(sp,'Distribution of photons')
sp.set_ylabel('dn/dE')
sp.grid(True)
#xx_e = np.linspace(0.0001,100,1e3)
xx_e = np.exp(np.linspace(np.log(1e0), np.log(1e3), 1e2))

sp4 = plt.subplot(2,2,4)
set_title(sp4,'Energy spectrum of radiation')
sp4.set_ylabel('dP/dE')
sp4.grid(True)
for energy_eV in beam_energies:
    yy_e = n_photons.spectral_at_energy(xx_e, energy_eV, lhc_bending_radius)
    label = '%i' % (energy_eV/1e9)
    sp.loglog(xx_e, yy_e,'.', label=label)
    sp4.semilogx(xx_e, xx_e*yy_e,'.', label=label)
sp.set_ylim(1e-15,None)

#    critical_angle = compute_critical_angle(energy_eV, lhc_bending_radius, copper_work_function_eV)
#    print('Critical angle for %.2e: %.2e' % (energy_eV, critical_angle))

for sp_ in sp,sp4:
    sp_.set_xlabel(r'$E_\gamma$ [eV]')
    sp_.axvline(copper_work_function_eV, label='$W_{Cu}$ [eV]', color='black')
sp4.legend(title='Energy [GeV]', bbox_to_anchor=(0.8,1))
sp.legend(title='Energy [GeV]', loc='upper left', bbox_to_anchor=(0.8,1))
#sp.set_ylim(1e-28,None)

if args.o:
    plt.suptitle('')
    plt.subplots_adjust(left=0.12, hspace=0.45, wspace=0.8)
    fig.savefig(os.path.expanduser(args.o))

if not args.noshow:
    plt.show()

