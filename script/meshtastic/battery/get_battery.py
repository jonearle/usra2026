import subprocess
import time
from csv_write import csvWrite
import meshtastic.serial_interface
import meshtastic.util

# Get node id
interface = meshtastic.serial_interface.SerialInterface()
nodeID = str('!' + hex(interface.myInfo.my_node_num)[2:])

while True:
    result = subprocess.run(
        ["meshtastic", "--info"], # change as needed
        capture_output=True,
        text=True,
        check=True
    )

    deviceMetrics = interface.nodes.get(nodeID, {}).get('deviceMetrics', {})

    data = [time.time(), nodeID]
    for value in deviceMetrics.values():
        data.append(value)

    csvWrite("/Users/Jon/usra2026/data/desk.csv", data)

    time.sleep(3600)

