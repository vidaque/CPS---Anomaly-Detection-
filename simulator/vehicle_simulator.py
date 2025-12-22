import time
import csv
import random
from datetime import datetime

class Vehicle:
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

    def read_sensors(self):
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "speed": round(self.speed + random.uniform(-0.5, 0.5), 2),
            "brake": int(self.brake),
            "steering": round(self.steering, 2)
        }

def run_simulation(steps=100):
    vehicle = Vehicle()

    with open("data/raw/vehicle_simulation.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["timestamp", "speed", "brake", "steering"]
        )
        writer.writeheader()

        for step in range(steps):
            if step % 30 == 0:
                vehicle.brake = not vehicle.brake

            vehicle.update_state()
            data = vehicle.read_sensors()
            writer.writerow(data)

            time.sleep(0.1)

if __name__ == "__main__":
    run_simulation()
