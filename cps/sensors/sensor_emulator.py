import random
from datetime import datetime

def emulate_speed(speed):
    return round(speed + random.uniform(-0.5, 0.5), 2)

def emulate_brake(brake):
    return int(brake)

def emulate_steering(steering):
    return round(steering + random.uniform(-0.3, 0.3), 2)

def read_sensors(vehicle_state):
    """
    Sensor abstraction layer.
    On Raspberry Pi, this will read from real sensors.
    """
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "speed": emulate_speed(vehicle_state["speed"]),
        "brake": emulate_brake(vehicle_state["brake"]),
        "steering": emulate_steering(vehicle_state["steering"])
    }
