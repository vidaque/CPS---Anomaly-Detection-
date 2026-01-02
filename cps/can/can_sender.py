import can
from config.can_config import CAN_INTERFACE, CAN_CHANNEL, CAN_ID


class CANTransmitter:
    """
    CPS CAN transmitter.
    Supports virtual CAN (vcan0) and real CAN (can0).
    """

    def __init__(self):
        self.bus = can.interface.Bus(
            channel=CAN_CHANNEL,
            interface=CAN_INTERFACE
        )

    def send(self, speed, brake, steering):
        data = [
            int(speed) & 0xFF,
            int(brake) & 0xFF,
            int(steering) & 0xFF
        ]

        msg = can.Message(
            arbitration_id=CAN_ID,
            data=data,
            is_extended_id=False
        )

        self.bus.send(msg)

    def close(self):
        """Gracefully shut down CAN bus"""
        self.bus.shutdown()
