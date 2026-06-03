import csv
import json
import time
import meshtastic
import meshtastic.serial_interface
from flask import Flask
from pubsub import pub

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
    packetID = packet.get("id")
    rssi = packet.get("rxRssi")
    snr = packet.get("rxSnr")
    lat = position.get("lat")
    long = position.get("long")
    alt = position.get("alt")
    # hopStart = packet.get("hopStart")
    # hopLimit = packet.get("hopLimit")
    # hopsUsed = getHopsUsed(hopStart, hopLimit)

    # Add to csv file
    with open("/home/jonearle/usra2026/data/bike_tests/bike_south_long_fast2.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([receivedTime,packetID,nodeID,rssi,snr,lat,long,alt])
    
    print("Data successfully written to CSV")

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive")

while True:
    time.sleep(1)