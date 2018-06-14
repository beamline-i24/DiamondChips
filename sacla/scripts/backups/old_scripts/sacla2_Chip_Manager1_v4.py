#!/usr/bin/python
import pv, os, re, sys
import math, time, string
from time import sleep
from ca import caput, caget
import sacla2_Chip_StartUp1_v4 as su
import sacla2_Chip_Mapping1_v4 as mapping

##############################################
# MANAGER  MANAGER  MANAGER  MANAGER MANAGER # 
# This version last edited 25Nov2016 by DAS  #
# RLO DNA at beamtime                        #
##############################################

def initialise():
    caput(pv.me14e_stage_x + '.VMAX', 20)
    caput(pv.me14e_stage_y + '.VMAX', 20)
    caput(pv.me14e_stage_z + '.VMAX', 20)
    caput(pv.me14e_filter + '.VMAX', 20)
    caput(pv.me14e_stage_x + '.VELO', 20)
    caput(pv.me14e_stage_y + '.VELO', 20)
    caput(pv.me14e_stage_z + '.VELO', 20)
    caput(pv.me14e_filter + '.VELO', 20)
    caput(pv.me14e_stage_x + '.ACCL', 0.00001)
    caput(pv.me14e_stage_y + '.ACCL', 0.00001)
    caput(pv.me14e_stage_z + '.ACCL', 0.00001)
    caput(pv.me14e_filter + '.ACCL', 0.00001)
    caput(pv.me14e_stage_x + '.HLM', 30)
    caput(pv.me14e_stage_x + '.LLM', -30)
    caput(pv.me14e_stage_y + '.HLM', 30)
    caput(pv.me14e_stage_y + '.LLM', -30)
    caput(pv.me14e_stage_z + '.HLM', 5.1)
    caput(pv.me14e_stage_z + '.LLM', -4.1)
    caput(pv.me14e_filter + '.HLM', 0.1)
    caput(pv.me14e_filter + '.LLM', -45.0)
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
    print 'Writing Parameter File'
    path = '/localhome/local/Documents/sacla/parameter_files/'

    f = open(path + 'parameters.txt','w')
    chip_name = caget(pv.me14e_chip_name)

    f.write('chip_name \t%s\n' %chip_name)
    print 'chip_name:', chip_name

    f.write('path \t%s\n' %path)
    print 'path:', path

    protein_name = caget(pv.me14e_filepath)
    f.write('protein_name \t%s\n' %protein_name)
    print 'protein_name:', protein_name

    n_exposures = caget(pv.me14e_gp3) 
    f.write('n_exposures \t%s\n' %n_exposures)
    print 'n_exposures', n_exposures

    chip_type = caget(pv.me14e_gp1) 
    f.write('chip_type \t%s\n' %chip_type)
    print 'chip_type', chip_type

    map_type = caget(pv.me14e_gp2) 
    f.write('map_type \t%s\n' %map_type)
    print 'map_type', map_type

    f.close()
    print '\n', 10*'set', '\n\n'

