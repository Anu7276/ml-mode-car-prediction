import requests
import json

url = "http://127.0.0.1:5000/api/predict"
data = {
    "Car_Name": "Nexon",
    "Year": 2021,
    "Fuel_Type": "Petrol",
    "Transmission": "Manual",
    "Kms_Driven": 20000,
    "Owner": 1,
    "Engine": 1199,
    "Power": 85,
    "Efficiency": 18.5,
    "Location": "Mumbai",
    "Seller_Type": "Individual",
    "Present_Price": 10.50,
    "Seats": 5
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
