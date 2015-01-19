#!/bin/bash
#
##############################################################################
# This script allows to call the masstruncate functionality of GeoWebCache for 
# all the layers that match specific regex
# Usage: 
# cleancache.sh regex
# e.g. 
# cleancache.sh "^topp\\:"
# cleancache.sh "^topp\\:states$"
# If regex not present use the standard input to clear layers
##############################################################################
 
#GEOSERVER ADMINISTRATOR CREDENTIALS
USER="admin"
PASSWORD="geoserver"

#GEOSERVER GWC REST URL
GWCRESTURLM="http://10.50.5.150:8080/geoserver_master/gwc/rest/"
GWCRESTURL1="http://10.50.5.151:8080/geoserver/gwc/rest/"
GWCRESTURL2="http://10.50.5.152:8080/geoserver/gwc/rest/"
GWCRESTURL3="http://10.50.5.153:8080/geoserver/gwc/rest/"
GWCRESTURL4="http://10.50.5.154:8080/geoserver/gwc/rest/"

# Use the rest URL of geoserver slave 1 as default
GWCRESTURL=$GWCRESTURL1

#THE REGEX TO PARSE
# e.g. 
# "^topp\\:" All layers for topp workspace
# "^topp\\:states$" The layer topp:states
REGEX="$1"

#HEADERS
CTYPE="Content-type: text/xml, application/x-www-form-urlencoded"
H_ACCEPT="Accept: text/xml"

#LAYER LIST SERVICE 
GWCLISTURL="${GWCRESTURL}layers/"
echo "*************************************************************************"
echo "**** GEOWEBCACHE CLEAN TOOL *********************************************"
echo "*************************************************************************"
echo "This tool helps to do a full tile cache clean (called Mass Truncate) for "
echo "a group of layers identified by a regex passed as argument."
echo "Quering layers to truncate at :"
echo "   ${GWCLISTURL}"
echo "*************************************************************************"

# NOTE: because of this issue: http://sourceforge.net/p/xmlstar/bugs/54/
# we use "-m query -v ." instead of "-v query" as suggested here : http://sourceforge.net/p/xmlstar/bugs/54/#e70c

usage () {
    progname=$(basename "$0")
    echo "Usage: $progname regex"
    echo "Please specify a regex as argument"
}

################################################################################
# clear_layers()
# Uses the GeoServer REST interface to clear cache to many GeoServer cluster 
# instances
################################################################################
clear_layers(){
    layers=$1
    for (( i=0; i<${#layers[@]}; i++ ));
    do 
        layer=${layers[i]};
          echo "* cleaning cache for layer : ${layer}";
          echo -ne "${layer} ----- (1/5)\r"
          curl -s -u "${USER}:${PASSWORD}"   -H  "${CTYPE}" -H "Accept: */*"  -H "Connection: keep-alive" --data-binary "<truncateLayer><layerName>${layer}</layerName></truncateLayer>" "${GWCRESTURLM}masstruncate/" > /dev/null
          echo -ne "${layer} x---- (2/5)\r"
          curl -s -u "${USER}:${PASSWORD}"   -H  "${CTYPE}" -H "Accept: */*"  -H "Connection: keep-alive" --data-binary "<truncateLayer><layerName>${layer}</layerName></truncateLayer>" "${GWCRESTURL1}masstruncate/" > /dev/null
          echo -ne "${layer} xx--- (3/5)\r"
          curl -s -u "${USER}:${PASSWORD}"   -H  "${CTYPE}" -H "Accept: */*"  -H "Connection: keep-alive" --data-binary "<truncateLayer><layerName>${layer}</layerName></truncateLayer>" "${GWCRESTURL2}masstruncate/" > /dev/null
          echo -ne "${layer} xxx-- (4/5)\r"
          curl -s -u "${USER}:${PASSWORD}"   -H  "${CTYPE}" -H "Accept: */*"  -H "Connection: keep-alive" --data-binary "<truncateLayer><layerName>${layer}</layerName></truncateLayer>" "${GWCRESTURL3}masstruncate/" > /dev/null
          echo -ne "${layer} xxxx- (5/5)\r"
          curl -s -u "${USER}:${PASSWORD}"   -H  "${CTYPE}" -H "Accept: */*"  -H "Connection: keep-alive" --data-binary "<truncateLayer><layerName>${layer}</layerName></truncateLayer>" "${GWCRESTURL4}masstruncate/" > /dev/null
          echo -ne "${layer} xxxxx (5/5)\r"
          echo -ne '\n'
        echo
    done;
}
################################################################################
# display_layers()
# Show the list of layers found using the regex
################################################################################
display_layers(){
    layers=$1
    for (( i=0; i<${#layers[@]}; i++ ));
    do 
        echo "  ${layers[i]}"
    done
}


################################################################################
# SCRIPT START
################################################################################

# test if argument passed
if [ $# -le 0 ]; then 
    # Not interactive mode read from stdin the layers
    while read line
    do
        layers=("${layers[@]}" $line)
    done
echo "*************************************************************************"
echo " Layers To Empty "
echo "*************************************************************************"
    display_layers $layers
echo "*************************************************************************"
    clear_layers $layers
    exit
fi

# Filter with regex
echo "*************************************************************************"
echo "Fitler with REGEX:"
echo "   ${REGEX}"
echo "*************************************************************************"
# Get the list of layers from GeoServer
layers=( $(curl -s -u "${USER}:${PASSWORD}" "${GWCLISTURL}"  -H  "${CTYPE}" | xmlstarlet sel  -t -m  "layers/layer/name" -v . -n | grep "${REGEX}" ) )
echo "${#layers[@]} layers found:"
display_layers $layers  

#CONFIRM TRUNCATE
read -r -p "Do you want to clear cache for these layers? (y/n) " REPLY
if [[ $REPLY =~ ^[Yy]$ ]]
then
    clear_layers $layers
    echo "END OF CACHE CLEAN"
else 
    echo "Exiting..."
fi
