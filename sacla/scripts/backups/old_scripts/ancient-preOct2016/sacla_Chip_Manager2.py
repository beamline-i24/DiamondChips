import pv
import os, re, sys
import math
import string
import subprocess as sb
from time import sleep
from ca import caput, caget 
from sacla_Chip_StartUp2 import get_xy
from sacla_Chip_StartUp2 import make_path_dict

##########################################
# New Chip_Manager for SACLA             #
# This version last edited 04 Mar by DAS #
##########################################

def initialise():
    caput(pv.me14e_stage_x + '.VMAX', 20)
    caput(pv.me14e_stage_y + '.VMAX', 20)
    caput(pv.me14e_stage_z + '.VMAX', 20)
    caput(pv.me14e_stage_x + '.VELO', 20)
    caput(pv.me14e_stage_y + '.VELO', 20)
    caput(pv.me14e_stage_z + '.VELO', 20)
    caput(pv.me14e_stage_x + '.ACCL', 0.00001)
    caput(pv.me14e_stage_y + '.ACCL', 0.00001)
    caput(pv.me14e_stage_z + '.ACCL', 0.00001)
    caput(pv.me14e_stage_x + '.HLM', 30)
    caput(pv.me14e_stage_x + '.LLM', -30)
    caput(pv.me14e_stage_y + '.HLM', 30)
    caput(pv.me14e_stage_y + '.LLM', -30)
    caput(pv.me14e_stage_z + '.HLM', 10)
    caput(pv.me14e_stage_z + '.LLM', -10)
    print 'DONT FORGET TO DO THIS: export EPICS_CA_ADDR_LIST=172.23.190.255'
    print 'DONT FORGET TO DO THIS: export EPICS_CA_AUTO_ADDR_LIST=NO'
    print 'Initialisation Complete'
    return 0

def setdcparameters():
    print '\n\n', 10*'set'
    f = open('/localhome/local/Documents/sacla/parameter_files/setdcparams.txt','w')
    
    chipname = caget(pv.me14e_chipname)
    f.write('chipname \t%s\n' %chipname)
    print '\n\nchipname:', chipname

    visit_id = '/localhome/local/Documents/sacla'
    f.write('visit_id \t%s\n' %visit_id)
    print 'visit_id:', visit_id

    filepath = caget(pv.me14e_filepath)
    f.write('filepath \t%s\n' %filepath)
    print 'filepath:', filepath

    chipcapacity = caget(pv.me14e_chipcapacity)
    f.write('chipcapacity \t%s\n' %chipcapacity)
    print 'chip capacity:', chipcapacity

    blockcapacity = caget(pv.me14e_blockcapacity)
    f.write('blockcapacity \t%s\n' %blockcapacity)
    print 'block capacity:', blockcapacity

    path_key = caget(pv.me14e_dcdetdist)
    f.write('path_key \t%s\n' %path_key)
    print 'path_key:', path_key
    path_dict = make_path_dict()
    
    for ky in path_dict.keys(): print 'keys available', ky
    xstart, ystart, xblocks, yblocks, coltype, path = path_dict[path_key]
    print 'xstart', xstart
    print 'ystart', ystart
    print 'xblocks', xblocks
    print 'yblocks', yblocks
    print 'coltype', coltype
    print 'path', path

    f.close()
    print 10*'set', '\n\n'
    return 0

def moveto(place):
    print place
    if place == 'zero':
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, 0.0)

    elif place == 'A9_al':
        caput(pv.me14e_stage_x, 18.975)  
        caput(pv.me14e_stage_y, 0.0)

    elif place == 'I1_la':
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, -21.375)

    elif place == 'I9_ll':
        caput(pv.me14e_stage_x, 18.975)  
        caput(pv.me14e_stage_y, -21.375)

    elif place == 'yag':
        caput(pv.me14e_stage_x, 43.0)  
        caput(pv.me14e_stage_y, -33.0)
        
   
    elif place == 'chip':
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, 0.0)
        
    elif place == 'load_position':
        caput(pv.me14e_stage_x, 0)  
        caput(pv.me14e_stage_y, 0)
        caput(pv.me14e_stage_z, 40)

    elif place == 'collect_position':
        caput(pv.me14e_stage_x, 0)  
        caput(pv.me14e_stage_y, 0)
        caput(pv.me14e_stage_z, 0)
                
    else:
        print 'Unknown Argument In Method moveto'

