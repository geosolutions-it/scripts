#!/bin/bash

# Simple scripts to backup CKAN databases
# The script will keep the 'KEEP_NUM' most recent backups and delete
# all others.

# DB backup output file
OUT_DIR=/usr/lib/ckan/backups

# Log file path
LOGFILE="/var/log/ckan/backup.log"

# How many backups to keep
KEEP_NUM=3

if [ ! -e "$LOGFILE" ]
then
    echo "[INFO] Creating logfile $LOGFILE"
    touch $LOGFILE
    if [ "$?" -ne "0" ]
    then
        echo "[ERR] Cannot create logfile: $LOGFILE" 1>&2
	exit 1
    fi
fi

# date format function
date_utc()
{
# Get current date in UTC (YYYY-MM-DDTHH:MM:SS-UTC)
DATE=`date -u +%Y-%m-%dT%H:%M:%S-UTC`
}

# Log functions
log_info()
{
date_utc
echo "[$DATE][INFO] $1" | tee -a $LOGFILE
}

log_error()
{
date_utc
echo "[$DATE][ERR] $1" | tee -a $LOGFILE
}

date_utc
# Ouput file name (Do not change this)
OUT_FILENAME_CKAN="ckan_backup-$DATE.sql"
OUT_FILENAME_DATASTORE="datastore_backup-$DATE.sql"
OUT_FILENAME_GZ="backup-$DATE.gz"

log_info "### Backup script Sarted"

if [ ! -d "$OUT_DIR" ]
then
    log_info "Backup folder does not exist"
    mkdir "$OUT_DIR"
    if [ "$?" -ne "0" ]
    then
	log_error "Unable to create output folder: $OUT_DIR"
	exit 1
    fi
fi

# listing existing backup files
existing_backups=`ls $OUT_DIR/*backup*`
declare -a backups=($existing_backups)
#printf "%s\n" "${backups[@]}"
log_info "Existing backups in folder $OUT_DIR:"
date_utc
i=0
for file in $existing_backups
do
    # extracting date from file
    file_date=`echo $file | cut -f2- -d'-' | cut -f1 -d'.'`
    secs_now=`date --utc --date "$DATE" +%s`
    secs_file=`date --utc --date "$file_date" +%s`
    diff_secs=$(( secs_now-secs_file ))
    log_info "`basename $file` date: $file_date age: $(( diff_secs/60 )) min"
    backups_age[$i]=$diff_secs
    i=$(( i+1 ))
done
#printf "%s\n" "${backups_age[@]}"
tot_backups="${#backups[@]}"
log_info "Total existing backups: $tot_backups" 

to_delete=$(( tot_backups-KEEP_NUM  ))
if [ "$to_delete" -gt "0" ]
then
    log_info "Number of backups to delete: $to_delete"
fi

exchange_backups()
{
    temp=${backups[$1]}
    backups[$1]=${backups[$2]}
    backups[$2]=$temp
}


exchange_ages()
{
    temp=${backups_age[$1]}
    backups_age[$1]=${backups_age[$2]}
    backups_age[$2]=$temp
}

for i in $(seq 1 $to_delete)
do
    j=0
    max_age=0
    oldest=-1
    for age in "${backups_age[@]}"
    do
        if [ "$age" -gt "$max_age" ]
        then
	    oldest="$j"
	    echo "new oldest: $oldest"
	    max_age=$age
	    echo "new age: $max_age"
        fi
        j=$(( j+1 ))
    done
    log_info "Deleting backup file ${backups[$oldest]} of age $(( backups_age[$oldest]/60 ))"
    rm -f ${backups[$oldest]} 
    if [ "$?" -ne "0" ]
    then
       log_error "Cannot delete old backup file:${backups[$oldest]}"
    fi
    # Updae array
    backups[$oldest]="deleted"
    backups_age[$oldest]="0"
done

# Stop CKAN and PostgreSQL
systemctl stop supervisord

# Restart CKAN and PostgreSQL
systemctl start supervisord

OUT_CKAN="$OUT_DIR/$OUT_FILENAME_CKAN"
log_info "Backing up database ckan to file: $OUT_CKAN"
pg_dump -U ckan ckan -f"$OUT_CKAN" 1>&2 | tee -a $LOGFILE
if [ "$?" -ne "0" ]
then
    log_error "Database 'ckan' backup creation failed with exit status: $?"
    exit 1
else
    log_info "Created backup of database 'ckan' with size: `du -h $OUT_CKAN`"
fi

OUT_DATASTORE="$OUT_DIR/$OUT_FILENAME_DATASTORE"
log_info "Backing up database ckan to file: $OUT_DATASTORE"
pg_dump -U ckan datastore -f"$OUT_DATASTORE" 1>&2 | tee -a $LOGFILE
if [ "$?" -ne "0" ]
then
    log_error "Database 'datastore' backup creation failed with exit status: $?"
    exit 1
else
    log_info "Created backup of database 'datastore' with size: `du -h $OUT_DATASTORE`"
fi

OUT_GZ="$OUT_DIR/$OUT_FILENAME_GZ"
log_info "Creating compressed archive"
tar cvzf $OUT_GZ $OUT_CKAN $OUT_DATASTORE
if [ "$?" -ne "0" ]
then
    log_error "Backup archive creation failed with exit status: $?"
    exit 1
else
    log_info "Created backup archive of size: `du -h $OUT_GZ`"
fi

log_info "Removing temprary .sql files..."
rm -f $OUT_CKAN $OUT_DATASTORE
if [ "$?" -ne "0" ]
then
    log_error "Deletion of temporary .sql files failed with exit status: $?"
    exit 1
fi

log_info "### Backup script Finished without errros"
exit 0
