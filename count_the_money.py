import hashlib
import time
import requests
import json

users = []
r = requests.get('http://localhost:80/blockchain/block').text
i = 0
all_blocks = r.split('|||')

while i < len(all_blocks):
    
    if "{" in all_blocks[i]:
        
        j = json.loads(all_blocks[i])
        
        if j['data']['transaction'][0]['from'] + ":0" in users:
            pass
        else:
            users.append(j['data']['transaction'][0]['from'] + ":0")
            
        if j['data']['transaction'][0]['to'] + ":0" in users:
            pass
        else:
            users.append(j['data']['transaction'][0]['to'] + ":0")
            
        i+=1
        
    else:
        i+=1

i = 0
x = 0

while x < len(users):
    
    while i < len(all_blocks):
    
        if "{" in all_blocks[i]:
        
            j = json.loads(all_blocks[i])
    
            
            if users[x].split(':')[0] in j['data']['transaction'][0]['to']:
                credit = int(users[x].split(':')[1])
                credit += int(j['data']['transaction'][0]['amount'])
                users[x] = users[x].split(':')[0] + ":" + str(credit)
                i+=1
            elif users[x].split(':')[0] in j['data']['transaction'][0]['from']:
                credit = int(users[x].split(':')[1])
                credit = credit - int(j['data']['transaction'][0]['amount'])
                users[x] = users[x].split(':')[0] + ":" + str(credit)
                i+=1
            else:
                i+=1
            #    users.append(j['data']['transaction'][0]['amount'])
        else:
            i+=1
            x+=1
    i=0
x+=1


print(users)