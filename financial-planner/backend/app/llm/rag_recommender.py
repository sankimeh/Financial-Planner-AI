import yfinance as yf
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import os

from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings

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
# 3. Build & Save Vector Store
# -----------------------------

def build_vector_store(documents, index_dir="faiss_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    os.makedirs(index_dir, exist_ok=True)
    vectorstore.save_local(index_dir)
    print(f"✅ Vector store saved to {index_dir}/")

# -----------------------------
# 4. Entry Point
# -----------------------------

def build_financial_rag():
    print("🚀 Starting RAG index creation...")

    # Sources (expand freely)
    article_urls = [
        "https://www.reuters.com/markets/global-markets-recession-graphic-2025-05-08/",
        "https://www.investopedia.com/what-will-it-take-for-stocks-to-keep-rising-what-experts-say-11729371",
        "https://www.marketwatch.com/story/wall-streets-outlook-sours-on-second-quarter-with-bigger-forecast-cuts-than-normal-1d89bb5c",
    ]

    pdf_urls = [
        "https://static.seekingalpha.com/uploads/sa_presentations/772/98772/original.pdf"
    ]

    tickers = [
        # Stocks
        "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "JNJ", "PFE", "JPM", "WFC",
        # ETFs
        "SPY", "VTI", "QQQ", "XLK", "XLF", "EFA", "EEM",
        # Bonds
        "TLT", "IEF", "LQD", "HYG",
        # Gold/Silver
        "GLD", "IAU", "SLV"
    ]

    documents = []

    for url in article_urls:
        documents.extend(scrape_article(url))

    for url in pdf_urls:
        documents.extend(scrape_pdf(url))

    documents.extend(fetch_stock_data(tickers))

    print(f"🧾 Total documents collected: {len(documents)}")

    build_vector_store(documents)

if __name__ == "__main__":
    build_financial_rag()
