This script parses the geoserver audit logs files.

### DIRECTORY

The script can list logs of a one or multiple directories using the `--directory` argument or `-d`

```
tomcat@wms-geoserver-slave-set-0:/var/geoserver/audits$ ./parser.py --directory "geoserver-wms-geoserver-slave-set-0-Slave/, geoserver-wms-geoserver-slave-set-1-Slave/" 
Level  Starttime                          Remoteaddr               Operation                Errormessage                                    
----------------------------------------------------------------------------------------------------------------------------------------------
Parsing file: geoserver-wms-geoserver-slave-set-0-Slave/geoserver_audit_20240830_190073.log
info   2024-08-30T14:10:07.182Z           85.131.101.113           GetCapabilities                                                          
info   2024-08-30T14:10:06.029Z           212.128.98.139           dispatch                                                                 
info   2024-08-30T14:10:05.804Z           176.116.124.187          dispatch                                                                 
info   2024-08-30T14:10:04.059Z           10.42.20.84              GetMap                                                                   
info   2024-08-30T14:10:05.663Z           10.12.81.202                                                                                      
info   2024-08-30T14:10:05.663Z           10.12.81.202                                                                                      
info   2024-08-30T14:10:04.503Z           10.42.20.84              GetMap                                                                   
info   2024-08-30T14:10:04.498Z           10.42.20.84              GetMap                                                                   
info   2024-08-30T14:10:04.5Z             10.42.20.84              GetMap   
```

### SINCE

The script can also list logs of the minutes/hours/days using the `--since` argument or `-s` followed with time unit (m: for minutes, h: for hours, d: for days).

```
$ ./parser.py --directory geoserver-wms-geoserver-slave-set-6-Slave  --since 1m 
Level  Starttime                          Remoteaddr               Operation                Errormessage                                
----------------------------------------------------------------------------------------------------------------------------------------------
Parsing file: geoserver-wms-geoserver-slave-set-6-Slave/geoserver_audit_20240830_185008.log
info   2024-08-30T14:42:59.337Z           197.253.114.164          dispatch                                                             
info   2024-08-30T14:42:59.208Z           3.29.54.48               dispatch                                                             
info   2024-08-30T14:42:59.048Z           80.249.72.62             dispatch                                                             
info   2024-08-30T14:42:59.044Z           80.249.72.62             dispatch                                                             
info   2024-08-30T14:42:58.341Z           46.1.136.47              GetFeatureInfo                                                       
info   2024-08-30T14:42:58.08Z            212.35.78.65             dispatch                                                             
info   2024-08-30T14:42:57.455Z           197.214.13.151           dispatch  
```

### LIMIT

Also it is possible to use the `--limit` or `-l` argument to limit the logs to specific number of lines.

```
$ ./parser.py --directory geoserver-wms-geoserver-slave-set-6-Slave  --limit 4
Level  Starttime                          Remoteaddr               Operation                Errormessage                              
----------------------------------------------------------------------------------------------------------------------------------------------
Parsing file: geoserver-wms-geoserver-slave-set-6-Slave/geoserver_audit_20240830_185008.log
info   2024-08-30T14:44:00.021Z           93.46.165.165            GetMap                                                             
info   2024-08-30T14:44:00.161Z           193.137.20.13            dispatch                                                           
info   2024-08-30T14:43:59.933Z           93.46.165.165            GetMap                                                             
info   2024-08-30T14:43:59.745Z           93.46.165.165            GetMap 
```

### ERRORS ONLY

The `--errors-only` or `-e` flag is also added to print errors only.

```
$ ./parser.py --directory geoserver-wms-geoserver-slave-set-0-Slave  --since 10m --limit 10 --errors-only
Level  Starttime                          Remoteaddr               Operation                Errormessage                                  
----------------------------------------------------------------------------------------------------------------------------------------------
Parsing file: geoserver-wms-geoserver-slave-set-0-Slave/geoserver_audit_20240830_190080.log
error  2024-08-30T14:46:07.195Z           10.42.32.221                                      Invalid date: 2024-8-30T14:15:0:00.000Z       
error  2024-08-30T14:46:07.097Z           10.42.32.221                                      Invalid date: 2024-8-30T14:15:0:00.000Z       
error  2024-08-30T14:46:06.599Z           10.42.32.221                                      Invalid date: 2024-8-30T14:15:0:00.000Z       
error  2024-08-30T14:46:06.497Z           10.42.32.221                                      Invalid date: 2024-8-30T14:15:0:00.000Z       
error  2024-08-30T14:46:06.402Z           10.42.32.221                                      Invalid date: 2024-8-30T14:15:0:00.000Z       
error  2024-08-30T14:46:06.401Z           10.42.32.221                                      Invalid date: 2024-8-30T14:15:0:00.000Z       
error  2024-08-30T14:46:06.401Z           10.42.32.221                                      Invalid date: 2024-8-30T14:15:0:00.000Z
```

### FIELDS

By default, the script return five (5) default fields. The log level, timestamp, sourceIP, type of request and error message. However additional fields can be added using the `--fields` or `-f` flag.

