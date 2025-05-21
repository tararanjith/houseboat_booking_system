import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("D://Allapy//final_datasetHB.csv")

# Ensure 'number_of_days' exists before filtering
if 'duration' in df.columns:
    df = df[df["duration"] == 1]  # Only keep 1-day bookings

# Encode categorical variables
label_encoders = {}
for col in ['houseboat_type', 'season']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# ---- USER INPUT SECTION ----
def predict_dynamic_price():
    print("\nEnter houseboat details for dynamic price prediction:")

    capacity = int(input("Capacity (number of people): "))
    bedrooms = int(input("Number of bedrooms: "))

    houseboat_type = input("Houseboat type (S for Standard, L for Luxury): ").strip().upper()
    houseboat_type = "Standard" if houseboat_type == "S" else "Luxury"

    season = input("Season (P for Peak, O for Off-Season): ").strip().upper()
    season = "Peak" if season == "P" else "Off-Season"

    # Encode categorical inputs
    houseboat_type_encoded = label_encoders['houseboat_type'].transform([houseboat_type])[0]
    season_encoded = label_encoders['season'].transform([season])[0]

    # **Find similar boats (ONLY 1-day bookings)**
    similar_boats = df[
        (df["capacity"] == capacity) & 
        (df["bedrooms"] == bedrooms) & 
        (df["houseboat_type"] == houseboat_type_encoded) & 
        (df["season"] == season_encoded)
    ]

    # **Compute base price (median of similar boats)**
    base_price = similar_boats["base_price"].median()

    if pd.isna(base_price):  
        base_price = df["base_price"].median()  # Use global median if no similar boats

    # **Apply seasonal multiplier**
    seasonal_multiplier = 1.2 if season == "Peak" else 0.85
    predicted_price = base_price * seasonal_multiplier

    # **Find actual dataset prices (for validation)**
    actual_prices = similar_boats["final_price"].tolist()

    if len(actual_prices) > 0:
        median_actual_price = np.median(actual_prices)
        price_diff = abs(predicted_price - median_actual_price)

        # **Adjust price if difference > 20%**
        if price_diff > (0.2 * median_actual_price):
            predicted_price = (predicted_price + median_actual_price) / 2  

    # **Print results**
    print("\n🔹 **Predicted Dynamic Price:** ₹{:.2f}".format(predicted_price))

# Run user input function
predict_dynamic_price()
>Enter houseboat details for dynamic price prediction:

🔹 **Predicted Dynamic Price:** ₹8500.00
