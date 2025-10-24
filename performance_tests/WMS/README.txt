This package contains :

* **test_all.jmx**: a jMeter test for performance tests.  
    You should have to adjust path to files, especially for the access logs
    (see the Test Plan User Defined Variables)

* **generate_csv.sh**: a script to generate csv with requests parameters.  
   
       It generates 2 files:  
       * csv/tiled.csv
       * csv/untiled.csv
       with the tiled and untiled requests samples.   
     
       Usage:  
         ./generate_csv.sh layername gridsetname region  
       e.g.  
         ./generate_csv.sh met9:ir108 EPSG:4326_level10 "-180 -90 180 90"  
         ./generate_csv.sh met9:ir108 EPSG:3995_level10 "-1.27E7 -1.27E7 1.27E7 1.27E7"  
    

* **filter_getMap.sh**:  a script that filter an apache log to get GetMap requests.  
    
      Usage:  
        ./filter_getMap.sh <filename>  
      e.g.   
        ./filter_getMap.sh access_log > getmaps_requests  
        

* **clean_csv.sh**: an utility script that remove the csv in the csv directory.  

Other folders contain: 

* **tiled**: scripts for get tiled random requests.  
    It contain a gridset directory with the current geowebcache.xml from geoserver data dir.  
    If the gridset changes you have to update this file to make the scripts create valid sample requests.         
* **untiled**: scripts to get untiled random requests.
* **time**: scripts to get the time parameters for a layer using the capabilities document. 
* **util**: other utility scripts. 

