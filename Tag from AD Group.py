# This script applies a tag to systems that have a user associated with them
# The users are pulled from an AD Group supplied by the user
#
# Colby Burkett
# McAfee, Inc.
# 2/26/2013

import mcafee
import os
import sys
import getpass
import active_directory
    
print 'This script will identify each computer in the target\nMcAfee ePO system with users from the AD Group: ePO Demo Test.\nIt will then tag each system with the prompted tag name.\n'
# Prompt for ePO v4.6+ IP
ePOIP=''
while ePOIP == '':
      ePOIP=raw_input('Please enter IP of McAfee ePO Server: ')

# Prompt for ePO username
ePOUser=''
while ePOUser == '':
      ePOUser=raw_input('Please enter username of TARGET McAfee ePO Server: ')

# Prompt for ePO user's password
ePOUserPwd=''
while ePOUserPwd == '':
      ePOUserPwd=getpass.getpass('Please enter password for ePO user \''+ePOUser+'\': ')

# Prompt for the AD Group Name
ADGroup='ePO Demo Tes'
while ADGroup == '':
      ePOTag=raw_input('Please enter name of the AD Group to pull usernames from: ')

# Prompt for Tag Name
ePOTag='Mail Sender'
while ePOTag == '':
      ePOTag=raw_input('Please enter name of Tag to be applied to the systems: ')

ePO_Demo = active_directory.find_group (ADGroup)
if ePO_Demo:
      all_users = set ()
      for group, groups, users in ePO_Demo.walk ():
        all_users.update (users)
else:
      print "'%s' AD Group not found - Exiting!" % (ADGroup)
      exit()

mc = mcafee.client(ePOIP,'8443',ePOUser,ePOUserPwd,'https','json')
for user in all_users:
        userSAM = user.SAMAccountName.lower().rstrip('\r\n')
        print 'User: '+userSAM
        systems = mc.system.find(userSAM);
        if systems:
              for system in systems:
                  if system['EPOComputerProperties.UserName'].lower() == userSAM:
                          mc.system.applyTag(system['EPOComputerProperties.ComputerName'],ePOTag);
                          #mc.system.clearTag(system['EPOComputerProperties.ComputerName'],ePOTag);
                          print 'Tag ['+ePOTag+'] applied to system ['+system['EPOComputerProperties.ComputerName']+'] with user ['+system['EPOComputerProperties.UserName']+']'
        userDisplay = user.displayName.lower().rstrip('\r\n')
        print 'User: '+userDisplay
        systems = mc.system.find(userDisplay);
        if systems:
              for system in systems:
                      if system['EPOComputerProperties.UserName'].lower() == userDisplay:
                              mc.system.applyTag(system['EPOComputerProperties.ComputerName'],ePOTag);
                              #mc.system.clearTag(system['EPOComputerProperties.ComputerName'],ePOTag);
                              print 'Tag ['+ePOTag+'] applied to system ['+system['EPOComputerProperties.ComputerName']+'] with user ['+system['EPOComputerProperties.UserName']+']'
        userFL = user.firstName.lower().rstrip('\r\n')+' '+user.lastName.lower().rstrip('\r\n')
        print 'User: '+userFL
        systems = mc.system.find(userFL);
        if systems:
              for system in systems:
                      if system['EPOComputerProperties.UserName'].lower() == userFL:
                              mc.system.applyTag(system['EPOComputerProperties.ComputerName'],ePOTag);
                              #mc.system.clearTag(system['EPOComputerProperties.ComputerName'],ePOTag);
                              print 'Tag ['+ePOTag+'] applied to system ['+system['EPOComputerProperties.ComputerName']+'] with user ['+system['EPOComputerProperties.UserName']+']'
						
