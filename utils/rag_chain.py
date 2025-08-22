import os
import google.generativeai as genai
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def retrieve(vs: Chroma, query: str, k: int = 4) -> List[Document]:
    """Retrieve top-k relevant documents from Chroma vectorstore."""
    retriever = vs.as_retriever(search_kwargs={"k": k})
    return retriever.get_relevant_documents(query)

def synthesize_answer(query: str, docs: List[Document]) -> str:
    """Generate an answer using Gemini model and retrieved docs."""
    
    # Friendly hardcoded replies for greetings or chit-chat
    greetings = ["hi", "hello", "hey", "good morning", "good evening","good afternoon"]
    if query.lower() in greetings:
        return "👋 Hello! I'm DocuBot, your AI assistant. How can I help you today?"
    if "how are you" in query.lower():
        return "😅 I’m just code, but I’m ready to assist you with your notes!"

    if not docs:
        return "🤖 I don’t know about this from the given documents."

    # Combine retrieved chunks into context
    context = "\n\n".join([d.page_content for d in docs])

    # Call Gemini API
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"""
        You are DocuBot, a helpful assistant. Use only the context below to answer.
        Answer naturally and clearly.

        Context:
        {context}

        Question:
        {query}

        If the answer is not present in the context, reply:
        "🤖 I don’t know about this from the given documents."
        """
    )

    return response.text.strip()

def answer_query(vs: Chroma, query: str, k: int = 4) -> Dict[str, Any]:
    """Main pipeline: retrieve, synthesize, and return answer + sources."""
    docs = retrieve(vs, query, k=k)
    answer = synthesize_answer(query, docs)

    # Extract sources (file paths from metadata)
    sources = list({d.metadata.get("source", "unknown") for d in docs})

    return {
        "answer": answer,
        "sources": sources
    }
