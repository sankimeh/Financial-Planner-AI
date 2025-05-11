import os
import json

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import requests

from app.llm.rag_recommender import build_financial_rag


# Load the vector store
def load_vector_store(index_dir="faiss_index"):
    if not os.path.exists(os.path.join(index_dir, "index.faiss")):
        print("⚠️ Index not found. Rebuilding...")
        build_financial_rag()  # imports this or move it into a shared utils module
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)


# Query Ollama with context
def query_ollama_with_context(user_query: str, k: int = 5):
    vectorstore = load_vector_store()
    results = vectorstore.similarity_search(user_query, k=k)
    context_chunks = "\n\n".join([doc.page_content[:2000] for doc in results])

    prompt = f"""You are a financial advisor AI. Based on the documents and reports below, give a recommendation in plain English.

### User Query:
{user_query}

### Context from reports and financial data:
{context_chunks}

Only use the context if it's helpful. Be concise but informative. Classify the recommendation as short-term, mid-term, or long-term.
"""

    print("🧠 Ollama Response:\n")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:latest",
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    full_output = ""
    for chunk in response.iter_lines():
        if chunk:
            try:
                data = json.loads(chunk.decode("utf-8"))
                full_output += data.get("response", "")
            except json.JSONDecodeError:
                continue  # Ignore malformed chunks

    print(full_output.strip())  # Clean and print only the model's final text

if __name__ == "__main__":
    user_input = input("Enter your investment goal or risk profile query: ")
    query_ollama_with_context(user_input)
