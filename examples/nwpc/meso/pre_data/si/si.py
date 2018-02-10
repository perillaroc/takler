#!/bin/env python
# @ comment = GRAPES
# @ job_type = serial
# # @ executable = ./si.exe
# @ input = /dev/null
# @ output = ./out/si_$(jobid).out
# @ error = ./out/si_$(jobid).err
# @ initialdir = ./
# # @ notify_user = wangdp@cma19n03
# @ class = normal
# @ notification = complete
# @ checkpoint = no
# @ restart = no
# @ queue
##################
# head
##################

import os
from datetime import datetime, timedelta
import subprocess
import shutil
import sys

print datetime.now()

sys.path.append('../../include')
import configure

###############
# param
###############

# param 
model_dt = configure.MODEL_DT
step_max = configure.STEP_MAX
step_output = configure.STEP_OUTPUT
begintime = configure.BEGINTIME

yyyy1 = configure.YYYY1
mm1 = configure.MM1
dd1 = configure.DD1
hh1 = configure.HH1
yyyy2 = configure.YYYY2
mm2 = configure.MM2
dd2 = configure.DD2
hh2 = configure.HH2

do_static = configure.DO_STATIC
make_surface_t = configure.MAKE_SURFACE_T

# dir
run_dir = configure.SI_RUN_DIR

# input static data
geodata_dir = configure.STATIC_CONDAT_DIR + "/geog"
condata_dir = configure.FCST_CONDAT_DIR

# input background data
bckg_dir = configure.BCKG_RUN_DIR

#BIN 
si_bin = configure.SI_BIN

########################
#	enter work dir
########################

if not os.path.isdir(run_dir):
    os.makedirs(run_dir)

os.chdir(run_dir)

# clean previous output
# TODO: rm -rf
if os.path.isfile('grapesbdy'):
    os.remove('grapesbdy')
if os.path.isfile('grapesinput'):
    os.remove('grapesinput')
if os.path.isfile('namelist.input'):
    os.remove('namelist.input')

#######################
# prepare data
#######################
#prepare geo data
if os.path.islink('geog_data'):
    os.remove('geog_data')
os.symlink(geodata_dir, 'geog_data')

#condata
if not os.path.exists('GENPARM.TBL'):
    shutil.copyfile(condata_dir + '/GENPARM.TBL', 'GENPARM.TBL')

if not os.path.exists('GEOGRID.TBL'):
    shutil.copyfile(condata_dir + '/GEOGRID.TBL', 'GEOGRID.TBL')

if not os.path.exists('LANDUSE.TBL'):
    shutil.copyfile(condata_dir + '/LANDUSE.TBL', 'LANDUSE.TBL')

if not os.path.exists('SOILPARM.TBL'):
    shutil.copyfile(condata_dir + '/SOILPARM.TBL', 'SOILPARM.TBL')

if not os.path.exists('VEGPARM.TBL'):
    shutil.copyfile(condata_dir + '/VEGPARM.TBL', 'VEGPARM.TBL')

if not os.path.exists('RRTM_DATA.TBL'):
    shutil.copyfile(condata_dir + '/RRTM_DATA', 'RRTM_DATA')

# bckgdata
if os.path.islink('bckg_data'):
    os.remove('bckg_data')
os.symlink(bckg_dir, 'bckg_data')

#################
# namelist
#################

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
   static_data_output = 1,
   split_output = .true.,
   modelvar_output = .false.,
   modelvar_split = .false.,
   time_step_modelvar_count_output = {step_output},
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
   init_date = {begin_date_time},
   start_year = {YYYY1},
   start_month = {MM1},
   start_day = {DD1},
   start_hour = {HH1},
   start_minute = 00,
   start_second = 00,
   end_year = {YYYY2},
   end_month = {MM2}
   end_day = {DD2},
   end_hour = {HH2},
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
""".format(
    model_dt=model_dt,
    step_max=step_max,
    step_output=step_output,
    begin_date_time=begintime,
    YYYY1=yyyy1,
    MM1=mm1,
    DD1=dd1,
    HH1=hh1,
    YYYY2=yyyy2,
    MM2=mm2,
    DD2=dd2,
    HH2=hh2,
    do_static=do_static,
    make_surface_t=make_surface_t
)

with open('namelist.input', 'w') as namelist_file:
    namelist_file.write(namelist_input_str)

############################################################
# run si.exe
print "Waiting for si.exe to finish..."
subprocess.check_call(si_bin)
print "si.exe finished"

# tests output
if os.path.isfile('grapesinput'):
    print "grapesinput created!"
else:
    print "grapesinput NOT created!"
    sys.exit(2)

#################
# clean up
#################

#rm -rf bckg

################
# tail
################

print datetime.now()
