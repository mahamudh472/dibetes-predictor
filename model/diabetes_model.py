import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
data_path = 'data/diabetes.csv'
data = pd.read_csv(data_path)

# Select all features except the target variable
X = data.drop('Outcome', axis=1)
y = data['Outcome']  # Target (whether or not the person has diabetes)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Data preprocessed successfully.")

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Initialize and train model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -------------------------------------------
# -------------------------------------------
# -------------------------------------------

import joblib

# Save the trained model
joblib.dump(model, 'saved_model/model.pkl')

# Save the scaler
joblib.dump(scaler, 'saved_model/scaler.pkl')

print("Model and scaler saved.")
