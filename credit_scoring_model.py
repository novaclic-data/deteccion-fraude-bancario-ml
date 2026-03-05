# =================================================================
# PROJECT: BANKING CREDIT SCORING - LOAN APPROVAL MODEL (AI)
# GOAL: Predict loan eligibility based on applicant solvency and credit history.
# =================================================================

import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# --- STEP 1: DATA INGESTION AND QUALITY CONTROL ---
# Loading the banking dataset and checking for missing values (nulls)
df = pd.read_csv(r"C:\Users\PC\OneDrive\Documentos\ia_ml\datos\prestamos_banco.csv")
print(f"--- DATASET LOADED: {len(df)} loan applications found ---")

# --- STEP 2: DATA CLEANSING (BANKING STANDARDS) ---
# Handling missing values in financial columns using MEDIAN
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median())
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].median())

# Handling categorical missing values using MODE (Most Frequent Value)
categorical_cols = ['Credit_History', 'Self_Employed', 'Dependents', 'Gender', 'Married']
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

print("✅ Data Cleansing Completed: No null values remaining.")

# --- STEP 3: STRATEGIC BUSINESS ANALYSIS (EDA) ---

# 1. Credit History Impact: The most critical feature for loan approval
credit_impact = pd.crosstab(df['Credit_History'], df['Loan_Status'], normalize='index') * 100
print("\n--- APPROVAL RATE BY CREDIT HISTORY (%) ---")
print(credit_impact)

# 2. Income vs Approval: Average applicant income
avg_income = df.groupby('Loan_Status')['ApplicantIncome'].mean()
print("\n--- AVERAGE APPLICANT INCOME BY LOAN STATUS ---")
print(avg_income)

# --- STEP 4: DATA VISUALIZATION (EXECUTIVE DASHBOARD) ---

# 1. Chart: Loan Approval by Property Area (Property Risk)
area_approval = pd.crosstab(df['Property_Area'], df['Loan_Status'], normalize='index') * 100
area_approval.plot(kind='bar', stacked=True, color=['#e74c3c', '#2ecc71'], figsize=(10, 6))
plt.title('Loan Approval Distribution by Property Area', fontsize=14)
plt.ylabel('Approval Percentage (%)')
plt.legend(title='Approved?', labels=['No (N)', 'Yes (Y)'])
plt.tight_layout()
plt.savefig("01_property_area_approval.png")
plt.close()

# 2. Chart: Feature Importance (What drives the bank's decision?)
# (We define X and y here to generate the importance plot)
features = ['Credit_History', 'Education', 'Married', 'Property_Area', 'LoanAmount', 'ApplicantIncome']
X_plot = pd.get_dummies(df[features], drop_first=True)
y_plot = df['Loan_Status']

# Temporary model for visualization
temp_model = RandomForestClassifier(n_estimators=100, random_state=42)
temp_model.fit(X_plot, y_plot)

importance = pd.Series(temp_model.feature_importances_, index=X_plot.columns)
plt.figure(figsize=(10, 6))
importance.sort_values(ascending=True).plot(kind='barh', color='#2ecc71')
plt.title('Credit Scoring: Top Features Driving Loan Approval', fontsize=14)
plt.xlabel('Importance Level (Weight in Decision)')
plt.tight_layout()
plt.savefig("04_scoring_feature_importance.png")
plt.close()

# --- STEP 5: MACHINE LEARNING PIPELINE (CREDIT SCORING AI) ---
X = X_plot
y = y_plot

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the "Credit Committee" Model
scoring_model = RandomForestClassifier(n_estimators=100, random_state=42)
scoring_model.fit(X_train, y_train)

# --- STEP 6: PERFORMANCE EVALUATION ---
print("\n--- BANKING PERFORMANCE REPORT (SCORING AI) ---")
predictions = scoring_model.predict(X_test)
print(classification_report(y_test, predictions))

# Exporting the trained AI model
joblib.dump(scoring_model, 'credit_scoring_model.pkl')
print("\n✅ SCORING PIPELINE COMPLETED: Model and insights exported successfully.")