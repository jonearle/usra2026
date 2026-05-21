import time
import meshtastic
import meshtastic.serial_interface

# Node: Meshtastic_b03c
iFace = meshtastic.serial_interface.SerialInterface()

packetsSent = 0

# Send test packets every two minutes
while True:
    # Send packet
    iFace.sendText(str(time.time()))

    # Update packets sent
    packetsSent += 1

    time.sleep(120)