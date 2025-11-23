import asyncio
import json
import time
import socket
import struct
import hashlib
import requests
from binascii import unhexlify, hexlify

print("===============================================================================================\n")

nameprogram = "Minelt (Mining Litecoin)\n"
descprogram = " Minelt is software for mining LiteCoin\n"
version = 1.0
devby = "Developed by Ananda Rauf Maududi\n"
devdate = "Started Developed: 23 November 2025"

print(nameprogram)
print(descprogram)
print("Version:", version)
print(devby)
print(devdate)

print("===============================================================================================\n")

class StratumClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.socket = None
        self.id_counter = 1
        self.mining_info = {}
        self.running = True

    async def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def send_message(self, message):
        if self.socket:
            json_message = json.dumps(message) + '\n'
            self.socket.sendall(json_message.encode())

    def receive_message(self):
        if self.socket:
            try:
                data = self.socket.recv(4096).decode()
                if data:
                    for line in data.split('\n'):
                        if line.strip():
                            return json.loads(line)
            except socket.timeout:
                return None
        return None

    def subscribe(self):
        message = {
            'id': self.id_counter,
            'method': 'mining.subscribe',
            'params': ['Minelt/1.0']
        }
        self.id_counter += 1
        self.send_message(message)
        return self.receive_message()

    def authorize(self, username, password):
        message = {
            'id': self.id_counter,
            'method': 'mining.authorize',
            'params': [username, password]
        }
        self.id_counter += 1
        self.send_message(message)
        return self.receive_message()

    def submit_work(self, job_id, nonce, extra_nonce2, ntime, nonce2):
        message = {
            'id': self.id_counter,
            'method': 'mining.submit',
            'params': [self.username, job_id, extra_nonce2, ntime, nonce]
        }
        self.id_counter += 1
        self.send_message(message)
        return self.receive_message()

    def close(self):
        self.running = False
        if self.socket:
            self.socket.close()

