#!/bin/ksh
# @ comment = GRAPES
# @ job_type = serial
# @ input = /dev/null
# @ output = ./out/t639_grib2bin.out
# @ error = ./out/t639_grib2bin.err
# @ initialdir = ./
# @ class = normal
# @ notification = complete
# @ checkpoint = no
# @ restart = no
# @ queue

set -x
set -e
set -u

date

###############
# predefine param
###############

DATA_TIME=2014061012
DATA_DIR=/cma/g2/COMMDATA/nwp/T639/op/2014/NWP_GMFS_639_gsi/prods/grib2_orig
BIN_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso/bin
RUN_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso/run/bckg

while getopts "t:d:r:" arg
do
	case $arg in
		t)
			DATA_TIME=$OPTARG
			;;
		d)
			DATA_DIR=$OPTARG
			;;
		r)
			RUN_DIR=$OPTARG
			;;
	esac
done

#######################################
# directory
#######################################


# directory
set_directory(){
	# data directory
	# input T639 data
	T639_GMFS=${DATA_DIR}
	# output background data
	RUN_DIR=${RUN_DIR}
	
	# program path
	# newdate
	NEWDATE_BIN=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4/data_proc/T639_proc/newdate
	# wgrib2
	WGRIB2_BIN=wgrib2
	# read_for_grapes
	#READ_FOR_GRAPES_BIN=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4/data_proc/T639_proc/read_for_grapes.exe
	READ_FOR_GRAPES_BIN=${BIN_DIR}/read_for_grapes_forGRIB2.exe
}

set_directory

#######################################
# parameter for wgrib2
#######################################

# date
DATE=`echo $DATA_TIME |cut -c1-8`
TIME=`echo $DATA_TIME |cut -c9-10`


set_parameter(){
	#==========================#
	# level 17
	#levels="10 20 30 50 70 100 150 200 250 300 400 500 600 700 850 925 1000"
	# level 24
	levels="10 20 30 50 70 100 150 200 250 300 350 400 450 500 550 600 650 700 750 800 850 900 925 950 975 1000"
	#==========================#
	
	forecast_time="012 015 018 021 024 027 030 033 036 039 042 045 048 051 054 057 060"

	endian="little_endian"
	if [ $endian = "big_endian" ];then
	   FMT='-ieee'
	else
	   FMT='-bin'
	fi
	#==========================#
	#---multiply levels ----
	HGT=':HGT:'
	TMP=':TMP:'
	UGRD=':UGRD:'
	VGRD=':VGRD:'
	SPFH=':SPFH:'
	#RH=':RH:'

	#---single level ----
	PS=':PRES:surface:'
	TS=':TMP:surface:'
	TMP2M=':TMP:2 m above'
	UGRD10M=':UGRD:10 m above'
	VGRD10M=':VGRD:10 m above'
	RH2M=':RH:2 m above'
	PRMSL=':PRMSL:'
	SOILT_1=':TMP:0-0.07 m below'
	SOILT_2=':TMP:0.07-0.28 m below'
	SOILT_3=':TMP:0.28-1 m below'
	SOILT_4=':TMP:1-2.55 m below'
	SOILW_1=':SPFH:0-0.07 m below'
	SOILW_2=':SPFH:0.07-0.28 m below'
	SOILW_3=':SPFH:0.28-1 m below'
	SOILW_4=':SPFH:1-2.55 m below'
	TERRAIN=':HGT:surface:'
	LAND='LAND:surface:'
}

set_parameter

###########################
# enter working space
###########################

test -d $RUN_DIR || mkdir -p $RUN_DIR
cd $RUN_DIR

#########################
# process
#########################

#
# ---- to get boundary 12 hours before -----
#
BDYTIME=$(${NEWDATE_BIN} $DATE$TIME -12)

for TTT in $forecast_time
do
    BDY=${T639_GMFS}/T639GSI2GRIB2_ORIG_${BDYTIME}/gmf.639.${BDYTIME}${TTT}.grb2
    if [ ! -s $BDY ];then
      echo "${BDY}: not found!"
      error
    fi

    updateBDYTIME=`${NEWDATE_BIN} $BDYTIME +$TTT `
	
	temp_file_name=T639_$updateBDYTIME

    test -s ${temp_file_name} && rm -f ${temp_file_name}
#---- for multiply levels-----------
    for lev in $levels
    do
      ${WGRIB2_BIN} $BDY | grep "${HGT}${lev} mb:"     | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}
    done

    for lev in $levels
    do
      ${WGRIB2_BIN} $BDY | grep "${TMP}${lev} mb:"     | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}
    done

    for lev in $levels
    do
      ${WGRIB2_BIN} $BDY | grep "${UGRD}${lev} mb:"    | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}
    done

    for lev in $levels
    do
      ${WGRIB2_BIN} $BDY | grep "${VGRD}${lev} mb:"    | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}
    done

    for lev in $levels
    do
      ${WGRIB2_BIN} $BDY | grep "${SPFH}${lev} mb:"    | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}
    done

#--- for single level ----
    ${WGRIB2_BIN} $BDY | grep "$PS"      | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "$TS"      | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "$TMP2M"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "$UGRD10M" | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "$VGRD10M" | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "$RH2M"    | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "$PRMSL"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "${SOILT_1}"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "${SOILT_2}"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "${SOILT_3}"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "${SOILT_4}"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "${SOILW_1}"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "${SOILW_2}"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "${SOILW_3}"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

    ${WGRIB2_BIN} $BDY | grep "${SOILW_4}"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

#    ${WGRIB2_BIN} $BDY | grep "${TERRAIN}"   | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}

#    ${WGRIB2_BIN} $BDY | grep "${LAND}"      | ${WGRIB2_BIN} $BDY -i -order we:ns -no_header -append $FMT ${temp_file_name}


    ######### execute file for grapes_si #######
    echo
    echo " Date converting is: --> $updateBDYTIME "

    ${READ_FOR_GRAPES_BIN} $updateBDYTIME

    ## delete the tmp-file
    echo "Delete the tmp file:"
    echo "                       "${temp_file_name}
    rm -f ${temp_file_name}
 
done

#############
# END
#############

date

set +x
set +u
set +e
