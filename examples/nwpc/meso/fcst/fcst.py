#!/bin/env python
# @ comment = GRAPES
# @ job_type = parallel
# @ input = /dev/null
# @ output = ./out/fcst_$(jobid).out
# @ error =  ./out/fcst_$(jobid).err
# @ initialdir =./ 
# @ environment = COPY_ALL;PYTHONUNBUFFERED=1
# @ notification = error
# @ checkpoint = no
# @ node = 8
# @ tasks_per_node = 32
# # @ wall_clock_limit = 4800
# # @ class = benchmark
## @ class = normald
## @ class = smalljob
# @ class = normal
## @ class = middlejob
## @ class = largemem
# @ network.MPI = sn_single,,US
# @ queue

import os
import sys
from datetime import datetime, timedelta
import shutil
import subprocess

os.environ['MP_EAGER_LIMIT'] = '32000'
os.environ['MP_INFOLEVEL'] = '2'
os.environ['MP_BUFFER_MEM'] = '64M'
os.environ['XLSMPOPTS'] = "parthds=1:spins=0:yields=0:schedule=affinity:stack=50000000"
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['AIXTHREAD_MNRATIO'] = '1:1'
os.environ['SPINLOOPTIME'] = '500'
os.environ['YIELDLOOPTIME'] = '500'
os.environ['OMP_DYNAMIC'] = 'FALSE,AIX_THREAD_SCOPE=S,MALLOCMULTIHEAP=TRUE'

print datetime.now()

sys.path.append('../include')
import configure

######################
# directory setting
######################
run_dir = configure.FCST_RUN_DIR
an_run_dir = configure.AN_RUN_DIR
si_run_dir = configure.SI_RUN_DIR
base_condat_dir = configure.BASE_CONDAT_DIR

grapes_bin = configure.GRAPES_BIN

############
# parameter
############
begintime = configure.BEGINTIME

#####################
# enter work space
#####################
if not os.path.isdir(run_dir):
    os.makedirs(run_dir)

os.chdir(run_dir)

#####################
# prepare data
#####################

# tbl data
print "copy tbl data...",
if not os.path.isfile("GENPARM.TBL"):
    shutil.copy(base_condat_dir + "/fcst/GENPARM.TBL", "GENPARM.TBL")

if not os.path.isfile("GEOGRID.TBL"):
    shutil.copy(base_condat_dir + "/fcst/GEOGRID.TBL", "GEOGRID.TBL")

if not os.path.isfile("LANDUSE.TBL"):
    shutil.copy(base_condat_dir + "/fcst/LANDUSE.TBL", "LANDUSE.TBL")

if not os.path.isfile("SOILPARM.TBL"):
    shutil.copy(base_condat_dir + "/fcst/SOILPARM.TBL", "SOILPARM.TBL")

if not os.path.isfile("VEGPARM.TBL"):
    shutil.copy(base_condat_dir + "/fcst/VEGPARM.TBL", "VEGPARM.TBL")

if not os.path.isfile("RRTM_DATA"):
    shutil.copy(base_condat_dir + "/fcst/RRTM_DATA", "RRTM_DATA")
print "Done"

# grapesinput grapesbdy
print "copy grapesbdy and grapesinput...",
###  TEMP don't use an
#shutil.copyfile('{si_run_dir}/grapesinput'.format(si_run_dir = si_run_dir), 'grapesinput')
#shutil.copyfile('{si_run_dir}/grapesbdy'.format(si_run_dir = si_run_dir), 'grapesbdy')

shutil.copyfile(an_run_dir + '/mdvar_proc/grapesbdy_new', 'grapesbdy')
shutil.copyfile('{an_run_dir}/mdvar_proc/grapesinput{begintime}'.format(
    an_run_dir=an_run_dir,
    begintime=begintime
), 'grapesinput')

if not os.path.isfile("grapesbdy"):
    print "Failed"
    sys.exit(1)

if not os.path.isfile("grapesinput"):
    print "Failed"
    sys.exit(1)

print "Done"

###########
# namelist.input
###########

print "copy namelist.input from si module...",
if os.path.isfile('namelist.input'):
    os.remove('namelist.input')
shutil.copy(si_run_dir + "/namelist.input", "namelist.input")
print "Done"

#####################
# run program
#####################
print "start grapes_bin..."
subprocess.check_call(grapes_bin)
print "DONE"

######################
# END
######################
print datetime.now()

