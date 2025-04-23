import streamlit as st
import pandas as pd
import os
import llm

import block_chain
import json

class ShipmentValidator:
    def __init__(self, shipment_data):
        self.shipment_data = shipment_data
        self.errors = []

    def validate(self):
        self.validate_required_fields()
        self.validate_country_of_origin()
        self.validate_product_type()
        self.validate_country_of_destination()
        self.validate_product_specific_rules()
        self.validate_quantity()
        # Add other validation methods here
        return len(self.errors) == 0, self.errors  # Returns True if valid, False if invalid, and the list of errors

    def validate_required_fields(self):
        required_fields = [
            "country_of_origin",
            "importer_address",
            "destination",
            "product_type",
            "product_code",
            "wt",
            "declared_value"
        ]
        for field in required_fields:
            if not self.shipment_data.get(field):
                self.errors.append(f"Required field missing: {field}")

    def validate_country_of_origin(self):
        if self.shipment_data.get("country_of_origin") != "India":
            self.errors.append("Country of origin must be India.")

    def validate_country_of_destination(self):
        res_c=["North Korea","Iran","Syria","Cuba","Sudan"]
        if self.shipment_data.get("destination") in res_c:
            self.errors.append(f"Cannot ship to restricted country:{self.shipment_data.get('destination')}.")

    def validate_product_type(self):
        res=["weapons","drugs","alcohol","dangerous chemicals","animals"]
        chat=(llm.chat_bot_category(self.shipment_data.get("product_type")).lower())
        chat = chat.rstrip("\n")
        for i in res:
            if i==chat.lower():
                self.errors.append(f"Cannot ship restricted product:{chat}.")
                break

    def validate_product_specific_rules(self):
        # product_name = self.shipment_data.get("product_name").lower()
        product_type = self.shipment_data.get("product_type")
        hs_code = self.shipment_data.get("product_code")

        # Spices-Specific Rules
        if "spice" in product_type:
            # Check the HS code for validity.
            if not hs_code.startswith("09"):
                self.errors.append("Invalid HS Code, spices usually start with 09")

        # Electronics-Specific Rules
        if "electronics" in product_type:
            if not hs_code.startswith("85"):
                self.errors.append("Invalid HS Code, electronics usually start with 85")
            if self.shipment_data.get("declared_value", 0) <= 100:
                self.errors.append("Declared value for electronics must exceed 100 USD")

    def validate_quantity(self):
        quantity = self.shipment_data.get("wt")
        if not isinstance(quantity, (int, float)):
            self.errors.append("weight must be a number.")
        elif quantity <= 0:
            self.errors.append("weight must be greater than zero.")

# Example Usage
# shipment_data = {
#     "country_of_origin": "iran",
#     "importer_address": "New York",
#     "country_of_destination": "USA",
#     "product_type": "laptop ",
#     "hs_code": "091030",
#     "wt": 300,
#     "declared_value": 200
# }


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


st.title("📦 Shipment Compliance & Upload")

option = st.radio("Choose Input Method:", ("Manual Entry", "Upload File"))
country_of_origin=""
destination=""
importer_address=""
product_code=""
product_type=""
declared_value=0
wt=0

data_dict={"country_of_origin": str(""), "destination": str(""), "importer_address": str(""), "product_code": str(""), "product_type": str(""), "declared_value": 0, "wt": 0}

if option == "Manual Entry":
    with st.form("shipment_form"):
        data_dict["country_of_origin"]= str(st.selectbox("Country of origin",["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador",
    "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (fmr. Swaziland)", "Ethiopia", "Fiji", "Finland", "France",
    "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
    "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
    "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan",
    "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar",
    "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia",
    "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal",
    "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan",
    "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar",
    "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia",
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa",
    "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan",
    "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
    "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]))
        data_dict["destination"] = ( st.selectbox("Destination Country",
                                   ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
                                    "Argentina", "Armenia", "Australia", "Austria",
                                    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
                                    "Belize", "Benin", "Bhutan",
                                    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
                                    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
                                    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China",
                                    "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica",
                                    "Croatia", "Cuba", "Cyprus", "Czechia", "Democratic Republic of the Congo",
                                    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador",
                                    "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia",
                                    "Eswatini (fmr. Swaziland)", "Ethiopia", "Fiji", "Finland", "France",
                                    "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
                                    "Guinea", "Guinea-Bissau",
                                    "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran",
                                    "Iraq", "Ireland",
                                    "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
                                    "Kuwait", "Kyrgyzstan",
                                    "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
                                    "Lithuania", "Luxembourg", "Madagascar",
                                    "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania",
                                    "Mauritius", "Mexico", "Micronesia",
                                    "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
                                    "Myanmar (Burma)", "Namibia", "Nauru", "Nepal",
                                    "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea",
                                    "North Macedonia", "Norway", "Oman", "Pakistan",
                                    "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru",
                                    "Philippines", "Poland", "Portugal", "Qatar",
                                    "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia",
                                    "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
                                    "Saudi Arabia",
                                    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
                                    "Slovenia", "Solomon Islands", "Somalia", "South Africa",
                                    "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden",
                                    "Switzerland", "Syria", "Taiwan",
                                    "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga",
                                    "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
                                    "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
                                    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
                                    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]))
        #print(type(data_dict[destination]))
        data_dict["importer_address"] = str(st.text_input("Importer address"))
        data_dict["product_code"] = str(st.text_input("Product HS Code"))
        data_dict["product_type"] = str(st.text_input("Product Type"))
        data_dict["declared_value"] = st.number_input("Declared Value ($)", min_value=0.0)
        data_dict["wt"] = st.number_input("Weight (kg)", min_value=0.1)

        submitted = st.form_submit_button("Check Compliance")

    if submitted:
        # with open('jsons/shipment_data.json', 'w') as json_file:
        #     json.dump(shipment_data, json_file, indent=4)
        # block_chain.shipping_data()

        
        #data_dict.popitem()

        validator = ShipmentValidator(data_dict)
        is_valid,errors = validator.validate()
        print(data_dict)

        if is_valid: 
            st.session_state["shipment"] = data_dict  # Store data_dict in session state
            st.switch_page("pages/val_true.py")
            st.experimental_rerun()
        else:
            st.switch_page("pages/val_false.py")
            st.experimental_rerun()
            for error in validator.errors:
                print(f"- {error}")
    # if submitted:
    #     compliance_passed = declared_value < 2000  # Fake compliance rule
    #     st.session_state["shipment"] = {
    #         "Parcel ID": country_of_origin,
    #         "Declared Value": f"${declared_value}",
    #         "Weight": f"{wt} kg",
    #         "Destination": destination,
    #         "Compliance Status": "✅ Compliant" if compliance_passed else "❌ Flagged",
    #         "Remarks": "All checks passed." if compliance_passed else "Declared value exceeds limit. Attach Form XYZ."
    #     }
    #     st.success("Redirecting to Validation...")
    #     st.switch_page("pages/val_false.py")
    #     st.experimental_rerun()

if option == "Upload File":
    uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        # Define the save path (same folder)
        save_path = os.path.join(os.getcwd(), uploaded_file.name)

        # Save the uploaded file
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File saved: {uploaded_file.name}")

        # Load the file for processing
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(save_path)
            st.switch_page("pages/val_true.py")
            st.experimental_rerun()
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(save_path)
            st.switch_page("pages/val_true.py")
            st.experimental_rerun()
        else:
            st.switch_page("pages/val_false.py")
            st.experimental_rerun()
