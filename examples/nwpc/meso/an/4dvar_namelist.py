#!/bin/env python
# generate namelists for 4dvar

# $14 => ${14} parameter positon in function

# #################
# head
# #################

import os
import sys
import shutil
from datetime import datetime, timedelta

print datetime.now()

sys.path.append('../include')
import configure

###############
# directory
###############
base_dir = configure.BASE_DIR
base_source_dir = configure.BASE_SOURCE_DIR

run_dir = base_dir + '/run/an'

geo_static_data_dir = configure.GEO_STATIC_DATA_DIR

############
# parameter
############
begin_date_time = configure.BEGIN_DATE_TIME
yyyymmddhh = configure.BEGINTIME
begintime = yyyymmddhh

mfcast_len = configure.MFCAST_LEN
do_static = configure.DO_STATIC
do_3dv = configure.DO_3DV

output_inteval = configure.OUTPUT_INTEVAL
model_dt = configure.MODEL_DT
make_surface_t = configure.MAKE_SURFACE_T

end_date_time = configure.END_DATE_TIME
endtime = configure.ENDTIME
step_max = mfcast_len * 3600 / model_dt
step_output = output_inteval * 3600 / model_dt

yyyy1 = configure.YYYY1
mm1 = configure.MM1
dd1 = configure.DD1
hh1 = configure.HH1

yyyy2 = configure.YYYY2
mm2 = configure.MM2
dd2 = configure.DD2
hh2 = configure.HH2

########################
#	enter work dir
########################
if not os.path.isdir(run_dir):
    os.makedirs(run_dir)

os.chdir(run_dir)

if not os.path.isdir('input'):
    os.makedirs('input')

if not os.path.isdir('output'):
    os.makedirs('output')

if not os.path.isdir('output/check'):
    os.makedirs('output/check')

if not os.path.isdir('grads'):
    os.makedirs('grads')

#ln -sf ${geo_static_data_dir} geog_data

#######################
# prepare data
#######################


#################
# namelists
#################

# namelist_h.input
print "generate namelist.h...",
if os.path.exists('namelist_h.input'):
    os.remove('namelist_h.input')

namelist_h_input_str = """ &namelist_01
   s_we = 1,
   e_we = 502,
   s_sn = 1,
   e_sn = 330,
   s_vert = 1,
   e_vert = 31,
   spec_bdy_width = 5,
   dt = {model_dt},
   time_step_max = {step_max},
   time_step_count_output = {step_output},
   step_phytend_output = 0,
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
   bl_surface_physics = 1,
   bl_pbl_physics = 1,
   cu_physics = 2 /

 &namelist_05
   init_date = {yyyymmddhh},
   start_year = {yyyy1},
   start_month = {mm1},
   start_day = {dd1},
   start_hour = {hh1},
   start_minute = 00,
   start_second = 00,
   end_year = {yyyy2},
   end_month = {mm2},
   end_day = {dd2},
   end_hour = {hh2},
   end_minute = 00,
   end_second = 00,
   interval_seconds = 10800,
   real_data_init_type = 2,
   bdyfrq = 10800,
   nested = .false.,
   specified = .false. /

 &namelist_bckg
  nz_bckg    = 17,
  xs_we_bckg = 0.,
  ys_sn_bckg = 0.,
  xe_we_bckg = 180.,
  ye_sn_bckg = 90.,
  xd_bckg    = 0.28125,
  yd_bckg    = 0.28125,
  p_bckg = 1000,925, 850, 700,
            600, 500, 400, 300,
            250, 200, 150, 100,
             70,  50,  30,  20, 10/

 &namelist_si
  ideal_flags = 0,       !ideal_flags=1 for idealtest and ideal_flags=0 for realdata
  do_static_data = {do_static},
  do_3dv = .false.,
  do_9210 = .false.,
  do_surface_t = {make_surface_t}, ! .true. not use surface temperature in T213 data set
  hinterp_method  = 2,
  vinterp_method  = 2,
  op_ver_lev = 2 /     ! op_ver_lev=0 for uniform level and op_ver_lev=1 for uneven level

 &namelist_dfilter
  do_df = .false.,
  df_period=10800.0 /        ! 2*T=2*10800sec=6hr :(-T,T), unit:sec
""".format(model_dt=model_dt,
           step_max=step_max,
           step_output=step_output,
           yyyy1=yyyy1,
           mm1=mm1,
           dd1=dd1,
           hh1=hh1,
           yyyy2=yyyy2,
           mm2=mm2,
           dd2=dd2,
           hh2=hh2,
           do_static=do_static,
           yyyymmddhh=yyyymmddhh,
           make_surface_t=make_surface_t
)
with open('namelist_h.input', 'w') as f:
    f.write(namelist_h_input_str)

