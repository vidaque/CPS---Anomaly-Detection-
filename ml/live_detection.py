import time
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# ---------------- PATHS ----------------
DATA_FILE = "data/live/can_stream.csv"

STATE_FILE = "ml/state.txt"
SCORE_FILE = "ml/anomaly_score.txt"
EVENT_LOG = "ml/events.log"
SEVERITY_FILE = "ml/severity.txt"

# ---------------- PARAMETERS ----------------
BASELINE_SAMPLES = 200
CHECK_INTERVAL = 1
ANOMALY_THRESHOLD = -0.15
PERSISTENCE_LIMIT = 5

# ---------------- INIT ----------------
os.makedirs("ml", exist_ok=True)

with open(STATE_FILE, "w") as f:
    f.write("NORMAL")

with open(SEVERITY_FILE, "w") as f:
    f.write("NONE")

open(EVENT_LOG, "a").close()

# ---------------- HELPERS ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["timestamp", "speed", "brake", "steering"])
    return pd.read_csv(DATA_FILE)

def extract_features(df):
    return df[["speed", "brake", "steering"]].values

def log_event(event, desc):
    with open(EVENT_LOG, "a") as f:
        f.write(f"{time.time()},{event},{desc}\n")

def write_state(state):
    with open(STATE_FILE, "w") as f:
        f.write(state)

def write_score(score):
    with open(SCORE_FILE, "w") as f:
        f.write(str(round(score, 4)))

def get_severity(counter):
    if counter >= 5:
        return "HIGH"
    elif counter >= 3:
        return "MEDIUM"
    elif counter >= 1:
        return "LOW"
    return "NONE"

# ---------------- MAIN ----------------
def main():
    print("[ML] CPS Anomaly Detection Engine Starting")

    # -------- BASELINE LEARNING --------
    baseline = []
    print("[ML] Learning baseline behavior...")

    while len(baseline) < BASELINE_SAMPLES:
        df = load_data()
        if len(df) > 0:
            baseline.append(df.iloc[-1])
            print(f"[ML] Baseline samples: {len(baseline)}/{BASELINE_SAMPLES}")
        time.sleep(0.1)

    baseline_df = pd.DataFrame(baseline)
    X_train = extract_features(baseline_df)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )
    model.fit(X_train)

    log_event("BASELINE", "Baseline learned")
    print("[ML] Baseline learned successfully")

    # -------- LIVE MONITORING --------
    anomaly_counter = 0
    current_state = "NORMAL"

    print("[ML] Live anomaly detection ACTIVE")

    while True:
        df = load_data()
        if len(df) == 0:
            time.sleep(CHECK_INTERVAL)
            continue

        latest = df.iloc[-1:]
        X = extract_features(latest)

        score = model.decision_function(X)[0]
        write_score(score)

        if score < ANOMALY_THRESHOLD:
            anomaly_counter += 1
        else:
            anomaly_counter = max(0, anomaly_counter - 1)

        severity = get_severity(anomaly_counter)
        with open(SEVERITY_FILE, "w") as f:
            f.write(severity)

        # -------- STATE MACHINE --------
        if anomaly_counter >= PERSISTENCE_LIMIT and current_state != "ATTACK":
            current_state = "ATTACK"
            write_state("ATTACK")
            log_event("ATTACK", f"Attack detected (Severity: {severity})")
            print("🚨 [ALERT] CPS UNDER ATTACK")

        elif anomaly_counter == 0 and current_state == "ATTACK":
            current_state = "RECOVERY"
            write_state("RECOVERY")
            log_event("RECOVERY", "System stabilizing")
            print("[ML] Recovery mode")

        elif current_state == "RECOVERY" and anomaly_counter == 0:
            current_state = "NORMAL"
            write_state("NORMAL")
            log_event("NORMAL", "System normal")
            print("[ML] CPS back to NORMAL")

        time.sleep(CHECK_INTERVAL)

# ---------------- SAFE EXIT ----------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        write_state("NORMAL")
        print("\n[ML] Detection stopped safely")
