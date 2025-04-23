from flask import Flask, request, jsonify
import t2

app = Flask(__name__)

# Replace this with your actual parcel compliance prediction function
@app.route('/predict_compliance', methods=['POST'])
def predict_compliance_api():
    try:
        parcel_data = request.get_json()  # Get JSON data from the request
        if not parcel_data:
            return jsonify({"error": "No JSON data provided"}), 400

        vdtr=t2.ShipmentValidator(parcel_data)
        prediction,errors=vdtr.validate()

        return jsonify(prediction)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app