#! /bin/bash

# Used to find out if a specfic workspace is slowing down the global GetCapabilities request
# Needs to be able to reach the REST interface (usually admin credentials are needed)
#
# To save output on disk:
# ./time_all_getcapabilities.sh &> results.txt

curl -u username:password --silent "http://hostname:8082/geoserver/rest/workspaces.json" -o workspaces.json

while IFS== read -r name; do
    echo "Workspace = $name"
    time curl --silent "http://hostname:8082/geoserver/$name/wms?version=1.1.1&service=wms&request=GetCapabilities" -o $name.xml
    echo -e "Result = $(wc -l < $name.xml)\n\n"
done < <(jq -r '.workspaces.workspace | .[].name' workspaces.json)
