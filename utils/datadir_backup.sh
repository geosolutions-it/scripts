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
# author: Lorenzo Natali - lorenzo.natali@geo-solutions.it
# date: 28 Feb 2014
#
# Simple GeoServer data dir backup/restore
############################################################
DATA_DIR=/var/lib/geoserver/config/
BACKUP_DIR=/home/toor/backups/
BACKUP_FILE_NAME=data_dir.tar.gz

gs_data_dir_dump()
{  
   local old_dir=`pwd`
   cd ${DATA_DIR} 
   echo "creating backup file  ${BACKUP_DIR}${BACKUP_FILE_NAME} from ${DATA_DIR}..."
   tar -czf ${BACKUP_DIR}${BACKUP_FILE_NAME} .
   cd $old_dir	   
   return $?
}

gs_data_dir_restore()
{  
   gs_data_dir_clean
   local old_dir=`pwd`
   cd ${DATA_DIR} 
   echo "extracting backup file  ${BACKUP_DIR}${BACKUP_FILE_NAME} into ${DATA_DIR} ..."
   tar -xzf ${BACKUP_DIR}${BACKUP_FILE_NAME} -C ${DATA_DIR}
   cd $old_dir	   
   return $?
}

gs_data_dir_clean()
{  
   cd ${DATA_DIR} 
   echo "cleaning  ${DATA_DIR} ..."
   rm -rf ${DATA_DIR}/*   
   return $?
}

if [ -z "$1" ]
  then
    echo "allowed argument : backup,restore"
    exit
fi

case "$1" in
backup) 
	gs_data_dir_dump
	echo "backup finished"
	exit;
   	;;
restore)
	# move the old directory 
	mv ${DATA_DIR} ${BACKUPDIR}moved
	#remove the old data dir
	rm -Rf ${BACKUPDIR}moved
	mkdir ${DATA_DIR}
   	gs_data_dir_restore
	echo "restore finished"
	exit
	;;
*) echo "allowed arguments: backup,restore"
   ;;
esac
