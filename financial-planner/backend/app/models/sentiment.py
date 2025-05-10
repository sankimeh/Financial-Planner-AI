from pydantic import BaseModel
from typing import List, Optional


class SentimentAnalysis(BaseModel):
    stock_ticker: str
    sentiment_score: float
    sentiment_label: str  # Positive, Neutral, Negative
    analysis_details: str  # Justification of sentiment score (e.g., news details)
    source: str  # News source
    confidence_score: float  # Confidence level of sentiment

class SentimentSummary(BaseModel):
    short_term_tips: List[SentimentAnalysis]
    long_term_tips: Optional[List[SentimentAnalysis]] = None
    overall_sentiment: str  # e.g., "Bullish", "Bearish", "Neutral"
