from flask import Flask, request

app = Flask(__name__)

# Store update location to be forwarded
currentLocation = {}

@app.route("/location", methods=["POST"])
def location():
    global currentLocation
    currentLocation = request.json

    return "OK"

app.run(host="0.0.0.0", port=8080)

