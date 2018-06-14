from ca import caput, caget
import time
from time import sleep

start = time.time()
print 'please wait'
for i in range(320):
    caput('ME14E-MO-CHIP-01:PMAC_STRING','ver')

finish = time.time()
print finish-start
