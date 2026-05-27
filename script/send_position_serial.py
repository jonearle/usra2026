import time
import json
import meshtastic
import meshtastic.serial_interface

# Node: Meshtastic_b03c
iFace = meshtastic.serial_interface.SerialInterface()

packetsSent = 1

# Send test packets 10 seconds
while True:
    # Send packet
    iFace.sendPosition()
    print("Packet sent")

    packetsSent += 1

    time.sleep(10)