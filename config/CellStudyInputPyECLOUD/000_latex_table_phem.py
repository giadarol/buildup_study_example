from __future__ import division, print_function
import os
import argparse
import create_pyecloud_input as cgi

parser = argparse.ArgumentParser()
parser.add_argument('-o', help='Output file', type=str)
parser.add_argument('-l', help='Limit output', action='store_true')
args = parser.parse_args()

if args.o:
    if os.path.isfile(args.o):
        os.remove(args.o)
    def print(*argv, **kwargs):
        __builtins__.print(*argv, **kwargs)
        with open(args.o,'a') as ff:
            __builtins__.print(*argv, file=ff, **kwargs)

header = '\t'+r"""Chamber type &"""
if args.l:
    header += r"""
$R_i$ &
$R_r$ &
$Y_i$ &
$Y_r$ &
$Y_i^*$ &
$Y_r^*$
"""
else:
    header += """
$N_i$ &
$N_r$ &
$N_t$ &
$n_\gamma$ &
refl\_frac &
k\_pe\_st"""

header += \
r"""
\\ \hline
"""
header = header.replace('\n',' ')

for ctr, mat in enumerate((cgi.materials, cgi.materials2)):
    lines = []
    for type_, material in mat.iteritems():
        ri = material['R_i']
        rr = material['R_r']
        yi = material['Y_i']
        yr = material['Y_r']
        yi2 = yi * (1-ri)
        yr2 = yr * (1-rr)
        ni = (1-ri)*yi
        nr = ri*yr
        nt = ni+nr
        k_pe_st, r = cgi.get_k_pe_st_and_r(6.5e12, **material)
        n_gamma = cgi.n_photons.n_photons_meter(6.5e12)


        line = '\t%s' % type_
        if args.l:
            line += '& %.1f &' % (ri*100)
            line += '%.1f &' % (rr*100)
            line += '%.1e &' % yi2
            line += '%.1e' % yr2
            line += '& %.1e &' % yi
            line += '%.1e '  % yr
        else:
            line += '& %.1e &' % ni
            line += '%.1e &' % nr
            line += '%.1e &' % nt
            line += '%.1e &' % n_gamma
            line += '%.2e &' % r
            line += '%.2e' % k_pe_st
        line += r'\\'

        lines.append(line)

    print(header)
    print('\n'.join(lines))

