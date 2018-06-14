#!/usr/bin/python
import pv, os, re, sys
import math, time, string
import numpy as np
from time import sleep
from ca import caput, caget
import Chip_StartUp_v5 as startup
import Chip_Mapping_v5 as mapping

##############################################
# MANAGER  MANAGER  MANAGER  MANAGER MANAGER # 
# This version last edited 25Apr2017 by DAS  #
# RLO at i24 beamtime                        #
##############################################

def initialise():
    caput(pv.me14e_stage_x + '.VMAX', 15)
    caput(pv.me14e_stage_y + '.VMAX', 15)
    caput(pv.me14e_stage_z + '.VMAX', 15)
    caput(pv.me14e_filter  + '.VMAX', 15)
    caput(pv.me14e_stage_x + '.VELO', 15)
    caput(pv.me14e_stage_y + '.VELO', 15)
    caput(pv.me14e_stage_z + '.VELO', 15)
    caput(pv.me14e_filter  + '.VELO', 15)
    caput(pv.me14e_stage_x + '.ACCL', 0.01)
    caput(pv.me14e_stage_y + '.ACCL', 0.01)
    caput(pv.me14e_stage_z + '.ACCL', 0.01)
    caput(pv.me14e_filter  + '.ACCL', 0.01)
    caput(pv.me14e_stage_x + '.HLM', 30)
    caput(pv.me14e_stage_x + '.LLM', -30)
    caput(pv.me14e_stage_y + '.HLM', 30)
    caput(pv.me14e_stage_y + '.LLM', -30)
    caput(pv.me14e_stage_z + '.HLM', 5.1)
    caput(pv.me14e_stage_z + '.LLM', -4.1)
    caput(pv.me14e_filter  + '.HLM', 0.1)
    caput(pv.me14e_filter  + '.LLM', -45.0)
    caput('ME14E-MO-IOC-01:GP1', 0)
    caput('ME14E-MO-IOC-01:GP2', 0)
    print 'Clearing'
    for i in range(3, 100):
        pvar = 'ME14E-MO-IOC-01:GP' + str(i)
        val = caput(pvar, 1)
        sys.stdout.write('.')
        sys.stdout.flush() 
    print '\nDONT FORGET TO DO THIS: export EPICS_CA_ADDR_LIST=172.23.190.255'
    print   'DONT FORGET TO DO THIS: export EPICS_CA_AUTO_ADDR_LIST=NO'
    print 'Initialisation Complete'

def write_parameter_file():
    print '\n\n', 10*'set', '\n'
    param_path = '/dls_sw/i24/scripts/fastchips/parameter_files/'
    param_fid = 'parameters.txt'
    print 'Writing Parameter File\n', param_path+param_fid

    f = open(param_path + param_fid,'w')

    chip_name = caget(pv.me14e_chip_name)
    f.write('chip_name \t%s\n' %chip_name)
    print 'chip_name:', chip_name

    #visit = '/dls/i24/data/2017/cm16788-2/'
    #visit = '/dls/i24/data/2017/nt14493-54/'
    visit = '/dls/i24/data/2017/nt14493-58/'
    f.write('visit \t\t%s\n' %visit)
    print 'visit:', visit

    sub_dir = caget(pv.me14e_filepath)
    f.write('sub_dir \t%s\n' %sub_dir)
    print 'sub_dir:', sub_dir

    n_exposures = caget(pv.me14e_gp3) 
    f.write('n_exposures \t%s\n' %n_exposures)
    print 'n_exposures', n_exposures

    chip_type = caget(pv.me14e_gp1) 
    f.write('chip_type \t%s\n' %chip_type)
    print 'chip_type', chip_type

    map_type = caget(pv.me14e_gp2) 
    f.write('map_type \t%s\n' %map_type)
    print 'map_type', map_type

    exptime = caget(pv.me14e_exptime) 
    f.write('exptime \t%s\n' %exptime)
    print 'exptime', exptime

    dcdetdist = caget(pv.me14e_dcdetdist) 
    f.write('dcdetdist \t%s\n' %dcdetdist)
    print 'dcdetdist', dcdetdist

    f.close()
    print '\n', 10*'set', '\n\n'

