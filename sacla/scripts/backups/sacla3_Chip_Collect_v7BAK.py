#!/usr/bin/python
import numpy as np
import pv, os, re, sys
import time, math, string
from time import sleep
from ca import caput, caget 
import logging as lg
#import setup_beamline as sup
from sacla3_Chip_StartUp_v7 import scrape_parameter_file
from sacla3_Chip_StartUp_v7 import get_format

lg.basicConfig(format='%(asctime)s %(levelname)s:   \t%(message)s',level=lg.DEBUG, filename='SACLA3v7.log')
##############################################
# COLLECT  COLLECT  COLLECT  COLLECT COLLECT # 
# This version last edited 03Sep2017 by DAS  #
# Prep for SACLA3                            #
##############################################

def flush_print(text):
    sys.stdout.write(str(text))
    sys.stdout.flush()

def get_chip_prog_values(chip_type, location, exptime=16, n_exposures=1):
    #### Hack for sacla3 to bismuth chip type for oxford inner
    if chip_type =='3':
            chip_type = '1'
    if chip_type in ['0','1','2','5']:
        xblocks, yblocks, x_num_steps, y_num_steps, w2w, b2b_horz, b2b_vert = get_format(chip_type)
        x_step_size = w2w
        y_step_size = w2w
        x_block_size = ((x_num_steps - 1) * w2w) + b2b_horz
        y_block_size = ((y_num_steps - 1) * w2w) + b2b_vert

        """ 
        print 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
        print x_num_steps
        print y_num_steps
        print xblocks
        print yblocks
        print w2w
        print b2b_horz
        print b2b_vert
        print x_block_size
        print y_block_size
        print 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
        '0' = 'Toronto' = [9, 9, 12, 12, 0.125, 2.2  , 2.5  ]
        '1' = 'Oxford ' = [8, 8, 20, 20, 0.125, 3.175, 3.175]
        '2' = 'Hamburg' = [3, 3, 53, 53, 0.150, 8.58 , 8.58 ]
        '5' = 'Regina ' = [7, 7, 20, 20, 0.125, 3.7  , 3.7  ]
        """ 

    if chip_type == '2':
        if caget(pv.me14e_gp2) == 2:
            print 'Full Mapping on Hamburg -> xblocks = 6'
            xblocks = 6
        else:
    	    xblocks = 3

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
     'DWELL_TIME':   [15, exptime], #SACLA 15ms + 1ms
     'X_START':      [16, 0],
     'Y_START':      [17, 0],
     'Z_START':      [18, 0],
     'X_NUM_BLOCKS': [20, xblocks], 
     'Y_NUM_BLOCKS': [21, yblocks],
     'X_BLOCK_SIZE': [24, x_block_size],
     'Y_BLOCK_SIZE': [25, y_block_size],
     'COLTYPE':      [26, 41],
     'N_EXPOSURES':  [30, n_exposures]}

    if location == 'i24': 
        chip_dict['DWELL_TIME'][1] = 1000 * float(exptime)

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
    sleep(0.2)
    print 'done'

def start_i24():
    print 'Starting i24'
    start_time = time.ctime()
    run_num = caget(pv.pilat_filenumber)
    print 80*'-', run_num
    chip_name, visit, sub_dir, n_exposures, chip_type, map_type, exptime, \
                                        dcdetdist = scrape_parameter_file(location='i24')
    sup.beamline('collect')
    print 'hello', dcdetdist, type(dcdetdist)
    sup.beamline('quickshot', [dcdetdist])

    if map_type == '0':
        chip_format = get_format(chip_type)[:4]
        total_numb_imgs = np.prod(chip_format)

    elif map_type == '1':
        chip_format = get_format(chip_type)[2:4]
        block_count = 0
        f = open('/dls_sw/i24/scripts/fastchips/litemaps/currentchip.map', 'r')
        for line in f.readlines():
            entry = line.split()
            if entry[2] == '1':
                block_count +=1
        f.close()
        print 'block_count', block_count
        print chip_format
        ####################
        n_exposures  = caget(pv.me14e_gp3)
        print n_exposures
        ####################
        #total_numb_imgs = np.prod(chip_format) * block_count
        total_numb_imgs = np.prod(chip_format) * block_count * n_exposures
        print 'Total number of images', total_numb_imgs

    elif map_type == '2':
        print 'FIX ME, Im not set up for full mapping '

    else:
        print 'Unknown map type'

    print 'total_numb_imgs' , total_numb_imgs, '\n\n\n' 
    filepath = visit + sub_dir
    filename = chip_name 
    #print 'AAAAAAAAAAAAAAAAAAAAA', filepath, filename
    sup.pilatus('fastchip', [filepath, filename, total_numb_imgs, exptime])
    #sup.pilatus('fastchip-hatrx', [filepath, filename, total_numb_imgs, exptime])
    sup.zebra1('fastchip')

    print 'Acquire Region'
    caput(pv.pilat_acquire, '1')        # Arm pilatus
    caput(pv.zebra1_pc_arm_out, '1')    # Arm zebra
    caput(pv.zebra1_soft_in_b1, '1')    # Open fast shutter (zebra gate)
    caput(pv.pilat_filename, filename)
    time.sleep(1.5)
    return start_time

