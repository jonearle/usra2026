import asyncio
import time
from meshcore import MeshCore, EventType
from meshcore_essentials import connectToDeviceBLE, getContact

def getAirtimeMetrics(interface):
    data = interface.commands.get_stats_radio()

async def main():
    meshcore = connectToDeviceBLE("B93730B7-CA50-4718-2293-57AE6FF3348B") # Change as needed

    wantedContact = getContact(meshcore, "1057D6AD") # Change as needed

    # Get initial time (to keep track of every 5 minutes)
    airtimeClock = time.time()
    packetClock = time.time()

    '''
    # Send msg
    while True:
        if wantedContact is not None:
            
        else:
            print("Could not find contact in question")'''

asyncio.run(main())