def define_current_chip(chipid):
    load_stock_map('clear')
    """
    Not sure what this is for:
    print 'Setting Mapping Type to Lite'
    caput(pv.me14e_gp2, 1)
    """
    chip_type = caget(pv.me14e_gp1)
    print chip_type, chipid
    if chipid == 'toronto':
        caput(pv.me14e_gp1, 0)
    elif chipid == 'oxford':
        caput(pv.me14e_gp1, 1)
    elif chipid == 'hamburg':
        caput(pv.me14e_gp1, 2)
    elif chipid == 'hamburgfull':
        caput(pv.me14e_gp1, 2)
    elif chipid == 'bismuth1':
        caput(pv.me14e_gp1, 3)
    elif chipid == 'bismuth2':
        caput(pv.me14e_gp1, 4)
    elif chipid == 'regina':
        caput(pv.me14e_gp1, 5)

    param_path = '/dls_sw/i24/scripts/fastchips/parameter_files/'
    f = open(param_path + chipid + '.pvar', 'r')
    for line in f.readlines():
        s = line.rstrip('\n')
        print s 
        if line.startswith('#'):
            continue
        caput(pv.me14e_pmac_str, s)

    print param_path + chipid + '.chip'
    print 10*'Done '

def save_screen_map():
    litemap_path = '/dls_sw/i24/scripts/fastchips/litemaps/'
    print '\n\nSaving', litemap_path + 'currentchip.map'
    f = open(litemap_path + 'currentchip.map','w')
    print 'Printing only blocks with block_val == 1'
    for x in range(1, 82):
        block_str = 'ME14E-MO-IOC-01:GP%i' %(x+10)
        block_val = caget(block_str) 
        if block_val == 1:
            print block_str, block_val
        line = '%02dstatus    P3%02d1 \t%s\n' %(x, x, block_val)
        f.write(line)
    f.close()
    print 10*'Done '
    return 0

def upload_parameters(chipid):
    if chipid == 'toronto':
        caput(pv.me14e_gp1, 0)
        width = 9
    elif chipid == 'oxford':
        caput(pv.me14e_gp1, 1)
        width = 8
    elif chipid == 'hamburg':
        caput(pv.me14e_gp1, 2)
        width = 3
    elif chipid == 'bismuth1':
        caput(pv.me14e_gp1, 3)
        width = 1
    elif chipid == 'bismuth2':
        caput(pv.me14e_gp1, 4)
        width = 7
    elif chipid == 'regina':
        caput(pv.me14e_gp1, 5)
        width = 7
    litemap_path = '/dls_sw/i24/scripts/fastchips/litemaps/'
    f = open(litemap_path + 'currentchip.map','r')
    print 'chipid', chipid
    print width
    x = 1
    for line in f.readlines()[:width**2]:
        cols = line.split( )
        pvar = cols[1]
        value = cols[2]
        s = pvar +'='+ value
        if value != '1':
            s2 = pvar + '   '
            sys.stdout.write(s2)
        else:
            sys.stdout.write(s+' ')
        sys.stdout.flush() 
        if x == width:
            print
            x = 1
        else:
            x += 1 
        caput(pv.me14e_pmac_str, s)
        sleep(0.02)
    print
    print 'Setting Mapping Type to Lite'
    caput(pv.me14e_gp2, 1)
    print 10*'Done '

def upload_full():
    fullmap_path = '/dls_sw/i24/scripts/fastchips/fullmaps/'
    f = open(fullmap_path + 'currentchip.full', 'r').readlines()

    for x in range(len(f) / 2):
        pmac_list = []
        for i in range(2):
	    pmac_list.append(f.pop(0).rstrip('\n'))
	writeline = " ".join(pmac_list)
	print writeline
	caput(pv.me14e_pmac_str, writeline)
	sleep(0.02)

    print 10*'Done '

