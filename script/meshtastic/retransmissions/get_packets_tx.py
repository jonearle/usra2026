import subprocess
import time
from csv_write import csvWrite
import meshtastic.serial_interface
import meshtastic.util

# Get node id
interface = meshtastic.serial_interface.SerialInterface()
node_id = str('!' + hex(interface.myInfo.my_node_num)[2:])
interface.close()

result = subprocess.run(
    ["meshtastic", "--request-telemetry", "local_stats", "--dest", node_id], # change as needed
    capture_output=True,
    text=True,
    check=True
)

stats = {}

# Strip plain text
for line in result.stdout.splitlines():
    if ":" in line:
        key, value = line.split(":", 1)

        try:
            stats[key.strip()] = float(value.strip())
        except ValueError:
            pass

try:
    line = [
        time.time(), 
        node_id, 
        stats["uptimeSeconds"],
        stats["channelUtilization"],
        stats["airUtilTx"],
        stats["numPacketsTx"],
        stats["numPacketsRx"],
        stats["numPacketsRxBad"],
        stats["numRxDupe"],
        stats["numTxRelay"],
        stats["numOnlineNodes"],
        stats["numTotalNodes"]]

    csvWrite("/Users/Jon/usra2026/data/retransmission/final.csv", line)
except:
    print("wait")
