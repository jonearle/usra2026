import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from csv_write import csvWrite

currentPath = ""
waitInterval = 360 # usually is 1200
intervals = [40, 60] # 5, 20, 40, 60, 300
paths = [
    #"/Users/Jon/usra2026/data/PlexToGB/5sec/5sec_night_ACK.csv",
    #"/Users/Jon/usra2026/data/PlexToGB/20sec/20sec_night_ACK.csv",
    "/Users/Jon/usra2026/data/PlexToGB/40sec/40sec_morning_ACK.csv",
    "/Users/Jon/usra2026/data/PlexToGB/1min/1min_morning_ACK.csv",
    #"/Users/Jon/usra2026/data/PlexToGB/5min/5min_night_ACK.csv"
]

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
            csvWrite(currentPath, [requestID, receivedTime, rssi, snr])   
            print(f"{requestID}, Data successfully written to CSV")


# Send test packets 10 seconds
for interval, path in zip(intervals, paths):
    currentPath = path

    iface = meshtastic.serial_interface.SerialInterface()
    pub.subscribe(onReceive, "meshtastic.receive.routing")

    localID = 1

    while localID <= 50:
        payloadString = f"{localID}, {time.time()}"

        iface.sendText(text=payloadString, destinationId='!dadfb8d4', wantAck=True) # Add once route is chosen
        print("Packet sent")

        localID += 1

        time.sleep(interval)

    iface.close()

    time.sleep(waitInterval)