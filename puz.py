import hashlib
import ecdsa
import requests

hex_number_256bit = 'your_hexadecimal_representation_of_256-bit_number'


start = int("40000000000000000", 16)
end = int("47777777777777777", 16)
target_address = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'
found = False

for i in range(start, end-1, -1):
    private_key = ecdsa.SigningKey.from_string(i.to_bytes(32, byteorder='big'), curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    public_key_bytes = public_key.to_string()
    compressed_public_key = b'\x02' + public_key_bytes[:32] if public_key_bytes[-1] % 2 == 0 else b'\x03' + public_key_bytes[:32]
    public_key_hash = hashlib.sha256(compressed_public_key).digest()
    public_key_hash = hashlib.new('ripemd160', public_key_hash).digest()
    network_byte = b'\x00'
    public_key_hash = network_byte + public_key_hash
    hash_1 = hashlib.sha256(public_key_hash).digest()
    hash_2 = hashlib.sha256(hash_1).digest()
    checksum = hash_2[:4]
    address_bytes = public_key_hash + checksum
    base58_alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    address = ''
    num = int.from_bytes(address_bytes, 'big')
    while num > 0:
        num, remainder = divmod(num, 58)
        address = base58_alphabet[remainder] + address
    address = '1' * (len(address_bytes) - len(address_bytes.lstrip(b'\x00'))) + address
    print(f"Private Key Found: {hex(i)[2:].rjust(64, '0')}")
    print(address)

    if address == target_address:
        print(f"Private Key Found: {hex(i)[2:].rjust(64, '0')}")
        found = True
        break

