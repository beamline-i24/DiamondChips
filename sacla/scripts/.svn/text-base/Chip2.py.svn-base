import os
import sys
import time
from subprocess import Popen, PIPE

def CoordinateSystem(fiducial_dict):
    #1mm / counts per nanometer (give cts/mm)
    scale = 10000
    #d1, d2 = fiducial_positions
    f1 = open('/dls_sw/work/R3.14.12.3/ioc/ME14E/ME14E-MO-IOC-01/ME14E-MO-IOC-01App/scripts/fiducial_1.txt','r')    
    f1_lines = f1.readlines()
    f1_lines_x = f1_lines[0].rstrip('/n') 
    f1_lines_y = f1_lines[1].rstrip('/n') 
    f1_lines_z = f1_lines[2].rstrip('/n') 
    f1_x = float(f1_lines_x)
    f1_y = float(f1_lines_y)
    f1_z = float(f1_lines_z)

    f2 = open('/dls_sw/work/R3.14.12.3/ioc/ME14E/ME14E-MO-IOC-01/ME14E-MO-IOC-01App/scripts/fiducial_2.txt','r')    
    f2_lines = f2.readlines()
    f2_lines_x = f2_lines[0].rstrip('/n') 
    f2_lines_y = f2_lines[1].rstrip('/n') 
    f2_lines_z = f2_lines[2].rstrip('/n') 
    f2_x = float(f2_lines_x)
    f2_y = float(f2_lines_y)
    f2_z = float(f2_lines_z)

    #Evaluate numbers
    x1factor = (f1_x / fiducial_dict['f1']['x']) *scale
    y1factor = (f1_y / f1_x)                     *scale
    z1factor = (f1_z / f1_x)                     *scale

    x2factor = (f2_x / f2_y)                     *scale
    y2factor = (f2_y / fiducial_dict['f2']['y']) *scale
    z2factor = (f2_z / f2_y)                     *scale

    z3factor = 1                                 *scale

    cs1 = "#1->%+1.5fX%+1.5fY%+1.5fZ" % (x1factor, y1factor, z1factor)
    cs2 = "#2->%+1.5fX%+1.5fY%+1.5fZ" % (-1*x2factor, y2factor, z2factor)
    cs3 = "#3->%+1.5fX%+1.5fY%+1.5fZ" % (z1factor, z2factor, z3factor)
     
    print cs1
    print cs2
    print cs3
    zz = Popen(['caput', 'ME14E-MO-CHIP-01:PMAC_STRING', '!x0y0z0'], stdout=PIPE , stderr=PIPE)
    time.sleep(2)
    a = Popen(['caput', 'ME14E-MO-CHIP-01:PMAC_STRING', cs1], stdout=PIPE , stderr=PIPE)
    time.sleep(2)
    b = Popen(['caput', 'ME14E-MO-CHIP-01:PMAC_STRING', cs2], stdout=PIPE , stderr=PIPE)
    time.sleep(2)
    c = Popen(['caput', 'ME14E-MO-CHIP-01:PMAC_STRING', cs3], stdout=PIPE , stderr=PIPE)

    a_stdout, a_stderr = a.communicate() 
    b_stdout, b_stderr = b.communicate() 
    c_stdout, c_stderr = c.communicate() 

    print a_stdout
    print b_stdout
    print c_stdout

def fiducial(point):
    x = Popen(['caget', 'ME14E-MO-CHIP-01:X.RBV'], stdout=PIPE , stderr=PIPE)
    y = Popen(['caget', 'ME14E-MO-CHIP-01:Y.RBV'], stdout=PIPE , stderr=PIPE)
    z = Popen(['caget', 'ME14E-MO-CHIP-01:Z.RBV'], stdout=PIPE , stderr=PIPE)
    x_stdout, x_stderr = x.communicate() 
    y_stdout, x_stderr = y.communicate() 
    z_stdout, x_stderr = z.communicate() 
    print x_stdout, y_stdout, z_stdout
    split_x = x_stdout.split()
    split_y = y_stdout.split()
    split_z = z_stdout.split()
    f = open('/dls_sw/work/R3.14.12.3/ioc/ME14E/ME14E-MO-IOC-01/ME14E-MO-IOC-01App/scripts/fiducial_%s.txt' %point,'w')
    f.write('%s\n' %split_x[1])
    f.write('%s\n' %split_y[1])
    f.write('%s\n' %split_z[1])
    f.close() 
    return 0
     
def run(prog_name, run_method):
    print prog_name, run_method
    if run_method == "fiducial_1":
        k = fiducial(1)

    if run_method == "fiducial_2":
        k = fiducial(2)

    if run_method == "make_cs":
        fiducial_dict = {}
        fiducial_dict['f1'] = {}
        fiducial_dict['f2'] = {}

        fiducial_dict['f1']['x'] = 18.975 
        fiducial_dict['f1']['y'] = 0 
        fiducial_dict['f1']['z'] = 0 

        fiducial_dict['f2']['x'] = 0 
        fiducial_dict['f2']['y'] = 21.375
        fiducial_dict['f2']['z'] = 0 
        
        print fiducial_dict

        k = CoordinateSystem(fiducial_dict)

    print 'done'

if  __name__ == '__main__':
    assert len(sys.argv) == 2, "Expecting an Argument [fiducial_1, fiducial_2, make_cs]"
    run(sys.argv[0], sys.argv[1])
