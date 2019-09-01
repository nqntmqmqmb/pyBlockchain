import requests
import hashlib
import json
import random
import os
from threading import Thread
import time


total_block_mined = 0

class IssouBlock:
    def __init__(self, header, timestamp, data, previous_hash):
        self.header = header
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.sha256_hash()
    
    def sha256_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.header).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

def next_block(previous_block, data):
    header = previous_block.header + 1
    timestamp = time.time()
    data = data
    previous_hash = previous_block.hash
    block = '{"header":' + str(header) + ',"timestamp":' + str(timestamp) + ',"data":' + data + ',"previous_hash":"' + previous_hash + '"}|||'
    file = open('block', 'a')
    file.write(block)
    file.close()
    return IssouBlock(header, timestamp, data, previous_hash)

blockchain = [IssouBlock(0, time.time(), "I am the first block!", "0")]
last_block = blockchain[0]

last_data = ""

while True:
    r = requests.get('http://localhost:80/blockchain/block').text
    i = 0
    if r != last_data:
        last_data = r
        all_blocks = r.split('|||')
        while i < len(all_blocks): #essayer avec un for
            if "{" in all_blocks[i]:
                j = json.loads(all_blocks[i])
                header = j['header']
                timestamp = j['timestamp']
                data = str(j['data']).replace(' ', '').replace("'", '"')
                previous_hash = j['previous_hash']
                new_block = IssouBlock(header, timestamp, data, previous_hash)
                blockchain.append(new_block)
                last_block = new_block
                i+=1
                os.system('cls' if os.name == 'nt' else 'clear')
                print("[*] Blockchain Reloaded")
                print("Successfully added block n°{}".format(str(i)))
            else:
                
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
