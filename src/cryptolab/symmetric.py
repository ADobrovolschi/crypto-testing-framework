"""Symmetric encryption: AES (CBC, CTR, GCM) and ChaCha20-Poly1305."""
import hashlib, os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from .utils import timed

def _cbc(key, data):
    iv = os.urandom(16)
    p = padding.PKCS7(128).padder()
    enc = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    ct = enc.update(p.update(data) + p.finalize()) + enc.finalize()
    def dec():
        d = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
        u = padding.PKCS7(128).unpadder()
        return u.update(d.update(ct) + d.finalize()) + u.finalize()
    return ct, dec

def _ctr(key, data):
    nonce = os.urandom(16)
    enc = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    ct = enc.update(data) + enc.finalize()
    def dec():
        d = Cipher(algorithms.AES(key), modes.CTR(nonce)).decryptor()
        return d.update(ct) + d.finalize()
    return ct, dec

def _gcm(key, data):
    n = os.urandom(12); a = AESGCM(key)
    ct = a.encrypt(n, data, None)
    return ct, lambda: a.decrypt(n, ct, None)

def _chacha(key, data):
    n = os.urandom(12); c = ChaCha20Poly1305(key)
    ct = c.encrypt(n, data, None)
    return ct, lambda: c.decrypt(n, ct, None)

ALGORITHMS = {
    "AES-128-CBC": (16, _cbc), "AES-256-CBC": (32, _cbc),
    "AES-128-CTR": (16, _ctr), "AES-256-CTR": (32, _ctr),
    "AES-128-GCM": (16, _gcm), "AES-256-GCM": (32, _gcm),
    "ChaCha20-Poly1305": (32, _chacha),
}

def benchmark(sizes=(1024, 102400, 1048576, 10485760)):
    results = []
    for name, (klen, fn) in ALGORITHMS.items():
        key = os.urandom(klen)
        for size in sizes:
            data = os.urandom(size)
            (ct, dec), t_enc = timed(fn, key, data)
            pt, t_dec = timed(dec)
            results.append({
                "algorithm": name, "size_bytes": size, "cipher_bytes": len(ct),
                "enc_s": t_enc, "dec_s": t_dec,
                "enc_mb_s": size / 1e6 / t_enc if t_enc else 0,
                "dec_mb_s": size / 1e6 / t_dec if t_dec else 0,
                "integrity_ok": hashlib.sha256(pt).digest() == hashlib.sha256(data).digest(),
            })
    return results
