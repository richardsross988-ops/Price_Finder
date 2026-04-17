from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

APIFY_KEY = os.environ.get("APIFY_KEY")

@app.route("/prices")
def prices():
    # Get the product name from the request
    product = request.args.get("product", "")

    # Ask Apify Google Shopping for prices
    response = requests.post(
        "https://api.apify.com/v2/acts/epctex~google-shopping-scraper/run-sync-get-dataset-items",
        params={"token": APIFY_KEY},
        json={
            "queries": [product],
            "maxResults": 10,
            "countryCode": "ZA",
            "languageCode": "en",
        }
    )

    # If something went wrong
    if response.status_code != 200:
        return jsonify({
            "error": "Could not get prices",
            "status": response.status_code,
            "details": response.text
        }), 500

    # Go through each result and pull out what we need
    results = []
    for item in response.json():
        results.append({
            "shop": item.get("seller", "Unknown"),
            "price": item.get("price", "N/A"),
            "original_price": item.get("originalPrice", "N/A"),
            "discount": item.get("discount", "N/A"),
            "title": item.get("title", ""),
            "url": item.get("url", ""),
        })

    # Sort results cheapest first
    def get_price(x):
        try:
            return float(str(x["price"]).replace("R","").replace(",","").strip())
        except:
            return 9999
    results.sort(key=get_price)

    return jsonify(results)

if __name__ == "__main__":
    app.run()
