import can
import time
from vehicle_simulator import Vehicle

bus = can.interface.Bus(
    channel='vcan0',
    interface='socketcan'
)

vehicle = Vehicle()

print("[CAN SENDER] Started")

try:
    while True:
        vehicle.update_state()
        data = vehicle.read_sensors()

        payload = [
            int(data["speed"]) & 0xFF,
            int(data["brake"]) & 0xFF,
            int(data["steering"] + 128) & 0xFF,
            0x00
        ]

        msg = can.Message(
            arbitration_id=0x123,
            data=payload,
            is_extended_id=False
        )

        bus.send(msg)
        print(f"[SENT] Speed={data['speed']} Brake={data['brake']} Steering={data['steering']}")

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\n[CAN SENDER] Stopped by user")

finally:
    bus.shutdown()
    print("[CAN SENDER] CAN interface closed")
