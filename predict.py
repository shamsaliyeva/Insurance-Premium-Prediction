import streamlit as st
import pickle
import pandas as pd

def load_model():
    with open('saved_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
random_forest = data['model']
scaler = data['scaler']
encoder = data['encoder']

def show_prediction():
    st.set_page_config(page_title="Insurance Premium Prediction", page_icon="📊")
    st.image('image.png')
    st.title("Insurance Premium Prediction")
    st.write("""### Please provide the following customer details to estimate their insurance expenses:""")

    # Gender selection
    gender = ('Male', 'Female')
    sex = st.selectbox("Select Customer's Gender", gender, index = None, placeholder="Choose an option")

    # Region selection
    location = ('southeast', 'southwest', 'northwest', 'northeast')
    region = st.selectbox("Select Customer's Region", location, index = None,  placeholder="Choose an option")

    # Age input
    age = st.number_input("Enter Customer's Age (years)", min_value=0, max_value=120, step=1)

    # Children input
    children = st.number_input("Enter Number of Customer's Children", min_value=0, step=1)

    # BMI input
    bmi = st.number_input("Enter Customer's Body Mass Index (BMI)", min_value=0.0, format="%.2f")

    # Smoking status input
    smoking = st.radio("Select Customer's Smoking Status", ("Non-smoker", "Smoker"))

    # Create a DataFrame with all possible columns for the input
    input_data = pd.DataFrame({
        'age': [age],
        'bmi': [bmi],
        'children': [children],
        'sex_female': [1 if sex == 'Female' else 0],
        'sex_male': [1 if sex == 'Male' else 0],
        'smoker_no': [1 if smoking == "Non-smoker" else 0],
        'smoker_yes': [1 if smoking == "Smoker" else 0],
        'region_northeast': [1 if region == 'northeast' else 0],
        'region_northwest': [1 if region == 'northwest' else 0],
        'region_southeast': [1 if region == 'southeast' else 0],
        'region_southwest': [1 if region == 'southwest' else 0],
    })

    # Scaling the numerical features
    numerical_features = ['age', 'bmi', 'children']
    input_data[numerical_features] = scaler.transform(input_data[numerical_features])

    # Calculate expenses button
    if st.button("Calculate Estimated Expenses"):
        if not sex or not region:
            st.warning("Please select both the customer's gender and region before calculating expenses.")
        else:
            prediction = random_forest.predict(input_data)
            st.subheader(f"The estimated insurance expense for the customer is: **${prediction[0]:.2f}**")
            st.success("Information processed successfully!")
