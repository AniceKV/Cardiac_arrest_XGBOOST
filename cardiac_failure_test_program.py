import joblib
import pandas as pd

MODEL_PATH = "models/cardiac_failure_detection.pkl"
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
        "age": 30,
        "gender": 1,
        "height": 176,
        "weight": 180.0,
        "ap_hi": 120,
        "ap_lo": 80,
        "cholesterol": 1,
        "gluc": 0,
        "smoke": 0,
        "alco": 0,
        "active": 1
    }

    print("Processing patient data...")
    result = predict_risk(sample_patient)
    print("\n--- Prediction Result ---")
    print(f"Risk Probability: {result['probability'] * 100:.2f}%")
    print(f"Risk Zone:        {result['risk_zone']}")
    print(
        f"Prediction:       {'POSITIVE (Screen for issue)' if result['screening_prediction'] == 1 else 'NEGATIVE (Likely healthy)'}")
