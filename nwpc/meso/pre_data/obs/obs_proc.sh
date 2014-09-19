#!/bin/sh

################
# head
################

set -x
set -e
set -u

###############
#	param
###############

RUN_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso/run/obs

DATA_TIME=2014061012
OBS_DIR=/cma/g2/COMMDATA/OPER/nwp/aob_reg
BACKGRD_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso/run/bckg

OBS_PROC_BIN=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4/4dvar/preproc/ObsGts/ObsProc.exe

while getopts "t:d:b:r:" arg
do
	case $arg in
		t)
			DATA_TIME=$OPTARG
			;;
		d)
			OBS_DIR=$OPTARG
			;;
		b)
			BACKGRD_DIR=$OPTARG
			;;
		r)
			RUN_DIR=$OPTARG
	esac
done

begintime=$DATA_TIME

test -d ${RUN_DIR} | mkdir -p ${RUN_DIR}
cd ${RUN_DIR} 
rm -f  ${RUN_DIR}/*

cd ${RUN_DIR}

######################
# namelist.obsproc
######################

cat > namelist.obsproc <<EOF
&record1
! for hlafs area but have 1 more grid at both x & y direction
 tkminlat= 15.0,
 tkmaxlat= 64.5,
 tkminlon= 70.0,
 tkmaxlon= 145.0 /

&record2 
 unit_in_buffs = 50,
! file_buffs = '${OBS_DIR}/aob${begintime}n.dat' /
 file_buffs = '${OBS_DIR}/aob${begintime}.dat' /

&record3 
 unit_out_obs = 60,
 file_out = '${RUN_DIR}/',
 file_obs_num = '${RUN_DIR}/obs_num${begintime}' /

&record4
 opt_checkwrite = 0,
 opt_wndwrite = 0,
 opt_msswrite = 0 /

 &record5
  AirepTopP=150.,
  AirepLowP=925.,
  SoundRhTop=100.,
  RhMin=5. /
EOF

################
# ObsProc.exe
################

${OBS_PROC_BIN}
sleep 10

#################
# rename outputs
#################

cd ${RUN_DIR}
cp TEMP TEMP${begintime}00
cp SYNOP SYNOP${begintime}00
cp SHIPS SHIPS${begintime}00
cp AIREP AIREP${begintime}00

#################
# clean up
#################

################
# tail
################

set +x
set +e
set +u
