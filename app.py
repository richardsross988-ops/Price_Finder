from flask import Flask, jsonify, request
import requests
import os

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
        return jsonify({
            "error": "Could not get prices",
            "status": response.status_code,
            "details": response.text
        }), 500

    data = response.json()
    shopping_results = data.get("shopping_results", [])

    results = []
    for item in shopping_results:
        results.append({
            "shop": item.get("source", "Unknown"),
            "price": item.get("price", "N/A"),
            "title": item.get("title", ""),
            results.append({
                "line": f"{shop} | {title} | {price}"
        })

    def get_price(x):
        try:
            return float(str(x["price"]).replace("R","").replace(",","").strip())
        except:
            return 9999

    results.sort(key=get_price)
    return jsonify(results)

if __name__ == "__main__":
    app.run()
