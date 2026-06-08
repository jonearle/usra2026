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

        radioStats = await meshcore.commands.get_stats_radio()

        #debug
        coreStats = await meshcore.commands.get_stats_core()
        packetStats = await meshcore.commands.get_stats_packets()

        print(coreStats.payload)
        print()
        print(radioStats.payload)
        print()
        print(packetStats.payload)
        print()
        print(msg)
        print()
        print(vars(msg))
        print()
        print(msg.__dict__)
        print()

        print("--------------------------")
        print()

asyncio.run(main())