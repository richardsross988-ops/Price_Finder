from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

SERPAPI_KEY = os.environ.get("SERPAPI_KEY")

@app.route("/prices")
def prices():
    product = request.args.get("product", "")

    response = requests.get(
        "https://serpapi.com/search",
        params={
            "engine": "google_shopping",
            "q": product,
            "api_key": SERPAPI_KEY,
            "gl": "za",
            "hl": "en",
            "location": "South Africa",
        }
    )

    if response.status_code != 200:
        return json.dumps({
            "error": "Could not get prices",
            "status": response.status_code,
            "details": response.text
        }, indent=4), 500

    data = response.json()
    shopping_results = data.get("shopping_results", [])

    results = []
    for item in shopping_results:
        results.append({
            "shop": item.get("source", "Unknown"),
            "price": item.get("price", "N/A"),
            "title": item.get("title", ""),
            "url": item.get("link", ""),
        })

    def get_price(x):
        try:
            return float(str(x["price"]).replace("R","").replace(",","").replace(" ","").strip())
        except:
            return 9999

    results.sort(key=get_price)

    # Build a neat readable output

        # Build a neat readable output
    output = "=" * 40 + "\n"
    output += f"  PRICE RESULTS FOR: {product.upper()}\n"
    output += "=" * 40 + "\n\n"
    
    for i, item in enumerate(results, 1):
        output += f"#{i}\n"
        output += f"  Shop:  {item['shop']}\n"
        output += f"  Item:  {item['title']}\n"
        output += f"  Price: {item['price']}\n"
        if item['url']:
            output += f"  Link:  {item['url']}\n"
        output += "-" * 40 + "\n"

    return output, 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run()
