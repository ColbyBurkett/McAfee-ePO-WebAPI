# Sample code to execute query and send email with results
# This exact query is focused on determining if a Policy was altered, as indicated in the Audit Log
#
# Colby Burkett
# 4/15/2019

import getpass
import mcafee
import os
import smtplib, ssl
import sys
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

print 'This script will export the contents of the desired query\n'
# Prompt for ePO IP
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

# Prompt for Query Name
ePOQuery='Policy Changes'
while ePOQuery == '':
      ePOQuery=raw_input('Please enter name of query: ')

mc = mcafee.client(ePOIP,'8443',ePOUser,ePOUserPwd,'https','json')
# Name the file
filename='output.csv'

# in "write" mode
file = open(filename,"w")
queries = mc.core.listQueries()
for query in queries:
      if query['name'] == ePOQuery:
            # View the query id or name or whatever based on what you glean from the prior results
            #print query['id']
            results = mc.core.executeQuery(str(query['id']))
            #print results to see what fields are avaialble in the query's output
            if results:
                  for result in results:
                        print '"'+result['OrionAuditLog.UserName']+ \
                        '","'+result['OrionAuditLog.Message']+ \
                        '","'+result['OrionAuditLog.EndTime'] + \
                        '","'+str(result['OrionAuditLog.CmdName'])+'"'
                        # Write the data to the file
                        file.write('"'+result['OrionAuditLog.UserName']+ \
                        '","'+result['OrionAuditLog.Message']+ \
                        '","'+result['OrionAuditLog.EndTime'] + \
                        '","'+str(result['OrionAuditLog.CmdName'])+'"\n')
                  # Be sure to close the file!!
                  file.close()
                  
                  # Email the file using available SMTP server & python features
                  # Placing the email functions here

                  smtp_server = "smtp.gmail.com"
                  sender_email = "you@server.com"
                  receiver_email = "them@server.com"
                  password = raw_input("Type your password and press enter:")

                  # instance of MIMEMultipart 
                  msg = MIMEMultipart() 
                    
                  # storing the senders email address   
                  msg['From'] = sender_email 
                    
                  # storing the receivers email address  
                  msg['To'] = receiver_email 
                    
                  # storing the subject  
                  msg['Subject'] = "Audit Log: Policy Changes"
                    
                  # string to store the body of the mail 
                  body = "Body_of_the_mail"
                    
                  # attach the body with the msg instance 
                  msg.attach(MIMEText(body, 'plain')) 
                    
                  # open the file to be sent  
                  attachment = open(filename, "rb") 
                    
                  # instance of MIMEBase and named as p 
                  p = MIMEBase('application', 'octet-stream') 
                    
                  # To change the payload into encoded form 
                  p.set_payload((attachment).read()) 
                    
                  # encode into base64 
                  encoders.encode_base64(p) 
                     
                  p.add_header('Content-Disposition', 'attachment', filename=filename) 
                    
                  # attach the instance 'p' to instance 'msg' 
                  msg.attach(p)
                  message = msg.as_string()
                  server = smtplib.SMTP_SSL(smtp_server, 465)
                  server.login(sender_email, password)
                  server.sendmail(sender_email, receiver_email, message)
                  server.quit()
