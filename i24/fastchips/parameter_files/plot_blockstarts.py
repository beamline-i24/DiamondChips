#!/usr/bin/python
import os, re, sys
import math, time, string
import numpy as np
import matplotlib.pyplot as plt

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
    print '\n\n\n\n'

    fig = plt.figure(figsize=(15, 15))
    fig.subplots_adjust(left   = 0.05,
                        bottom = 0.05,
                        right  = 0.95, 
                        top    = 0.95,
                        wspace = 0.00, 
                        hspace = -0.0)

    axs = fig.add_subplot(111, axisbg='white')

    fid_list = ['oxford_darren.BAK', 'oxford.pvar']
    c_list = ['k','r']
    x_list, y_list = [],[]
    b_list = []
    for i, fid in enumerate(fid_list):
        block_start_list = scrape_pvar_file(fid)
        for entry in block_start_list:
            block, x, y = entry
	    x_list.append(float(x))
	    y_list.append(float(y))
            b_list.append((float(x), float(y)))
	    axs.plot(float(x), float(y), marker='o', ms=10, alpha=0.8, c=c_list[i])


    #X1,Y1 = np.mgrid[0:22.225:4j, 0:22.225:4j]
    #X2,Y2 = np.mgrid[0:22.225:4j, 24.6:2.375:4j]
    #axs.scatter(X1,Y1)
    #axs.scatter(X2,Y2)

    x = np.array(x_list)
    y = np.array(y_list)
    x3,y3 = np.meshgrid(x, y)
    #axs.scatter(x3, y3)

    b = np.array(b_list)
    #axs.scatter(b)
    #axs.plot(b, marker='o')

    
    axs.invert_yaxis()
    plt.show()

    print '\n\n\n\n', 10*'Done '

if __name__ == '__main__':
    main()
plt.close()
