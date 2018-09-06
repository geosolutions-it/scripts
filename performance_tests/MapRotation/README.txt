This folder contains :

* **MapRotation_params.py**: a script to generate a csv with random requests parameters.  
   
  The script runs with Python 3.x versions.    

  The script requires 2 inputs:
    
    * The number of the requests that you want to perform (You can set also this number in the Loop Count in the jMeter test plan).
    * The path of your workspace followed by the name of the CSV file that you want to generate.

       It generates a file:  
       * /{your_file_name}.csv
       
       containing four columns:  1) random angle; 
                                 2) random width;
				 3) random height;
                                 3) random bbox.


* **maprotation_plan.jmx**: a jMeter test plan for WMS requests test having the angle as a parameter.  
  * You should have to adjust the HOST, PORT and the path value, e.g. C:\path\{filename}.csv and for the error file, in the Test Plan User Defined Variables.
  * Set the EPSG:id value in the Test Plan User Defined Variables.
  * Set the image format.
  * Set the layer name that you want to use for the requests in the Test Plan User Defined Variables.
   