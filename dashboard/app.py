import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CPS Security Monitoring Platform",
    page_icon="🚗",
    layout="wide"
)

# ---------- LOAD CSS ----------
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
st.markdown("""
<div class="section">
<p>Live sensor charts (speed, steering, brake) will appear here.</p>
</div>
""", unsafe_allow_html=True)

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