def define_current_chip(chipid):
    load_stock_map('clear')
    """
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

    path = '/localhome/local/Documents/sacla/parameter_files/'
    f = open(path + chipid + '.pvar', 'r')
    for line in f.readlines():
        s = line.rstrip('\n')
        print s 
        if line.startswith('#'):
            continue
        caput(pv.me14e_pmac_str, s)

    print path + chipid + '.chip'
    print 10*'Done '

    """
    path = '/localhome/local/Documents/sacla/parameter_files/'
    f = open(path + chipid + '.chip','r')
    print 'reading', path + chipid + '.chip'
    print 'writing to pmac'
    x = 0
    for line in f:
        cols = line.split( )
        pvar = cols[1]
        value = cols[2]
        s = pvar +'='+ value
        if value == '0':
            sys.stdout.write(s+'    \t')
        else:
            sys.stdout.write(s+'\t')
        sys.stdout.flush() 
        caput(pv.me14e_pmac_str, s)
        sleep(0.02)
        if x == 3:
            print
            x = 0
        else:
            x += 1 
    print path + chipid + '.chip'
    print 10*'Done '
    """

def save_screen_map():
    path = '/localhome/local/Documents/sacla/litemaps/'
    print '\n\nSaving', path + 'currentchip.map'
    f = open(path + 'currentchip.map','w')
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
    path = '/localhome/local/Documents/sacla/litemaps/'
    f = open(path + 'currentchip.map','r')
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
    path = '/localhome/local/Documents/sacla/fullmaps/'
    f = open(path + 'currentchip.full', 'r').readlines()

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

    path = '/localhome/local/Documents/sacla/litemaps/'
    lite_map_fid = caget(pv.me14e_gp5) + '.lite'
    print 'opening', path + lite_map_fid
    f = open(path + lite_map_fid, 'r')

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
    chip_name, path, protein_name, n_exposures, chip_type, map_type = su.scrape_parameter_file()
    file_path = path.replace('parameter_files', 'fullmaps')
    full_map_fid = file_path + caget(pv.me14e_gp5) + '.spec'
    print 'opening', full_map_fid
    mapping.plot_file(full_map_fid, chip_type)
    print '\n\n', 10*'PNG '
    mapping.convert_chip_to_hex(full_map_fid, chip_type)
    os.system("cp %s %s" % (full_map_fid[:-4]+'full', file_path+'currentchip.full'))
    print 10*'Done ', '\n'

def moveto(place):
    print 5 * (place + ' ')
    chip_type = caget(pv.me14e_gp1)
    if chip_type == 0:
	    print 'Toronto Move'
	    if place == 'origin':  
                print 'ere'                 
                caput(pv.me14e_stage_x, 0.0)
                caput(pv.me14e_stage_y, 0.0)
	    if place == 'f1':
                caput(pv.me14e_stage_x, +18.975)
                caput(pv.me14e_stage_y, 0.0)
	    if place == 'f2':
                caput(pv.me14e_stage_x, 0.0)
                caput(pv.me14e_stage_y, -21.375)
    
    elif chip_type == 1:
        print 'Oxford Move'
        if place == 'origin':
            caput(pv.me14e_stage_x, 0.0)
            caput(pv.me14e_stage_y, 0.0)
        if place == 'f1':
            caput(pv.me14e_stage_x, +25.60)
            caput(pv.me14e_stage_y, 0.0)
        if place == 'f2':
            caput(pv.me14e_stage_x, 0.0)
            caput(pv.me14e_stage_y, -25.60)

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
            caput(pv.me14e_stage_y, -24.968)

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
            caput(pv.me14e_stage_y, -17.175)

    else:
        print 'Unknown chip_type move'

    if place == 'zero':
        caput(pv.me14e_pmac_str, '!x0y0z0')

    elif place == 'yag':
        caput(pv.me14e_stage_x, 1.0)  
        caput(pv.me14e_stage_y, 1.0)  
        caput(pv.me14e_stage_z, 1.0)
   
    elif place == 'load_position':
        caput(pv.me14e_stage_x, 2.0)  
        caput(pv.me14e_stage_y, 2.0)
        caput(pv.me14e_stage_z, 0.0)

    elif place == 'collect_position':
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, 0.0)
        caput(pv.me14e_stage_z, 0.0)

    elif place == 'lightin':
        caput(pv.me14e_filter, 0)  

    elif place == 'lightout':
        caput(pv.me14e_filter, -38)

def fiducial(point):
    path = '/localhome/local/Documents/sacla/parameter_files/'
    x = caget(pv.me14e_stage_x + '.RBV')
    y = caget(pv.me14e_stage_y + '.RBV')
    z = caget(pv.me14e_stage_z + '.RBV')
    print '\nWriting Fiducial File', 20*('%s ' %point)
    print '\n'.join([str(x), str(y), str(z)])
    f = open(path + 'fiducial_%s.txt' %point, 'w')
    f.write('%1.3f\n' %x)
    f.write('%1.3f\n' %y)
    f.write('%1.3f' %z)
    f.close() 
    print 10*'Done '
     
def cs_maker():
    scale = 10000
    f1 = open('/localhome/local/Documents/sacla/parameter_files/fiducial_1.txt','r')    
    f1_lines = f1.readlines()
    f1_x = float(f1_lines[0].rstrip('/n')) 
    f1_y = float(f1_lines[1].rstrip('/n')) 
    f1_z = float(f1_lines[2].rstrip('/n')) 
    f2 = open('/localhome/local/Documents/sacla/parameter_files/fiducial_2.txt','r')    
    f2_lines = f2.readlines()
    f2_x = float(f2_lines[0].rstrip('/n')) 
    f2_y = float(f2_lines[1].rstrip('/n')) 
    f2_z = float(f2_lines[2].rstrip('/n')) 
    #Evaluate numbers
    chip_type = caget(pv.me14e_gp1)
    print chip_type
    if chip_type == 0:
        #x1factor = (f1_x / 18.975) * scale

        x1factor = (f1_x / 14.575) * scale
        y1factor = (f1_y / f1_x)   * scale
        z1factor = (f1_z / f1_x)   * scale

        x2factor = (f2_x / f2_y)   * scale
        #y2factor = (f2_y / 21.375) * scale
        y2factor = (f2_y / 16.375) * scale
        z2factor = (f2_z / f2_y)   * scale

        z3factor = scale

    elif chip_type == 1:
        x1factor = (f1_x / 25.60)  * scale
        y1factor = (f1_y / f1_x)   * scale
        z1factor = (f1_z / f1_x)   * scale
        x2factor = (f2_x / f2_y)   * scale
        y2factor = (f2_y / 25.60)  * scale
        z2factor = (f2_z / f2_y)   * scale
        z3factor = scale

    elif chip_type == 2:
        x1factor = (f1_x / 24.968)  * scale #24.96 add 75 microns?!?
        y1factor = (f1_y / f1_x)   * scale
        z1factor = (f1_z / f1_x)   * scale
        x2factor = (f2_x / f2_y)   * scale
        y2factor = (f2_y / 24.968)  * scale
        z2factor = (f2_z / f2_y)   * scale
        z3factor = scale

    elif chip_type == 4:
        x1factor = (f1_x / 27.5)  * scale
        y1factor = (f1_y / f1_x)   * scale
        z1factor = (f1_z / f1_x)   * scale
        x2factor = (f2_x / f2_y)   * scale
        y2factor = (f2_y / 27.5)  * scale
        z2factor = (f2_z / f2_y)   * scale
        z3factor = scale

    elif chip_type == 5:
        x1factor = (f1_x / 17.183)  * scale #17.175
        y1factor = (f1_y / f1_x)   * scale #(f1_y / f1_x)
        z1factor = (f1_z / f1_x)   * scale
        x2factor = (f2_x / f2_y)   * scale #(f2_x / f2_y)
        y2factor = (f2_y / 17.183)  * scale
        z2factor = (f2_z / f2_y)   * scale
        z3factor = scale

    else:
        print 'Unknown chip type'

    cs1 = "#1->%+1.3fX%+1.3fY%+1.3fZ" % (x1factor, y1factor, z1factor)
    cs2 = "#2->%+1.3fX%+1.3fY%+1.3fZ" % (-1*x2factor, y2factor, z2factor)
    cs3 = "#3->0X+0Y%+fZ"             % (z3factor)
    print '\n'.join([cs1, cs2, cs3])

    caput(pv.me14e_pmac_str, '!x0y0z0')
    sleep(0.5)
    caput(pv.me14e_pmac_str, '&2')
    sleep(0.5)
    caput(pv.me14e_pmac_str, cs1)
    sleep(0.5)
    caput(pv.me14e_pmac_str, cs2)
    sleep(0.5)
    caput(pv.me14e_pmac_str, cs3)
    sleep(0.5)
    print 'long wait, please be patient' 
    caput(pv.me14e_pmac_str, '!x0y0z0')
    sleep(1.5)
    if chip_type == 0:
        sleep(0.5)
        caput(pv.me14e_pmac_str, '#1hmz#2hmz#3hmz')
        sleep(0.5)

    elif chip_type == 1:
        sleep(0.5)
        caput(pv.me14e_pmac_str, '!X0.5Y0.5Z0')
        print 'Oxford Chip Shift Origin'
        sleep(1)
        caput(pv.me14e_pmac_str, '#1hmz#2hmz#3hmz')
        sleep(0.5)
        caput(pv.me14e_pmac_str, '!x0y0z0')
        sleep(0.5)

    elif chip_type == 2:
        sleep(0.5)
        caput(pv.me14e_pmac_str, '#1hmz#2hmz#3hmz')
        sleep(0.5)
        """
        caput(pv.me14e_pmac_str, '!X-3.91Y0.775Z0')
        #X3.9Y0.765
        print 'Hamburg Chip Shift Origin'
        sleep(1)
        caput(pv.me14e_pmac_str, '#1hmz#2hmz#3hmz')
        sleep(0.5)
        caput(pv.me14e_pmac_str, '!x0y0z0')
        sleep(0.5)
        """

    elif chip_type == 4:
        sleep(0.5)
        caput(pv.me14e_pmac_str, '#1hmz#2hmz#3hmz')
        sleep(0.5)

    elif chip_type == 5:
        sleep(2)
        caput(pv.me14e_pmac_str, '!X-3.69Y-3.695Z0')
        print 'Regina Chip Shift Origin'
        sleep(1)
        caput(pv.me14e_pmac_str, '#1hmz#2hmz#3hmz')
        sleep(0.5)
        caput(pv.me14e_pmac_str, '!x0y0z0')
        sleep(0.5)
    else:
	    print 'cs-else'
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
        su.run()
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
