import asyncio
import time
from csv_write import csvWrite
from meshcore import MeshCore, EventType
from meshcore_essentials import connectToDeviceBLE, getContact

async def main():
    localID = 0

    meshcore = connectToDeviceBLE("B93730B7-CA50-4718-2293-57AE6FF3348B") # Change as needed

    wantedContact = getContact(meshcore, "1057D6AD") # Change as needed

    sub = meshcore.subscribe(EventType.ACK, handleACK)
    
    # Send msg
    while localID < 100:
        payloadString = f"{localID}, {time.time()}"

        if wantedContact is not None:
            result = await meshcore.commands.send_msg(
                wantedContact, 
                payloadString
            )

            if result.type == EventType.ERROR:
                print("Error sending message")

            localID += 1
        else:
            print("Could not find contact in question")

        await asyncio.sleep(5) # Adjust depending on the test

asyncio.run(main())
