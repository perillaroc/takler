#!/bin/ksh
# @ job_type = serial
# @ output = ./out/m4dvar.out
# @ error = ./out/m4dvar.err
# @ notification = error
# @ checkpoint = no
# @ restart = no
# @ comment = GRAPES
# @ class= normal
# @ queue

set -x
set -e
set -u

date

######################
# directory param
######################
BASE_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso
BASE_SOURCE_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4

BASE_RUN_DIR=${BASE_DIR}/run
AN_RUN_DIR=${BASE_RUN_DIR}/an
SI_RUN_DIR=${BASE_RUN_DIR}/si
OBS_RUN_DIR=${BASE_RUN_DIR}/obs
FCST_RUN_DIR=${BASE_RUN_DIR}/fcst
RUN_DIR=${AN_RUN_DIR}/mdvar_proc

CONDAT_DIR=${BASE_DIR}/condat
AN_CONDAT_DIR=${CONDAT_DIR}/an

MDVAR_BIN=${BASE_SOURCE_DIR}/fcst/modelvar_proc/mdvar.exe
NEWDATE_BIN=${BASE_SOURCE_DIR}/fcst/grapes_model/run/newdate
############
# parameter
############

YYYYMMDDHH=2014061012
mfcast_len=24
do_static=.true.
do_3dv=.true.

output_inteval=3                 #model output inteval in hour
model_dt=90                      #model time step in second
make_surface_t=.false.

begintime=$YYYYMMDDHH
endtime=$( ${NEWDATE_BIN} $begintime +$mfcast_len)
step_max=`expr $mfcast_len \* 3600 \/ $model_dt`
step_output=`expr $output_inteval \* 3600 \/ $model_dt`

YYYY1=`echo $begintime | cut -c1-4`
MM1=`echo $begintime | cut -c5-6`
DD1=`echo $begintime | cut -c7-8`
HH1=`echo $begintime | cut -c9-10`

YYYY2=`echo $endtime | cut -c1-4`
MM2=`echo $endtime | cut -c5-6`
DD2=`echo $endtime | cut -c7-8`
HH2=`echo $endtime | cut -c9-10`


#####################
# enter work space
#####################
test -d ${RUN_DIR} || mkdir -p ${RUN_DIR}
cd ${RUN_DIR}

rm -f grapesinput
rm -f grapesbdy_old

#############
# prepare data
#############

cp ${AN_RUN_DIR}/output/grapesinput-4dv-${begintime} grapesinput${begintime}
cp ${SI_RUN_DIR}/grapesbdy grapesbdy_old

########################
# generate namelist
###########################

generate_namelist_mdvar(){
test -f namelist_mdvar || rm -r namelist_mdvar
cat > namelist_mdvar <<EOF
 &namelist_01
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
   start_year = $1,
   start_month = $2,
   start_day = $3,
   start_hour = $4,
   end_year = $5,
   end_month = $6,
   end_day = $7,
   end_hour = $8,
   interval_seconds = 10800 /

 &namelist_03
   num_soil_layers = 4,
   spec_bdy_width = 5 /
EOF
}

generate_namelist_mdvar $YYYY1 $MM1 $DD1 $HH1 $YYYY2 $MM2 $DD2 $HH2

###############
# run program
##############
${MDVAR_BIN}

#############
# post
#############
sleep 10
test -d ${FCST_RUN_DIR} || mkdir -p ${FCST_RUN_DIR}
cp grapesbdy_new ${FCST_RUN_DIR}/grapesbdy
cp grapesinput${begintime} ${FCST_RUN_DIR}/grapesinput

#############
# END
##############
date
