import csv
import time
import meshtastic
import meshtastic.ble_interface
from pubsub import pub

def getHopsUsed(hopStart, hopLimit):
    return hopStart - hopLimit

def getLatency(receivedTime, sendTime):
    return receivedTime - sendTime

# What to do when a packet is received
def onReceive(packet, interface):
    # Get metrics
    receivedTime = time.time()
    sendTime = float(packet["decoded"]["payload"].decode())
    nodeID = packet.get("fromId")
    packetID = packet.get("requestId")
    rssi = packet.get("rxRssi")
    snr = packet.get("rxSnr")
    hopStart = packet.get("hopStart")
    hopLimit = packet.get("hopLimit")
    hopsUsed = getHopsUsed(hopStart, hopLimit)
    latency = getLatency(receivedTime, sendTime)

    # Add to csv file
    with open("/Users/Jon/USRA2026/data/packet_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([receivedTime,packetID,nodeID,rssi,snr,latency,hopsUsed])
    
    print("Data successfully written to CSV")

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.ble_interface.BLEInterface(address="CFCE6566-57CF-6F07-12E8-2A9C44129E5D")
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive.text")

while True:
    time.sleep(1)