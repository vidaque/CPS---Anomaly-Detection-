import time
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

DATA_FILE = "data/live/can_stream.csv"

BASELINE_SAMPLES = 200
WINDOW_SIZE = 25
CHECK_INTERVAL = 2

ANOMALY_RATIO_THRESHOLD = 0.5   # 50% of window anomalous
PERSISTENCE_THRESHOLD = 3       # consecutive windows

print("[ML] CPS Anomaly Detection System Starting...")

scaler = StandardScaler()
model = IsolationForest(
    n_estimators=150,
    contamination=0.1,
    random_state=42
)

model_trained = False
anomaly_counter = 0


def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except Exception:
        return pd.DataFrame()


try:
    while True:
        df = load_data()

        # ---------- BASELINE LEARNING ----------
        if not model_trained:
            if len(df) < BASELINE_SAMPLES:
                print(f"[ML] Learning baseline... ({len(df)}/{BASELINE_SAMPLES})")
                time.sleep(1)
                continue

            baseline = df.iloc[:BASELINE_SAMPLES][
                ["speed", "brake", "steering"]
            ]

            X_train = scaler.fit_transform(baseline)
            model.fit(X_train)

            model_trained = True
            print("[ML] Baseline learned successfully")
            print("[ML] Live anomaly detection ACTIVATED")
            continue

        # ---------- LIVE DETECTION ----------
        if len(df) < BASELINE_SAMPLES + WINDOW_SIZE:
            time.sleep(1)
            continue

        window = df.tail(WINDOW_SIZE)[
            ["speed", "brake", "steering"]
        ]

        X_test = scaler.transform(window)
        preds = model.predict(X_test)

        anomaly_ratio = (preds == -1).sum() / WINDOW_SIZE

        if anomaly_ratio >= ANOMALY_RATIO_THRESHOLD:
            anomaly_counter += 1
            print(
                f"[ML] Suspicious behavior "
                f"(confidence={anomaly_ratio:.2f}, streak={anomaly_counter})"
            )
        else:
            anomaly_counter = 0
            print("[ML] CPS behavior normal")

        if anomaly_counter >= PERSISTENCE_THRESHOLD:
            print("🚨 [ALERT] CONFIRMED CPS CAN ATTACK DETECTED 🚨")
            anomaly_counter = 0  # prevent alert spam

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n[ML] Anomaly detection stopped by user. Exiting cleanly.")

