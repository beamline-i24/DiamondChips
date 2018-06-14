import sys
import time
import subprocess

def main(which_way):

    if which_way == 'YAG':
        print 'Go to', which_way
        subprocess.call(['caput','ME14E-MO-CHIP-01:X, '43'])
        time.sleep(0.1)
        subprocess.call(['caput','ME14E-MO-CHIP-01:Y, '-33'])
        time.sleep(1.0)
        subprocess.call(['caput','BL24I-RS-ABSB-02:MP:SELECT', 'CheckBeam'])
        print 'YAG in. Chip out'
   
    elif which_way == 'chip':
        print 'Go to',which_way
        subprocess.call(['caput','BL24I-RS-ABSB-02:MP:SELECT', 'Data Collection'])
        subprocess.call(['caput','BL24I-AL-APTR-01:MP:SELECT', 'In'])
        time.sleep(1.0)
        subprocess.call(['caput','ME14E-MO-CHIP-01:X, '0'])
        time.sleep(0.1)
        subprocess.call(['caput','ME14E-MO-CHIP-01:Y, '0'])
        print 'YAG out. Apertures in. Chip in.'

    elif which_way == 'load':
        print 'Go to',which_way
        #Haven't tested these positions
        subprocess.call(['caput','ME14E-MO-CHIP-01:X, '43'])
        time.sleep(0.1)
        subprocess.call(['caput','ME14E-MO-CHIP-01:Y, '-33'])
        time.sleep(0.1)
        subprocess.call(['caput','ME14E-MO-CHIP-01:Z, '10'])
        subprocess.call(['caput','BL24I-RS-ABSB-02:MP:SELECT', 'Robot'])
        subprocess.call(['caput','BL24I-AL-APTR-01:MP:SELECT', 'Out'])
        subprocess.call(['caput', 'BL24I-EA-DET-01:Z', '1499'])
        print 'Ready for chip exchange'

    else:
        print 'Great Big Error'

    return 0

if __name__ == '__main__':
    main(sys.argv[1])
