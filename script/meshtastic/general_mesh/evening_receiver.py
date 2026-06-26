import meshtastic
import time
from pubsub import pub
from csv_write import csvWrite

currentPath = ""
intervals = [1450, 2200, 3200, 4200, 16200]
paths = [
    "/Users/Jon/usra2026/data/PlexToGB/5sec/5sec_night.csv",
    "/Users/Jon/usra2026/data/PlexToGB/20sec/20sec_night.csv",
    "/Users/Jon/usra2026/data/PlexToGB/40sec/40sec_night.csv",
    "/Users/Jon/usra2026/data/PlexToGB/1min/1min_night.csv",
    "/Users/Jon/usra2026/data/PlexToGB/5min/5min_night.csv"
]

def onReceive(packet, interface):
    receivedTime = time.time()

    if packet["decoded"]["portnum"] == "TEXT_MESSAGE_APP":
        packetID = packet.get('id')

        # Hop data
        fromId = packet.get("fromId")
        toId = packet.get("toId")
        relayNode = packet.get("relayNode")
        hops = packet.get("hopStart") - packet.get("hopLimit")

        # Payload (delivery rate + latency)
        decoded = packet.get("decoded", {})
        payload = decoded.get('text', '')

        # Signal strength
        rssi = packet.get("rxRssi")
        snr = packet.get("rxSnr")

        csvWrite(currentPath, [packetID, fromId, toId, relayNode, hops, payload, rssi, snr])   
        print(f"{payload}, Data successfully written to CSV")

# Connect to receiver node
iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

for interval, path in zip(intervals, paths):
    currentPath = path

    startTime = time.time()
    while time.time() - startTime < interval:
        time.sleep(1)

