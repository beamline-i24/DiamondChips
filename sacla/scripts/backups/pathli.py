#!/usr/bin/python
import string

def get_format(chip_type):
    if chip_type == '0':
	return [9, 12]
    elif chip_type == '1':
	return [8, 20]
    elif chip_type == '2':
	return [3, 53]
    else:
	print 'chip_type error in get_format'
        return 0

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
        elif way == 'expand':
            for entry in li:
                for rep in range(len(li)):
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
    chip_format = get_format(chip_type)
    blk_num = chip_format[0]
    wnd_num = chip_format[1]
    uppercase_list = list(string.ascii_uppercase)[:blk_num]
    lowercase_list = list(string.ascii_lowercase + string.ascii_uppercase + '0')[:wnd_num]
    print len(lowercase_list)
    number_list = [str(x) for x in range(1,blk_num+1)]

    block_list = zippum([uppercase_list, 'expand', 0], [number_list, 'typewriter', 0])
    window_list = zippum([lowercase_list, 'expand', 0], [lowercase_list, 'typewriter', 0])

    alphanumeric_list = []
    for block in block_list:
        for window in window_list:
            alphanumeric_list.append(block + '_' + window)
    print len(alphanumeric_list)
    return alphanumeric_list

def get_collect_order(chip_type):
    chip_format = get_format(chip_type)
    blk_num = chip_format[0]
    wnd_num = chip_format[1]
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
	
def test():
    pathli_0 = pathli([], '')
    pathli_0 = pathli(['f', 'u'], '')
    pathli_0 = pathli(['f', 'u'], 'typewriter')
    pathli_0 = pathli(['f', 'u'], 'typewriter', 1)
    pathli_0 = pathli(['f', 'u'], 'snake', 0)

    l =  ['h','e','l','p','me']
    print 'eeeeeeeeee', l
    pathli_1 = pathli(l, 'typewriter')
    print 'eeeeeeeeee', l
    pathli_1 = pathli(l, 'typewriter', reverse=True)
    print 'eeeeeeeeee', l
    print 'fffffffffffffffffff'
    print 'list'
    print l
    print 'fffffffffffffffffff'
    pathli_2 = pathli(l, 'snake')
    print 'snake'
    print pathli_2
    print 'fffffffffffffffffff'
    pathli_1 = pathli(l, 'snake', reverse=True)
    print 'snake reverse'
    print pathli_1
    print 'fffffffffffffffffff'

    #alphanumeric test
    wind_list = ['a','b','c']
    windreps = pathli(wind_list, 'expand')
    windlong = pathli(wind_list, 'typewriter')
    alphanumeric_list = []
    for a,b in zip(windreps, windlong):
	alphanumeric_list.append(a+b)
    #print alphanumeric_list

def main():

    classic_list = get_alphanumeric('0')
    magis_list = get_alphanumeric('1')
    hll_list = get_alphanumeric('2')
    for x in hll_list[-60:]: print x,

    classic_path = get_collect_order('0')
    magis_path = get_collect_order('1')
    hll_path = get_collect_order('2')

if __name__ == '__main__':
    main()
