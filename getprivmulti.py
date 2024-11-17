import multiprocessing
import os
import json
import ecdsa
import p2pkh_util
import common_util
import time

def private_key_to_public_key(private_key):
    sk = ecdsa.SigningKey.from_string(private_key.to_bytes(32, byteorder='big'), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    return public_key

def generate_private_key(seed):
    private_key = seed % (ecdsa.SECP256k1.order)
    return private_key

def process_chunk(start, end, target_address, core_num, checkpoint_interval=1000000):
    timenow = time.time()
    for i in range(start, end + 1):
        hex_num = format(i, '064x')
        pv_key = bytes.fromhex(hex_num)
        public_key_compressed = common_util.prikey_to_pubkey(pv_key, compressed=True)
        #print(public_key_compressed)
        address = p2pkh_util.pubkey_to_p2pkh_addr(public_key_compressed, b'\x00')
        result = f"{address}"
        if i % 100000 == 1:
            print(f"Core {core_num}: Checking key {i - start}")
            time100k = time.time() - timenow
            print(f"Performance of core: {100000/time100k} addr/sec ")
            timenow = time.time()
            print(hex_num)
        if target_address in result:
            print(f'COOL - Found by Core {core_num}')
            print(hex_num)
            with open('result.txt', 'a') as f:
                f.write(f"{hex_num}{result}\n")
            return hex_num

        # Save checkpoint
        if i % checkpoint_interval == 0:
            save_checkpoint(i, core_num)

    return None


def save_checkpoint(current_num, core_num):
    with open(f'checkpoint_core_{core_num}.json', 'w') as f:
        json.dump({'last_checked': current_num, 'core': core_num}, f)


def load_checkpoints(num_cores):
    checkpoints = []
    for i in range(num_cores):
        if os.path.exists(f'checkpoint_core_{i}.json'):
            with open(f'checkpoint_core_{i}.json', 'r') as f:
                data = json.load(f)
                checkpoints.append(data['last_checked'])
        else:
            checkpoints.append(None)
    return checkpoints


def main():
    seed = "0000000000000000000000000000000000000000000000060000000000000000"
    seed2 = "000000000000000000000000000000000000000000000006ffffffffffffffff"
    target_address = '1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9'

    start_num = int(seed, 16)
    end_num = int(seed2, 16)

    # Determine the number of CPU cores to use
    num_cores = multiprocessing.cpu_count()
    #num_cores = 120

    # Load checkpoints if they exist
    checkpoints = load_checkpoints(num_cores)

    # Calculate the chunk size for each process
    chunk_size = (end_num - start_num + 1) // num_cores

    # Create a pool of worker processes
    with multiprocessing.Pool(num_cores) as pool:
        # Prepare the arguments for each chunk
        chunk_args = []
        for i in range(num_cores):
            chunk_start = start_num + i * chunk_size
            chunk_end = min(start_num + (i + 1) * chunk_size - 1, end_num)

            # If checkpoint exists for this core, use it as the start
            if checkpoints[i] is not None:
                chunk_start = max(chunk_start, checkpoints[i] + 1)
                print(f"Resuming Core {i} from checkpoint: {chunk_start}")

            chunk_args.append((chunk_start, chunk_end, target_address, i))

        # Map the process_chunk function to the chunks
        results = pool.starmap(process_chunk, chunk_args)

    # Check if any process found a match
    for result in results:
        if result:
            print(f"Match found: {result}")
            break


if __name__ == "__main__":
    main()


