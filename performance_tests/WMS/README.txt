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

    ./generate_csv.sh <layer_name> <gridset_id> "x0 x1 y0 y1" <count>

    e.g.:

    ./generate_csv.sh osm:osm_roads EPSG:4326 "-79.76 -57.10 44.99 62.59" 100

5. Toggle the "Tiled" or "Untiled" controllers from the JMeter test plan and run the tests
