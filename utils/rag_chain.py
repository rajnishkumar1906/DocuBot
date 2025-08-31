import os
import google.generativeai as genai
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from dotenv import load_dotenv

# Load Gemini API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def retrieve(vs: Chroma, query: str, k: int = 4) -> List[Document]:
    """Retrieve top-k relevant documents from Chroma vectorstore."""
    retriever = vs.as_retriever(search_kwargs={"k": k})
    return retriever.get_relevant_documents(query)

def synthesize_answer(query: str, docs: List[Document], chat_history: List[tuple]) -> str:
    """Generate an answer using Gemini model based on retrieved docs."""
    history_string = "\n".join([f"{role}: {msg}" for role, msg in chat_history])

    greetings = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
    thanks_phrases = ["thanks", "thank you", "nice", "cool", "great"]

    query_lower = query.lower().strip()
    if query_lower in greetings:
        return "👋 Hello! I'm DocuBot, your AI assistant. How can I help you today?"
    if any(phrase in query_lower for phrase in thanks_phrases):
        return "You're welcome! I'm glad I could help."
    if "how are you" in query_lower:
        return "😅 I’m just code, but I’m ready to assist you with your notes!"

    context = "\n\n".join([d.page_content for d in docs]) or "No relevant documents found."

    prompt = f"""
You are DocuBot, an AI assistant. Answer questions using only the uploaded documents and conversation history.

Conversation History:
{history_string}

Context:
{context}

Question:
{query}

Answer:
Answer with bulleted questions.
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating content: {e}")
        return f"Sorry, I couldn't generate an answer due to an error. Please try again. (Error: {e})"

def answer_query(vs: Chroma, query: str, chat_history: List[tuple], k: int = 4) -> Dict[str, Any]:
    """Retrieve documents, generate answer, and return sources."""
    try:
        docs = retrieve(vs, query, k=k)
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return {"answer": "Sorry, I couldn't retrieve documents from the database. Please try again.", "sources": []}
    
    answer = synthesize_answer(query, docs, chat_history)
    sources = list({d.metadata.get("source", "unknown") for d in docs})
    return {"answer": answer, "sources": sources}