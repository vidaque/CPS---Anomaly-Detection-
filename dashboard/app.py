import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CPS Security Monitoring Platform",
    page_icon="🚗",
    layout="wide"
)

# ---------------- LOAD CSS ----------------
CSS_FILE = "styles.css"
if os.path.exists(CSS_FILE):
    with open(CSS_FILE) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- CONSTANTS ----------------
DATA_FILE = "../data/live/can_stream.csv"
STATE_FILE = "../ml/state.txt"

# ---------------- DATA LOADER ----------------
def load_live_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["timestamp", "speed", "brake", "steering"])
    return pd.read_csv(DATA_FILE)

# ---------------- SYSTEM HEALTH ----------------
def get_system_health(df, timeout=10):
    health = {
        "simulator": "INACTIVE",
        "receiver": "INACTIVE",
        "ml": "INACTIVE"
    }

    if not os.path.exists(DATA_FILE):
        return health

    # Check file modification time (real activity check)
    file_mtime = os.path.getmtime(DATA_FILE)
    now_ts = time.time()
    file_delta = now_ts - file_mtime

    if file_delta <= timeout:
        health["simulator"] = "ACTIVE"
        health["receiver"] = "ACTIVE"

    return health


# ---------------- CPS STATE ----------------
def get_cps_state():
    if not os.path.exists(STATE_FILE):
        return "NORMAL"

    with open(STATE_FILE) as f:
        state = f.read().strip()

    return state if state else "NORMAL"

# ---------------- HEADER ----------------
st.markdown("# 🚗 Cyber-Physical Security Monitoring Platform")
st.markdown("### ML-Based Anomaly Detection for Smart Vehicle CPS")
st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Platform Info")
st.sidebar.markdown("**System Mode:** Simulation")
st.sidebar.markdown("**CAN Interface:** vcan0")
st.sidebar.markdown("**ML Model:** Isolation Forest")
st.sidebar.markdown("**Attacks Implemented:**")
st.sidebar.write("- Replay Attack")
st.sidebar.write("- Timing / Delay Attack")
st.sidebar.write("- Sensor Spoofing")
st.sidebar.markdown("---")
st.sidebar.markdown("**Phase:** Phase-1 Monitoring")

# ---------------- LOAD DATA ----------------
df_live = load_live_data()
health = get_system_health(df_live)
cps_state = get_cps_state()

# ---------------- KPI METRICS ----------------
st.markdown("## 📊 System Overview")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("CPS State", cps_state)

with k2:
    st.metric("Simulator", health["simulator"])

with k3:
    st.metric("Receiver", health["receiver"])

with k4:
    st.metric("ML Engine", "ACTIVE")

# ---------------- SYSTEM HEALTH PANEL ----------------
st.markdown("## 🧩 System Health Overview")
st.markdown(f"""
<div class="section">
<b>Simulator:</b> {health['simulator']}<br>
<b>Receiver:</b> {health['receiver']}<br>
<b>ML Engine:</b> ACTIVE<br>
<b>CAN Interface:</b> vcan0
</div>
""", unsafe_allow_html=True)

# ---------------- CPS STATE ----------------
state_class = {
    "NORMAL": "normal",
    "ATTACK": "attack",
    "RECOVERY": "recovery"
}.get(cps_state, "normal")

st.markdown("## 🚦 CPS Operational State")
st.markdown(f"""
<div class="section">
Current State: <span class="status {state_class}">{cps_state}</span><br>
</div>
""", unsafe_allow_html=True)

# ---------------- LIVE MONITORING ----------------
st.markdown("## 📡 Live CPS Monitoring")
left, right = st.columns([2, 1])

with left:
    st.markdown("### Vehicle Telemetry")
    telemetry_container = st.empty()

with right:
    st.markdown("### ML Intelligence")
    st.markdown("""
    <div class="section">
    <b>Anomaly Score:</b> Monitoring<br>
    <b>Status:</b> Standby<br>
    <b>Confidence:</b> N/A
    </div>
    """, unsafe_allow_html=True)

# ---------------- TELEMETRY LOOP ----------------
while True:
    df = load_live_data()

    with telemetry_container.container():
        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

            df = df.tail(100)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.line_chart(df.set_index("timestamp")["speed"])
            with c2:
                st.line_chart(df.set_index("timestamp")["steering"])
            with c3:
                st.line_chart(df.set_index("timestamp")["brake"])
        else:
            st.info("Waiting for CPS data...")

    time.sleep(1)
