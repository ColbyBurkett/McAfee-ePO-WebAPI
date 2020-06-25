# Simple snippet to Import TIE File Reputations from a file
'''
Reputation values:

0   = Not Set (use this to clear/delete an Enterprise reputation
1   = Known Malicious
15  = Most Likely Malicious
30  = Might be Malicious
50  = Unknown
70  = Might be Trusted
85  = Most likely Trusted
99  = Known Trusted File
100 = Known Trusted Installer

File format:
test.exe,md5,E539E67EBCDE132E1B51925EA32EE094,99,"MD5 for random file"
test2.dll,sha1,474BC498B6E96107C749AB56E77C1094E19ECE5D,99,"SHA1 for random file"
'''

# Output of https://epo:8443/remote/core.help?command=tie.setReputations
'''
tie.setReputations [fileReps] [certReps]
JSON string for file or certificate reputations with Base64 encoded hash values.
Specify at least one fileReps or certReps. Both can be specified too. If you use
a browser, encode the URL.
Parameters:
 fileReps (param 1) - JSON string of file reputations. At least one hash need to
be present. Optional parameters: "name" and "comment". Ex: 

[{"sha1":"frATnSF1c5s8yw0REAZ4IL5qvSk=","md5":"8se7isyX+S6Yei1Ah9AhsQ==","sha256":"39Gv4ExOzWr5SMNMrObQJ3A3SSSzEoz2MFi4X8YNAVQ=","reputation":"99"},{"sha1":"d3HtjhR0Eb3qN6c+vVxeqVVe0t4=","md5":"V+0uApv5yjk4PSpnHvT7UA==","reputation":"85"}]
 certReps (param 2) - JSON string of certificate reputations. Both sha1 and
publicKeySha1 are required. Optional parameter: "comment". Ex: 

[{"sha1":"frATnSF1c5s8yw0REAZ4IL5qvSk=","publicKeySha1":"frATnSF1c5s8yw0REAZ4IL5qvSk=","reputation":"99"}]
'''

import base64
import csv
import json
import mcafee

mc = mcafee.client('your IP here', '8443', 'your ePO username', 'your ePO user passwd')

# Read the file and set the reputations
with open('reputations.csv') as f:
    fileReputations = csv.reader(f)
    for rowofdata in fileReputations:
        name = rowofdata[0].lower()
        hashType = rowofdata[1].lower()
        fileHash = rowofdata[2].upper()
        reputation = rowofdata[3]
        comment = rowofdata[4]
        Info = json.dumps([{hashType:base64.b64encode(fileHash.decode("hex")),'reputation':reputation,'name':name,'comment':comment}])
        print mc.tie.setReputations(Info)
