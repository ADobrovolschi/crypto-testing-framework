"""Native `openssl speed` benchmarks."""
import shutil, subprocess

def openssl_speed(algs=("aes-128-cbc", "aes-256-cbc", "sha256", "sha512"), seconds=1):
    if not shutil.which("openssl"):
        return {"available": False, "note": "openssl not installed"}
    out = {}
    for a in algs:
        try:
            r = subprocess.run(["openssl", "speed", "-seconds", str(seconds), "-evp", a],
                               capture_output=True, text=True, timeout=60)
            out[a] = r.stdout.strip().splitlines()[-2:] if r.returncode == 0 else r.stderr.strip()
        except Exception as e:
            out[a] = str(e)
    return {"available": True, "results": out}
