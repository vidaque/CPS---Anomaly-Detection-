import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import classification_report

# Load data
df = pd.read_csv("data/processed/features.csv")
X = df.drop(columns=["label"])
y = df["label"]

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------- Isolation Forest ----------
iso = IsolationForest(contamination=0.3, random_state=42)
iso.fit(X_scaled)
iso_pred = np.where(iso.predict(X_scaled) == -1, 1, 0)

# ---------- Autoencoder (MLP) ----------
X_train = X_scaled[y == 0]
autoencoder = MLPRegressor(
    hidden_layer_sizes=(8, 4, 8),
    max_iter=500,
    random_state=42
)
autoencoder.fit(X_train, X_train)

recon = autoencoder.predict(X_scaled)
mse = np.mean((X_scaled - recon) ** 2, axis=1)
threshold = np.percentile(mse[y == 0], 95)
ae_pred = (mse > threshold).astype(int)

# ---------- Ensemble ----------
ensemble_pred = np.logical_or(iso_pred, ae_pred).astype(int)

print("\n[ENSEMBLE RESULTS]")
print(classification_report(y, ensemble_pred))
