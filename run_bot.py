from pathlib import Path
from utils.loader import ensure_dirs, find_files, load_documents, chunk_documents
from utils.vectorstore import get_vectorstore, index_documents
from utils.rag_chain import answer_query
import re

# --- Formatting helpers ---
def clean_markdown(text: str) -> str:
    """Remove unnecessary Markdown symbols for cleaner console output."""
    text = text.replace("###", "\n").replace("**", "")
    text = text.replace("* ", "• ")  # convert bullets
    text = re.sub(r"[*#`_>-]+", "", text)  # clean extra symbols
    text = re.sub(r"\s+", " ", text)       # collapse extra spaces
    return text.strip()


# --- Paths ---
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
PERSIST_DIR = BASE_DIR / "data"

# Ensure folders exist
ensure_dirs(DOCS_DIR, PERSIST_DIR)

# Make sure memory file exists
MEMORY_FILE = DOCS_DIR / "memory.txt"
if not MEMORY_FILE.exists():
    MEMORY_FILE.write_text("This file stores remembered facts.\n")

# --- Index files ---
files = find_files(DOCS_DIR)
if not files:
    print("⚠️ No files found in docs/. Please add some files.")
else:
    docs = load_documents(files)
    chunks = chunk_documents(docs)
    vs = get_vectorstore(PERSIST_DIR)
    n = index_documents(vs, chunks)
    print(f"✅ Indexed {n} chunks from {len(files)} file(s).")

# --- Conversation history ---
conversation_history = []

# --- Q&A loop ---
while True:
    query = input("\n❓ Ask your question (or type 'exit' to quit): ").strip()
    if query.lower() in ["exit", "quit"]:
        print("👋 Exiting. Bye!")
        break

    # Handle memory command
    if query.lower().startswith("remember "):
        memory_fact = query[9:].strip()
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{memory_fact}")
        # Dynamically index the new memory
        new_docs = load_documents([MEMORY_FILE])
        new_chunks = chunk_documents(new_docs)
        index_documents(vs, new_chunks)
        print("💾 Saved to memory and updated vector store!")
        continue

    # Add user message to history
    conversation_history.append({"role": "user", "content": query})

    # Retrieve + answer
    result = answer_query(vs, query, k=4)

    print("\n🧠 Answer:\n")
    print(clean_markdown(result["answer"]))

   
    # Save bot reply to history
    conversation_history.append({"role": "assistant", "content": result["answer"]})
