# This sets up a lightweight MCP-style chatbot using Ollama locally
# It bypasses LangChain function-calling agents and uses prompt composition.
import json
import os
import requests
from rapidfuzz import process

from app.core.utils.user_util import get_user_profile_summary
from app.data.investment_data import extended_investment_db
from app.models.user import User
from app.llm.fund_commentry_rag import build_fund_rag_index
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# -------------------------------------------------
# Fuzzy Fund Resolver Utility
# -------------------------------------------------

def resolve_fund_name(user_input: str, fund_names: list[str], threshold: int = 80) -> str | None:
    match, score, _ = process.extractOne(user_input.lower(), fund_names)
    return match if score >= threshold else None

# -------------------------------------------------
# Structured Fund Info
# -------------------------------------------------

def get_fund_metadata(fund_query: str) -> dict:
    fund_name = resolve_fund_name(fund_query, extended_investment_db.keys())
    if not fund_name:
        return {"error": f"Could not identify fund for input: '{fund_query}'"}
    return extended_investment_db[fund_name]

# -------------------------------------------------
# RAG Retriever (FAISS + LangChain)
# -------------------------------------------------

def load_fund_rag_vector_store(index_dir="faiss_index"):
    if not os.path.exists(os.path.join(index_dir, "index.faiss")):
        print("⚠️ Index not found. Building RAG index...")
        build_fund_rag_index()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

vectorstore = load_fund_rag_vector_store()

def search_fund_rag(query: str, fund_query: str = "") -> list:
    fund_name = resolve_fund_name(fund_query, extended_investment_db.keys()) if fund_query else None
    if fund_name:
        results = vectorstore.similarity_search(query, k=4, filter={"fund": fund_name})
    else:
        results = vectorstore.similarity_search(query, k=4)
    return [doc.page_content for doc in results]

# -------------------------------------------------
# User Profile Summary
# -------------------------------------------------

def summarize_user_profile(user_dict: dict) -> str:
    user = User(**user_dict)
    summary = get_user_profile_summary(user)
    lines = [f"Name: {summary['name']}", f"Risk Profile: {summary['risk_profile']}",
             f"Monthly Surplus: ₹{summary['monthly_surplus']:.2f}",
             "Emergency Fund Adequate: ✅" if summary['has_emergency_fund'] else "Emergency Fund Adequate: ❌"]
    if summary['goal_breakdown']:
        lines.append("\nGoals:")
        for term, goals in summary['goal_breakdown'].items():
            lines.append(f"- {term.replace('_', ' ').title()}: {', '.join(goals) if goals else 'None'}")
    if summary['loan_obligations']:
        lines.append(f"\nActive Loans: {', '.join(summary['loan_obligations'])}")
    return "\n".join(lines)

# -------------------------------------------------
# Ollama Local Chat Engine
# -------------------------------------------------

def query_ollama(prompt: str, model="llama3.2:latest") -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": True
            },
            stream=True,
            timeout=60
        )

        full_output = ""
        for chunk in response.iter_lines():
            if chunk:
                try:
                    data = json.loads(chunk.decode("utf-8"))
                    full_output += data.get("response", "")
                except json.JSONDecodeError:
                    continue
        return full_output.strip()
    except Exception as e:
        return f"[Ollama Error] {e}"

# -------------------------------------------------
# MCP-style Advisor Chat Handler
# -------------------------------------------------

def run_chatbot(message: str, user_profile: dict, fund_query: str = "") -> str:
    fund_name = resolve_fund_name(fund_query, list(extended_investment_db.keys())) if fund_query else None
    fund_meta = extended_investment_db.get(fund_name) if fund_name else None

    # 1. Summarize user
    try:
        user = User(**user_profile)
        user_summary = get_user_profile_summary(user)
    except Exception as e:
        user_summary = f"Could not summarize user: {e}"

    # 2. Search RAG
    rag_context = ""
    if fund_name:
        try:
            rag_docs = vectorstore.similarity_search(message, k=4, filter={"fund": fund_name})
            rag_context = "\n\n".join([doc.page_content for doc in rag_docs])
        except Exception as e:
            rag_context = f"Could not retrieve RAG documents: {e}"

    # 3. Build full prompt
    prompt_parts = ["You are a financial advisor helping a client with a specific investment question.\n",
                    "=== USER PROFILE ===\n" + str(user_summary)]

    if fund_name:
        prompt_parts.append(f"=== FUND NAME ===\n{fund_name}")

    if fund_meta:
        fund_info = "\n".join([f"{k}: {v}" for k, v in fund_meta.items()])
        prompt_parts.append(f"=== FUND METADATA ===\n{fund_info}")

    if rag_context:
        prompt_parts.append(f"=== RAG CONTEXT ===\n{rag_context}")

    prompt_parts.append(f"=== USER QUESTION ===\n{message.strip()}")

    full_prompt = "\n\n".join(prompt_parts)

    # 4. Send to Ollama
    return query_ollama(full_prompt)

# Example usage:
# response = run_chatbot("What are the risks of this fund?", user_profile_dict, fund_query="ICICI Long Term")
# print(response)
