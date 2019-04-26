import os
import shutil as sht
import numpy as np

import replaceline as rl
import CellStudyInputPyECLOUD.create_pyecloud_input as cpi


tag_prefix = 'lhc'
	
tobecopied = 'job.job beam.beam machine_parameters.input secondary_emission_parameters.input simulation_parameters.input cos_sq_inv_CDF.mat'

current_dir = os.getcwd()
study_folder =  current_dir.split('/config')[0]
workspace_folder = os.path.abspath('../../')


scan_folder = study_folder+'/simulations'

from scenarios_NxNy_Dt import machines

del_max_vect = np.arange(1.,2.0, 0.1)
fact_beam_vect = [1.1e11]
bl_4_sigma_s_vect = [1e-9]
beams_list = ['450GeV']
devices_sim = ['ArcDipReal']

#debug
#sht.rmtree(scan_folder)

# photoemission model: 'optimistic' or 'conservative'
#model = 'optimistic'
#if model == 'optimistic':
#    material = cpi.optimistic['Cu co-lam. with sawtooth']
#elif model == 'conservative':
#    material = cpi.conservative['Cu co-lam. with sawtooth']  


os.mkdir(scan_folder)
os.mkdir(scan_folder+'/progress')

launch_file_lines = []
launch_file_lines +=['#!/bin/bash\n']

prog_num=0

