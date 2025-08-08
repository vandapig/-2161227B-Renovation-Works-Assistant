import os, glob, streamlit as st
from utils.rag import rebuild_index_from_folders
import sys
try:
    import pysqlite3 as sqlite3  # type: ignore
    sys.modules['sqlite3'] = sqlite3
except Exception:
    pass
    
st.set_page_config(page_title="BCA and HDB Renovation Works Assistant", page_icon="🧱", layout="wide")

# ---- Hardcoded login ----
USERNAME = "admin"
PASSWORD = "BCA_123_Reno"

def login():
    st.title("🧱 Renovation Works Assistant")
    st.caption("RAG-enabled Q&A on renovation guidelines by BCA and HDB — preloaded docs + uploads.")

    # Mandatory Disclaimer in expander
    with st.expander("IMPORTANT NOTICE (click to expand)", expanded=True):
        st.markdown("""
**This web application is a prototype for educational purposes only.**  
The information provided here is **NOT** intended for real-world usage and **should not** be relied upon for decisions, especially those related to financial, legal, or healthcare matters.

LLMs may generate inaccurate or incorrect information. **You are responsible** for how you use any generated output.

Always consult qualified professionals for accurate and personalized advice.
        """)

    if "auth" not in st.session_state:
        st.session_state.auth = False

    if not st.session_state.auth:
        with st.form("login-form", clear_on_submit=False):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in")
            if submitted:
                if u == USERNAME and p == PASSWORD:
                    st.session_state.auth = True
                    st.success("Logged in! Loading guides…")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
                    st.stop()

login()

# ---- Build / load index once per session ----
if "rag" not in st.session_state:
    st.session_state.rag = None
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []

if st.session_state.rag is None:
    os.makedirs("data/uploads", exist_ok=True)
    guides = sorted(glob.glob("data/guides/*.pdf"))
    uploads = sorted(glob.glob("data/uploads/*.pdf"))
    with st.spinner(f"Indexing {len(guides) + len(uploads)} PDF(s)…"):
        st.session_state.rag = rebuild_index_from_folders(["data/guides", "data/uploads"], chunk_size=1000, chunk_overlap=200)
        st.session_state.indexed_files = [os.path.basename(p) for p in guides + uploads]
    st.success("Index ready.")

# ---- Sidebar ----
st.sidebar.header("Navigation")
st.sidebar.page_link("pages/About_Us.py", label="About Us")
st.sidebar.page_link("pages/Methodology.py", label="Methodology")
st.sidebar.page_link("app.py", label="Home / Case 1 (Chat)")
st.sidebar.page_link("pages/Case_0_Upload_Documents.py", label="Case 0 — Upload Documents")
st.sidebar.page_link("pages/Case_2_Intelligent_Search.py", label="Case 2 — Intelligent Search")


# ---- Show loaded PDFs ----
st.subheader("📄 Loaded Guides")
st.write(", ".join(st.session_state.indexed_files) if st.session_state.indexed_files else "_No PDFs found yet._")

# ---- Case 1: Chat ----
st.markdown("### 💬 Case 1 — Chat with the renovation guides")

if "history" not in st.session_state:
    st.session_state.history = []

for role, content in st.session_state.history:
    with st.chat_message(role):
        st.write(content)

user_q = st.chat_input("Ask a question about the renovation guides…")
if user_q:
    st.session_state.history.append(("user", user_q))
    with st.chat_message("user"):
        st.write(user_q)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            answer, refs = st.session_state.rag.query(user_q, k=3)
            st.markdown(answer)
            if refs:
                with st.expander("Show sources"):
                    for i, (content, meta) in enumerate(refs, 1):
                        src = meta.get("source", "unknown")
                        st.markdown(f"**Source {i} — {src}:**")
                        st.write(content[:1200] + ("…" if len(content) > 1200 else ""))
            st.session_state.history.append(("assistant", answer))