print "Done"
print "===============namelist_h.input============"
print namelist_h_input_str
print "=================END======================="

# namelist.input
print "generate namelist.input...",

if os.path.exists('namelist.input'):
    os.remove('namelist.input')

namelist_input_str = """ &namelist_01
   s_we = 1,
   e_we = 502,
   s_sn = 1,
   e_sn = 330,
   s_vert = 1,
   e_vert = 31,
   spec_bdy_width = 5,
   dt = {model_dt},
   time_step_max = {step_max},
   time_step_count_output = {step_output},
   step_phytend_output = 0,
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
   mp_lc_logical = .false.,    ! .true. for microphysics, .false. for largescale_rain
   mp_physics = 0,
   lc_physics = 0,    ! now only 1 can selected(031212)
   ra_lw_physics = 0,
   ra_sw_physics = 0,
   bl_sfclay_physics = 0,
   bl_surface_physics = 0,
   bl_pbl_physics = 0,
   cu_physics = 0 /

 &namelist_05
   init_date = {yyyymmddhh},
   start_year = {yyyy1},
   start_month = {mm1},
   start_day = {dd1},
   start_hour = {hh1},
   start_minute = 00,
   start_second = 00,
   end_year = {yyyy2},
   end_month = {mm2},
   end_day = {dd2},
   end_hour = {hh2},
   end_minute = 00,
   end_second = 00,
   interval_seconds = 10800,
   real_data_init_type = 2,
   bdyfrq = 10800,
   nested = .false.,
   specified = .true. /

 &namelist_bckg
  nz_bckg    = 17,
  xs_we_bckg = 0.,
  ys_sn_bckg = 0.,
  xe_we_bckg = 180.,
  ye_sn_bckg = 90.,
  xd_bckg    = 0.28125,
  yd_bckg    = 0.28125,
  p_bckg = 1000,925, 850, 700,
            600, 500, 400, 300,
            250, 200, 150, 100,
             70,  50,  30,  20, 10/

 &namelist_si
  ideal_flags = 0,       !ideal_flags=1 for idealtest and ideal_flags=0 for realdata
  do_static_data = {do_static},
  do_3dv = .false.,
  do_9210 = .false.,
  do_surface_t = {make_surface_t}, ! .true. not use surface temperature in bckg data set
  hinterp_method  = 2,
  vinterp_method  = 2,
  op_ver_lev = 2 /       ! op_ver_lev=0 for uniform level and op_ver_lev=1 for uneven level

 &namelist_dfilter
  do_df = .false.,
  df_period=10800.0 /        ! 2*T=2*10800sec=6hr :(-T,T), unit:sec
""".format(model_dt=model_dt,
           step_max=step_max,
           step_output=step_output,
           yyyy1=yyyy1,
           mm1=mm1,
           dd1=dd1,
           hh1=hh1,
           yyyy2=yyyy2,
           mm2=mm2,
           dd2=dd2,
           hh2=hh2,
           do_static=do_static,
           yyyymmddhh=yyyymmddhh,
           make_surface_t=make_surface_t
)

with open('namelist.input', 'w') as f:
    f.write(namelist_input_str)

print "Done"
print "===============namelist.input=============="
print namelist_input_str
print "=================END======================="

# namelist.4dvar

print "generate namelist.4dvar...",
if os.path.exists('namelist.4dvar'):
    os.remove('namelist.4dvar')

