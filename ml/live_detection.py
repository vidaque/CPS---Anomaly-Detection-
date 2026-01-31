import time
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime

# ---------------- PATHS ----------------
DATA_FILE = "data/live/can_stream.csv"

STATE_FILE = "ml/state.txt"
SCORE_FILE = "ml/anomaly_score.txt"
EVENT_LOG = "ml/events.log"

# ---------------- PARAMETERS ----------------
BASELINE_SAMPLES = 200          # number of samples to learn normal behavior
CHECK_INTERVAL = 1              # seconds
ANOMALY_THRESHOLD = -0.15       # isolation forest score threshold
PERSISTENCE_LIMIT = 5           # how many consecutive anomalies = ATTACK

# ---------------- INIT FILES ----------------
os.makedirs("ml", exist_ok=True)

with open(STATE_FILE, "w") as f:
    f.write("NORMAL")

open(EVENT_LOG, "a").close()

# ---------------- HELPERS ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["timestamp", "speed", "brake", "steering"])
    return pd.read_csv(DATA_FILE)

def extract_features(df):
    return df[["speed", "brake", "steering"]].values

def log_event(event, description):
    with open(EVENT_LOG, "a") as f:
        f.write(f"{time.time()},{event},{description}\n")

def write_state(state):
    with open(STATE_FILE, "w") as f:
        f.write(state)

def write_score(score):
    with open(SCORE_FILE, "w") as f:
        f.write(str(round(score, 4)))

# ---------------- MAIN ----------------
def main():
    print("[ML] CPS Anomaly Detection Engine Starting...")

    # -------- BASELINE LEARNING --------
    baseline_data = []

    print("[ML] Learning baseline behavior...")
    while len(baseline_data) < BASELINE_SAMPLES:
        df = load_data()
        if len(df) > 0:
            baseline_data.append(df.iloc[-1])
            print(f"[ML] Baseline samples: {len(baseline_data)}/{BASELINE_SAMPLES}")
        time.sleep(0.1)

    baseline_df = pd.DataFrame(baseline_data)
    X_train = extract_features(baseline_df)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )
    model.fit(X_train)

    print("[ML] Baseline learned successfully")
    log_event("BASELINE", "Baseline behavior learned")

    # -------- LIVE MONITORING --------
    anomaly_counter = 0
    current_state = "NORMAL"

    print("[ML] Live anomaly detection ACTIVATED")

    while True:
        df = load_data()
        if len(df) == 0:
            time.sleep(CHECK_INTERVAL)
            continue

        latest = df.iloc[-1:]
        X = extract_features(latest)

        score = model.decision_function(X)[0]
        write_score(score)

        # -------- ANOMALY LOGIC --------
        if score < ANOMALY_THRESHOLD:
            anomaly_counter += 1
        else:
            anomaly_counter = max(0, anomaly_counter - 1)

        # -------- STATE TRANSITIONS --------
        if anomaly_counter >= PERSISTENCE_LIMIT and current_state != "ATTACK":
            current_state = "ATTACK"
            write_state("ATTACK")
            log_event("ATTACK", "Persistent anomaly detected")
            print("⚠️  [ALERT] CPS ATTACK DETECTED")

        elif anomaly_counter == 0 and current_state == "ATTACK":
            current_state = "RECOVERY"
            write_state("RECOVERY")
            log_event("RECOVERY", "System stabilizing after attack")
            print("[ML] Entering recovery state")

        elif current_state == "RECOVERY" and anomaly_counter == 0:
            current_state = "NORMAL"
            write_state("NORMAL")
            log_event("NORMAL", "System returned to normal")
            print("[ML] CPS back to NORMAL")

        time.sleep(CHECK_INTERVAL)

# ---------------- SAFE SHUTDOWN ----------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[ML] Detection stopped by user")
        write_state("NORMAL")
