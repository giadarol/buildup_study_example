from __future__ import division
import numpy as np

import info_on_half_cells as info
import create_pyecloud_input as cpi


mag_len_dict = info.mag_len_dict
n_cells = sum(mag_len_dict['Total'].values())

madx_key_dict ={
    'DRIFT' :       'Drift',
    'HKICKER':      'MCBH',
    'VKICKER':      'MCBV',
    #'MULTIPOLE':    'MQ',
    'OCTUPOLE':     'MO',
    'QUADRUPOLE':   'MQ',
    'SBEND':        'MB',
    'SEXTUPOLE':    'MS',
}


mag_len_dict_avg = {}
for key, len_occurence_dict in mag_len_dict.iteritems():
    if key in madx_key_dict:
        lengths = np.array(len_occurence_dict.keys())
        occurences = np.array(len_occurence_dict.values())
        new_key = madx_key_dict[key]
        if new_key in mag_len_dict_avg:
            old_val = mag_len_dict_avg[new_key]
            print new_key
        else:
            old_val = 0
        mag_len_dict_avg[new_key] = np.sum(lengths*occurences)/n_cells + old_val
    elif 'Total' in key:
        pass
    else:
        print('Neglected: %s' % key)


typical_dict = info.type_occurence_dict['13R2']['dict']
typical_dict2 = {}

for key in typical_dict.keys():
    if key in madx_key_dict:
        typical_dict2[madx_key_dict[key]] = typical_dict[key]


# Alternating focussing and defocussing sextupoles
mag_len_dict_avg['MS2'] = mag_len_dict_avg['MS']/2
mag_len_dict_avg['MS'] = mag_len_dict_avg['MS']/2

def format_number(list_, device):
    if list_ is None:
        return '-'
    arr = np.array(list_)
    if np.all(arr == 0):
        return '-'

    number = arr[-1]
    if 1 <= number <= 10:
        str_ = '%.2f ' % number
    else:
        str_ = ('%.2e' % number).replace('e+0', '$\cdot 10^{')+'}$ '

    try:
        str_ += dev_grad_dict[device]
    except KeyError:
        str_ += 'T'

    return str_

if __name__ == '__main__':
    # Prints out a latex table of magnets
    magnets = cpi.magnets

    devices = (
        'Drift',
        'MB',
        'MCBH',
        'MCBV',
        'MQ',
        'MS',
        'MS2',
        'MO',
    )

    dev_title_dict = {
        'Drift' : 'Drift',
        'MB'    : 'Main Bend (MB)',
        'MCBH'  : 'Horizontal corrector (MCBH)',
        'MCBV'  : 'Vertical corrector (MCBV)',
        'MQ'    : 'Main quadrupole (MQ)',
        'MS'    : 'Main sextupole (MS)',
        'MS2'   : 'Main sextupole (MS2)',
        'MO'    : 'Main octupole (MO)'
    }

    dev_grad_dict = {
        'MQ' : 'T/m',
        'MS' : 'T/m$^2$',
        'MS2' : 'T/m$^2$',
        'MO' : 'T/m$^3$',
    }

    single_element_length_dict = {}
    for key, subdict in info.single_element_length_dict.iteritems():
        ordered = sorted(subdict.keys(), key=lambda x: subdict[x])
        print key, ordered[:2]
        try:
            single_element_length_dict[madx_key_dict[key]] = max(subdict.keys())
        except:
            pass
    single_element_length_dict['MS2'] = single_element_length_dict['MS']
    single_element_length_dict['Drift'] = '-'

    print('\n')
    leader = ' '*3*4
    tot_length = 0
    for key in devices:
        subdict = mag_len_dict_avg[key]
        B_multip, B_skew = cpi.get_b_multip(6.5e12, **magnets[key])
        length = mag_len_dict_avg[key]
        try:
            single_element_length = '%.2f' % single_element_length_dict[key]
        except (KeyError, TypeError):
            single_element_length = '-'
        B_skew_str = format_number(B_skew, key)
        B_multip_str = format_number(B_multip, key)

        if B_multip_str == '-':
            if B_skew_str != '-':
                B_str = B_skew_str + ' (skew)'
            else:
                B_str = '-'
        elif B_skew_str == '-':
            B_str = B_multip_str
        print leader + r'%s & %s & %.2f & %s \\' % (dev_title_dict[key], single_element_length, length, B_str)
        tot_length += length

    print '\nTotal length: %.2f' % tot_length



