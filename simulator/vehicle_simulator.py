import time
import csv
import os
import random

from cps.sensors.sensor_emulator import read_sensors
from cps.can.can_sender import CANTransmitter

CSV_PATH = "data/raw/vehicle_simulation.csv"
SLEEP_TIME = 0.1


class Vehicle:
    """Vehicle physical dynamics (no sensor logic here)"""

    def __init__(self):
        self.speed = 0.0
        self.brake = False
        self.steering = 0.0

    def update_state(self):
        if self.brake:
            self.speed = max(0, self.speed - 3)
        else:
            self.speed += random.uniform(0.5, 1.5)

        self.steering += random.uniform(-0.3, 0.3)

    def get_state(self):
        return {
            "speed": self.speed,
            "brake": self.brake,
            "steering": self.steering
        }


def ensure_csv():
    os.makedirs("data/raw", exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["timestamp", "speed", "brake", "steering"]
            )
            writer.writeheader()


def run_simulation():
    print("[CPS] Vehicle simulator started (sensor emulation + CAN)")

    vehicle = Vehicle()
    can_tx = CANTransmitter()

    ensure_csv()

    try:
        with open(CSV_PATH, "a", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["timestamp", "speed", "brake", "steering"]
            )

            step = 0
            while True:
                if step % 30 == 0:
                    vehicle.brake = not vehicle.brake

                vehicle.update_state()

                vehicle_state = vehicle.get_state()
                data = read_sensors(vehicle_state)

                writer.writerow(data)
                f.flush()

                can_tx.send(
                    data["speed"],
                    data["brake"],
                    data["steering"]
                )

                time.sleep(SLEEP_TIME)
                step += 1

    except KeyboardInterrupt:
        print("\n[CPS] Simulator stopped by user")

    finally:
        can_tx.close()
        print("[CPS] CAN bus closed cleanly")


if __name__ == "__main__":
    run_simulation()
