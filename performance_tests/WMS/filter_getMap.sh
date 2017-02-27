 cat $1 | grep '\(geoserver\/\)\(wms\|wfs\|ows\)' | grep -i  "request=getmap"
