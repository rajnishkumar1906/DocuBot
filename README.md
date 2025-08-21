# DocuBot: Your Personal AI Knowledge Base

**DocuBot** is a private, local-first AI assistant designed to help developers and tech professionals instantly find information within their own codebase, notes, and personal documentation. Tired of searching through countless files to remember how you solved a problem? DocuBot provides a conversational search interface over your fragmented knowledge base.

## 💡 The Core Idea

In a world of cloud-based AI, DocuBot offers a truly personal and secure solution. Instead of sending your sensitive code to a third-party API, DocuBot runs entirely on your local machine, using an intelligent Retrieval-Augmented Generation (RAG) pipeline to give you answers about your own work.

## ✨ Key Features

* **100% Private:** Your code and notes never leave your computer. All processing happens locally.
* **Conversational Search:** Ask natural language questions like, "What was that Python script I used to handle S3 uploads?"
* **Offline Access:** Works without an internet connection, ensuring you always have access to your knowledge base.
* **Lightweight & Efficient:** Built with minimal dependencies to run smoothly on any machine.

## 🚀 Getting Started

These instructions will get a basic version of DocuBot up and running on your local machine.

### Prerequisites

You will need Python 3.8+ and a command-line interface.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/DocuBot.git](https://github.com/your-username/DocuBot.git)
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
    *(Create a `requirements.txt` file with the following contents: `streamlit`, `chromadb`, and `sentence-transformers`)*

4.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```
    *(Make sure you have an `app.py` script as provided in our previous discussion.)*

## 🛠️ Built With

* **[Streamlit](https://streamlit.io/)** - For the interactive web UI.
* **[ChromaDB](https://www.trychroma.com/)** - The local-first, open-source vector database.
* **[Sentence-Transformers](https://www.sbert.net/)** - The framework for generating local embeddings.

## 🤝 Contributions

This is a personal project, but feel free to open issues or suggest features if you find it useful.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.