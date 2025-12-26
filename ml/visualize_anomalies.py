import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv("data/processed/features.csv")

X = df.drop(columns=["label"])
y = df["label"]

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Isolation Forest
iso = IsolationForest(contamination=0.3, random_state=42)
iso.fit(X_scaled)

scores = -iso.decision_function(X_scaled)

# Plot
plt.figure()
plt.plot(scores, label="Anomaly Score")
plt.scatter(
    np.where(y == 1),
    scores[y == 1],
    label="Actual Attacks",
    marker="x"
)
plt.xlabel("Time Window Index")
plt.ylabel("Anomaly Score")
plt.title("CPS Anomaly Score Over Time")
plt.legend()
plt.show()
