import joblib
import pandas as pd

MODEL_PATH = "cardiac_failure_detection.pkl"
model = joblib.load(MODEL_PATH)

THRESHOLD = 0.35

BINS = [0.0, 0.20, 0.35, 0.50, 0.70, 1.0]
LABELS = [
    "Very Low Risk",
    "Low Risk",
    "Moderate Risk",
    "High Risk",
    "Very High Risk"
]

FEATURES = [
    "age",
    "gender",
    "height",
    "weight",
    "ap_hi",
    "ap_lo",
    "cholesterol",
    "gluc",
    "smoke",
    "alco",
    "active"
]


def predict_risk(inputs: dict):
    X = pd.DataFrame([inputs], columns=FEATURES)
    X['age'] = X['age'] / 100.0
    X['gender'] = X['gender'] - 1
    X['cholesterol'] = (X['cholesterol'] - 1) / 2.0
    prob = model.predict_proba(X)[0, 1]
    prediction = int(prob >= THRESHOLD)

    risk_zone = pd.cut(
        [prob],
        bins=BINS,
        labels=LABELS,
        include_lowest=True
    )[0]

    return {
        "probability": round(float(prob), 4),
        "screening_prediction": prediction,
        "risk_zone": str(risk_zone),
        "input_summary": inputs
    }


if __name__ == "__main__":
    sample_patient = {
        "age": 20,  # 55 years old
        "gender": 1,  # 1 = Female
        "height": 165,  # cm
        "weight": 65.0,  # kg
        "ap_hi": 120,  # Systolic BP (Normal)
        "ap_lo": 80,  # Diastolic BP (Normal)
        "cholesterol": 1,  # 1 = Normal
        "gluc": 1,  # 1 = Normal
        "smoke": 0,  # 0 = No
        "alco": 0,  # 0 = No
        "active": 1  # 1 = Yes
    }

    print("Processing patient data...")
    result = predict_risk(sample_patient)
    print("\n--- Prediction Result ---")
    print(f"Risk Probability: {result['probability'] * 100:.2f}%")
    print(f"Risk Zone:        {result['risk_zone']}")
    print(
        f"Prediction:       {'POSITIVE (Screen for issue)' if result['screening_prediction'] == 1 else 'NEGATIVE (Likely healthy)'}")
