"""Main orchestrator: tests -> benchmarks -> attacks -> report."""
import argparse, sys
from . import asymmetric, attacks, benchmarks, hashing, reporting, symmetric
from .utils import get_logger

def step(log, name, fn, results):
    log.info("Running: %s", name)
    try:
        results[name] = fn()
    except Exception as e:
        log.error("Failed %s: %s", name, e)
        results[name] = {"error": str(e)}

def main(argv=None):
    ap = argparse.ArgumentParser(description="CryptoLab")
    ap.add_argument("--quick", action="store_true", help="small file sizes only")
    ap.add_argument("--out", default="results", help="output directory")
    args = ap.parse_args(argv)
    log = get_logger(logfile=f"{args.out}/cryptolab.log")
    sizes = (1024, 102400) if args.quick else (1024, 102400, 1048576, 10485760)
    r = {}
    step(log, "symmetric", lambda: symmetric.benchmark(sizes), r)
    step(log, "asymmetric", asymmetric.benchmark, r)
    step(log, "hash_avalanche", hashing.avalanche, r)
    step(log, "hash_compare", hashing.compare, r)
    step(log, "hash_performance", hashing.performance, r)
    step(log, "salt_demo", hashing.salt_demo, r)
    step(log, "integrity_demo", hashing.integrity_demo, r)
    step(log, "attack_dictionary", attacks.run_dictionary, r)
    step(log, "attack_rainbow", attacks.rainbow_table_attack, r)
    step(log, "attack_salted", attacks.salted_attack, r)
    step(log, "openssl_speed", benchmarks.openssl_speed, r)
    log.info("JSON: %s", reporting.save_json(r, f"{args.out}/results.json"))
    log.info("HTML: %s", reporting.save_html(r, f"{args.out}/report.html"))
    return 0

if __name__ == "__main__":
    sys.exit(main())
