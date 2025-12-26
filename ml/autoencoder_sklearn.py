import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

# Load data
df = pd.read_csv("data/processed/features.csv")

X = df.drop(columns=["label"])
y = df["label"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train only on NORMAL data
X_train = X_scaled[y == 0]

# Autoencoder using MLP
autoencoder = MLPRegressor(
    hidden_layer_sizes=(8, 4, 8),
    activation="relu",
    max_iter=500,
    random_state=42
)

autoencoder.fit(X_train, X_train)

# Reconstruction
reconstructed = autoencoder.predict(X_scaled)
mse = np.mean((X_scaled - reconstructed) ** 2, axis=1)

# Threshold
threshold = np.percentile(mse[y == 0], 95)

# Predictions
y_pred = (mse > threshold).astype(int)

print("\n[Autoencoder (MLP) Results]")
print(classification_report(y, y_pred))
