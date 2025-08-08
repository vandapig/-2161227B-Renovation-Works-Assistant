"""Call ensure_vectorstore() early in your app to build the index if missing."""
import os
from pathlib import Path
import subprocess
import sys

def ensure_vectorstore():
    vs_dir = Path("vectorstore")
    if vs_dir.exists() and any(vs_dir.iterdir()):
        return  # looks populated
    print("[info] vectorstore missing or empty; building...")
    # Run builder with current interpreter to reuse env
    result = subprocess.run([sys.executable, "build_vectorstore.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError("Failed to build vectorstore")
    print("[info] vectorstore built.")

if __name__ == "__main__":
    ensure_vectorstore()