def start_sacla():
    print 'Starting SACLA'
    start_time = time.ctime()
    chip_name, sub_dir, n_exposures, chip_type, map_type = scrape_parameter_file(location='SACLA')
    #### Hack for sacla3 to bismuth chip type for oxford inner
    if str(chip_type) =='3':
            chip_type = '1'
    if map_type == '0':
        chip_format = get_format(chip_type)[:4]
        total_numb_imgs = np.prod(chip_format)

    elif map_type == '1':
        chip_format = get_format(chip_type)[2:4]
        block_count = 0
        f = open('/localhome/local/Documents/sacla/parameter_files/currentchip.map', 'r')
        for line in f.readlines():
            entry = line.split()
            if entry[2] == '1':
                block_count +=1
        f.close()
        print 'block_count', block_count
        print chip_format
        ####################
        n_exposures  = caget(pv.me14e_gp3)
        print n_exposures
        ####################
        #total_numb_imgs = np.prod(chip_format) * block_count * n_exposures
        #print 'Total number of images', total_numb_imgs

    elif map_type == '2':
        print 'FIX ME, Im not set up for full mapping '

    else:
        print 'Unknown map type'

    return start_time

def finish_i24():
    print 'Finishing i24'
    caput(pv.zebra1_soft_in_b1, '0')          # Close the fast shutter
    caput(pv.zebra1_pc_arm_out, '0')          # Disarm the zebra
    sleep(0.2)
    sup.zebra1('return-to-normal')
    sup.pilatus('return-to-normal')
    caput(pv.me14e_pmac_str, '!x0y0z0')
    end_time = time.ctime()
    return end_time

def finish_sacla():
    print 'Finishing SACLA'
    caput(pv.me14e_pmac_str, '!x0y0z0')
    end_time = time.ctime()
    return end_time

def get_prog_num(chip_type, map_type):
    #### Hack for sacla3 to bismuth chip type for oxford inner
    if str(chip_type) =='3':
            chip_type = '1'
    if chip_type in ['0', '1', '2', '5']:
        if map_type == '0':
    	    print 'Map Type is None'
            return 11
        elif map_type == '1': 
    	    print 'Map Type is Mapping Lite'
            return 12
        elif map_type == '2':
	    print 'Map Type is FULL'
            return 13
        else:
    	    print 'Unknown map_type'
	    print map_type
            return 0

    elif chip_type == '3':
	print 'Bismuth Chip Type 1'
        return 11

    elif chip_type == '4':
	print 'Bismuth Chip Type 2'
        return 12
    else:
        print 'Unknown Chip Type'

def main(location='i24'):
    print 'Location is', location, 'Starting'
    # ABORT BUTTON 
    caput(pv.me14e_gp9, 0)

    if location == 'i24':
        chip_name, visit, sub_dir, n_exposures, chip_type, map_type, exptime, \
                                        dcdetdist = scrape_parameter_file(location='i24')
        print 'exptime', exptime
        print 'visit', visit
        print 'dcdetdist', dcdetdist
    else:
        chip_name, sub_dir, n_exposures, chip_type, map_type = scrape_parameter_file(location='SACLA')

    print '\n\nChip name is', chip_name
    print 'sub_dir', sub_dir
    print 'n_exposures', n_exposures
    print 'chip_type', chip_type
    print 'map type', map_type
    print 'Getting Prog Dictionary'
    #### Hack for sacla3 to bismuth chip type for oxford inner
    lg.info('CHIP_COLLECT\tMain:Hack for SACLA3')
    if str(chip_type) =='3':
            chip_type = '1'
    if location =='i24':
	chip_prog_dict = get_chip_prog_values(chip_type, location, exptime=exptime, n_exposures=n_exposures)
    else:
    	chip_prog_dict = get_chip_prog_values(chip_type, location, n_exposures=n_exposures)
    print 'Loading Motion Program Data'
    load_motion_program_data(chip_prog_dict, map_type)

    if location == 'i24':
        start_time = start_i24()
    elif location == 'SACLA':
        start_time = start_sacla()
    else:
        print 'Something here... start_time = start_sacla()' 
        #caput('ME14E-DI-CAM-01:CAM:Acquire', 'Done')
        #caput('ME14E-DI-CAM-03:CAM:Acquire', 'Done')

    print 'Moving to Start'
    caput(pv.me14e_pmac_str, '!x0y0z0')
    sleep(3.5)
    
    prog_num = get_prog_num(chip_type, map_type)
    print 'Resting'
    sleep(1.0)
    print 'pmacing'
    caput(pv.me14e_pmac_str, '&2b%sr' %prog_num)
    print 'Resting'
    sleep(1.0)

    while True:
        # me14e_gp9 is the ABORT button
        if caget(pv.me14e_gp9) == 0:
	    i = 0
            text_list = ['|', '/', '-', '\\']
	    while True:
		line_of_text = '\r\t\t\t Waiting   ' + 30*('%s' %text_list[i%4])
		flush_print(line_of_text)
		sleep(0.5)
                i += 1
		if caget(pv.me14e_gp9) != 0:
		    print 50*'ABORTED '
                    caput(pv.me14e_pmac_str, 'A')
                    sleep(1.0)
                    caput(pv.me14e_pmac_str, 'P2401=0')
		    break
                if caget(pv.me14e_scanstatus) == 0:
		    print '\n', 20*'DONE '
		    break
                #if caget(pv.pilat_acquire) == 'Done':
		#    print '\n', 20*'DONE '
		#    break
	else:
	    break
	break

    if location == 'i24':
        end_time = finish_i24()
    if location == 'SACLA':
        end_time = finish_sacla()

    print 'Start time:', start_time
    print 'End time:  ', end_time

if __name__ == "__main__":
    main(location='SACLA')
