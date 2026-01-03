import can
import csv
import time
import os
from config.can_config import CAN_INTERFACE, CAN_CHANNEL

OUTPUT_FILE = "data/live/can_stream.csv"


def ensure_output():
    os.makedirs("data/live", exist_ok=True)
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "speed", "brake", "steering"])


def main():
    ensure_output()

    bus = can.interface.Bus(
        channel=CAN_CHANNEL,
        interface=CAN_INTERFACE
    )

    print("[RECEIVER] Listening on CAN bus...")

    try:
        with open(OUTPUT_FILE, "a", newline="") as f:
            writer = csv.writer(f)

            for msg in bus:
                timestamp = time.time()

                # Decode CPS sensor data
                speed = msg.data[0]
                brake = msg.data[1]
                steering = msg.data[2]

                writer.writerow([timestamp, speed, brake, steering])
                f.flush()

    except KeyboardInterrupt:
        print("\n[RECEIVER] Receiver stopped by user")

    finally:
        bus.shutdown()
        print("[RECEIVER] CAN bus closed cleanly")


if __name__ == "__main__":
    main()
