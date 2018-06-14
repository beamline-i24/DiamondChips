import pv
import os, re, sys
import time, math, string
from time import sleep
from ca import caput, caget 

###############################################
# OLD Chip_StartUp from SACLA1  experiment    #
# This version last edited 21Oct2016 by DAS   #
###############################################

def classic_fiducials():
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
    return fiducial_list           

def get_xy(addr, chip_type='classic'):
    if chip_type == 'classic':
        w2w = 0.125
        b2b_horz = 0.825
        b2b_vert = 1.125
        cell_format = [9, 9, 12, 12]
    else:
	print 'unknown chip type'
    entry = addr.split('_')[-2:]
    R, C = entry[0][0], entry[0][1]
    r2, c2 = entry[1][0], entry[1][1]
    blockR = string.uppercase.index(R)
    blockC = int(C) - 1
    windowR = string.lowercase.index(r2)
    windowC = string.lowercase.index(c2)
    x = (blockC * b2b_horz) + (blockC * (cell_format[2]-1) * w2w) + (windowC * w2w)
    y = (blockR * b2b_vert) + (blockR * (cell_format[3]-1) * w2w) + (windowR * w2w)
    return x, y 

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

def alphanumeric(chip_name):
    list_of_lines = []
    fiducial_list = classic_fiducials()
    for R in string.letters[26:35]:
        for C in [str(num) for num in range(1,10)]:
            for r in string.letters[:12]:
                for c in string.letters[:12]:
                    addr = '_'.join([R+C, r+c])
                    xtal_name = '_'.join([chip_name, addr])
                    (x, y) = get_xy(xtal_name)
                    if addr in fiducial_list:
                        pres = '0'
                    else:
                        pres = '-1'
                    line = '\t'.join([xtal_name, str(x), str(y), '0.0', pres]) + '\n'
                    list_of_lines.append(line)
    return list_of_lines

def shot_order(chip_name):
    road_list = ['A','B','C','D','E','F','G','H','I']
    daor_list = ['I','H','G','F','E','D','C','B','A']
    cros_list = ['1','2','3','4','5','6','7','8','9']
    wind_list = ['a','b','c','d','e','f','g','h','i','j','k','l']
    dniw_list = ['l','k','j','i','h','g','f','e','d','c','b','a']
    fiducial_list = classic_fiducials()
    list_of_lines = []
    for C in range(9):
        for R in range(9):
            for c in range(12):
                for r in range(12):
                    if (C % 2 == 0):
                        if (c % 2 == 0):
                            addr = road_list[R] + cros_list[C] + '_' + wind_list[c] + wind_list[r]
                        else:
                            addr = road_list[R] + cros_list[C] + '_' + wind_list[c] + dniw_list[r]
                    else:
                        if (c % 2 == 0):
                            addr = daor_list[R] + cros_list[C] + '_' + dniw_list[c] + wind_list[r]
                        else:
                            addr = daor_list[R] + cros_list[C] + '_' + dniw_list[c] + dniw_list[r]
                    xtal_name = '_'.join([chip_name, addr])
                    (x, y) = get_xy(xtal_name)
                    if addr in fiducial_list:
                        pres = '0'
                    else:
                        pres = '-1'
                    line = '\t'.join([xtal_name, str(x), str(y), '0.0', pres]) + '\n'
                    list_of_lines.append(line)
    return list_of_lines

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
        g.write('#&SACLA\tprotein_name = %s\n'    %protein_name)
        g.write('#&SACLA\tn_exposures  = %s\n'     %n_exposures)
        g.write('#&SACLA\tchip_type    = %s\n'     %chip_type)
        g.write('#&SACLA\tmap_type     = %s\n'     %map_type)
        g.write('#\n')
        g.write('#XtalAddr      XCoord  YCoord  ZCoord  Present Shot  Spare04 Spare03 Spare02 Spare01\n')
    g.close()

def write_file(suffix='.addr', order='alphanumeric'):
    chip_name, path, protein_name, n_exposures, chip_type, map_type = scrape_parameter_file()
    file_path = '/localhome/local/Documents/sacla/chips/' + protein_name
    full_file_path = file_path + '/' + chip_name + suffix
    g = open(full_file_path, 'a')
    if order == 'alphanumeric':
        for line in alphanumeric(chip_name):
            g.write(line)
    elif order == 'shot_order':
        for line in shot_order(chip_name):
            g.write(line)
    else:
	print '?'
    g.close() 

def main():
    check_files(['.addr', '.shot'])
    write_headers(['.addr', '.shot'])
    write_file('.addr', 'alphanumeric')
    write_file('.shot', 'shot_order')

if __name__ == '__main__':
    main()
