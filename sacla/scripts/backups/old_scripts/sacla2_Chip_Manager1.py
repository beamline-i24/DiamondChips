import pv
import os, re, sys
import math, time, string
from time import sleep
from ca import caput, caget 
from sacla2_Chip_StartUp1 import get_xy
from sacla2_Chip_StartUp1 import scrape_parameter_file

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
    path = '/localhome/local/Documents/sacla/parameter_files/'
    f = open(path + chipid + '.chip','r')
    print 'reading', path + chipid + '.chip'
    print 'writing to pmac'
    for line in f:
        cols = line.split( )
        pvar = cols[1]
        value = cols[2]
        s = str(pvar) + '=' + str(value)
        #print 'set P-variable', s
	sys.stdout.write(s+' ')
	sys.stdout.flush() 
        caput(pv.me14e_pmac_str, s)
        sleep(0.02)
    print
    print path + chipid + '.chip'
    print 10*'Done '

def upload_parameters():
    path = '/localhome/local/Documents/sacla/litemaps/'
    f = open(path + 'currentchip.map','r')
    for line in f:
        cols = line.split( )
        pvar = cols[1]
        value = cols[2]
        s = str(pvar) + '=' + str(value)
        #print 'set P-variable', s
	sys.stdout.write(s+' ')
	sys.stdout.flush() 
        caput(pv.me14e_pmac_str, s)
        sleep(0.02)
    print
    print 10*'Done '

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

def load_stock_map(map_choice):
    print 'Please wait, adjusting lite map'
    x33 = [31,32,33,40,51,50,49,42,41]
    x55 = [25,24,23,22,21,34,39,52,57,58,59,60,61,48,43,30] + x33
    x77 = [11,12,13,14,15,16,17,20,35,38,53,56,71,70,69,68,67,66,65,62,47,44,29,26] + x55
    x99 = [9,8,7,6,5,4,3,2,1,18,19,36,37,54,55,72,73,74,75,76,77,78,79,80,81,64,63,46,45,28,27,10] + x77
    x44 = [22,21,20,19,30,35,46,45,44,43,38,27,28,29,36,37]
    x66 = [10,11,12,13,14,15,18,31,34,47,50,51,52,53,54,55,42,39,26,23] + x44
    x88 = [8,7,6,5,4,3,2,1,16,17,32,33,48,49,64,63,62,61,60,59,58,57,56,41,40,25,24,9] + x66
    map_dict = {}
    map_dict['clear']= [1]
    map_dict['x33'] = x33
    map_dict['x44'] = x44
    map_dict['x55'] = x55
    map_dict['x66'] = x66
    map_dict['x77'] = x77
    map_dict['x88'] = x88
    map_dict['x99'] = x99
    print 'Clearing'
    for i in range(1, 82):
        pvar = 'ME14E-MO-IOC-01:GP' + str(i + 10)
        val = caget(pvar)
	if val == 1:
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

    chip_type = caget(pv.me14e_gp1) 
    if chip_type == 0:
	print 'Toronto Block Order'
	block_dict = toronto_block_dict
    elif chip_type == 1:
	print 'Oxford Block Order'
	block_dict = oxford_block_dict
    else:
	print 'here'

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

def moveto(place):
    print 5 * (place + ' ')
    chip_type = caget(pv.me14e_gp1)
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

    else:
	print 'Unknown chip_type move'

    if place == 'zero':
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, 0.0)

    elif place == 'yag':
        caput(pv.me14e_stage_x, 1.0)  
        caput(pv.me14e_stage_y, 1.0)  
        caput(pv.me14e_stage_z, 1.0)
   
    elif place == 'load_position':
        caput(pv.me14e_stage_x, 2.0)  
        caput(pv.me14e_stage_y, 2.0)
        caput(pv.me14e_stage_z, 2.0)

    elif place == 'collect_position':
        caput(pv.me14e_stage_x, 0.0)  
        caput(pv.me14e_stage_y, 0.0)
        caput(pv.me14e_stage_z, 0.0)

def fiducial(point):
    path = '/localhome/local/Documents/sacla/parameter_files/'
    x = caget(pv.me14e_stage_x + '.RBV')
    y = caget(pv.me14e_stage_y + '.RBV')
    z = caget(pv.me14e_stage_z + '.RBV')
    print 'Writing Fiducial File', 30*str(point)
    print path
    print '\n'.join([str(x),str(y),str(z)])
    f = open(path + 'fiducial_%s.txt' %point, 'w')
    f.write('%1.3f\n' %x)
    f.write('%1.3f\n' %y)
    f.write('%1.3f' %z)
    f.close() 
    print 'Writing Fiducial File', 30*str(point)
     
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
        x1factor = (f1_x / 18.975) * scale
        y1factor = (f1_y / f1_x)   * scale
        z1factor = (f1_z / f1_x)   * scale
        x2factor = (f2_x / f2_y)   * scale
        y2factor = (f2_y / 21.375) * scale
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
	pass

    else:
	print 'Unknown chip type'

    cs1 = "#1->%+1.3fX%+1.3fY%+1.3fZ" % (x1factor, y1factor, z1factor)
    cs2 = "#2->%+1.3fX%+1.3fY%+1.3fZ" % (-1*x2factor, 1*y2factor, z2factor)
    cs3 = "#3->0X+0Y%+fZ"    % (z3factor)
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
    
    caput(pv.me14e_pmac_str, '!x0y0z0')
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
    else:
	print 'yo'
    print 10*'CSDone '

def main(args):
    if args[1] == 'initialise':
        initialise()

    elif args[1] == 'moveto':
        moveto(args[2])
    elif args[1] == 'fiducial':
        fiducial(args[2])
    elif args[1] == 'cs_maker':
        cs_maker()
    elif args[1] == 'write_parameter_file':
        write_parameter_file()

    elif args[1] == 'define_current_chip':
        chipid = args[2]
        define_current_chip(chipid)
    elif args[1] == 'load_stock_map':
        map_choice = args[2]
        load_stock_map(map_choice)

    elif args[1] == 'load_lite_map':
	load_lite_map()
    elif args[1] == 'save_screen_map':
        save_screen_map()
    elif args[1] == 'upload_parameters':
        upload_parameters()

    else:
        print 'Unknown Command'

if  __name__ == '__main__':
    main(sys.argv)
