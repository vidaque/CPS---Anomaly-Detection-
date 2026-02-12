import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# ===============================
# AUTO REFRESH EVERY 2 SECONDS
# ===============================
st_autorefresh(interval=2000, key="soc_refresh")

st.set_page_config(
    page_title="CPS-SHIELD SOC",
    layout="wide"
)

# ===============================
# PROJECT ROOT PATH
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILE = os.path.join(BASE_DIR, "data/live/can_stream.csv")
STATE_FILE = os.path.join(BASE_DIR, "ml/state.txt")
SEVERITY_FILE = os.path.join(BASE_DIR, "ml/severity.txt")
SCORE_FILE = os.path.join(BASE_DIR, "ml/anomaly_score.txt")
EVENT_LOG = os.path.join(BASE_DIR, "ml/events.log")

# ===============================
# SAFE FILE READ
# ===============================
def read_file(path, default="N/A"):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return default

def file_active(path, timeout=5):
    if not os.path.exists(path):
        return False
    last_mod = os.path.getmtime(path)
    return (time.time() - last_mod) < timeout

def load_data():
    try:
        df = pd.read_csv(DATA_FILE, on_bad_lines="skip")
        return df
    except:
        return pd.DataFrame()

# ===============================
# LOAD LIVE STATE
# ===============================
state = read_file(STATE_FILE, "NORMAL")
severity = read_file(SEVERITY_FILE, "NONE")
score = read_file(SCORE_FILE, "0.0")
df = load_data()

simulator_active = file_active(DATA_FILE)
HEARTBEAT_PATH = os.path.join(BASE_DIR, "ml/heartbeat.txt")
ml_active = file_active(HEARTBEAT_PATH)



# ===============================
# HEADER
# ===============================
st.markdown("""
<h1 style='color:#00ffff;font-size:50px;margin-bottom:0px;'>
CPS-SHIELD
</h1>
<h3 style='color:#9ca3af;margin-top:0px;'>
Cyber-Physical System Security Operations Center
</h3>
<hr>
""", unsafe_allow_html=True)

# ===============================
# ALERT SECTION
# ===============================
if state == "ATTACK":
    st.error(f"🚨 SYSTEM UNDER ATTACK | Severity: {severity}")
elif state == "RECOVERY":
    st.warning("⚠ System Recovering")
else:
    st.success("✅ System Operating Normally")

# ===============================
# KPI ROW
# ===============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("CPS State", state)
col2.metric("Severity Level", severity)
col3.metric("Anomaly Score", score)
col4.metric("Last Update", datetime.now().strftime("%H:%M:%S"))

st.divider()

# ===============================
# DONUT THREAT VISUAL
# ===============================
st.subheader("Threat Severity Visualization")

color_map = {
    "NONE": "#00ff9c",
    "LOW": "#facc15",
    "MEDIUM": "#fb923c",
    "HIGH": "#ef4444"
}

level_map = {
    "NONE": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3
}

value = level_map.get(severity, 0)

fig = go.Figure(go.Pie(
    values=[value, 3-value],
    hole=0.7,
    marker_colors=[color_map.get(severity, "#00ff9c"), "#1f2937"],
    textinfo="none"
))

fig.update_layout(
    showlegend=False,
    height=300,
    margin=dict(t=0, b=0, l=0, r=0)
)

st.plotly_chart(fig, width="stretch")

st.divider()

# ===============================
# TELEMETRY
# ===============================
st.subheader("Live Vehicle Telemetry")

if not df.empty and "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df = df.tail(100)
    st.line_chart(df.set_index("timestamp")[["speed", "steering"]])
else:
    st.info("Waiting for simulator data...")

st.divider()

# ===============================
# EVENT TIMELINE
# ===============================
st.subheader("Security Event Timeline")

if os.path.exists(EVENT_LOG):
    try:
        events = pd.read_csv(EVENT_LOG, header=None,
                             names=["time", "event", "description"])
        events["time"] = pd.to_datetime(events["time"], unit="s")

        if "clear_ui" not in st.session_state:
            st.session_state.clear_ui = False

        if not st.session_state.clear_ui:
            st.dataframe(events.tail(15), width="stretch")

        if st.button("Clear Timeline View"):
            st.session_state.clear_ui = True

    except:
        st.info("Event log not readable.")
else:
    st.info("No security events recorded yet.")

st.divider()

# ===============================
# SYSTEM HEALTH
# ===============================
st.subheader("System Health Monitoring")

colA, colB = st.columns(2)

colA.metric("Simulator Status", 
            "ACTIVE" if simulator_active else "INACTIVE")

colB.metric("ML Engine Status", 
            "ACTIVE" if ml_active else "INACTIVE")
