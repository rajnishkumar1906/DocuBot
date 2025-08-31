import streamlit as st
from pathlib import Path
import PyPDF2
import docx
import re
from utils.loader import chunk_documents
from utils.vectorstore import get_vectorstore, index_documents
from utils.rag_chain import answer_query, retrieve
from langchain.schema import Document

# ----------------------------
# Helpers
# ----------------------------
def clean_markdown(text: str) -> str:
    """Removes common markdown artifacts for cleaner display."""
    text = text.replace("###", "\n").replace("**", "")
    text = text.replace("* ", "• ")
    text = re.sub(r"[*#`_>-]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_text(file):
    """Extract text from TXT, PDF, or DOCX files."""
    try:
        if file.type == "text/plain":
            return file.read().decode("utf-8")
        elif file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        elif file.type in [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
        ]:
            doc = docx.Document(file)
            return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        st.warning(f"⚠️ Could not read {file.name}: {e}")
    return ""

# ----------------------------
# Setup directories & session state
# ----------------------------
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
PERSIST_DIR = BASE_DIR / "data"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
PERSIST_DIR.mkdir(parents=True, exist_ok=True)

if "vs" not in st.session_state:
    st.session_state.vs = get_vectorstore(PERSIST_DIR)
if "history" not in st.session_state:
    st.session_state.history = []
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

st.set_page_config(page_title="DocuBot", layout="wide")

# ----------------------------
# Theme selection
# ----------------------------
theme = st.radio("Theme", ["☀️ Light", "🌙 Dark"], horizontal=True, label_visibility="collapsed")
if theme.startswith("☀️"):
    body_bg = "linear-gradient(135deg, #f0f4ff, #e0f7fa)"
    chat_bg = "#ffffff"
    bot_bg = "#f0f2f5"
    bot_color = "#333333"
    user_msg_bg = "linear-gradient(45deg, #00c6ff, #0072ff)"
    user_msg_color = "white"
else:
    body_bg = "linear-gradient(135deg, #1a1a2e, #16213e)"
    chat_bg = "#22223b"
    bot_bg = "#3a3f47"
    bot_color = "#f0f0f0"
    user_msg_bg = "linear-gradient(45deg, #3f51b5, #2196f3)"
    user_msg_color = "white"

# ----------------------------
# CSS Styling
# ----------------------------
st.markdown(f"""
<style>
body, .stApp {{ 
    background: {body_bg};
    color: {bot_color}; 
}}
.main-container {{
    display: flex;
    justify-content: space-between;
    height: 100vh;
}}
.left-sidebar {{
    width: 30%;
    padding: 1rem;
    box-sizing: border-box;
    background-color: {body_bg};
}}
.right-content {{
    width: 65%;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    height: 100%;
    box-sizing: border-box;
}}
.chat-container {{
    flex-grow: 1;
    overflow-y: auto;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    border-radius: 12px;
    background: {chat_bg};
    box-shadow: 0 1px 5px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}}
.user-msg {{
    background: {user_msg_bg};
    color: {user_msg_color};
    padding: 10px 14px;
    border-radius: 18px 18px 0 18px;
    max-width: 70%;
    word-wrap: break-word;
    align-self: flex-end;
    font-size: 15px;
}}
.bot-msg {{
    background-color: {bot_bg};
    color: {bot_color};
    padding: 10px 14px;
    border-radius: 18px 18px 18px 0;
    max-width: 70%;
    word-wrap: break-word;
    align-self: flex-start;
    font-size: 15px;
}}
.file-card {{
    background: #e0f7fa;
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 5px;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}}
.file-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}
.stChatInput {{
    position: sticky;
    bottom: 0;
    width: 100%;
    z-index: 1000;
}}
/* New rule to fix the file uploader label color in dark mode */
.stApp.dark-mode .stFileUploader label p,
.stApp.dark-mode .stFileUploader label span {{
    color: {bot_color};
}}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Layout
# ----------------------------
left_col, right_col = st.columns([1, 2])

# ----- Left Column: File Upload -----
with left_col:
    st.markdown("## 🤖 DocuBot")
    uploaded_files = st.file_uploader(
        "📂 **Upload your cool files!** (TXT, PDF, DOCX)",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            content = extract_text(file)
            if not content.strip():
                st.warning(f"⚠️ Could not extract text from {file.name}")
                continue

            doc = [Document(page_content=content, metadata={"source": file.name})]
            chunks = chunk_documents(doc)
            count = index_documents(st.session_state.vs, chunks)
            st.session_state.file_uploaded = True

            st.markdown(
                f'<div class="file-card">📄 **{file.name}** — Indexed {count} chunks 🎉</div>',
                unsafe_allow_html=True
            )

# ----- Right Column: Chat -----
with right_col:
    st.markdown("## 💬 Conversation")
    chat_container = st.container(height=500, border=False)
    with chat_container:
        for role, msg in st.session_state.history:
            if role == "User":
                st.markdown(f'<div class="user-msg">{msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg">{msg}</div>', unsafe_allow_html=True)

prompt = st.chat_input("Ask me anything about your documents...")

if prompt:
    st.session_state.history.append(("User", prompt))

    vs = st.session_state.vs

    # Retrieve docs based on the prompt
    retrieved_docs = retrieve(vs, prompt, k=5)

    if not retrieved_docs:
        answer_text = "No relevant content found in the uploaded documents."
    else:
        # Pass the file_uploaded state to the answer_query function
        answer_result = answer_query(
            vs, 
            prompt, 
            st.session_state.history, 
            st.session_state.file_uploaded, 
            k=5
        )
        answer_text = answer_result["answer"]
    
    st.session_state.history.append(("DocuBot", clean_markdown(answer_text)))
    st.rerun()
