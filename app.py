from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_price(url, css_selector):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")
        el = soup.select_one(css_selector)
        return el.get_text(strip=True) if el else "N/A"
    except:
        return "Error"

@app.route("/prices")
def prices():
    product = request.args.get("product", "")
    
    # ADD YOUR SHOPS HERE — find the CSS selector by right-clicking
    # a price on the shop's website → Inspect → copy the selector
    shops = [
        {
            "name": "Checkers",
            "url": f"https://www.checkers.co.za/search?q={product}",
            "selector": ".price"   # <-- update this per shop
        },
        {
            "name": "Pick n Pay",
            "url": f"https://www.pnp.co.za/pnpstorefront/pnp/en/search?q={product}",
            "selector": ".priceVal"
        },
    ]
    
    results = []
    for shop in shops:
        price = scrape_price(shop["url"], shop["selector"])
        results.append({"shop": shop["name"], "price": price, "url": shop["url"]})
    
    return jsonify(results)

if __name__ == "__main__":
    app.run()