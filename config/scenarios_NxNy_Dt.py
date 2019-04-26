ccc = 299792458.

machines = {}


	
########################################################################
# LHC (same used for HL-LHC study)
########################################################################

machines['LHC'] = {}	

# beam definition	
machines['LHC']['beams'] = {}
machines['LHC']['beams']['450GeV']={'energy': 450e9, 'sigmaz':.11}
machines['LHC']['beams']['6500GeV']={'energy': 6500e9, 'sigmaz':0.09}
machines['LHC']['beams']['7000GeV']={'energy': 7000e9, 'sigmaz':0.09}
machines['LHC']['beams']['7500GeV']={'energy': 7500e9, 'sigmaz':0.09}
# component definition
machines['LHC']['devices'] = {}


machines['LHC']['devices']['ArcDipReal'] = {'betafx':85., 'betafy':90., 
									'B_map_file':None, 
									'fact_Bmap_per_eV':0.,
									'B0y_per_eV':8.33/7000e9, 
									'chamb_type':'polyg_cython',
									'x_aper':0.023,  
									'y_aper':0.018,  
									'filename_chm':'LHC_chm_ver.mat'}
machines['LHC']['devices']['ArcDipReal']['config']={\
	'450GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 25e-12},
	'6500GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 25e-12},
	'7000GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 25e-12},
	'7500GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 25e-12}}
	

	
machines['LHC']['devices']['ArcQuadReal'] = {'betafx':85., 'betafy':90., 
									'B_map_file': 'analytic_qaudrupole_unit_grad', 
									'fact_Bmap_per_eV':12.1/450e9,
									'B0y_per_eV':0., 
									'chamb_type':'polyg_cython',
									'x_aper':0.023,  
									'y_aper':0.018,  
									'filename_chm':'LHC_chm_ver.mat'}
machines['LHC']['devices']['ArcQuadReal']['config']={\
	'450GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 10e-12},
	'6500GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 5e-12},
	'7000GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 5e-12},
	'7500GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 5e-12}}


machines['LHC']['devices']['ArcDriftReal'] = {'betafx':85., 'betafy':90., 
									'B_map_file':None, 
									'fact_Bmap_per_eV':0.,
									'B0y_per_eV':0., 
									'chamb_type':'polyg_cython',
									'x_aper':0.023,  
									'y_aper':0.018,  
									'filename_chm':'LHC_chm_ver.mat'}
machines['LHC']['devices']['ArcDriftReal']['config']={\
	'450GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 25e-12},
	'6500GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 25e-12},
	'7000GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 25e-12},
	'7500GeV':{'beam_field_file':'computeFD', 'Nx':None,'Ny':None,'nimag':None, 'Dh_beam_field': .1e-3, 'N_sub_steps':5, 'Dt': 25e-12}}
