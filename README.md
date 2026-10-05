# CryptoLab: Comparative Analysis of Cryptographic Algorithms

A modular Python framework for **testing, comparing and evaluating** cryptographic algorithms (AES, ChaCha20, RSA, ECC, hash functions). It was developed for a bachelor's thesis (2025) on a Kali Linux VM running on Hyper-V. It also runs on macOS and other Linux systems.

> **Educational use only.** The attack simulations run against locally generated data. Do not use this code against systems you do not own.

## Features

| Module | File | Contents |
|---|---|---|
| Symmetric encryption | `symmetric.py` | AES-128/256 (CBC, CTR, GCM), ChaCha20-Poly1305: throughput, overhead, integrity checks |
| Asymmetric encryption | `asymmetric.py` | RSA-2048/3072 vs ECC P-256: signatures/s, verifications/s, key generation |
| Hash functions | `hashing.py` | Avalanche effect, MD5/SHA-1/SHA-256/SHA-512/SHA3 comparison, performance, salting, integrity |
| Attack demos | `attacks.py` | Dictionary attack, rainbow table, protection offered by salts |
| Benchmarks | `benchmarks.py` | Native `openssl speed` wrapper |
| Reporting | `reporting.py` | Structured JSON export and an HTML dashboard |
| Orchestration | `main.py` | Runs everything and keeps going if one test fails |

## Repository structure

```
crypto-testing-framework/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── src/cryptolab/
│   ├── __init__.py
│   ├── main.py
│   ├── symmetric.py
│   ├── asymmetric.py
│   ├── hashing.py
│   ├── attacks.py
│   ├── benchmarks.py
│   ├── reporting.py
│   └── utils.py
├── tests/
├── scripts/        # Kali and macOS setup, ISO verification
├── docs/           # thesis PDF and screenshots
└── results/        # generated output (git-ignored)
```

## Installation

### macOS

```bash
brew install python git          # skip if already installed
git clone https://github.com/ADobrovolski/crypto-testing-framework.git
cd crypto-testing-framework
bash scripts/setup_macos.sh
source .venv/bin/activate
```

### Kali Linux / Debian

```bash
git clone https://github.com/<user>/crypto-testing-framework.git
cd crypto-testing-framework
bash scripts/setup_kali.sh
source .venv/bin/activate
```

## Usage

```bash
export PYTHONPATH=src
python -m cryptolab.main            # full run
python -m cryptolab.main --quick    # small files, faster
pytest -q                           # unit tests
```

Output goes to `results/`: `results.json`, `report.html` and `cryptolab.log`. On macOS, run `open results/report.html` to view the dashboard.

## Test environment (from the thesis)

- Hyper-V, Generation 2 VM (UEFI), 4 vCPU, 8 GB RAM, 80 GB disk, Default Switch
- Kali Linux, hostname `kali-crypto-lab`
- OpenSSL and the Python `cryptography` library

## Key findings

- **AES-128-CBC** reached about 1,504 MB/s. **ChaCha20** beat AES-256 on large files in the thesis tests (431 vs 334 MB/s).
- **ECC P-256** produced about 29x more signatures per second than RSA-2048, with keys 8x smaller. RSA verifies faster.
- **Unsalted hashes**: 100% of common passwords were cracked instantly. **Unique salts**: 0 successful attacks.
- Avoid **MD5** and **SHA-1**. Recommended: SHA-256 or SHA-3, AES-256-GCM, ChaCha20, ECC P-256, TLS 1.3.

Results depend on hardware (for example AES-NI), so your numbers will differ. On Apple Silicon, expect different AES and ChaCha20 ratios.

## Limitations

- Only OpenSSL and the `cryptography` library were tested.
- No real side-channel attacks were performed.
- AES-GCM and SHA-384 were not available in the OpenSSL version used in the thesis.

## Future work

Post-quantum cryptography (Kyber, Dilithium, SPHINCS+), ARM and RISC-V testing, side-channel tests, large-scale testing.

## License

MIT. See `LICENSE`.
