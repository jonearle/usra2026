import subprocess
import time
import json
import meshtastic
import meshtastic.serial_interface
from csv_write import csvWrite

sender = True

def getAirtimeMetrics():
    # Run traceroute
    try:
        result = subprocess.run(["meshtastic", "--info", "--json"], 
                                capture_output=True, 
                                text=True,
                                check=True,
                                timeout=30)

        data = json.loads(result.stdout)
        airUtilTx = data["deviceMetrics"]["airUtilTx"]
        uptimeSeconds = data["deviceMetrics"]["uptimeSeconds"]
    
        csvWrite("/Users/Jon/usra2026/data/airtime/MT_airtime_PlexToGB.csv", [time.time(), uptimeSeconds, airUtilTx])
    except subprocess.TimeoutExpired:
        print("Subprocess timed out after 30 seconds")

# Connect to device
iface = meshtastic.serial_interface.SerialInterface()

# Get initial time (to keep track of every 5 minutes)
airtimeClock = time.time()
packetClock = time.time()

# Get initial airtime usage
getAirtimeMetrics()
numChecks = 1

# Get airtime usage every 5 minutes
while numChecks < 13:
    if sender and time.time() - sendClock >= 30:
        iface.sendText(text="test", destinationId='!dadfb8d4')
        print("Packet sent")
        sendClock = time.time()

    if time.time() - airtimeClock >= 300:
        getAirtimeMetrics()
        airtimeClock = time.time()
        numChecks += 1

    time.sleep(1)