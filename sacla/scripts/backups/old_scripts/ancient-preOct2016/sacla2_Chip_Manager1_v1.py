import pv
import os, re, sys
import math
import string
from time import sleep
from ca import caput, caget 
from sacla2_Chip_StartUp1 import get_xy
from sacla2_Chip_StartUp1 import make_path_dict
from sacla2_Chip_StartUp1 import scrape_dcparameters

###########################################
# OLD Chip_Manager from SACLA1  experiment    #
# This version last edited 21Oct2016 by DAS   #
###########################################

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
    print 'Have you tried autowriting to the GPs?'
    print 'DONT FORGET TO DO THIS: export EPICS_CA_ADDR_LIST=172.23.190.255'
    print 'DONT FORGET TO DO THIS: export EPICS_CA_AUTO_ADDR_LIST=NO'
    print 'Initialisation Complete'

def setdcparameters():
    print '\n\n', 10*'set', '\n'
    path_dict = make_path_dict()
    print 'keys available'
    for ky in sorted(path_dict.keys()): 
        print ky,
    path = '/localhome/local/Documents/sacla/parameter_files/'
    print '\n\nSaving to', path

    f = open(path + 'setdcparams.txt','w')
    chipname = caget(pv.me14e_chipname)
    f.write('chipname \t%s\n' %chipname)
    print 'chipname:', chipname

    visit_id = '/localhome/local/Documents/sacla'
    f.write('visit_id \t%s\n' %visit_id)
    print 'visit_id:', visit_id

    proteinname = caget(pv.me14e_filepath)
    f.write('proteinname \t%s\n' %proteinname)
    print 'proteinname:', proteinname

    num_of_shots = caget(pv.me14e_gp3) 
    f.write('num_of_shots \t%s\n' %num_of_shots)
    print 'num_of_shots', num_of_shots

    chip_type = caget(pv.me14e_gp1) 
    f.write('chip_type \t%s\n' %chip_type)
    print 'chip_type', chip_type

    map_type = caget(pv.me14e_gp2) 
    f.write('map_type \t%s\n' %map_type)
    print 'map_type', map_type

    if map_type == 1:
        path_key = caget(pv.me14e_gp4)
    else:
        path_key = 99

    f.write('path_key \t%s\n' %path_key)
    print 'path_key:', path_key, '\n', 30*('%i ' %path_key)
    f.close()

    xstart, ystart, xblocks, yblocks, coltype, path = path_dict[path_key]
    print '\nxstart', xstart
    print 'ystart', ystart
    print 'xblocks', xblocks
    print 'yblocks', yblocks
    print 'coltype', coltype
    print 'path', path[0], '------>', path[-1]
    print 'Number of Blocks', len(path)
    print '\n', 10*'set', '\n\n'

def setchipparameters():
    path = '/localhome/local/Documents/sacla/parameter_files/'
    print '\n\nSaving to', path + 'currentchip.map'
    f = open(path + 'currentchip.map','w')
    #Currently a bit of a hack. Change to a loop. While n is less then nblocks.
    print 'Printing only blocks with block_val == 1'
    for x in range(1, 82):
        block_str = 'ME14E-MO-IOC-01:GP%i' %(x+10)
        block_val = caget(block_str) 
        if block_val == 1:
            print block_str, block_val
        line = '%02dstatus    P3%02d1 \t%s\n' %(x, x, block_val)
        f.write(line)
    f.close()
    return 0

def uploadchipparameters():
    path = '/localhome/local/Documents/sacla/parameter_files/'
    f = open(path + 'currentchip.map','r')
    for line in f:
        cols = line.split( )
        pvar = cols[1]
        value = cols[2]
        s = str(pvar) + '=' + str(value)
        print 'set P-variable', s
        caput(pv.me14e_pmac_str, s)
        sleep(0.02)
    print 'done'

def definechipgeometry():
    chipname, visit_id, proteinname, num_of_shots, chip_type, map_type, path_key = scrape_dcparameters()
    path = '/localhome/local/Documents/sacla/parameter_files/'
    if chip_type == '0':
        chipid = 'toronto'
    elif chip_type == '1':
        chipid = 'oxford'
    elif chip_type == '2':
        chipid = 'hamburg'
    f = open(path + chipid + '.chip','r')
    print 'reading', path + chipid + '.chip'
    print 'writing to pmac'
    for line in f:
        cols = line.split( )
        pvar = cols[1]
        value = cols[2]
        s = str(pvar) + '=' + str(value)
        print 'set P-variable', s
        caput(pv.me14e_pmac_str, s)
        sleep(0.02)
    print 'done'

def clear_lite_map():
    print 'Please wait, clearing map'
    for i in range(1, 82):
        pvar = 'ME14E-MO-IOC-01:GP' + str(i + 10)
        caput(pvar, 0)
        sleep(0.02)
    print 'map cleared'
    return 1

def fill_lite_map():
    print 'Please wait, filling map'
    for i in range(1, 82):
        pvar = 'ME14E-MO-IOC-01:GP' + str(i + 10)
        caput(pvar, 1)
        sleep(0.02)
    print 'map filled'
    return 1

