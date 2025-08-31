-----

# DocuBot: Your Personal AI Knowledge Base 🤖

**DocuBot** is a private, local-first AI assistant designed to help you interact with your own documents. By leveraging the power of a **Retrieval-Augmented Generation (RAG)** pipeline, it provides a conversational interface that can answer questions, summarize content, and extract information directly from your personal files.

## ✨ Key Features

  * **100% Private:** Your files and data never leave your computer. All document processing and model inference happen locally for complete privacy.
  * **Conversational Q\&A:** Ask natural language questions like, "What were the key findings from the Q3 report?" and get instant, fact-based answers.
  * **Multi-Format Support:** Easily upload and chat with documents in multiple formats, including **TXT**, **PDF**, and **DOCX**.
  * **Offline Access:** The application works without an internet connection, ensuring you always have access to your knowledge base, anywhere, anytime.
  * **Lightweight & Efficient:** Built with a minimal set of dependencies to run smoothly on a personal machine.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You will need **Python 3.8+** and a command-line interface.

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/DocuBot.git
    cd DocuBot
    ```

2.  **Create and Activate a Virtual Environment:**

    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *Make sure to create a `requirements.txt` file with the necessary libraries, such as `streamlit`, `chromadb`, `sentence-transformers`, `google-generativeai`, and `python-dotenv`.*

4.  **Run the Application:**

    ```bash
    streamlit run app.py
    ```

### How to Use

1.  **Upload Files:** Once the application is running in your browser, use the file uploader on the left sidebar to add your documents.
2.  **Indexing:** The application will automatically process the documents and index them. You will receive a confirmation message in the sidebar when each file is ready to be queried.
3.  **Start Chatting:** Use the chat input at the bottom of the page to ask questions about your documents. The RAG system will retrieve the most relevant information to answer your questions.

-----

## 🧠 Behind the Scenes: The RAG Pipeline

DocuBot is built on a sophisticated RAG pipeline. Here's a brief overview of the core technologies and how they work together:

  * **Streamlit:** Provides the interactive web UI, handling all the front-end logic.
  * **Sentence-Transformers:** Used to create **vector embeddings** from the document chunks. These embeddings are numerical representations that capture the semantic meaning of the text.
  * **ChromaDB:** A fast, local **vector database** that stores the embeddings and enables efficient similarity search to find relevant information in your documents.
  * **Google Gemini 1.5 Flash:** The powerful LLM that takes the retrieved document chunks and the user's query to generate a concise and accurate final answer.

-----

## 🤝 Contributions

This is a personal project, but feel free to open issues or suggest features. All feedback is welcome\!

## 📄 License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

To learn how to create a more professional-looking GitHub profile and README, you can watch this video.