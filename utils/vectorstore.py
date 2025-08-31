import chromadb
from pathlib import Path
from langchain_community.vectorstores import Chroma
from utils.embedder import get_embedder
from langchain.schema import Document

def get_vectorstore(persist_dir: Path, collection_name: str = "docubot") -> Chroma:
    """Initializes and returns a persistent Chroma vector store."""
    embeddings = get_embedder()
    
    # Use the `Chroma` constructor directly with persist_directory
    # This is the more stable and recommended way for a local vector store
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(persist_dir)
    )

def index_documents(vs: Chroma, documents: list[Document]) -> int:
    """Indexes a list of documents into the Chroma vectorstore."""
    # This assumes the vectorstore is already initialized and persistent
    vs.add_documents(documents)
    vs.persist()
    return len(documents)