```
$ ./parser.py --directory geoserver-wms-geoserver-slave-set-0-Slave  --since 10m --limit 10  --fields path,layer
Level  Starttime                          Remoteaddr               Operation                Errormessage                                      Path                     Layer                
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parsing file: geoserver-wms-geoserver-slave-set-0-Slave/geoserver_audit_20240830_190080.log
info   2024-08-30T14:47:23.017Z           85.76.50.190             GetCapabilities                                                            /msg_fes/rgb_convection/wms                     
info   2024-08-30T14:47:22.806Z           77.111.247.58            GetMap                                                                     /msg_fes/wms             msg_fes:rdt          
info   2024-08-30T14:47:21.959Z           51.255.198.134           GetMap                                                                     /ows                     osmgray:ne_10m_bathymetry, osmgray:simplified_land_polygons, osmgray:land_polygons, osmgray:builtup_area, osmgray:waterareas, osmgray:waterways, msg_fes:rgb_eview, backgrounds:ne_10m_coastline, osmgray:ne_10m_admin_1_states_provinces_lines, osmgray:ne_10m_admin_0_boundary_lines_land
info   2024-08-30T14:47:21.666Z           94.65.88.90              dispatch                                                                   /gwc/service/wmts                             
info   2024-08-30T14:47:21.377Z           94.65.88.90              GetMap                                                                     /msg_fes/wms             msg_fes:rgb_airmass  
info   2024-08-30T14:47:21.008Z           94.65.88.90              GetMap                                                                     /msg_fes/wms             msg_fes:rgb_airmass  
info   2024-08-30T14:47:19.668Z           94.65.88.90              GetMap                                                                     /msg_fes/wms             msg_fes:rgb_airmass  
info   2024-08-30T14:47:19.524Z           131.228.2.16             GetCapabilities                                                            /msg_fes/rgb_convection/wms                     
info   2024-08-30T14:47:19.505Z           197.253.114.66           dispatch                                                                   /gwc/service/wmts                             
info   2024-08-30T14:47:19.132Z           185.44.145.1             GetMap                                                                     /msg_fes/wms             msg_fes:rdt 
```

The list of supported fields can be found using the `--help` flag.

```
tomcat@wms-geoserver-slave-set-0:/var/geoserver/audits$ ./parser.py --help
usage: parser.py [-h] [-e] [-s SINCE] [-d DIRECTORY] [-f FIELDS] [-t] [--ip IP] [-l LIMIT]

Parse and highlight errors/warnings in a CSV log file.

optional arguments:
  -h, --help            show this help message and exit
  -e, --errors-only     Only display errors from the log file
  -s SINCE, --since SINCE
                        Filter files modified within this time period (e.g., '15m' for 15 minutes)
  -d DIRECTORY, --directory DIRECTORY
                        Path to the directory containing log files
  -f FIELDS, --fields FIELDS
                        Comma-separated list of additional fields to include in the output Supported fields: 'id', 'internalHost', 'service', 'owsVersion', 'operation',
                        'subOperation', 'layer', 'bbox', 'path', 'queryString', 'bodyAsString', 'httpMethod', 'startTime', 'endTime', 'totalTime', 'remoteAddr', 'remoteUser',
                        'remoteUserAgent', 'responseStatus', 'responseLength', 'responseContentType', 'error', 'errorMessage'
  -t, --tail            Continuously monitor the directory for new log files and process them
  --ip IP               Filter log entries by IP address
  -l LIMIT, --limit LIMIT
                        Limit the number of log lines to print
tomcat@wms-geoserver-slave-set-0:/var/geoserver/audits$ 
```

### SOURCE IP

It is also possible to filter logs by IP using the `--ip` argument.

```
$ ./parser.py --directory geoserver-wms-geoserver-slave-set-0-Slave  --since 10m --limit 4 --ip 77.111.247.58
Level  Starttime                          Remoteaddr               Operation                Errormessage                                  
----------------------------------------------------------------------------------------------------------------------------------------------
Parsing file: geoserver-wms-geoserver-slave-set-0-Slave/geoserver_audit_20240830_190080.log
info   2024-08-30T14:48:00.554Z           77.111.247.58            GetFeatureInfo                                                         
info   2024-08-30T14:47:54.282Z           77.111.247.58            GetFeatureInfo                                                         
info   2024-08-30T14:47:49.529Z           77.111.247.58            dispatch                                                               
info   2024-08-30T14:47:47.256Z           77.111.247.58            GetMap
```

### ALL ARGS.

All arguements can be combined in one execution.

```
$ ./parser.py --directory geoserver-wms-geoserver-slave-set-6-Slave  --since 10m  --limit 5   --fields path,remoteUser --errors-only  --ip 10.42.32.221
Level  Starttime                          Remoteaddr               Operation                Errormessage                                      Path                     Remoteuser           
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parsing file: geoserver-wms-geoserver-slave-set-6-Slave/geoserver_audit_20240830_185006.log
error  2024-08-30T14:32:02.695Z           10.42.32.221                                      Could not find layer msg_rss:rgb_airmass_nrt      /wms                     anonymous            
error  2024-08-30T14:32:01.498Z           10.42.32.221                                      Could not find layer msg_rss:rgb_airmass_nrt      /wms                     anonymous            
error  2024-08-30T14:31:02.128Z           10.42.32.221             GetMap                                                                     /wms                     anonymous            
error  2024-08-30T14:31:02.715Z           10.42.32.221                                      Invalid date: 2024-8-24T18:30:0:00.000Z           /wms                     anonymous            
error  2024-08-30T14:31:02.697Z           10.42.32.221                                      Invalid date: 2024-8-24T18:30:0:00.000Z           /wms                     anonymous  
```
