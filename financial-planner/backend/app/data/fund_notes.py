# Generating RAG-style documents for all 6 funds based on previously collected structured and unstructured data
rag_documents_full = {
    "HDFC Flexi Cap Fund": [
        "HDFC Flexi Cap Fund is designed for long-term investors with a high risk appetite. Its flexible strategy allows investing across large-cap, mid-cap, and small-cap companies, depending on market opportunities. This fund is ideal for wealth creation over a 7-10+ year horizon and suits goals like retirement or child education.",
        "Historically, the fund has delivered consistent long-term performance with a 3-year return of 15.2% and 10-year return of 14.1%, beating its benchmark NIFTY 500 TRI in most years. The fund’s performance benefits from a diversified portfolio and active allocation shifts.",
        "The fund carries a high level of volatility with a standard deviation of 19.8% and Sharpe ratio of 1.1. It has experienced a drawdown of -24.5% in previous market corrections, highlighting its risk-return profile. Investors must be comfortable with temporary losses.",
        "Top holdings include Infosys, HDFC Bank, and ICICI Bank. The fund actively rotates among sectors based on earnings outlook and macroeconomic indicators. It uses a bottom-up stock selection strategy with moderate portfolio turnover.",
        "There is an exit load of 1% if redeemed within 1 year. Gains above ₹1 lakh are taxed at 10% under equity LTCG. It is not an ELSS fund and hence does not provide Section 80C tax benefits.",
    ],

    "Axis Bluechip Fund": [
        "Axis Bluechip Fund is a large-cap mutual fund focusing on top 100 companies by market capitalization. It is suitable for mid-term investors (3-5 years) seeking relatively stable returns from blue-chip stocks. The fund is appropriate for moderately risk-tolerant investors.",
        "The fund has delivered a 3-year return of 12.6% and a 10-year return of 12.9%, with lower volatility compared to flexi-cap or mid-cap funds. It aims to outperform the NIFTY 100 TRI index by focusing on quality stocks with strong fundamentals.",
        "Its risk profile is medium, with a standard deviation of 14.6% and Sharpe ratio of 0.95. It has a lower drawdown than multi-cap funds, making it a good core equity holding.",
        "Top holdings include TCS, Hindustan Unilever, and Reliance Industries. The fund manager uses a growth-at-reasonable-price (GARP) strategy to balance quality and valuation.",
        "Axis Bluechip Fund has an exit load of 1% if redeemed within 12 months. Long-term gains above ₹1 lakh are taxed at 10%. It is not a tax-saving fund.",
    ],

    "GOI Savings Bond 2030": [
        "The Government of India Savings Bond 2030 offers a fixed interest rate of 7.1% and is best suited for conservative long-term investors seeking capital preservation and steady income. It is backed by sovereign guarantee, making it virtually risk-free.",
        "This bond does not trade on the secondary market and has a maturity date of December 31, 2030. It is ideal for long-term capital preservation goals such as retirement or fixed income planning.",
        "Returns are fixed at 7.1% per annum, compounded half-yearly. Since there is no market-linked risk, returns are stable irrespective of market conditions.",
        "There is no expense ratio or management cost. The interest income is taxable as per the investor’s income slab under ‘Income from Other Sources’.",
        "Premature withdrawal is generally not allowed, except in special cases such as for senior citizens or under RBI guidelines. No exit load applies.",
    ],

    "PSU Bank Bond": [
        "PSU Bank Bonds are debt instruments issued by government-owned banks. They typically offer better returns than G-Secs but with slightly higher credit risk. This bond provides a fixed 6.5% interest and suits mid-term income-focused investors.",
        "This bond matures in June 2027 and is tradable on the secondary market, offering some liquidity. It is suitable for conservative investors looking for a balance between safety and yield.",
        "Returns are fixed and not market linked. The interest is paid semi-annually or annually depending on the issue. The bond is not subject to market volatility unless traded on exchanges.",
        "Interest income is taxable as per investor’s slab rate. There is no exit load but capital gains may arise if sold before maturity in the secondary market.",
        "These bonds are backed by PSU banks, which have government support. However, they are not risk-free like sovereign bonds and should be evaluated based on the issuer’s credit rating.",
    ],

    "Nippon India Gold ETF": [
        "Nippon India Gold ETF is an open-ended exchange traded fund that invests in physical gold of 99.9% purity. It provides investors with a convenient way to gain exposure to gold prices without dealing with physical storage.",
        "This fund is suitable for mid-term investors looking to hedge against inflation, currency depreciation, or market uncertainty. Historically, gold has outperformed during geopolitical crises or economic slowdowns.",
        "The ETF has delivered a 3-year return of 9.6% and a 5-year return of 11.2%. Its performance tracks domestic gold prices. It is more stable than equities but can underperform during bull markets.",
        "Volatility is medium, with a Sharpe ratio of 0.85 and standard deviation of 12.1%. The ETF has a relatively low drawdown of -10.5%, making it a good diversifier in an equity-heavy portfolio.",
        "There is no exit load on redemption. Units are taxed like non-equity mutual funds — gains held for over 3 years are taxed at 20% with indexation; short-term gains are taxed as per slab.",
    ],

    "ICICI Prudential Silver ETF": [
        "ICICI Prudential Silver ETF invests in physical silver and tracks domestic silver prices. Silver is a volatile commodity and is suitable for short- to mid-term tactical allocations.",
        "This fund is appropriate for aggressive investors who want exposure to precious metals beyond gold. Silver can deliver high returns in commodity bull cycles but carries high volatility.",
        "The fund has delivered a 1-year return of 17.4% since its inception in 2022. It is a relatively new offering with limited performance history, but offers a way to diversify commodity exposure.",
        "Volatility is high, with standard deviation of 22.3% and drawdown of -15.7%. It is not suitable for conservative investors or long-term capital protection goals.",
        "There is no exit load. Taxation follows the same rules as other non-equity ETFs. Long-term gains (after 3 years) are taxed at 20% with indexation.",
    ]
}