def load_stock_map(map_choice):
    print 'Please wait, adjusting lite map'
    #
    r33 = [19,18,17,26,31,32,33,24,25]
    r55 = [9,10,11,12,13,16,27,30,41,40,39,38,37,34,23,20] + r33 
    r77 = [7,6,5,4,3,2,1,14,15,28,29,42,43,44,45,46,47,48,49,36,35,22,21,8] + r55
    #
    h33 = [3,2,1,6,7,8,9,4,5]
    x33 = [31,32,33,40,51,50,49,42,41]
    x55 = [25,24,23,22,21,34,39,52,57,58,59,60,61,48,43,30] + x33
    x77 = [11,12,13,14,15,16,17,20,35,38,53,56,71,70,69,68,67,66,65,62,47,44,29,26] + x55
    x99 = [9,8,7,6,5,4,3,2,1,18,19,36,37,54,55,72,73,74,75,76,77,78,79,80,81,64,63,46,45,28,27,10] + x77
    x44 = [22,21,20,19,30,35,46,45,44,43,38,27,28,29,36,37]
    x49 = [x+1 for x in range(49)]
    x66 = [10,11,12,13,14,15,18,31,34,47,50,51,52,53,54,55,42,39,26,23] + x44
    x88 = [8,7,6,5,4,3,2,1,16,17,32,33,48,49,64,63,62,61,60,59,58,57,56,41,40,25,24,9] + x66

    map_dict = {}
    map_dict['clear']= [1]
    #
    map_dict['r33'] = r33
    map_dict['r55'] = r55
    map_dict['r77'] = r77
    #
    map_dict['h33'] = h33
    #
    map_dict['x33'] = x33
    map_dict['x44'] = x44
    map_dict['x49'] = x49
    map_dict['x55'] = x55
    map_dict['x66'] = x66
    map_dict['x77'] = x77
    map_dict['x88'] = x88
    map_dict['x99'] = x99
    print 'Clearing'
    for i in range(1, 82):
        pvar = 'ME14E-MO-IOC-01:GP' + str(i + 10)
        caput(pvar, 0)
	sys.stdout.write('.')
	sys.stdout.flush() 
    print '\nmap cleared'
    print 'loading map_choice', map_choice
    for i in map_dict[map_choice]:
        pvar = 'ME14E-MO-IOC-01:GP' + str(i + 10)
        caput(pvar, 1)
    print 10*'Done '

