#!/usr/bin/env bash
CONTAINER_NAME="postgresql"
TIMEOUT=5
PGUSER="postgres"
TARGET_DATABASE="osm"
DBHOST="localhost"
ENV_PATH="/home/geosolutions/compose/postgresql/.env"
LOGFILE="/var/log/geoserver/watchdog-postgres.log"
source $ENV_PATH
TEST_QUERY="SELECT NOW();"
test_pg() {
  #Check pg is working with a timeout of 5 seconds
  PGCONNECT_TIMEOUT=${TIMEOUT} PGPASSWORD=${POSTGRES_PASSWORD} psql -U $PGUSER -d $TARGET_DATABASE -h $DBHOST -c "${TEST_QUERY}" 2>&1 >> $LOGFILE
}

restart_pg() {
  docker restart ${CONTAINER_NAME}
}
capture_logs() {
  docker logs --tail 1000 $CONTAINER_NAME &>> $LOGFILE
}
check_pg_uptime() {
  #Check uptime with a timeout of 5 seconds
  UPTIME=$(PGCONNECT_TIMEOUT=${TIMEOUT} PGPASSWORD=${POSTGRES_PASSWORD} \
  psql -U $PGUSER -d $TARGET_DATABASE -h $DBHOST -c \
  "SELECT date_trunc('second', current_timestamp - pg_postmaster_start_time()) as uptime WHERE date_trunc('second', current_timestamp - pg_postmaster_start_time()) >'00:30:00';")
  CHECK_UPTIME=$(echo ${UPTIME} | grep '(0')
  if [ "${CHECK_UPTIME}" == "" ]; then
    return 0
  else
    return 100
  fi
}

# if server uptime is less than half and hour, do nothing at all
check_pg_uptime 2>&1 >> $LOGFILE

#if server uptime > 30 minutes check with a query if important data works
if [ $? -eq 0 ]; then
  test_pg
  # if query fails or psql returns an exit value different from 0, restart pg
  if [ $? -ne 0 ]; then
    echo "Dumping docker logs before restart for postgres container $CONTAINER_NAME" >> $LOGFILE
    capture_logs
    echo "Restarting postgres container $CONTAINER_NAME" >> $LOGFILE	  
    restart_pg
    echo "Restarted postgres container $CONTAINER_NAME" >> $LOGFILE
  fi
fi
