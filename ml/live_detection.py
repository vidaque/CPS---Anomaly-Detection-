import os
import time
import pandas as pd
from sklearn.ensemble import IsolationForest

# =====================================================
# PATHS
# =====================================================
DATA_FILE = "data/live/can_stream.csv"
STATE_FILE = "ml/state.txt"
SCORE_FILE = "ml/anomaly_score.txt"
SEVERITY_FILE = "ml/severity.txt"
EVENT_LOG = "ml/events.log"
HEARTBEAT_FILE = "ml/heartbeat.txt"

# =====================================================
# PARAMETERS (TUNED FOR STRONGER DETECTION)
# =====================================================
BASELINE_SAMPLES = 200
CHECK_INTERVAL = 1

CONTAMINATION = 0.1
ANOMALY_THRESHOLD = -0.05
PERSISTENCE_LIMIT = 3
WARMUP_SECONDS = 5

# =====================================================
# INIT FILES
# =====================================================
os.makedirs("ml", exist_ok=True)

def safe_write(path, value):
    with open(path, "w") as f:
        f.write(str(value))
def update_heartbeat():
    with open(HEARTBEAT_FILE, "w") as f:
        f.write(str(time.time()))

safe_write(STATE_FILE, "NORMAL")
safe_write(SEVERITY_FILE, "NONE")
safe_write(SCORE_FILE, "0.0")
open(EVENT_LOG, "a").close()

# =====================================================
# HELPERS
# =====================================================
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["timestamp","speed","brake","steering"])

    try:
        df = pd.read_csv(
            DATA_FILE,
            on_bad_lines="skip"
        )

        expected = ["timestamp","speed","brake","steering"]
        if not all(col in df.columns for col in expected):
            return pd.DataFrame(columns=expected)

        return df[expected]

    except Exception:
        return pd.DataFrame(columns=["timestamp","speed","brake","steering"])


def extract_features(df):
    return df[["speed","brake","steering"]].values


def log_event(event, description):
    with open(EVENT_LOG, "a") as f:
        f.write(f"{time.time()},{event},{description}\n")


def get_severity(counter):
    if counter >= 6:
        return "HIGH"
    elif counter >= 4:
        return "MEDIUM"
    elif counter >= 2:
        return "LOW"
    return "NONE"


# =====================================================
# MAIN ENGINE
# =====================================================
def main():
    print("[ML] CPS Anomaly Detection Engine Starting")
    print("[ML] Learning baseline behavior...")

    baseline_samples = []

    while len(baseline_samples) < BASELINE_SAMPLES:
        df = load_data()
        if not df.empty:
            baseline_samples.append(df.iloc[-1])
            print(f"[ML] Baseline samples: {len(baseline_samples)}/{BASELINE_SAMPLES}")
        time.sleep(0.1)

    baseline_df = pd.DataFrame(baseline_samples)
    X_train = extract_features(baseline_df)

    model = IsolationForest(
        n_estimators=100,
        contamination=CONTAMINATION,
        random_state=42
    )

    model.fit(X_train)

    log_event("BASELINE", "Baseline learned")
    print("[ML] Baseline learned successfully")

    print(f"[ML] Warming up for {WARMUP_SECONDS} seconds...")
    time.sleep(WARMUP_SECONDS)

    print("[ML] Live anomaly detection ACTIVE")

    anomaly_counter = 0
    current_state = "NORMAL"

    while True:
        update_heartbeat()
        df = load_data()

        if df.empty:
            time.sleep(1)
            continue

        latest = df.iloc[-1:]
        X = extract_features(latest)

        try:
            score = model.decision_function(X)[0]
        except Exception:
            time.sleep(1)
            continue

        safe_write(SCORE_FILE, round(score, 4))

        if score < ANOMALY_THRESHOLD:
            anomaly_counter += 1
        else:
            anomaly_counter = max(0, anomaly_counter - 1)

        severity = get_severity(anomaly_counter)
        safe_write(SEVERITY_FILE, severity)

        print(f"[ML DEBUG] Score: {round(score,4)} | Counter: {anomaly_counter}")

        # =========================
        # STATE MACHINE
        # =========================
        if anomaly_counter >= PERSISTENCE_LIMIT and current_state != "ATTACK":
            current_state = "ATTACK"
            safe_write(STATE_FILE, "ATTACK")
            log_event("ATTACK", f"Attack detected (Severity: {severity})")
            print("🚨 [ALERT] CPS UNDER ATTACK")

        elif anomaly_counter == 0 and current_state == "ATTACK":
            current_state = "RECOVERY"
            safe_write(STATE_FILE, "RECOVERY")
            log_event("RECOVERY", "System stabilizing")
            print("[ML] Recovery mode")

        elif current_state == "RECOVERY" and anomaly_counter == 0:
            current_state = "NORMAL"
            safe_write(STATE_FILE, "NORMAL")
            log_event("NORMAL", "System back to normal")
            print("[ML] CPS back to NORMAL")

        time.sleep(CHECK_INTERVAL)


# =====================================================
# SAFE EXIT
# =====================================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        safe_write(STATE_FILE, "NORMAL")
        print("\n[ML] Detection stopped safely")
