import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from csv_write import csvWrite

# What to do when a packet is received
def onReceive(packet, interface):
    receivedTime = time.time()

    if packet["decoded"]["portnum"] == "TEXT_MESSAGE_APP":
        decoded = packet.get("decoded", {})
        payload = decoded.get('text', '')
        packetID = packet.get('id')
        rssi = packet.get("rxRssi")
        snr = packet.get("rxSnr")

        csvWrite("/Users/Jon/usra2026/data/PlexToGB/5sec.csv", [payload, packetID, receivedTime, rssi, snr])   
        print(f"{payload}, Data successfully written to CSV")

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive")

while True:
    time.sleep(1)