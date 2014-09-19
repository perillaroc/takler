#!/bin/ksh
# @ job_type = parallel
# @ comment = GRAPES
# @ input = /dev/null
# @ output = ./out/4dvar_$(jobid).out
# @ error = ./out/4dvar_$(jobid).err 
# @ initialdir = ./
# @ notification = complete
# @ checkpoint = no
# @ node = 1
# @ tasks_per_node = 32
# @ class = normal
## @ class = smalljob
## @ class = minijob
## @ wall_clock_limit=10800
# @ job_name = GRAPES
# @ network.MPI = sn_all,,US
# @ queue


## must be set equal to (CPUs-per-node / tasks_per_node)
export OMP_NUM_THREADS=1

## suggestion from Jim Edwards to reintroduce XLSMPOPTS on 11/13/03
export XLSMPOPTS="stack=256000000"
export AIXTHREAD_SCOPE=S
export MALLOCMULTIHEAP=TRUE
export OMP_DYNAMIC=FALSE

## Do our best to get sufficient stack memory
ulimit -s unlimited
ulimit -c unlimited

set -x
set -e
set -u


###############
# directory
###############
BASE_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso
BASE_SOURCE_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4
RUN_DIR=${BASE_DIR}/run/an
#RUN_DIR=${BASE_SOURCE_DIR}/4dvar/m4dv/rundir

CONDAT_DIR=${BASE_DIR}/condat

M4DVAR_BIN=${BASE_SOURCE_DIR}/4dvar/m4dv/rundir/4dvar.exe

##########################
# enter work directory
##########################
test -d ${RUN_DIR} || mkdir -p ${RUN_DIR}
cd ${RUN_DIR}

###############
# Prepare data
###############
rm -f rsl*

# *.dat
test -f Eigenchi.dat || cp ${CONDAT_DIR}/an/Eigenchi.dat .
test -f Eigenhum.dat || cp ${CONDAT_DIR}/an/Eigenhum.dat .
test -f Eigenmss.dat || cp ${CONDAT_DIR}/an/Eigenmss.dat .
test -f Eigenpsi.dat || cp ${CONDAT_DIR}/an/Eigenpsi.dat .


###############
# run
################

${M4DVAR_BIN}
