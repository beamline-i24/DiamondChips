import pv
import os, re, sys
import time, math, string
from time import sleep
from ca import caput, caget 

##########################################
# NEW Chip_Manager for SACLA  experiment #
# This version last edited 04 Mar by DAS #
##########################################

def addr_scrape(fid):
    f = open(fid, 'r').readlines()
    chipname = fid.split('.')[0]
    for line in f:
        if line.startswith("#&SACLA"):
            entry = line.rstrip().split()
            if 'filepath' in entry[1].lower():
                filepath = str(entry[3])
            elif 'chipcapacity' in entry[1].lower():
                chipcapacity = int(entry[3])
            elif 'blockcapacity' in entry[1].lower():
                blockcapacity = int(entry[3])
            elif 'exptime' in entry[1].lower():
                exptime = float(entry[3])
            else:
                print line, entry
        else:
            pass
    if 'dls/i24/data' in filepath:
        filepath = filepath.replace('dls/i24/data','ramdisk')
        print 'Detector filepath:', filepath
    else:
        print 'Possible filepath error, expected /dls/i24/data/ in filepath'
        print '    -------------->', chipname, filepath, chipcapacity, blockcapacity, exptime
    return chipname, filepath, chipcapacity, blockcapacity, exptime

def get_xy(addr, chip_type=11664):
    w2w = 0.125
    b2b_horz = 0.825
    b2b_vert = 1.125
    cell_format = [9, 9, 12, 12]
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

def make_path_dict():
    path_dict = {}
    path_dict[11] = [0, 0, 1, 1['A1_aa']]
    path_dict[12] = [0, 0, 1, 2['A1_aa','B1_aa']]
    path_dict[14] = [0, 0, 1, 4['A1_aa','A2_la','A3_aa','A4_la']]
    path_dict[19] = [0, 0, 1, 9['A1_aa','B1_aa','C1_aa','D1_aa','E1_aa','F1_aa','G1_aa','H1_aa','I1_aa']]
    path_dict[23] = [0, 0, 2, 3['A1_aa','B1_aa','C1_aa','C2_la','B2_la','A2_la']]
    path_dict[77] = [['H2_la','G2_la','F2_la','E2_la','D2_la','C2_la','B2_la',\
                     'B3_aa','C3_aa','D3_aa','E3_aa','F3_aa','G3_aa','H3_aa',\
                     'H4_la','G4_la','F4_la','E4_la','D4_la','C4_la','B4_la',\
                     'B5_aa','C5_aa','D5_aa','E5_aa','F5_aa','G5_aa','H5_aa',\
                     'H6_la','G6_la','F6_la','E6_la','D6_la','C6_la','B6_la',\
                     'B7_aa','C7_aa','D7_aa','E7_aa','F7_aa','G7_aa','H7_aa',\
                     'H8_la','G8_la','F8_la','E8_la','D8_la','C8_la','B8_la',]]
    path_dict[99] = [0, 0, 9, 9['A1_aa','B1_aa','C1_aa','D1_aa','E1_aa','F1_aa','G1_aa','H1_aa','I1_aa',\
                     'I2_la','H2_la','G2_la','F2_la','E2_la','D2_la','C2_la','B2_la','A2_la',\
                     'A3_aa','B3_aa','C3_aa','D3_aa','E3_aa','F3_aa','G3_aa','H3_aa','I3_aa',\
                     'I4_la','H4_la','G4_la','F4_la','E4_la','D4_la','C4_la','B4_la','A4_la',\
                     'A5_aa','B5_aa','C5_aa','D5_aa','E5_aa','F5_aa','G5_aa','H5_aa','I5_aa',\
                     'I6_la','H6_la','G6_la','F6_la','E6_la','D6_la','C6_la','B6_la','A6_la',\
                     'A7_aa','B7_aa','C7_aa','D7_aa','E7_aa','F7_aa','G7_aa','H7_aa','I7_aa',\
                     'I8_la','H8_la','G8_la','F8_la','E8_la','D8_la','C8_la','B8_la','A8_la',\
                     'A9_aa','B9_aa','C9_aa','D9_aa','E9_aa','F9_aa','G9_aa','H9_aa','I9_aa']]
    return path_dict

