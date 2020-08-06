import hashlib
import time
import requests
import json
import os
import pickle

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
    previous_hash = previous_block.hash
    block = '{"header":' + str(header) + ',"timestamp":' + str(timestamp) + ',"data":' + data + ',"previous_hash":"' + previous_hash + '"}|||'
    with open('block', 'a') as file:
        file.write(block)
    return IssouBlock(header, timestamp, data, previous_hash)

blockchain = [IssouBlock(0, time.time(), "I am the first block!", "0")]
last_block = blockchain[0]

while True:
    r = requests.get('http://localhost:80/blockchain/block').text
    i = 0
    all_blocks = r.split('|||')
    while i < len(all_blocks):
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
            print(" - New block added -")
            print("Number : " + str(getattr(new_block, 'header')))
            print("Hash : " + getattr(new_block, 'hash'))
            print("Data : " + str(getattr(new_block, 'data')))
            print("Previous hash : " + getattr(new_block, 'previous_hash') + "\n")
        else:
            data = requests.get("http://localhost:80/blockchain/NV_block").text
            if "{" in data :
                with open('blocks.txt', 'a+') as file:
                    file.write(data)

                with open('blocks.txt') as f:
                    blocks = f.readlines()

                for my_block in blocks:
                    if "{" in my_block:
                        my_block = my_block.rstrip()
                        j = json.loads(my_block)
                        new_block = next_block(last_block, my_block)
                        blockchain.append(new_block)
                        last_block = new_block
                        last_data = my_block

                        print(" - New block added -")
                        print("Number : " + str(getattr(new_block, 'header')))
                        print("Hash : " + getattr(new_block, 'hash'))
                        print("Data : " + getattr(new_block, 'data'))
                        print("Previous hash : " + getattr(new_block, 'previous_hash') + "\n")
                        with open("NV_block", "r") as f:
                            lines = f.readlines()
                        with open("NV_block", "w") as f:
                            for line in lines:
                                if line.strip("\n") != my_block:
                                    f.write(line)
                        try:
                            os.remove('blocks.txt')
                        except FileNotFoundError:
                            pass
