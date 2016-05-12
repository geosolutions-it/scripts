#GEOSERVER ADMINISTRATOR CREDENTIALS
USER="admin"
PASSWORD="password"

#GEOSERVER GWC REST URL
GWCRESTURLM="http://10.50.5.150:8080/geoserver_master/gwc/rest/"
GWCRESTURL1="http://10.50.5.151:8080/geoserver/gwc/rest/"
GWCRESTURL2="http://10.50.5.152:8080/geoserver/gwc/rest/"
GWCRESTURL3="http://10.50.5.153:8080/geoserver/gwc/rest/"
GWCRESTURL4="http://10.50.5.154:8080/geoserver/gwc/rest/"

# Use the rest URL of geoserver slave 1 as default
GWCRESTURL=$GWCRESTURL1

# Use the rest URL of geoserver slave 1 as default
GWCRESTURL=$GWCRESTURL1

#THE REGEX TO PARSE
# e.g. 
# "^publiacqua\\:" All layers for publiacqua workspace
# "^publiacqua\\:fgn_allaccio_asse$" The layer publiacqua:fgn_allaccio_asse
REGEX="$1"

#HEADERS
CTYPE="Content-type: text/xml, application/x-www-form-urlencoded"
H_ACCEPT="Accept: text/xml"

#LAYER LIST SERVICE 
GWCLISTURL="${GWCRESTURL}layers/"

#GWC_DIR
GWC_DIR=/opt/geoserver-cache/

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
#checks if a dir can be deleted. return 1 if it is fine
check_dir(){
       dir=$1;
       if [[ $dir == "" ]];
        then
        echo "The directory name is an empty string" 
        return 0;
       fi
       if [[ $dir == "_gwc_in_progress_deletes_/" ]];
        then
        echo "The directory is reserved" 
        return 0;
       fi 
       if [[ $dir == "lockfiles/" ]];
        then
        echo "The directory is reserved" 
        return 0;
       fi 
       if [[ $dir == "tmp/" ]];
        then
        echo "The directory is reserved" 
        return 0;
       fi 
       return 1;
}

check_exists() {
    dir=$1;
    dir=${dir::-1}
    for (( i=0; i<${#layers[@]}; i++ ));
    do 
        layer=${layers[i]};
        layer_dir_name=${layer/:/_}
        # echo "compare $layer_dir_name with $dir"
        if [ "$layer_dir_name" == "$dir" ]; then
          echo "$layer found for $dir"
          return 1
        fi
    done;
}
confirm_delete() {
    #CONFIRM TRUNCATE
    d=$1;
    echo "$d directory is not present in GWC"
    read -r -p "Do you want to remove this directory. (y/n) " REPLY
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "deleting $GWC_DIR$d"
        rm -rf $GWC_DIR$d
        echo "deleted $d"
    else 
        echo "Skipping directory $GWC_DIR/$d"
    fi
}

# Get the list of layers from GeoServer
layers=( $(curl -s -u "${USER}:${PASSWORD}" "${GWCLISTURL}"  -H  "${CTYPE}" | xmlstarlet sel  -t -m  "layers/layer/name" -v . -n | grep "${REGEX}" ) )
echo "${#layers[@]} layers found:"
#display_layers $layers
cd $GWC_DIR
for d in */ ; do
    echo "***************"
    echo "check layer $d "
    echo "---------------"
    check_exists $d
    exist=$?
    check_dir $d
    suspect=$?
    echo $exist $suspect 
    if [[ $exist -eq 0 ]] && [[ $suspect -eq 1 ]];
        then 
            confirm_delete $d
        else 
            echo "$d exists. continue"
    fi 
done


