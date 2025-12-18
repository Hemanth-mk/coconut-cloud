from flask import Flask, request, jsonify
from disease_info import disease_data
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Coconut Disease API is running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    label = data.get("label")

    if not label:
        return jsonify({"error": "No label provided"}), 400

    info = disease_data.get(label.lower())

    if not info:
        return jsonify({"error": "Disease not found"}), 404

    return jsonify({
        "disease": label,
        "info": info
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
