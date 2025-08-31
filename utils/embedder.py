from langchain_community.embeddings import HuggingFaceEmbeddings

DEFAULT_MODEL = "all-MiniLM-L6-v2"

def get_embedder(model_name: str = DEFAULT_MODEL):
    """
    Return a HuggingFace embedding model explicitly on the CPU.
    """
    # The device parameter is passed directly to the model initialization.
    model_kwargs = {"device": "cpu"}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs
    )
