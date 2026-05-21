import time
import meshtastic
import meshtastic.ble_interface

# Node: Meshtastic_b03c
iFace = meshtastic.ble_interface.BLEInterface(address="B93730B7-CA50-4718-2293-57AE6FF3348B")

packetsSent = 0

# Send test packets every 2 minutes
while True:
    # Send packet
    iFace.sendTelemetry()

    # Update packets sent
    packetsSent += 1

    time.sleep(120)