import time
import csv
import meshtastic
import meshtastic.ble_interface
from pubsub import pub

# Record when packet was sent for latency
sendTimes = {}

def getHopsUsed(hopStart, hopLimit):
    if hopStart is not None and hopLimit is not None:
        hopsUsed = getHopsUsed(hopStart, hopLimit)
    
    return hopsUsed

def getLatency(receivedTime, packetID):
    global sendTimes
    
    # Get latency and delete the stores send time
    if packetID in sendTimes: 
        latency = receivedTime - sendTimes[packetID]
        del sendTimes[packetID]
        return latency
    else:
        return

# What to do when a packet is received
def onReceive(packet, interface):
    print("Ping received")

    # Get metrics
    receivedTime = time.time()
    nodeID = packet.get("fromId")
    packetID = packet.get("requestId")
    rssi = packet.get("rxRssi")
    snr = packet.get("rxSnr")
    hopStart = packet.get("hopStart")
    hopLimit = packet.get("hopLimit")
    hopsUsed = getHopsUsed(hopStart, hopLimit)
    latency = getLatency(receivedTime, packetID)

    # Add to csv file
    with open("/Users/Jon/USRA2026/data/packet_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([receivedTime,packetID,nodeID,rssi,snr,latency,hopsUsed])
    
    print("Data successfully written to CSV")

# Create file header
with open("/Users/Jon/USRA2026/data/packet_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp","packetID","nodeID","rssi","snr","latency","hopsUsed"])

# Connect to sender/ping node
# Node: Meshtastic_b6c8
iface = meshtastic.ble_interface.BLEInterface(address="CFCE6566-57CF-6F07-12E8-2A9C44129E5D")
print("Connected to " + str(iface.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive")

# Send a packet every 2 minutes
while True:
    packet = iface.sendText("p", destinationId="!dadfb03c", wantAck=True)

    print("Ping sent")

    # Locally store send time
    sendTimes[packet.id] = time.time()   

    time.sleep(15)

