import time
import meshtastic
import meshtastic.ble_interface
from pubsub import pub

def getHopsUsed(hopStart, hopLimit):
    return hopStart - hopLimit

# Not sure how to do this yet where packets sent is in send_text
def getDeliveryRate(packetsReceived, packetsSent):
    if (packetsSent == 0):
        return 0
    return ((packetsReceived / packetsSent) * 100)

def getLatency(receivedTime, sendTime):
    return receivedTime - sendTime

packetHistory = []
packetsReceived = 0

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.ble_interface.BLEInterface(address="CFCE6566-57CF-6F07-12E8-2A9C44129E5D")
print("Connected to " + str(iFace.getLongName()))

# What to do when a packet is received
def onReceive(packet, interface):
    global packetsReceived

    # Make sure we are only working with text (for now?)
    if packet["decoded"]["portnum"] != "TEXT_MESSAGE_APP":
        return

    # Get time packet was sent and received
    receivedTime = time.time()
    sendTime = float(packet["decoded"]["payload"].decode())
    
    # Update packets received
    packetsReceived += 1

    # Create packet dictionary (simplifed one only for data we need)
    packetInfo = {
        "timestamp": receivedTime,
        "nodeID": packet["fromId"],
        "packetID": packet["id"],
        "rssi": packet["rxRssi"],
        "snr": packet["rxSnr"],
        "hopStart": packet["hopStart"],
        "hopLimit": packet["hopLimit"],
        "hopsUsed": getHopsUsed(packet["hopStart"], packet["hopLimit"]),
        "latency": getLatency(receivedTime, sendTime)
    }

    # Add packetInfo to packetHistory
    packetHistory.append(packetInfo)

    # Print packet data
    print(*packetInfo.values(), sep=", ")

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive.text")

while True:
    time.sleep(1)