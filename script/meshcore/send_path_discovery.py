import asyncio
import csv
import requests
import json
import inspect
from meshcore import MeshCore, EventType

async def main():
    # Connect to device
    # T-Beam v1.1 on MacOS = B93730B7-CA50-4718-2293-57AE6FF3348B
    # Ubuntu will always be /dev/ttyACM0
    try:
        meshcore = await MeshCore.create_ble('D4:D4:DA:DF:B8:D6')
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
    # LoRa32 = C53894B0
    # T-Beam = 584C7D9A
    for contact in contacts.payload.values():
        if contact["adv_name"] == "9AD878FD":
            wantedContact = contact
            break

    def handle_rx(event):
        print(event.payload)

    # Subscribe to radio log data
    meshcore.subscribe(EventType.RX_LOG_DATA,handle_rx)

    while True:
        # Send path discovery request
        if wantedContact is not None:
            result = await meshcore.commands.send_path_discovery_sync(
                wantedContact
            )
        else:
            print("Could not find contact in question")
            break

        if result is None:
            print("Result is none")
            await asyncio.sleep(10)
            continue

        rssi = result['rssi']
        snr = result['snr']
        path_len = result['path_len']
        path = result['path']

        # Open CSV file and write
        with open(
            "data/mesh_routing_test/test.csv", 
            "a", 
            newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow([rssi, snr, path_len, path])

        await asyncio.sleep(10)

asyncio.run(main())