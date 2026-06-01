import time
import json
import requests
import meshtastic
import meshtastic.serial_interface

# Node: Meshtastic_b03c
iFace = meshtastic.serial_interface.SerialInterface()

packetsSent = 1

# Send test packets 10 seconds
while True:
    # Get location
    location = requests.get("http://localhost:8080/location").json()

    payload = {
        "lat": location['lat'],
        "long": location['lon'],
        "alt": location['alt']
    }

    iFace.sendData(json.dumps(payload).encode())

    packetsSent += 1

    time.sleep(10)