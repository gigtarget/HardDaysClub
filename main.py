from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/premarket")
def get_premarket_data():
    return {
        "nifty": "NIFTY 50: 24,346.70 ↑ +12.50 pts",
        "sensex": "SENSEX: 74,050 ↑ +250 pts",
        "global": "Dow +0.8%, Nasdaq +1.2%, SGX Nifty +0.6%",
        "fii": "FII: +₹1,200 Cr | DII: -₹600 Cr",
        "outlook": "Market likely to open higher amid strong global cues."
    }

    try:
        session.get("https://www.nseindia.com")  # warm-up
        response = session.get("https://www.nseindia.com/api/marketStatus")
        market_data = response.json()

        # Dummy static data (you can parse response if needed)
        return {{
            "nifty": "NIFTY 50: 24,346.70 ↑ +12.50 pts",
            "sensex": "SENSEX: 74,050 ↑ +250 pts",
            "global": "Dow +0.8%, Nasdaq +1.2%, SGX Nifty +0.6%",
            "fii": "FII: +₹1,200 Cr | DII: -₹600 Cr",
            "outlook": "Market likely to open higher amid strong global cues."
        }}
    except Exception as e:
        return {{"error": str(e)}}        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