def load_lite_map():
    load_stock_map('clear')
    toronto_block_dict = {\
            'A1':'01', 'A2':'02', 'A3':'03', 'A4':'04', 'A5':'05', 'A6':'06','A7':'07', 'A8':'08', 'A9':'09'
           ,'B1':'18', 'B2':'17', 'B3':'16', 'B4':'15', 'B5':'14', 'B6':'13','B7':'12', 'B8':'11', 'B9':'10'
           ,'C1':'19', 'C2':'20', 'C3':'21', 'C4':'22', 'C5':'23', 'C6':'24','C7':'25', 'C8':'26', 'C9':'27'
           ,'D1':'36', 'D2':'35', 'D3':'34', 'D4':'33', 'D5':'32', 'D6':'31','D7':'30', 'D8':'29', 'D9':'28'
           ,'E1':'37', 'E2':'38', 'E3':'39', 'E4':'40', 'E5':'41', 'E6':'42','E7':'43', 'E8':'44', 'E9':'45'
           ,'F1':'54', 'F2':'53', 'F3':'52', 'F4':'51', 'F5':'50', 'F6':'49','F7':'48', 'F8':'47', 'F9':'46'
           ,'G1':'55', 'G2':'56', 'G3':'57', 'G4':'58', 'G5':'59', 'G6':'60','G7':'61', 'G8':'62', 'G9':'63'
           ,'H1':'72', 'H2':'71', 'H3':'70', 'H4':'69', 'H5':'68', 'H6':'67','H7':'66', 'H8':'65', 'H9':'64'
           ,'I1':'73', 'I2':'74', 'I3':'75', 'I4':'76', 'I5':'77', 'I6':'78','I7':'79', 'I8':'80', 'I9':'81'}
    oxford_block_dict = {\
            'A1':'01', 'A2':'02', 'A3':'03', 'A4':'04', 'A5':'05', 'A6':'06','A7':'07', 'A8':'08'
           ,'B1':'16', 'B2':'15', 'B3':'14', 'B4':'13', 'B5':'12', 'B6':'11','B7':'10', 'B8':'09'
           ,'C1':'17', 'C2':'18', 'C3':'19', 'C4':'20', 'C5':'21', 'C6':'22','C7':'23', 'C8':'24'
           ,'D1':'32', 'D2':'31', 'D3':'30', 'D4':'29', 'D5':'28', 'D6':'27','D7':'26', 'D8':'25'
           ,'E1':'33', 'E2':'34', 'E3':'35', 'E4':'36', 'E5':'37', 'E6':'38','E7':'39', 'E8':'40'
           ,'F1':'48', 'F2':'47', 'F3':'46', 'F4':'45', 'F5':'44', 'F6':'43','F7':'42', 'F8':'41'
           ,'G1':'49', 'G2':'50', 'G3':'51', 'G4':'52', 'G5':'53', 'G6':'54','G7':'55', 'G8':'56'
           ,'H1':'64', 'H2':'63', 'H3':'62', 'H4':'61', 'H5':'60', 'H6':'59','H7':'58', 'H8':'57'}
    regina_block_dict = {\
            'A1':'01', 'A2':'02', 'A3':'03', 'A4':'04', 'A5':'05', 'A6':'06','A7':'07'
           ,'B1':'14', 'B2':'13', 'B3':'12', 'B4':'11', 'B5':'10', 'B6':'09','B7':'08'
           ,'C1':'15', 'C2':'16', 'C3':'17', 'C4':'18', 'C5':'19', 'C6':'20','C7':'21'
           ,'D1':'28', 'D2':'27', 'D3':'26', 'D4':'25', 'D5':'24', 'D6':'23','D7':'22'
           ,'E1':'29', 'E2':'30', 'E3':'31', 'E4':'32', 'E5':'33', 'E6':'34','E7':'35'
           ,'F1':'42', 'F2':'41', 'F3':'40', 'F4':'39', 'F5':'38', 'F6':'37','F7':'36'
           ,'G1':'43', 'G2':'44', 'G3':'45', 'G4':'46', 'G5':'47', 'G6':'48','G7':'49'}
    hamburg_block_dict = {\
            'A1':'01', 'A2':'02', 'A3':'03'
           ,'B1':'06', 'B2':'05', 'B3':'04'
           ,'C1':'07', 'C2':'08', 'C3':'09'}
    chip_type = caget(pv.me14e_gp1) 
    if chip_type == 0:
        print 'Toronto Block Order'
	block_dict = toronto_block_dict
    elif chip_type == 1:
        print 'Oxford Block Order'
	block_dict = oxford_block_dict
    elif chip_type == 2:
        print 'Hamburg Block Order'
	block_dict = hamburg_block_dict
    elif chip_type == 5:
        print 'Regina Block Order'
	block_dict = regina_block_dict

    litemap_path = '/dls_sw/i24/scripts/fastchips/litemaps/'
    litemap_fid = caget(pv.me14e_gp5) + '.lite'
    print 'opening', litemap_path + litemap_fid
    f = open(litemap_path + litemap_fid, 'r')

    print 'please wait, loading LITE map' 
    for line in f.readlines():
        entry = line.split()
        block_name = entry[0]
        yesno = entry[1]
        block_num = toronto_block_dict[block_name] 
        pvar = 'ME14E-MO-IOC-01:GP' + str(int(block_num) + 10)
        print block_name, yesno, pvar
        caput(pvar, yesno)
    print 10*'Done '

