#!/usr/bin/env bash
# Verify a Kali ISO checksum (Linux: sha256sum, macOS: shasum -a 256)
set -euo pipefail
ISO="${1:?Usage: $0 <file.iso>}"
if command -v sha256sum >/dev/null; then sha256sum "$ISO"; else shasum -a 256 "$ISO"; fi
