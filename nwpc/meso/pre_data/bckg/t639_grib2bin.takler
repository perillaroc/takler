#!/bin/env python
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

from datetime import datetime, timedelta
import os
import sys
import subprocess

print datetime.now()

sys.path.append('../../include')
import configure

# ##############
# predefine param
# ##############

#######################################
# directory
#######################################

# directory
# data directory
# input T639 data
t639_gmfs = configure.T639_BCKG_DATA_DIR
# output background data
run_dir = configure.BCKG_RUN_DIR

wgrib2_bin = configure.WGRIB2_BIN
read_for_grapes_bin = configure.READ_FOR_GRAPES_BIN

begin_date_time = configure.BEGIN_DATE_TIME

#######################################
# parameter for wgrib2
#######################################

# date
DATE = begin_date_time.strftime("%Y%m%d")
TIME = begin_date_time.strftime("%H")


#==========================#
# level 17
#levels="10 20 30 50 70 100 150 200 250 300 400 500 600 700 850 925 1000"
# level 24
levels = ['10', '20', '30', '50', '70', '100', '150', '200', '250', '300', '350', '400', \
          '450', '500', '550', '600', '650', '700', '750', '800', '850', '900', '925', \
          '950', '975', '1000']
#==========================#

forecast_time = ["012", "015", "018", "021", "024", "027", "030", \
                 "033", "036", "039", "042", "045", "048", "051", "054", "057", "060"]

endian = "little_endian"
if endian == "big_endian":
    FMT = '-ieee'
else:
    FMT = '-bin'

#==========================#
#---multiply levels ----
HGT = ':HGT:'
TMP = ':TMP:'
UGRD = ':UGRD:'
VGRD = ':VGRD:'
SPFH = ':SPFH:'
#RH=':RH:'

multiply_level_list = [HGT, TMP, UGRD, VGRD, SPFH]

#---single level ----
PS = ':PRES:surface:'
TS = ':TMP:surface:'
TMP2M = ':TMP:2 m above'
UGRD10M = ':UGRD:10 m above'
VGRD10M = ':VGRD:10 m above'
RH2M = ':RH:2 m above'
PRMSL = ':PRMSL:'
SOILT_1 = ':TMP:0-0.07 m below'
SOILT_2 = ':TMP:0.07-0.28 m below'
SOILT_3 = ':TMP:0.28-1 m below'
SOILT_4 = ':TMP:1-2.55 m below'
SOILW_1 = ':SPFH:0-0.07 m below'
SOILW_2 = ':SPFH:0.07-0.28 m below'
SOILW_3 = ':SPFH:0.28-1 m below'
SOILW_4 = ':SPFH:1-2.55 m below'
TERRAIN = ':HGT:surface:'
LAND = 'LAND:surface:'

single_level_list = [PS, TS, TMP2M, UGRD10M, VGRD10M, RH2M, PRMSL, SOILT_1, \
                     SOILT_2, SOILT_3, SOILT_4, SOILW_1, SOILW_2, SOILW_3, SOILW_4]

###########################
# enter working space
###########################

if not os.path.isdir(run_dir):
    os.makedirs(run_dir)

print "entering working space... %s" % run_dir
os.chdir(run_dir)

#########################
# process
#########################

#
# ---- to get boundary 12 hours before -----
#
d = timedelta(hours=-12)
bdytime = begin_date_time + d
BDYTIME = bdytime.strftime("%Y%m%d%H")

for TTT in forecast_time:
    BDY = t639_gmfs + "/T639GSI2GRIB2_ORIG_" + BDYTIME + "/gmf.639." + BDYTIME + TTT + ".grb2"
    if not os.path.isfile(BDY):
        print BDY + ": not found!"
        sys.exit(1)
    update_bdy_time = bdytime + timedelta(hours=int(TTT))
    updateBDYTIME = update_bdy_time.strftime("%Y%m%d%H")

    temp_file_name = "T639_" + updateBDYTIME

    if os.path.isfile(temp_file_name):
        os.remove(temp_file_name)

    #---- for multiply levels-----------
    print "multiply levels"
    for field in multiply_level_list:
        for lev in levels:
            wgrib2_command = wgrib2_bin + ' ' + BDY + ' | grep "' + field + lev + ' mb:"     | ' + wgrib2_bin + ' ' + BDY + ' -i -order we:ns -no_header -append ' + FMT + ' ' + temp_file_name
            print "+%s " % wgrib2_command
            subprocess.check_call(wgrib2_command, shell=True)

            #--- for single level ----
    print "single levels"
    for field in single_level_list:
        wgrib2_command = wgrib2_bin + ' ' + BDY + ' | grep "' + field + '"      | ' + \
                         wgrib2_bin + ' ' + BDY + ' -i -order we:ns -no_header -append ' + FMT + ' ' + temp_file_name
        subprocess.check_call(wgrib2_command, shell=True)

    ######### execute file for grapes_si #######
    print " Date converting is: --> " + updateBDYTIME
    command_str = read_for_grapes_bin + ' ' + updateBDYTIME
    print command_str
    subprocess.check_call(command_str, shell=True)

    ## delete the tmp-file
    print "Delete the tmp file:"
    print "                       " + temp_file_name
    os.remove(temp_file_name)

#############
# END
#############

print datetime.now()