def fiducial(point):
    print 'Writing Fiducial File', 30*str(point)
    f = open('/localhome/local/Documents/sacla/parameter_files/fiducial_%s.txt' %point,'w')
    print caget(pv.me14e_stage_x + '.RBV')
    print caget(pv.me14e_stage_y + '.RBV')
    print caget(pv.me14e_stage_z + '.RBV')
    f.write('%1.3f\n' %caget(pv.me14e_stage_x + '.RBV'))
    f.write('%1.3f\n' %caget(pv.me14e_stage_y + '.RBV'))
    f.write('%1.3f\n' %caget(pv.me14e_stage_z + '.RBV'))
    f.close() 
    print 'Writing Fiducial File', 30*str(point)
    return 0
     
def cs_maker():
    fiducial_dict = {}
    fiducial_dict['f1'] = {}
    fiducial_dict['f2'] = {}

    fiducial_dict['f1']['x'] = 18.975 
    fiducial_dict['f1']['y'] = 0 
    fiducial_dict['f1']['z'] = 0 

    fiducial_dict['f2']['x'] = 0 
    fiducial_dict['f2']['y'] = 21.375
    fiducial_dict['f2']['z'] = 0 
    
    #1mm / counts per nanometer (give cts/mm)
    scale = 10000
    #d1, d2 = fiducial_positions
    f1 = open('/localhome/local/Documents/sacla/parameter_files/fiducial_1.txt','r')    
    f1_lines = f1.readlines()
    f1_lines_x = f1_lines[0].rstrip('/n') 
    f1_lines_y = f1_lines[1].rstrip('/n') 
    f1_lines_z = f1_lines[2].rstrip('/n') 
    f1_x = float(f1_lines_x)
    f1_y = float(f1_lines_y)
    f1_z = float(f1_lines_z)

    f2 = open('/localhome/local/Documents/sacla/parameter_files/fiducial_2.txt','r')    
    f2_lines = f2.readlines()
    f2_lines_x = f2_lines[0].rstrip('/n') 
    f2_lines_y = f2_lines[1].rstrip('/n') 
    f2_lines_z = f2_lines[2].rstrip('/n') 
    f2_x = float(f2_lines_x)
    f2_y = float(f2_lines_y)
    f2_z = float(f2_lines_z)
    #Evaluate numbers
    x1factor = (f1_x / fiducial_dict['f1']['x']) *scale
    y1factor = (f1_y / f1_x)                     *scale
    z1factor = (f1_z / f1_x)                     *scale
    x2factor = (f2_x / f2_y)                     *scale
    y2factor = (f2_y / fiducial_dict['f2']['y']) *scale
    z2factor = (f2_z / f2_y)                     *scale
    z3factor = scale

    cs1 = "#1->%+1.5fX%+1.5fY%+1.5fZ" % (x1factor, y1factor, z1factor)
    cs2 = "#2->%+1.5fX%+1.5fY%+1.5fZ" % (-1*x2factor, y2factor, z2factor)
    cs3 = "#3->0X+0Y%+fZ"    % (z3factor)
    print cs1
    print cs2
    print cs3
    caput(pv.me14e_pmac_str, '!x0y0z0')
    sleep(1)
    caput(pv.me14e_pmac_str, '&2')
    sleep(1)
    caput(pv.me14e_pmac_str, cs1)
    sleep(1)
    caput(pv.me14e_pmac_str, cs2)
    sleep(1)
    caput(pv.me14e_pmac_str, cs3)
    sleep(1)
    print 'done'

def main(args):
    if args[1] == 'moveto':
        moveto(args[2])
    elif args[1] == 'fiducial':
        fiducial(args[2])
    elif args[1] == 'cs_maker':
        cs_maker()
    elif args[1] == 'setdcparameters':
        setdcparameters()
    elif args[1] == 'initialise':
        initialise()

    else:
        print 'Unknown Command'
    pass

if  __name__ == '__main__':
    main(sys.argv)
