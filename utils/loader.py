from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

ALLOWED_EXTS = {".txt", ".md", ".py", ".json", ".csv"}

def ensure_dirs(docs_dir: Path, persist_dir: Path) -> None:
    docs_dir.mkdir(parents=True, exist_ok=True)
    persist_dir.mkdir(parents=True, exist_ok=True)

def find_files(root: Path) -> List[Path]:
    return [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in ALLOWED_EXTS]

def load_documents(paths: List[Path]) -> List[Document]:
    docs: List[Document] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            docs.append(Document(page_content=text, metadata={"source": str(path)}))
        except Exception:
            continue
    return docs

def chunk_documents(docs: List[Document], chunk_size=500, chunk_overlap=50) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(docs)
