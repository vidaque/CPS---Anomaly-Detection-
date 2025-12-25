import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load feature dataset
df = pd.read_csv("data/processed/features.csv")

# Separate features and labels
X = df.drop(columns=["label"])
y = df["label"]

# Feature scaling (VERY IMPORTANT)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data (train mostly on normal data)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42
)

# Isolation Forest model
model = IsolationForest(
    n_estimators=100,
    contamination=0.3,   # expected anomaly ratio
    random_state=42
)

# Train model
model.fit(X_train)

# Predict anomalies
y_pred = model.predict(X_test)

# Convert predictions: -1 → anomaly (1), 1 → normal (0)
y_pred = [1 if p == -1 else 0 for p in y_pred]

# Evaluation
print("\n[PHASE 5] Confusion Matrix")
print(confusion_matrix(y_test, y_pred))

print("\n[PHASE 5] Classification Report")
print(classification_report(y_test, y_pred))
