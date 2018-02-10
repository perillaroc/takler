#!/bin/ksh
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
BASE_RUN_DIR=${BASE_DIR}/run
RUN_DIR=${BASE_DIR}/run/an
#RUN_DIR=${BASE_SOURCE_DIR}/4dvar/m4dv/rundir

OBS_DIR=${BASE_DIR}/run/obs
CONDAT_DIR=${BASE_DIR}/condat
AN_CONDAT_DIR=${CONDAT_DIR}/an

SI_RUN_DIR=${BASE_RUN_DIR}/si

M4DVAR_H_BIN=${BASE_SOURCE_DIR}/4dvar/m4dv/rundir/4dvar_h.exe

##########################
# enter work directory
##########################
test -d ${RUN_DIR} || mkdir -p ${RUN_DIR}
cd ${RUN_DIR}

cp -f ${SI_RUN_DIR}/grapesinput .

###############
# Prepare data
###############
rm -f rsl*

# OBS GTS
ln -sf ${OBS_DIR} ${RUN_DIR}/input/GTS

# rmsdate
ln -sf ${AN_CONDAT_DIR}/input/rmsdata ${RUN_DIR}/input/rmsdata

# tbl data
test -f GENPARM.TBL || cp ${CONDAT_DIR}/fcst/GENPARM.TBL .
test -f GEOGRID.TBL || cp ${CONDAT_DIR}/fcst/GEOGRID.TBL .
test -f LANDUSE.TBL || cp ${CONDAT_DIR}/fcst/LANDUSE.TBL .
test -f SOILPARM.TBL || cp ${CONDAT_DIR}/fcst/SOILPARM.TBL .
test -f VEGPARM.TBL || cp ${CONDAT_DIR}/fcst/VEGPARM.TBL .
test -f RRTM_DATA || cp ${CONDAT_DIR}/fcst/RRTM_DATA .

###############
# run
################

${M4DVAR_H_BIN}
