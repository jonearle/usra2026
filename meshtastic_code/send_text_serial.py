import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub

# Node: Meshtastic_b03c
iFace = meshtastic.serial_interface.SerialInterface()

packetsSent = 0

# Send test packets every ??? seconds
while True:
    # Send packet
    iFace.sendText(str(time.time()))

    # Update packets sent
    packetsSent += 1

    time.sleep(15)