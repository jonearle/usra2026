import asyncio
import csv
import requests
import json
import time
from meshcore import MeshCore, EventType

def csvWrite(path, data):
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

async def connectBLE(bleAddress):
    # Connect to device
    # T-Beam v1.1 on MacOS = B93730B7-CA50-4718-2293-57AE6FF3348B
    # Ubuntu will always be /dev/ttyACM0
    try:
        iface = await MeshCore.create_ble(bleAddress)
    except ConnectionError:
        print("Failed to connect")
        return
    if iface is None:
        print("Failed to connect")
        return
    print("Device successfully connected")

    return iface

# Returns 1 if message was successfully sent, 0 if failed
async def sendPayload(interface, payload, contactInfo):
    # Send message (to forces contact update)
    result = await interface.commands.send_msg(
        contactInfo, 
        json.dumps(payload)
    )
    if result is None:
        print("Failed to send payload")
        return 0
    else:
        print("Sent payload successfully")
        return 1

# Obtains GPS data from web server
async def getGPSData():
    # Get location
    try:
        location = requests.get("http://localhost:8080/location").json()
    except Exception as e:
        print(f"GPS Error: {e}")
        await asyncio.sleep(5)
        return None

    gpsData = {
        "lat": location['lat'],
        "lon": location['lon'],
        "alt": location['alt']
    }
    
    return gpsData

# Function will find the contact in question 
# and in doing so will give the routing details as
# routes are stored in the receiver's contact info instead of the message
async def contactLookupPathUpdate(interface, contactName):
    # Get contacts
    # The path is stored in the contact - we need to send messages to force the path to be updated while mobile
    contacts = await interface.commands.get_contacts()
    if contacts.type == EventType.ERROR:
        print("Error getting contacts")
        return
    
    # Find contact and update path into
    # Contacts = 9AD87FD, 1057D6AD
    wantedContact = None
    for contact in contacts.payload.values():
        if contact["adv_name"] == contactName:
            wantedContact = contact
            break
    
    return wantedContact

async def main():
    # Connect to device via bluetooth
    meshcore = await connectBLE('B93730B7-CA50-4718-2293-57AE6FF3348B')
    if meshcore is None:
        return

    # Find initial contact
    contactInfo = await contactLookupPathUpdate(meshcore, "1057D6AD")

    # Track sent messages for delivery rate
    packetID = 0

    while True:
        timestamp = time.time()

        # Get location
        payload = await getGPSData()
        if payload == None:
            continue
        
        # Assign packet id
        payload["packetID"] = packetID
        
        # Send message containing GPS data
        success = 0
        success += await sendPayload(meshcore, payload, contactInfo)
        if success != 0:
            packetID += 1

        await asyncio.sleep(1)

        # Obtain updated contact/path info
        contactInfo = await contactLookupPathUpdate(meshcore, "1057D6AD")

        # Set data
        path_len = contactInfo['out_path_len']
        path = contactInfo['out_path']
        lastmod = contactInfo['lastmod']
        lat = payload["lat"]
        lon = payload["lon"]
        alt = payload["alt"]

        data = [timestamp, payload["packetID"], path_len, path, lastmod, lat, lon, alt]

        # Open CSV file and write
        csvWrite("/Users/Jon/USRA2026/data/desk.csv", data)

        await asyncio.sleep(10)

asyncio.run(main())