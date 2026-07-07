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
    decoded = packet.get("decoded")
    if not decoded:
        return
    if decoded.get("portnum") != "TEXT_MESSAGE_APP":
        return
    
    # Get payload
    try:
        payload = json.loads(decoded["payload"].decode())
    except:
        return

    # Get metrics
    receivedTime = time.time()
    sendTime = payload.get("sendTime")
    localID = payload.get("localID")
    nodeID = packet.get("fromId")
    packetID = packet.get("id")
    rssi = packet.get("rxRssi")
    snr = packet.get("rxSnr")
    lat = payload.get("lat")
    long = payload.get("long")
    alt = payload.get("alt")
    hopStart = packet.get("hopStart")
    hopLimit = packet.get("hopLimit")

    # Add to csv file
    csvWrite("/Users/Jon/USRA2026/data/bike_comparison_test/meshtastic.csv", [localID,packetID,nodeID,sendTime,receivedTime,rssi,snr,lat,long,alt,hopStart,hopLimit])    
    print("Data successfully written to CSV")

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive")

while True:
    time.sleep(1)