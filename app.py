from flask import Flask, request, jsonify
from ultralytics import YOLO
from disease_info import disease_data
import tempfile
import os

app = Flask(__name__)

# Load YOLO model ONCE
model = YOLO("best.pt")

@app.route("/", methods=["GET"])
def home():
    return "Coconut Disease Detection API is running"

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "Image not provided"}), 400

    image_file = request.files["image"]

    # Save temp image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image_path = tmp.name
        image_file.save(image_path)

    # YOLO prediction
    results = model(image_path)

    os.remove(image_path)

    if len(results[0].boxes) == 0:
        return jsonify({"disease": "no disease detected"})

    cls_id = int(results[0].boxes.cls[0])
    label = model.names[cls_id].lower()

    info = disease_data.get(label)

    if not info:
        return jsonify({"disease": label, "info": "No details found"})

    return jsonify({
        "disease": label,
        "info": info
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
