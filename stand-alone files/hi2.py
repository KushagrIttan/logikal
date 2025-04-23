state_coordinates = {
    "andhra pradesh": (15.9129, 79.7400), "amaravati": (16.5735, 80.3587),
    "arunachal pradesh": (28.2180, 94.7278), "itanagar": (27.0844, 93.6053),
    "assam": (26.2006, 92.9376), "dispur": (26.1408, 91.7906),
    "bihar": (25.0961, 85.3131), "patna": (25.5941, 85.1376),
    "chhattisgarh": (21.2787, 81.8661), "raipur": (21.2514, 81.6296),
    "goa": (15.2993, 74.1240), "panaji": (15.4909, 73.8278),
    "gujarat": (22.2587, 71.1924), "gandhinagar": (23.2156, 72.6369),
    "haryana": (29.0588, 76.0856), "chandigarh": (30.7333, 76.7794),
    "himachal pradesh": (31.1048, 77.1734), "shimla": (31.1048, 77.1734),
    "jharkhand": (23.6102, 85.2799), "ranchi": (23.3441, 85.3096),
    "karnataka": (15.3173, 75.7139), "bangalore": (12.9716, 77.5946),
    "kerala": (10.8505, 76.2711), "thiruvananthapuram": (8.5241, 76.9366),
    "madhya pradesh": (22.9734, 78.6569), "bhopal": (23.2599, 77.4126),
    "maharashtra": (19.7515, 75.7139), "mumbai": (19.0760, 72.8777),
    "manipur": (24.6637, 93.9063), "imphal": (24.8170, 93.9368),
    "meghalaya": (25.4670, 91.3662), "shillong": (25.5788, 91.8933),
    "mizoram": (23.1645, 92.9376), "aizawl": (23.7271, 92.7176),
    "nagaland": (26.1584, 94.5624), "kohima": (25.6751, 94.1086),
    "odisha": (20.9517, 85.0985), "bhubaneswar": (20.2961, 85.8245),
    "punjab": (31.1471, 75.3412), "chandigarh": (30.7333, 76.7794),
    "rajasthan": (27.0238, 74.2179), "jaipur": (26.9124, 75.7873),
    "sikkim": (27.5330, 88.5122), "gangtok": (27.3389, 88.6065),
    "tamil nadu": (11.1271, 78.6569), "chennai": (13.0827, 80.2707),
    "telangana": (18.1124, 79.0193), "hyderabad": (17.3850, 78.4867),
    "tripura": (23.9408, 91.9882), "agartala": (23.8315, 91.2868),
    "uttar pradesh": (26.8467, 80.9462), "lucknow": (26.8467, 80.9462),
    "uttarakhand": (30.0668, 79.0193), "dehradun": (30.3165, 78.0322),
    "west bengal": (22.9868, 87.8550), "kolkata": (22.5726, 88.3639),
    # union territories
    "andaman and nicobar islands": (11.7401, 92.6586), "port blair": (11.6234, 92.7265),
    "chandigarh": (30.7333, 76.7794),
    "dadra and nagar haveli and daman and diu": (20.3974, 72.8328), "daman": (20.3974, 72.8328),
    "lakshadweep": (10.5667, 72.6417), "kavaratti": (10.5626, 72.6369),
    "delhi": (28.7041, 77.1025),
    "puducherry": (11.9416, 79.8083),
    "jammu and kashmir": (33.2778, 75.3412), "srinagar": (34.0837, 74.7973),
    "ladakh": (34.1526, 77.5770), "leh": (34.1526, 77.5770)
    }

def get_lat_long(state_name):
    return state_coordinates.get(state_name, (None, None))


# Example usage
def fetcher():
    origin = input("Enter the origin state, UT, capital, or major city name: ").lower()
    destination = input("Enter the destination state, UT, capital, or major city name: ").lower()

    origin_lat, origin_long = get_lat_long(origin)
    destination_lat, destination_long = get_lat_long(destination)

    if None not in (origin_lat, origin_long, destination_lat, destination_long):
        return origin_lat, origin_long, destination_lat, destination_long
    else:
        print("Invalid origin or destination name or not found!")
        return None, None, None, None


print(fetcher())