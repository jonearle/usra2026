import meshtastic
import meshtastic.serial_interface

iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

iFace.localNode.resetNodeDb()
iFace.nodes.clear()