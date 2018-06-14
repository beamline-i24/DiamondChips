#!/usr/bin/python
import pv
from ca import caget, caput
import os, re, sys
import math, time, string

def scrape_pvar_file(fid):
    block_start_list = []
    f = open(fid,'r')
    for line in f.readlines():
        line = line.rstrip()
        if line.startswith('#'):
            continue
        elif line.startswith('P3000'):
            continue
        elif line.startswith('P3011'):
            continue
        elif not len(line.split(' ')) == 2:
            continue
        else:
            entry = line.split(' ')
            block_num = entry[0][2:4]
            x = entry[0].split('=')[1]
            y = entry[1].split('=')[1]
            block_start_list.append([block_num, x, y])
    f.close()
    return block_start_list

def main():
    block_start_list = scrape_pvar_file('oxford.pvar')
    for entry in block_start_list:
        block, x, y = entry
        print block, x, y
        caput(pv.me14e_pmac_str, '!x%sy%s' %(x,y)) 
        time.sleep(0.4)
    print 10*'Done '

if __name__ == '__main__':
    main()
