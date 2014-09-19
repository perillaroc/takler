#!/bin/env python
# @ comment = GRAPES
# @ job_type = serial
# @ input = /dev/null
# @ output = ./out/obs_proc.out
# @ error = ./out/obs_proc.err
# @ initialdir = ./
# @ class = normal
# @ notification = complete
# @ checkpoint = no
# @ restart = no
# @ queue

# ###############
# head
# ###############

import os
import sys
import subprocess
import shutil
from datetime import datetime, timedelta
import time

print datetime.now()

sys.path.append('../../include')
import configure

###############
#	param
###############
obs_data_dir = configure.OBS_DATA_DIR
run_dir = configure.OBS_RUN_DIR

obs_proc_bin = configure.OBS_PROC_BIN

begintime = configure.BEGINTIME


###################
# enter workspace
###################

if not os.path.isdir(run_dir):
    os.makedirs(run_dir)
os.chdir(run_dir)

os.system("rm -f  " + run_dir + "/*")

######################
# namelist.obsproc
######################
namelist_obsproc_str = """&record1
! for hlafs area but have 1 more grid at both x & y direction
 tkminlat= 15.0,
 tkmaxlat= 64.5,
 tkminlon= 70.0,
 tkmaxlon= 145.0 /

&record2 
 unit_in_buffs = 50,
! file_buffs = '{obs_data_dir}/aob{begintime}n.dat' /
 file_buffs = '{obs_data_dir}/aob{begintime}.dat' /

&record3 
 unit_out_obs = 60,
 file_out = '{run_dir}/',
 file_obs_num = '{run_dir}/obs_num{begintime}' /

&record4
 opt_checkwrite = 0,
 opt_wndwrite = 0,
 opt_msswrite = 0 /

&record5
  AirepTopP=150.,
  AirepLowP=925.,
  SoundRhTop=100.,
  RhMin=5. /
""".format(obs_data_dir=obs_data_dir, begintime=begintime, run_dir=run_dir)

with open('namelist.obsproc', 'w') as namelist_file:
    namelist_file.write(namelist_obsproc_str)


################
# ObsProc.exe
################
print "Start to excute {0}".format(obs_proc_bin)
subprocess.check_call(obs_proc_bin)
print "Done"
#time.sleep(10)
#################
# rename outputs
#################
print "rename outputs...",
shutil.copyfile("TEMP", "TEMP" + begintime + "00")
shutil.copyfile("SYNOP", "SYNOP" + begintime + "00")
shutil.copyfile("SHIPS", "SHIPS" + begintime + "00")
shutil.copyfile("AIREP", "AIREP" + begintime + "00")
print "Done"
#################
# clean up
#################

################
# tail
################
print datetime.now()
