

# Script to create an NSX services
 
import requests
import sys
import csv			# to be able to read and write csv files


# If you have urllib3 uncomment this section to disable anoying warnings if using a self signed cert on NSX Manager.
#import urllib3
#urllib3.disable_warnings()

#
# Otherwise uncomment the following section to just hide the warnings ;)
import logging
logging.captureWarnings(True)

#
# This section is used if you want to use command line variables to pass to the script
#
#if len(sys.argv) != 6:
# print (len(sys.argv))
# print ("Usage: python nsx-create-service.py username password nsx_manager_hostname scope input_file_name ")
# sys.exit()
# 
#_user = sys.argv[1]
#_password = sys.argv[2]
#_nsxmgr = sys.argv[3]
#_scope = sys.argv[4]
#_inputfile = sys.argv[5]

#
# Instead we are going to hard code the variables into the script
_user = 'root'
_password = 'VMware1!'
_nsxmgr = 'nsxmgr-l-01a.corp.local'
_scope = 'datacenter-2'
_inputfile = 'nsx-services.txt'

# Initialise the logfile, will overwrite the last log file.
_logfile = open('log-nsx-create-service.txt', 'w')
_logfile.close()

#
# Open the logfile to append the logs. Must open it in binary mode so that it always adheres 
# to special characters like /n rather than quesry the OS, and then on Windows it will 
# literally print /n instead of a new line.
#
_logfile = open('log-nsx-create-service.txt', 'a+')

# Set the application content type to xml
_myheaders = {'Content-Type': 'application/xml'}

with open('%s' % _inputfile, 'r+') as _csvinput:
	spamreader = csv.reader(_csvinput, delimiter=',', quotechar='|')
	for row in spamreader:
		_svcName = (row[0])
		_svcDesc = (row[1])
		_svcProtocol = (row[2])
		_svcPort = (row[3])
		_myxml = '<?xml version="1.0" encoding="UTF-8" ?>'\
			'<application>'\
			'<objectId/>'\
			'<type>'\
			'<typeName/>'\
			'</type>'\
			'<description>' + _svcDesc + '</description>'\
			'<name>' + _svcName + '</name>'\
			'<revision>0</revision>'\
			'<objectTypeName/>'\
			'<element>'\
			'<applicationProtocol>' + _svcProtocol + '</applicationProtocol>'\
			'<value>' + _svcPort + '</value>'\
			'</element>'\
			'</application>'

		_requests_url = 'https://%s//api/2.0/services/application/%s' % (_nsxmgr, _scope)
		print ('Creating service %s' % _svcName)
		_success = requests.post((_requests_url), data=_myxml, headers=_myheaders, auth=(_user, _password), verify=False)
		_logfile.write('%s, ' % _svcName);
		_logfile.write('%s, ' % _success);
		_logfile.write('%s' % _success.text);
		# Write a new line - Windows
		_logfile.write('\r\n');
		# Write a new line - Linux
		#_logfile.write('\n');
exit()


