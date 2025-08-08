import streamlit as st
import os

st.set_page_config(page_title="Methodology", page_icon="🛠", layout="wide")

st.title("🛠 Methodology")

st.markdown("""
This application uses **Retrieval‑Augmented Generation (RAG)**. At startup it loads PDFs, extracts text, chunks, embeds, and builds a local, file‑based vector index. Queries then retrieve top matches for grounded answers.

### Data Flow
1. **Load** – PDFs from `data/guides/` and any uploads from `data/uploads/`.
2. **Extract** – Text extracted with `pypdf`.
3. **Chunk** – Text split into overlapping sections for better recall.
4. **Embed** – OpenAI embeddings for each chunk.
5. **Index** – Stored in Chroma (persistent) under `vectorstore/`.
6. **Query** – User question/keywords embedded and matched via cosine similarity.
7. **Answer** – For Case 1, the LLM forms a response using retrieved context; for Case 2, snippets are shown directly.
""")

st.subheader("Case 1 — Chat with Preloaded Guides")
case1_path = "assets/flowcharts/case1_flowchart.png"
if os.path.exists(case1_path):
    st.image(case1_path, caption="Flowchart — Case 1", use_container_width=True)
else:
    st.info(f"Add flowchart image at: {case1_path}")

st.subheader("Case 2 — Intelligent Search")
case2_path = "assets/flowcharts/case2_flowchart.png"
if os.path.exists(case2_path):
    st.image(case2_path, caption="Flowchart — Case 2", use_container_width=True)
else:
    st.info(f"Add flowchart image at: {case2_path}")
