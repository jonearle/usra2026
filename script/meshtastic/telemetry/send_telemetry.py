import time
import meshtastic
import meshtastic.serial_interface

# Node: Meshtastic_b03c
iFace = meshtastic.serial_interface.SerialInterface()

iFace.sendTelemetry(destinationId="!6c73daa0") # Add once route is chosen

time.sleep(5)