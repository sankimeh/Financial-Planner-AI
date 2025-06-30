# This sets up a lightweight MCP-style chatbot using Ollama locally
# It bypasses LangChain function-calling agents and uses prompt composition.
import json
import os
import requests
from rapidfuzz import process, fuzz

from app.core.utils.user_util import get_user_profile_summary
from app.data.investment_data import extended_investment_db
from app.models.user import User
from app.llm.fund_commentry_rag import build_fund_rag_index
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# -------------------------------------------------
# Fuzzy Fund Resolver
# -------------------------------------------------

def resolve_fund_name(user_input: str, fund_names: list[str], threshold: int = 80) -> str | None:
    user_input = user_input.lower().strip()
    fund_names_normalized = [name.lower() for name in fund_names]

    alias_map = {
    "axis bluechip": "Axis Bluechip Fund",
    "hdfc flexi cap": "HDFC Flexi Cap Fund",
    "hdfc flexicap": "HDFC Flexi Cap Fund",
    "hdfc flexi cap fund": "HDFC Flexi Cap Fund",
    "goi savings bond": "GOI Savings Bond 2030",
    "goi bond": "GOI Savings Bond 2030",
    "government savings bond": "GOI Savings Bond 2030",
    "psu bank bond": "PSU Bank Bond",
    "nippon gold etf": "Nippon India Gold ETF",
    "nippon india gold": "Nippon India Gold ETF",
    "icici silver etf": "ICICI Prudential Silver ETF",
    "icici prudential silver": "ICICI Prudential Silver ETF",
    "silver etf": "ICICI Prudential Silver ETF"
    }

    if user_input in alias_map:
        return alias_map[user_input]

    match, score, _ = process.extractOne(user_input, fund_names_normalized, scorer=fuzz.partial_ratio)
    print(f"[DEBUG] Match: {match}, Score: {score}")
    return match if score >= threshold else None

def get_actual_fund_key(resolved_name: str, fund_db: dict) -> str | None:
    for key in fund_db.keys():
        if key.lower() == resolved_name.lower():
            return key
    return None


# -------------------------------------------------
# Structured Fund Info
# -------------------------------------------------

def get_fund_metadata(fund_query: str) -> dict:
    fund_name = resolve_fund_name(fund_query, extended_investment_db.keys())
    if not fund_name:
        return {"error": f"Could not identify fund for input: '{fund_query}'"}
    return extended_investment_db[fund_name]

# -------------------------------------------------
# Load RAG Vector Store
# -------------------------------------------------

def load_fund_rag_vector_store(index_dir="faiss_index"):
    if not os.path.exists(os.path.join(index_dir, "index.faiss")):
        print("\u26a0\ufe0f Index not found. Building RAG index...")
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
# Local Ollama Chat
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
# Main MCP Chatbot Entry Point
# -------------------------------------------------

def run_chatbot(message: str, user_profile: dict, fund_query: str = "") -> str:
    try:
        user = User(**user_profile)
    except Exception as e:
        return f"[User Profile Error] {e}"

    print(f"[DEBUG] fund_query: {fund_query}")

    fund_name = resolve_fund_name(fund_query, list(extended_investment_db.keys())) if fund_query else None
    print(f"[DEBUG] resolved fund_name: {fund_name}")

    actual_fund_key = get_actual_fund_key(fund_name, extended_investment_db)
    fund_meta = extended_investment_db.get(actual_fund_key) if actual_fund_key else None

    try:
        rag_chunks = search_fund_rag(message, fund_query=fund_name) if fund_name else []
    except Exception as e:
        rag_chunks = [f"[RAG Error] {e}"]

    # Generate personalized advice based on fund_meta and user_profile
    personalized_advice = ""
    if fund_meta:
        personalized_advice = generate_investment_advice(fund_meta, user_profile)
        print(f"[DEBUG] Personalized Advice:\n{personalized_advice}")

    prompt = build_investment_prompt(
        user_profile=user_profile,
        fund_metadata=fund_meta,
        rag_chunks=rag_chunks,
        question=message.strip(),
        personalized_advice=personalized_advice
    )

    return query_ollama(prompt)


# -------------------------------------------------
# Prompt Composer
# -------------------------------------------------

