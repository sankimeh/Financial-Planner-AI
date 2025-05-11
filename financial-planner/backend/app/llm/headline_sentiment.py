import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from langchain.schema import Document

# Load FinBERT sentiment analyzer
sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def fetch_yahoo_finance_headlines():
    url = "https://finance.yahoo.com/most-active"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    headlines = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        # Find news headlines inside table rows or anchor tags
        for tag in soup.select("a[href*='/quote/']"):
            text = tag.get_text(strip=True)
            if text and 10 < len(text) < 120:
                headlines.append(text)
        return list(set(headlines))[:20]
    except Exception as e:
        print(f"[Yahoo Error] {e}")
        return []

def analyze_headline_sentiments(headlines):
    docs = []
    try:
        results = sentiment_pipeline(headlines)
        for i, result in enumerate(results):
            docs.append(
                Document(
                    page_content=headlines[i],
                    metadata={
                        "source": "Yahoo Finance",
                        "sentiment": result['label'],
                        "score": result['score']
                    }
                )
            )
    except Exception as e:
        print(f"[FinBERT Error] {e}")
    return docs

def get_sentiment_documents():
    print("📰 Fetching Yahoo Finance headlines...")
    headlines = fetch_yahoo_finance_headlines()
    if not headlines:
        print("⚠️ No headlines found.")
        return []
    print(f"📈 Analyzing {len(headlines)} headlines with FinBERT...")
    return analyze_headline_sentiments(headlines)