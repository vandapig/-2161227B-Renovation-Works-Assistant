import os, streamlit as st
from utils.rag import rebuild_index_from_folders

st.set_page_config(page_title="Upload Documents", page_icon="📤", layout="wide")
st.title("📤 Case 0 — Upload PDFs")

upload_dir = "data/uploads"
os.makedirs(upload_dir, exist_ok=True)

files = st.file_uploader("Select one or more PDFs", type=["pdf"], accept_multiple_files=True)
if st.button("Save & Rebuild Index") and files:
    count = 0
    for f in files:
        path = os.path.join(upload_dir, f.name)
        with open(path, "wb") as out:
            out.write(f.read())
        count += 1
    st.success(f"Saved {count} file(s). Rebuilding index…")
    st.session_state.rag = rebuild_index_from_folders(["data/guides", "data/uploads"])
    st.session_state.indexed_files = sorted(os.listdir("data/guides")) + sorted(os.listdir("data/uploads"))
    st.success("Index rebuilt. Go back to Home / Case 1 to chat.")