import asyncio
import csv
import time
from meshcore import MeshCore, EventType
from csv_write import csvWrite


async def main():
    # Connect to device via bluetooth
    # T-Beam v1.1 = B93730B7-CA50-4718-2293-57AE6FF3348B
    try:
        meshcore = await MeshCore.create_ble(
            "B93730B7-CA50-4718-2293-57AE6FF3348B"
            )
    except ConnectionError:
        print("Failed to connect")
        return
    if meshcore is None:
        print("Failed to connect")
        return
    print("Device successfully connected")

    # Get messages and write data to CSV
    while True:
        msg = await meshcore.commands.get_msg(timeout=1)

        receivedTime = time.time()

        if msg.type != EventType.CONTACT_MSG_RECV:
            continue

        payload = msg.payload["message"]

        try:
            int(payload) # If this is successful that means it is a delivery_rate oriented message

            csvWrite("/Users/Jon/usra2026/data/delivery_rate/meshcore_delivery_rate.csv", [payload, receivedTime])   
            print(f"{payload}, Data successfully written to CSV")
        except ValueError:
            try:
                float(payload)

                csvWrite("/Users/Jon/usra2026/data/latency/meshcore_latency.csv", [payload, receivedTime])   
                print(f"{payload}, Data successfully written to CSV")
            except ValueError:
                print("Not the correct packet")

      

asyncio.run(main())