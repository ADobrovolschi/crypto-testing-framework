import logging, time
from pathlib import Path

def get_logger(name="cryptolab", logfile="results/cryptolab.log"):
    Path(logfile).parent.mkdir(parents=True, exist_ok=True)
    log = logging.getLogger(name)
    if not log.handlers:
        log.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        for h in (logging.StreamHandler(), logging.FileHandler(logfile)):
            h.setFormatter(fmt)
            log.addHandler(h)
    return log

def timed(fn, *a, repeat=3, **kw):
    """Return (result, best time in seconds)."""
    best, res = float("inf"), None
    for _ in range(repeat):
        t = time.perf_counter()
        res = fn(*a, **kw)
        best = min(best, time.perf_counter() - t)
    return res, best
