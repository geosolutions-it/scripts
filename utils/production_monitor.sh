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
# author: Lorenzo Natali lorenzo.natali#geo-solutions.it
# date: 16 Apr 2013
#
# This script monitor a directory. When some files are created
# in that directory, the current production instances are refreshed
############################################################
MONITOR_DIR=/dati/geoserver_datadir/command/
RELOAD_FILE_NAME=reload_prod
BACKUP_FILE_NAME=backup
RESTORE_FILE_NAME=restore
CLEAR_LOG_FILE=clear_log
reload_config () {
	echo "reloading production configuration..."
	./gsreload.sh
}
cd "$(dirname "$0")"
#monitor the directory  (-m option) reqursive(-r) (q is quite)
#once a file is created, the output is in the format %w%f (full path of the file) 
inotifywait -mqr --format '%w%f' -e create ${MONITOR_DIR} | while read f
do
	echo "created file $f"
	#check file for reload
	if [ "$f" == "${MONITOR_DIR}${RELOAD_FILE_NAME}" ]; then
                echo "====================================="
                date
		echo "Operation: reload  in production"
                echo "====================================="

		reload_config
		
	fi
	if [ "$f" == "${MONITOR_DIR}${BACKUP_FILE_NAME}" ]; then
                echo "===================================="
                date
		echo "Operation: Backup Data Directory"
                echo "===================================="

		./datadir_backup.sh backup
		
	fi
	if [ "$f" == "${MONITOR_DIR}${RESTORE_FILE_NAME}" ]; then
		echo "===================================="
		date
		echo "Operation: Restore last backup"
		echo "===================================="
		./datadir_backup.sh restore
		reload_config
		./gsreload_master.sh
		
	fi
	if [ "$f" == "${MONITOR_DIR}${CLEAR_LOG_FILE}" ]; then
		echo "====================================" > "${MONITOR_DIR}execution_log"
                date
                echo "Operation: CLEAR LOG"
                echo "===================================="
		
        fi

	#delete anyway the file
	rm $f -f
		
done
