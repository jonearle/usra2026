import asyncio
import requests
import json
from meshcore import MeshCore, EventType

async def main():
    # Connect to device
    # T-Beam v1.1 on MacOS = B93730B7-CA50-4718-2293-57AE6FF3348B
    # Ubuntu will always be /dev/ttyACM0
    try:
        meshcore = await MeshCore.create_serial('/dev/ttyACM0')
    except ConnectionError:
        print("Failed to connect")
        return
    if meshcore is None:
        print("Failed to connect")
        return
    print("Device successfully connected")

    # Get contacts
    wantedContact = None
    contacts = await meshcore.commands.get_contacts()
    if contacts.type == EventType.ERROR:
        print("Error getting contacts")
        return
    
    # Find contact: change name where needed
    # Can find adv_name with meshcli
    for contact in contacts.payload.values():
        if contact["adv_name"] == "C53894B0":
            wantedContact = contact
            break

    while True:
        # Get location
        try:
            location = requests.get("http://localhost:8080/location").json()
        except Exception as e:
            print(f"GPS Error: {e}")
            await asyncio.sleep(10)
            continue

        payload = {
            "lat": location['lat'],
            "long": location['lon'],
            "alt": location['alt']
        }

        # Send msg
        if wantedContact is not None:
            result = await meshcore.commands.send_binary_req(
                wantedContact, 
                json.dumps(payload).encode('utf-8')
            )
            print(result) # for initial debug
            if result.type == EventType.ERROR:
                print("Error sending message")
        else:
            print("Could not find contact in question")

        asyncio.sleep(10)

asyncio.run(main())