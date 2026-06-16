import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from csv_write import csvWrite

# What to do when a packet is received
def onReceive(packet, interface):
    receivedTime = time.time()

    if packet["decoded"]["portnum"] == "TEXT_MESSAGE_APP":
        sendTime = float(packet["decoded"]["payload"].decode("utf-8"))
        diff = receivedTime - sendTime

        rssi = packet.get("rxRssi")
        snr = packet.get("rxSnr")
        
        # Add to csv file
        csvWrite("/Users/Jon/USRA2026/data/bike_comparison_test/meshtastic.csv", [sendTime, receivedTime, diff, rssi, snr])    
        print(f"{diff}, Data successfully written to CSV")

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive")

while True:
    time.sleep(1)