"""Hash functions: avalanche, comparison, performance, salting, integrity."""
import hashlib, os
from .utils import timed

ALGOS = ["md5", "sha1", "sha256", "sha512", "sha3_256"]
STATUS = {"md5": "Deprecated", "sha1": "Obsolete", "sha256": "Recommended",
          "sha512": "Very strong", "sha3_256": "Recommended"}

def h(algo, data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.new(algo, data).hexdigest()

def bit_diff_percent(h1, h2):
    return bin(int(h1, 16) ^ int(h2, 16)).count("1") / (len(h1) * 4) * 100

def avalanche(base="password123", variants=("password124", "Password123")):
    out = []
    for algo in ["md5", "sha1", "sha256"]:
        hb = h(algo, base)
        for v in variants:
            out.append({"algorithm": algo, "input_a": base, "input_b": v,
                        "bit_diff_pct": bit_diff_percent(hb, h(algo, v))})
    return out

def compare(text="This is a text for testing hash functions"):
    return [{"algorithm": a, "bits": hashlib.new(a).digest_size * 8,
             "hash": h(a, text), "status": STATUS[a]} for a in ALGOS]

def performance(sizes=(1024, 102400, 1048576)):
    out = []
    for size in sizes:
        data = os.urandom(size)
        for a in ["md5", "sha256", "sha512"]:
            _, t = timed(h, a, data, repeat=5)
            out.append({"size_bytes": size, "algorithm": a, "time_s": t,
                        "mb_s": size / 1e6 / t if t else 0})
    return out

def salt_demo(password="password123", users=3):
    no_salt = [h("sha256", password) for _ in range(users)]
    salted = []
    for _ in range(users):
        salt = os.urandom(8)
        salted.append({"salt": salt.hex(), "hash": hashlib.sha256(salt + password.encode()).hexdigest()})
    return {"no_salt": no_salt, "all_identical_no_salt": len(set(no_salt)) == 1,
            "salted": salted, "all_unique_salted": len({s["hash"] for s in salted}) == users}

def integrity_demo():
    ha = h("sha256", "Important document with confidential information")
    hb = h("sha256", "Important document with MODIFIED information")
    return {"original": ha, "modified": hb, "tamper_detected": ha != hb}
