#!/bin/ksh
# @ comment = GRAPES
# @ job_type = serial
# @ input = /dev/null
# @ output = ./out/grads2grib2_$(jobid).out
# @ error =  ./out/grads2grib2_$(jobid).err
# @ initialdir =./ 
# @ notification = error
# @ checkpoint = no
# @ class = normal
# @ queue

#############################
#	grads to grib2 orgin
#############################

set -x
set -u
set -e

date

######################
# directory setting
######################
BASE_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso
BASE_SOURCE_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4
BASE_CONDAT_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso/condat
BIN_DIR=${BASE_DIR}/bin

PRODS_CONDAT_DIR=${BASE_CONDAT_DIR}/prods

BASE_RUN_DIR=${BASE_DIR}/run
RUN_DIR=${BASE_RUN_DIR}/prods
POST_RUN_DIR=${BASE_RUN_DIR}/post
AN_RUN_DIR=${BASE_RUN_DIR}/an
SI_RUN_DIR=${BASE_RUN_DIR}/si
FCST_RUN_DIR=${BASE_RUN_DIR}/fcst

GRADS2GRIB_BIN_DIR=${BIN_DIR}/grads2grib.exe

############
# parameter
############

levels=26

YYYYMMDDHH=2014061012

current_forcast_hour=000

while getopts "t:b:r:g:c:" arg
do
	case $arg in
		t)
			YYYYMMDDHH=$OPTARG
			;;
		b)
			BCKG_DIR=$OPTARG
			;;
		r)
			RUN_DIR=$OPTARG
			;;
	esac
done

model_name=GRAPES_MESO2GRIB2_ORIG
begintime=$YYYYMMDDHH
init_time=${begintime}
start_time=$( smsdate ${begintime} +${current_forcast_hour})
end_time=$start_time

cur_time_str=${begintime}${current_forcast_hour}00

#####################
# enter work space
#####################
work_space_dir=${RUN_DIR}/grib2_orig/${current_forcast_hour}
test -d ${work_space_dir} || mkdir -p ${work_space_dir}
cd ${work_space_dir}

#####################
# prepare data
#####################

ln -sf ${FCST_RUN_DIR}/postvar${cur_time_str} .
ln -sf ${FCST_RUN_DIR}/post.ctl_${cur_time_str} .
cp ${PRODS_CONDAT_DIR}/grib/cma.grib2 .
cp ${PRODS_CONDAT_DIR}/grib/grib_para_file.base.orig.grib2 grib_para_file

###########
# namelist.input
###########

ctl_file_name=post.ctl_${cur_time_str}

cat > namelist.input <<EOF
&input_file
grads_ctl  = "./${ctl_file_name}"
/
&model_parameter
model_name          = "${model_name}"
init_time           = "${init_time}"
start_time          = "${start_time}"
end_time            = "${end_time}"
/
&grads_parameter
grads_map_type      = 0      ! 0:lon-lat map(GRAPES,AREM)   1:lambert map(MM5,WRF)
nx_grads            = 502    ! east-west direction
ny_grads            = 330    ! south-north direction
nz_grads            = 1
dx_grads            = 0.15
dy_grads            = 0.15
slon_grads          = 70.0
elon_grads          = 145.15
slat_grads          = 15.0
elat_grads          = 64.35
!
corner_lon_grads    = 120.0
corner_lat_grads    = 42.0
corner_i_grads      = 40
corner_j_grads      = 35
STD_LON_grads       = 120.0      !the same as corner_lon
TRUE_LAT1_grads     = 30.0,
TRUE_LAT2_grads     = 60.0
MAP_DX_grads        = 15000.
MAP_DY_grads        = 15000.
/
&grib_parameter1
grib_map_type       = 0
nx_grib             = 502
ny_grib             = 330
dx_grib             = 0.15
dy_grib             = -0.15
slon_grib           = 70.0
elon_grib           = 145.15
slat_grib           = 64.35
elat_grib           = 15.0
!
corner_lon_grib     = 120.0
corner_lat_grib     = 42.0
corner_i_grib       = 40
corner_j_grib       = 35
STD_LON_grib        = 120.0      !the same as corner_lon
TRUE_LAT1_grib      = 30.0,
TRUE_LAT2_grib      = 60.0
MAP_DX_grib         = 15000.
MAP_DY_grib         = 15000.
/
&grib_parameter2
grib_type           = 2    ! 1: grib1,    2: grib2,    12: grib1 and grib2
grib_para_file      = "./grib_para_file"
dt_grib             = 9999  ! 9999: only 1 time level, others: normal value
file_status         = 0     ! 0: create a new file,  1: append an old file
quality_control     = 0     ! 0: NO,  1: YES
/
EOF

#####################
# run program
#####################
${GRADS2GRIB_BIN_DIR}

######################
# END
######################
date


