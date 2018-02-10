#!/bin/env python
# @ comment = GRAPES
# @ job_type = serial
# @ input = /dev/null
# @ output = ./out/post_$(jobid).out
# @ error =  ./out/post_$(jobid).err
# @ initialdir =./ 
# @ environment = COPY_ALL;PYTHONUNBUFFERED=1
# @ notification = error
# @ checkpoint = no
# @ class = normal
# @ queue

import os
import sys
from datetime import datetime, timedelta
import shutil
import subprocess

print datetime.now()

sys.path.append('../include')
import configure

# #####################
# directory setting
# #####################
run_dir = configure.POST_RUN_DIR
fcst_run_dir = configure.FCST_RUN_DIR

product_bin = configure.PRODUCT_BIN

############
# parameter
############

# common parameter

begintime = configure.BEGINTIME

mfcast_len = configure.MFCAST_LEN

output_inteval = configure.OUTPUT_INTEVAL

levels = configure.LEVELS

#file params

forecast_list = range(0, mfcast_len + output_inteval, output_inteval)
forecast_list_str = ["%03d" % one_forecast_hour for one_forecast_hour in forecast_list]

current_forcast_time = forecast_list_str[0]

cur_time_str = begintime + current_forcast_time + '00'

#####################
# enter work space
#####################
curernt_work_space_dir = '{run_dir}/{current_forcast_time}' \
    .format(run_dir=run_dir, current_forcast_time=current_forcast_time)
if not os.path.isdir(curernt_work_space_dir):
    os.makedirs(curernt_work_space_dir)
os.chdir(curernt_work_space_dir)

#####################
# prepare data
#####################
post_var_file_name = 'postvar{cur_time_str}'.format(cur_time_str=cur_time_str)
if os.path.islink(post_var_file_name):
    os.remove(post_var_file_name)
os.symlink(fcst_run_dir + '/' + post_var_file_name, post_var_file_name)

post_ctl_file_name = 'post.ctl_{cur_time_str}'.format(cur_time_str=cur_time_str)
if os.path.islink(post_ctl_file_name):
    os.remove(post_ctl_file_name)
os.symlink(fcst_run_dir + '/' + post_ctl_file_name, post_ctl_file_name)

###########
# namelist.input
###########

if os.path.isfile('namelist.input'):
    os.remove('namelist.input')
namelist_input_str = str()
if levels is 17:
    namelist_input_str = """&ctl_file
path                =    "."
grads_ctl           =    "post.ctl_{cur_time_str}"
ctl_flag            =    "meso" ! (global,meso,ruc)
/
&choose_output
vor_div_c           =    true    !global,meso,ruc
rh_c                =    true    !global,meso,ruc
t_td_c              =    true    !global,meso,ruc
t_adv_vor_adv_c     =    false    !global
q_flux_div_c        =    true    !global,meso,ruc
thetase_c           =    true    !global,meso,ruc
ki_c                =    true    !global,meso,ruc
t24_c               =    false   !meso
h24_c               =    false   !meso
p24_c               =    false   !meso
h500_c              =    false   !meso
rain_c              =    false   !meso
rain3_c             =    false   !meso
rain6_c             =    false   !meso
rain12_c            =    false   !meso
rain24_c            =    false   !meso
speed_c             =    true    !global,meso,ruc
cal_smooth_c        =    false   !global,meso,ruc
CALCAPE_c           =    true    !global,meso,ruc
calq2m_rh2m_c       =    true    !meso,ruc
calrh2td2m_c        =    false   !meso,ruc
post2dbz_c          =    false   !global,meso,ruc
cal_dttase_c        =    false   !global,meso,ruc
cal_sweat_c         =    true    !global,meso,ruc
cal_srh_c           =    false   !global,meso,ruc
cal_tempadv_c       =    false   !meso,ruc
cal_shr_c           =    false   !global,meso,ruc
cal_PcTcLiLfc_c     =    true    !meso,ruc
cal_bli_c           =    true    !global,meso,ruc
ilc_c               =    true    !global,meso,ruc
/
&grib_parameter1
vsel1               =   1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 0, 0, 0
vsel2               =   1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 0, 0, 0
vsel3               =   1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 0, 0, 0
vsel4               =   1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 0, 0, 0
/
&grib_parameter2
dpbnd               =   300.E2
itype               =   1
/
""".format(cur_time_str=cur_time_str)

elif levels is 26:
    namelist_input_str = """&ctl_file
path                =    "."
grads_ctl           =    "post.ctl_{cur_time_str}"
ctl_flag            =    "meso" ! (global,meso,ruc)
/
&choose_output
vor_div_c           =    true    !global,meso,ruc
rh_c                =    true    !global,meso,ruc
t_td_c              =    true    !global,meso,ruc
t_adv_vor_adv_c     =    false    !global
q_flux_div_c        =    true    !global,meso,ruc
thetase_c           =    true    !global,meso,ruc
ki_c                =    true    !global,meso,ruc
t24_c               =    false   !meso
h24_c               =    false   !meso
p24_c               =    false   !meso
h500_c              =    false   !meso
rain_c              =    false   !meso
rain3_c             =    false   !meso
rain6_c             =    false   !meso
rain12_c            =    false   !meso
rain24_c            =    false   !meso
speed_c             =    true    !global,meso,ruc
cal_smooth_c        =    true    !global,meso,ruc
CALCAPE_c           =    true    !global,meso,ruc
calq2m_rh2m_c       =    true    !meso,ruc
calrh2td2m_c        =    true    !meso,ruc
post2dbz_c          =    true    !global,meso,ruc
cal_dttase_c        =    true    !global,meso,ruc
cal_sweat_c         =    true    !global,meso,ruc
cal_srh_c           =    true    !global,meso,ruc
cal_tempadv_c       =    true    !meso,ruc
cal_shr_c           =    true    !global,meso,ruc
cal_PcTcLiLfc_c     =    true    !meso,ruc
cal_bli_c           =    true    !global,meso,ruc
ilc_c               =    true    !global,meso,ruc
/
&grib_parameter1
vsel1     =  1000,975,950,925,900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,150,100,70,50,30,20,10,0,0,0,0
vsel2     =  1000,975,950,925,900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,150,100,70,50,30,20,10,0,0,0,0
vsel3     =  1000,975,950,925,900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,150,100,70,50,30,20,10,0,0,0,0
vsel4     =  1000,975,950,925,900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,150,100,70,50,30,20,10,0,0,0,0
/
&grib_parameter2
dpbnd               =   300.E2
itype               =   1
/
""".format(cur_time_str=cur_time_str)

with open('namelist.input', 'w') as f:
    f.write(namelist_input_str);


#####################
# run program
#####################
subprocess.check_call(product_bin)

#####################
# post
#####################
diag_ctl_file_name = "diag.ctl_{cur_time_str}".format(cur_time_str=cur_time_str)
if os.path.exists(diag_ctl_file_name):
    shutil.move(diag_ctl_file_name, os.path.dirname(os.getcwd()) + "/" + diag_ctl_file_name)
else:
    print diag_ctl_file_name + ' is not exists!'

diag_file_name = 'diag_{cur_time_str}'.format(cur_time_str=cur_time_str)
if os.path.exists(diag_file_name):
    shutil.move(diag_file_name, os.path.dirname(os.getcwd()) + "/" + diag_file_name)
else:
    print diag_file_name + ' is not exists!'


######################
# END
######################
print datetime.now()