def scrape_dcparameters():
    f = open('/localhome/local/Documents/sacla/parameter_files/setdcparams.txt', 'r').readlines()
    for line in f:
        entry = line.rstrip().split()
        if 'chipname' in entry[0].lower():
            chipname = entry[1]
        elif 'visit_id' in entry[0].lower():
            visit_id = entry[1]
        elif 'filepath' in entry[0].lower():
            filepath = entry[1]
        elif 'chipcapacity' in entry[0].lower():
            chipcapacity = entry[1]
        elif 'blockcapacity' in entry[0].lower():
            blockcapacity = entry[1]
    print chipname
    print visit_id
    print filepath
    print chipcapacity
    print blockcapacity
    return chipname, visit_id, filepath, chipcapacity, blockcapacity

def get_chip_dict(chip_fid):
    chip_dict = {}
    try:
        f = open(chip_fid, 'r')
    except IOError as e:
        print 'Total Fail', e.errno, e.strerror
    else:
        ############################################
        #for line in f.readlines()[6:40]:
        for line in f.readlines()[6:10]:
            xtal_dict = {}
            entry = line.rstrip('\n').split('\t')
            if '-----------' in entry[1]:
                continue
            else:
                xtal_name = entry[0]         
                xtal_dict['xtal_name'] = xtal_name         
                xtal_dict['xtal_pres'] = entry[1]
                xtal_dict['xtal_spec'] = entry[2]
                xtal_dict['xtal_dat1'] = entry[3]
                xtal_dict['xtal_dat2'] = entry[4]
                xtal_dict['xtal_fnsh'] = entry[5]
                chip_dict[xtal_name] = xtal_dict 
    return chip_dict 

def index11664():
    road_list = ['Adams','Bush','Clinton','Dwight','Eisenhwr', 'Ford', 'Grant', 'Hoover', 'India']
    cross_list = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th','9th']
    block_row_list = ['a','b','c','d','e','f','g','h','i','j','k','l']
    block_col_list = ['a','b','c','d','e','f','g','h','i','j','k','l']
    return road_list, cross_list, block_row_list, block_col_list

def index11664_fiducials():
    road_list, cross_list, block_row_list, block_col_list = index11664()
    corners_list = []
    for road in road_list:
        for cross in cross_list:
            for r2 in block_row_list:
                for c2 in block_col_list:
                    addr = road[0] + cross[:-2] + '_' + r2 + c2
                    if r2+c2 in ['aa', 'la', 'll']:
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

def CheckFile(path, fid):
    if os.path.isfile(path + '/' + fid):
        timestr = time.strftime("%Y%m%d_%H%M%S_")
        timestamp_fid = path + '/' + timestr + fid 
        os.rename(path + '/' + fid, timestamp_fid)
        print '\n', path + fid, 'already exists ... moving old file to:\n', timestamp_fid
    return 1

def SaveFile(tmp_fid, fid):
    if os.path.isfile(fid):
        timestr = time.strftime("%Y%m%d_%H%M%S_")
        timestamp_fid = timestr + fid 
        os.rename(fid, timestamp_fid)
        print '\n', fid, 'already exists ... moving old file to:', timestamp_fid
        print 'Saving', fid
        os.rename(tmp_fid, fid)
        if os.path.isfile(fid):
            print fid, 'Saved'
        else:
            print 'An Error Occured Saving', fid
    else:
        print '\nSaving', fid
        os.rename(tmp_fid, fid)
        if os.path.isfile(fid):
            print fid, 'Saved'
        else:
            print 'An Error Occured Saving', fid

def shotLister_W_SnakeRows(path, fid):
    f = open(path + '/' + fid, 'r')
    header = f.readlines()[:11]
    f.close()
    chip_dict = {}
    f = open(path + '/' + fid, 'r')
    for line in f.readlines()[11:]:
        entry = line.split('\t')
        addr = entry[0][-5:]
        chip_dict[addr] = entry
    f.close()
    road_list = ['A','B','C','D','E','F','G','H','I']
    daor_list = ['I','H','G','F','E','D','C','B','A']
    cros_list = ['1','2','3','4','5','6','7','8','9']
    sorc_list = ['9','8','7','6','5','4','3','2','1']
    wind_list = ['a','b','c','d','e','f','g','h','i','j','k','l']
    dniw_list = ['l','k','j','i','h','g','f','e','d','c','b','a']
    shot_list = []
    for r in range(9):
        for c in range(9):
            for wr in range(12):
                for wc in range(12):
                    if (r % 2 == 0):
                        if (wr % 2 == 0):
                            addr = road_list[r] + cros_list[c] + '_' + wind_list[wc] + wind_list[wr]
                            shot_list.append(addr)
                            #print addr
                        else:
                            addr = road_list[r] + cros_list[c] + '_' + dniw_list[wc] + wind_list[wr]
                            shot_list.append(addr)
                            #print addr
                    else:
                        if (wr % 2 == 0):
                            addr = road_list[r] + sorc_list[c] + '_' + wind_list[wc] + dniw_list[wr]
                            shot_list.append(addr)
                            #print 't', addr
                        else:
                            addr = road_list[r] + sorc_list[c] + '_' + dniw_list[wc] + dniw_list[wr]
                            shot_list.append(addr)
                            #print 't', addr
    spec_fid = fid[:-4] + 'spec'
    print spec_fid
    g = open(path + '/' + spec_fid, 'w')
    for x in header:
        g.write(x)
    for x in shot_list:
        line = '\t'.join(chip_dict[x])
        g.write(line)
    g.close()
    return 0

