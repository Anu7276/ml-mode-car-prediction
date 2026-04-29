import os

import joblib
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS


BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE_DIR, "projects", "frontend")
MODEL_PATH = os.path.join(BASE_DIR, "projects", "model", "car_price_model.pkl")

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)

try:
    model = joblib.load(MODEL_PATH)
except Exception as exc:
    print(f"Error loading model: {exc}")
    model = None


@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/predict")
def predict_page():
    return send_from_directory(FRONTEND_DIR, "predict.html")


@app.route("/about")
def about_page():
    return send_from_directory(FRONTEND_DIR, "about.html")


@app.route("/contact")
def contact_page():
    return send_from_directory(FRONTEND_DIR, "contact.html")


@app.route("/team")
def team_page():
    return send_from_directory(FRONTEND_DIR, "team.html")


@app.route("/api/predict", methods=["POST"])
def predict_api():
    if model is None:
        return jsonify({"error": "Model not loaded on server"}), 500

    try:
        data = request.get_json() or {}

        current_year = 2026
        data["Car_Age"] = current_year - int(data.get("Year", current_year))

        numerical_fields = [
            "Year",
            "Car_Age",
            "Kms_Driven",
            "Owner",
            "Engine",
            "Power",
            "Efficiency",
            "Present_Price",
            "Seats",
        ]
        for key in numerical_fields:
            data[key] = float(data.get(key, 0))

        prediction = model.predict(pd.DataFrame([data]))

        return jsonify({"predicted_price": round(float(prediction[0]), 2)})
    except Exception as exc:
        print(f"Prediction error: {exc}")
        return jsonify({"error": str(exc)}), 400


@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(FRONTEND_DIR, path)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
