# This program will launch system detail page
import mcafee
import os
import sys
from sys import exit

# ePO IP
ePOIP=''
# Login username
ePOUser=''
# Login user's password
ePOUserPwd=''

mc = mcafee.client(ePOIP,'8443',ePOUser,ePOUserPwd,'https','json')

computerName = 'COMPUTERNAME'
systems = mc.system.find(computerName)

if not systems:
    #print regsrv + ": " + input + " not found"
    print input + " not found"
    quit()
else:
    for system in systems:
        compname = system['EPOComputerProperties.ComputerName']
        sysurl = 'https://'+ePOIP+':8443/ComputerMgmt/getSystem.do?search=' + compname
        os.system('"%%comspec%% /c "c:/Program Files/Internet Explorer/iexplore.exe"" %s' % sysurl )



