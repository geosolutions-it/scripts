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
# author: carlo cancellieri - ccancellieri@geo-solutions.it
# date: 7 Apr 2011
#
# simple watchdog for webservice
############################################################

# the url to use to test the service
URL=http://90.147.39.246/geoserver/styles/default_point.sld
#URL=http://10.20.2.4:8080/ergorr/
#URL=http://10.20.2.4:9090/geobatch/
#URL=http://localhost:8080/ergorr/

#set the connection timeout (in seconds)
TIMEOUT=30

# seconds to wait to recheck the service (this is not cron)
# tomcat restart time
TOMCAT_TIMEOUT=50

# used to filter the process (to get the pid)
# use: ps -efl
# to see what you have to filter
FILTER="GEOSERVER_DATA_DIR"
#FILTER="GEOBATCH_DATA_DIR"
#FILTER="buddata"

# the service to restart
# should be a script placed here:
# /etc/init.d/
# 
SERVICE="tomcat"

# the output file to use as log
# must exists otherwise the stdout will be used
# NOTE: remember to logrotate this file!!!
LOGFILE="/var/tomcat/server_1/logs/watchdog.log"

# maximum tries to perform a quick restart
# when the service fails to be started a quick (30 sec)
# restart will be tried at least $RETRY times
# if restart fails RETRY times  the script ends returning '100'
RETRY=3

################### WATCHDOG #####################

times=0;

if [ ! -e "$LOGFILE" ]; then
	LOGFILE="/dev/stdout"
	echo "`date` WatchDog output file: NOT EXISTS using: ${LOGFILE}" >> "${LOGFILE}"
else
	echo "`date` WatchDog setting output to: ${LOGFILE}" >> "${LOGFILE}"
fi


#loop
while [ "$times" -lt "$RETRY" ]
do
	#try to access tomcat's page
	wget -O - -T "${TIMEOUT}" -o "/dev/null" --proxy=off ${URL} >> "${LOGFILE}" 2>&1
	#decide on reply
	if [ "$?" -eq 0 ]; then
		echo "`date` WatchDog Status: OK -> tomcat is responding at URL: ${URL}" >> "${LOGFILE}" 
		exit 0;
	else
		echo "`date` WatchDog Status: BAD -> tomcat do NOT respond (URL: ${URL})" >> "${LOGFILE}"
		echo "`date` WatchDog Action: Stopping service ${buddata}" >> "${LOGFILE}"

		PIDFILE=`/etc/init.d/${SERVICE} stop |awk '/PID/{gsub(".*[(]","",$0);gsub("[)].*","",$0); print $0}'`
		if [ -e "$PIDFILE" ]; then
			echo "`date` removing pid file: $PIDFILE" >> "${LOGFILE}"
			rm "$PIDFILE" >> "${LOGFILE}" 2>&1
		fi
		sleep 1

		for thepin in `ps -efl | awk -v FILTER="${FILTER}" '!/awk/&&/org.apache.catalina.startup.Bootstrap/{if ($0 ~ FILTER) {print $4}}'`; do
			echo "`date` WatchDog Action: Stop failed -> killing service ${buddata} (pid: ${thepin})" >> "${LOGFILE}"
			kill -15 "${thepin}" >> "${LOGFILE}" 2>&1
			sleep "$TIMEOUT"
			while [ "${thepin}" = "`ps -efl | awk -v FILTER="${FILTER}" '!/awk/&&/org.apache.catalina.startup.Bootstrap/{if ($0 ~ FILTER) {print $4}}'`" ];
			do 
				echo "`date` WatchDog Action: killing failed -> Re-killing service $buddata (pid: ${thepin})" >> "${LOGFILE}"
				kill -9 "${thepin}" >> "${LOGFILE}" 2>&1
				sleep "$TIMEOUT"
			done
		done

		echo "`date` WatchDog Action: Starting service ${buddata}" >> "${LOGFILE}"

		/etc/init.d/${SERVICE} start >> "${LOGFILE}" 2>&1
		if [ "$?" -eq 0 ]; then
			echo "`date` WatchDog Action: service ${buddata} STARTED" >> "${LOGFILE}"
			times=`expr "$times" "+" "1"`
			# give tomcat time to start
			sleep "$TOMCAT_TIMEOUT"
			# let's retest the connection STILL NOT RETURN
		elif [ "$?" -eq 1 ]; then
			times=`expr "$times" "+" "1"`
			echo "`date` WatchDog Action: service ${buddata} ALREADY STARTED (WHAT'S HAPPENING? -> quick retry (try: $times of: $RETRY))" >> "${LOGFILE}"
			# give tomcat time to start
			sleep "$TOMCAT_TIMEOUT"
		else
			times=`expr "$times" "+" "1"`
			echo "`date` WatchDog Action: Starting service FAILED ${buddata} (WHAT'S HAPPENING? -> quick retry (try: $times of: $RETRY))" >> "${LOGFILE}"
			# give tomcat time to start
			sleep "$TOMCAT_TIMEOUT"
		fi
	fi
done
echo "`date` WatchDog Action: Starting service FAILED ${buddata} (WHAT's HAPPENING? -> exit (status: 100))" >> "${LOGFILE}"
return 100
