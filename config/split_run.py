import numpy as np

runfilepath = '../run'

list_subfixes = 'ecldcode gianni'.split()

N_subfiles = len(list_subfixes)

with open(runfilepath) as fid:
	lines = fid.readlines()

first = lines[0]

del lines[0]

nlines_per_file = len(lines)/2/N_subfiles*2

for ii in xrange(N_subfiles):
	lines_curr = lines[ii*nlines_per_file:(ii+1)*nlines_per_file]
	if ii == N_subfiles-1:
		lines_curr += lines[(ii+1)*nlines_per_file:]
	with open(runfilepath+'_'+list_subfixes[ii], 'w') as fid:
		fid.writelines([first]+lines_curr)
