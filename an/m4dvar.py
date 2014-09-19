#!/bin/env python
# @ job_type = serial
# @ output = ./out/m4dvar.out
# @ error = ./out/m4dvar.err
# @ initialdir = ./
# @ environment = COPY_ALL;PYTHONUNBUFFERED=1
# @ notification = error
# @ checkpoint = no
# @ restart = no
# @ comment = GRAPES
# @ class= normal
# @ queue

import os;
import sys;
from datetime import datetime, timedelta
import shutil
import glob
import subprocess

print datetime.now()

sys.path.append('../include')
import configure

# #####################
# directory param
# #####################
an_run_dir = configure.AN_RUN_DIR
si_run_dir = configure.SI_RUN_DIR

run_dir = an_run_dir + '/mdvar_proc'

mdvar_bin = configure.MDVAR_BIN
############
# parameter
############

begintime = configure.BEGINTIME

yyyy1 = configure.YYYY1
mm1 = configure.MM1
dd1 = configure.DD1
hh1 = configure.HH1

yyyy2 = configure.YYYY2
mm2 = configure.MM2
dd2 = configure.DD2
hh2 = configure.HH2


#####################
# enter work space
#####################
if not os.path.isdir(run_dir):
    os.makedirs(run_dir)
os.chdir(run_dir)

if os.path.isfile('grapesinput'):
    os.remove('grapesinput')

if os.path.isfile('grapesbdy_old'):
    os.remove('grapesbdy_old')

#############
# prepare data
#############
shutil.copyfile(an_run_dir + '/output/grapesinput-4dv-' + begintime,
                'grapesinput' + begintime)
shutil.copyfile(si_run_dir + '/grapesbdy', 'grapesbdy_old')

###########################
# generate namelist
###########################
if os.path.isfile('namelist_mdvar'):
    os.remove('namelist_mdvar')

namelist_mdvar_str = """ &namelist_01
   s_we = 1,
   e_we = 502,
   s_sn = 1,
   e_sn = 330,
   s_vert = 1,
   e_vert = 31,
   xs_we = 70.,
   ys_sn = 15.,
   xd = 0.15,
   yd = 0.15      /

&namelist_02
   start_year = {yyyy1},
   start_month = {mm1},
   start_day = {dd1},
   start_hour = {hh1},
   end_year = {yyyy2},
   end_month = {mm2},
   end_day = {dd2},
   end_hour = {hh2},
   interval_seconds = 10800 /

 &namelist_03
   num_soil_layers = 4,
   spec_bdy_width = 5 /
EOF""".format(
    yyyy1=yyyy1,
    mm1=mm1,
    dd1=dd1,
    hh1=hh1,
    yyyy2=yyyy2,
    mm2=mm2,
    dd2=dd2,
    hh2=hh2,
)

with open('namelist_mdvar', 'w') as f:
    f.write(namelist_mdvar_str)

###############
# run program
##############
print "start MDVAR...",
subprocess.check_call(mdvar_bin)
print "Done"

#############
# post
#############


#############
# END
##############
print datetime.now()
