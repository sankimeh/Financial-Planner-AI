import yfinance as yf
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import os
import datetime

from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from headline_sentiment import get_sentiment_documents

# -----------------------------
# 1. PDF & Article Scraper
# -----------------------------

def scrape_pdf(url):
    docs = []
    try:
        response = requests.get(url)
        filename = "temp_report.pdf"
        with open(filename, "wb") as f:
            f.write(response.content)
        with fitz.open(filename) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
        os.remove(filename)
        docs.append(Document(page_content=text, metadata={"source": url}))
    except Exception as e:
        print(f"[PDF Error] {url}: {e}")
    return docs

def scrape_article(url):
    docs = []
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        text = "\n".join([p.text for p in soup.find_all("p")])
        docs.append(Document(page_content=text, metadata={"source": url}))
    except Exception as e:
        print(f"[Article Error] {url}: {e}")
    return docs

# -----------------------------
# 2. Yahoo Finance Scraper
# -----------------------------

def fetch_stock_data(tickers):
    docs = []
    for symbol in tickers:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1y")
            if hist.empty:
                continue
            hist_text = hist.reset_index().to_string(index=False)
            profile = stock.info.get("longBusinessSummary", "")
            content = f"Ticker: {symbol}\n\nProfile:\n{profile}\n\nHistory:\n{hist_text}"
            docs.append(Document(page_content=content, metadata={"ticker": symbol}))
        except Exception as e:
            print(f"[Stock Error] {symbol}: {e}")
    return docs

# -----------------------------
# 3. Market Sentiment Scrapers
# -----------------------------

def scrape_aaii_sentiment():
    url = "https://www.aaii.com/sentimentsurvey"
    docs = []
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        result_block = soup.find("div", class_="sentiment-survey-results")
        if not result_block:
            raise Exception("Sentiment data not found on AAII page")
        text = result_block.get_text("\n", strip=True)
        docs.append(Document(page_content=text, metadata={"source": url, "type": "sentiment", "name": "AAII"}))
    except Exception as e:
        print(f"[AAII Error] {e}")
    return docs

def scrape_sffed_sentiment():
    url = "https://www.frbsf.org/research-and-insights/data-and-indicators/daily-news-sentiment-index/"
    docs = []
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraph = soup.find("div", class_="body-text").get_text("\n", strip=True)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        docs.append(Document(page_content=paragraph, metadata={"source": url, "type": "sentiment", "name": "SF Fed", "date": date_str}))
    except Exception as e:
        print(f"[SF Fed Error] {e}")
    return docs

def scrape_sumgrowth_sentiment():
    url = "https://www.sumgrowth.com/InfoPages/Market-Sentiment.aspx"
    docs = []
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        content_block = soup.find("div", id="content")
        summary = content_block.get_text("\n", strip=True) if content_block else ""
        docs.append(Document(page_content=summary, metadata={"source": url, "type": "sentiment", "name": "SumGrowth"}))
    except Exception as e:
        print(f"[SumGrowth Error] {e}")
    return docs

def collect_sentiment_documents():
    print("📊 Collecting sentiment data...")
    docs = []
    docs.extend(scrape_aaii_sentiment())
    docs.extend(scrape_sffed_sentiment())
    docs.extend(scrape_sumgrowth_sentiment())
    print(f"✅ Sentiment documents collected: {len(docs)}")
    return docs

# -----------------------------
# 4. Build & Save Vector Store
# -----------------------------

def build_vector_store(documents, index_dir="faiss_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    os.makedirs(index_dir, exist_ok=True)
    vectorstore.save_local(index_dir)
    print(f"✅ Vector store saved to {index_dir}/")

# -----------------------------
# 5. Entry Point
# -----------------------------

def build_financial_rag():
    print("🚀 Starting RAG index creation...")

    article_urls = [
        "https://www.reuters.com/markets/global-markets-recession-graphic-2025-05-08/",
        "https://www.investopedia.com/what-will-it-take-for-stocks-to-keep-rising-what-experts-say-11729371",
        "https://www.marketwatch.com/story/wall-streets-outlook-sours-on-second-quarter-with-bigger-forecast-cuts-than-normal-1d89bb5c",
    ]

    pdf_urls = [
        "https://static.seekingalpha.com/uploads/sa_presentations/772/98772/original.pdf"
    ]

    tickers = [
        # Mega cap tech
        "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "CRM",

        # Large US financials
        "JPM", "WFC", "BAC", "GS", "MS", "AXP", "C", "USB", "BK", "BLK",

        # Healthcare
        "JNJ", "PFE", "MRK", "ABBV", "UNH", "CVS", "LLY",

        # ETFs (broad index)
        "SPY", "VTI", "QQQ", "DIA", "IWM", "VOO",

        # ETFs (sector)
        "XLK", "XLF", "XLE", "XLY", "XLI", "XLV", "XLC", "XLU", "XLB", "XLRE",

        # International & emerging
        "EFA", "EEM", "VEA", "VWO", "FXI",

        # Bonds
        "TLT", "IEF", "SHY", "LQD", "HYG", "AGG", "BND",

        # Commodities & metals
        "GLD", "IAU", "SLV", "DBC", "DBA",

        # Crypto-related (optional)
        "COIN", "MSTR", "RIOT"
    ]

    documents = []

    for url in article_urls:
        documents.extend(scrape_article(url))

    for url in pdf_urls:
        documents.extend(scrape_pdf(url))

    documents.extend(fetch_stock_data(tickers))
    documents.extend(collect_sentiment_documents())
    documents.extend(get_sentiment_documents())

    print(f"🧾 Total documents collected: {len(documents)}")

    build_vector_store(documents)

if __name__ == "__main__":
    build_financial_rag()
