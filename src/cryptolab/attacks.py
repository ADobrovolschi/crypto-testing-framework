"""EDUCATIONAL attack simulations on hashes (dictionary, rainbow, salt).
Runs only on locally generated data. Never target real systems."""
import hashlib, os, time
from .hashing import h

WORDLIST = ["password", "123456", "admin", "qwerty", "letmein", "welcome",
            "password123", "iloveyou", "abc123", "12345678", "root"]

def dictionary_attack(target_hash, algo, wordlist=WORDLIST, salt=b""):
    t = time.perf_counter()
    for w in wordlist:
        if hashlib.new(algo, salt + w.encode()).hexdigest() == target_hash:
            return {"cracked": True, "password": w, "time_s": time.perf_counter() - t}
    return {"cracked": False, "password": None, "time_s": time.perf_counter() - t}

def run_dictionary(passwords=("password", "123456", "admin"), algos=("md5", "sha256")):
    return [{"algorithm": a, "target": p, **dictionary_attack(h(a, p), a)}
            for a in algos for p in passwords]

def rainbow_table_attack(passwords=("password", "123456", "admin")):
    t0 = time.perf_counter()
    table = {h("md5", w): w for w in WORDLIST}
    t_build = time.perf_counter() - t0
    t1 = time.perf_counter()
    hits = sum(1 for p in passwords if h("md5", p) in table)
    return {"table_size": len(table), "build_s": t_build, "cracked": hits,
            "total": len(passwords), "lookup_s": time.perf_counter() - t1}

def salted_attack(passwords=("password", "123456", "admin")):
    table = {h("sha256", w): w for w in WORDLIST}
    hits = sum(hashlib.sha256(os.urandom(8) + p.encode()).hexdigest() in table for p in passwords)
    return {"cracked_with_salt": hits, "total": len(passwords)}
