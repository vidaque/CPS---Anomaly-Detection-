import streamlit as st
import pandas as pd
import time
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CPS Security Monitoring Platform",
    page_icon="🚗",
    layout="wide"
)

# ---------------- CONSTANTS ----------------
DATA_FILE = "../data/live/can_stream.csv"
STATE_FILE = "../ml/state.txt"
SCORE_FILE = "../ml/anomaly_score.txt"
SEVERITY_FILE = "../ml/severity.txt"
EVENT_LOG = "../ml/events.log"

# ---------------- HELPERS ----------------
def load_live_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["timestamp", "speed", "brake", "steering"])
    return pd.read_csv(DATA_FILE)

def get_health(timeout=10):
    if not os.path.exists(DATA_FILE):
        return "INACTIVE"
    return "ACTIVE" if time.time() - os.path.getmtime(DATA_FILE) <= timeout else "INACTIVE"

def read_file(path, default="N/A"):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return f.read().strip()

# ---------------- HEADER ----------------
st.markdown("# 🚗 Cyber-Physical Security Monitoring Platform")
st.markdown("### ML-Based Anomaly Detection for Smart Vehicle CPS")
st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Platform Info")
st.sidebar.write("Mode: Simulation")
st.sidebar.write("CAN: vcan0")
st.sidebar.write("Model: Isolation Forest")
st.sidebar.write("Attacks: Replay / Timing / Spoofing")

# ---------------- READ STATES ----------------
df = load_live_data()
health = get_health()
cps_state = read_file(STATE_FILE, "NORMAL")
severity = read_file(SEVERITY_FILE, "NONE")
score = read_file(SCORE_FILE, "N/A")

# ---------------- KPI METRICS ----------------
st.markdown("## 📊 System Overview")
k1, k2, k3, k4 = st.columns(4)
k1.metric("CPS State", cps_state)
k2.metric("System Health", health)
k3.metric("Severity", severity)
k4.metric("Anomaly Score", score)

# ---------------- ALERT BANNER ----------------
if cps_state == "ATTACK":
    st.error(f"🚨 SECURITY ALERT: CPS UNDER ATTACK (Severity: {severity})")
elif cps_state == "RECOVERY":
    st.warning("⚠️ CPS IN RECOVERY MODE")

# ---------------- MAIN GRID ----------------
left, right = st.columns([2, 1])

with left:
    st.markdown("## 📡 Live Vehicle Telemetry")
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.tail(100)

        c1, c2, c3 = st.columns(3)
        c1.line_chart(df.set_index("timestamp")["speed"])
        c2.line_chart(df.set_index("timestamp")["steering"])
        c3.line_chart(df.set_index("timestamp")["brake"])
    else:
        st.info("Waiting for CPS data...")

with right:
    st.markdown("## 🧠 ML Intelligence")
    st.markdown(f"""
    - **State:** {cps_state}
    - **Severity:** {severity}
    - **Score:** {score}
    """)

# ---------------- EVENT TIMELINE ----------------
st.markdown("## 🧾 Security Event Timeline")

if os.path.exists(EVENT_LOG):
    events = pd.read_csv(EVENT_LOG, header=None, names=["time", "event", "description"])
    events["time"] = pd.to_datetime(events["time"], unit="s")
    st.dataframe(events.tail(10))
else:
    st.info("No security events yet.")

# ---------------- EXPORT ----------------
st.markdown("## 📤 Export Report")

if os.path.exists(EVENT_LOG):
    csv = events.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Security Report (CSV)",
        csv,
        "cps_security_report.csv",
        "text/csv"
    )
