from new.pages import llm, block_chain
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
            "country_of_destination",
            "product_type",
            "hs_code",
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
        res_c=["north korea","iran","syria","cuba","sudan"]
        if self.shipment_data.get("country_of_destination").lower() in res_c:
            self.errors.append(f"Cannot ship to restricted country:{self.shipment_data.get('country_of_destination')}.")

    def validate_product_type(self):
        res=["weapons","drugs","alcohol","dangerous chemicals","animals"]
        chat=(llm.chat_bot_category(self.shipment_data.get("product_type")))
        chat = chat.rstrip("\n")
        for i in res:
            if i==chat.lower():
                self.errors.append(f"Cannot ship restricted product:{chat}.")
                break

    def validate_product_specific_rules(self):
        # product_name = self.shipment_data.get("product_name").lower()
        product_type = self.shipment_data.get("product_type").lower()
        hs_code = self.shipment_data.get("hs_code")

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


# flag=0 # 0->manual input, 1->csv
# if ('sample.pdf'):
#     flag=1
# #in case of csv file:
#
# if flag==1:
#     try :
#         with open('sample-data.csv', mode='r') as csv_file:
#             csv_reader = csv.DictReader(csv_file)
#             shipment_data_list = [row for row in csv_reader]
#     except FileNotFoundError:
#         print("File not found.")




# Example Usage
shipment_data = {
    "country_of_origin": "India",
    "importer_address": "New York",
    "country_of_destination": "USA",
    "product_type": "smartphone",
    "hs_code": "091030",
    "wt": 300,
    "declared_value": 200}

shipment_data2={'country_of_origin': 'India', 
               'country_of_destination': 'Afghanistan', 
               'importer_address': 'qdewf', 
               'hs_code': '03412', 
               'product_type': 'Smartphone', 
               'declared_value': 90.0, 
               'wt': 800.0}




with open('new/pages/jsons/shipment_data.json', 'w') as json_file:
    json.dump(shipment_data, json_file, indent=4)
block_chain.shipping_data()

validator = ShipmentValidator(shipment_data2)
is_valid, errors = validator.validate()

if is_valid:
    print("Shipment is valid.")
else:
    print("Shipment is invalid. Errors:")
    for error in errors:
        print(f"- {error}")
