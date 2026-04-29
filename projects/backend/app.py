import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import joblib

# Initialize Flask with custom static folder path
app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'car_price_model.pkl')

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- Page Routes ---

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict')
def predict_page():
    return send_from_directory(app.static_folder, 'predict.html')

@app.route('/about')
def about_page():
    return send_from_directory(app.static_folder, 'about.html')

@app.route('/contact')
def contact_page():
    return send_from_directory(app.static_folder, 'contact.html')

@app.route('/team')
def team_page():
    return send_from_directory(app.static_folder, 'team.html')

# --- API Routes ---

@app.route('/api/predict', methods=['POST'])
def predict_api():
    if model is None:
        return jsonify({"error": "Model not loaded on server"}), 500

    try:
        data = request.get_json()
        
        # Calculate Car_Age as it's a required feature for the model
        current_year = 2026
        if 'Year' in data:
            data['Car_Age'] = current_year - int(data['Year'])
        else:
            data['Car_Age'] = 0

        # Ensure numerical conversion for model inputs
        numerical_fields = ['Year', 'Car_Age', 'Kms_Driven', 'Owner', 'Engine', 'Power', 'Efficiency', 'Present_Price', 'Seats']
        for key in numerical_fields:
            if key in data:
                data[key] = float(data[key])
            else:
                # Default value if missing to avoid model crash
                data[key] = 0.0
        
        df = pd.DataFrame([data])
        
        # Ensure column order or presence doesn't cause issues if model expects specific columns
        prediction = model.predict(df)
        
        return jsonify({
            "predicted_price": round(float(prediction[0]), 2)
        })

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 400

# Proxy for other static files
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
