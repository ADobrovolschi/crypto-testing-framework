#!/usr/bin/env bash
# Kali Linux / Debian setup
set -euo pipefail
sudo apt update && sudo apt install -y python3 python3-venv python3-pip openssl git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest
echo "Ready. Run: PYTHONPATH=src python -m cryptolab.main --quick"
