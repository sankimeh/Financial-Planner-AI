from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import requests

# Load the vector store
def load_vector_store(index_dir="faiss_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

# Query Ollama with context
def query_ollama_with_context(user_query: str, k: int = 5):
    # Step 1: Load vector store
    vectorstore = load_vector_store()

    # Step 2: Get top k relevant documents
    results = vectorstore.similarity_search(user_query, k=k)
    context_chunks = "\n\n".join([doc.page_content[:2000] for doc in results])  # truncate to avoid overload

    # Step 3: Construct prompt
    prompt = f"""You are a financial advisor AI. Based on the documents and reports below, give a recommendation in plain English.

### User Query:
{user_query}

### Context from reports and financial data:
{context_chunks}

Only use the context if it's helpful. Be concise but informative. Classify the recommendation as short-term, mid-term, or long-term. 
"""

    # Step 4: Query Ollama (streaming)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:latest",
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    print("🧠 Ollama Response:")
    for chunk in response.iter_lines():
        if chunk:
            print(chunk.decode("utf-8"), end="", flush=True)

if __name__ == "__main__":
    user_input = input("Enter your investment goal or risk profile query: ")
    query_ollama_with_context(user_input)