def load_full_map():
    chip_name, visit, sub_dir, n_exposures, chip_type, map_type = startup.scrape_parameter_file()
    fullmap_path = '/dls_sw/i24/scripts/fastchips/fullmaps/'
    fullmap_fid = filemap_path + caget(pv.me14e_gp5) + '.spec'
    print 'opening', fullmap_fid
    mapping.plot_file(fullmap_fid, chip_type)
    print '\n\n', 10*'PNG '
    mapping.convert_chip_to_hex(full_map_fid, chip_type)
    os.system("cp %s %s" % (fullmap_fid[:-4]+'full', fullmap_path+'currentchip.full'))
    print 10*'Done ', '\n'

def moveto(place):
    print 5 * (place + ' ')
    chip_type = caget(pv.me14e_gp1)
    print 'CHIP TYPE', chip_type
    if chip_type == 0:
	    print 'Toronto Move'
	    if place == 'origin':
                caput(pv.me14e_stage_x, 0.0)
                caput(pv.me14e_stage_y, 0.0)
	    if place == 'f1':
                caput(pv.me14e_stage_x, +18.975)
                caput(pv.me14e_stage_y, 0.0)
	    if place == 'f2':
                caput(pv.me14e_stage_x, 0.0)
                caput(pv.me14e_stage_y, +21.375)
    
    elif chip_type == 1:
        print 'Oxford Move'
        if place == 'origin':
            caput(pv.me14e_stage_x, 0.0)
            caput(pv.me14e_stage_y, 0.0)
        if place == 'f1':
            caput(pv.me14e_stage_x, +25.40)
            caput(pv.me14e_stage_y, 0.0)
        if place == 'f2':
            caput(pv.me14e_stage_x, 0.0)
            caput(pv.me14e_stage_y, +25.40)

    elif chip_type == 2:
        print 'Hamburg Move'
        if place == 'origin':
            caput(pv.me14e_stage_x, 0.0)
            caput(pv.me14e_stage_y, 0.0)
        if place == 'f1':
            #caput(pv.me14e_stage_x, +17.16)
            caput(pv.me14e_stage_x, +24.968)
            caput(pv.me14e_stage_y, 0.0)
        if place == 'f2':
            caput(pv.me14e_stage_x, 0.0)
            #caput(pv.me14e_stage_y, -26.49)
            caput(pv.me14e_stage_y, +24.968)

    elif chip_type == 5:
        print 'Regina Move'
        if place == 'origin':
            caput(pv.me14e_stage_x, 0.0)
            caput(pv.me14e_stage_y, 0.0)
        if place == 'f1':
            caput(pv.me14e_stage_x, +17.175)
            caput(pv.me14e_stage_y, 0.0)
        if place == 'f2':
            caput(pv.me14e_stage_x, 0.0)
            caput(pv.me14e_stage_y, +17.175)

    else:
        print 'Unknown chip_type move'

    # Non Chip Specific Move
    if place == 'zero':
        caput(pv.me14e_pmac_str, '!x0y0z0')

    elif place == 'yag':
        caput(pv.me14e_stage_x, 1.0)  
        caput(pv.me14e_stage_y, 1.0)  
        caput(pv.me14e_stage_z, 1.0)
   
    elif place == 'load_position':
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, 0.0)
        caput(pv.me14e_stage_z, 0.0)
        caput(pv.absb_mp_select, 'Robot')
        caput(pv.ap1_mp_select, 'Robot')
        caput(pv.blight_mp_select, 'Out')
        caput(pv.det_z, 1480)

    elif place == 'collect_position':
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, 0.0)
        caput(pv.me14e_stage_z, 0.0)
        caput(pv.absb_mp_select, 'Data Collection')
        caput(pv.ap1_mp_select, 'In')
        caput(pv.blight_mp_select, 'In')

    elif place == 'lightin':
        caput(pv.me14e_filter, 0)  

    elif place == 'lightout':
        caput(pv.me14e_filter, -38)

