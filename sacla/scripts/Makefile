TOP = ../..
include $(TOP)/configure/CONFIG

DATA += $(patsubst ../%, %, $(wildcard ../*.py))
DATA += $(patsubst ../%, %, $(wildcard ../*.sh))
DATA += $(patsubst ../%, %, $(wildcard ../*.txt))

include $(TOP)/configure/RULES