class LitecoinMiner:
    def __init__(self, host, port, username, password, ltc_address):
        self.client = StratumClient(host, port, username, password)
        self.mining_info = {}
        self.running = True
        self.ltc_address = ltc_address
        self.ltc_balance = 0

    def calculate_hash(self, header):
        return hashlib.sha256(hashlib.sha256(header).digest()).digest()

    async def start_mining(self):
        if not await self.client.connect():
            return

        print("Subscribing to pool...")
        subscribe_result = self.client.subscribe()
        print(f"Subscribe result: {subscribe_result}")

        print("Authorizing worker...")
        auth_result = self.client.authorize(self.client.username, self.client.password)
        print(f"Auth result: {auth_result}")

        print("Starting mining loop...")
        while self.running:
            try:
                message = self.client.receive_message()
                if message:
                    if message.get('method') == 'mining.notify':
                        job = message.get('params')
                        if job:
                            print(f"New job received: {job[0]}")
                            self.mining_info = {
                                'job_id': job[0],
                                'prev_hash': job[1],
                                'coinb1': job[2],
                                'coinb2': job[3],
                                'merkle_branch': job[4],
                                'version': job[5],
                                'nbits': job[6],
                                'ntime': job[7],
                                'clean_jobs': job[8]
                            }
                            await self.mine_job()
                    elif message.get('id'):
                        print(f"Response: {message}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

            await asyncio.sleep(0.1)

    async def mine_job(self):
        if not self.mining_info:
            return

        print(f"Mining job {self.mining_info['job_id']}...")
        
        version = unhexlify(self.mining_info['version'].encode())
        prev_hash = unhexlify(self.mining_info['prev_hash'].encode())[::-1]
        merkle_root = self.calculate_merkle_root()
        ntime = unhexlify(self.mining_info['ntime'].encode())
        nbits = unhexlify(self.mining_info['nbits'].encode())
        nonce = b'\x00\x00\x00\x00'

        header = version + prev_hash + merkle_root + ntime + nbits + nonce
        
        for i in range(1000000):
            nonce_val = struct.pack('<I', i)
            full_header = version + prev_hash + merkle_root + ntime + nbits + nonce_val
            
            hash_result = hashlib.sha256(hashlib.sha256(full_header).digest()).digest()
            
            if hash_result.hex() < '00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF':
                print(f"Block found! Nonce: {i}")
                submit_result = self.client.submit_work(
                    self.mining_info['job_id'],
                    hexlify(nonce_val).decode(),
                    '0000000000000000',
                    self.mining_info['ntime'],
                    hexlify(nonce_val).decode()
                )
                print(f"Submit result: {submit_result}")
                
                self.ltc_balance += 0.01
                print(f"Balance increased! Current balance: {self.ltc_balance} LTC")
                
                await self.check_and_transfer_ltc()
                break

            if i % 10000 == 0:
                print(f"Trying nonce {i}...")

    def calculate_merkle_root(self):
        return b'\x00' * 32

    async def check_and_transfer_ltc(self):
        if self.ltc_balance > 0:
            print(f"Detected Litecoin balance: {self.ltc_balance} LTC")
            print(f"Attempting to transfer to address: {self.ltc_address}")
            
            print(f"Transfer of {self.ltc_balance} LTC to {self.ltc_address} simulated successfully!")
            
            self.ltc_balance = 0

class Checkdata():
    def __init__(self):
        self.pool_host = 'eu.litecoinpool.org'
        self.pool_port = 3333
        self.litecoin_address = None
        self.protocol = 'stratum+tcp'
        self.worker_name = 'anandaraufm.08'
        self.worker_password = '412412'
        self.pool_configs = []
        self.ltc_addresses = []

    def read_pool_config(self):
        try:
            with open('account_pool.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if 'stratum+tcp://' in line:
                            url_part = line.split()[0]
                            host_port = url_part.replace('stratum+tcp://', '')
                            host, port_str = host_port.split(':')
                            
                            params = {}
                            for item in line.split():
                                if ':' in item:
                                    key_val = item.split(':', 1)
                                    if len(key_val) == 2:
                                        key, val = key_val
                                        params[key.lower()] = val.strip()
                            
                            protocol = params.get('protocol', 'stratum+tcp')
                            username = params.get('username', '')
                            password = params.get('password', '')
                            
                            self.pool_configs.append({
                                'host': host,
                                'port': int(port_str),
                                'protocol': protocol,
                                'username': username,
                                'password': password
                            })
        except FileNotFoundError:
            print("account_pool.txt file not found. Using default values.")
        except Exception as e:
            print(f"Error reading account_pool.txt: {e}")

    def read_ltc_addresses(self):
        try:
            with open('ltc_addrs.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line:
                        self.ltc_addresses.append(line)
        except FileNotFoundError:
            print("ltc_addrs.txt file not found.")
        except Exception as e:
            print(f"Error reading ltc_addrs.txt: {e}")

    def checkdata(self):
        print("Starting data checks...\n")
        
        print("Reading pool configurations from account_pool.txt...")
        self.read_pool_config()
        
        if self.pool_configs:
            print(f"Found {len(self.pool_configs)} pool configuration(s)")
            for i, config in enumerate(self.pool_configs):
                print(f"Pool {i+1}: {config['protocol']}://{config['host']}:{config['port']}")
            
            selected_pool = self.pool_configs[0]
            self.pool_host = selected_pool['host']
            self.pool_port = selected_pool['port']
            self.protocol = selected_pool['protocol']
            self.worker_name = selected_pool['username']
            self.worker_password = selected_pool['password']
        else:
            print("Using default pool configuration")
        
        print(f"Pool Configuration: {self.protocol}://{self.pool_host}:{self.pool_port}")
        print("Pool Configuration OK!\n")

        print("Reading Litecoin addresses from ltc_addrs.txt...")
        self.read_ltc_addresses()
        
        if self.ltc_addresses:
            print(f"Found {len(self.ltc_addresses)} Litecoin address(es)")
            for i, addr in enumerate(self.ltc_addresses):
                print(f"Address {i+1}: {addr}")
            
            self.litecoin_address = self.ltc_addresses[0]
        else:
            print("No Litecoin addresses found in ltc_addrs.txt")
            self.litecoin_address = input("Enter Your Litecoin Address: ")
        
        if self.litecoin_address and len(self.litecoin_address) >= 26 and len(self.litecoin_address) <= 35:
            print(f"Litecoin Address: {self.litecoin_address}")
            print("Litecoin Address OK!\n")
        else:
            print("Litecoin Address Invalid!")
            return False

        print("All checks completed successfully!")
        return True

    async def connect_to_pool(self):
        try:
            miner = LitecoinMiner(self.pool_host, self.pool_port, self.worker_name, self.worker_password, self.litecoin_address)
            await miner.start_mining()
        except Exception as e:
            print(f"Connection error: {e}")

if __name__ == "__main__":
    checkingdata = Checkdata()
    
    if checkingdata.checkdata():
        asyncio.run(checkingdata.connect_to_pool())
    else:
        print("Data checks failed. Exiting...")
