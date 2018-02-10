#!/bin/env python
# @ job_type = parallel
# @ comment = GRAPES
# @ input = /dev/null
# @ output = ./out/4dvar_$(jobid).out
# @ error = ./out/4dvar_$(jobid).err 
# @ initialdir = ./
# @ environment = COPY_ALL;PYTHONUNBUFFERED=1
# @ notification = complete
# @ checkpoint = no
# @ node = 1
# @ tasks_per_node = 32
# @ class = normal
# # @ class = smalljob
# # @ class = minijob
# # @ wall_clock_limit=10800
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

condat_dir = configure.BASE_CONDAT_DIR

m4dvar_bin = configure.M4DVAR_BIN

##########################
# enter work directory
##########################
if not os.path.isdir(run_dir):
    os.makedirs(run_dir)
os.chdir(run_dir)

###############
# Prepare data
###############
rsl_file_names = glob.glob("rsl*")
for rsl_file_name in rsl_file_names:
    os.remove(rsl_file_name)

# *.dat
if not os.path.exists('Eigenchi.dat'):
    shutil.copyfile(condat_dir + '/an/Eigenchi.dat', 'Eigenchi.dat')

if not os.path.exists('Eigenhum.dat'):
    shutil.copyfile(condat_dir + '/an/Eigenhum.dat', 'Eigenhum.dat')

if not os.path.exists('Eigenmss.dat'):
    shutil.copyfile(condat_dir + '/an/Eigenmss.dat', 'Eigenmss.dat')

if not os.path.exists('Eigenpsi.dat'):
    shutil.copyfile(condat_dir + '/an/Eigenpsi.dat', 'Eigenpsi.dat')


###############
# run
################

subprocess.check_call(m4dvar_bin, shell=True)

###############
# tail
###############
print datetime.now()

