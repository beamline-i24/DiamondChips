#!/bin/sh

#Zeros the stages and sets readbacks to zero

caput ME14E-MO-CHIP-01:PMAC_STRING \#1hmz\#2hmz\#3hmz
sleep 0.5
caput ME14E-MO-CHIP-01:X 0
caput ME14E-MO-CHIP-01:Y 0
caput ME14E-MO-CHIP-01:Z 0
