from langchain_community.embeddings import SentenceTransformerEmbeddings

DEFAULT_MODEL = "all-MiniLM-L6-v2"

def get_embedder(model_name: str = DEFAULT_MODEL):
    """
    Return a SentenceTransformer embedding model on CPU to avoid meta tensor errors.
    """
    return SentenceTransformerEmbeddings(model_name=model_name, model_kwargs={"device": "cpu"})