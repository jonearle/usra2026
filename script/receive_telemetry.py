import time
import meshtastic
import meshtastic.ble_interface
from pubsub import pub

packetHistory = []
packetsReceived = 0

def getAirtime(uptimeSeconds, airUtilTx):
    return uptimeSeconds * (airUtilTx / 100)

# What to do when a packet is received
def onReceive(packet, interface):
    global packetsReceived

    # Make sure we are only working with text (for now?)
    if packet["decoded"]["portnum"] != "TELEMETRY_APP":
        return
    
    # Update packets received
    packetsReceived += 1

    deviceMetrics = packet["decoded"]["telemetry"]["deviceMetrics"]

    # Create packet dictionary (simplifed one only for data we need)
    packetInfo = {
        "timestamp": time.time(),
        "nodeID": packet["fromId"],
        "packetID": packet["id"],
        "rssi": packet["rxRssi"],
        "snr": packet["rxSnr"],
        "batteryLevel": deviceMetrics["batteryLevel"],
        "voltage": deviceMetrics["voltage"],
        "airUtilTx": deviceMetrics["airUtilTx"],
        "uptimeSeconds": deviceMetrics["uptimeSeconds"],
        "channelUtilization": deviceMetrics["channelUtilization"],
        "airtime": getAirtime(deviceMetrics["uptimeSeconds"], deviceMetrics["airUtilTx"]),
    }

    # Add packetInfo to packetHistory
    packetHistory.append(packetInfo)

    # Print packet data
    print("Packet Info:")
    print(*packetInfo.values(), sep=", ")
    print()

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.ble_interface.BLEInterface(address="CFCE6566-57CF-6F07-12E8-2A9C44129E5D")
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive")

while True:
    time.sleep(1)