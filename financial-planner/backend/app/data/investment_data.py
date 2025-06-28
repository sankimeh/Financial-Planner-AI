# Expanding each investment product with more detailed performance data

extended_investment_db = {
    "HDFC Flexi Cap Fund": {
        "category": "Mutual Fund",
        "sub_category": "Equity",
        "term": "Long",
        "risk_level": "High",
        "benchmark": "NIFTY 500 TRI",
        "fund_house": "HDFC Mutual Fund",
        "isin": "INF179K01HQ2",
        "expense_ratio": 1.07,
        "aum_cr": 38000,  # in Crores
        "inception_date": "1995-01-01",
        "returns": {
            "1yr": 18.3,
            "3yr": 15.2,
            "5yr": 13.4,
            "10yr": 14.1,
            "since_inception": 15.8
        },
        "volatility": "High",
        "sharpe_ratio": 1.1,
        "standard_deviation": 19.8,
        "drawdown": -24.5,
        "top_holdings": ["Infosys", "HDFC Bank", "ICICI Bank"],
        "exit_load": "1% if redeemed within 1 year"
    },
    "Axis Bluechip Fund": {
        "category": "Mutual Fund",
        "sub_category": "Large Cap",
        "term": "Mid",
        "risk_level": "Moderate",
        "benchmark": "NIFTY 100 TRI",
        "fund_house": "Axis Mutual Fund",
        "isin": "INF846K01V59",
        "expense_ratio": 1.18,
        "aum_cr": 32000,
        "inception_date": "2010-01-01",
        "returns": {
            "1yr": 11.4,
            "3yr": 12.6,
            "5yr": 11.1,
            "10yr": 12.9,
            "since_inception": 13.2
        },
        "volatility": "Medium",
        "sharpe_ratio": 0.95,
        "standard_deviation": 14.6,
        "drawdown": -17.3,
        "top_holdings": ["TCS", "HUL", "Reliance Industries"],
        "exit_load": "1% if redeemed within 12 months"
    },
    "GOI Savings Bond 2030": {
        "category": "Bond",
        "sub_category": "Government",
        "term": "Long",
        "risk_level": "Low",
        "benchmark": "10-Year G-Sec",
        "fund_house": "Government of India",
        "isin": "IN0020200071",
        "expense_ratio": 0.0,
        "interest_rate": 7.1,
        "interest_type": "Fixed",
        "maturity_date": "2030-12-31",
        "returns": {
            "1yr": 7.1,
            "3yr": 7.1,
            "5yr": 7.1
        },
        "taxation": "Interest taxable as per income slab",
        "exit_load": "Lock-in till maturity"
    },
    "PSU Bank Bond": {
        "category": "Bond",
        "sub_category": "PSU",
        "term": "Mid",
        "risk_level": "Low-Medium",
        "benchmark": "CRISIL Bond Index",
        "fund_house": "Various PSU Banks",
        "isin": "N/A",
        "expense_ratio": 0.0,
        "interest_rate": 6.5,
        "interest_type": "Fixed",
        "maturity_date": "2027-06-30",
        "returns": {
            "1yr": 6.5,
            "3yr": 6.4
        },
        "taxation": "Interest taxable as per income slab",
        "exit_load": "Tradable in secondary market"
    },
    "Nippon India Gold ETF": {
        "category": "ETF",
        "sub_category": "Gold",
        "term": "Mid",
        "risk_level": "Medium",
        "benchmark": "Domestic Gold Price",
        "fund_house": "Nippon India Mutual Fund",
        "isin": "INF204KB17I5",
        "expense_ratio": 0.83,
        "aum_cr": 5000,
        "inception_date": "2007-03-01",
        "returns": {
            "1yr": 12.7,
            "3yr": 9.6,
            "5yr": 11.2,
            "since_inception": 10.4
        },
        "volatility": "Medium",
        "sharpe_ratio": 0.85,
        "standard_deviation": 12.1,
        "drawdown": -10.5,
        "top_holdings": ["Gold (99.9% purity)"],
        "exit_load": "None"
    },
    "ICICI Prudential Silver ETF": {
        "category": "ETF",
        "sub_category": "Silver",
        "term": "Short-Mid",
        "risk_level": "High",
        "benchmark": "Domestic Silver Price",
        "fund_house": "ICICI Prudential Mutual Fund",
        "isin": "INF109KC1NT4",
        "expense_ratio": 0.9,
        "aum_cr": 1200,
        "inception_date": "2022-01-01",
        "returns": {
            "1yr": 17.4,
            "3yr": None,
            "since_inception": 13.2
        },
        "volatility": "High",
        "sharpe_ratio": 1.05,
        "standard_deviation": 22.3,
        "drawdown": -15.7,
        "top_holdings": ["Physical Silver"],
        "exit_load": "None"
    }
}
