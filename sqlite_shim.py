# Ensure systems with old stdlib sqlite can still load a new-enough sqlite3 via pysqlite3-binary
import sys
try:
    import pysqlite3 as sqlite3  # type: ignore
    sys.modules['sqlite3'] = sqlite3
except Exception:
    # If import fails we fall back to stdlib sqlite3; Chroma may error if version < 3.35
    pass
