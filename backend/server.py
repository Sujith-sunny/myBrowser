from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder="../ui", static_url_path="/")
CORS(app)  # Enable CORS for all routes

# Load API key and Search Engine ID from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY_MAIN")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID_MAIN")
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# Check if API key and Search Engine ID are loaded
if not GOOGLE_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
    raise EnvironmentError("GOOGLE_API_KEY or GOOGLE_SEARCH_ENGINE_ID is not set in the .env file.")

@app.route("/")
def homepage():
    """Serve the homepage."""
    return send_from_directory(app.static_folder, "homepage.html")

@app.route("/results.html")
def results_page():
    """Serve the results page."""
    return send_from_directory(app.static_folder, "results.html")

@app.route("/search", methods=["GET"])
def search():
    """Handle search queries."""
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_SEARCH_ENGINE_ID,
        "q": query
    }

    print(f"Received query: {query}")
    print(f"Requesting Google API with params: {params}")

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