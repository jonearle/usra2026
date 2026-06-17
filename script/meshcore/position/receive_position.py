import asyncio
import csv
import json
from meshcore import MeshCore, EventType

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

        if msg.type != EventType.CONTACT_MSG_RECV:
            continue

        locationData = json.loads(msg.payload['text'])
        lat = locationData["lat"]
        long = locationData["long"]
        alt = locationData["alt"]

        radioStats = await meshcore.commands.get_stats_radio()

        rssi = radioStats.payload["last_rssi"]
        snr = radioStats.payload["last_snr"]

        # Open CSV file and write
        with open(
            "/Users/Jon/USRA2026/data/desk.csv", 
            "a", 
            newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow([rssi, snr, lat, long, alt])

        print("Data successfully written to CSV")

asyncio.run(main())