namelist_4dvar_str = """&record1
 ANALYSIS_VERSION = 'GRAPES_4DVAR_2.0' /

&record2
 VERT_COOR = 'Terrian-Following Height' /

&record3
 ANALYSIS_DATE = '{begintime}' /

&record4
 miy_h= 330, 
 mjx_h= 502, 
 miy_l= 330,
 mjx_l= 502,  
 mks  = 1,
 mkp  = 31 /   

&record5
 lats   = 15.0,
 lonw   = 70.0,
 dlat_h = 0.15,
 dlon_h = 0.15,
 dlat_l = 0.15,
 dlon_l = 0.15 / 

&record6 
 tkminlat  =  15.0,
 tkmaxlat  =  64.3,
 tkminlon  =  70.0, 
 tkmaxlon  = 145.0,
 ptop_sound= 10.0 /

&record7 
 iobs_sound= 1,
 id_obsuv_sound = 1,
 id_obsmss_sound= 1,
 id_obshum_sound= 1 /

&record8
 iobs_synop= 1, 
 id_obsuv_synop = 0,
 id_obsmss_synop= 1,
 id_obshum_synop= 0 /

&record9
 iobs_ships= 1,
 id_obsuv_ships = 1,
 id_obsmss_ships= 1,
 id_obshum_ships= 1 /

&record10
 iobs_airep= 1,
 id_obsuv_airep = 1,
 id_obsT_airep  = 2 /   ! just=2, only T for airep.

&record11
 iobs_satob= 0,
 id_obsuv_satob = 1 /  

&record12
 iobs_bda= 0,
 id_obsVt_bda = 0,
 id_obsmss_bda= 0,
 id_obshum_bda= 0 /

&record13
 iobs_gpspw= 0 /

&record14
 iobs_noaa16_hirs = 0,
 iobs_noaa16_amsua= 0,
 iobs_noaa16_amsub= 0,
 iobs_noaa17_hirs = 0,
 iobs_noaa17_amsua= 0,
 iobs_noaa17_amsub= 0,
 iobs_noaa15_amsua= 0,
 iobs_noaa15_amsub= 0 /

&record15
 lbiasprep  = 0,
 lbias  = 0 /

&record16 
 iobs_vad= 0,
 id_obsuv_vad = 1,
 id_obsmss_vad= 1 /

&record20
 id_modmss     = 1,
 id_modhum     = 3,
 id_bal        = 2,
 id_output_ana = 1 /

&record21 
 file_output = './output/' /
 
&record22 
 file_sound = './input/GTS/TEMP', 
 file_synop = './input/GTS/SYNOP',
 file_ships = './input/GTS/SHIPS',
 file_airep = './input/GTS/AIREP',
 file_satob = './input/GTS/SATOB', 
 file_vad = './input/VAD/VAD' /
 
&record23 
 file_bda = './input/bogus/{begintime}.BDA' /

&record24
 file_gpspw = './input/gpspw/GPSG' /

&record25
 file_noaa16_hirs  = './input/rt7data/noaa16_hrs{begintime}',
 file_noaa16_amsua = './input/rt7data/noaa16_ama{begintime}',
 file_noaa16_amsub = './input/rt7data/noaa16_amb{begintime}',
 file_noaa17_hirs  = './input/rt7data/noaa17_hrs{begintime}',
 file_noaa17_amsua = './input/rt7data/noaa17_ama{begintime}',
 file_noaa17_amsub = './input/rt7data/noaa17_amb{begintime}',
 file_noaa15_amsua = './input/rt7data/noaa15_ama{begintime}',
 file_noaa15_amsub = './input/rt7data/noaa15_amb{begintime}',
 file_pftrop   = './input/rt7para/prof_trop.dat',
 file_input_xxx= './input/rt7para/input_hirs.dat',
                 './input/rt7para/input_amsua.dat',
                 './input/rt7para/input_amsub.dat',
                 './input/rt7para/input_hirs.dat',
                 './input/rt7para/input_amsua.dat',
                 './input/rt7para/input_amsub.dat', 
                 './input/rt7para/input_hirs.dat', 
                 './input/rt7para/input_amsua.dat',
                 './input/rt7para/input_amsub.dat' /

&record30
 file_xbchk     = './output/check/xbchk.dat',
 file_dxa_binary= './output/dxa{begintime}.dat',
 file_xa_binary = './output/xa{begintime}.dat',
 file_dxa_grads = './output/grads/dxa_grads.dat',
 file_xa_grads  = './output/grads/xa_grads.dat',
 file_dxa_NetCDF= './output/dxa_NetCDF.dat',
 file_xa_NetCDF = './output/xa_NetCDF.dat' /
 
&record31 
 file_gtschk         = './output/check/chk',
 file_bdachk         = './output/check/chk',
 file_gpspwchk       = './output/check/chkgps', 
 file_noaa16hirschk  = './output/check/noaa16hirschk.dat',
 file_noaa16amsuachk = './output/check/noaa16amsuachk.dat',
 file_noaa16amsubchk = './output/check/noaa16amsubchk.dat',
 file_noaa17hirschk  = './output/check/noaa17hirschk.dat',
 file_noaa17amsuachk = './output/check/noaa17amsuachk.dat',
 file_noaa17amsubchk = './output/check/noaa17amsubchk.dat',
 file_noaa15amsuachk = './output/check/noaa15amsuachk.dat',
 file_noaa15amsubchk = './output/check/noaa15amsubchk.dat' /

&record32
 file_dsound= './output/check/dsound{begintime}',
 file_dsynop= './output/check/dsynop{begintime}',
 file_dships= './output/check/dships{begintime}',
 file_dairep= './output/check/dairep{begintime}',
 file_dsatob= './output/check/dsatob{begintime}',
 file_dbda  = './output/check/dbda{begintime}',
 file_dgpspw= './output/check/dgpspw{begintime}',
 file_dvad= './output/check/dvad',
 file_innotbnoaa16hirs = './output/check/innotbnoaa16hirs.dat',
 file_innotbnoaa16amsua= './output/check/innotbnoaa16amsua.dat',
 file_innotbnoaa16amsub= './output/check/innotbnoaa16amsub.dat',
 file_innotbnoaa17hirs = './output/check/innotbnoaa17hirs.dat',
 file_innotbnoaa17amsua= './output/check/innotbnoaa17amsua.dat',
 file_innotbnoaa17amsub= './output/check/innotbnoaa17amsub.dat' 
 file_innotbnoaa15amsua= './output/check/innotbnoaa15amsua.dat',
 file_innotbnoaa15amsub= './output/check/innotbnoaa15amsub.dat' /

&record33
 file_mininfo = './output/check/mini_info{begintime}.dat', 
 file_minerror= './output/check/mini_error{begintime}.dat' /

&record34
 surfout  = './output/' /

&record35
 dqcu_sound  = 4.0,
 dqcv_sound  = 4.0,
 dqcmss_sound= 2.5,
 dqchum_sound= 3.5,
 dqcu_synop  = 4.0,
 dqcv_synop  = 4.0,
 dqcmss_synop= 4.0,
 dqchum_synop= 4.0,
 dqcu_ships  = 4.0,
 dqcv_ships  = 4.0,
 dqcmss_ships= 4.0,
 dqchum_ships= 4.0,
 dqcu_airep  = 4.0,
 dqcv_airep  = 4.0,
 dqcT_airep  = 4.0,
 dqcu_vad    = 4.0,
 dqcv_vad    = 4.0,
 dqcmss_vad  = 2.5,
 dqcu_satob  = 4.0,
 dqcv_satob  = 4.0  /

&record36
 dqcVt_bda  = 3.5,
 dqcmss_bda = 2.5,
 dqchum_bda = 3.5 /

&record37
 dqc_gpspw = 4.0 /

&record40
 mcut=31,
 Lkppsi=5,
 Lkpchi=5,
 Lkpmss=5,
 Lkphum=2,
 rf_passes=10,
 rf_lengthpsi=500000.0,
 rf_lengthchi=500000.0,
 rf_lengthmss=500000.0,
 rf_lengthhum=200000.0 /

&record41
 eps0  = 0.001,
 ntmax = 50 /

&record42
 inmc_mss = 1,
  dpath_mss='./input/rmsdata/piu1112.dat',
 inmc_psi= 1,
  dpath_psi='./input/rmsdata/psi1112.dat',
 inmc_chi= 1,
  dpath_chi='./input/rmsdata/chi1112.dat',
 inmc_hum= 1,
  dpath_rh='./input/rmsdata/rh1112.dat', 
  dpath_q='./input/rmsdata/q1112.dat' /

&record51
 int_obs = -36, 
 first_outloop = .true. /
""".format(begintime=begintime)

with open('namelist.4dvar', 'w') as f:
    f.write(namelist_4dvar_str)
print "Done"
print "===============namelist.4dvar============"
print namelist_4dvar_str
print "=================END======================="


#################
# clean up
#################

################
# tail
################

print datetime.now()



