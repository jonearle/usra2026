import json
import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from csv_write import csvWrite

def getHopsUsed(hopStart, hopLimit):
    return hopStart - hopLimit

# What to do when a packet is received
def onReceive(packet, interface):
    # Get position
    try:
        position = json.loads(packet["decoded"]["payload"].decode())
    except:
        return

    # Get metrics
    receivedTime = time.time()
    nodeID = packet.get("fromId")
    # packetID = packet.get("id")
    rssi = packet.get("rxRssi")
    snr = packet.get("rxSnr")
    lat = position.get("lat")
    long = position.get("long")
    alt = position.get("alt")
    hopStart = packet.get("hopStart")
    hopLimit = packet.get("hopLimit")
    hopsUsed = getHopsUsed(hopStart, hopLimit)

    # Add to csv file
    csvWrite("/Users/Jon/USRA2026/data/bike_comparison_test/meshtastic.csv", [receivedTime,nodeID,rssi,snr,lat,long,alt,hopsUsed])    
    print("Data successfully written to CSV")

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive")

while True:
    time.sleep(1)