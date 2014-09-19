#!/bin/ksh
# @ comment = GRAPES
# @ job_type = serial
# @ input = /dev/null
# @ output = ./out/post_$(jobid).out
# @ error =  ./out/post_$(jobid).err
# @ initialdir =./ 
# @ notification = error
# @ checkpoint = no
# @ class = normal
# @ queue

set -x
set -u
set -e

date

######################
# directory setting
######################
BASE_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso
BASE_SOURCE_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4

BASE_RUN_DIR=${BASE_DIR}/run
RUN_DIR=${BASE_RUN_DIR}/post
AN_RUN_DIR=${BASE_RUN_DIR}/an
SI_RUN_DIR=${BASE_RUN_DIR}/si
FCST_RUN_DIR=${BASE_RUN_DIR}/fcst

NEWDATE_BIN=${BASE_SOURCE_DIR}/fcst/grapes_model/run/newdate
PRODUCT_BIN=${BASE_DIR}/src/post/grapes_post_diag_ibm/product.exe

############
# parameter
############

levels=26

YYYYMMDDHH=2014061012
mfcast_len=24
do_static=.true.
do_3dv=.true.

output_inteval=3                 #model output inteval in hour
model_dt=90                      #model time step in second
make_surface_t=.false.

current_forcast_time=000

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

cur_time_str=${begintime}${current_forcast_time}00

#####################
# enter work space
#####################
test -d ${RUN_DIR}/${current_forcast_time} || mkdir -p ${RUN_DIR}/${current_forcast_time}
cd ${RUN_DIR}/${current_forcast_time}

#####################
# prepare data
#####################

ln -sf ${FCST_RUN_DIR}/postvar${cur_time_str} .
ln -sf ${FCST_RUN_DIR}/post.ctl_${cur_time_str} .

###########
# namelist.input
###########
test -f namelist.input || rm -rf namelist.input

if [ $levels -eq 17 ];then
   test -s namelist.input && rm -f namelist.input
   cat > namelist.input <<EOF
&ctl_file
path                =    "."
grads_ctl           =    "post.ctl_${cur_time_str}"
ctl_flag            =    "meso" ! (global,meso,ruc)
/
&choose_output
vor_div_c           =    true    !global,meso,ruc
rh_c                =    true    !global,meso,ruc
t_td_c              =    true    !global,meso,ruc
t_adv_vor_adv_c     =    false    !global
q_flux_div_c        =    true    !global,meso,ruc
thetase_c           =    true    !global,meso,ruc
ki_c                =    true    !global,meso,ruc
t24_c               =    false   !meso
h24_c               =    false   !meso
p24_c               =    false   !meso
h500_c              =    false   !meso
rain_c              =    false   !meso
rain3_c             =    false   !meso
rain6_c             =    false   !meso
rain12_c            =    false   !meso
rain24_c            =    false   !meso
speed_c             =    true    !global,meso,ruc
cal_smooth_c        =    false   !global,meso,ruc
CALCAPE_c           =    true    !global,meso,ruc
calq2m_rh2m_c       =    true    !meso,ruc
calrh2td2m_c        =    false   !meso,ruc
post2dbz_c          =    false   !global,meso,ruc
cal_dttase_c        =    false   !global,meso,ruc
cal_sweat_c         =    true    !global,meso,ruc
cal_srh_c           =    false   !global,meso,ruc
cal_tempadv_c       =    false   !meso,ruc
cal_shr_c           =    false   !global,meso,ruc
cal_PcTcLiLfc_c     =    true    !meso,ruc
cal_bli_c           =    true    !global,meso,ruc
ilc_c               =    true    !global,meso,ruc
/
&grib_parameter1
vsel1               =   1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 0, 0, 0
vsel2               =   1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 0, 0, 0
vsel3               =   1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 0, 0, 0
vsel4               =   1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 0, 0, 0
/
&grib_parameter2
dpbnd               =   300.E2
itype               =   1
/
EOF
elif [ $levels -eq 26 ];then
   test -s namelist.input && rm -f namelist.input
   cat > namelist.input <<EOF
&ctl_file
path                =    "."
grads_ctl           =    "post.ctl_${cur_time_str}"
ctl_flag            =    "meso" ! (global,meso,ruc)
/
&choose_output
vor_div_c           =    true    !global,meso,ruc
rh_c                =    true    !global,meso,ruc
t_td_c              =    true    !global,meso,ruc
t_adv_vor_adv_c     =    false    !global
q_flux_div_c        =    true    !global,meso,ruc
thetase_c           =    true    !global,meso,ruc
ki_c                =    true    !global,meso,ruc
t24_c               =    false   !meso
h24_c               =    false   !meso
p24_c               =    false   !meso
h500_c              =    false   !meso
rain_c              =    false   !meso
rain3_c             =    false   !meso
rain6_c             =    false   !meso
rain12_c            =    false   !meso
rain24_c            =    false   !meso
speed_c             =    true    !global,meso,ruc
cal_smooth_c        =    true    !global,meso,ruc
CALCAPE_c           =    true    !global,meso,ruc
calq2m_rh2m_c       =    true    !meso,ruc
calrh2td2m_c        =    true    !meso,ruc
post2dbz_c          =    true    !global,meso,ruc
cal_dttase_c        =    true    !global,meso,ruc
cal_sweat_c         =    true    !global,meso,ruc
cal_srh_c           =    true    !global,meso,ruc
cal_tempadv_c       =    true    !meso,ruc
cal_shr_c           =    true    !global,meso,ruc
cal_PcTcLiLfc_c     =    true    !meso,ruc
cal_bli_c           =    true    !global,meso,ruc
ilc_c               =    true    !global,meso,ruc
/
&grib_parameter1
vsel1     =  1000,975,950,925,900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,150,100,70,50,30,20,10,0,0,0,0
vsel2     =  1000,975,950,925,900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,150,100,70,50,30,20,10,0,0,0,0
vsel3     =  1000,975,950,925,900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,150,100,70,50,30,20,10,0,0,0,0
vsel4     =  1000,975,950,925,900,850,800,750,700,650,600,550,500,450,400,350,300,250,200,150,100,70,50,30,20,10,0,0,0,0
/
&grib_parameter2
dpbnd               =   300.E2
itype               =   1
/
EOF
fi

#####################
# run program
#####################
${PRODUCT_BIN}

#####################
# post
#####################
test -s diag.ctl_${cur_time_str} && mv diag.ctl_${cur_time_str} ..
test -s diag_${cur_time_str} && mv diag_${cur_time_str} ..

######################
# END
######################
date
