#!/bin/ksh
# @ comment = GRAPES
# @ job_type = serial
## @ executable = ./si.exe
# @ input = /dev/null
# @ output = ./out/si_$(jobid).out
# @ error = ./out/si_$(jobid).err
# @ initialdir = ./
## @ notify_user = wangdp@cma19n03
# @ class = normal
# @ notification = complete
# @ checkpoint = no
# @ restart = no
# @ queue
##################
# head
##################

set -x
set -e
set -u

###############
# param
###############

#
RUN_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso/run/si

# input static data
GEODATA_DIR=/cma/g2/COMMDATA/static/rfs/geog/v3
CONDATA_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4/fcst/grapes_model/run

# input background data
BCKG_DIR=/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso/run/bckg

# program directory
SI_BIN=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4/fcst/grapes_model/run/si.exe
NEWDATE_BIN=/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4/fcst/grapes_model/run/newdate

YYYYMMDDHH=2014061012
mfcast_len=24
do_static=.true.
do_3dv=.true.

output_inteval=3                 #model output inteval in hour
model_dt=90                      #model time step in second
make_surface_t=.false.

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
		g)
			GEODATA_DIR=$OPTARG
			;;
		c)
			CONDATA_DIR=$OPTARG
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

########################
#	enter work dir
########################

test -d ${RUN_DIR} || mkdir -p ${RUN_DIR}
cd ${RUN_DIR}

# clean previous output
rm -f grapesbdy grapesinput namelist.input

#######################
# prepare data
#######################
#prepare geo data
ln -sf ${GEODATA_DIR} geog_data

#condata
test -f GENPARM.TBL || cp ${CONDATA_DIR}/GENPARM.TBL .
test -f GEOGRID.TBL || cp ${CONDATA_DIR}/GEOGRID.TBL .
test -f LANDUSE.TBL || cp ${CONDATA_DIR}/LANDUSE.TBL .
test -f SOILPARM.TBL || cp ${CONDATA_DIR}/SOILPARM.TBL .
test -f VEGPARM.TBL || cp ${CONDATA_DIR}/VEGPARM.TBL .
test -f RRTM_DATA || cp ${CONDATA_DIR}/RRTM_DATA .

# bckgdata
ln -fs ${BCKG_DIR} bckg_data

#################
# namelist
#################

# generate namelist
#./namelist_grapes_t639data.sh $model_dt $step_max $step_output \
#            $YYYY1 $MM1 $DD1 $HH1 $YYYY2 $MM2 $DD2 $HH2 $do_static \
#            $YYYYMMDDHH ${make_surface_t}
cat > namelist.input << END_OF_DATA
 &namelist_01
   s_we = 1,
   e_we = 502,
   s_sn = 1,
   e_sn = 330,
   s_vert = 1,
   e_vert = 31,
   spec_bdy_width = 5,
   dt = $model_dt,
   time_step_max = $step_max,
   time_step_count_output = $step_output,
   step_phytend_output = 0,
   static_data_output = 1,
   split_output = .true.,
   modelvar_output = .false.,
   modelvar_split = .false.,
   time_step_modelvar_count_output = $step_output,
   wind_output = .true.,
   maxit = 2,
   interp = 0,
   irec = 0,
   nh = 1,
   writetofile = .false.,
   xs_we = 70.,
   ys_sn = 15.,
   cen_lat = 40.,
   xd = 0.15,
   yd = 0.15,
   ztop = 35000.0,
   epson_depart = 1.0,
   i_parent_start = 1,
   j_parent_start = 1,
   shw = 1,
   parent_grid_ratio = 1  / 

 &namelist_02
   dyn_opt = 4,
   coor_opt=1,              !gal=1,sleve1=2
   diff_opt = 1,
   km_opt = 1,
   damp_opt = 0,
   spec_zone = 1,
   relax_zone = 4,
   isfflx = 1,
   ifsnow = 0,
   icloud = 1,
   num_soil_layers = 4,
   julyr = 0,
   julday = 1,
   gmt = 0,
   radt = 60.,
   bldt = 0,
   cudt = 5,
   time_step_begin_restart = 0 /

 &namelist_03
   mp_lc_logical = .true.,    ! .true. for microphysics, .false. for largescale_rain
   mp_physics = 13,
   lc_physics = 1,    ! now only 1 can selected(031212)
   ra_lw_physics = 1,
   ra_sw_physics = 1,
   bl_sfclay_physics = 1,
   bl_surface_physics = 3,
   bl_pbl_physics = 1,
   cu_physics = 2 /

 &namelist_05
   init_date = $YYYYMMDDHH,
   start_year = $YYYY1,
   start_month = $MM1,
   start_day = $DD1,
   start_hour = $HH1,
   start_minute = 00,
   start_second = 00,
   end_year = $YYYY2,
   end_month = $MM2
   end_day = $DD2,
   end_hour = $HH2,
   end_minute = 00,
   end_second = 00,
   interval_seconds = 10800,
   real_data_init_type = 2,
   bdyfrq = 10800,
   nested = .false.,
   specified = .true. /

 &namelist_bckg
  nz_bckg    = 26,
  xs_we_bckg = 0.,
  ys_sn_bckg = -90.,
  xe_we_bckg = 359.71875,
  ye_sn_bckg = 90.,
  xd_bckg    = 0.28125,
  yd_bckg    = 0.28125,
  p_bckg = 1000, 975, 950, 925, 900, 850, 800, 750, 700, 650,
            600, 550, 500, 450, 400, 350, 300,
            250, 200, 150, 100,
             70,  50,  30,  20, 10/

 &namelist_si
  ideal_flags = 0,       !ideal_flags=1 for idealtest and ideal_flags=0 for realdata
  do_static_data = $do_static,
  do_3dv = .false.,
  do_9210 = .false.,
  do_surface_t = ${make_surface_t}, ! .true. not use surface temperature in T213 data set
  hinterp_method  = 2,
  vinterp_method  = 2,
  op_ver_lev = 2 /     ! op_ver_lev=0 for uniform level and op_ver_lev=1 for uneven level

 &namelist_dfilter
  do_df = .false.,
  df_period=10800.0 /        ! 2*T=2*10800sec=6hr :(-T,T), unit:sec
END_OF_DATA

############################################################

# run si.exe
${SI_BIN} #> si.log.$YYYY1$MM1$DD1$HH1

sleep 60

# tests output
if [ -e grapesinput ]; then
	echo grapesinput created!
	#if [ $do_3dv = .true. ]; then
	#	mv grapesinput ${GRAPES_M4DV_DIR}/m4dv/rundir/grapesinput
	#fi
else
	echo grapesinput NOT created!
	exit 2
fi


#################
# clean up
#################
#rm -rf bckg_data

################
# tail
################

set +x
set +e
set +u
