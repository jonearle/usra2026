import asyncio
import time
from csv_write import csvWrite
from meshcore import MeshCore, EventType
from meshcore_essentials import connectToDeviceBLE, getContact

async def main():
    meshcore = connectToDeviceBLE("B93730B7-CA50-4718-2293-57AE6FF3348B") # Change as needed

    wantedContact = getContact(meshcore, "1057D6AD") # Change as needed

    async def handleBattery():
        csvWrite("/Users/Jon/usra2026/data/battery/MC_battery.csv")
        print(f"{time.time()}: Successfully polled battery info")

    sub = meshcore.subscribe(EventType.BATTERY, handleBattery)

    async def triggerBattery():
        while True:
            print("Triggered battery event")
            asyncio.sleep(3600)

    task = asyncio.create_task(triggerBattery())

    try:
        # Keep program running
        print("Monitoring battery...")
        await asyncio.sleep(float('inf'))
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Clean up
        task.cancel()
        await meshcore.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

    

