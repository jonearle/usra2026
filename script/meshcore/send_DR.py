import asyncio
from meshcore import MeshCore, EventType
from meshcore_essentials import connectToDeviceBLE, getContact

async def main():
    packetID = 0

    meshcore = connectToDeviceBLE("B93730B7-CA50-4718-2293-57AE6FF3348B") # Change as needed

    wantedContact = getContact(meshcore, "1057D6AD") # Change as needed
    
    # Send msg
    while packetID < 500:
        if wantedContact is not None:
            result = await meshcore.commands.send_msg(
                wantedContact, 
                str(packetID)
            )

            if result.type == EventType.ERROR:
                print("Error sending message")

            packetID += 1
        else:
            print("Could not find contact in question")

        await asyncio.sleep(5)

asyncio.run(main())