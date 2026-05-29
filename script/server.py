from flask import Flask, request

app = Flask(__name__)

# Location storage
currentLocation = {}

# Write to server with POST
@app.route("/location", methods=["POST"])
def updateLocation():
    global currentLocation
    currentLocation = request.json

    print(currentLocation)

    return "OK"

# Access server with GET
@app.route("/location", methods=["GET"])
def getLocation():
    return currentLocation

app.run(host="0.0.0.0", port=8080)

