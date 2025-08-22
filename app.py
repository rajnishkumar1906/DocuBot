import streamlit as st
from pathlib import Path
from utils.loader import ensure_dirs, find_files, load_documents, chunk_documents
from utils.vectorstore import get_vectorstore, index_documents
from utils.rag_chain import answer_query
import re

# --- Formatting helpers ---
def clean_markdown(text: str) -> str:
    text = text.replace("###", "\n").replace("**", "")
    text = text.replace("* ", "• ")
    text = re.sub(r"[*#`_>-]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# --- Paths ---
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
PERSIST_DIR = BASE_DIR / "data"

ensure_dirs(DOCS_DIR, PERSIST_DIR)

MEMORY_FILE = DOCS_DIR / "memory.txt"
if not MEMORY_FILE.exists():
    MEMORY_FILE.write_text("This file stores remembered facts.\n")

# --- Load and index docs ---
files = find_files(DOCS_DIR)
if not files:
    st.warning("No files found in docs/. Please add some files.")
else:
    docs = load_documents(files)
    chunks = chunk_documents(docs)
    vs = get_vectorstore(PERSIST_DIR)
    n = index_documents(vs, chunks)
    # st.success(f"Indexed {n} chunks from {len(files)} file(s).")

# --- Streamlit UI ---
st.title("🧠 DocuBot Chat")
st.write("Ask questions about your notes and code!")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Type your question here:", "")

if user_input:
    query = user_input.strip()

    # Handle memory command
    if query.lower().startswith("remember "):
        memory_fact = query[9:].strip()
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{memory_fact}")
        new_docs = load_documents([MEMORY_FILE])
        new_chunks = chunk_documents(new_docs)
        index_documents(vs, new_chunks)
        st.success("💾 Saved to memory and updated vector store!")
    else:
        result = answer_query(vs, query, k=4)
        answer = clean_markdown(result["answer"])

        # Save conversation
        st.session_state.history.append(("User", query))
        st.session_state.history.append(("DocuBot", answer))

# Display chat history
for role, msg in st.session_state.history:
    if role == "User":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**DocuBot:** {msg}")
        if "sources" in locals() and result.get("sources"):
            st.markdown(f"*Sources:* {', '.join(result['sources'])}")
