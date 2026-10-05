from cryptolab import hashing, attacks, symmetric

def test_known_sha256():
    assert hashing.h("sha256", "password") == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

def test_avalanche_near_50():
    assert all(35 < r["bit_diff_pct"] < 65 for r in hashing.avalanche())

def test_salt_unique():
    d = hashing.salt_demo()
    assert d["all_identical_no_salt"] and d["all_unique_salted"]

def test_dictionary_cracks_weak():
    assert attacks.dictionary_attack(hashing.h("md5", "admin"), "md5")["cracked"]

def test_salted_attack_fails():
    assert attacks.salted_attack()["cracked_with_salt"] == 0

def test_symmetric_integrity():
    assert all(r["integrity_ok"] for r in symmetric.benchmark(sizes=(1024,)))
