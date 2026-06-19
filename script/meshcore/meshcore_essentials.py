import asyncio
from meshcore import MeshCore, EventType

# Connect to meshcore device via bluetooth
async def connectToDeviceBLE(macAddress):
    try:
        meshcore = await MeshCore.create_ble( macAddress)
    except ConnectionError:
        print("Failed to connect")
        return None
    if meshcore is None:
        print("Failed to connect")
        return None
    print("Device successfully connected")
    return meshcore

# Get a specific contact from a meshcore device
# Get name from CLI
async def getContact(name, interface):
    wantedContact = None
    contacts = await interface.commands.get_contacts()
    if contacts.type == EventType.ERROR:
        print("Error getting contacts")
        return None
    
    for contact in contacts.payload.values():
        if contact["adv_name"] == name:
            return wantedContact