def shotLister_E_SnakeCols(path, fid):
    f = open(path + '/' + fid, 'r')
    header = f.readlines()[:11]
    f.close()
    chip_dict = {}
    f = open(path + '/' + fid, 'r')
    for line in f.readlines()[11:]:
        entry = line.split('\t')
        addr = entry[0][-5:]
        chip_dict[addr] = entry
    f.close()
    road_list = ['A','B','C','D','E','F','G','H','I']
    daor_list = ['I','H','G','F','E','D','C','B','A']
    cros_list = ['1','2','3','4','5','6','7','8','9']
    sorc_list = ['9','8','7','6','5','4','3','2','1']
    wind_list = ['a','b','c','d','e','f','g','h','i','j','k','l']
    dniw_list = ['l','k','j','i','h','g','f','e','d','c','b','a']
    shot_list = []
    for c in range(9):
        print
        for r in range(9):
            print
            for wc in range(12):
                print
                for wr in range(12):
                    if (c % 2 == 0):
                        if (wc % 2 == 0):
                            addr = road_list[r] + cros_list[c] + '_' + wind_list[wc] + wind_list[wr]
                            shot_list.append(addr)
                            print addr,
                        else:
                            addr = road_list[r] + cros_list[c] + '_' + wind_list[wc] + dniw_list[wr]
                            shot_list.append(addr)
                            print addr,
                    else:
                        if (wc % 2 == 0):
                            addr = daor_list[r] + cros_list[c] + '_' + dniw_list[wc] + wind_list[wr]
                            shot_list.append(addr)
                            print addr,
                        else:
                            addr = daor_list[r] + cros_list[c] + '_' + dniw_list[wc] + dniw_list[wr]
                            shot_list.append(addr)
                            print addr
    spec_fid = fid[:-4] + 'shot'
    print spec_fid
    g = open(path + '/' + spec_fid, 'w')
    for x in header:
        g.write(x)
    for x in shot_list:
        line = '\t'.join(chip_dict[x])
        g.write(line)
    g.close()
    return 0

def shotLister_E_SnakeCols_reverse(path, fid):
    print 'Writing Shot'
    f = open(path + '/' + fid, 'r')
    header = f.readlines()[:11]
    f.close()
    chip_dict = {}
    f = open(path + '/' + fid, 'r')
    for line in f.readlines()[11:]:
        entry = line.split('\t')
        addr = entry[0][-5:]
        chip_dict[addr] = entry
    f.close()
    road_list = ['A','B','C','D','E','F','G','H','I']
    daor_list = ['I','H','G','F','E','D','C','B','A']
    cros_list = ['1','2','3','4','5','6','7','8','9']
    sorc_list = ['9','8','7','6','5','4','3','2','1']
    wind_list = ['a','b','c','d','e','f','g','h','i','j','k','l']
    dniw_list = ['l','k','j','i','h','g','f','e','d','c','b','a']
    shot_list = []
    for c in range(9):
        for r in range(9):
            for wc in range(12):
                for wr in range(12):
                    if (c % 2 == 0):
                        if (wc % 2 == 0):
                            addr = daor_list[r] + sorc_list[c] + '_' + dniw_list[wc] + dniw_list[wr]
                            shot_list.append(addr)
                        else:
                            addr = daor_list[r] + sorc_list[c] + '_' + dniw_list[wc] + wind_list[wr]
                            shot_list.append(addr)
                    else:
                        if (wc % 2 == 0):
                            addr = road_list[r] + sorc_list[c] + '_' + wind_list[wc] + dniw_list[wr]
                            shot_list.append(addr)
                        else:
                            addr = road_list[r] + sorc_list[c] + '_' + wind_list[wc] + wind_list[wr]
                            shot_list.append(addr)
    spec_fid = fid[:-4] + 'shot'
    print spec_fid
    g = open(path + '/' + spec_fid, 'w')
    for x in header:
        g.write(x)
    for x in shot_list:
        line = '\t'.join(chip_dict[x])
        g.write(line)
    g.close()
    return 0

