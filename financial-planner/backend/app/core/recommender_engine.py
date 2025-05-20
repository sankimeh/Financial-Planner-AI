import os
import json
import requests

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.llm.rag_recommender import build_financial_rag
from app.models.user import User


# Load the vector store
def load_vector_store(index_dir="faiss_index"):
    if not os.path.exists(os.path.join(index_dir, "index.faiss")):
        print("⚠️ Index not found. Rebuilding...")
        build_financial_rag()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)


# Normalize keys (e.g., "Equity Picks" -> "equity_picks")
def normalize_keys(d):
    def normalize_key(k): return k.lower().replace(" ", "_")
    if isinstance(d, dict):
        return {normalize_key(k): normalize_keys(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [normalize_keys(i) for i in d]
    return d


# Query Ollama with context
def query_ollama_for_portfolio(user_data: User, allocation: dict, k: int = 5, return_dict: bool = True):
    """
    Generate structured portfolio recommendation based on user profile, allocation, and market context.
    """

    # Load market context
    vectorstore = load_vector_store()
    results = vectorstore.similarity_search("market outlook and stock opportunities", k=k)
    context_chunks = "\n\n".join([doc.page_content[:2000] for doc in results])

    # Format loans
    loans = "\n".join([f"   - {loan.__class__.__name__}: ${loan.amount} at {loan.interest_rate}% interest" for loan in
                       user_data.loans])

    # Format goals
    goals = "\n".join(
        [f"   - {goal.name} (${goal.target_amount} in {goal.months_to_achieve} months)" for goal in user_data.goals])

    # User summary
    user_summary = f"""
👤 USER PROFILE:
- Name: {user_data.name}
- Age: {user_data.age}, Risk Profile: {user_data.risk_profile}
- Income: ${user_data.income:.2f}, Expenses: ${user_data.expenses:.2f}
- Monthly Surplus: ${user_data.monthly_surplus:.2f}
- Emergency Fund: ${user_data.emergency_fund:.2f}
- Insurance: {', '.join(user_data.insurances)}
- Loans:
{loans}
- Goals:
{goals}
"""

    # Asset allocation
    alloc_text = f"""💼 TARGET ALLOCATION:
- Equity: {allocation['equity']}%
- Bonds: {allocation['bonds']}%
- Commodities: {allocation['commodities']}%
"""

    # Prompt for LLM
    prompt = f"""
You are a financial advisor AI.

Given the following user profile and current market outlook, recommend a personalized investment portfolio.
Stick to the asset allocation ratios and provide recommendations as structured JSON output.

🔍 Include:
- Equity picks: list of tickers with name, rationale, and time horizon ([Short-Term], [Mid-Term], [Long-Term])
- Bond picks: same as above
- Commodity picks: same as above

### USER INFO
{user_summary}

{alloc_text}

### MARKET OUTLOOK
{context_chunks}

📦 RETURN OUTPUT IN JSON FORMAT AS:
{{
  "equity_picks": [
    {{
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "reason": "Strong fundamentals, good cash flow",
      "horizon": "Long-Term"
    }},
    ...
  ],
  "bond_picks": [...],
  "commodity_picks": [...]
}}

Only return the JSON — no extra explanation.
"""

    # Send to Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:latest",
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    # Collect streamed output
    full_output = ""
    for chunk in response.iter_lines():
        if chunk:
            try:
                data = json.loads(chunk.decode("utf-8"))
                full_output += data.get("response", "")
            except json.JSONDecodeError:
                continue

    # Optional JSON parsing
    if return_dict:
        try:
            json_start = full_output.find('{')
            raw_output = json.loads(full_output[json_start:])

            # Remove wrapper like "recommendations" and normalize keys
            if isinstance(raw_output, dict) and "recommendations" in raw_output:
                raw_output = raw_output["recommendations"]

            cleaned = normalize_keys(raw_output)
            return cleaned
        except Exception as e:
            print("⚠️ Error parsing JSON response:", e)
            return {"error": "Failed to parse LLM output", "raw": full_output}
    else:
        return full_output.strip()
