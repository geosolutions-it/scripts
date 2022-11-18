#!/bin/bash
# This sample script generate tiled and untiled requests for the layer, gridset
# and other parameters provided. 


#######################
# Common options
CAPABILITIES_URL="https://cae-dga-cace-web-d-echogeosrv.azurewebsites.net/geoserver/ows?service=wms&version=1.3.0&request=GetCapabilities"
LAYER=${1:-osm:osm}

GRIDSET=${2:-EPSG\:4326}
REGION=${3:-"-180 -90 180 90"}
#######################
#Limit of rows to create
REQPERGRANULE=${4:-100}
TIME_RECORDS_LIMIT=5

#######################
#Tiled Options
LEVELS="1,2,3,4,5,6,7,8,9"

GRIDSET_DIR="tiled/gridsets"

#######################
#Untiled Options
MAXSIZE="2048 2048"
MINSIZE="512 512"
SRSNAME="${GRIDSET%_level*}"
MAXRES="0.07"
MINRES="0.007"

######################
# OUTPUT files
TILED_FILE=csv/tiled.csv
UNTILED_FILE=csv/untiled.csv

###############################################################################
# TEMP_FILES
TIMES_FILE=$(mktemp)
UNTILED_TEMP_FILE=$(mktemp)
CAPABILITIES_DOC=ows.xml

###############################################################################
# SCRIPT START
###############################################################################
echo "Options"
echo "LAYER  : ${LAYER}"
echo "GRIDSET: $GRIDSET"
echo "SRS    : $SRSNAME"
echo "REGION : $REGION"
echo
echo "Downloading current capabilities document..."
wget -q -O  - "${CAPABILITIES_URL}" > ${CAPABILITIES_DOC}

echo "Fetching times for layer ${LAYER}..."
#Get Times 
# python time/time_request.py -capabilities_doc ${CAPABILITIES_DOC} -layer ${LAYER} -name  > ${TIMES_FILE} 

echo "Generating tiled requests for layer ${LAYER}..."
#Generate Tiled Requests 
# python tiled/tiled_request.py -count ${REQPERGRANULE} -gridset ${GRIDSET} -gridset_dir ${GRIDSET_DIR} -region ${REGION} -levels ${LEVELS} -auxiliary_csv ${TIMES_FILE} -srs >> ${TILED_FILE}
python tiled/tiled_request.py -layer ${LAYER} -count ${REQPERGRANULE} -gridset ${GRIDSET} -gridset_dir ${GRIDSET_DIR} -region ${REGION} -levels ${LEVELS} -srs > ${TILED_FILE}

echo "Generating untiled requests for layer ${LAYER}..."
#Generate Untiled Requests (with SRS NAME)
# python untiled/wms_request.py -region  ${REGION} -maxsize ${MAXSIZE} -minsize ${MINSIZE} -maxres ${MAXRES} -minres ${MINRES} -count ${REQPERGRANULE} | awk -vd="${SRSNAME}" '{$0=$0";"d}1'  > ${UNTILED_TEMP_FILE}
python untiled/wms_request.py -region ${REGION} -maxsize ${MAXSIZE} -minsize ${MINSIZE} -maxres ${MAXRES} -minres ${MINRES} -layer ${LAYER} -count ${REQPERGRANULE} | awk -vd="${SRSNAME}" '{$0=$0";"d}1'  > ${UNTILED_FILE}
#Cartesina product with tunes file
# ./util/cartesian.sh -d ";" ${TIMES_FILE} ${UNTILED_TEMP_FILE}>> ${UNTILED_FILE}
echo "cleaning temporary files"
rm -f $TIMES_FILE
rm -f $UNTILED_TEMP_FILE
