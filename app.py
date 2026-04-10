import streamlit as st
import pandas as pd
import pickle

# 1. Load the Saved Brain and Map
try:
    with open('car_model.pkl', 'rb') as file:
        model_data = pickle.load(file)
    model = model_data['model']
    expected_columns = model_data['columns']
except FileNotFoundError:
    st.error("Error: 'car_model.pkl' not found. Make sure it is in the same folder as this script!")
    st.stop()

# 2. Build the Visual Interface
st.title("🚗 Used Car Price Predictor")
st.write("Enter the details of a car to instantly estimate its market value.")

col1, col2 = st.columns(2)

with col1:
    # Using text input for brand/model so you can type any car that was in the dataset
    brand = st.text_input("Brand (e.g., Kia, Maruti, BMW)", value="Kia")
    model_name = st.text_input("Exact Model Name (e.g., Seltos GTX Plus)", value="Seltos GTX Plus")
    year = st.slider("Manufacturing Year", min_value=2000, max_value=2024, value=2019)
    kms = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=18000)
    seats = st.selectbox("Number of Seats", [4, 5, 6, 7, 8], index=1)

with col2:
    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    owner = st.selectbox("Ownership History", ["First Owner", "Second Owner", "Third Owner", "Fourth Owner", "Fifth Owner"])
    engine = st.number_input("Engine Capacity (cc)", min_value=500, max_value=5000, value=1353)
    mileage = st.number_input("Mileage (kmpl)", min_value=5.0, max_value=40.0, value=16.5)

# 3. The Prediction Button Logic
if st.button("Predict Market Price", type="primary"):
    
    # Create the blank row filled with zeros
    input_data = {col: 0 for col in expected_columns}
    
    # Fill in the numerical data
    input_data['manufacturing_year'] = year
    input_data['kms_driven'] = kms
    input_data['seats'] = seats
    input_data['mileage(kmpl)'] = mileage
    input_data['engine(cc)'] = engine
    
    # Turn the specific text categories into 1s (True) based on what the user selected
    if f"brand_{brand}" in expected_columns:
        input_data[f"brand_{brand}"] = 1
    if f"model_name_{model_name}" in expected_columns:
        input_data[f"model_name_{model_name}"] = 1
    if f"fuel_type_{fuel}" in expected_columns:
        input_data[f"fuel_type_{fuel}"] = 1
    if f"transmission_{transmission}" in expected_columns:
        input_data[f"transmission_{transmission}"] = 1
    if f"ownsership_{owner}" in expected_columns:
        input_data[f"ownsership_{owner}"] = 1

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Ask the model for the price
    prediction = model.predict(input_df)[0]
    
    # Display the result
    st.success(f"### Estimated Value: ₹ {prediction:.2f} Lakhs")
    st.balloons()