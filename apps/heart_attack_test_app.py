import streamlit as st
import pandas as pd
import joblib
import shap
from streamlit_shap import st_shap

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Heart Attack Risk Test",
    page_icon="❤️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    /* Main background with soft skin tint */
    .main {
        background: linear-gradient(135deg, #FFF5F5 0%, #FFE9E9 100%);
    }

    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #FF6B9D 0%, #C9184A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        text-align: center;
        color: #8B5A5A;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Form container */
    .stForm {
        background: #FFF0F3;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(201, 24, 74, 0.08);
        border: 1px solid #FFE0E9;
    }

    /* Input fields */
    .stNumberInput input, .stSelectbox select {
        border-radius: 10px;
        border: 1.5px solid #FFD6E0;
        background: #FFFAFA;
        color: #2D3748;
        transition: all 0.3s ease;
    }

    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #FF6B9D;
        box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.1);
        background: #FFFBFC;
    }

    /* Labels */
    label {
        color: #6B4848 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    /* Submit button */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B9D 0%, #C9184A 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(201, 24, 74, 0.25);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(201, 24, 74, 0.35);
    }

    /* Result cards */
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }

    /* Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #FFD6E0, transparent);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: #FFF0F3;
        border-radius: 10px;
        border: 1px solid #FFE9EE;
        color: #6B4848;
        font-weight: 600;
    }

    .streamlit-expanderContent {
        background: #FFF8FA;
        border: 1px solid #FFE9EE;
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 1rem;
    }

    /* Section headers */
    h2, h3 {
        color: #6B4848;
        font-weight: 600;
    }

    /* Metrics */
    .stMetric {
        background: #FFFBFC;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #FFE9EE;
    }

    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, #FFF5F7 0%, #FFE9F0 100%);
        border-left: 4px solid #FF6B9D;
    }

    .stSuccess {
        background: linear-gradient(135deg, #F0FFF4 0%, #E6F9ED 100%);
        border-left: 4px solid #48BB78;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #8B5A5A;
        font-size: 0.9rem;
        padding: 2rem 0 1rem 0;
    }

    /* Card effect for result column */
    .result-card {
        background: #FFF0F3;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(201, 24, 74, 0.08);
        border: 1px solid #FFE0E9;
        min-height: 400px;
    }
</style>
""", unsafe_allow_html=True)

MODEL_PATH = "models/heart_attack_detection.pkl"
THRESHOLD = 0.35


# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()

# ---------------- HEADER ----------------
st.markdown("<h1 class='main-header'>❤️ Heart Attack Risk Assessment</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>AI-Powered Cardiovascular Screening Tool by CorVigil</p>", unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ----------------
form_col, result_col = st.columns([1.6, 1.4], gap="large")

with form_col:
    with st.form("heart_attack_form"):
        st.markdown("<h3 style='color: #2D3748;'>📋 Patient Information</h3>", unsafe_allow_html=True)
        st.markdown("")

        # -------- INPUT GRID --------
        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            age = st.number_input("Age", 1, 120, 55)
            sex = st.selectbox("Sex", ["Female", "Male"])
            chest_pain = st.selectbox(
                "Chest Pain Type",
                ["ATA", "NAP", "TA", "ASY"]
            )

        with col2:
            resting_bp = st.number_input("Resting BP (mmHg)", 80, 250, 120)
            cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 250)
            fasting_bs = st.selectbox("Fasting Blood Sugar > 120", ["No", "Yes"])

        with col3:
            max_hr = st.number_input("Max Heart Rate", 60, 220, 150)
            oldpeak = st.number_input("Oldpeak", 0.0, 10.0, 1.0)
            exercise_angina = st.selectbox("Exercise Angina", ["No", "Yes"])

        st.markdown("")
        col4, col5 = st.columns(2, gap="medium")

        with col4:
            resting_ecg = st.selectbox(
                "Resting ECG",
                ["Normal", "ST", "LVH"]
            )

        with col5:
            st_slope = st.selectbox(
                "ST Slope",
                ["Up", "Flat", "Down"]
            )

        st.markdown("")
        submit = st.form_submit_button(
            "🔍 Analyze Risk",
            use_container_width=True
        )

# ---------------- PREDICTION & RESULTS ----------------
with result_col:
    if not submit:
        st.markdown("### 📊 Results")
        st.markdown("")
        st.info("👈 Fill out the form and click **Analyze Risk** to see your cardiovascular risk assessment")
        st.markdown("")
        st.markdown("#### What to expect:")
        st.markdown("• Risk probability score")
        st.markdown("• Key contributing factors")
        st.markdown("• Personalized recommendations")
    else:
        # Prepare the input for the model
        input_data = {
            "Age": age,
            "RestingBP": resting_bp,
            "Cholesterol": cholesterol,
            "MaxHR": max_hr,
            "Oldpeak": oldpeak,
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

        st.markdown("### 📊 Assessment Result")
        st.markdown("")

        if prediction == 1:
            st.error(
                f"**⚠️ Elevated Risk Detected**\n\n"
                f"Risk Probability: **{prob * 100:.1f}%**\n\n"
                f"Threshold: {THRESHOLD * 100:.0f}%"
            )
            st.markdown("**Recommendation:** Please consult with a healthcare provider for further evaluation.")
        else:
            st.success(
                f"**✅ Low Risk Assessment**\n\n"
                f"Risk Probability: **{prob * 100:.1f}%**\n\n"
                f"Threshold: {THRESHOLD * 100:.0f}%"
            )
            st.markdown("**Recommendation:** Continue maintaining healthy lifestyle habits.")

# ---------------- SHAP EXPLANATION SECTION ----------------
if submit:
    st.markdown("")
    st.markdown("### 🎯 Risk Factor Analysis")
    st.markdown("Understanding what's influencing your assessment")

    try:
        actual_model = model[-1]
        explainer = shap.Explainer(actual_model)
        shap_v = explainer(X)
        values = shap_v.values[0]
        feature_names = X.columns.tolist()

        # Feature information dictionary
        feature_info = {
            "age": {
                "display_name": "Age",
                "risk_description": "Age is a natural risk factor - cardiovascular risk typically increases with age due to cumulative wear on the heart and blood vessels.",
                "protective_description": "Your age group shows lower baseline cardiovascular risk. Maintaining healthy habits now provides strong long-term protection.",
                "recommendations": [
                    "Continue regular cardiovascular screenings",
                    "Maintain heart-healthy lifestyle habits",
                    "Monitor blood pressure and cholesterol annually"
                ]
            },
            "restingbp": {
                "display_name": "Resting Blood Pressure",
                "risk_description": "Elevated blood pressure means your heart is working harder to pump blood, which can strain the cardiovascular system over time.",
                "protective_description": "Your blood pressure is in a healthy range, reducing strain on your heart and blood vessels.",
                "recommendations": [
                    "Reduce sodium intake to less than 2,300mg daily",
                    "Engage in regular aerobic exercise (150 min/week)",
                    "Practice stress management techniques",
                    "Maintain healthy body weight"
                ]
            },
            "cholesterol": {
                "display_name": "Cholesterol Level",
                "risk_description": "Elevated cholesterol can lead to plaque buildup in arteries, restricting blood flow and increasing heart disease risk.",
                "protective_description": "Your cholesterol levels are well-managed, supporting clear and healthy blood vessels.",
                "recommendations": [
                    "Increase fiber intake (oats, beans, fruits)",
                    "Choose healthy fats (olive oil, avocados, nuts)",
                    "Limit saturated fats and trans fats",
                    "Consider omega-3 fatty acids (fish, flaxseed)"
                ]
            },
            "maxhr": {
                "display_name": "Maximum Heart Rate",
                "risk_description": "Your maximum heart rate response during exercise can indicate cardiovascular fitness and overall heart health.",
                "protective_description": "Your heart rate response shows good cardiovascular fitness.",
                "recommendations": [
                    "Continue regular cardiovascular exercise",
                    "Monitor heart rate during physical activity",
                    "Gradually increase exercise intensity over time"
                ]
            },
            "oldpeak": {
                "display_name": "ST Depression (Oldpeak)",
                "risk_description": "ST depression on an ECG can indicate reduced blood flow to the heart during stress or exercise.",
                "protective_description": "Your ECG shows healthy heart electrical activity during stress.",
                "recommendations": [
                    "Continue regular cardiac monitoring",
                    "Maintain current exercise routine",
                    "Follow up with cardiologist as recommended"
                ]
            },
            "sex": {
                "display_name": "Biological Sex",
                "risk_description": "Biological factors related to sex hormones and genetics can influence cardiovascular risk patterns.",
                "protective_description": "Your biological profile shows favorable cardiovascular risk patterns.",
                "recommendations": [
                    "Be aware of sex-specific risk factors",
                    "Women: Monitor cardiovascular health after menopause",
                    "Men: Increased vigilance after age 45"
                ]
            },
            "chestpain": {
                "display_name": "Chest Pain Pattern",
                "risk_description": "Certain chest pain patterns can indicate reduced blood flow to the heart muscle.",
                "protective_description": "Your chest pain pattern shows lower cardiac risk characteristics.",
                "recommendations": [
                    "Report any new or changing chest discomfort to your doctor",
                    "Learn to recognize cardiac vs non-cardiac chest pain",
                    "Seek immediate care for severe chest pain"
                ]
            },
            "fastingbs": {
                "display_name": "Fasting Blood Sugar",
                "risk_description": "Elevated fasting blood sugar can damage blood vessels and increase cardiovascular disease risk.",
                "protective_description": "Your blood sugar is well-controlled, protecting your blood vessels.",
                "recommendations": [
                    "Monitor carbohydrate portions",
                    "Choose complex carbs over simple sugars",
                    "Exercise regularly to improve insulin sensitivity",
                    "Get HbA1c tested if glucose remains elevated"
                ]
            },
            "restingecg": {
                "display_name": "Resting ECG",
                "risk_description": "ECG abnormalities can indicate heart muscle changes or previous cardiac events.",
                "protective_description": "Your resting ECG shows normal heart electrical activity.",
                "recommendations": [
                    "Continue regular ECG monitoring",
                    "Report any new symptoms to your doctor",
                    "Maintain heart-healthy lifestyle"
                ]
            },
            "exerciseangina": {
                "display_name": "Exercise-Induced Angina",
                "risk_description": "Chest pain during exercise can indicate inadequate blood flow to the heart muscle.",
                "protective_description": "No exercise-induced chest pain indicates good cardiac perfusion.",
                "recommendations": [
                    "Report any exercise-related chest discomfort",
                    "Gradually increase exercise intensity",
                    "Warm up and cool down properly"
                ]
            },
            "stslope": {
                "display_name": "ST Slope Pattern",
                "risk_description": "Abnormal ST slope patterns can indicate cardiac stress and reduced blood flow.",
                "protective_description": "Your ST slope pattern shows healthy cardiac stress response.",
                "recommendations": [
                    "Continue regular cardiac assessments",
                    "Maintain current fitness level",
                    "Follow cardiologist recommendations"
                ]
            }
        }

        # Build and sort factors
        factors = []
        for val, name in zip(values, feature_names):
            base_name = name.lower().replace("_", "").replace(" ", "")

            feature_data = None
            for key in feature_info.keys():
                if key in base_name or base_name.startswith(key):
                    feature_data = feature_info[key]
                    break

            if feature_data:
                factors.append({
                    "name": feature_data["display_name"],
                    "impact": val,
                    "risk_desc": feature_data["risk_description"],
                    "protective_desc": feature_data["protective_description"],
                    "recommendations": feature_data["recommendations"]
                })

        factors = sorted(factors, key=lambda x: abs(x['impact']), reverse=True)

        # Display top 4 factors
        for i, f in enumerate(factors[:4], 1):
            is_risk = f['impact'] > 0

            with st.expander(
                    f"**{i}. {f['name']}** {'⚠️ Risk Factor' if is_risk else '✅ Protective Factor'}",
                    expanded=(i <= 2)
            ):
                col1, col2 = st.columns([2.5, 1])

                with col1:
                    if is_risk:
                        st.markdown("**📌 Impact:**")
                        st.write(f['risk_desc'])
                    else:
                        st.markdown("**📌 Benefit:**")
                        st.write(f['protective_desc'])

                with col2:
                    impact_magnitude = min(abs(f['impact']), 1.0)
                    st.metric(
                        "Strength",
                        f"{impact_magnitude * 100:.0f}%",
                        delta="Higher" if is_risk else "Lower",
                        delta_color="inverse" if is_risk else "normal"
                    )

                st.markdown(f"**{'📋 Actions to Take' if is_risk else '🌟 Keep It Up'}:**")
                for rec in f['recommendations']:
                    st.markdown(f"• {rec}")

        # Summary
        st.markdown("---")
        risk_count = sum(1 for f in factors[:4] if f['impact'] > 0)
        protective_count = 4 - risk_count

        if risk_count > protective_count:
            st.info(
                f"💡 **Action Plan:** {risk_count} modifiable risk factors identified. "
                f"Focus on the high-impact factors first for maximum benefit."
            )
        else:
            st.success(
                f"💡 **Great News:** {protective_count} protective factors are working in your favor. "
                f"Continue these healthy habits for optimal cardiovascular health."
            )

    except Exception as e:
        st.info(
            "📊 **Clinical Assessment:** Your data has been analyzed. "
            "Continue regular health monitoring and maintain heart-healthy lifestyle habits."
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p class='footer-text'>"
    "⚕️ Medical Disclaimer: This tool is for educational and screening purposes only. "
    "It does not replace professional medical diagnosis or advice. "
    "Please consult with a qualified healthcare provider for medical concerns."
    "</p>",
    unsafe_allow_html=True
)