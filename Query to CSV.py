# This script executes a query against ePO and writes it to a CSV

import mcafee
import csv

# ePO IP
ePOIP=''
# Login username
ePOUser=''
# Login user's password
ePOUserPwd=''
# Name the file
filename='output.csv'

mc = mcafee.client(ePOIP,'8443',ePOUser,ePOUserPwd,'https','json')
# Prompt for Query Name
ePOQuery=''
while ePOQuery == '':
      ePOQuery=raw_input('Please enter name of query: ')

mc = mcafee.client(ePOIP,'8443',ePOUser,ePOUserPwd,'https','json')

queries = mc.core.listQueries()
for query in queries:
      if query['name'] == ePOQuery:
            # View the query id or name or whatever based on what you glean from the prior results
            results = mc.core.executeQuery(str(query['id']))
            #print results to see what fields are available in the query's output
            if results:
                  with open(filename, 'wb') as f:
                        w = csv.writer(f)
                        # Write the headers to the file
                        w.writerow(results[0].keys())
                        for result in results:
                              # Write each row to the file
                              w.writerow(result.values())

