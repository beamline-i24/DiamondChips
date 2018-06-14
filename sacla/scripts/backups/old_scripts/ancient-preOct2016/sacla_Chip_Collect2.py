import pv
import os, re, sys
import time, math, string
from time import sleep
from ca import caput, caget 
from shutil import copyfile
from sacla_Chip_StartUp2 import get_xy
from sacla_Chip_StartUp2 import make_path_dict
from sacla_Chip_StartUp2 import scrape_dcparameters

########################################
# NEW Chip_Collection for SACLA        #
# This version last edited 04 Mar, DAS #
#########################################

def get_chip_prog_values(xstart=0, ystart=0, xblocks=9, yblocks=9, coltype=41):
    chip_dict = \
    {'X_NUM_STEPS':  [11, 12],
     'Y_NUM_STEPS':  [12, 12],
     'X_STEP_SIZE':  [13, 0.125],
     'Y_STEP_SIZE':  [14, 0.125],
     'DWELL_TIME':   [15, 16], #SACLA 15ms + 1ms
     'X_START':      [16, xstart],
     'Y_START':      [17, ystart],
     'Z_START':      [18, 0],
     'X_NUM_BLOCKS': [20, xblocks],
     'Y_NUM_BLOCKS': [21, yblocks],
     'X_BLOCK_SIZE': [24, 2.2],
     'Y_BLOCK_SIZE': [25, 2.5],
     'COLTYPE':      [26, coltype]}
    return chip_dict

def load_motion_program_data(motion_program_dict):
    print 'Loading prog vars for chip'
    for k, v in motion_program_dict.items():
        pvar = 1100 + v[0]  
        value = str(v[1])
        s = 'P' + str(pvar) + '=' + str(value)
	print 'loaded onto PMAC:', s 
        caput(pv.me14e_pmac_str, s)
        sleep(0.02)
    print 'done'

def main():
    print 'Starting'
    starttime = time.ctime()
    caput(pv.me14e_pmac_str, '!x0y0z0')

    path_dict = make_path_dict()
    chipname, visit_id, filepath, chipcapacity, blockcapacity, path_key = scrape_dcparameters()
    xstart, ystart, xblocks, yblocks, coltype, path = path_dict[int(path_key)]
    print '\n\nChip name is', chipname
    print 'visit_id', visit_id
    print 'filepath', filepath
    print 'chipcapacity', chipcapacity
    print 'blockcapacity', blockcapacity
    print 'path_key:', path_key
    print 'path:', path
    print 'xstart', xstart
    print 'ystart', ystart
    print 'xblocks', xblocks
    print 'yblocks', yblocks
    print 'coltype', coltype
    chip_prog_dict = get_chip_prog_values(xstart, ystart, xblocks, yblocks, coltype)

    print 'Moving to Start'
    caput(pv.me14e_pmac_str, '!x%sy%sz0' %(xstart, ystart))
    sleep(1)

    load_motion_program_data(chip_prog_dict)
    caput(pv.me14e_pmac_str, '&2b11r')
    endtime = time.ctime()
    print 3*'\n'
    print 'Summary'
    print 'Chip name:', chipname
    print 'Filepath:', filepath
    print 'Number of images collected:', chipcapacity
    print 'Start time:', starttime
    print 'End time:', endtime
    print 3*'\n'

if __name__ == "__main__":
    main()
