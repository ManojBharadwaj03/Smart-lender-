# Smart Lender - Loan Eligibility Prediction System

Smart Lender is a machine learning-powered loan eligibility prediction app built with Python and Flask. It evaluates applicant information using multiple classifiers and deploys the best model for real-time prediction.

## Features
- Preprocess loan applicant data
- Train Decision Tree, Random Forest, KNN, and XGBoost models
- Select and save the best-performing model
- Provide a Flask web interface for real-time loan eligibility prediction

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows
   # or source venv/bin/activate   # Linux/macOS
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Train the model:
   ```bash
   python train_model.py
   ```
4. Run the Flask app:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## Data
Place a loan dataset at `data/loan_data.csv` with the following columns:
- Gender
- Married
- Education
- Self_Employed
- ApplicantIncome
- CoapplicantIncome
- LoanAmount
- Loan_Amount_Term
- Credit_History
- Property_Area
- Loan_Status

If no dataset is present, the app will use a built-in sample dataset for training.

## Notes
- The project saves the trained model to `models/best_loan_model.pkl`.
- You can replace the sample data with your own loan eligibility dataset and re-run training.
