from fastapi import APIRouter
from random import uniform

from app.models.sentiment import SentimentSummary

router = APIRouter()


@router.get("/sentiment/{stock_ticker}")
async def get_sentiment(stock_ticker: str):
    sentiment_data = [
        {"stock_ticker": stock_ticker, "sentiment_score": uniform(-1.0, 1.0), "sentiment_label": "Positive",
         "analysis_details": "News looks good", "source": "NewsAPI", "confidence_score": 0.85},
        {"stock_ticker": stock_ticker, "sentiment_score": uniform(-1.0, 1.0), "sentiment_label": "Neutral",
         "analysis_details": "No strong signals", "source": "NewsAPI", "confidence_score": 0.60}
    ]

    return SentimentSummary(short_term_tips=sentiment_data, overall_sentiment="Neutral")
