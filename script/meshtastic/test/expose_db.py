# Generated code

import meshtastic
import meshtastic.serial_interface

iface = meshtastic.serial_interface.SerialInterface()

print(f"Connected to {iface.getLongName()}\n")

print(f"{'Node':<6} {'Hops':<5} {'SNR (dB)':<8}")
print("-" * 25)

for node in iface.nodes.values():
    user = node.get("user", {})

    print(
        f"{user.get('shortName', 'N/A'):<6} "
        f"{str(node.get('hopsAway', 'N/A')):<5} "
        f"{str(node.get('snr', 'N/A')):<8}"
    )