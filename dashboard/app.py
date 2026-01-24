import streamlit as st
import pandas as pd
import time
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CPS Security Monitoring Platform",
    page_icon="🚗",
    layout="wide"
)

# ---------- LOAD CSS ----------
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
DATA_FILE = "../data/live/can_stream.csv"

def load_live_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["timestamp", "speed", "brake", "steering"])
    return pd.read_csv(DATA_FILE)

# ---------- HEADER ----------
st.markdown("# 🚗 Cyber-Physical Security Monitoring Platform")
st.markdown("### ML-Based Anomaly Detection for Smart Vehicle CPS")
st.markdown("---")

# ---------- GLOBAL SYSTEM STATUS ----------
st.markdown("## 🧩 System Health Overview")
st.markdown("""
<div class="section">
<b>Simulator:</b> <span class="status normal">Running</span><br>
<b>CAN Interface:</b> vcan0<br>
<b>Receiver:</b> Active<br>
<b>ML Engine:</b> Monitoring
</div>
""", unsafe_allow_html=True)

# ---------- CPS STATE ----------
st.markdown("## 🚦 CPS Operational State")
st.markdown("""
<div class="section">
Current State: <span class="status normal">NORMAL</span><br>
Description: CPS operating within expected parameters.
</div>
""", unsafe_allow_html=True)

# ---------- LIVE TELEMETRY PLACEHOLDER ----------
st.markdown("## 📡 Live CPS Telemetry")

telemetry_section = st.empty()

while True:
    df = load_live_data()

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.tail(100)  # last 100 points only

        with telemetry_section.container():
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
        telemetry_section.info("Waiting for CPS data...")

    time.sleep(1)


# ---------- ATTACK & SECURITY PLACEHOLDER ----------
st.markdown("## 🧨 Security Events & Attacks")
st.markdown("""
<div class="section">
<p>Attack detection events and timelines will appear here.</p>
</div>
""", unsafe_allow_html=True)

# ---------- ANALYTICS PLACEHOLDER ----------
st.markdown("## 📊 Analytics & Forensics")
st.markdown("""
<div class="section">
<p>Offline statistical analysis and comparisons will appear here.</p>
</div>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<center>CPS IDS Platform • Phase-1 Monitoring Layer</center>", unsafe_allow_html=True)
