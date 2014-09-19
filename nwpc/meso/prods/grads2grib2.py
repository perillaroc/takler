#!/bin/env python
# @ comment = GRAPES
# @ job_type = serial
# @ input = /dev/null
# @ output = ./out/grads2grib2_$(jobid).out
# @ error =  ./out/grads2grib2_$(jobid).err
# @ initialdir =./ 
# @ environment = COPY_ALL;PYTHONUNBUFFERED=1
# @ notification = error
# @ checkpoint = no
# @ class = normal
# @ queue

# ############################
# grads to grib2 orgin
#############################

import os
import sys
from datetime import datetime, timedelta
import shutil
import subprocess

print datetime.now()

sys.path.append('../include')
import configure

######################
# directory setting
######################
prods_condat_dir = configure.PRODS_CONDAT_DIR

run_dir = configure.PRODS_RUN_DIR
post_run_dir = configure.POST_RUN_DIR
fcst_run_dir = configure.FCST_RUN_DIR

grads2grib_bin = configure.GRADS2GRIB_BIN_DIR

############
# parameter
############

# common parameter

begin_date_time = configure.BEGIN_DATE_TIME

mfcast_len = configure.MFCAST_LEN

output_inteval = configure.OUTPUT_INTEVAL  #model output inteval in hour

begintime = configure.BEGINTIME

levels = configure.LEVELS

model_name = 'GRAPES_MESO2GRIB2_ORIG'

#file params

forecast_list = range(0, mfcast_len + output_inteval, output_inteval)
forecast_list_str = ["%03d" % one_forecast_hour for one_forecast_hour in forecast_list]
current_forecast_hour_index = 0;
current_forcast_hour = forecast_list_str[current_forecast_hour_index]

cur_time_str = begintime + current_forcast_hour + '00'

init_time = begintime
start_time = begin_date_time + timedelta(hours=forecast_list[current_forecast_hour_index])
end_time = start_time

#####################
# enter work space
#####################
work_space_dir = "{run_dir}/grib2_orig/{current_forcast_hour}".format(
    run_dir=run_dir,
    current_forcast_hour=current_forcast_hour)

if not os.path.isdir(work_space_dir):
    os.makedirs(work_space_dir)
os.chdir(work_space_dir)

#####################
# prepare data
#####################
file_name = 'postvar{cur_time_str}'.format(cur_time_str=cur_time_str)
if os.path.islink(file_name):
    os.remove(file_name)
os.symlink('{fcst_run_dir}/{file_name}'.format(fcst_run_dir=fcst_run_dir, file_name=file_name),
           file_name)

ctl_file_name = 'post.ctl_${cur_time_str}'.format(cur_time_str=cur_time_str)
if os.path.islink(ctl_file_name):
    os.remove(ctl_file_name)
os.symlink('{fcst_run_dir}/{ctl_file_name}'.format(fcst_run_dir=fcst_run_dir, ctl_file_name=ctl_file_name),
           ctl_file_name)

shutil.copyfile('{prods_condat_dir}/grib/cma.grib2'.format(prods_condat_dir=prods_condat_dir),
                'cma.grib2')
shutil.copyfile('{prods_condat_dir}/grib/grib_para_file.base.orig.grib2'.format(prods_condat_dir=prods_condat_dir),
                'grib_para_file')


###########
# namelist.input
###########

namelist_input_str = """&input_file
grads_ctl  = "./{ctl_file_name}"
/
&model_parameter
model_name          = "{model_name}"
init_time           = "{init_time}"
start_time          = "{start_time}"
end_time            = "{end_time}"
/
&grads_parameter
grads_map_type      = 0      ! 0:lon-lat map(GRAPES,AREM)   1:lambert map(MM5,WRF)
nx_grads            = 502    ! east-west direction
ny_grads            = 330    ! south-north direction
nz_grads            = 1
dx_grads            = 0.15
dy_grads            = 0.15
slon_grads          = 70.0
elon_grads          = 145.15
slat_grads          = 15.0
elat_grads          = 64.35
!
corner_lon_grads    = 120.0
corner_lat_grads    = 42.0
corner_i_grads      = 40
corner_j_grads      = 35
STD_LON_grads       = 120.0      !the same as corner_lon
TRUE_LAT1_grads     = 30.0,
TRUE_LAT2_grads     = 60.0
MAP_DX_grads        = 15000.
MAP_DY_grads        = 15000.
/
&grib_parameter1
grib_map_type       = 0
nx_grib             = 502
ny_grib             = 330
dx_grib             = 0.15
dy_grib             = -0.15
slon_grib           = 70.0
elon_grib           = 145.15
slat_grib           = 64.35
elat_grib           = 15.0
!
corner_lon_grib     = 120.0
corner_lat_grib     = 42.0
corner_i_grib       = 40
corner_j_grib       = 35
STD_LON_grib        = 120.0      !the same as corner_lon
TRUE_LAT1_grib      = 30.0,
TRUE_LAT2_grib      = 60.0
MAP_DX_grib         = 15000.
MAP_DY_grib         = 15000.
/
&grib_parameter2
grib_type           = 2    ! 1: grib1,    2: grib2,    12: grib1 and grib2
grib_para_file      = "./grib_para_file"
dt_grib             = 9999  ! 9999: only 1 time level, others: normal value
file_status         = 0     ! 0: create a new file,  1: append an old file
quality_control     = 0     ! 0: NO,  1: YES
/
""".format(
    ctl_file_name=ctl_file_name,
    model_name=model_name,
    init_time=init_time,
    start_time=start_time,
    end_time=end_time
)

#####################
# run program
#####################
subprocess.check_call(grads2grib_bin, shell=True)

######################
# END
######################
print datetime.now()


