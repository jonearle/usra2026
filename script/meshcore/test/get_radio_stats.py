import asyncio
from meshcore import MeshCore, EventType

async def main():
    # Connect to device
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

    # Get stats
    result = await meshcore.commands.get_stats_radio()
    if result.type == EventType.ERROR:
        print("Failed to get radio stats")
    else:
        print("Radio stats:")
        for stat, value in result.payload:
            print(f"{stat}: {value}")
    
    await meshcore.disconnect()

asyncio.run(main())