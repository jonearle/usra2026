import time
from flask import Flask, request

app = Flask(__name__)

# Location storage
currentLocation = {}

# Write to server with POST
@app.route("/location", methods=["POST"])
def updateLocation():
    global currentLocation
    packet = request.json

    if time.time() - packet['tst'] < 300:
        currentLocation = packet
        print(currentLocation)
        return "OK"

    return "Location is stale"

# Access server with GET
@app.route("/location", methods=["GET"])
def getLocation():
    return currentLocation

app.run(host="0.0.0.0", port=8080)

