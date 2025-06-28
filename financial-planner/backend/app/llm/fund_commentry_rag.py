import os
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.data.fund_notes import rag_documents_full


# ----------------------------------------
# 1. Sample RAG content (already curated)
# ----------------------------------------



# ----------------------------------------
# 2. Convert to LangChain Documents
# ----------------------------------------

def build_fund_documents():
    documents = rag_documents_full;
    for fund_name, chunks in rag_documents_full.items():
        for chunk in chunks:
            documents.append(Document(page_content=chunk, metadata={"fund": fund_name}))
    return documents

# ----------------------------------------
# 3. Build and Save Vector Store
# ----------------------------------------

def build_fund_rag_index(index_dir="rag_fund_index"):
    print("🚀 Building RAG index for curated fund data...")
    docs = build_fund_documents()
    print(f"📄 Total fund chunks: {len(docs)}")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    os.makedirs(index_dir, exist_ok=True)
    vectorstore.save_local(index_dir)
    print(f"✅ Fund RAG index saved to {index_dir}/")

if __name__ == "__main__":
    build_fund_rag_index()
