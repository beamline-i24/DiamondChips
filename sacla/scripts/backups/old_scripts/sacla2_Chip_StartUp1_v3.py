#!/usr/bin/python
import pv, os, re, sys
import time, math, string
from time import sleep
from ca import caput, caget 
import numpy as np

##############################################
# STARTUP  STARTUP  STARTUP  STARTUP STARTUP # 
# This version last edited 07Nov2016 by DAS  #
##############################################

def scrape_parameter_file():
    path = '/localhome/local/Documents/sacla/parameter_files/'
    f = open(path + 'parameters.txt', 'r').readlines()
    for line in f:
        entry = line.rstrip().split()
        if 'chip_name' in entry[0].lower():
            chip_name = entry[1]
        elif 'path' in entry[0].lower():
            path = entry[1]
        elif 'protein_name' in entry[0].lower():
            protein_name = entry[1]
        elif 'n_exposures' in entry[0].lower():
	    n_exposures = entry[1]
        elif 'chip_type' in entry[0].lower():
	    chip_type = entry[1]
        elif 'map_type' in entry[0].lower():
	    map_type = entry[1]
    return chip_name, path, protein_name, n_exposures, chip_type, map_type

def fiducials(chip_type):
    if chip_type == '0':
        corners_list = []
        for R in string.letters[26:35]:
            for C in [str(num) for num in range(1,10)]:
                for r in string.letters[:12]:
                    for c in string.letters[:12]:
                        addr = '_'.join([R+C, r+c])
                        if r+c in ['aa', 'la', 'll']:
                            corners_list.append(addr)
        position_list = [\
        'A1_ag', 'A2_ag', 'A3_ag', 'A4_ag', 'A5_ag', 'A6_ag', 'A7_ag', 'A8_ag','A9_ag', \
        'A1_aj', 'A2_bj', 'A3_cj', 'A4_ak', 'A5_bk', 'A6_ck', 'A7_al', 'A8_bl','A9_cl', \
        'B1_bg', 'B2_bg', 'B3_bg', 'B4_bg', 'B5_bg', 'B6_bg', 'B7_bg', 'B8_bg','B9_bg', \
        'B1_aj', 'B2_bj', 'B3_cj', 'B4_ak', 'B5_bk', 'B6_ck', 'B7_al', 'B8_bl','B9_cl', \
        'C1_cg', 'C2_cg', 'C3_cg', 'C4_cg', 'C5_cg', 'C6_cg', 'C7_cg', 'C8_cg','C9_cg', \
        'C1_aj', 'C2_bj', 'C3_cj', 'C4_ak', 'C5_bk', 'C6_ck', 'C7_al', 'C8_bl','C9_cl', \
        'D1_ah', 'D2_ah', 'D3_ah', 'D4_ah', 'D5_ah', 'D6_ah', 'D7_ah', 'D8_ah','D9_ah', \
        'D1_aj', 'D2_bj', 'D3_cj', 'D4_ak', 'D5_bk', 'D6_ck', 'D7_al', 'D8_bl','D9_cl', \
        'E1_bh', 'E2_bh', 'E3_bh', 'E4_bh', 'E5_bh', 'E6_bh', 'E7_bh', 'E8_bh','E9_bh', \
        'E1_aj', 'E2_bj', 'E3_cj', 'E4_ak', 'E5_bk', 'E6_ck', 'E7_al', 'E8_bl','E9_cl', \
        'F1_ch', 'F2_ch', 'F3_ch', 'F4_ch', 'F5_ch', 'F6_ch', 'F7_ch', 'F8_ch','F9_ch', \
        'F1_aj', 'F2_bj', 'F3_cj', 'F4_ak', 'F5_bk', 'F6_ck', 'F7_al', 'F8_bl','F9_cl', \
        'G1_ai', 'G2_ai', 'G3_ai', 'G4_ai', 'G5_ai', 'G6_ai', 'G7_ai', 'G8_ai','G9_ai', \
        'G1_aj', 'G2_bj', 'G3_cj', 'G4_ak', 'G5_bk', 'G6_ck', 'G7_al', 'G8_bl','G9_cl', \
        'H1_bi', 'H2_bi', 'H3_bi', 'H4_bi', 'H5_bi', 'H6_bi', 'H7_bi', 'H8_bi','H9_bi', \
        'H1_aj', 'H2_bj', 'H3_cj', 'H4_ak', 'H5_bk', 'H6_ck', 'H7_al', 'H8_bl','H9_cl', \
        'I1_ci', 'I2_ci', 'I3_ci', 'I4_ci', 'I5_ci', 'I6_ci', 'I7_ci', 'I8_ci','I9_ci', \
        'I1_aj', 'I2_bj', 'I3_cj', 'I4_ak', 'I5_bk', 'I6_ck', 'I7_al', 'I8_bl','I9_cl']
        fiducial_list = sorted(corners_list + position_list)

    elif chip_type == '2':
        fiducial_list = ['A1_aa', 'A1_a0', 'A1_00', 'A1_ba'] 
        print 'This list is INCOMPLETE'

    elif chip_type in ['1','3','4']:
        fiducial_list = [] 

    else:
        print 'Unknown chip_type in fiducials'
    return fiducial_list           

