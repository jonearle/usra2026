import meshtastic
import meshtastic.serial_interface

iFace = meshtastic.serial_interface.SerialInterface()

iFace.sendText(text="test", destinationId="!dadfb6c8")