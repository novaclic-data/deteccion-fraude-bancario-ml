# =================================================================
# PROJECT: BANKING FRAUD DETECTION SYSTEM (ANTI-FRAUD AI)
# GOAL: Maximize ROI by detecting 94% of fraudulent transactions.
# =================================================================

import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# --- STEP 1: DATA INGESTION AND INITIAL DIAGNOSTICS ---
df = pd.read_csv("C:\Users\PC\OneDrive\Documentos\ia_ml\datos\fraude_pagos.csv")
print(f"--- DATASET LOADED: {len(df)} records found ---")

# --- STEP 2: EXPLORATORY DATA ANALYSIS (EDA) ---
# Risk analysis by Payment Method and Device
payment_risk = df.groupby('Payment_Method')['Fraudulent'].mean() * 100
device_risk = df.groupby('Device_Used')['Fraudulent'].mean() * 100

print("\n--- FRAUD RISK BY PAYMENT METHOD (%) ---")
print(payment_risk.sort_values(ascending=False))

# Financial Diagnostics: Average Fraud Amount vs Legal
monto_promedio = df.groupby('Fraudulent')['Transaction_Amount'].mean()
print("\n--- AVERAGE TRANSACTION AMOUNT (0:Legal | 1:Fraud) ---")
print(monto_promedio)

# Account Age Impact
account_impact = df.groupby('Fraudulent')['Account_Age'].mean()
print("\n--- AVERAGE ACCOUNT AGE (LOYALTY VS RISK) ---")
print(account_impact)

# --- STEP 3: DATA VISUALIZATION (STRATEGIC INSIGHTS) ---

# 1. Bar Chart: Risk by Payment Method
plt.figure(figsize=(10, 6))
plt.bar(['UPI', 'Credit Card', 'Net Banking', 'Debit Card'], [5.14, 4.9, 4.9, 4.8], color=['#c0392b', '#2980b9', '#2980b9', '#2980b9'])
plt.axhline(y=1, color='green', linestyle='--', label='Normal Risk Level (<1%)')
plt.title('High Risk Alert: Fraud Frequency by Payment Method', fontsize=14)
plt.ylabel('Risk Percentage (%)')
plt.legend()
plt.tight_layout()
plt.savefig("01_payment_risk_analysis.png")
plt.close()

# 2. Histogram: Fraudulent Amount Distribution
plt.figure(figsize=(10, 6))
plt.hist(df[df['Fraudulent'] == 1]['Transaction_Amount'], bins=30, color='#e74c3c', edgecolor='black', alpha=0.7)
plt.axvline(3118, color='yellow', linestyle='dashed', linewidth=2, label='Average Fraud Amount ($3,118)')
plt.title('Distribution of Fraudulent Transaction Amounts', fontsize=14)
plt.xlabel('Amount ($)')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig("03_fraud_amount_distribution.png")
plt.close()

# --- STEP 4: MACHINE LEARNING PREPARATION (FEATURE ENGINEERING) ---
X = df[['Transaction_Amount', 'Payment_Method', 'Device_Used', 'Account_Age']]
y = df['Fraudulent']

# One-Hot Encoding for categorical variables
X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- STEP 5: MODEL TRAINING (RANDOM FOREST) ---
# Weighting the Fraud class (1) to maximize RECALL
class_weights = {0: 1, 1: 100}

model = RandomForestClassifier(
    n_estimators=100, 
    class_weight=class_weights, 
    max_depth=10, 
    random_state=42,
    n_jobs=-1 
)

model.fit(X_train, y_train)

# --- STEP 6: PERFORMANCE EVALUATION AND EXPORT ---
predictions = model.predict(X_test)
print("\n--- CYBERSECURITY PERFORMANCE REPORT ---")
print(classification_report(y_test, predictions))

# Feature Importance Plot
importancia = pd.Series(model.feature_importances_, index=X.columns)
plt.figure(figsize=(10, 6))
importancia.sort_values(ascending=True).tail(10).plot(kind='barh', color='#f39c12')
plt.title('Key Fraud Indicators (Feature Importance)', fontsize=14)
plt.xlabel('Impact Level')
plt.tight_layout()
plt.savefig("04_fraud_key_features.png")
plt.close()

# Save the trained AI
joblib.dump(model, 'fraud_detection_model.pkl')
print("\n✅ AI PIPELINE COMPLETED: Model and insights successfully exported.")