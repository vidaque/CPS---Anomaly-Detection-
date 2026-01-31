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
def get_system_health(df, timeout=5):
    health = {
        "simulator": "INACTIVE",
        "receiver": "INACTIVE",
        "ml": "INACTIVE"
    }

    if not df.empty:
        last_time = pd.to_datetime(df["timestamp"].iloc[-1])
        now = datetime.utcnow()
        delta = (now - last_time).total_seconds()

        if delta <= timeout:
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

# ---------------- LOAD DATA ----------------
df_live = load_live_data()
health = get_system_health(df_live)
cps_state = get_cps_state()

# ---------------- SYSTEM HEALTH PANEL ----------------
st.markdown("## 🧩 System Health Overview")

st.markdown(f"""
<div class="section">
<b>Simulator:</b>
<span class="status {'normal' if health['simulator']=='ACTIVE' else 'attack'}">
{health['simulator']}
</span><br>

<b>Receiver:</b>
<span class="status {'normal' if health['receiver']=='ACTIVE' else 'attack'}">
{health['receiver']}
</span><br>

<b>ML Engine:</b>
<span class="status normal">Monitoring</span><br>

<b>CAN Interface:</b> vcan0
</div>
""", unsafe_allow_html=True)

# ---------------- CPS STATE PANEL ----------------
state_class = {
    "NORMAL": "normal",
    "ATTACK": "attack",
    "RECOVERY": "recovery"
}.get(cps_state, "normal")

st.markdown("## 🚦 CPS Operational State")

st.markdown(f"""
<div class="section">
Current State:
<span class="status {state_class}">
{cps_state}
</span><br>
Description: CPS operating under {cps_state.lower()} conditions.
</div>
""", unsafe_allow_html=True)

# ---------------- LIVE TELEMETRY ----------------
st.markdown("## 📡 Live CPS Telemetry")
telemetry_container = st.empty()

while True:
    df = load_live_data()

    with telemetry_container.container():
        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.tail(100)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("### 🚗 Speed")
                st.line_chart(df.set_index("timestamp")["speed"])

            with col2:
                st.markdown("### 🔄 Steering")
                st.line_chart(df.set_index("timestamp")["steering"])

            with col3:
                st.markdown("### 🛑 Brake")
                st.line_chart(df.set_index("timestamp")["brake"])
        else:
            st.info("Waiting for CPS data...")

    time.sleep(1)

