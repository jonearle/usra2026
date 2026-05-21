import time
import meshtastic
import meshtastic.ble_interface
from pubsub import pub

# Node: Meshtastic_b03c
iFace = meshtastic.ble_interface.BLEInterface(address="B93730B7-CA50-4718-2293-57AE6FF3348B")

packetsSent = 0

# Send test packets every ??? seconds
while True:
    # Send packet
    iFace.sendText(str(time.time()))

    # Update packets sent
    packetsSent += 1

    time.sleep(15)