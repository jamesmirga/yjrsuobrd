import multiprocessing
from bitcoinlib.keys import Key
from ecdsa import SECP256k1
import binascii

# Definierte Zieladresse und Schlüsselbereich
TARGET_ADDRESS = '1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9'
START_KEY = int('0000000000000000000000000000000000000000000000040000000000000000', 16)
STOP_KEY = int('000000000000000000000000000000000000000000000007ffffffffffffffff', 16)

def check_key_range(start, stop):
    for i in range(start, stop):
        private_key = hex(i)[2:].zfill(64)
        key = Key(import_key=private_key, network='bitcoin')
        if key.address() == TARGET_ADDRESS:
            return private_key
    return None

def main():
    # Anzahl der Prozesse
    num_processes = multiprocessing.cpu_count()
    key_range = STOP_KEY - START_KEY
    chunk_size = key_range // num_processes

    pool = multiprocessing.Pool(processes=num_processes)
    tasks = [(START_KEY + i * chunk_size, START_KEY + (i + 1) * chunk_size) for i in range(num_processes)]

    result = None
    for res in pool.starmap(check_key_range, tasks):
        if res is not None:
            result = res
            break

    if result:
        print(f"Private Key gefunden: {result}")
    else:
        print("Kein Private Key gefunden im gegebenen Bereich.")

if __name__ == '__main__':
    main()