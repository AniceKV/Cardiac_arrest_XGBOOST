import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Cardiac Risk Assessment",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
    }

    .sub-header {
        font-size: 1.3rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 500;
    }

    /* Card styling */
    .info-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }

    .result-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
        min-height: 400px;
    }

    /* Risk box styling */
    .risk-box {
        padding: 24px;
        border-radius: 12px;
        margin: 16px 0;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }

    .risk-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
    }

    .very-low { 
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        border: 2px solid #b1dfbb;
    }
    .low { 
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        border: 2px solid #abdde5;
    }
    .moderate { 
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        border: 2px solid #ffe082;
    }
    .high { 
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        border: 2px solid #f1b0b7;
    }
    .very-high { 
        background: linear-gradient(135deg, #f5c6cb 0%, #f17a7a 100%);
        color: #721c24;
        border: 2px solid #e08e8e;
    }

    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }

    /* Input sections */
    .input-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }

    div[data-testid="metric-container"] > label {
        font-weight: 600 !important;
        color: #475569 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 8px;
        font-weight: 600;
        padding: 1rem;
    }

    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border-left-width: 4px;
    }

    /* Spacing */
    div[data-testid="stHorizontalBlock"] {
        gap: 1.5rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        margin-top: 3rem;
        color: #475569;
        font-size: 0.95rem;
    }

    /* Form sections */
    .stForm {
        background: linear-gradient(135deg, #fff5f7 0%, #ffe8f0 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid #ffc4d6;
    }

    /* Form input styling for better contrast */
    .stForm label {
        color: #1e293b !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8),
                     -1px -1px 2px rgba(255, 255, 255, 0.8),
                     1px -1px 2px rgba(255, 255, 255, 0.8),
                     -1px 1px 2px rgba(255, 255, 255, 0.8);
    }

    .stForm .stMarkdown h4 {
        color: #1e293b !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8),
                     -1px -1px 2px rgba(255, 255, 255, 0.8),
                     1px -1px 2px rgba(255, 255, 255, 0.8),
                     -1px 1px 2px rgba(255, 255, 255, 0.8);
    }

    /* Section icons with better visibility */
    .stForm .stMarkdown p {
        color: #1e293b !important;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8),
                     -1px -1px 2px rgba(255, 255, 255, 0.8),
                     1px -1px 2px rgba(255, 255, 255, 0.8),
                     -1px 1px 2px rgba(255, 255, 255, 0.8);
    }

    /* Checkbox labels - make them black */
    .stCheckbox label {
        color: #000000 !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8),
                     -1px -1px 2px rgba(255, 255, 255, 0.8),
                     1px -1px 2px rgba(255, 255, 255, 0.8),
                     -1px 1px 2px rgba(255, 255, 255, 0.8);
    }

    .stCheckbox span {
        color: #000000 !important;
    }

    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    </style>
""", unsafe_allow_html=True)

MODEL_PATH = "models/cardiac_failure_detection.pkl"
THRESHOLD = 0.30

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
        st.error(f"🚨 Model file '{MODEL_PATH}' not found. Please ensure the model is in the correct directory.")
        return None


def predict_risk(inputs: dict, model):
    X = pd.DataFrame([inputs], columns=FEATURES)
    X['age'] = X['age'] / 100.0
    X['gender'] = X['gender'] - 1
    X['cholesterol'] = (X['cholesterol'] - 1) / 2.0
    X['bmi'] = X['weight'] / ((X['height'] * 0.01) ** 2)
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
        mode="gauge+number",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Probability", 'font': {'size': 20, 'color': '#1e293b', 'family': 'Inter'}},
        number={'suffix': "%", 'font': {'size': 56, 'color': '#667eea', 'family': 'Inter'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#94a3b8"},
            'bar': {'color': "#667eea", 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, 20], 'color': '#d4edda'},
                {'range': [20, 35], 'color': '#d1ecf1'},
                {'range': [35, 50], 'color': '#fff3cd'},
                {'range': [50, 70], 'color': '#f8d7da'},
                {'range': [70, 100], 'color': '#f5c6cb'}
            ],
            'threshold': {
                'line': {'color': "#dc2626", 'width': 5},
                'thickness': 0.8,
                'value': THRESHOLD * 100
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#1e293b", 'family': "Inter"},
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig


def main():
    # Header
    st.markdown('<div class="main-header">❤️ Cardiac Risk Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Cardiovascular Health Screening Platform</div>',
                unsafe_allow_html=True)

    model = load_model()
    if model is None:
        st.stop()

    # Initialize session state
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    # Input Form
    with st.form("patient_form"):
        st.markdown('<p class="section-header">📋 Patient Information</p>', unsafe_allow_html=True)

        # Demographics Section
        st.markdown("#### 👤 Demographics")
        demo_col1, demo_col2, demo_col3, demo_col4 = st.columns(4)

        with demo_col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=55, step=1, help="Patient's age in years")
        with demo_col2:
            gender = st.selectbox("Gender", options=[1, 2], format_func=lambda x: "Female" if x == 1 else "Male")
        with demo_col3:
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=165, step=1)
        with demo_col4:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=65.0, step=0.5)

        st.markdown("<br>", unsafe_allow_html=True)

        # Vital Signs Section
        st.markdown("#### 🩺 Vital Signs")
        vital_col1, vital_col2 = st.columns(2)

        with vital_col1:
            ap_hi = st.number_input("Systolic BP", min_value=80, max_value=250, value=120, step=1,
                                    help="Upper blood pressure reading (mmHg)")
        with vital_col2:
            ap_lo = st.number_input("Diastolic BP", min_value=40, max_value=150, value=80, step=1,
                                    help="Lower blood pressure reading (mmHg)")

        st.markdown("<br>", unsafe_allow_html=True)

        # Lab Results Section
        st.markdown("#### 🧪 Laboratory Results")
        lab_col1, lab_col2 = st.columns(2)

        with lab_col1:
            cholesterol = st.selectbox(
                "Cholesterol Level",
                options=[1, 2, 3],
                format_func=lambda x: {1: "✅ Normal", 2: "⚠️ Above Normal", 3: "🔴 Well Above Normal"}[x]
            )
        with lab_col2:
            gluc = st.selectbox(
                "Glucose Level",
                options=[1, 2, 3],
                format_func=lambda x: {1: "✅ Normal", 2: "⚠️ Above Normal", 3: "🔴 Well Above Normal"}[x]
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Lifestyle Factors Section
        st.markdown("#### 🏃 Lifestyle Factors")

        # Add specific styling for checkboxes
        st.markdown("""
            <style>
            div[data-testid="stForm"] .stCheckbox label span {
                color: #000000 !important;
                font-weight: 600 !important;
            }
            div[data-testid="stForm"] .stCheckbox label {
                color: #000000 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        lifestyle_col1, lifestyle_col2, lifestyle_col3 = st.columns(3)

        with lifestyle_col1:
            smoke = st.checkbox("🚬 Current Smoker")
            st.markdown('<style>.stCheckbox:nth-of-type(1) label p {color: #000000 !important;}</style>',
                        unsafe_allow_html=True)
        with lifestyle_col2:
            alco = st.checkbox("🍷 Alcohol Consumer")
            st.markdown('<style>.stCheckbox:nth-of-type(2) label p {color: #000000 !important;}</style>',
                        unsafe_allow_html=True)
        with lifestyle_col3:
            active = st.checkbox("💪 Physically Active", value=True)
            st.markdown('<style>.stCheckbox:nth-of-type(3) label p {color: #000000 !important;}</style>',
                        unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button("🔍 Assess Cardiac Risk", type="primary", use_container_width=True)

    # Process form submission
    if submit_button:
        st.session_state.form_submitted = True

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
        with st.spinner("🔄 Analyzing patient data..."):
            result = predict_risk(inputs, model)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-header">📊 Assessment Results</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Display results in columns
        result_col1, result_col2 = st.columns([1, 1], gap="large")

        with result_col1:
            st.markdown("### 📈 Risk Visualization")
            fig = create_gauge_chart(result['probability'])
            st.plotly_chart(fig, use_container_width=True)

        with result_col2:
            st.markdown("### 🎯 Risk Analysis")

            # Risk probability
            prob_percentage = result['probability'] * 100
            st.markdown(f"**Calculated Risk Probability:** `{prob_percentage:.2f}%`")

            st.markdown("<br>", unsafe_allow_html=True)

            # Risk zone with color coding
            risk_class_map = {
                "Very Low Risk": "very-low",
                "Low Risk": "low",
                "Moderate Risk": "moderate",
                "High Risk": "high",
                "Very High Risk": "very-high"
            }
            risk_class = risk_class_map.get(result['risk_zone'], 'moderate')

            # Icon mapping
            risk_icons = {
                "Very Low Risk": "🟢",
                "Low Risk": "🔵",
                "Moderate Risk": "🟡",
                "High Risk": "🟠",
                "Very High Risk": "🔴"
            }
            risk_icon = risk_icons.get(result['risk_zone'], '⚪')

            st.markdown(f'<div class="risk-box {risk_class}">{risk_icon} {result["risk_zone"]}</div>',
                        unsafe_allow_html=True)

            # Screening recommendation
            if result['screening_prediction'] == 1:
                st.error(
                    "**⚠️ POSITIVE SCREENING**\n\n"
                    "**Recommendation:** Further cardiac evaluation is advised. "
                    "Please consult with a cardiologist for comprehensive assessment."
                )
            else:
                st.success(
                    "**✅ NEGATIVE SCREENING**\n\n"
                    "**Recommendation:** Patient appears to be at lower risk. "
                    "Continue regular health monitoring and maintain healthy lifestyle habits."
                )

        # BMI Section
        bmi = weight / ((height / 100) ** 2)

        st.markdown("<br>", unsafe_allow_html=True)

        # BMI Interpretation
        bmi_col1, bmi_col2, bmi_col3, bmi_col4 = st.columns(4)

        with bmi_col1:
            st.metric("📏 Body Mass Index", f"{bmi:.1f}")
        with bmi_col2:
            if bmi < 18.5:
                bmi_category = "Underweight"
                bmi_color = "🔵"
            elif 18.5 <= bmi < 25:
                bmi_category = "Normal"
                bmi_color = "🟢"
            elif 25 <= bmi < 30:
                bmi_category = "Overweight"
                bmi_color = "🟡"
            else:
                bmi_category = "Obese"
                bmi_color = "🔴"
            st.metric("Category", f"{bmi_color} {bmi_category}")
        with bmi_col3:
            st.metric("Blood Pressure", f"{ap_hi}/{ap_lo} mmHg")
        with bmi_col4:
            st.metric("Risk Threshold", f"{THRESHOLD * 100:.0f}%")

        # Patient Summary
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-header">📋 Complete Patient Summary</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:
            st.markdown("##### 👤 Demographics")
            st.metric("Age", f"{age} years")
            st.metric("Gender", "Female" if gender == 1 else "Male")
            st.metric("Height", f"{height} cm")
            st.metric("Weight", f"{weight} kg")

        with summary_col2:
            st.markdown("##### 🔬 Clinical Measurements")
            st.metric("Systolic BP", f"{ap_hi} mmHg")
            st.metric("Diastolic BP", f"{ap_lo} mmHg")
            st.metric("Cholesterol", {1: "Normal", 2: "Above Normal", 3: "Well Above Normal"}[cholesterol])
            st.metric("Glucose", {1: "Normal", 2: "Above Normal", 3: "Well Above Normal"}[gluc])

        with summary_col3:
            st.markdown("##### 🏃 Lifestyle Profile")
            st.metric("Smoking Status", "🚬 Yes" if smoke else "✅ No")
            st.metric("Alcohol Use", "🍷 Yes" if alco else "✅ No")
            st.metric("Physical Activity", "💪 Active" if active else "⚠️ Inactive")
            st.metric("BMI Status", f"{bmi_color} {bmi_category}")

    elif not st.session_state.form_submitted:
        # Welcome screen
        st.markdown("<br>", unsafe_allow_html=True)

        st.info(
            "👋 **Welcome!** Please fill in the patient information above and click 'Assess Cardiac Risk' to begin the evaluation.")

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Purpose")
            st.write(
                "Provides preliminary cardiac risk assessment based on patient vitals, "
                "laboratory results, and lifestyle factors using advanced AI algorithms."
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("### 🤖 How It Works")
            st.write(
                "Utilizes machine learning models trained on extensive cardiovascular health "
                "datasets to identify potential risk factors and provide accurate risk stratification."
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("### ⚠️ Disclaimer")
            st.write(
                "This is a screening tool only and does not replace professional medical advice. "
                "Always consult healthcare professionals for diagnosis and treatment."
            )
            st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="footer">'
        '<p><b>⚕️ Medical Disclaimer</b></p>'
        '<p>This application is designed for screening and educational purposes only. '
        'It does not replace professional medical advice, diagnosis, or treatment. '
        'Always seek the advice of your physician or other qualified health provider with any questions regarding a medical condition.</p>'
        '<p style="margin-top: 1rem; color: #94a3b8; font-size: 0.85rem;"></p>'
        '</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()