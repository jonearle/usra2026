import csv
import time
import meshtastic
import meshtastic.ble_interface
from pubsub import pub

def getHopsUsed(hopStart, hopLimit):
    return hopStart - hopLimit

# What to do when a packet is received
def onReceive(packet, interface):
    # Get position
    position = packet["decoded"]["position"]

    # Get metrics
    receivedTime = time.time()
    nodeID = packet.get("fromId")
    packetID = packet.get("id")
    rssi = packet.get("rxRssi")
    snr = packet.get("rxSnr")
    lat = position.get("latitude")
    long = position.get("longitude")
    alt = position.get("altitude")
    # hopStart = packet.get("hopStart")
    # hopLimit = packet.get("hopLimit")
    # hopsUsed = getHopsUsed(hopStart, hopLimit)

    # Add to csv file
    with open("/Users/Jon/USRA2026/data/wickwire_inside_noelevation/long_fast.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([receivedTime,packetID,nodeID,rssi,snr,lat,long,alt])
    
    print("Data successfully written to CSV")

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.ble_interface.BLEInterface(address="CFCE6566-57CF-6F07-12E8-2A9C44129E5D")
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive.position")

while True:
    time.sleep(1)