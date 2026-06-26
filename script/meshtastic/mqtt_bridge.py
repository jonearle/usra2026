import json
import meshtastic.serial_interface
import paho.mqtt.client as mqtt
from pubsub import pub

def onReceive(packet, interface):
    try:
        payload = json.dumps(packet)
        client.publish("meshtastic/packets", payload)
    except Exception:
        print("Error:", Exception)

client = mqtt.Client()
client.connect("localhost", 8080)

iface = meshtastic.serial_interface.SerialInterface()
print("Connected to " + str(iface.getLongName()))

pub.subscribe(onReceive, "meshtastic.receive")



