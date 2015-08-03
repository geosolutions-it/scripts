#!/bin/bash
#The MIT License
#
#Copyright (c) 2011 GeoSolutions S.A.S.
#http://www.geo-solutions.it
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
############################################################
# author: tobia di pisa - tobia.dipisa@geo-solutions.it
# date: 11 Oct 2013
#
# Simple GeoWebCache truncate configuration script
# Copyright 2015, GeoSolutions Sas.
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# 
############################################################

## The path of the script's log file 
LOGFILE="/opt/gwclogs/gwctruncate.log"

## The GeoWebCache REST endpoint for the truncate operation
GWCRESTURL="http://localhost:8080/geoserver/gwc/rest/seed"

## The administrator account us/pw in GeoServer
ACCOUNT="admin:geoserver"

## The Tiles GridSet to truncate
GRIDSETID="EPSG:4326"

## The Tiles GridSet to truncate
TILEFORMAT="image\/png8"

## The Tiles GridSet to truncate
ZOOMSTART=0

## The Tiles GridSet to truncate
ZOOMSTOP=21

## The list of layers and related styles to truncate
LAYERLIST="topp:states=default;topp:states=pophatch;topp:states=polygon;topp:tasmania_roads=default"

PFILTER=""

gwc_truncate()
{
	## Split layers definition in LAYERLIST
	IFS=";"
	ary=($LAYERLIST)

	for key in "${!ary[@]}";
	do
		LAYER=${ary[$key]};
		echo "LAYER: ${LAYER}";

		## Split layer name and availables styles
		IFS="="
		sts=($LAYER)
				
		LAYERNAME=${sts[0]}
		STYLE=${sts[1]}
			
		echo "STYLE: ${STYLE}"                
		echo "LAYER NAME: ${LAYERNAME}"

		if [[ "${STYLE}" != "default" ]]; then
			PFILTER="'parameters':{'entry':{'string':['STYLES', '${STYLE}']}}"
			echo "FILTER: ${PFILTER}"

			echo "Sending request body: {'seedRequest':{'name':'${LAYERNAME}','gridSetId':'${GRIDSETID}','zoomStart':'${ZOOMSTART}','zoomStop':'${ZOOMSTOP}','format':${TILEFORMAT}','type':'truncate','threadCount':4, ${PFILTER}}}" >> $LOGFILE

			echo "Sending request to the URL: ${GWCRESTURL}/${LAYERNAME}.json" >> $LOGFILE

			curl -v -u ${ACCOUNT} -XPOST -H "Content-type: application/json" -d "{'seedRequest':{'name':'${LAYERNAME}','gridSetId':'${GRIDSETID}','zoomStart':'${ZOOMSTART}','zoomStop':'${ZOOMSTOP}','format':'${TILEFORMAT}','type':'truncate','threadCount':4, ${PFILTER}}}" "${GWCRESTURL}/${LAYERNAME}.json"
			
		else
			echo "Truncating only the Default style Tiles for Layer: ${LAYERNAME}" >> $LOGFILE
		
			echo "Sending request body: {'seedRequest':{'name':'${LAYERNAME}','gridSetId':'${GRIDSETID}','zoomStart':'${ZOOMSTART}','zoomStop':'${ZOOMSTOP}','format':${TILEFORMAT}','type':'truncate','threadCount':4}}" >> $LOGFILE

			echo "Sending request to the URL: ${GWCRESTURL}/${LAYERNAME}.json" >> $LOGFILE

			curl -v -u ${ACCOUNT} -XPOST -H "Content-type: application/json" -d "{'seedRequest':{'name':'${LAYERNAME}','gridSetId':'${GRIDSETID}','zoomStart':'${ZOOMSTART}','zoomStop':'${ZOOMSTOP}','format':'${TILEFORMAT}','type':'truncate','threadCount':4}}" "${GWCRESTURL}/${LAYERNAME}.json"
		fi
	done

	return $?
}

if [ ! -e "$LOGFILE" ]; then
	LOGFILE="/dev/stdout"
	echo "`date` Output file: DOES NOT EXIST: using ${LOGFILE}" >> "${LOGFILE}"
else
	echo "`date` Setting output to: ${LOGFILE}" >> "${LOGFILE}"
fi

gwc_truncate

## Testing on gwc_truncate exit code
if [ "$?" -eq 0 ] ; then
	echo "`date` GeoWebCache Truncate Status: OK " >> $LOGFILE
	exit 0;
else
	echo "`date` GeoWebCache Truncate Status: FAIL " >> $LOGFILE
fi

done

echo "`date` GeoWebCache Truncate Action: FAILED (WHAT's HAPPENING? -> exit (status: 100))" >> "${LOGFILE}"
exit 100
