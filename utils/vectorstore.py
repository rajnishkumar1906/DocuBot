from pathlib import Path
from typing import List
from langchain_chroma import Chroma
from langchain.schema import Document
from .embedder import get_embedder
import chromadb

def get_vectorstore(persist_dir: Path, collection_name: str = "docubot") -> Chroma:
    """Initializes and returns a persistent Chroma vector store."""
    
    client = chromadb.PersistentClient(path=str(persist_dir))
    embeddings = get_embedder()
    
    return Chroma(
        client=client,
        embedding_function=embeddings,
        collection_name=collection_name,
    )

def index_documents(vs: Chroma, chunks: List[Document]) -> int:
    """Adds document chunks to the vector store."""
    if not chunks:
        return 0
    vs.add_documents(chunks)
    return len(chunks)