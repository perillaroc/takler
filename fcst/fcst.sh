#!/bin/ksh
# @ comment = GRAPES
# @ job_type = parallel
# @ input = /dev/null
# @ output = ./out/fcst_$(jobid).out
# @ error =  ./out/fcst_$(jobid).err
# @ initialdir =./ 
# @ notification = error
# @ checkpoint = no
# @ node = 8
# @ tasks_per_node = 32
## @ wall_clock_limit = 4800
## @ class = benchmark
## @ class = normald
## @ class = smalljob
# @ class = normal
## @ class = middlejob
## @ class = largemem
# @ network.MPI = sn_single,,US
# @ queue

export MP_EAGER_LIMIT=32000
export MP_INFOLEVEL=2
export MP_BUFFER_MEM=64M
export XLSMPOPTS="parthds=1:spins=0:yields=0:schedule=affinity:stack=50000000"
export OMP_NUM_THREADS=1
export AIXTHREAD_MNRATIO=1:1
export SPINLOOPTIME=500
export YIELDLOOPTIME=500
export OMP_DYNAMIC=FALSE,AIX_THREAD_SCOPE=S,MALLOCMULTIHEAP=TRUE

set -x
set -u
set -e

date

######################
# directory setting
######################

BASE_RUN_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso/run
RUN_DIR=${BASE_RUN_DIR}/fcst
AN_RUN_DIR=${BASE_RUN_DIR}/an
SI_RUN_DIR=${BASE_RUN_DIR}/si

CONDAT_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso/condat

GRAPES_BIN=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4/fcst/grapes_model/run/grapes.exe


#####################
# enter work space
#####################
test -d ${RUN_DIR} || mkdir -p ${RUN_DIR}
cd ${RUN_DIR}

#####################
# prepare data
#####################


# tbl data
test -f GENPARM.TBL || cp ${CONDAT_DIR}/fcst/GENPARM.TBL .
test -f GEOGRID.TBL || cp ${CONDAT_DIR}/fcst/GEOGRID.TBL .
test -f LANDUSE.TBL || cp ${CONDAT_DIR}/fcst/LANDUSE.TBL .
test -f SOILPARM.TBL || cp ${CONDAT_DIR}/fcst/SOILPARM.TBL .
test -f VEGPARM.TBL || cp ${CONDAT_DIR}/fcst/VEGPARM.TBL .
test -f RRTM_DATA || cp ${CONDAT_DIR}/fcst/RRTM_DATA .

###  TEMP don't use an
#cp -r ${SI_RUN_DIR}/grapesinput .
#cp -r ${SI_RUN_DIR}/grapesbdy .

test -f grapesbdy || exit 1
test -f grapesinput || exit 1

###########
# namelist.input
###########

test -f namelist.input || rm -f namelist.input
cp ${SI_RUN_DIR}/namelist.input .

#####################
# run program
#####################
${GRAPES_BIN}

######################
# END
######################
date