def scrape_mtr_directions():
    param_path = '/dls_sw/i24/scripts/fastchips/parameter_files/'
    f = open(param_path + 'motor_direction.txt', 'r')
    mtr1_dir, mtr2_dir, mtr3_dir = 1,1,1
    for line in f.readlines():
        if line.startswith('mtr1'):
            mtr1_dir = float(int(line.split('=')[1]))
        elif line.startswith('mtr2'):
            mtr2_dir = float(int(line.split('=')[1]))
        elif line.startswith('mtr3'):
            mtr3_dir = float(int(line.split('=')[1]))
        else:
            continue
    f.close()
    return mtr1_dir, mtr2_dir, mtr3_dir

def fiducial(point):
    scale = 10000.0
    param_path = '/dls_sw/i24/scripts/fastchips/parameter_files/'

    mtr1_dir, mtr2_dir, mtr3_dir = scrape_mtr_directions()

    rbv_1 = caget(pv.me14e_stage_x + '.RBV')
    rbv_2 = caget(pv.me14e_stage_y + '.RBV')
    rbv_3 = caget(pv.me14e_stage_z + '.RBV')

    raw_1 = caget(pv.me14e_stage_x + '.RRBV')
    raw_2 = caget(pv.me14e_stage_y + '.RRBV')
    raw_3 = caget(pv.me14e_stage_z + '.RRBV')
    """  
    June 8th 2017 change from this to rbv
    f_x = (mtr1_dir*raw_1) / scale
    f_y = (mtr2_dir*raw_2) / scale
    f_z = (mtr3_dir*raw_3) / scale
    """  
    f_x = rbv_1 
    f_y = rbv_2 
    f_z = rbv_3 

    print '\nWriting Fiducial File', 20*('%s ' %point)
    print 'MTR\tRBV\tRAW\tDirect.\tf_value'
    print 'MTR1\t%1.4f\t%i\t%i\t%1.4f' % (rbv_1, raw_1, mtr1_dir, f_x)
    print 'MTR2\t%1.4f\t%i\t%i\t%1.4f' % (rbv_2, raw_2, mtr2_dir, f_y)
    print 'MTR3\t%1.4f\t%i\t%i\t%1.4f' % (rbv_3, raw_3, mtr3_dir, f_z)
    print 'Writing Fiducial File', 20*('%s ' %point)

    f = open(param_path + 'fiducial_%s.txt' %point, 'w')
    f.write('MTR\tRBV\tRAW\tCorr\tf_value\n')
    f.write('MTR1\t%1.4f\t%i\t%i\t%1.4f\n' % (rbv_1, raw_1, mtr1_dir, f_x))
    f.write('MTR2\t%1.4f\t%i\t%i\t%1.4f\n' % (rbv_2, raw_2, mtr2_dir, f_y))
    f.write('MTR3\t%1.4f\t%i\t%i\t%1.4f'   % (rbv_3, raw_3, mtr3_dir, f_z))
    f.close() 
    print 10*'Done '

def scrape_mtr_fiducials(point):
    param_path = '/dls_sw/i24/scripts/fastchips/parameter_files/'
    f = open(param_path+'fiducial_%i.txt' %point,'r')    
    f_lines = f.readlines()[1:]
    f_x = float(f_lines[0].rsplit()[4]) 
    f_y = float(f_lines[1].rsplit()[4])  
    f_z = float(f_lines[2].rsplit()[4])  
    f.close()
    return f_x, f_y, f_z

