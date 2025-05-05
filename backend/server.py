from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace with your Google API key and Search Engine ID
GOOGLE_API_KEY = "AIzaSyBkdkBKn6WfSTFVffycB92zdqYRew20jy0"
GOOGLE_SEARCH_ENGINE_ID = "82432ef5bb6204755"
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"


# FIXME: Add error handling for the Google API request
# TODO: Do not expose the API key in the code and use environment variables instead



@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_SEARCH_ENGINE_ID,
        "q": query
    }
    try:
        response = requests.get(GOOGLE_SEARCH_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return jsonify({"error": "Failed to fetch search results"}), 500

    data = response.json()
    results = []

    # Extract relevant results from the Google API response
    if "items" in data:
        for item in data["items"]:
            results.append({
                "title": item["title"],
                "url": item["link"],
                "snippet": item.get("snippet", "")
            })

    return jsonify(results)  # Always return a JSON array

if __name__ == "__main__":
    app.run(debug=True, port=5000)