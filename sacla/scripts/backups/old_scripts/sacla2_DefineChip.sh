#!/bin/sh
python /dls_sw/work/R3.14.12.3/ioc/ME14E/ME14E-MO-IOC-01/ME14E-MO-IOC-01App/scripts/sacla2_Chip_Manager1.py write_parameter_file
python /dls_sw/work/R3.14.12.3/ioc/ME14E/ME14E-MO-IOC-01/ME14E-MO-IOC-01App/scripts/sacla2_Chip_StartUp1.py
echo 'All Done. Ready for data collection'
