# This script executes a custom query against ePO to return a list of systems with Custom Prop 1 equal to 'CN=*', and no desired tag
# It then tags the system, and issues an agent wakeup call.

import mcafee

# ePO IP
ePOIP=''
# Login username
ePOUser=''
# Login user's password
ePOUserPwd=''
# Tag Name
ePOTag='Server'

mc = mcafee.client(ePOIP,'8443',ePOUser,ePOUserPwd,'https','json')
ePOTagSet = mc.system.findTag(ePOTag)
if ePOTagSet:
      for ePOTagInfo in ePOTagSet:
          systems = mc.core.executeQuery(target='EPOLeafNode',
                                         select='(select EPOComputerProperties.ComputerName EPOComputerProperties.ParentID EPOComputerProperties.UserProperty1)',
                                         where='(and(startsWith EPOComputerProperties.UserProperty1 "CN=") (doesNotHaveTag EPOLeafNode.AppliedTags '+str(ePOTagInfo['tagId'])+'))')
          if systems:
                for system in systems:
                    mc.eeadmin.assignUser(systemNode='True',nodeId=str(system['EPOComputerProperties.ParentID']),dn=system['EPOComputerProperties.UserProperty1'])
                    mc.system.applyTag(system['EPOComputerProperties.ComputerName'],ePOTag)
                    print 'Tag ['+ePOTag+'] applied to system ['+system['EPOComputerProperties.ComputerName']+']'
                    mc.system.wakeupAgent(ids=str(system['EPOComputerProperties.ParentID']))
                    print 'Agent wakeup issued for system ['+system['EPOComputerProperties.ComputerName']+']'
          else:
                print 'No systems found'
else:
      print 'Error: Tag not found'
