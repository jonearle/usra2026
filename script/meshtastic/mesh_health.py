import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub

# make sure that the neighbour_info module is turned on for ALL nodes in the mesh

def on_receive(packet, interface):
    decoded = packet.get("decoded", {})

    if decoded.get("portnum") == "NEIGHBORINFO_APP":
        print(packet)

# Connect to receiver node
iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

pub.subscribe(on_receive, "meshtastic.receive")

while True:
    time.sleep(1)



