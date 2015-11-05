#!/bin/bash

HARVEST_FOLDER=/var/data/ftp/update
ZIP_FILE=/upload/data.zip

# script used for processing tiffs
SCRIPT_PATH=/var/data/gisdata/coverage/warp.py
# logfile
LOGFILE=$HARVEST_FOLDER/harvest.log 
# where to put processed tiffs
GISDATA=/var/data/gisdata

# Shapefile-Layers association CSV file
CSV_FILE=$HARVEST_FOLDER/csv_ingestion
# databese ip or host
DBHOST=123.123.123.123
#username and password to connect to DB
DBUSER=dbuser
DBPASS=dbpass

#user and password for GeoServer Harvesting
user=""
password=""

rm $LOGFILE
touch $LOGFILE
if [ "$?" -ne 0 ]
then
   echo "cannot create logfile $LOGFILE" 
   exit 1
fi
chmod 777 $LOGFILE

cd $HARVEST_FOLDER  
if [ "$?" -ne 0 ]
then
   echo "cannot cd into $HARVEST_FOLDER" >> $LOGFILE 
   exit 1
fi

### Raster data ingestion ###
echo "### Processing Raster Data ###" >> $LOGFILE

if [ ! -e $HARVEST_FOLDER/$ZIP_FILE ]
then
    echo "data file not found! .. exiting" >> $LOGFILE
    exit 1
fi

unzip -o $HARVEST_FOLDER/$ZIP_FILE -d $HARVEST_FOLDER/new_data_tmp

if [ "$?" -ne 0 ]
then
   echo "error extracting $HARVEST_FOLDER/$ZIP_FILE ..exiting" >> $LOGFILE 
   exit 1
fi

pushd .
cd $HARVEST_FOLDER/new_data_tmp/...
files=`find . -name *.tif | xargs`
for file in $files
do
	echo "Processing $file" >> $LOGFILE
 	tmpdir=$(dirname $file)
 	filename=$(basename $file)
 	warped="warped/$tmpdir"
 	translated="translated/$tmpdir"
 	mkdir -p $warped
 	mkdir -p $translated
 	gdalwarp $file "$warped/$filename" -t_srs EPSG:4326
 	gdal_translate -co "TILED=YES" -co "BLOCKXSIZE=512" -co "BLOCKYSIZE=512" "$warped/$filename" "$translated/$filename"
 	gdaladdo -r cubic "$translated/$filename" 2 4 8 16 32 64 128 
 	mkdir -p $GISDATA/.../$tmpdir
 	mv $translated/$filename $GISDATA/.../$tmpdir/$filename < y
 	chown -R tomcat7:tomcat7 $GISDATA/.../$tmpdir/$filename
 	abspath=$(realpath $GISDATA/coverage/.../$tmpdir/$filename)
 	echo "Ingestion of file: $file" >> $LOGFILE
 	curl -v -u $user:$password -XPOST -H "Content-type: text/plain" -d "file://$abspath" "http://localhost:8080/geoserver/rest/.../external.imagemosaic"	
done
 
rm -rf ./warped ./translated
 
 
 cd $HARVEST_FOLDER/new_data_tmp/...
 files=`find . -name *.tif | xargs`
 for file in $files
 do
 	echo "Processing $file" >> $LOGFILE
        tmpdir=$(dirname $file)
        filename=$(basename $file)
        warped="warped/$tmpdir"
        translated="translated/$tmpdir"
        mkdir -p $warped
        mkdir -p $translated
        gdalwarp $file "$warped/$filename" -t_srs EPSG:4326
        gdal_translate -co "TILED=YES" -co "BLOCKXSIZE=512" -co "BLOCKYSIZE=512" "$warped/$filename" "$translated/$filename"
        gdaladdo -r cubic "$translated/$filename" 2 4 8 16 32 64 128
        mkdir -p $GISDATA/.../$tmpdir
	mv $translated/$filename $GISDATA/.../$tmpdir/$filename < y
	chown -R tomcat7:tomcat7 $GISDATA/.../$tmpdir/$filename
	abspath=$(realpath $GISDATA/coverage/.../$tmpdir/$filename)
	echo "Ingestion of file: $file" >> $LOGFILE
        curl -v -u $user:$password -XPOST -H "Content-type: text/plain" -d "file://$abspath" "http://localhost:8080/geoserver/rest/..../external.imagemosaic"
done
 
rm -rf ./warped ./translated
 
popd
# fix permissions
chown -R tomcat7 $GISDATA/coverage
#
echo "### Processing Raster Data Finished  ###" >> $LOGFILE

### Vector data ingestion ###
echo "### Processing Vector Data ###" >> $LOGFILE

# CSV file with <shapefile - layer> associations
echo "Opening CSV file: $CSV_FILE" >> $LOGFILE
if [ ! -f $CSV_FILE ]
then
    echo "$CSV_FILE file not found" >> $LOGFILE
    exit 1
fi

# parse CSV file
COUNT=0
OLDIFS=$IFS
IFS=,
while read shapefile layer opts
do
    # skip comments, blank lines and lines statting with " "
    if [[ "$shapefile" = \#* || "$shapefile" = \ * || -z $shapefile ]]
    then
    continue
    fi
    Shapefiles[$COUNT]=$shapefile
    Layers[$COUNT]=$layer
    Opts[$COUNT]=$opts
    ((COUNT++))
done < $CSV_FILE
IFS=$OLDIFS

echo "Read $COUNT lines from $CSV_FILE" >> $LOGFILE

# Get list of shapefiles to ingest

files=`find $HARVEST_FOLDER/new_data_tmp/shp/ -name *.shp | xargs`
echo $files
# ingest shapefiles according to directions in CSV file
for file in $files
do
    found="false"
    bname=$(basename $file)
    echo "Ingesting shapefile $file" >> $LOGFILE
    # check shapefile name against the array
    for ((i=0; i < $COUNT; i++))
    do
        if [ "$bname" == "${Shapefiles[$i]}" ]
        then
	    echo "Processing Vector: $file" >> $LOGFILE
            ogr2ogr -f "PostgreSQL" PG:"host=$DBHOST user=$DBUSER dbname=dbname password=$DBPASS" $HARVEST_FOLDER/new_data_tmp/shp/${Shapefiles[$i]} -nln ${Layers[$i]} ${Opts[$i]}
            found="true"

	    # truncating cache
	    echo "Truncating cache for Layer: ${Layers[$i]}" >> $LOGFILE
            ./gwc.sh masstruncate dbname:${Layers[$i]} -a $user:$password -u http://localhost:8080/geoserver/gwc/rest
            break
        fi
    done
    if [ "$found" == "false" ]
    then
        echo "Error processing Vector: unknown shapefile \"$file\", ignoring it..." >> $LOGFILE
    fi
done

echo "### Processing Vector Data Finished  ###" >> $LOGFILE

echo "cleanup... removing temporary files" >> $LOGFILE
echo "deleting temporary files and zip file" >> $LOGFILE
rm -rf $HARVEST_FOLDER/new_data_tmp/* $HARVEST_FOLDER/upload/data.zip

exit 0
