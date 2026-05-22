import time
import meshtastic
import meshtastic.serial_interface

# Node: Meshtastic_b03c
iFace = meshtastic.serial_interface.SerialInterface()

# Send test packets every two minutes
while True:
    # Send packet
    iFace.sendText(str(time.time()))

    time.sleep(120)