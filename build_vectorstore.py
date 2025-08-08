#!/usr/bin/env python3
"""Build a Chroma vectorstore from files under data/guides and data/uploads.

- Skips binary/vectorstore artifacts
- Supports: .txt, .md, .pdf (via pypdf)
- Uses sentence-transformers (all-MiniLM-L6-v2) for embeddings
- Writes to ./vectorstore (gitignored)
"""
import os
import sys
import hashlib
from pathlib import Path
from typing import Iterable, List, Tuple

# SQLite shim must be imported BEFORE chromadb
try:
    import pysqlite3 as sqlite3  # noqa: F401
    sys.modules['sqlite3'] = sqlite3
except Exception:
    pass

import chromadb
from chromadb.utils import embedding_functions

# -------- Config --------
DATA_DIRS = [Path("data/guides"), Path("data/uploads")]
VECTORSTORE_DIR = Path("vectorstore")
COLLECTION_NAME = "renovation_guides"
ALLOWED_EXTS = {".txt", ".md", ".pdf"}
MODEL_NAME = "all-MiniLM-L6-v2"

def iter_files() -> Iterable[Path]:
    for base in DATA_DIRS:
        if not base.exists():
            continue
        for root, _, files in os.walk(base):
            for f in files:
                p = Path(root) / f
                if p.suffix.lower() in ALLOWED_EXTS:
                    yield p

def load_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            print(f"[WARN] Failed to parse PDF: {path}: {e}")
            return ""
    return ""

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
    # Simple whitespace chunker
    if not text:
        return []
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += max(1, chunk_size - overlap)
    return chunks

def make_id(path: Path, idx: int, chunk: str) -> str:
    h = hashlib.sha1((str(path) + str(idx) + chunk[:128]).encode("utf-8")).hexdigest()
    return f"{path.stem}-{idx}-{h[:8]}"

def main():
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(VECTORSTORE_DIR))
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
    col = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embed_fn)

    add_count = 0
    for path in iter_files():
        text = load_text(path)
        chunks = chunk_text(text)
        if not chunks:
            continue
        ids = []
        docs = []
        metas = []
        for i, ch in enumerate(chunks):
            ids.append(make_id(path, i, ch))
            docs.append(ch)
            metas.append({"source": str(path)})
        # Chroma de-duplicates by id; safe to re-run
        col.add(ids=ids, documents=docs, metadatas=metas)
        add_count += len(ids)
        print(f"[ADD] {path} -> {len(ids)} chunks")
    print(f"Done. Added/updated {add_count} chunks into collection '{COLLECTION_NAME}' at {VECTORSTORE_DIR}")

if __name__ == "__main__":
    main()
