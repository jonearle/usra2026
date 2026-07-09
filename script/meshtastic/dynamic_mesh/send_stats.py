import time
import json
import requests
import meshtastic
import meshtastic.serial_interface
from meshtastic.mesh_interface import MeshInterface

# Node: Meshtastic_b03c
iFace = meshtastic.serial_interface.SerialInterface()

try:
    localID = 1

    # Send test packets 10 seconds
    while True:
        # Get location
        location = requests.get("http://localhost:8080/location").json()

        payload = {
            "localID": localID,
            "sendTime": time.time(),
            "lat": location['lat'],
            "long": location['lon'],
            "alt": location['alt']
        }

        iFace.sendData(json.dumps(payload).encode())

        print("Packet sent")

        localID += 1

        time.sleep(30)
except (KeyboardInterrupt, MeshInterface.MeshInterfaceError):
    print(f"Packets sent: {localID}")

