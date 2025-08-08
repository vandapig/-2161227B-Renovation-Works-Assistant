# 🧱 BCA and HDB Renovation Work Assistant

This application runs on:
- Streamlit UI + **hardcoded login** (`admin` / password in code)
- **One LLM (OpenAI)** for embeddings & chat
- **RAG** over static docs
- **File‑based vector store (Chroma) with persistence** in `vectorstore/`


## ✨ Features
- **Case 1 — Chat with Preloaded Documents** (RAG Q&A with sources)
- **Case 2 — Intelligent Search / Snippet Explorer** (top‑k snippets + scores)
- **Case 0 — Upload Documents** (add PDFs to index at runtime)

## 📦 Folder Structure
```
bca_renovation_assistant_v1_compliance/
├─ app.py
├─ pages/
│  ├─ Case_0_Upload_Documents.py
│  ├─ Case_2_Intelligent_Search.py
│  ├─ About_Us.py
│  └─ Methodology.py
├─ utils/
│  └─ rag.py
├─ assets/
│  └─ flowcharts/
│     ├─ PUT_FLOWCHARTS_HERE.txt
│     ├─ case1_flowchart.png
│     └─ case2_flowchart.png
├─ data/
│  ├─ guides/   (preload PDFs here)
│  └─ uploads/  (user uploads stored here)
├─ vectorstore/ (created at runtime by Chroma)
├─ requirements.txt
└─ .streamlit/
   └─ config.toml
```

## ⚙️ Setup (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 🔑 Configure API Key
Add your OpenAI key via either:
- **Env var (quick):**
  ```powershell
  $env:OPENAI_API_KEY = "sk-..."
  ```
- **Or** Streamlit secrets (optional for deployment):
  Create `.streamlit/secrets.toml` with
  ```toml
  OPENAI_API_KEY = "sk-..."
  ```

## ▶️ Run
```powershell
python -m streamlit run app.py
```

**Login:**  
- Username: `admin`  
- Password: (hardcoded in `app.py`, default: `BCA_123_Reno`)

## 🖼 Flowcharts
Put your PNGs here:
```
assets/flowcharts/case1_flowchart.png
assets/flowcharts/case2_flowchart.png
```
The Methodology page will display them automatically.

## 🚀 Notes
- New PDFs uploaded via **Case 0** are saved to `data/uploads/` and the index is rebuilt.
- Vector store persists under `vectorstore/`, so the app can reuse it between runs.