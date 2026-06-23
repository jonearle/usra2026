import asyncio
import time
from csv_write import csvWrite
from meshcore import MeshCore, EventType
from meshcore_essentials import connectToDeviceBLE, getContact

async def handleACK(event):
    receivedTime = time.time()
    payload = event.payload
    requestID = payload.get("code") 
    rssi = payload.get("rssi")
    snr = payload.get("snr")

    csvWrite(
        "/Users/Jon/usra2026/data/PlexToGB/5sec_ACK_MC.csv", 
        [requestID, receivedTime, rssi, snr]
        )   
    print(f"{requestID}, Data successfully written to CSV")

async def main():
    localID = 0

    meshcore = connectToDeviceBLE("B93730B7-CA50-4718-2293-57AE6FF3348B") # Change as needed

    wantedContact = getContact(meshcore, "1057D6AD") # Change as needed

    sub = meshcore.subscribe(EventType.ACK, handleACK)
    
    # Send msg
    while localID < 300:
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
