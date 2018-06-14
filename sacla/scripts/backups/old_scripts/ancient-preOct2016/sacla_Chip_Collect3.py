import pv
import os, re, sys
import time, math, string
from time import sleep
from ca import caput, caget 
from sacla_Chip_StartUp3 import get_xy
from sacla_Chip_StartUp3 import make_path_dict
from sacla_Chip_StartUp3 import scrape_dcparameters

########################################
# NEW Chip_Collection for SACLA        #
# This version last edited at SACLA, DAS/RLO #
#########################################

def get_chip_prog_values(xstart=0, ystart=0, xblocks=9, yblocks=9, coltype=41, block_id=11):
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
     'BLOCK_ID':     [31, block_id]}
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
    chipname, visit_id, proteinname, chipcapacity, blockcapacity, path_key = scrape_dcparameters()
    xstart, ystart, xblocks, yblocks, coltype, path = path_dict[int(path_key)]
    block_id = str(string.uppercase.index(path[0][0])+1) + path[0][1]
    print '\n\nChip name is', chipname
    print 'visit_id', visit_id
    print 'proteinname', proteinname
    print 'chipcapacity', chipcapacity
    print 'blockcapacity', blockcapacity
    print 'path_key:', path_key
    print 'path:', path
    print 'xstart', xstart
    print 'ystart', ystart
    print 'xblocks', xblocks
    print 'yblocks', yblocks
    print 'Block ID', block_id 
    print 'coltype', coltype
    chip_prog_dict = get_chip_prog_values(xstart, ystart, xblocks, yblocks, coltype, block_id)

    print 'Moving to Start'
    caput(pv.me14e_pmac_str, '!x%sy%sz0' %(xstart, ystart))
    sleep(1)

    load_motion_program_data(chip_prog_dict)
    caput(pv.me14e_pmac_str, '&2b11r')
    #caput(pv.me14e_pmac_str, '&2b24r')
    
    #endtime = time.ctime()
    print 3*'\n'
    print 'Summary'
    print 'Chip name:', chipname
    print 'Protein name:', proteinname
    print 'Number of images collected:', chipcapacity
    print 'Start time:', starttime
    #print 'End time:', endtime
    #caput(pv.me14e_pmac_str, '!x0y0z0')
    print 3*'\n'

if __name__ == "__main__":
    main()
