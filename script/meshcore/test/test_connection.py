import asyncio
from meshcore import MeshCore

async def main():
    # Connect to device
    # T-Beam v1.1 = B93730B7-CA50-4718-2293-57AE6FF3348B
    try:
        meshcore = await MeshCore.create_ble("B93730B7-CA50-4718-2293-57AE6FF3348B")
    except ConnectionError:
        print("Failed to connect")
    else:
        print("Device successfully connected")
        await meshcore.disconnect()

asyncio.run(main())
        
