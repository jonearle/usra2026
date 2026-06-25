import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from csv_write import csvWrite

iface = meshtastic.serial_interface.SerialInterface()

localID = 1

# Send test packets 10 seconds
while localID <= 354:
    iface.sendText(text="test", destinationId='!dadfb8d4') # Add once route is chosen
    print("Packet sent")

    localID += 1

    time.sleep(5)

iface.close()