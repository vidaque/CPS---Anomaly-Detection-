import can
import csv
from datetime import datetime

bus = can.interface.Bus(
    channel='vcan0',
    interface='socketcan'
)

print("[CAN RECEIVER] Listening on vcan0")

try:
    with open("data/raw/can_logs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "speed", "brake", "steering"])

        for msg in bus:
            speed = msg.data[0]
            brake = msg.data[1]
            steering = msg.data[2] - 128

            writer.writerow([
                datetime.utcnow().isoformat(),
                speed,
                brake,
                steering
            ])

            print(f"[RECEIVED] Speed={speed} Brake={brake} Steering={steering}")

except KeyboardInterrupt:
    print("\n[CAN RECEIVER] Stopped by user")

finally:
    bus.shutdown()
    print("[CAN RECEIVER] CAN interface closed")
