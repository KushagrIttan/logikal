import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_excel(r"training_data/final.xlsx")

# Drop unnecessary columns
df.drop([
    "GpsProvider", "BookingID", "Market/Regular ", "BookingID_Date", "vehicle_no", "Origin_Location", 
    "Destination_Location", "Data_Ping_time", "Planned_ETA", "Current_Location", "DestinationLocation",  
    "actual_eta", "Curr_lat", "Curr_lon", "ontime", "OriginLocation_Code", "DestinationLocation_Code", 
    "trip_start_date", "trip_end_date", "TRANSPORTATION_DISTANCE_IN_KM", "vehicleType", 
    "Minimum_kms_to_be_covered_in_a_day", "Driver_Name", "Driver_MobileNo", "customerID", "customerNameCode", 
    "supplierID", "supplierNameCode","Org_lat_lon","Des_lat_lon"
], axis=1, inplace=True)

# Define target variable and predictors
Y = df["delay"]  
X = df.drop(["delay", "Material Shipped"], axis=1)  

# Standardize data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.30, random_state=42)

# Train logistic regression model
lr = LogisticRegression()
lr.fit(X_train, Y_train)

# Make predictions
Y_pred = lr.predict(X_test)

# Evaluate model
accuracy = accuracy_score(Y_test, Y_pred)
print(f'Accuracy: {accuracy:.2f}')
print(classification_report(Y_test, Y_pred))

# Save model and scaler
joblib.dump(lr, "compliance_checker_model.pkl")
joblib.dump(scaler, "scaler.pkl")

import numpy as np
import pandas as pd
import joblib

# Load trained model and scaler
model = joblib.load("compliance_checker_model.pkl")
scaler = joblib.load("scaler.pkl")

# # Get user input
# ORG_LAT = float(input("Enter the origin latitude: "))
# ORG_LONG = float(input("Enter the origin longitude: "))
# DEST_LAT = float(input("Enter the destination latitude: "))
# DEST_LONG = float(input("Enter the destination longitude: "))
#
# #
# # Convert user input to a DataFrame with the same column names used during training
# user_input_df = pd.DataFrame([[ORG_LAT, ORG_LONG, DEST_LAT, DEST_LONG]], columns=["ORG_LAT", "ORG_LONG", "DEST_LAT", "DEST_LONG"])
# #
# # # Scale user input
# user_input_scaled = scaler.transform(user_input_df)  # Now input matches training data format
#
# # Make prediction
# prediction = model.predict(user_input_scaled)
#
# # Display result
# if prediction[0] == 1:
#     print("COMPLIANCE CHECKING PROCESS: CLEARED!")
# else:
#     print("COMPLIANCE NOT CLEARED.")

import hi2

ORG_LAT, ORG_LONG, DEST_LAT, DEST_LONG = hi2.fetcher()

if None in (ORG_LAT, ORG_LONG, DEST_LAT, DEST_LONG):
    print("Failed to get valid coordinates. Exiting.")
else:
    # Proceed with ML model
    user_input_df = pd.DataFrame([[ORG_LAT, ORG_LONG, DEST_LAT, DEST_LONG]],
                                 columns=["ORG_LAT", "ORG_LONG", "DEST_LAT", "DEST_LONG"])

    user_input_scaled = scaler.transform(user_input_df)
    prediction = model.predict(user_input_scaled)

    print("COMPLIANCE CHECKING PROCESS: CLEARED!" if prediction[0] == 1 else "COMPLIANCE NOT CLEARED.")
