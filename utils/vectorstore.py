from pathlib import Path
from typing import List
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from .embedder import get_embedder

def get_vectorstore(persist_dir: Path, collection_name: str = "docubot") -> Chroma:
    embeddings = get_embedder()
    return Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings,
        collection_name=collection_name,
    )

def index_documents(vs: Chroma, chunks: List[Document]) -> int:
    if not chunks:
        return 0
    vs.add_documents(chunks)
    vs.persist()
    return len(chunks)
