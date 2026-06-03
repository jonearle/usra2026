import time
import meshtastic
import meshtastic.serial_interface

iface = meshtastic.serial_interface.SerialInterface()
print("Connected")

while True:
    id = iface.getMyNodeInfo()["user"]["id"]
    node = iface.nodes[id]
    print(node)
    position = node.get("position", {})

    print("Latitude:", position.get("latitude"))
    print("Longitude:", position.get("longitude"))
    print("Altitude:", position.get("altitude"))
    print("GPS Time:", position.get("time"))

    print("------------------")

    time.sleep(1)