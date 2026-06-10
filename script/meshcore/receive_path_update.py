import asyncio
import csv
import json
import time
from meshcore import MeshCore, EventType

def csvWrite(path, data):
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

async def connectBLE(bleAddress):
    # Connect to device
    # T-Beam v1.1 on MacOS = B93730B7-CA50-4718-2293-57AE6FF3348B
    # Ubuntu will always be /dev/ttyACM0
    try:
        iface = await MeshCore.create_ble(bleAddress)
    except ConnectionError:
        print("Failed to connect")
        return
    if iface is None:
        print("Failed to connect")
        return
    print("Device successfully connected")

    return iface

async def main():
    # Connect to device via bluetooth
    # T-Beam v1.1 = B93730B7-CA50-4718-2293-57AE6FF3348B
    meshcore = await connectBLE("B93730B7-CA50-4718-2293-57AE6FF3348B")
    if meshcore is None:
        return

    # Subscribe to raw data events
    def handle_packet(event):
        timestamp = time.time()

        msg = json.loads(event.payload["txt"])

        data = [timestamp, msg["lat"], msg["lon"], msg["alt"], msg["packetID"]]

        csvWrite("/Users/Jon/USRA2026/data/desk.csv", data)

    meshcore.subscribe(EventType.CONTACT_MSG_RECV, handle_packet)

    while True:
        await asyncio.sleep(1)

asyncio.run(main())