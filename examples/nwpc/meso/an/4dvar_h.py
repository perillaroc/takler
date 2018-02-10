#!/bin/env python
# @ job_type = parallel
# @ comment = GRAPES
# @ input = /dev/null
# @ output = ./out/4dvar_h_$(jobid).out
# @ error = ./out/4dvar_h_$(jobid).err 
# @ initialdir = ./
# @ notification = complete
# @ checkpoint = no
# @ node = 1
# @ tasks_per_node = 32
# @ comment = GRAPES
# @ class = normal
# # @ class = smalljob
# # @ class = minijob
## @ wall_clock_limit=10800
# @ job_name = GRAPES
# @ network.MPI = sn_all,,US
# @ queue

import os;
import sys;
from datetime import datetime
import shutil
import glob
import subprocess

## must be set equal to (CPUs-per-node / tasks_per_node)
os.environ['OMP_NUM_THREADS'] = '1'

## suggestion from Jim Edwards to reintroduce XLSMPOPTS on 11/13/03
os.environ['XLSMPOPTS'] = "stack=256000000"
os.environ['AIXTHREAD_SCOPE'] = 'S'
os.environ['MALLOCMULTIHEAP'] = 'TRUE'
os.environ['OMP_DYNAMIC'] = 'FALSE'

print datetime.now()

sys.path.append('../include')
import configure

###############
# directory
###############
run_dir = configure.AN_RUN_DIR

obs_run_dir = configure.OBS_RUN_DIR
an_condat_dir = configure.AN_CONDAT_DIR
fcst_condat_dir = configure.FCST_CONDAT_DIR

si_run_dir = configure.SI_RUN_DIR

m4dvar_h_bin = configure.M4DVAR_H_BIN

##########################
# enter work directory
##########################
if not os.path.isdir(run_dir):
    os.makedirs(run_dir)

os.chdir(run_dir)

shutil.copyfile(si_run_dir + '/grapesinput', 'grapesinput')

###############
# Prepare data
###############
rsl_file_names = glob.glob("rsl*")
for rsl_file_name in rsl_file_names:
    os.remove(rsl_file_name)

# OBS GTS
if os.path.islink(run_dir + '/input/GTS'):
    os.remove(run_dir + '/input/GTS')
os.symlink(obs_run_dir, run_dir + '/input/GTS')

# rmsdate
if os.path.islink(run_dir + '/input/rmsdata'):
    os.remove(run_dir + '/input/rmsdata')
os.symlink(an_condat_dir + '/input/rmsdata', run_dir + '/input/rmsdata')

# tbl data

if not os.path.exists('GENPARM.TBL'):
    shutil.copyfile(fcst_condat_dir + '/GENPARM.TBL', 'GENPARM.TBL')

if not os.path.exists('GEOGRID.TBL'):
    shutil.copyfile(fcst_condat_dir + '/GEOGRID.TBL', 'GEOGRID.TBL')

if not os.path.exists('LANDUSE.TBL'):
    shutil.copyfile(fcst_condat_dir + '/LANDUSE.TBL', 'LANDUSE.TBL')

if not os.path.exists('SOILPARM.TBL'):
    shutil.copyfile(fcst_condat_dir + '/SOILPARM.TBL', 'SOILPARM.TBL')

if not os.path.exists('VEGPARM.TBL'):
    shutil.copyfile(fcst_condat_dir + '/VEGPARM.TBL', 'VEGPARM.TBL')

if not os.path.exists('RRTM_DATA.TBL'):
    shutil.copyfile(fcst_condat_dir + '/RRTM_DATA', 'RRTM_DATA')

###############
# run
################
subprocess.check_call(m4dvar_h_bin, shell=True)

print datetime.now()

