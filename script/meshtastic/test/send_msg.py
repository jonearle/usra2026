import meshtastic
import time
import meshtastic.serial_interface

iFace = meshtastic.serial_interface.SerialInterface()

while True:
    iFace.sendText(text="test", destinationId="!ea2468b0")
    print("message sent")

    time.sleep(10)