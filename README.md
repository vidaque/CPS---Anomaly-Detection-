# 🚗 CPS-SHIELD  
### Machine Learning Based Anomaly Detection for Cyber-Physical Systems  
#### Smart Vehicle Case Study

---

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/ML-IsolationForest-orange?style=for-the-badge&logo=scikitlearn)
![SocketCAN](https://img.shields.io/badge/CAN-SocketCAN-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red?style=for-the-badge&logo=streamlit)
![Status](https://img.shields.io/badge/System-Live%20Detection-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-Academic-lightgrey?style=for-the-badge)

</p>

---

## 📌 Project Overview

**CPS-SHIELD** is a real-time Security Operations Center (SOC) simulation designed to detect cyber attacks in **Cyber-Physical Systems (CPS)** using Machine Learning.

This project models a **Smart Vehicle environment**, simulates CAN communication, injects cyber attacks, and detects anomalies using an unsupervised ML model.

It demonstrates how intelligent anomaly detection can protect safety-critical automotive systems.

---

## 🎯 Core Objectives

✔ Simulate smart vehicle dynamics  
✔ Emulate CAN bus communication  
✔ Inject real cyber attacks  
✔ Detect anomalies using ML  
✔ Visualize results in a SOC-style dashboard  

---

## 🏗 System Architecture

Vehicle Simulator
↓
Virtual CAN Bus (vcan0)
↓
CAN Receiver
↓
Live Telemetry Stream (CSV)
↓
ML Detection Engine
↓
SOC Dashboard (Streamlit)


---

## 🧠 Machine Learning Engine

### Algorithm Used:
**Isolation Forest**

### Why Isolation Forest?

- Unsupervised anomaly detection
- No labeled attack dataset required
- Fast and lightweight
- Suitable for real-time CPS systems

### Detection Logic:

1. Learn baseline normal vehicle behavior  
2. Compute anomaly score for live data  
3. Apply threshold-based detection  
4. Use persistence counter to avoid false positives  
5. State transition model:

NORMAL → ATTACK → RECOVERY → NORMAL


---

## 🚨 Implemented Attack Modules

### 🔥 Sensor Spoofing Attack
Injects extreme speed and steering values to simulate malicious ECU manipulation.

### ♻ Replay Attack
Replays previously recorded CAN frames to simulate deceptive behavior.

### ⏳ Timing / Delay Attack
Alters CAN message timing to simulate communication disruption.

---

## 📊 SOC Dashboard Features

- Real-time anomaly detection status
- Severity classification (NONE / LOW / MEDIUM / HIGH)
- Dynamic donut threat visualization
- Live vehicle telemetry graph
- Security event timeline
- System health monitoring
- Auto-refresh mechanism

---

## ⚙ Technologies Used

- Python 3
- Scikit-learn
- Isolation Forest
- SocketCAN (vcan0)
- Pandas
- Streamlit
- Plotly

---

## 🚀 How To Run

### 1️⃣ Enable Virtual CAN

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
2️⃣ Start Vehicle Simulator
python3 simulator/vehicle_simulator.py
3️⃣ Start CAN Receiver
python3 receiver/can_receiver.py
4️⃣ Start ML Detection Engine
python3 -m ml.live_detection
5️⃣ Launch SOC Dashboard
streamlit run dashboard/app.py
6️⃣ Trigger Attack
python3 attacks/attack_spoofing.py
📈 Expected System Behavior
Scenario	ML State	Dashboard
Normal Operation	NORMAL	Green
Active Attack	ATTACK	Red Alert
Attack Stopped	RECOVERY	Yellow
Stabilized	NORMAL	Green
🛡 Detection Scope
This system performs:

✔ Real-time anomaly detection
✔ Severity assessment
✔ Live SOC visualization

Future upgrades may include:

Automated mitigation response

Multi-model ensemble detection

Deep learning-based CPS defense

Hardware deployment on Raspberry Pi

Production-grade streaming architecture

📂 Project Structure
attacks/
simulator/
receiver/
ml/
dashboard/
config/
cps/
🎓 Academic Relevance
This project demonstrates:

Cyber-Physical System security

Automotive intrusion detection

Machine learning in critical infrastructure

SOC monitoring design

Real-time anomaly detection

👨‍💻 Developed By
Aadith KV


🔬 Future Scope
Hardware implementation (Raspberry Pi + CAN HAT)

Cloud-based monitoring system

Automotive IDS integration

Multi-layer CPS defense architecture

📜 License
Academic Project – For Educational Use Only
