---
### **DocuBot: A Deep Dive into the RAG Pipeline**

This document provides a detailed explanation of the core technologies and architecture behind the DocuBot application. It's intended for those who want to understand how the project works beyond the basic setup and features.

#### **1. The RAG Pipeline: A Step-by-Step Breakdown**

The DocuBot application is built around a **Retrieval-Augmented Generation (RAG)** pipeline. This system processes and uses your documents to answer questions accurately and privately. The process is divided into two main phases: **Data Ingestion** and **Query Answering**.

**Phase 1: Data Ingestion (What happens when you upload a file?)**

This is the process of taking your raw documents and preparing them for the AI to use.

1.  **Document Loading & Chunking:**
    * The user uploads a file (`.pdf`, `.docx`, `.txt`) via the Streamlit interface.
    * The `loader.py` script reads the raw text from the file.
    * The text is then split into smaller, manageable pieces called **chunks**. This is a crucial step because LLMs have a limited context window, and they cannot process an entire document at once.

2.  **Embedding & Indexing:**
    * Each text chunk is fed into a **Sentence Transformer** model (`all-MiniLM-L6-v2`). This model converts the text into a **vector embedding**—a list of numbers that represents the semantic meaning of the chunk.
    * These vector embeddings, along with their original text chunks, are stored in a local **vector database**, **ChromaDB**. This database is highly optimized for quickly finding similar vectors, which is key for the next phase.

**Phase 2: Query Answering (What happens when you ask a question?)**

This is the core of the RAG system, where the user's question is answered.

1.  **Retrieval:**
    * The user's question is converted into a vector embedding using the same Sentence Transformer model.
    * The system performs a **similarity search** in the ChromaDB. It finds the document chunks whose vector embeddings are numerically closest to the question's embedding. This is known as **semantic search**, as it finds information based on meaning, not just keywords.

2.  **Augmentation & Generation:**
    * The most relevant document chunks are combined with the user's original question to create a single, detailed **augmented prompt**.
    * This augmented prompt is sent to the **Google Gemini 1.5 Flash** LLM.
    * The LLM generates a comprehensive and accurate answer based *only* on the provided context. This process ensures the response is factual and avoids the common LLM problem of "hallucinating" information.
    * The final response is displayed to the user in the chat interface.

#### **2. Core Technologies**

* **Python:** The programming language used to build the entire application.
* **Streamlit:** A powerful Python framework for creating the interactive and user-friendly web interface.
* **ChromaDB:** A lightweight, open-source **vector database** that runs locally on your machine.
* **Sentence-Transformers:** A library used to generate the **vector embeddings** from text.
* **Google Gemini 1.5 Flash:** A large language model that serves as the "brain" of the system, responsible for the final text generation.

---