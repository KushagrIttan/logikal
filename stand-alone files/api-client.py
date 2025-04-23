import requests
import json


url = 'http://127.0.0.1:5000/predict_compliance'  # Your API endpoint
parcel_data = {
    "country_of_origin": "pakistan",
    "importer_address": "New York",
    "country_of_destination": "iran",
    "product_type": "dog ",
    "hs_code": "091030",
    "wt": 300,
    "declared_value": 200
}

headers = {'Content-type': 'application/json'}
response = requests.post(url, data=json.dumps(parcel_data), headers=headers)

if response.status_code == 200:
    prediction = response.json()
    if prediction:
        print("Shipment is valid.")
    else:
        print("Shipment is invalid.")
    # print(prediction)
else:
    print(f"Error: {response.status_code}, {response.text}")