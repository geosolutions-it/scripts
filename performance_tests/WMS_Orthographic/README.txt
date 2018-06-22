This folder contains :

* **wms_orthographic_requests.py**: a script to generate a csv with random WMS requests parameters for the Orthographic projection.  
   
  The script runs with Python 3.x versions.       

  The script requires 4 inputs:
    
    * The number of the requests that you want to perform (You can set also this number in the Loop Count in the jMeter test plan).
    * The width of the viewer in pixel.
    * The height of the viewer in pixel.
    * The path of your workspace followed by the name of the CSV file that you want to generate.

       It generates a file:  
       * /{your_file_name}.csv
       
       containing 5 columns: 1) The longitute of the projection center; 
                                 2) The latitude of the projection center;
                                 3) The width of the viewer in pixel;
				 4) The height of the viewer in pixel;
				 5) The coordinates of the Bounding Box. 


* **wmts_random_tiles_requests_plan.jmx**: a jMeter test plan for WMTS requests test.  
  * You should have to adjust the path value, e.g. C:\path\tilematrix.csv, in the Test Plan User Defined Variables.
  * Set the EPSG:id value in the Test Plan User Defined Variables.
  * Set the image format.
  * Set the layer name that you want to use for the requests in the Test Plan User Defined Variables.
  * Set the test duration for each group thread in the Test Plan User Defined Variables.
  
N.B.: You should download the WMTS GetCapabilities file and place it in your workspace directory. 