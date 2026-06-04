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
    
    # Send msg
    if wantedContact is not None:
        result = await meshcore.commands.send_msg(
            wantedContact, 
            "test"
        )
        if result.type == EventType.ERROR:
            print("Error sending message")
    else:
        print("Could not find contact in question")

    await meshcore.disconnect()

asyncio.run(main())