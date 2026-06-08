import asyncio
import csv
import json
from meshcore import MeshCore, EventType
from meshcoredecoder import MeshCoreDecoder
from meshcoredecoder.types.enums import PayloadType

async def main():
    # Connect to device via bluetooth
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

    # Subscribe to raw data events
    def handle_packet(event):
        try:
            raw_hex = event.payload['payload']
            
            packet = MeshCoreDecoder.decode(raw_hex)

            if (
                packet.payload_type == PayloadType.Trace 
                and packet.payload.get('decoded')
            ):
                trace = packet.payload['decoded']
                print(trace.get_path_with_snr())

        except Exception as e:
            print(f"Error: {e}")

    meshcore.subscribe(EventType.RX_LOG_DATA, handle_packet)

    while True:
        await asyncio.sleep(1)

asyncio.run(main())