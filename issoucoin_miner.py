import requests
import hashlib
import json
import random
import os
from threading import Thread

total_block_mined = 0

while True:
    transactions = requests.get('http://localhost:80/blockchain/mine').text
    if transactions != "":
        file = open('transactions.txt', 'a+')
        file.write(transactions)
        file.close()

        with open('transactions.txt') as f:
            my_transaction = f.readline().rstrip()

        j = json.loads(my_transaction)

        word1 = j['proof-of-work-word1']
        word2 = j['proof-of-work-word2']
        startby = j['proof-of-work-startby']

        found = 0
        string = word1 + "," + word2 + "!"
        i=0

        while found == 0:
            new_string = string + str(i)
            sha = hashlib.sha256()
            sha.update(new_string.encode('utf8'))

            if sha.hexdigest()[:4] == str(startby):
                r = requests.post('http://localhost:80/blockchain/verify.php', data={'transaction':my_transaction, 'POW': sha.hexdigest(), 'i':i}).text
                if "OK" in r:
                    total_block_mined+=1
                    print("Successfully mined {} blocks".format(str(total_block_mined)))
                    found = 1
                else:
                    print("ERROR !!!!!!")
                    break
            else:
                i+=1

        os.remove('transactions.txt')