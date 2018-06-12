This folder contains :

* **csv_generator_for_wmts_tests.py**: a script to generate a csv with random requests parameters.  
  
  The script requires 5 inputs:
    
    * The minimum and the maximum bounds of the level. For example, 1 and 19 (See the XML GetCapabilities to figure out the level bounds of each layer).
    * The number of the requests that you want to perform (You can set also this number in the Loop Count in the jMeter test plan).
    * The Layer Identifier, NOT the TITLE, written in quotes (e.g. 'Layer Identifier'), 
      (See the XML GetCapabilities to figure out the difference between the tiltle and identifier). 
    * The EPSG Id (e.g. 'EPSG:4326').

       It generates a file:  
       * /tilematrix.csv
       
       containing three columns: 1) random levels between the min and max bounds already setted; 
				 2) random matrix columns related to the level;
				 3) random matrix rows related to the level.


* **wmts_random_tiles_requests_plan.jmx**: a jMeter test plan for WMTS requests test.  
  * You should have to adjust the path value, C:\path\tilematrix.csv, in the Test Plan User Defined Variables.
  * Set the EPSG:id value in the Test Plan User Defined Variables.
  * Set the image format.
  * Set the layer name that you want to use for the requests in the Test Plan User Defined Variables.

