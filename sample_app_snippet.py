# --- Place these lines at the VERY TOP of your Streamlit app, BEFORE any Chroma import ---
import sys
try:
    import pysqlite3 as sqlite3  # type: ignore
    sys.modules['sqlite3'] = sqlite3
except Exception:
    pass

from ensure_vectorstore import ensure_vectorstore
ensure_vectorstore()

# ... then your usual imports and app code
# import chromadb
# client = chromadb.PersistentClient(path="vectorstore")
# col = client.get_or_create_collection(name="renovation_guides")
