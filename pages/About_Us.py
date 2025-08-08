import streamlit as st

st.set_page_config(page_title="About Us", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About Us")
st.markdown("""
The **BCA and HDB Renovation Works Assistant** is developed as part of the **AI Bootcamp Capstone Project**.

### 🎯 Scope & Objectives
- **Centralise** official renovation rules from BCA/HDB (PDFs).
- **Personalise** answers via AI chat grounded in retrieved context.
- **Simplify** complex guidelines into clear, concise language.
- **Engage** users with interactive chat and search.

### 📚 Sources
- Official **BCA** & **HDB** renovation guides (PDFs placed under `data/guides/`).

### 🚀 Current Version Features
1. **Case 1** — Chat with preloaded documents (RAG Q&A with sources)
2. **Case 2** — Intelligent key word search
3. **Case 0** — Upload documents to expand the knowledge base
""")
