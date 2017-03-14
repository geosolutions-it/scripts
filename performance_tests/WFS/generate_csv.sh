#!/bin/bash
# This sample script generate tiled and untiled requests for the layer, gridset
# and other parameters provided. 

#######################
# Common options
#CAPABILITIES_URL="http://demo.geo-solutions.it/geoserver/ows?service=wfs&version=1.1.0&request=GetCapabilities"
#CAPABILITIES_USER=""
#CAPABILITIES_PASS=""

#LAYER=${1:-unused:layer}

# TODO: why _level10 , also why the escape?
#GRIDSET=${2:-EPSG\:3857_level10}

# this must be the same SRS
REGION=${3:-"100000 525000 420000 980000"}
SRSNAME="${4:-"urn:ogc:def:crs:EPSG::27700"}"

#######################
# WFS Options
SIZE=10000

#######################
#Limit of rows to create
#REQPERGRANULE=10
#TIME_RECORDS_LIMIT=5

#######################
#Tiled Options
#LEVELS="1,2,3,4,5,6,7,8,9"

#GRIDSET_DIR="tiled/gridsets"

#######################
#Untiled Options
#MAXSIZE="2048 2048"
#MINSIZE="512 512"
#MAXRES="0.07"
#MINRES="0.007"

######################
# OUTPUT files
#TILED_FILE=csv/tiled.csv
#UNTILED_FILE=csv/untiled.csv
WFS_FILE=csv/wfs_bboxes.csv

###############################################################################
# TEMP_FILES
#TIMES_FILE=$(mktemp)
#UNTILED_TEMP_FILE=$(mktemp)
#CAPABILITIES_DOC=tmp/ows.xml

###############################################################################
# SCRIPT START
###############################################################################
echo "Options"
#echo "LAYER  : ${LAYER}"
#echo "GRIDSET: $GRIDSET"
echo "SRS    : $SRSNAME"
echo "REGION : $REGION"
echo "SIZE   : $SIZE"
echo
#echo "Downloading current capabilities document..."

#wget_params="-q -O"
#if [[ ! -z "${CAPABILITIES_USER// }" ]]; then 
#  wget_params=" $wget_params --user=$CAPABILITIES_USER --password=$CAPABILITIES_PASS --auth-no-challenge"
#fi

# ensure the capabilities doc parent folder exists and output to it
#mkdir -p `dirname ${CAPABILITIES_DOC}` && echo "${wget_params}" - "${CAPABILITIES_URL}" > ${CAPABILITIES_DOC}

#mkdir -p `dirname ${CAPABILITIES_DOC}` && wget "${wget_params}" - "${CAPABILITIES_URL}" > ${CAPABILITIES_DOC}
#exit

#echo "Fetching times for layer ${LAYER}..."
#Get Times 
#python time/time_request.py -capabilities_doc ${CAPABILITIES_DOC} -layer ${LAYER} -name  > ${TIMES_FILE} 

#echo "Generating tiled requests for layer ${LAYER}..."
#Generate Tiled Requests 
#python tiled/tiled_request.py -count ${REQPERGRANULE} -gridset ${GRIDSET} -gridset_dir ${GRIDSET_DIR} -region ${REGION} -levels ${LEVELS}  -auxiliary_csv ${TIMES_FILE} -srs >> ${TILED_FILE}

echo "Generating wfs requests..."
#Generate Untiled Requests (with SRS NAME)
mkdir -p `dirname ${WFS_FILE}` && python wfs_request.py -region  ${REGION} -size ${SIZE} -srs ${SRSNAME} > ${WFS_FILE}

echo "Output: ${WFS_FILE}"
#Cartesina product with tunes file
#./util/cartesian.sh -d ";" ${TIMES_FILE} ${UNTILED_TEMP_FILE}>> ${UNTILED_FILE}
#echo "cleaning temporaney files"
#rm -f $TIMES_FILE
#rm -f $UNTILED_TEMP_FILE