def load_lite_map():
    clear_lite_map()
    block_dict = {'A1':'01', 'A2':'02', 'A3':'03', 'A4':'04', 'A5':'05', 'A6':'06','A7':'07', 'A8':'08', 'A9':'09'
                 ,'B1':'18', 'B2':'17', 'B3':'16', 'B4':'15', 'B5':'14', 'B6':'13','B7':'12', 'B8':'11', 'B9':'10'
                 ,'C1':'19', 'C2':'20', 'C3':'21', 'C4':'22', 'C5':'23', 'C6':'24','C7':'25', 'C8':'26', 'C9':'27'
                 ,'D1':'36', 'D2':'35', 'D3':'34', 'D4':'33', 'D5':'32', 'D6':'31','D7':'30', 'D8':'29', 'D9':'28'
                 ,'E1':'37', 'E2':'38', 'E3':'39', 'E4':'40', 'E5':'41', 'E6':'42','E7':'43', 'E8':'44', 'E9':'45'
                 ,'F1':'54', 'F2':'53', 'F3':'52', 'F4':'51', 'F5':'50', 'F6':'49','F7':'48', 'F8':'47', 'F9':'46'
                 ,'G1':'55', 'G2':'56', 'G3':'57', 'G4':'58', 'G5':'59', 'G6':'60','G7':'61', 'G8':'62', 'G9':'63'
                 ,'H1':'72', 'H2':'71', 'H3':'70', 'H4':'69', 'H5':'68', 'H6':'67','H7':'66', 'H8':'65', 'H9':'64'
                 ,'I1':'73', 'I2':'74', 'I3':'75', 'I4':'76', 'I5':'77', 'I6':'78','I7':'79', 'I8':'80', 'I9':'81'}
    path = '/localhome/local/Documents/sacla/litemaps/'
    lite_map_fid = caget(pv.me14e_gp5) + '.lite'
    print 'opening', path + lite_map_fid
    f = open(path + lite_map_fid,'r')
    print 'please wait, loading LITE map'
    for line in f.readlines():
        entry = line.split()
        block_name = entry[0]
        yesno = entry[1]
        block_num = block_dict[block_name] 
        pvar = 'ME14E-MO-IOC-01:GP' + str(int(block_num) + 10)
        print block_name, yesno, pvar
        caput(pvar, yesno)
    print 'Done'

def moveto(place):
    print place
    if place == 'zero':
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, 0.0)

    elif place == 'A9_al':
        caput(pv.me14e_stage_x, +18.975)  
        #caput(pv.me14e_stage_x, -18.975)  
        caput(pv.me14e_stage_y, 0.0)

    elif place == 'I1_la':
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, -21.375)

    elif place == 'I9_ll':
        caput(pv.me14e_stage_x, 18.975)  
        caput(pv.me14e_stage_y, -21.375)

    elif place == 'B2_aa':
        caput(pv.me14e_stage_x, 3.7)  
        caput(pv.me14e_stage_y, -2.45)

    elif place == 'B8_al':
        print 'This is relative to B2_aa as origin!!!'
        caput(pv.me14e_stage_x, 14.575)  
        caput(pv.me14e_stage_y, 0.0)

    elif place == 'H2_la':
        print 'This is relative to B2_aa as origin!!!'
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, -16.375)

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
    path = '/localhome/local/Documents/sacla/parameter_files/'
    x = caget(pv.me14e_stage_x + '.RBV')
    y = caget(pv.me14e_stage_y + '.RBV')
    z = caget(pv.me14e_stage_z + '.RBV')
    print 'Writing Fiducial File', 30*str(point)
    print path
    print '\n'.join([str(x),str(y),str(z)]), '\n'
    f = open(path + 'fiducial_%s.txt' %point, 'w')
    f.write('%1.3f\n' %x)
    f.write('%1.3f\n' %y)
    f.write('%1.3f\n' %z)
    f.close() 
    print 'Writing Fiducial File', 30*str(point)
     
def cs_maker():
    fiducial_dict = {}
    fiducial_dict['f1'] = {}
    fiducial_dict['f2'] = {}

    fiducial_dict['f1']['x'] = 18.975 
    #fiducial_dict['f1']['x'] = 14.575 
    fiducial_dict['f1']['y'] = 0 
    fiducial_dict['f1']['z'] = 0 

    fiducial_dict['f2']['x'] = 0 
    fiducial_dict['f2']['y'] = 21.375
    #fiducial_dict['f2']['y'] = 16.375
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

    cs1 = "#1->%+1.3fX%+1.3fY%+1.3fZ" % (x1factor, y1factor, z1factor)
    cs2 = "#2->%+1.3fX%+1.3fY%+1.3fZ" % (-1*x2factor, 1*y2factor, z2factor)
    cs3 = "#3->0X+0Y%+fZ"    % (z3factor)
    print cs1
    print cs2
    print cs3
    sleep(1)
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
    caput(pv.me14e_pmac_str, '!x0y0z0')
    sleep(1)
    #caput(pv.me14e_pmac_str, '!x-2.2y-2.5z0')
    #sleep(1)
    caput(pv.me14e_pmac_str, '#1hmz#2hmz#3hmz')
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
    elif args[1] == 'setchipparameters':
        setchipparameters()
    elif args[1] == 'uploadchipparameters':
        uploadchipparameters()
    elif args[1] == 'definechipgeometry':
        definechipgeometry()
    elif args[1] == 'load_lite_map':
        load_lite_map()
    elif args[1] == 'clear_lite_map':
        clear_lite_map()
    elif args[1] == 'fill_lite_map':
        fill_lite_map()
    else:
        print 'Unknown Command'
    pass

if  __name__ == '__main__':
    main(sys.argv)
