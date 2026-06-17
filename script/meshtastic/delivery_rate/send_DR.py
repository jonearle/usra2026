import time
import meshtastic
import meshtastic.serial_interface

# Node: Meshtastic_b03c
iFace = meshtastic.serial_interface.SerialInterface()

packetID = 1

# Send test packets 10 seconds
while packetID <= 1000:
    iFace.sendText(text=str(packetID), destinationId="???") # Add once route is chosen

    packetID += 1

    time.sleep(5)

