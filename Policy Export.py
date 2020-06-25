# This script exports policies by name
#
# Colby Burkett
# McAfee Inc. 2020

import mcafee
import getpass

# Prompt for ePO v4.6+ IP
ePOIP=''
while ePOIP == '':
      ePOIP=raw_input('Please enter IP of McAfee ePO v4.6+ Server: ')

# Prompt for ePO username
ePOUser=''
while ePOUser == '':
      ePOUser=raw_input('Please enter username of TARGET McAfee ePO v4.6+ Server: ')

# Prompt for ePO user's password
ePOUserPwd=''
while ePOUserPwd == '':
      ePOUserPwd=getpass.getpass('Please enter password for ePO user \''+ePOUser+'\': ')

# Prompt for Policy Name
polname=''
while polname == '':
      polname=raw_input('Please enter name of policy to be applied to the systems: ')

# Instantiate the ePO connection/object
mc = mcafee.client(ePOIP,'8443',ePOUser,ePOUserPwd,'https','json')

# Fetch the policy object by name
policies = mc.policy.find(polname)
if not policies:
    print 'Policy not found'
else:
      # Create a unique set of Policy ProductIDs
      prdIds = set()
      for policy in policies:
            if policy['productId']:
                  prdIds.add(policy['productId'])
      for prdId in prdIds:
            # Export the policy to a file on the ePO Server's host OS drive (c:\reports)
            print mc.policy.export(prdId, polname+" "+prdId+".xml")
