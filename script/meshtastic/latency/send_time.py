import time
import meshtastic
import meshtastic.serial_interface

# Node: Meshtastic_b03c
iFace = meshtastic.serial_interface.SerialInterface()

count = 1

# Send test packets 10 seconds
while count <= 500:
    iFace.sendText(text=str(time.time()), destinationId='!dadfb03c')
    
    print("Packet sent") # Add once route is chosen

    count += 1

    time.sleep(5)