def build_investment_prompt(
    user_profile: dict,
    fund_metadata: dict | None,
    rag_chunks: list[str],
    question: str,
    personalized_advice: str = ""
) -> str:
    try:
        user = User(**user_profile)
        summary = get_user_profile_summary(user)
    except Exception as e:
        summary = {"error": f"Invalid user profile: {e}"}

    lines = ["You are a helpful financial advisor AI. Answer based on the following context."]

    # User Profile
    lines.append("\n=== USER PROFILE ===")
    if "error" in summary:
        lines.append(summary["error"])
    else:
        lines.append(f"Name: {summary['name']}")
        lines.append(f"Risk Profile: {summary['risk_profile']}")
        lines.append(f"Monthly Surplus: ₹{summary['monthly_surplus']:.2f}")
        lines.append("Emergency Fund: ✅" if summary["has_emergency_fund"] else "Emergency Fund: ❌")
        if summary["goal_breakdown"]:
            lines.append("Goals:")
            for term, goals in summary["goal_breakdown"].items():
                lines.append(f"- {term.title()}: {', '.join(goals)}" if goals else f"- {term.title()}: None")
        if summary["loan_obligations"]:
            lines.append(f"Active Loans: {', '.join(summary['loan_obligations'])}")

    # Fund Metadata
    if fund_metadata:
        lines.append("\n=== FUND METADATA ===")
        for k, v in fund_metadata.items():
            lines.append(f"{k}: {v}")

    # Personalized Advice
    if personalized_advice:
        lines.append("\n=== PERSONALIZED ADVICE ===")
        lines.append(personalized_advice.strip())

    # RAG Context
    if rag_chunks:
        lines.append("\n=== RAG CONTEXT ===")
        for idx, chunk in enumerate(rag_chunks, 1):
            lines.append(f"[{idx}] {chunk.strip()}")

    # User Question
    lines.append("\n=== USER QUESTION ===")
    lines.append(question)

    return "\n".join(lines)


def assess_emergency_fund(emergency_fund: float, surplus: float) -> str:
    if emergency_fund >= surplus * 3:
        return "Your emergency fund appears adequate, covering over 3 months of expenses."
    else:
        return (
            "Currently, your emergency fund might not be sufficient. It's recommended to build an emergency fund "
            "covering at least 3-6 months of expenses before making new investments."
        )

def get_risk_compatibility(user_risk: str, fund_risk: str, fund_type: str) -> str:
    match = (fund_risk.lower(), user_risk.lower())
    if match == ("low", "conservative"):
        return f"This low-risk {fund_type} aligns well with your conservative profile."
    elif match == ("medium", "moderate"):
        return f"This medium-risk {fund_type} fits your moderate risk appetite."
    elif match == ("high", "aggressive"):
        return f"This high-risk {fund_type} could suit your aggressive growth strategy."
    else:
        return f"Given your {user_risk} risk profile, this {fund_risk} risk {fund_type} may need to be balanced with other investments."

def summarize_performance(fund_meta: dict) -> str:
    sharpe = fund_meta.get("sharpe_ratio")
    drawdown = fund_meta.get("drawdown")
    if sharpe is not None and drawdown is not None:
        return f"The fund has a Sharpe Ratio of {sharpe:.2f} and a drawdown of {drawdown}%, suggesting a balanced risk-return profile."
    elif sharpe is not None:
        return f"The Sharpe Ratio of {sharpe:.2f} reflects how well it compensates for risk."
    elif drawdown is not None:
        return f"The fund has experienced a drawdown of {drawdown}% in past downturns."
    return "Performance metrics are not fully available for this fund."

def analyze_goals(goals: list[dict], fund_term: str) -> str:
    if not goals:
        return "No specific goals provided."

    goal_summary = []
    for g in goals:
        months = g.get("months_to_achieve", 0)
        goal_name = g.get("name", "goal")
        if months <= 36:
            goal_summary.append(f"Your short-term goal '{goal_name}' may not align well with a {fund_term}-term product.")
        elif 36 < months <= 84:
            goal_summary.append(f"Your mid-term goal '{goal_name}' could benefit from moderately risky investments.")
        else:
            goal_summary.append(f"Your long-term goal '{goal_name}' may be supported by a {fund_term}-term product.")

    return "\n".join(goal_summary)

def generate_investment_advice(fund_meta: dict, user_profile: dict) -> str:
    # Extract fund info
    fund_risk = fund_meta.get("risk_level", "moderate")
    fund_term = fund_meta.get("term", "long")
    fund_type = fund_meta.get("category", "investment")

    # Extract user info
    emergency_fund = user_profile.get("emergency_fund", 0)
    income = user_profile.get("income", 0)
    expenses = user_profile.get("expenses", 0)
    surplus = income - expenses
    user_risk = user_profile.get("risk_profile", "moderate")
    goals = user_profile.get("goals", [])

    # Generate advice parts
    parts = [
        assess_emergency_fund(emergency_fund, surplus),
        get_risk_compatibility(user_risk, fund_risk, fund_type),
        summarize_performance(fund_meta),
        analyze_goals(goals, fund_term),
        "Remember, all investments carry risk, and past performance is no guarantee of future results. Diversify your portfolio and consult with a certified financial advisor for personalized guidance."
    ]

    return "\n\n".join(parts)

