from pydantic import BaseModel
from typing import List

class RAGRecommendation(BaseModel):
    stock_ticker: str
    bond_ticker: str
    gold_ticker: str
    stock_analysis: str
    bond_analysis: str
    gold_analysis: str
    source: str
    confidence_score: float  # Confidence level in recommendation

class FinalRecommendation(BaseModel):
    user_id: str
    recommendations: List[RAGRecommendation]
    overall_strategy: str  # e.g., "Aggressive", "Balanced", "Conservative"
