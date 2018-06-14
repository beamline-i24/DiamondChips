#!/bin/usr/python
from subprocess import Popen, PIPE

def caget(pv):
    val = None
    while val is None:
        try:  
            a = Popen(['caget', pv], stdout=PIPE, stderr=PIPE) 
            a_stdout, a_stderr = a.communicate()
            val = a_stdout.split()[1]
            val = evaluate(val)
        except:
            print 'Exception in ca-cagt'
            pass
    return val

def caput(pv, new_val):
    check = Popen(['cainfo', pv], stdout=PIPE, stderr=PIPE)
    check_stdout, check_stderr = check.communicate()
    if check_stdout.split()[11] == 'DBF_CHAR':
        a = Popen(['caput', '-S', pv, str(new_val)], stdout=PIPE, stderr=PIPE) 
        a_stdout, a_stderr = a.communicate()
    else: 
        a = Popen(['caput', pv, str(new_val)], stdout=PIPE, stderr=PIPE) 
        a_stdout, a_stderr = a.communicate()

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
