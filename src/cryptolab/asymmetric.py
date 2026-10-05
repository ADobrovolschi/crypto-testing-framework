"""Asymmetric crypto: RSA-2048/3072 vs ECC P-256 (ECDSA)."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from .utils import timed

MSG = b"test message for digital signature"

def _rsa(bits):
    key, t_gen = timed(lambda: rsa.generate_private_key(65537, bits), repeat=1)
    pad = padding.PKCS1v15()
    sig, t_sign = timed(key.sign, MSG, pad, hashes.SHA256(), repeat=20)
    _, t_ver = timed(key.public_key().verify, sig, MSG, pad, hashes.SHA256(), repeat=20)
    return {"algorithm": f"RSA-{bits}", "key_bits": bits, "keygen_s": t_gen,
            "sign_per_s": 1 / t_sign, "verify_per_s": 1 / t_ver}

def _ecc():
    key, t_gen = timed(lambda: ec.generate_private_key(ec.SECP256R1()), repeat=1)
    alg = ec.ECDSA(hashes.SHA256())
    sig, t_sign = timed(key.sign, MSG, alg, repeat=20)
    _, t_ver = timed(key.public_key().verify, sig, MSG, alg, repeat=20)
    return {"algorithm": "ECC-P256", "key_bits": 256, "keygen_s": t_gen,
            "sign_per_s": 1 / t_sign, "verify_per_s": 1 / t_ver}

def benchmark():
    return [_rsa(2048), _rsa(3072), _ecc()]
