import meshtastic
import meshtastic.ble_interface
from pubsub import pub
import pprint

iFace = meshtastic.ble_interface.BLEInterface(address="CFCE6566-57CF-6F07-12E8-2A9C44129E5D")

def onReceive(packet, interface):
    pprint.pprint(packet)

pub.subscribe(onReceive, "meshtastic.receive")

input("Listening for packets...")