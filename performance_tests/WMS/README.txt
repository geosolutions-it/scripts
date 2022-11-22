How to use it
=============

1. Open the "test_all.jmx" test plan on JMeter and set the main parameters
   HOST
   HTTP_SCHEMA
   HTTP_PORT
   (other optional)

2. Edit the "generate_csv.sh" and set the "CAPABILITIES_URL" accordingly

3. Make sure the "tiled/gridsets/geowebcache.xml" files contains the definitions you would like to use in case of Tiled requests

4. Generate the random requests on the CSV files

    ./generate_csv.sh <layer_name> <gridset_id> "x0 x1 y0 y1" <count> <zoom_levels>

    e.g.:

    ./generate_csv.sh osm:roads EPSG:3857 "-8262132.606676765 -8122983.243185173 5681544.414062212 5741972.112518539" 5000 "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21"

5. Toggle the "Tiled" or "Untiled" controllers from the JMeter test plan, update the global settings accordingly and run the tests
