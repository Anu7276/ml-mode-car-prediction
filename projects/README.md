# Vehicle Price Prediction System (Tata Motors)

A complete end-to-end machine learning solution to predict the resale price of Tata vehicles. This project includes a data processing pipeline, a trained Random Forest model, a Flask REST API, and a modern web frontend.

## 🚀 Features
- **Accurate Predictions**: Powered by a tuned Random Forest Regressor ($R^2 \approx 0.99$).
- **Modern UI**: Responsive, card-based design with glassmorphism effects.
- **Smart Logic**: Automatically calculates car age from the registration year.
- **Real-time API**: Flask-based backend for instant price estimation.
- **Confidence Range**: Displays a ±5% estimated market price range.

## 🛠️ Tech Stack
- **Machine Learning**: Python, Scikit-Learn, Pandas, Joblib.
- **Backend**: Flask, Flask-CORS.
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+).

## 📁 Project Structure
```text
project/
├── model/
│   └── car_price_model.pkl       # Optimized Random Forest model
├── backend/
│   └── app.py                    # Flask API server
├── frontend/
│   ├── index.html                # Web interface structure
│   ├── style.css                 # Premium styling
│   └── script.js                 # Frontend logic & API calls
├── dataset/
│   └── tata_vehicle_price_dataset_v2.csv # Raw vehicle data
├── vehicle_price_prediction.py    # ML pipeline script
└── README.md                     # Project documentation
```

## ⚙️ How to Run

### 1. Prerequisites
Ensure you have Python installed. Install the required libraries:
```bash
pip install pandas scikit-learn joblib flask flask-cors
```

### 2. Train the Model (Optional)
The model is already provided in the `model/` folder. If you wish to retrain it:
```bash
python vehicle_price_prediction.py
```

### 3. Start the Backend API
Navigate to the `backend/` folder and run the Flask app:
```bash
python backend/app.py
```
The server will start at `http://127.0.0.1:5000`.

### 4. Launch the Frontend
Open `frontend/index.html` in any modern web browser.

## 📊 Example Input/Output
- **Input**: Nexon, 2021, Petrol, Manual, 15000 Kms, 1199cc, 118bhp, 17.5kmpl, 5 Seater, ₹8.5L Present Price.
- **Output**: Estimated Resale Price: ₹6.45 Lakhs (Range: ₹6.1L – ₹6.8L).

## 📝 License
This project is for educational purposes.
