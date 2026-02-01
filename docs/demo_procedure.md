# CPS Anomaly Detection – Demo Procedure

## Normal Baseline Phase
1. Start vehicle simulator
2. Start CAN receiver
3. Start ML anomaly detection
4. Allow baseline learning on normal behavior
5. Verify CPS state is NORMAL

## Attack Demonstration Phase
6. Launch attack script (replay / delay / spoofing)
7. Observe anomaly detection
8. Verify CPS state switches to ATTACK
9. Observe dashboard alert and severity escalation

## Recovery Phase
10. Stop attack
11. Observe recovery and return to NORMAL