def shotLister_L2RWs_TypewriterRows(fid):
    f = open(fid, 'r')
    header = f.readlines()[:6]
    f.close()
    
    chip_dict = {}
    f = open(fid, 'r')
    for line in f.readlines()[6:]:
        entry = line.split('\t')
        addr = entry[0][-5:]
        chip_dict[addr] = entry
    f.close()
    
    road_list = ['A','B','C','D','E','F','G','H','I']
    cros_list = ['1','2','3','4','5','6','7','8','9']
    wndw_list = ['a','b','c','d','e','f','g','h','i','j','k','l']
    rvrs_list = ['l','k','j','i','h','g','f','e','d','c','b','a']
    
    shot_list = []
    for r in range(9):
        for c in range(9):
            for wr in range(12):
                for wc in range(12):
                    if (wr % 2 == 0):
                        addr = road_list[r] + cros_list[c] + '_' + wndw_list[wc] + wndw_list[wr]
                        shot_list.append(addr)
                        #print addr
                    else:
                        addr = road_list[r] + cros_list[c] + '_' + rvrs_list[wc] + wndw_list[wr]
                        shot_list.append(addr)
                        #print addr
            #print
    tmp_spec_fid = 'Oxfile.spec'
    g = open(tmp_spec_fid, 'w')
    for x in header: g.write(x)
    for x in shot_list:
        line = '\t'.join(chip_dict[x])
        g.write(line)
    g.close()

    spec_fid = fid[:-4] + 'spec'
    print spec_fid
    SaveFile(tmp_spec_fid, spec_fid)
    return 0

def main():
    road_list, cross_list, block_row_list, block_col_list = index11664()
    fiducial_list = index11664_fiducials()
    chipname, visit_id, filepath, chipcapacity, blockcapacity = scrape_dcparameters()
    path = visit_id + '/chips/' + filepath
    try:
        os.stat(path)
    except:
        os.makedirs(path)
    fid = chipname + '.addr'
    CheckFile(path, fid)
    g = open(path + '/' + fid, 'w')
    line1 = '#23456789012345678901234567890123456789012345678901234567890123456789012345678901234567890\n#\n'
    line2 = '#&SACLA\tproteinname = %s\n'       %filepath
    line3 = '#&SACLA\tlocalfolder = %s\n'       %visit_id
    line4 = '#&SACLA\tchipname = %s\n'       %chipname
    line5 = '#&SACLA\tchipcapacity = %s\n'   %chipcapacity
    line6 = '#&SACLA\tblockcapacity = %s\n'  %blockcapacity
    line7 = '#\n'    
    line8 = '#XtalAddr      XCoord  YCoord  ZCoord  Present Shot  Spare04 Spare03 Spare02 Spare01\n'    
    g.write(line1)
    g.write(line2)
    g.write(line3)
    g.write(line4)
    g.write(line5)
    g.write(line6)
    g.write(line7)
    g.write(line8)
    previous_x, previous_y = 0.0, 0.0
    available_addr_list = []
    for road in road_list:
        for cross in cross_list:
            city_block = road + ' & ' + cross
            city_block_short = road[0] + cross[:-2]
            for r2 in block_row_list:
                for c2 in block_col_list:
                    block_addr = r2 + c2
                    addr = '_'.join([city_block_short, block_addr])
                    xtal_name = '_'.join([chipname, city_block_short, block_addr])
                    (x, y) = get_xy(xtal_name)
                    if addr in fiducial_list:
                        xtal_xcrd = str(x) 
                        xtal_ycrd = str(y)
                        xtal_zcrd = '0.0'
                        xtal_pres = '0'
                        line = '\t'.join([xtal_name, xtal_xcrd, xtal_ycrd, xtal_zcrd, xtal_pres]) + '\n'
                        g.write(line)
                    else:
                        available_addr_list.append(addr)
                        xtal_xcrd = str(x) 
                        xtal_ycrd = str(y)
                        xtal_zcrd = '0.0'
                        xtal_pres = '1'
                        line = '\t'.join([xtal_name, xtal_xcrd, xtal_ycrd, xtal_zcrd, xtal_pres]) + '\n'
                        g.write(line)
                    previous_x = x
                    previous_y = y
                #print
    g.close() 
    x = shotLister_W_SnakeRows(path, fid)
    y = shotLister_E_SnakeCols_reverse(path, fid)

if __name__ == '__main__':
    main()