def get_format(chip_type):
    if chip_type == '0':
        w2w = 0.125
        b2b_horz = 0.825
        b2b_vert = 1.125
        chip_format = [9, 9, 12, 12]
    elif chip_type == '1':
        w2w = 0.125
        b2b_horz = 0.800
        b2b_vert = 0.800
        chip_format = [8, 8, 20, 20]
    elif chip_type == '2':
        w2w = 0.150
        b2b_horz = 0.780
        b2b_vert = 0.780
        chip_format = [3, 3, 53, 53]
    elif chip_type == '1':
        w2w = 0.600
        b2b_horz = 0.0
        b2b_vert = 0.0
        chip_format = [1, 1, 25, 25]
    else:
	    print 'unknown chip type'
    cell_format = chip_format + [w2w, b2b_horz, b2b_vert]
    return cell_format 

def get_xy(addr, chip_type):
    entry = addr.split('_')[-2:]
    R, C = entry[0][0], entry[0][1]
    r2, c2 = entry[1][0], entry[1][1]
    blockR = string.uppercase.index(R)
    blockC = int(C) - 1
    lowercase_list = list(string.ascii_lowercase + string.ascii_uppercase + '0')
    windowR = lowercase_list.index(r2)
    windowC = lowercase_list.index(c2)

    x_block_num, y_block_num, x_window_num, y_window_num, w2w, b2b_horz, b2b_vert = get_format(chip_type)

    x = (blockC * b2b_horz) + (blockC * (x_window_num-1) * w2w) + (windowC * w2w)
    y = (blockR * b2b_vert) + (blockR * (y_window_num-1) * w2w) + (windowR * w2w)
    return x, y 

def pathli(l=[], way='typewriter', reverse=False):
    if reverse == True:
        li = list(reversed(l))
    else:
	li = list(l)
    long_list = []
    if li:
        if way == 'typewriter':
            for i in range(len(li)**2):
              long_list.append(li[i%len(li)])
        elif way == 'snake':
            lr = list(reversed(li))
            for rep in range(len(li)):
                if rep%2 == 0:
                    long_list += li
                else: 
                    long_list += lr
        elif way == 'snake53':
            lr = list(reversed(li))
            for rep in range(53):
                if rep%2 == 0:
                    long_list += li
                else: 
                    long_list += lr
        elif way == 'expand':
            for entry in li:
                for rep in range(len(li)):
                    long_list.append(entry)
        elif way == 'expand28':
            for entry in li:
                for rep in range(28):
                    long_list.append(entry)
        elif way == 'expand25':
            for entry in li:
                for rep in range(25):
                    long_list.append(entry)
        else:
            print 'no known path'
    else:
        print 'no list'
    return long_list 
 
def zippum(list_1_args, list_2_args):
    list_1, type_1, reverse_1 = list_1_args
    list_2, type_2, reverse_2 = list_2_args
    A_path = pathli(list_1, type_1, reverse_1)
    B_path = pathli(list_2, type_2, reverse_2)
    zipped_list = []
    for a,b in zip(A_path, B_path):
        zipped_list.append(a + b)
    return zipped_list

def get_alphanumeric(chip_type):
    cell_format = get_format(chip_type)
    blk_num = cell_format[0]
    wnd_num = cell_format[2]
    uppercase_list = list(string.ascii_uppercase)[:blk_num]
    lowercase_list = list(string.ascii_lowercase + string.ascii_uppercase + '0')[:wnd_num]
    number_list = [str(x) for x in range(1,blk_num+1)]

    block_list = zippum([uppercase_list, 'expand', 0], [number_list, 'typewriter', 0])
    window_list = zippum([lowercase_list, 'expand', 0], [lowercase_list, 'typewriter', 0])

    alphanumeric_list = []
    for block in block_list:
        for window in window_list:
            alphanumeric_list.append(block + '_' + window)
    print len(alphanumeric_list)
    return alphanumeric_list

