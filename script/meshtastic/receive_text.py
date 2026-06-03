import csv
import time
import json
import meshtastic
import meshtastic.ble_interface
from pubsub import pub

packetsReceived = 0

def getHopsUsed(hopStart, hopLimit):
    return hopStart - hopLimit

def getDeliveryRate(packetsSent, packetsReceived):
    return (packetsReceived / packetsSent) * 100

def getLatency(receivedTime, sendTime):
    latency = receivedTime - sendTime
    return round(latency, 3)

# What to do when a packet is received
def onReceive(packet, interface):
    # Update packetsReceived
    global packetsReceived
    packetsReceived += 1

    # Decode payload
    payload = json.loads(packet["decoded"]["payload"].decode())

    # Get metrics
    receivedTime = time.time()
    sendTime = float(payload["sendTime"])
    nodeID = packet.get("fromId")
    packetID = packet.get("id")
    rssi = packet.get("rxRssi")
    snr = packet.get("rxSnr")
    # hopStart = packet.get("hopStart")
    # hopLimit = packet.get("hopLimit")
    # hopsUsed = getHopsUsed(hopStart, hopLimit)
    latency = getLatency(receivedTime, sendTime)
    deliveryRate = getDeliveryRate(int(payload["packetsSent"]), packetsReceived)

    # Add to csv file
    with open("/Users/Jon/USRA2026/data/wickwire_inside_noelevation/long_fast.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([receivedTime,packetID,nodeID,rssi,snr,latency,deliveryRate])
    
    print("Data successfully written to CSV")

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.ble_interface.BLEInterface(address="CFCE6566-57CF-6F07-12E8-2A9C44129E5D")
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive.text")

while True:
    time.sleep(1)