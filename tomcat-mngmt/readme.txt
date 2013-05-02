These Instructions are valid both for Ubuntu and CentOs scripts. 
The Ubuntu version use the start-stop-daemon command instead of daemon command.

The tomcatService script depends on tomcatRunner, the script assumes the presence of setenv.sh script in $CATALINA_BASE/bin directory.

1) copy both files into /etc/init.d folder, set execution permission and owner to root.

2) copy the tomcatService file many time as the number of your desidered CATALINA_BASE instance and rename them with the service name you want assign.

3) open each tomcatService and set the properties on top of the file, in the section called "frequent settings area"

4) give a look at the next settings area and be sure that all settings are ok.

5) set the startup of the services

6) You must run the service as superuser, the service will be owned by the user specified in "frequent settings area"
	examples 
		$ sudo service tomcatService start
		$ sudo service tomcatService stop
		$ sudo service tomcatService status
		$ sudo service tomcatService restart