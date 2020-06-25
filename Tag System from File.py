# This script applies a tag to systems that have a user associated with them
# The computer list input is from a file called 'computers.txt'.
# Format of the file should be one computer name per line
# Name must be an exact match for tag to be applied.

import mcafee
import os
import sys

# ePO IP
ePOIP=''
# Login username
ePOUser=''
# Login user's password
ePOUserPwd=''

# Prompt for Tag Name
ePOTag=''
while ePOTag == '':
      ePOTag=raw_input('Please enter name of Tag to be applied to the systems: ')
      
mc = mcafee.client(ePOIP,'8443',ePOUser,ePOUserPwd,'https','json')
logfile = open('computers_apply.log','w')
file = open('computers.txt', 'r')
for computer in file:
      computer = computer.rstrip('\r\n')
      print 'Computer: '+computer;
      systems = mc.system.find(computer)
      if systems:
            for system in systems:
                  if system['EPOComputerProperties.ComputerName'] == computer:
                        print 'Found computer: '+ computer
                        print 'Applying tag: ' + ePOTag
                        mc.system.applyTag(system['EPOComputerProperties.ComputerName'],ePOTag);
                        #mc.system.clearTag(system['EPOComputerProperties.ComputerName'],ePOTag);
                        print 'Tag ['+ePOTag+'] applied to system ['+system['EPOComputerProperties.ComputerName']+']'
                  else:
                        print 'Computer '+computer+' not found.'
                        logfile.write('Computer '+computer+' not found.\n')
      else:
            print 'Computer ['+computer+'] not found.'
            logfile.write('Computer ['+computer+'] not found.\n')
file.close()
logfile.close()

