# DocuBot: Your Personal AI Knowledge Base 🤖

**DocuBot** is a private, local-first AI assistant that helps you interact with your own documents. Using a **Retrieval-Augmented Generation (RAG)** pipeline, it provides a conversational interface to answer questions, summarize content, and extract information directly from your personal files.

## ✨ Key Features

* **100% Private:** Your files and data never leave your computer. All processing and model inference happen locally for complete privacy.
* **Conversational Q&A:** Ask natural language questions like, "What were the key findings from the Q3 report?" and get instant, fact-based answers.
* **Multi-Format Support:** Chat with documents in multiple formats, including **TXT**, **PDF**, and **DOCX**.
* **Offline Access:** Works without an internet connection, so your knowledge base is always available.
* **Lightweight & Efficient:** Minimal dependencies allow smooth performance on personal machines.

## 🚀 Getting Started

Follow these instructions to set up DocuBot on your local machine.

### Prerequisites

* **Python 3.8+**
* Command-line interface (Terminal, PowerShell, etc.)

### Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/your-username/DocuBot.git
cd DocuBot
```

2. **Create and Activate a Virtual Environment:**

```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

> Ensure your `requirements.txt` includes essential libraries such as `streamlit`, `chromadb`, `sentence-transformers`, `google-generativeai`, and `python-dotenv`.

4. **Run the Application:**

```bash
streamlit run app.py
```

### How to Use

1. **Upload Files:** Use the file uploader to add your documents.
2. **Indexing:** The app automatically processes and indexes your documents. A confirmation message appears for each successfully indexed file.
3. **Start Chatting:** Use the chat input to ask questions. DocuBot retrieves relevant information and generates concise answers.

---

## 🧠 Behind the Scenes: The RAG Pipeline

DocuBot relies on a RAG system that combines vector search with LLM generation:

* **Streamlit:** Provides the interactive web interface.
* **Sentence-Transformers:** Generates **vector embeddings** for semantic understanding of document chunks.
* **ChromaDB:** Stores embeddings and performs efficient similarity search to retrieve relevant content.
* **Google Gemini 1.5 Flash:** Processes retrieved content and the user query to generate precise, context-aware answers.


Do you want me to do that next?
