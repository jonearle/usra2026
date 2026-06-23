import asyncio
import csv
import time
from meshcore import MeshCore, EventType
from csv_write import csvWrite
from meshcore_essentials import connectToDeviceBLE, getContact


async def main():
    # Connect to device via bluetooth
    # T-Beam v1.1 = B93730B7-CA50-4718-2293-57AE6FF3348B
    meshcore = connectToDeviceBLE("B93730B7-CA50-4718-2293-57AE6FF3348B")

    # Get messages and write data to CSV
    while True:
        msg = await meshcore.commands.get_msg(timeout=1)

        receivedTime = time.time()

        if msg.type != EventType.CONTACT_MSG_RECV:
            continue

        payload = msg.payload.get("message")
        rssi = msg.payload.get("rssi")
        snr = msg.payload.get("snr")

        csvWrite(
            "/Users/Jon/usra2026/data/delivery_rate/meshcore_delivery_rate.csv", 
            [payload, receivedTime, rssi, snr]
            )   
        print(f"{payload}, Data successfully written to CSV")

      

asyncio.run(main())