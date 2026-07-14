import os
from flask import Flask, render_template, request
import joblib

app = Flask(__name__)
MODEL_PATH = os.path.join("models", "best_loan_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Model file not found. Run 'python train_model.py' first.")

model = joblib.load(MODEL_PATH)
FEATURES = [
    "Gender",
    "Married",
    "Education",
    "Self_Employed",
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
    "Property_Area",
]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    form = request.form
    try:
        values = [
            form.get("gender", "Male"),
            form.get("married", "Yes"),
            form.get("education", "Graduate"),
            form.get("self_employed", "No"),
            float(form.get("applicant_income", "0") or 0),
            float(form.get("coapplicant_income", "0") or 0),
            float(form.get("loan_amount", "0") or 0),
            float(form.get("loan_amount_term", "360") or 0),
            int(form.get("credit_history", "1") or 0),
            form.get("property_area", "Urban"),
        ]
    except ValueError:
        return render_template(
            "result.html",
            decision="Invalid input",
            confidence="N/A",
            error_message="Please enter valid numeric values for income, loan amount, and loan term.",
        )

    input_data = [values]
    prediction = model.predict(input_data)[0]
    probability = None
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(input_data)[0].max()

    decision = "Loan Approved" if prediction == 1 else "Loan Rejected"
    confidence = f"{probability * 100:.1f}%" if probability is not None else "N/A"

    return render_template(
        "result.html",
        decision=decision,
        confidence=confidence,
        input_data=dict(zip(FEATURES, values)),
        error_message=None,
    )


if __name__ == "__main__":
    app.run(debug=True)
