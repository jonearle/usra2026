import time
import json
import meshtastic
import meshtastic.serial_interface

# Node: Meshtastic_b03c
iFace = meshtastic.serial_interface.SerialInterface()

packetsSent = 1

# Send test packets every 2 minutes
while True:
    payload = {
        "packetsSent": packetsSent,
        "sendTime": time.time()
    }

    # Send packet
    iFace.sendText(json.dumps(payload))

    packetsSent += 1

    time.sleep(30)