def cs_maker():
    chip_type = caget(pv.me14e_gp1)
    fiducial_dict = {}
    fiducial_dict[0] = [18.975, 21.375]
    fiducial_dict[1] = [25.400, 25.400]
    fiducial_dict[2] = [24.968, 24.968]
    fiducial_dict[4] = [27.500, 27.500]
    fiducial_dict[5] = [17.175, 17.175]
    print chip_type, fiducial_dict[chip_type]

    mtr1_dir, mtr2_dir, mtr3_dir = scrape_mtr_directions()
    f1_x, f1_y, f1_z = scrape_mtr_fiducials(1)
    f2_x, f2_y, f2_z = scrape_mtr_fiducials(2)
    """
    Theory
    Rx: rotation about X-axis, pitch
    Ry: rotation about Y-axis, yaw
    Rz: rotation about Z-axis, roll
    The order of rotation is Roll->Yaw->Pitch (Rx*Ry*Rz)
    Rx           Ry          Rz
    |1  0   0| | Cy  0 Sy| |Cz -Sz 0|   | CyCz        -CxSz         Sy  |
    |0 Cx -Sx|*|  0  1  0|*|Sz  Cz 0| = | SxSyCz+CxSz -SxSySz+CxCz -SxCy|
    |0 Sx  Cx| |-Sy  0 Cy| | 0   0 1|   |-CxSyCz+SxSz  CxSySz+SxCz  CxCy|
    """
    # Rotation Around Z #
    Sz1 =       f1_y / fiducial_dict[chip_type][0] 
    Sz2 = -1 * (f2_x / fiducial_dict[chip_type][1]) 
    Sz = 0.5 * (Sz1 + Sz2)
    Sz = -1.0 * Sz
    Cz = np.sqrt((1 - Sz**2))
    print 'Sz1 , %1.4f, %1.4f' % (Sz1, np.degrees(np.arcsin(Sz1)))
    print 'Sz2 , %1.4f, %1.4f' % (Sz2, np.degrees(np.arcsin(Sz2)))
    print 'Sz ,  %1.4f, %1.4f' % (Sz, np.degrees(np.arcsin(Sz)))
    print 'Cz ,  %1.4f, %1.4f\n' % (Cz, np.degrees(np.arccos(Cz)))
    # Rotation Around Y #
    Sy = f1_z /  fiducial_dict[chip_type][0]  
    Cy = np.sqrt((1 - Sy**2))
    print 'Sy , %1.4f, %1.4f' % (Sy, np.degrees(np.arcsin(Sy)))
    print 'Cy , %1.4f, %1.4f\n' % (Cy, np.degrees(np.arccos(Cy)))
    # Rotation Around X #
    Sx = f2_z /  fiducial_dict[chip_type][1]  
    Cx = np.sqrt((1 - Sx**2))
    print 'Sx , %1.4f, %1.4f' % (Sx, np.degrees(np.arcsin(Sx)))
    print 'Cx , %1.4f, %1.4f\n' % (Cx, np.degrees(np.arccos(Cx)))

    scalex,scaley,scalez  = 10010.0, 10000.68, 10000.0
    x1factor = mtr1_dir * scalex * (Cy * Cz)
    y1factor = mtr2_dir * scaley * (-1. * Cx * Sz)
    z1factor = mtr3_dir * scalez * Sy 

    x2factor = mtr1_dir * scalex * ((Sx*Sy*Cz) + (Cx*Sz))
    y2factor = mtr2_dir * scaley * ((Cx*Cz) - (Sx*Sy*Sz))
    z2factor = mtr3_dir * scalez * (-1. * Sx * Cy) 
    
    x3factor = mtr1_dir * scalex * ((Sx*Sz) - (Cx*Sy*Cz)) 
    y3factor = mtr2_dir * scaley * ((Cx*Sy*Sz) + (Sx*Cz))
    z3factor = mtr3_dir * scalez * (Cx* Cy)
    """
    Rx           Ry          Rz
    |1  0   0| | Cy  0 Sy| |Cz -Sz 0|   | CyCz        -CxSz         Sy  |
    |0 Cx -Sx|*|  0  1  0|*|Sz  Cz 0| = | SxSyCz+CxSz -SxSySz+CxCz -SxCy|
    |0 Sx  Cx| |-Sy  0 Cy| | 0   0 1|   |-CxSyCz+SxSz  CxSySz+SxCz  CxCy|
    """
    cs1 = "#1->%+1.3fX%+1.3fY%+1.3fZ" % (x1factor, y1factor, z1factor)
    cs2 = "#2->%+1.3fX%+1.3fY%+1.3fZ" % (x2factor, y2factor, z2factor)
    cs3 = "#3->%+1.3fX%+1.3fY%+1.3fZ" % (x3factor, y3factor, z3factor)
    print '\n'.join([cs1, cs2, cs3])

    print 'These should be 10,000. This is the sum of the squares of the factors'
    print np.sqrt(x1factor**2 + y1factor**2 + z1factor**2)
    print np.sqrt(x2factor**2 + y2factor**2 + z2factor**2)
    print np.sqrt(x3factor**2 + y3factor**2 + z3factor**2)

    print 'Long wait, please be patient' 
    caput(pv.me14e_pmac_str, '!x0y0z0')
    sleep(2.5)
    caput(pv.me14e_pmac_str, '&2')
    caput(pv.me14e_pmac_str, cs1)
    caput(pv.me14e_pmac_str, cs2)
    caput(pv.me14e_pmac_str, cs3)
    caput(pv.me14e_pmac_str, '!x0y0z0')
    sleep(0.1)
    caput(pv.me14e_pmac_str, '#1hmz#2hmz#3hmz')
    sleep(0.1)
    # NEXT THREE LINES COMMENTED OUT FOR CS TESTS 5 JUNE
    #caput(pv.me14e_pmac_str, '!x0.4y0.4')
    #sleep(0.1)
    #caput(pv.me14e_pmac_str, '#1hmz#2hmz#3hmz')
    print 10*'CSDone '

