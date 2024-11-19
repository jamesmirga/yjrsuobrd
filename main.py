import random
from bitcoin import privtopub, encode_pubkey, pubtoaddr, decode_privkey
from rich.console import Console
import multiprocessing

console = Console()
def clear():
    console.clear()
# Function to generate Bitcoin addresses
def generate_address(prefix):
    total = 0
    while True:  
        low  = 0x40000000000000000
        high = 0x7ffffffffffffffff
        val = str(hex(random.randrange(low, high)))[2:]
        result = val.rjust(48 + len(val), '0')
        priv = result
        pub = privtopub(decode_privkey(priv, 'hex'))
        pubkey1 = encode_pubkey(pub, "bin_compressed")
        addr = pubtoaddr(pubkey1)
        n = addr
        total += 1
        if n.startswith(prefix):
            console.print ("FOUND!", priv, addr,  result)
            k1 = priv
            k2 = pub
            k3 = addr

            with open('found.txt', 'a') as file:
                file.write("Private key: " + str(k1) + '\n' + "Public key: " + str(k2) + '\n' + "Address: " + str(k3) + '\n\n')
            break
        else:
            clear()
            console.print("TOTAL: ", total,"\n", addr, end='\r')

if __name__ == '__main__':
    console = Console()
    prefix = '1BY8GQbnue'  # Desired prefix
    num_processes = multiprocessing.cpu_count() * 4  # Number of CPU cores

    # Create processes
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=generate_address, args=(prefix,))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()
