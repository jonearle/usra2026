import time
import meshtastic
import meshtastic.serial_interface

iface = meshtastic.serial_interface.SerialInterface()

packetID = 1

# Send test packets 10 seconds
while packetID <= 500:
    iface.sendText(text=str(packetID), destinationId='!dadfb03c') # Add once route is chosen

    print("Packet sent")

    packetID += 1

    time.sleep(5)

