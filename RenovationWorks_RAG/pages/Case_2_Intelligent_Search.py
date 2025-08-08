import streamlit as st

st.set_page_config(page_title="Case 2 — Intelligent Keyword Search", page_icon="🔎", layout="wide")
st.title("🔎 Case 2 — Intelligent Keyword Search")

if "rag" not in st.session_state or st.session_state.rag is None:
    st.warning("Index is not loaded yet. Go back to Home to initialize the guides.")
    st.stop()

rag = st.session_state.rag

q = st.text_input("Enter a search phrase (e.g., 'false ceiling requirements', 'mezzanine approval'):")
st.markdown("*Tip: The search looks through all preloaded renovation guides and returns the most relevant text snippets.*")

topk = st.slider(
    "Number of results to show",
    1, 10, 5,
    help="How many of the most relevant snippets to display. For example, 3 shows the top three matches."
)

if st.button("Search") and q.strip():
    with st.spinner("Searching…"):
        results = rag.retrieve(q, k=topk)
    st.markdown(f"### Results for: `{q}`")
    for i, (content, meta, score) in enumerate(results, 1):
        src = meta.get("source", "unknown")
        st.markdown(f"**{i}. {src} — score: `{score:.4f}`**")
        st.write(content[:1200] + ("…" if len(content) > 1200 else ""))