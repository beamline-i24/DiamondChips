#!/usr/bin/python
import pv, os, re, sys
import time, math, string
from time import sleep
from ca import caput, caget 
from sacla2_Chip_StartUp1_v4 import scrape_parameter_file

##############################################
# COLLECT  COLLECT  COLLECT  COLLECT COLLECT # 
# This version last edited 25Nov2016 by DAS  #
# RLO DNA at beamtime                        #
##############################################

def get_chip_prog_values(chip_type, n_exposures=1):
    if chip_type == '0':
    	print 'This is a Toronto Chip'
    	x_num_steps = 12
    	y_num_steps = 12
    	x_step_size = 0.125
    	y_step_size = 0.125
    	xblocks = 9
    	yblocks = 9
    	x_block_size = 2.2
    	y_block_size = 2.5
    elif chip_type == '1':
    	print 'This is an Oxford Chip'
    	print 'This is a HACK', 30*'HACK'
    	x_num_steps = 60
    	y_num_steps = 1
    	x_step_size = 0.3
    	y_step_size = 0.3
    	xblocks = 1
    	yblocks = 1
    	x_block_size = 40 
    	y_block_size = 40
        #x_num_steps = 20
    	#y_num_steps = 20
    	#x_step_size = 0.125
    	#y_step_size = 0.125
    	#xblocks = 8
    	#yblocks = 8
    	#x_block_size = 3.175
    	#y_block_size = 3.175
    elif chip_type == '2':
    	print 'This is a Hamburg Chip'
    	x_num_steps = 53
    	y_num_steps = 53
    	x_step_size = 0.150
    	y_step_size = 0.150
        if caget(pv.me14e_gp2) == 2:
            print 'Full Mapping on Hamburg -> xblocks = 6'
            xblocks = 6
        else:
    	    xblocks = 3
    	yblocks = 3
    	x_block_size = 8.58
    	y_block_size = 8.58
    elif chip_type == '5':
    	print 'This is a Regina Chip'
    	x_num_steps = 20
    	y_num_steps = 20
    	x_step_size = 0.125
    	y_step_size = 0.125
    	xblocks = 7
    	yblocks = 7
    	x_block_size = 3.70
    	y_block_size = 3.70
    elif chip_type == '4':
    	print 'This is a Bismuth Chip'
    	x_num_steps = caget(pv.me14e_gp6)
        y_num_steps = caget(pv.me14e_gp7)
    	x_step_size = caget(pv.me14e_gp8)
    	y_step_size = x_step_size
    	xblocks = 7
    	yblocks = 7
    	x_block_size = 15 #placeholder
    	y_block_size = 15 #placeholder
    else:
    	print 'Unknown chip_type'
    chip_dict = \
    {'X_NUM_STEPS':  [11, x_num_steps],
     'Y_NUM_STEPS':  [12, y_num_steps],
     'X_STEP_SIZE':  [13, x_step_size],
     'Y_STEP_SIZE':  [14, y_step_size],
     'DWELL_TIME':   [15, 16], #SACLA 15ms + 1ms
     'X_START':      [16, 0],
     'Y_START':      [17, 0],
     'Z_START':      [18, 0],
     'X_NUM_BLOCKS': [20, xblocks],
     'Y_NUM_BLOCKS': [21, yblocks],
     'X_BLOCK_SIZE': [24, x_block_size],
     'Y_BLOCK_SIZE': [25, y_block_size],
     'COLTYPE':      [26, 41],
     'N_EXPOSURES':  [30, n_exposures]}
    return chip_dict

def load_motion_program_data(motion_program_dict, map_type):
    print 'Loading prog vars for chip'
    if map_type == '0':
	    prefix = 11
    elif map_type == '1':
	    prefix = 12
    elif map_type == '2':
	    prefix = 13
    else:
        print 'Unknown map_type'

    for key in sorted(motion_program_dict.keys()):
        v = motion_program_dict[key]
        pvar_base = prefix * 100
        pvar = pvar_base + v[0]  
        value = str(v[1])
        s = 'P' + str(pvar) + '=' + str(value)
        print key, '\t', s 
        caput(pv.me14e_pmac_str, s)
        sleep(0.02)
    print 'done'

def main():
    print 'Starting'
    chip_name, path, protein_name, n_exposures, chip_type, map_type = scrape_parameter_file()
    print '\n\nChip name is', chip_name
    print 'path', path
    print 'protein_name', protein_name
    print 'n_exposures', n_exposures
    print 'chip_type', chip_type
    print 'map type', map_type
    
    if chip_type in ['0', '1', '2', '5']:
        print 'Moving to Start'
        caput(pv.me14e_pmac_str, '!x0y0z0')
        print 'Killing Camera' 
        print 20*'THIS ISNT DONE YET'
       #caput('ME14E-DI-CAM-01:CAM:Acquire', 'Done')
       #caput('ME14E-DI-CAM-03:CAM:Acquire', 'Done')
        if map_type == '0':
    	    print 'Map Type is None'
            chip_prog_dict = get_chip_prog_values(chip_type, n_exposures)
            sleep(1.5)
            load_motion_program_data(chip_prog_dict, map_type)
            caput(pv.me14e_pmac_str, '&2b11r')

        elif map_type == '1': 
    	    print 'Map Type is Mapping Lite'
            chip_prog_dict = get_chip_prog_values(chip_type, n_exposures)
            print 'Moving to Start'
            caput(pv.me14e_pmac_str, '!x0y0z0')
            sleep(1.5)
            load_motion_program_data(chip_prog_dict, map_type)
            caput(pv.me14e_pmac_str, '&2b12r')

        elif map_type == '2':
	    print 'This is full mapping'
            chip_prog_dict = get_chip_prog_values(chip_type, n_exposures)
            print 'Moving to Start'
            caput(pv.me14e_pmac_str, '!x0y0z0')
            sleep(1.5)
            load_motion_program_data(chip_prog_dict, map_type)
            caput(pv.me14e_pmac_str, '&2b13r')
          
        else:
    	    print 'Unknown map_type'
	    print map_type

    if chip_type == '3':
	print 'Bismuth Chip Type 1'
        print 'Not Killing Camera' 
	print 'Getting Prog Dictionary'
        chip_prog_dict = get_chip_prog_values(chip_type, n_exposures)
	print 'Loading Motion Program Data'
        load_motion_program_data(chip_prog_dict, map_type)
	sleep(1)
	print 'Running &2b11r'
        caput(pv.me14e_pmac_str, '&2b11r')
        
    elif chip_type == '4':
	print 'Bismuth Chip Type 2'
        print 'Not Killing Camera' 
	print 'Getting Prog Dictionary'
        chip_prog_dict = get_chip_prog_values(chip_type, n_exposures)
	print 'Loading Motion Program Data'
        load_motion_program_data(chip_prog_dict, map_type)
	sleep(1)
	print 'Running &2b12r'
        caput(pv.me14e_pmac_str, '&2b12r')
'''
    if chip_type in ['3', '4']:
	print 'Bismuth Chip Type'
        print 'Not Killing Camera' 
	print 'Getting Prog Dictionary'
        chip_prog_dict = get_chip_prog_values(chip_type, n_exposures)
	print 'Loading Motion Program Data'
        load_motion_program_data(chip_prog_dict, map_type)
	sleep(1)
	print 'Running &2b11r'
        caput(pv.me14e_pmac_str, '&2b11r')

        print 'Chip name:', chip_name
        print 'Protein name:%s\n' %protein_name
        print 10*'Done'
'''        
if __name__ == "__main__":
    main()
