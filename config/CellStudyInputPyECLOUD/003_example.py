import create_pyecloud_input as cpi



energy_eV = 6500e9
model = 'optimistic' # choose between "optimistic" and "conservative"





if model == 'optimistic':
    material = cpi.optimistic['Cu co-lam. with sawtooth']
elif model == 'conservative':
    material = cpi.conservative['Cu co-lam. with sawtooth']
else:
    raise ValueError('What?!')
    
dict_phem = cpi.get_complete_photoemission_info(energy_eV, 
            R_i = material['R_i'], Y_i = material['Y_i'], Y_r = material['Y_r'])


print '\nModel: %s Energy: %.1f GeV\n'%(model, energy_eV/1e9)            
for kk in sorted(dict_phem):
    print kk, dict_phem[kk]
    


