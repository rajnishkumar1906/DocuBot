from langchain_community.embeddings import SentenceTransformerEmbeddings

DEFAULT_MODEL = "all-MiniLM-L6-v2"

def get_embedder(model_name: str = DEFAULT_MODEL):
    return SentenceTransformerEmbeddings(model_name=model_name)