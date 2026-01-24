import streamlit as st
import pandas as pd
import joblib

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Heart Attack Risk Test",
    page_icon="💔",
    layout="wide"
)

MODEL_PATH = "models/heart_attack_detection.pkl"
THRESHOLD = 0.35  # binary classification

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# ---------------- UI ----------------
st.markdown(
    "<h1 style='text-align:center;'>❤️ Heart Attack Risk Prediction</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:gray;'>Binary classification screening tool</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# Centered layout
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    with st.form("heart_attack_form"):

        st.subheader("Patient Information")

        # -------- Numeric Inputs --------
        age = st.number_input("Age", 1, 120, 55)
        resting_bp = st.number_input("Resting Blood Pressure (mmHg)", 80, 250, 120)
        cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 250)
        max_hr = st.number_input("Max Heart Rate", 60, 220, 150)
        oldpeak = st.number_input("Oldpeak", 0.0, 10.0, 1.0)

        # -------- Categorical / Binary Inputs --------
        sex = st.selectbox("Sex", ["Female", "Male"])
        fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["No", "Yes"])
        exercise_angina = st.selectbox("Exercise Induced Angina", ["No", "Yes"])

        chest_pain = st.selectbox(
            "Chest Pain Type",
            ["ATA", "NAP", "TA", "ASY"]
        )

        resting_ecg = st.selectbox(
            "Resting ECG",
            ["Normal", "ST", "LVH"]
        )

        st_slope = st.selectbox(
            "ST Slope",
            ["Up", "Flat", "Down"]
        )

        submit = st.form_submit_button("Predict Risk")

# ---------------- PREDICTION ----------------
if submit:
    input_data = {
        # numeric
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,

        # binary
        "FastingBS": 1 if fasting_bs == "Yes" else 0,
        "Sex_M": 1 if sex == "Male" else 0,

        "ChestPainType_ATA": 1 if chest_pain == "ATA" else 0,
        "ChestPainType_NAP": 1 if chest_pain == "NAP" else 0,
        "ChestPainType_TA": 1 if chest_pain == "TA" else 0,

        "RestingECG_Normal": 1 if resting_ecg == "Normal" else 0,
        "RestingECG_ST": 1 if resting_ecg == "ST" else 0,

        "ExerciseAngina_Y": 1 if exercise_angina == "Yes" else 0,

        "ST_Slope_Flat": 1 if st_slope == "Flat" else 0,
        "ST_Slope_Up": 1 if st_slope == "Up" else 0,
    }

    X = pd.DataFrame([input_data])

    prob = model.predict_proba(X)[0, 1]
    prediction = int(prob >= THRESHOLD)

    st.markdown("---")
    st.subheader("Result")

    if prediction == 1:
        st.error(
            f"⚠️ **Heart Attack Risk: YES**\n\n"
            f"Probability: **{prob * 100:.2f}%**"
        )
    else:
        st.success(
            f"✅ **Heart Attack Risk: NO**\n\n"
            f"Probability: **{prob * 100:.2f}%**"
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray; font-size:0.9rem;'>"
    "Disclaimer: This tool is for educational screening only and does not replace medical advice."
    "</p>",
    unsafe_allow_html=True
)
