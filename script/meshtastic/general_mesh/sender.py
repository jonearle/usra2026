import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from csv_write import csvWrite

def onReceive(packet, interface):
    receivedTime = time.time()
    if packet.get('decoded', {}).get('portnum') == 'ROUTING_APP':
        decoded = packet.get('decoded', {})
        routing = decoded.get('routing', {})

        requestID = decoded.get('requestId')  
        rssi = packet.get("rxRssi")
        snr = packet.get("rxSnr")
        error = routing.get('errorReason')

        if error == 'NONE' or error == 'ERROR_NONE' or error == 0:
            csvWrite("/Users/Jon/usra2026/data/deliveryrate_by_snr/dr_by_snr_ack.csv", [requestID, receivedTime, rssi, snr])   
            print(f"{requestID}, Data successfully written to CSV")


iface = meshtastic.serial_interface.SerialInterface()
pub.subscribe(onReceive, "meshtastic.receive.routing")

localID = 1

# Send test packets 10 seconds
while localID <= 50:
    payloadString = f"{localID}, {time.time()}"

    iface.sendText(text=payloadString, destinationId='!dadfb6c8', wantAck=True) # Add once route is chosen
    print("Packet sent")

    localID += 1

    time.sleep(20)

iface.close()