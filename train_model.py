import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb
from sklearn.metrics import accuracy_score
import joblib

DATA_PATH = os.path.join("data", "loan_data.csv")
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "best_loan_model.pkl")

CATEGORICAL_COLUMNS = [
    "Gender",
    "Married",
    "Education",
    "Self_Employed",
    "Credit_History",
    "Property_Area",
]
NUMERIC_COLUMNS = [
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
]
TARGET_COLUMN = "Loan_Status"

SAMPLE_DATA = [
    {
        "Gender": "Male",
        "Married": "Yes",
        "Education": "Graduate",
        "Self_Employed": "No",
        "ApplicantIncome": 5849,
        "CoapplicantIncome": 0.0,
        "LoanAmount": 128.0,
        "Loan_Amount_Term": 360.0,
        "Credit_History": 1,
        "Property_Area": "Urban",
        "Loan_Status": "Y",
    },
    {
        "Gender": "Male",
        "Married": "Yes",
        "Education": "Graduate",
        "Self_Employed": "No",
        "ApplicantIncome": 4583,
        "CoapplicantIncome": 1508.0,
        "LoanAmount": 128.0,
        "Loan_Amount_Term": 360.0,
        "Credit_History": 1,
        "Property_Area": "Rural",
        "Loan_Status": "N",
    },
    {
        "Gender": "Male",
        "Married": "Yes",
        "Education": "Not Graduate",
        "Self_Employed": "Yes",
        "ApplicantIncome": 3000,
        "CoapplicantIncome": 0.0,
        "LoanAmount": 66.0,
        "Loan_Amount_Term": 360.0,
        "Credit_History": 1,
        "Property_Area": "Urban",
        "Loan_Status": "Y",
    },
    {
        "Gender": "Female",
        "Married": "No",
        "Education": "Graduate",
        "Self_Employed": "No",
        "ApplicantIncome": 6000,
        "CoapplicantIncome": 0.0,
        "LoanAmount": 141.0,
        "Loan_Amount_Term": 360.0,
        "Credit_History": 1,
        "Property_Area": "Urban",
        "Loan_Status": "Y",
    },
    {
        "Gender": "Male",
        "Married": "No",
        "Education": "Graduate",
        "Self_Employed": "Yes",
        "ApplicantIncome": 5417,
        "CoapplicantIncome": 4196.0,
        "LoanAmount": 267.0,
        "Loan_Amount_Term": 360.0,
        "Credit_History": 1,
        "Property_Area": "Urban",
        "Loan_Status": "Y",
    },
    {
        "Gender": "Male",
        "Married": "Yes",
        "Education": "Not Graduate",
        "Self_Employed": "No",
        "ApplicantIncome": 2333,
        "CoapplicantIncome": 1516.0,
        "LoanAmount": 95.0,
        "Loan_Amount_Term": 360.0,
        "Credit_History": 1,
        "Property_Area": "Rural",
        "Loan_Status": "N",
    },
    {
        "Gender": "Female",
        "Married": "Yes",
        "Education": "Graduate",
        "Self_Employed": "No",
        "ApplicantIncome": 3036,
        "CoapplicantIncome": 2504.0,
        "LoanAmount": 158.0,
        "Loan_Amount_Term": 360.0,
        "Credit_History": 1,
        "Property_Area": "Urban",
        "Loan_Status": "Y",
    },
    {
        "Gender": "Male",
        "Married": "No",
        "Education": "Graduate",
        "Self_Employed": "No",
        "ApplicantIncome": 4006,
        "CoapplicantIncome": 1526.0,
        "LoanAmount": 168.0,
        "Loan_Amount_Term": 360.0,
        "Credit_History": 1,
        "Property_Area": "Urban",
        "Loan_Status": "N",
    },
    {
        "Gender": "Male",
        "Married": "No",
        "Education": "Not Graduate",
        "Self_Employed": "No",
        "ApplicantIncome": 12841,
        "CoapplicantIncome": 10968.0,
        "LoanAmount": 350.0,
        "Loan_Amount_Term": 360.0,
        "Credit_History": 1,
        "Property_Area": "Urban",
        "Loan_Status": "Y",
    },
    {
        "Gender": "Female",
        "Married": "Yes",
        "Education": "Not Graduate",
        "Self_Employed": "No",
        "ApplicantIncome": 3200,
        "CoapplicantIncome": 0.0,
        "LoanAmount": 200.0,
        "Loan_Amount_Term": 360.0,
        "Credit_History": 0,
        "Property_Area": "Semiurban",
        "Loan_Status": "N",
    },
]


def load_data():
    if os.path.exists(DATA_PATH):
        print(f"Loading dataset from {DATA_PATH}")
        return pd.read_csv(DATA_PATH)

    print("Dataset not found. Using sample loan data for training.")
    return pd.DataFrame(SAMPLE_DATA)


def preprocess_features(df):
    df = df.copy()
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Dataset must include the target column '{TARGET_COLUMN}'.")

    df[TARGET_COLUMN] = df[TARGET_COLUMN].map({"Y": 1, "N": 0, 1: 1, 0: 0})
    df = df.dropna(subset=CATEGORICAL_COLUMNS + NUMERIC_COLUMNS + [TARGET_COLUMN])

    X = df[CATEGORICAL_COLUMNS + NUMERIC_COLUMNS]
    y = df[TARGET_COLUMN].astype(int)
    return X, y


def build_pipeline(classifier):
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_COLUMNS),
            ("cat", categorical_transformer, CATEGORICAL_COLUMNS),
        ],
        remainder="drop",
        sparse_threshold=0,
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("classifier", classifier)])


def train_and_select_best_model(X_train, X_test, y_train, y_test):
    models = {
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42, n_estimators=100),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "XGBoost": xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42, n_estimators=100),
    }

    best_pipeline = None
    best_score = 0.0
    best_name = None

    for name, classifier in models.items():
        pipeline = build_pipeline(classifier)
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        score = accuracy_score(y_test, predictions)
        print(f"{name} accuracy: {score * 100:.1f}%")

        if score > best_score:
            best_score = score
            best_pipeline = pipeline
            best_name = name

    if best_pipeline is None:
        raise RuntimeError("Failed to train any model.")

    print(f"Best model: {best_name} with accuracy {best_score * 100:.1f}%")
    return best_pipeline


def save_model(model):
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved best model to {MODEL_PATH}")


def main():
    df = load_data()
    X, y = preprocess_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    best_model = train_and_select_best_model(X_train, X_test, y_train, y_test)
    save_model(best_model)


if __name__ == "__main__":
    main()
