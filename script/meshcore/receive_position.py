import asyncio
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

    # Get messages
    while True:
        msg = await meshcore.commands.get_msg(timeout=1)

        if msg.type == EventType.NO_MORE_MSGS:
            print("No messages")
            continue

        print()

    await meshcore.disconnect()

asyncio.run(main())