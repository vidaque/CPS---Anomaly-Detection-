import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="CPS Security Operations Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# GLOBAL CSS (SOC STYLE)
# ======================================================
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #e5e7eb;
}

h1, h2, h3 {
    color: #f9fafb;
    font-weight: 600;
}

.small-label {
    color: #9ca3af;
    font-size: 12px;
}

.card {
    background-color: #111827;
    padding: 18px;
    border-radius: 8px;
    margin-bottom: 12px;
    border: 1px solid #1f2937;
}

.kpi-value {
    font-size: 28px;
    font-weight: 700;
}

.kpi-label {
    font-size: 12px;
    color: #9ca3af;
}

.alert-critical {
    background: linear-gradient(90deg, #7f1d1d, #dc2626);
    padding: 16px;
    border-radius: 6px;
    font-size: 18px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 15px;
}

.alert-warning {
    background: linear-gradient(90deg, #78350f, #f59e0b);
    padding: 16px;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    text-align: center;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# FILE PATHS
# ======================================================
DATA_FILE = "../data/live/can_stream.csv"
STATE_FILE = "../ml/state.txt"
SEVERITY_FILE = "../ml/severity.txt"
SCORE_FILE = "../ml/anomaly_score.txt"
EVENT_LOG = "../ml/events.log"

# ======================================================
# HELPERS
# ======================================================
def read_file(path, default="N/A"):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return f.read().strip()

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["timestamp","speed","brake","steering"])
    return pd.read_csv(DATA_FILE)

# ======================================================
# SIDEBAR (SOC NAVIGATION)
# ======================================================
st.sidebar.markdown("## 🚗 CPS SOC")
st.sidebar.markdown("**Environment**: Simulation")
st.sidebar.markdown("**CAN Interface**: vcan0")
st.sidebar.markdown("**Detection Engine**: Isolation Forest")
st.sidebar.markdown("---")
st.sidebar.markdown("### Attack Scenarios")
st.sidebar.markdown("- Sensor Spoofing")
st.sidebar.markdown("- Replay Attack")
st.sidebar.markdown("- Timing / Delay Attack")
st.sidebar.markdown("---")
st.sidebar.markdown("### Project Phase")
st.sidebar.markdown("Detection & Monitoring")

# ======================================================
# LOAD STATE
# ======================================================
df = load_data()
state = read_file(STATE_FILE, "NORMAL")
severity = read_file(SEVERITY_FILE, "NONE")
score = read_file(SCORE_FILE, "0.0")

# ======================================================
# HEADER
# ======================================================
st.markdown("# Cyber-Physical Security Operations Center")
st.markdown("### ML-Based Anomaly Detection for Smart Vehicle CPS")

# ======================================================
# ALERTS
# ======================================================
if state == "ATTACK":
    st.markdown(f"""
    <div class="alert-critical">
    🚨 ACTIVE CPS SECURITY INCIDENT — SEVERITY: {severity}
    </div>
    """, unsafe_allow_html=True)
elif state == "RECOVERY":
    st.markdown("""
    <div class="alert-warning">
    ⚠ CPS RECOVERY MODE — MONITORING STABILITY
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# KPI ROW
# ======================================================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-label">CPS STATE</div>
        <div class="kpi-value">{state}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-label">SEVERITY</div>
        <div class="kpi-value">{severity}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-label">ANOMALY SCORE</div>
        <div class="kpi-value">{score}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-label">LAST UPDATE</div>
        <div class="kpi-value">{datetime.now().strftime('%H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# MAIN GRID
# ======================================================
left, right = st.columns([3, 2])

# ---------------- TELEMETRY ----------------
with left:
    st.markdown("## 📊 Vehicle Telemetry")

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.tail(120)

        st.line_chart(
            df.set_index("timestamp")[["speed", "steering"]],
            height=280
        )
    else:
        st.info("Awaiting live CPS telemetry...")

# ---------------- ML INTELLIGENCE ----------------
with right:
    st.markdown("## 🧠 Detection Intelligence")
    st.markdown(f"""
    <div class="card">
        <b>Model:</b> Isolation Forest<br><br>
        <b>Status:</b> {state}<br>
        <b>Severity:</b> {severity}<br>
        <b>Anomaly Score:</b> {score}<br><br>
        <b>Updated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# INCIDENT TIMELINE
# ======================================================
st.markdown("## 🧾 Security Event Timeline")

if os.path.exists(EVENT_LOG):
    events = pd.read_csv(EVENT_LOG, header=None, names=["time","event","description"])
    events["time"] = pd.to_datetime(events["time"], unit="s")
    st.dataframe(events.tail(12), use_container_width=True)
else:
    st.info("No security events recorded.")

# ======================================================
# EXPORT
# ======================================================
st.markdown("## 📤 Export Incident Report")

if os.path.exists(EVENT_LOG):
    st.download_button(
        "Download Incident Report (CSV)",
        events.to_csv(index=False),
        "cps_incident_report.csv",
        "text/csv"
    )
