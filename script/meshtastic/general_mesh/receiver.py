import json
import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from csv_write import csvWrite

# What to do when a packet is received
def onReceive(packet, interface):
    receivedTime = time.time()

    # Get position
    try:
        position = json.loads(packet["decoded"]["payload"].decode())
    except:
        return

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

        # Location
        lat = position.get("lat")
        long = position.get("long")

        # Signal strength
        rssi = packet.get("rxRssi")
        snr = packet.get("rxSnr")

        csvWrite("/Users/Jon/usra2026/data/PlexToGB/5sec.csv", [packetID, fromId, toId, relayNode, hops, payload, lat, long, rssi, snr])   
        print(f"{payload}, Data successfully written to CSV")

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive")

while True:
    time.sleep(1)