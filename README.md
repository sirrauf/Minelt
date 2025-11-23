# Minelt (Mining Litecoin)

Minelt is a Python-based Litecoin mining software that connects to mining pools using the Stratum protocol. The software reads pool configurations and Litecoin addresses from external files and attempts to mine Litecoin blocks by solving cryptographic puzzles.

## Screenshots

![Minelt Screenshot](screenshot.png) *Example screenshot of the Minelt mining interface*

## Table of Contents

- [Minelt (Mining Litecoin)](#minelt-mining-litecoin)
- [Screenshots](#screenshots)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Virtual Environment Setup](#virtual-environment-setup)
  - [Installation](#installation)
  - [Configuration](#configuration)
    - [Pool Configuration](#pool-configuration)
    - [Litecoin Addresses](#litecoin-addresses)
  - [Usage](#usage)
  - [Architecture](#architecture)
    - [Classes](#classes)
    - [Data Flow](#data-flow)
  - [Limitations](#limitations)
  - [License](#license)

## Features

- Connects to Litecoin mining pools using the Stratum protocol
- Reads pool configurations from `account_pool.txt`
- Reads Litecoin addresses from `ltc_addrs.txt`
- Implements basic Stratum client functionality
- Performs simplified mining operations
- Supports multiple pool configurations with failover

## Requirements

- Python 3.7 or higher
- Standard Python libraries (no external dependencies required for basic functionality)

## Virtual Environment Setup

It's recommended to use a virtual environment to isolate the project dependencies:

```bash
# Create virtual environment
python -m venv minelt_env

# Activate virtual environment
# On Windows:
minelt_env\Scripts\activate
# On macOS/Linux:
source minelt_env/bin/activate

# Install required packages
pip install -r requirements.txt
```

To deactivate the virtual environment when done:
```bash
deactivate
```

## Installation

1. Clone or download the repository
2. Set up virtual environment (recommended)
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create configuration files as described in the Configuration section

## Configuration

### Pool Configuration

Create a file named `account_pool.txt` with the following format:

```
stratum+tcp://eu.litecoinpool.org:3333 port: 3333 protocol: stratum+tcp username: anandaraufm.08 password: 412412
stratum+tcp://us.litecoinpool.org:3333 port: 3333 protocol: stratum+tcp username: anandaraufm.08 password: 412412
stratum+tcp://us2.litecoinpool.org:3333 port: 3333 protocol: stratum+tcp username: anandaraufm.08 password: 412412
```

Each line contains:
- Pool URL in stratum+tcp format
- Port number
- Protocol type
- Username for authentication
- Password for authentication

### Litecoin Addresses

Create a file named `ltc_addrs.txt` containing your Litecoin addresses, one per line:

```
LYourLitecoinAddressHere1
LYourLitecoinAddressHere2
```

## Usage

1. Ensure configuration files are properly set up
2. Activate your virtual environment (if using one)
3. Run the script:
   ```bash
   python minelt.py
   ```
4. The program will:
   - Read pool configurations from `account_pool.txt`
   - Read Litecoin addresses from `ltc_addrs.txt`
   - Connect to the first available pool
   - Subscribe to mining jobs
   - Attempt to mine blocks

## Architecture

### Classes

#### `StratumClient`
Handles communication with the mining pool using the Stratum protocol.
- Manages socket connections
- Sends and receives JSON-RPC messages
- Handles subscription and authorization

#### `LitecoinMiner`
Implements the mining logic.
- Receives mining jobs from the pool
- Attempts to solve the cryptographic puzzle
- Submits successful solutions to the pool

#### `Checkdata`
Handles configuration and validation.
- Reads configuration files
- Validates pool settings and addresses
- Manages the mining startup process

### Data Flow

1. `Checkdata` reads configuration files
2. Validates pool settings and addresses
3. Creates `LitecoinMiner` instance with validated data
4. `LitecoinMiner` connects to the pool via `StratumClient`
5. Subscribes to mining jobs
6. Receives jobs and attempts to mine
7. Submits successful solutions

## Limitations

- This implementation uses simplified hashing (SHA256 instead of Scrypt) which is not suitable for actual Litecoin mining
- Mining difficulty is simplified for demonstration purposes
- Actual Litecoin mining requires specialized hardware and proper Scrypt implementation
- The code is for educational purposes and not intended for production mining



## License

This project is licensed under the Apache 2 License. See the LICENSE file for details.
