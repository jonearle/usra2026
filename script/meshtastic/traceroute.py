from csv_write import csvWrite
import subprocess
import re
import time

destinationAddress = "!dadfb0cc"
trID = 0

while True:
    trID += 1

    # Run traceroute
    try:
        result = subprocess.run(["meshtastic", "--traceroute", destinationAddress], 
                                capture_output=True, 
                                text=True,
                                timeout=30)
    except subprocess.TimeoutExpired:
        print("Subprocess timed out after 30 seconds")
        continue

    # Make sure traceroute was successful
    result = result.stdout
    success = ("Route traced towards destination:" in result)
    if not success:
        print("Traceroute failed")
        break

    # Clean output for route
    route = re.findall(r'!\w+', result)
    snrs = re.findall(r'\(([\d.-]+)', result)
    route.pop(0)
    route = list(dict.fromkeys(route))
    snrs = forward_snrs = snrs[:len(snrs)//2]

    # Get route length
    routeLength = len(route) - 1

    # Turn route/snrs into string for csv
    route = ",".join(route)
    snrs = ",".join(snrs)

    csvWrite("/Users/Jon/USRA2026/data/desk.csv", [trID, route, routeLength, snrs])

    print("Traceroute successful")

    # Wait for cooldown
    time.sleep(31)




    

                            