for machine_name in machines.keys():
	machine = machines[machine_name]
	beams = machine['beams']
	devices = machine['devices']
	for device_name in devices_sim:
		device = devices[device_name]
		for beam_name in beams_list:
			beam = beams[beam_name]
			ener_curr = beam['energy']
                        # calculate photoemission parameters
                        #k_pe_st_curr = cpi.get_complete_photoemission_info(ener_curr, R_i = material['R_i'], Y_i = material['Y_i'], Y_r = material['Y_r'])['k_pe_st']
                        #refl_frac_curr =  cpi.get_complete_photoemission_info(ener_curr, R_i = material['R_i'], Y_i = material['Y_i'], Y_r = material['Y_r'])['refl_frac']
			#sigmaz = beam['sigmaz']
			config = device['config'][beam_name]
			for fact_beam in fact_beam_vect:
					for del_max in del_max_vect:
						for bl_4_sigma_s in bl_4_sigma_s_vect:
								prog_num +=1
								current_sim_ident= '%s_%s_%s_sey%1.2f_%.1fe11ppb_bl_%.2fns'%(machine_name, device_name, beam_name, del_max,fact_beam/1e11,bl_4_sigma_s/1e-9)
								sim_tag = tag_prefix+'%03d'%prog_num
								print sim_tag, current_sim_ident
								current_sim_folder = scan_folder+'/'+current_sim_ident
								os.mkdir(current_sim_folder)
								

								rl.replaceline_and_save(fname = 'secondary_emission_parameters.input',
								 findln = 'del_max =', newline = 'del_max = %f\n'%del_max)
								 
								#~ rl.replaceline_and_save(fname = 'beam.beam',
								 #~ findln = 'sigmaz =', newline = 'sigmaz = %e\n'%sigmaz)
								 
								rl.replaceline_and_save(fname = 'beam.beam',
								 findln = 'sigmaz =', newline = 'sigmaz = %e/4.*299792458.\n'%bl_4_sigma_s)			

								rl.replaceline_and_save(fname = 'beam.beam',
								 findln = 'fact_beam =', newline = 'fact_beam = %e\n'%fact_beam)							 
								
							
								rl.replaceline_and_save(fname = 'machine_parameters.input',
								 findln = 'betafx =', newline = 'betafx = %.2f\n'%(device['betafx']))

								rl.replaceline_and_save(fname = 'machine_parameters.input',
								 findln = 'betafy =', newline = 'betafy = %.2f\n'%(device['betafy']))
								
								B_multip = [device['B0y_per_eV']*ener_curr]
								
								if device['fact_Bmap_per_eV']>0.:
									B_multip.append(device['fact_Bmap_per_eV']*ener_curr)
								
								rl.replaceline_and_save(fname = 'machine_parameters.input',
								 findln = 'B_multip =', newline = 'B_multip = %s\n'%repr(B_multip))

								rl.replaceline_and_save(fname = 'machine_parameters.input',
								 findln = 'chamb_type =', newline = 'chamb_type = %s\n'%repr(device['chamb_type']))							
								
								rl.replaceline_and_save(fname = 'machine_parameters.input',
								 findln = 'x_aper =', newline = 'x_aper = %e\n'%device['x_aper'])						
								
								rl.replaceline_and_save(fname = 'machine_parameters.input',
								 findln = 'y_aper =', newline = 'y_aper = %e\n'%device['y_aper'])						
								
								rl.replaceline_and_save(fname = 'machine_parameters.input',
								 findln = 'filename_chm =', newline = 'filename_chm = %s\n'%repr(device['filename_chm']))							
                                                                #rl.replaceline_and_save(fname = 'machine_parameters.input',
                                                                # findln = 'k_pe_st =', newline = 'k_pe_st = %e\n'%k_pe_st_curr)

                                                                #rl.replaceline_and_save(fname = 'machine_parameters.input',
                                                                # findln = 'refl_frac =', newline = 'refl_frac = %e\n'%refl_frac_curr)								
								rl.replaceline_and_save(fname = 'beam.beam',
								 findln = 'beam_field_file =', newline = 'beam_field_file = %s\n'%repr(config['beam_field_file']))
								
								rl.replaceline_and_save(fname = 'beam.beam',
								 findln = 'Nx =', newline = 'Nx = %s\n'%repr(config['Nx']))					
								
								rl.replaceline_and_save(fname = 'beam.beam',
								 findln = 'Ny =', newline = 'Ny = %s\n'%repr(config['Ny']))						
								
								rl.replaceline_and_save(fname = 'beam.beam',
								 findln = 'nimag =', newline = 'nimag = %s\n'%repr(config['nimag']))						
								
								rl.replaceline_and_save(fname = 'beam.beam',
								 findln = 'Dh_beam_field =', newline = 'Dh_beam_field = %s\n'% repr(config['Dh_beam_field']))
														
								rl.replaceline_and_save(fname = 'beam.beam',
								 findln = 'energy_eV = ', newline = 'energy_eV = %e\n'%ener_curr)						
								
								rl.replaceline_and_save(fname = 'machine_parameters.input',
								 findln = 'N_sub_steps =', newline = 'N_sub_steps = %d\n'%config['N_sub_steps'])
								
								rl.replaceline_and_save(fname = 'simulation_parameters.input',
								 findln = 'Dt =', newline = 'Dt = %e\n'%config['Dt'])

					 
								 
								rl.replaceline_and_save(fname = 'simulation_parameters.input',
								 findln = 'logfile_path =', newline = 'logfile_path = '+'\''+ current_sim_folder+'/logfile.txt'+'\''+'\n')
								 
								rl.replaceline_and_save(fname = 'simulation_parameters.input',
								 findln = 'progress_path =', newline = 'progress_path = '+'\'' + scan_folder+'/progress/' +sim_tag+'\''+ '\n')
							
								rl.replaceline_and_save(fname = 'simulation_parameters.input',
								 findln = 'stopfile =', newline = 'stopfile = \''+scan_folder+'/progress/stop\'\n')


								if type(device['B_map_file']) is str:
									if '.mat' in device['B_map_file']:
										sht.copy(device['B_map_file'],current_sim_folder)
									
								if type(device['filename_chm']) is str:
									if '.mat' in device['filename_chm']:
										sht.copy(device['filename_chm'],current_sim_folder)

								rl.replaceline_and_save(fname = 'job.job',
													 findln = 'CURRDIR=/',
													 newline = 'CURRDIR='+current_sim_folder)
								rl.replaceline_and_save(fname = 'job.job',
													 findln = 'WORKFOLDER=',
													 newline = 'WORKFOLDER='+workspace_folder)
													 
								os.system('cp -r %s %s'%(tobecopied, current_sim_folder))
								launch_file_lines += ['bsub -L /bin/bash -J '+ sim_tag + 
										' -o '+ current_sim_folder+'/STDOUT',
										' -e '+ current_sim_folder+'/STDERR',
										' -q 2nd < '+current_sim_folder+'/job.job\n', 'bjobs\n']
									
								
	
with open(study_folder+'/run', 'w') as fid:
	fid.writelines(launch_file_lines)
os.chmod(study_folder+'/run',0755)


import htcondor_config as htcc
htcc.htcondor_config(scan_folder, time_requirement_days=2.)
