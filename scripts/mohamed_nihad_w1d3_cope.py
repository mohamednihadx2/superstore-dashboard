import streamlit as st
import pandas as pd

st.title("🏋️ Health & Fitness Calculator")
st.write("Calculate your BMI, daily calorie needs, and ideal weight range.")
st.markdown("---")

st.header("Personal Details")

name = st.text_input("Enter your Name")

age = st.number_input(
    "Enter your Age",
    min_value=10,
    max_value=100,
    value=20
)

sex = st.radio(
    "Select Gender",
    ["Male", "Female"],
    horizontal=True
)

weight = st.slider(
    "Weight (kg)",
    min_value=30.0,
    max_value=150.0,
    step=0.5,
    value=60.0
)

height = st.slider(
    "Height (cm)",
    min_value=100,
    max_value=220,
    value=170
)

st.write(
    f"Name: {name}, Age: {age}, Gender: {sex}, Weight: {weight} kg, Height: {height} cm"
)


st.header("BMI Calculator")

height_m = height / 100
bmi = round(weight / (height_m ** 2), 1)

st.metric("BMI", bmi)

if bmi < 18.5:
    bmi_class = "Underweight"
    health_risk = "Moderate"
    st.warning(f"{bmi_class} - Health Risk: {health_risk}")

elif bmi < 25:
    bmi_class = "Normal Weight"
    health_risk = "Low"
    st.success(f"{bmi_class} - Health Risk: {health_risk}")

elif bmi < 30:
    bmi_class = "Overweight"
    health_risk = "Elevated"
    st.warning(f"{bmi_class} - Health Risk: {health_risk}")

else:
    bmi_class = "Obese"
    health_risk = "High"
    st.error(f"{bmi_class} - Health Risk: {health_risk}")


st.header("Daily Calorie Need")

activity_options = {
    "Sedentary (desk job)": 1.2,
    "Lightly active (1–3 days/wk)": 1.375,
    "Moderately active (3–5 days)": 1.55,
    "Very active (6–7 days)": 1.725,
    "Extra active (athlete)": 1.9
}

activity = st.selectbox(
    "Select Activity Level",
    list(activity_options.keys())
)

multiplier = activity_options[activity]

# BMR Calculation
if sex == "Male":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

daily_calories = round(bmr * multiplier)

st.metric("Daily Calories Needed", f"{daily_calories} kcal")

st.header("Ideal Weight Range")

if sex == "Male":
    ideal_weight = 52 + 1.9 * ((height / 2.54) - 60)
else:
    ideal_weight = 49 + 1.7 * ((height / 2.54) - 60)

low_weight = round(ideal_weight * 0.9, 1)
high_weight = round(ideal_weight * 1.1, 1)

col1, col2 = st.columns(2)

with col1:
    st.metric("Low Range", f"{low_weight} kg")

with col2:
    st.metric("High Range", f"{high_weight} kg")

    st.header("Full Summary")

if st.button("Show my summary"):

    st.write(f"### Hello {name}")

    st.write(f"""
    **Age:** {age}

    **Gender:** {sex}

    **Weight:** {weight} kg

    **Height:** {height} cm

    **BMI:** {bmi} ({bmi_class})

    **Health Risk:** {health_risk}

    **Daily Calories Needed:** {daily_calories} kcal

    **Ideal Weight Range:** {low_weight} kg - {high_weight} kg
    """)
