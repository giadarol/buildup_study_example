import os
import scipy.io as sio
from scipy.constants import c as clight
import numpy as np

pbunch = 1.1e11
nbunches = 30

dirs = os.listdir('simulations/')
dirs.remove('progress')

lsuccess = [] 
for dd in dirs:
    try:
        data = sio.loadmat('simulations/' + dd +'/Pyecltest.mat')
        
        lam = np.squeeze(data['lam_t_array'])
        t = np.squeeze(data['t'])
        
        totint = np.trapz(lam, t*clight)
        success = (np.abs(totint/pbunch - nbunches) < 0.1)
    except Exception:
	success = False
    lsuccess.append(success)

n_success = np.sum(lsuccess)
print('Successful: %d/%d'%(n_success, len(dirs)))

with open('check.txt', 'w') as fid:
    fid.write('Successful: %d/%d\n'%(n_success, len(dirs)))

