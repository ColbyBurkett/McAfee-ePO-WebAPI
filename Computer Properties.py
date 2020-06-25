# This simple script is an example to retrieve Computer Properties from
# a McAfee ePO Server. using the mcafee.py library from McAfee
import mcafee

# ePO IP
ePOIP=''
# Login username
ePOUser=''
# Login user's password
ePOUserPwd=''

mc = mcafee.client(ePOIP,'8443',ePOUser,ePOUserPwd,'https','json')

computer = 'COMPUTERNAME'
systems = mc.system.find(computer)
if systems:
      for system in systems:
            # Display all the property elements in the object
            print(system)
            if system['EPOComputerProperties.ComputerName'] == computer:
                  print('Found computer: '+ computer)
            else:
                  print('Computer '+computer+' not found.')
else:
      print('Computer ['+computer+'] not found.')