def cs_reset():
    cs1 = "#1->%+10000X%+0Y%+0Z"
    cs2 = "#2->%+0X%+10000Y%+0Z"
    cs3 = "#3->0X+0Y+10000Z"
    print '\n'.join([cs1, cs2, cs3])
    caput(pv.me14e_pmac_str, '&2')
    sleep(0.5)
    caput(pv.me14e_pmac_str, cs1)
    sleep(0.5)
    caput(pv.me14e_pmac_str, cs2)
    sleep(0.5)
    caput(pv.me14e_pmac_str, cs3)
    print 10*'CSDone '

def main(args):
    if args[1] == 'initialise':
        initialise()

    elif args[1] == 'pvar_test':
        chipid = args[2]
        pvar_test(chipid)

    elif args[1] == 'moveto':
        moveto(args[2])
    elif args[1] == 'fiducial':
        fiducial(args[2])
    elif args[1] == 'cs_maker':
        cs_maker()
    elif args[1] == 'write_parameter_file':
        write_parameter_file()
        startup.run()
    elif args[1] == 'define_current_chip':
        chipid = args[2]
        define_current_chip(chipid)
    elif args[1] == 'load_stock_map':
        map_choice = args[2]
        load_stock_map(map_choice)
    elif args[1] == 'load_lite_map':
	    load_lite_map()
    elif args[1] == 'load_full_map':
	    load_full_map()
    elif args[1] == 'save_screen_map':
        save_screen_map()
    elif args[1] == 'upload_full':
        upload_full()
    elif args[1] == 'upload_parameters':
        chipid = args[2]
        upload_parameters(chipid)
    elif args[1] == 'cs_reset':
        cs_reset()

    else:
        print 'Unknown Command'

if  __name__ == '__main__':
    main(sys.argv)
