import pv
import os, re, sys
import time, math, string
from time import sleep
from ca import caput, caget 
from sacla2_Chip_StartUp1 import get_xy
from sacla2_Chip_StartUp1 import make_path_dict
from sacla2_Chip_StartUp1 import scrape_dcparameters

###############################################
# OLD Chip_Collect from SACLA1  experiment    #
# This version last edited 21Oct2016 by DAS   #
###############################################

def get_chip_prog_values(xstart=0, ystart=0, xblocks=9, yblocks=9, coltype=41, block_id=11, num_of_shots=1):
    chip_dict = \
    {'X_NUM_STEPS':  [11, 12],
     'Y_NUM_STEPS':  [12, 12],
     'X_STEP_SIZE':  [13, 0.125],
     'Y_STEP_SIZE':  [14, 0.125],
     #'X_STEP_SIZE':  [13, 0.001],
     #'Y_STEP_SIZE':  [14, 0.001],
     'DWELL_TIME':   [15, 16], #SACLA 15ms + 1ms
     #'DWELL_TIME':   [15, 55], #10Hz test
     #'DWELL_TIME':   [15, 105], #5Hz test
     'X_START':      [16, xstart],
     'Y_START':      [17, ystart],
     'Z_START':      [18, 0],
     'X_NUM_BLOCKS': [20, xblocks],
     'Y_NUM_BLOCKS': [21, yblocks],
     'X_BLOCK_SIZE': [24, 2.2],
     'Y_BLOCK_SIZE': [25, 2.5],
     'COLTYPE':      [26, coltype],
     'N_EXPOSURES':  [30, num_of_shots],
     'BLOCK_ID':     [31, block_id]}
    return chip_dict

def load_motion_program_data(motion_program_dict, map_type):
    print 'Loading prog vars for chip'
    if map_type == '0':
	    prefix = 11
    elif map_type == '1':
	    prefix = 11
    elif map_type == '2':
	    prefix = 12
    elif map_type == '3':
	    prefix = 13
    else:
	    print 'Unknown map_type'

    #for k, v in motion_program_dict.items():
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
    starttime = time.ctime()
    caput(pv.me14e_pmac_str, '!x0y0z0')
    chipname, visit_id, proteinname, num_of_shots, chip_type, map_type, path_key = scrape_dcparameters()

    if map_type == '0' or map_type == '1':
        path_dict = make_path_dict()
	print path_dict.keys()
	print path_key + '_classic'
        print path_dict[path_key + '_classic']
        xstart, ystart, xblocks, yblocks, coltype, path = path_dict[path_key + '_classic']
        # What is block id? Is it used by the motion program?
        block_id = str(string.uppercase.index(path[0][0])+1) + path[0][1]
        print '\n\nChip name is', chipname
        print 'visit_id', visit_id
        print 'proteinname', proteinname
        print 'path_key:', path_key
        print 'path:', path
        print 'xstart', xstart
        print 'ystart', ystart
        print 'xblocks', xblocks
        print 'yblocks', yblocks
        print 'Block ID', block_id 
        print 'coltype', coltype
	print 'num_of_shots', num_of_shots
        chip_prog_dict = get_chip_prog_values(xstart, ystart, xblocks, yblocks, coltype, block_id, num_of_shots)
        print 'Moving to Start'
        caput(pv.me14e_pmac_str, '!x%sy%sz0' %(xstart, ystart))
        sleep(1.5)
        load_motion_program_data(chip_prog_dict, map_type)
        print 'Killing Camera' 
        #caput('ME14E-DI-CAM-01:CAM:Acquire', 'Done')
        #caput('ME14E-DI-CAM-03:CAM:Acquire', 'Done')
        #sleep(0.2)
        caput(pv.me14e_pmac_str, '&2b11r')
        endtime = time.ctime()
        print 3*'\n'
        print 'Summary'
        print 'Chip name:', chipname
        print 'Protein name:', proteinname
        print 'Start time:', starttime
        print 'End time:', endtime
        #caput(pv.me14e_pmac_str, '!x0y0z0')
        print 3*'\n'

    elif map_type == '2': 
        path_dict = make_path_dict()
	print path_dict.keys()
	print path_key + '_classic'
        print path_dict[path_key + '_classic']
        xstart, ystart, xblocks, yblocks, coltype, path = path_dict[path_key + '_classic']
        # What is block id? Is it used by the motion program?
        block_id = str(string.uppercase.index(path[0][0])+1) + path[0][1]
        print '\n\nChip name is', chipname
        print 'visit_id', visit_id
        print 'proteinname', proteinname
        print 'path_key:', path_key
        print 'path:', path
        print 'xstart', xstart
        print 'ystart', ystart
        print 'Block ID', block_id 
        print 'coltype', coltype
	print 'num_of_shots', num_of_shots
        chip_prog_dict = get_chip_prog_values(xstart, ystart, xblocks, yblocks, coltype, block_id, num_of_shots)
        print 'Moving to Start'
        caput(pv.me14e_pmac_str, '!x%sy%sz0' %(xstart, ystart))
        sleep(1.5)
        load_motion_program_data(chip_prog_dict, map_type)
        print 'Killing Camera' 
        #caput('ME14E-DI-CAM-01:CAM:Acquire', 'Done')
        #caput('ME14E-DI-CAM-03:CAM:Acquire', 'Done')
        #sleep(0.2)
        caput(pv.me14e_pmac_str, '&2b12r')
        endtime = time.ctime()
        print 3*'\n'
        print 'Summary'
        print 'Chip name:', chipname
        print 'Protein name:', proteinname
        print 'Start time:', starttime
        print 'End time:', endtime
        #caput(pv.me14e_pmac_str, '!x0y0z0')
        print 3*'\n'
    elif map_type == '3': 
        caput(pv.me14e_pmac_str, '&2b13r')
    else:
	    print 'Unknown map_type'
        
if __name__ == "__main__":
    main()
