from __future__ import division, print_function
import os
import re
import gzip

from twiss_file_utils import TfsLine, HalfCell


# Config
vkicker_is_hkicker = False
no_ds_in_mag_len_dict = True
twiss_file_name_tfs = os.path.dirname(os.path.abspath(__file__)) + '/twiss_lhcb1_2.tfs.gz'

re_arc_start = re.compile('(S)\.ARC\.(\d\d)\.B1')
re_arc_end = re.compile('E\.ARC\.\d\d\.B1')
re_sbend_hc = re.compile('^"MB\.[ABC](\d+[LR]\d+)\.B1"$')

re_ds_start = re.compile('(S)\.DS\.([RL]\d)\.B1')
re_ds_end = re.compile('E\.DS\.([RL]\d)\.B1')

# State Machine
look_for_arc = 0
in_arc = 1
in_prefix = 2
in_ds = 3
look_for_ds = 4
status = in_prefix

hc_name = ''
arc = None
half_cell = None
arc_hc_dict = {}


with gzip.open(twiss_file_name_tfs, 'r') as tfs_file:
    for line_n, line in enumerate(iter(tfs_file)):
        split = line.split()
        if status == in_prefix:
            if '$' in line:
                status = look_for_arc
        elif status == look_for_arc:
            if re_arc_start.search(line):
                status = in_arc
                arc = ''.join(re_arc_start.search(line).groups())
                arc_half_cells = []
                this_hc = HalfCell(None)
                arc_hc_dict[arc] = arc_half_cells
        elif status == in_arc:
            if re_arc_end.search(line) is not None:
                status = look_for_arc
            else:
                this_name = split[0]
                info = re_sbend_hc.search(this_name)
                if info is not None:
                    hc_name = info.group(1)
                    if hc_name != this_hc.name:
                        if 1 < this_hc.length < 53:
                            print('length smaller than 53', line_n, this_name)
                        this_hc = HalfCell(hc_name)
                        arc_half_cells.append(this_hc)
                this_line = TfsLine(line, vkicker_is_hkicker)
                this_hc.add_line(this_line)

                if this_hc.length > 54:
                    print('length larger than 54:', line_n, this_name)

# Find out how often each half cell type appears in the LHC
type_occurence_dict = {}
all_hcs = []
for arc, arc_half_cells in arc_hc_dict.iteritems():
    for cell_ctr, hc in enumerate(arc_half_cells):
        all_hcs.append(hc)
        hc.create_dict()
        hc.round_dict(precision=2)
        for key, subdict in type_occurence_dict.iteritems():
            if hc.len_type_dict == subdict['dict']:
                subdict['n'] += 1
                subdict['cells'].append((arc, hc.name, cell_ctr))
                break
        else:
            type_occurence_dict[hc.name] = {
                    'dict': hc.len_type_dict,
                    'n': 1, 'cell': hc,
                    'cells': [(arc, hc.name, cell_ctr)]}

def insert_to_dict(Dict, key, length):
    if key not in Dict:
        Dict[key] = {}
    if length not in Dict[key]:
        Dict[key][length] = 0
    Dict[key][length] += 1


mag_len_dict = {}
single_element_length_dict = {}
for arc, arc_half_cells in arc_hc_dict.iteritems():
    for hc in arc_half_cells:
        if not no_ds_in_mag_len_dict or no_ds_in_mag_len_dict and hc.length > 53:
            for key, length in hc.len_type_dict.iteritems():
                if type(length) is not list:
                    insert_to_dict(mag_len_dict, key, length)
                    #if key not in ('DRIFT', 'Total_sdiff', 'Total'):
                    #    try:
                    #        new_length = length / hc.len_type_dict['order'].count(key)
                    #    except:
                    #        print(key, hc.len_type_dict['order'])
                    #        raise
                    #    insert_to_dict(single_element_length_dict, key, new_length)

for cell in all_hcs:
    lengths = cell.len_type_dict['length']
    types = cell.len_type_dict['order']
    for type_, length in zip(types, lengths):
        length = round(length, 2)
        insert_to_dict(single_element_length_dict, type_, length)

