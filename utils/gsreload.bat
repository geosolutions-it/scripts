@echo off
rem The MIT License
rem 
rem Copyright (c) 2015 GeoSolutions S.A.S.
rem http://www.geo-solutions.it
rem 
rem Permission is hereby granted, free of charge, to any person obtaining a copy
rem of this software and associated documentation files (the "Software"), to deal
rem in the Software without restriction, including without limitation the rights
rem to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
rem copies of the Software, and to permit persons to whom the Software is
rem furnished to do so, subject to the following conditions:
rem 
rem The above copyright notice and this permission notice shall be included in
rem all copies or substantial portions of the Software.
rem 
rem THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
rem IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
rem FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
rem AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
rem LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
rem OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
rem THE SOFTWARE.

rem ###########################################################
rem  author: Lorenzo Pini - lorenzo.pini@geo-solutions.it
rem  date: 26 Jul 2015
rem 
rem  Simple GeoServer configuration reload script for Window
rem
rem  REQUIREMENTS:
rem  - curl must be in the PATH (http://curl.haxx.se/download.html)
rem ###########################################################

set errorlevel=

rem  the url to use to test the service
rem  !make sure to implement the url_test logic also into the bottom function
set URLA="http://localhost:8080/geoserver/rest/reload"
set URLB="http://localhost:8081/geoserver/rest/reload"

set ACCOUNT="admin:geoserver"

rem  the output file to use as log
rem  must exists otherwise the stdout will be used
rem  NOTE: remember to logrotate this file!!!
rem LOGFILE="/var/log/gsreload.log"
set LOGFILE="gsreload.log"

rem  maximum tries to perform a quick restart
rem  when the request fails another request will be tried at least $RETRY times
rem  if the new request fails RETRY times the script ends returning '100'
rem set RETRY=1

rem ################### RELOAD GEOSERVER CONFIGURATION  #####################

call:reload_config %URLA%
call:reload_config %URLB%

goto:eof

:reload_config

curl -sS -XPOST -u %ACCOUNT% %~1 >> %LOGFILE%

rem echo Error Level is: %errorlevel%
rem echo Error Level is: %errorlevel% >> %LOGFILE%

IF %errorlevel%==0 echo "%date% %time% GeoServer Reload Status: OK - %~1 is responding " >> %LOGFILE%
IF NOT %errorlevel%==0 echo "%date% %time% GeoServer Reload Status: FAIL - %~1 is NOT responding " >> %LOGFILE%

goto:eof

rem echo "`date` GeoServer Reload configuration Action: FAILED (WHAT's HAPPENING? -> exit (status: 100))" >> "${LOGFILE}"
rem exit 100
