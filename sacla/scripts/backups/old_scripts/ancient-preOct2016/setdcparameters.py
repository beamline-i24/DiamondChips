import sys
import time
import subprocess
from subprocess import Popen, PIPE
from time import sleep

def evaluate(val):
    try:
        int(val)
        return int(val)
    except:
        try:
            float(val)
            return float(val)
        except ValueError:
            return val

def caget(pv):
    print 'Caget', pv,
    a = Popen(['caget', pv], stdout=PIPE, stderr=PIPE) 
    a_stdout, a_stderr = a.communicate()
    val = a_stdout.split()[1]
    val = evaluate(val)
    print val
    return val

def main():
    visitID = '/dls/i24/data/2016/cm14486-1'
    filepath = caget('ME14E-MO-CHIP-01:filePath')
    chipname = caget('ME14E-MO-CHIP-01:chipName')
    chipcapacity = caget('ME14E-MO-CHIP-01:chipCapacity')
    blockcapacity = caget('ME14E-MO-CHIP-01:blockCapacity')
    exptime = caget('ME14E-MO-CHIP-01:expTime')
    dcdetdist=caget('ME14E-MO-CHIP-01:detDistance')

    print '\n','\n', 'Visit:', visitID
    print 'filepath:', filepath
    print 'chipname:', chipname
    print 'chip capacity:', chipcapacity
    print 'block capacity:', blockcapacity
    print 'exposure time:', exptime
    print 'detector distance:', dcdetdist
    print '\n'


    f = open('/dls_sw/work/R3.14.12.3/ioc/ME14E/ME14E-MO-IOC-01/ME14E-MO-IOC-01App/scripts/datacollparameters.txt','w')
    line1 ="visit \t%s\n" %(visitID)
    line2 ="filepath \t%s\n" %(filepath)
    line3 ="chipname \t%s\n" %(chipname)
    line4 ="chipcapacity \t%s\n" %(chipcapacity)
    line5 ="blockcapacity \t%s\n" %(blockcapacity)
    line6 ="exposure \t%s\n" %(exptime)
    line7 ='distance \t%s\n' %(dcdetdist)

    f.write(line1)
    f.write(line2)
    f.write(line3)
    f.write(line4)
    f.write(line5)
    f.write(line6)
    f.write(line7)

if __name__ == '__main__':
    main()
