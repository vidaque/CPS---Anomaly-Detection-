import time
import os
import csv
import random

DATA_FILE = "data/live/can_stream.csv"

def ensure_file():
    os.makedirs("data/live", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "speed", "brake", "steering"])

def main():
    print("[ATTACK] 🔥 EXTREME Spoofing Attack Started")
    ensure_file()

    try:
        with open(DATA_FILE, "a", newline="") as f:
            writer = csv.writer(f)

            while True:
                spoof_speed = random.uniform(200, 260)     # extreme speed
                spoof_brake = random.choice([0, 1])
                spoof_steering = random.uniform(80, 140)   # extreme steering

                writer.writerow([
                    time.time(),
                    spoof_speed,
                    spoof_brake,
                    spoof_steering
                ])
                f.flush()

                print("🔥 Injected EXTREME spoofed data")

                time.sleep(0.15)

    except KeyboardInterrupt:
        print("\n[ATTACK] Spoofing stopped safely")

if __name__ == "__main__":
    main()
