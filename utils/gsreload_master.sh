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
# date: 16 Apr 2013
#
# Simple GeoServer configuration reload script
############################################################

# the url to use to test the service
# !make sure to implement the url_test logic also into the bottom function
URL="http://localhost:8080/geoserver_master/rest/reload"

ACCOUNT="admin:L*Comune"

# the output file to use as log
# must exists otherwise the stdout will be used
# NOTE: remember to logrotate this file!!!
LOGFILE="/var/log/gsreload.log"

# maximum tries to perform a quick restart
# when the request fails another request will be tried at least $RETRY times
# if the new request fails RETRY times the script ends returning '100'
RETRY=1

################### RELOAD GEOSERVER CONFIGURATION  #####################

reload_config()
{
   curl -XPOST -u ${ACCOUNT} ${URL} > "${LOGFILE}"

   return $?
}


times=0;

if [ ! -e "$LOGFILE" ]; then
	LOGFILE="/dev/stdout"
	echo "`date` Output file: DOES NOT EXIST: using ${LOGFILE}" >> "${LOGFILE}"
else
	echo "`date` Setting output to: ${LOGFILE}" >> "${LOGFILE}"
fi


#loop
while [ "$times" -lt "$RETRY" ]
do
  	reload_config

    #testing on reload_config exit code
	if [ "$?" -eq 0 ] ; then
		echo "`date` GeoServer Reload Status: OK -> $SERVICE is responding at URLs" >> $LOGFILE
		exit 0;
	else
		echo "`date` GeoServer Reload Status: FAIL -> $SERVICE is NOT responding properly at URLs" >> $LOGFILE
	fi
done
echo "`date` GeoServer Reload configuration Action: FAILED (WHAT's HAPPENING? -> exit (status: 100))" >> "${LOGFILE}"
exit 100
