import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub

# What to do when a packet is received
def onReceive(packet, interface):
    if packet["decoded"]["portnum"] == "TELEMETRY_APP":
        print(packet)

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive")

while True:
    time.sleep(1)