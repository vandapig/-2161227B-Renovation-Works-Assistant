import sys
try:
    import pysqlite3 as sqlite3  # type: ignore
    sys.modules['sqlite3'] = sqlite3
except Exception:
    pass
    
import os, glob, pathlib
from typing import List, Tuple

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader

PERSIST_DIR = "vectorstore"

def _extract_text_from_pdf(path: str) -> str:
    parts = []
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            try:
                parts.append(page.extract_text() or "")
            except Exception:
                pass
    except Exception:
        return ""
    return "\n".join(parts)

def _split_texts(texts: List[str], metadatas: List[dict], chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[ "\n\n", "\n", " ", "" ],
    )
    docs, metas = [], []
    for text, meta in zip(texts, metadatas):
        for chunk in splitter.split_text(text):
            docs.append(chunk)
            metas.append(meta)
    return docs, metas

def build_index_from_paths(pdf_paths: List[str], chunk_size=1000, chunk_overlap=200):
    texts, metas = [], []
    for p in pdf_paths:
        pth = pathlib.Path(p)
        if pth.exists() and pth.suffix.lower() == ".pdf":
            txt = _extract_text_from_pdf(str(pth))
            if txt.strip():
                texts.append(txt)
                metas.append({ "source": pth.name })
    if not texts:
        raise RuntimeError("No valid PDFs with extractable text were found.")

    docs, doc_metas = _split_texts(texts, metas, chunk_size, chunk_overlap)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vs = Chroma.from_texts(
        docs,
        embedding=embeddings,
        metadatas=doc_metas,
        persist_directory=PERSIST_DIR,
    )
    vs.persist()
    return RAGHelper(vs)

def rebuild_index_from_folders(folders: List[str], **kw):
    pdfs = []
    for folder in folders:
        pdfs += glob.glob(os.path.join(folder, "*.pdf"))
    pdfs = sorted(set(pdfs))
    return build_index_from_paths(pdfs, **kw)

class RAGHelper:
    def __init__(self, vectorstore: Chroma):
        self.vs = vectorstore
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def query(self, question: str, k: int = 3) -> Tuple[str, List[tuple]]:
        docs = self.vs.similarity_search(question, k=k)
        context = "\n\n---\n\n".join(d.page_content for d in docs)
        messages = [
            {"role": "system", "content": "Answer strictly from CONTEXT. If missing, say you don't know. Keep it clear and cite sources."},
            {"role": "user", "content": f"Question: {question}\n\nCONTEXT:\n{context}"},
        ]
        resp = self.llm.invoke(messages)
        answer = getattr(resp, "content", str(resp))
        refs = [(d.page_content, d.metadata) for d in docs]
        return answer, refs

    def retrieve(self, query: str, k: int = 5):
        docs_scores = self.vs.similarity_search_with_score(query, k=k)
        out = []
        for d, score in docs_scores:
            out.append((d.page_content, d.metadata, float(score)))
        return out
