import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from csv_write import csvWrite

# What to do when a packet is received
def onReceive(packet, interface):
    receivedTime = time.time()

    if packet["decoded"]["portnum"] == "TELEMETRY_APP":
        payload = packet["decoded"]["telemetry"]["deviceMetrics"]

        nodeID = packet["fromId"]

        air_util_tx_ms = payload["airUtilTx"]
        uptime_seconds = payload["uptimeSeconds"]

        csvWrite("/Users/Jon/usra2026/data/desk.csv", [receivedTime, nodeID, air_util_tx_ms, uptime_seconds])


    if packet["decoded"]["portnum"] == "TEXT_MESSAGE_APP":
        payload = packet["decoded"]["payload"].decode("utf-8")

        try:
            int(payload) # If this is successful that means it is a delivery_rate oriented message

            csvWrite("/Users/Jon/usra2026/data/delivery_rate/meshtastic_delivery_rate.csv", [payload, receivedTime])   
            print(f"{payload}, Data successfully written to CSV")
        except ValueError:
            try:
                float(payload)

                csvWrite("/Users/Jon/usra2026/data/latency/meshtastic_latency.csv", [payload, receivedTime])   
                print(f"{payload}, Data successfully written to CSV")
            except ValueError:
                print("Not the correct packet")

# Connect to receiver node
# Node: Meshtastic_b6c8
iFace = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iFace.getLongName()))

# Subscribe to receiving packets
pub.subscribe(onReceive, "meshtastic.receive")

while True:
    time.sleep(1)