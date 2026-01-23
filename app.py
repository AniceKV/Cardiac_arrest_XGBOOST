import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Cardiac Risk Assessment",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .very-low { background-color: #d4edda; color: #155724; }
    .low { background-color: #d1ecf1; color: #0c5460; }
    .moderate { background-color: #fff3cd; color: #856404; }
    .high { background-color: #f8d7da; color: #721c24; }
    .very-high { background-color: #f5c6cb; color: #721c24; }
    </style>
""", unsafe_allow_html=True)

MODEL_PATH = "models/cardiac_failure_detection.pkl"
THRESHOLD = 0.35

BINS = [0.0, 0.20, 0.35, 0.50, 0.70, 1.0]
LABELS = ["Very Low Risk", "Low Risk", "Moderate Risk", "High Risk", "Very High Risk"]

FEATURES = ["age", "gender", "height", "weight", "bmi",
            "ap_hi", "ap_lo", "cholesterol", "gluc",
            "smoke", "alco", "active"]




@st.cache_resource
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        st.error(f" Model file '{MODEL_PATH}' not found. Please ensure the model is in the correct directory.")
        return None


def predict_risk(inputs: dict, model):
    X = pd.DataFrame([inputs], columns=FEATURES)
    X['age'] = X['age'] / 100.0
    X['gender'] = X['gender'] - 1
    X['cholesterol'] = (X['cholesterol'] - 1) / 2.0
    X['bmi']=X['weight']/((X['height']*0.01)**2)
    prob = model.predict_proba(X)[0, 1]
    prediction = int(prob >= THRESHOLD)

    risk_zone = pd.cut([prob], bins=BINS, labels=LABELS, include_lowest=True)[0]

    return {
        "probability": round(float(prob), 4),
        "screening_prediction": prediction,
        "risk_zone": str(risk_zone),
        "input_summary": inputs
    }


def create_gauge_chart(probability):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Probability (%)", 'font': {'size': 24}},
        number={'suffix': "%", 'font': {'size': 48}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 20], 'color': '#d4edda'},
                {'range': [20, 35], 'color': '#d1ecf1'},
                {'range': [35, 50], 'color': '#fff3cd'},
                {'range': [50, 70], 'color': '#f8d7da'},
                {'range': [70, 100], 'color': '#f5c6cb'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': THRESHOLD * 100
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"},
        height=400
    )

    return fig


def main():
    # Header
    st.markdown('<div class="main-header">❤️ Cardiac Risk Assessment System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Cardiovascular Health Screening Tool</div>', unsafe_allow_html=True)

    model = load_model()
    if model is None:
        st.stop()

    st.sidebar.header(" Patient Information")
    st.sidebar.markdown("---")

    st.sidebar.subheader("Demographics")
    age = st.sidebar.number_input("Age (years)", min_value=1, max_value=120, value=55, step=1)
    gender = st.sidebar.selectbox("Gender", options=[1, 2], format_func=lambda x: "Female" if x == 1 else "Male")
    height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=165, step=1)
    weight = st.sidebar.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=65.0, step=0.5)

    st.sidebar.subheader("Vital Signs")
    ap_hi = st.sidebar.number_input("Systolic BP (mmHg)", min_value=80, max_value=250, value=120, step=1)
    ap_lo = st.sidebar.number_input("Diastolic BP (mmHg)", min_value=40, max_value=150, value=80, step=1)

    st.sidebar.subheader("Lab Results")
    cholesterol = st.sidebar.selectbox(
        "Cholesterol Level",
        options=[1, 2, 3],
        format_func=lambda x: {1: "Normal", 2: "Above Normal", 3: "Well Above Normal"}[x]
    )
    gluc = st.sidebar.selectbox(
        "Glucose Level",
        options=[1, 2, 3],
        format_func=lambda x: {1: "Normal", 2: "Above Normal", 3: "Well Above Normal"}[x]
    )

    # Lifestyle Factors
    st.sidebar.subheader("Lifestyle")
    smoke = st.sidebar.checkbox("Smoker")
    alco = st.sidebar.checkbox("Alcohol Consumer")
    active = st.sidebar.checkbox("Physically Active", value=True)

    st.sidebar.markdown("---")
    predict_button = st.sidebar.button(" Assess Risk", type="primary", use_container_width=True)

    # Main content area
    if predict_button:
        # Prepare input data
        inputs = {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "ap_hi": ap_hi,
            "ap_lo": ap_lo,
            "cholesterol": cholesterol,
            "gluc": gluc,
            "smoke": int(smoke),
            "alco": int(alco),
            "active": int(active)
        }

        # Get prediction
        with st.spinner("Analyzing patient data..."):
            result = predict_risk(inputs, model)

        # Display results
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader(" Risk Assessment")
            fig = create_gauge_chart(result['probability'])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader(" Assessment Results")
            st.markdown(f"**Risk Probability:** {result['probability'] * 100:.2f}%")

            # Risk zone with color coding
            risk_class_map = {
                "Very Low Risk": "very-low",
                "Low Risk": "low",
                "Moderate Risk": "moderate",
                "High Risk": "high",
                "Very High Risk": "very-high"
            }
            risk_class = risk_class_map.get(result['risk_zone'], 'moderate')
            st.markdown(f'<div class="risk-box {risk_class}">{result["risk_zone"]}</div>', unsafe_allow_html=True)

            # Screening recommendation
            st.markdown("---")
            if result['screening_prediction'] == 1:
                st.error(
                    "**POSITIVE SCREENING**\n\nRecommendation: Further cardiac evaluation advised. Please consult with a cardiologist.")
            else:
                st.success(
                    "**NEGATIVE SCREENING**\n\nRecommendation: Patient appears to be at lower risk. Continue regular health monitoring.")

            # BMI calculation
            bmi = weight / ((height / 100) ** 2)
            st.markdown("---")
            st.markdown(f"**Body Mass Index (BMI):** {bmi:.1f}")

        # Additional Information
        st.markdown("---")
        st.subheader(" Patient Summary")

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:
            st.metric("Age", f"{age} years")
            st.metric("Gender", "Female" if gender == 1 else "Male")
            st.metric("BMI", f"{bmi:.1f}")

        with summary_col2:
            st.metric("Blood Pressure", f"{ap_hi}/{ap_lo} mmHg")
            st.metric("Cholesterol", {1: "Normal", 2: "Above Normal", 3: "Well Above Normal"}[cholesterol])
            st.metric("Glucose", {1: "Normal", 2: "Above Normal", 3: "Well Above Normal"}[gluc])

        with summary_col3:
            st.metric("Smoker", "Yes" if smoke else "No")
            st.metric("Alcohol", "Yes" if alco else "No")
            st.metric("Physical Activity", "Yes" if active else "No")

    else:
        # Initial state - show instructions
        st.info(" Please enter patient information in the sidebar and click 'Assess Risk' to begin the evaluation.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### Purpose")
            st.write(
                "This tool provides preliminary cardiac risk assessment based on patient vitals, lab results, and lifestyle factors.")

        with col2:
            st.markdown("###  How It Works")
            st.write(
                "Using machine learning algorithms trained on cardiovascular health data to identify potential risk factors.")

        with col3:
            st.markdown("### Disclaimer")
            st.write(
                "This is a screening tool only. Always consult healthcare professionals for medical diagnosis and treatment.")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
        " <b>Medical Disclaimer:</b> This application is for screening purposes only and does not replace professional medical advice, diagnosis, or treatment."
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()