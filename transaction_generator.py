import requests
import random
import string

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

i=0
amount = 0

users=[]

while i < 10:
    users.append(randomString(10))
    i+=1

i=0

while i < 20:
    sender = random.randint(0,10)
    receiver = random.randint(0,10)
    add = random.randint(1000,150000)
    amount+=add
    requests.post('http://localhost/blockchain/transaction.php', data={'from':users[sender], 'to':users[receiver], 'amount':add}).text
    
    print(users[sender] + " SEND " + str(add) + " TO " + users[receiver])
    i+=1
    
