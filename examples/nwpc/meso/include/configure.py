#!/bin/env python
# configure.py
# configure file

# ########
# param depended on project locaiton.
# ########

BASE_DIR = '/cma/g3/wangdp/nwp/system/grapes_meso/my_grapes_meso'
BASE_SOURCE_DIR = '/cma/g3/wangdp/nwp/system/grapes_meso/GRAPES_MESO3.3.2.4'
GEO_STATIC_DATA_DIR = '/cma/g2/COMMDATA/static/rfs/geog/v3'

# ###############
# run directory
################
BASE_RUN_DIR = BASE_DIR + '/run'
BCKG_RUN_DIR = BASE_RUN_DIR + '/bckg'
OBS_RUN_DIR = BASE_RUN_DIR + '/obs'
AN_RUN_DIR = BASE_RUN_DIR + '/an'
SI_RUN_DIR = BASE_RUN_DIR + '/si'
FCST_RUN_DIR = BASE_RUN_DIR + '/fcst'
POST_RUN_DIR = BASE_RUN_DIR + '/post'
PRODS_RUN_DIR = BASE_RUN_DIR + '/prods'

BASE_CONDAT_DIR = BASE_DIR + '/condat'
AN_CONDAT_DIR = BASE_CONDAT_DIR + '/an'
SI_CONDAT_DIR = BASE_CONDAT_DIR + '/si'
FCST_CONDAT_DIR = BASE_CONDAT_DIR + '/fcst'
POST_CONDAT_DIR = BASE_CONDAT_DIR + '/post'
PRODS_CONDAT_DIR = BASE_CONDAT_DIR + '/prods'
STATIC_CONDAT_DIR = BASE_CONDAT_DIR + '/static'

BASE_BIN_DIR = BASE_DIR + '/bin'

###############
# bin dierctory
###############

# pre_data/bckg
# wgrib2
WGRIB2_BIN = "/cma/u/app/wgrib2/bin/wgrib2"
# read_for_grapes
READ_FOR_GRAPES_BIN = BASE_BIN_DIR + "/read_for_grapes_forGRIB2.exe"

# obs
OBS_PROC_BIN = "{BASE_SOURCE_DIR}/4dvar/preproc/ObsGts/ObsProc.exe".format(BASE_SOURCE_DIR=BASE_SOURCE_DIR)

# si
SI_BIN = BASE_SOURCE_DIR + '/fcst/grapes_model/run/si.exe'

# an
M4DVAR_H_BIN = BASE_SOURCE_DIR + '/4dvar/m4dv/rundir/4dvar_h.exe'
M4DVAR_BIN = BASE_SOURCE_DIR + '/4dvar/m4dv/rundir/4dvar.exe'
MDVAR_BIN = BASE_SOURCE_DIR + '/fcst/modelvar_proc/mdvar.exe'

# fcst
GRAPES_BIN = BASE_SOURCE_DIR + '/fcst/grapes_model/run/grapes.exe'

# post
PRODUCT_BIN = BASE_DIR + '/src/post/grapes_post_diag_ibm/product.exe'

# prods
GRADS2GRIB_BIN_DIR = BASE_BIN_DIR + '/grads2grib.exe'


#########################################
# param depended on running environment
#########################################

# model param

MFCAST_LEN = 24
DO_STATIC = '.true.'
DO_3DV = '.true.'

OUTPUT_INTEVAL = 3  # model output interval in hour
MODEL_DT = 90  # model time step in second
MAKE_SURFACE_T = '.false.'

STEP_MAX = MFCAST_LEN * 3600 / MODEL_DT
STEP_OUTPUT = OUTPUT_INTEVAL * 3600 / MODEL_DT

LEVELS = 26

# datetime

from datetime import datetime, timedelta

BEGIN_DATE_TIME = datetime.strptime("2014090812", "%Y%m%d%H")
BEGINTIME = BEGIN_DATE_TIME.strftime("%Y%m%d%H")
YYYY1 = BEGIN_DATE_TIME.strftime("%Y")
MM1 = BEGIN_DATE_TIME.strftime("%m")
DD1 = BEGIN_DATE_TIME.strftime("%d")
HH1 = BEGIN_DATE_TIME.strftime("%H")

END_DATE_TIME = BEGIN_DATE_TIME + timedelta(hours=MFCAST_LEN)
ENDTIME = END_DATE_TIME.strftime("%Y%m%d%H")
YYYY2 = END_DATE_TIME.strftime("%Y")
MM2 = END_DATE_TIME.strftime("%m")
DD2 = END_DATE_TIME.strftime("%d")
HH2 = END_DATE_TIME.strftime("%H")


#########################################
# date from other system.
#########################################
T639_BCKG_DATA_DIR = "/cma/g2/COMMDATA/nwp/T639/op/{YYYY1}/NWP_GMFS_639_gsi/prods/grib2_orig".format(YYYY1=YYYY1)
OBS_DATA_DIR = "/cma/g2/COMMDATA/OPER/nwp/aob_reg"



