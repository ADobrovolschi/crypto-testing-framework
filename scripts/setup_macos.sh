#!/usr/bin/env bash
# macOS setup (Intel or Apple Silicon)
set -euo pipefail
command -v python3 >/dev/null || { echo "Install Python first: brew install python"; exit 1; }
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt pytest
python3 --version
echo "Ready. Run: PYTHONPATH=src python -m cryptolab.main --quick"
