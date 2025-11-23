import asyncio
import json
import time
import socket
import struct
import hashlib
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
    def __init__(self, host, port, username, password):
        self.client = StratumClient(host, port, username, password)
        self.mining_info = {}
        self.running = True

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
            full_header = version + prev_hash + merkle_root + ntime + n