def get_shot_order(chip_type):
    cell_format = get_format(chip_type)
    blk_num = cell_format[0]
    wnd_num = cell_format[2]
    uppercase_list = list(string.ascii_uppercase)[:blk_num]
    number_list = [str(x) for x in range(1, blk_num+1)]
    lowercase_list = list(string.ascii_lowercase + string.ascii_uppercase + '0')[:wnd_num]
    
    block_list = zippum([uppercase_list, 'snake', 0], [number_list, 'expand', 0])
    window_dn = zippum([lowercase_list, 'expand', 0], [lowercase_list, 'snake', 0])
    window_up = zippum([lowercase_list, 'expand', 1], [lowercase_list, 'snake', 0])

    switch = 0
    count = 0
    collect_list = [] 
    for block in block_list:
    	if switch == 0:
    	    for window in window_dn:
    	        collect_list.append(block + '_' + window)
            count += 1
            if count == blk_num:
                count = 0
                switch = 1
    	else:
    	    for window in window_up:
    	        collect_list.append(block + '_' + window)
            count += 1
            if count == blk_num:
                count = 0
                switch = 0

    print len(collect_list)
    return collect_list

def write_file(suffix='.addr', order='alphanumeric'):
    chip_name, path, protein_name, n_exposures, chip_type, map_type = scrape_parameter_file()
    file_path = '/localhome/local/Documents/sacla/chips/' + protein_name
    full_file_path = file_path + '/' + chip_name + suffix

    fiducial_list = fiducials(chip_type)
    if order == 'alphanumeric':
        addr_list = get_alphanumeric(chip_type)
    elif order == 'shot':
        addr_list = get_shot_order(chip_type)

    list_of_lines = []
    for addr in addr_list:
       xtal_name = '_'.join([chip_name, addr])
       (x, y) = get_xy(xtal_name, chip_type)
       if addr in fiducial_list:
           pres = '0'
       else:
           #pres = '-1'
           pres = str(np.random.randint(2))
       line = '\t'.join([xtal_name, str(x), str(y), '0.0', pres]) + '\n'
       list_of_lines.append(line)

    g = open(full_file_path, 'a')
    for line in list_of_lines:
        g.write(line)
    g.close() 

def check_files(args):
    chip_name, path, protein_name, n_exposures, chip_type, map_type = scrape_parameter_file()
    file_path = path.replace('parameter_files', 'chips') + protein_name
    try:
        os.stat(file_path)
    except:
        os.makedirs(file_path)
    for suffix in args:
        full_file_path = file_path + '/' + chip_name + suffix
        if os.path.isfile(full_file_path):
            timestr = time.strftime("%Y%m%d_%H%M%S_")
            timestamp_fid = file_path + '/' + timestr + chip_name + suffix 
            os.rename(full_file_path, timestamp_fid)
            print 'Already exists ... moving old file:', timestamp_fid
    return 1

def write_headers(args):
    chip_name, path, protein_name, n_exposures, chip_type, map_type = scrape_parameter_file()
    for suffix in ['.addr', '.shot']:
        full_file_path = path.replace('parameter_files', 'chips') + protein_name + '/'+ chip_name + suffix
        g = open(full_file_path, 'w')
        g.write('#23456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\n#\n')
        g.write('#&SACLA\tchip_name    = %s\n'     %chip_name)
        g.write('#&SACLA\tlocalfolder  = %s\n'     %path)
        g.write('#&SACLA\tprotein_name = %s\n'     %protein_name)
        g.write('#&SACLA\tn_exposures  = %s\n'     %n_exposures)
        g.write('#&SACLA\tchip_type    = %s\n'     %chip_type)
        g.write('#&SACLA\tmap_type     = %s\n'     %map_type)
        g.write('#\n')
        g.write('#XtalAddr      XCoord  YCoord  ZCoord  Present Shot  Spare04 Spare03 Spare02 Spare01\n')
    g.close()

def run():
    print 'run StartUp'
    check_files(['.addr', '.shot'])
    write_headers(['.addr', '.shot'])
    write_file('.addr', 'alphanumeric')
    write_file('.shot', 'shot')
    write_file('rando.spec', 'shot')
    print 10*'Done '

def main():
    print 'In main'

if __name__ == '__main__':
    main()
