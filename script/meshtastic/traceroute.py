from csv_write import csvWrite
import subprocess
import time
import re

def logToCSV(resultLog):
    # Get list of tokens where each one is either the node or the SNR
    tokens = []
    for line in resultLog.strip().split("\n"):
        if "traced towards" in line or "traced back" in line:
            continue    
        else:
            direction = [] # Each direction list is the tokens for that direction (forward or backward).
            nodes = line.split("-->")
            for node in nodes:
                matches = re.findall(r"![a-fA-F0-9]+|[-+]?\d+(?:\.\d+)?dB", node)
                for match in matches:
                    direction.append(match)
            tokens.append(direction)

    # Get path from tokens list and write to CSV
    for direction in tokens:
        path = direction[0] + ', ' + direction[1] + ', ' + direction[2] # First path is the first 3
        csvWrite("/Users/Jon/usra2026/data/traceroutes/goldberg.csv", path)
        for x in range(1, len(direction) - 3, 2): # rest of the paths
            fromNode = direction[x]
            toNode = direction[x + 2]
            snr = direction[x + 3]
            path = fromNode + ', ' + toNode + ', ' + snr
            csvWrite("/Users/Jon/usra2026/data/traceroutes/goldberg.csv", path)

def __main__():
    addresses = ['6c73daa0', 'dadfb0cc', 'dadfb6c8', 'dadfb008', 'dadfb03c', 'dadfb8d4']
    attempts = [0] * len(addresses)
    success = [0] * len(addresses)
    index = -1

    try:
        testName = input("Name of this test: \n")

        while True:
            index = (index + 1) % len(addresses)
            attempts[index] += 1

            # Run traceroute
            try:
                result = subprocess.run(["meshtastic", "--traceroute", addresses[index]], 
                                        capture_output=True, 
                                        text=True,
                                        timeout=30)
            except subprocess.TimeoutExpired:
                print("Subprocess timed out after 30 seconds")
                continue

            # Make sure traceroute was successful
            result = result.stdout
            isSuccessful = ("Route traced towards destination:" in result and "(?dB)" not in result)
            if not isSuccessful:
                print("Traceroute failed")
                time.sleep(30)
                continue
            print("Traceroute successful")

            # Convert logs into CSV data
            logToCSV(result)
            
            # Add to delivery rate counter and change address index
            success[index] += 1

            # Wait for cooldown
            time.sleep(30)
    finally:
        # Write summary metrics to txt file
        with open("/Users/Jon/usra2026/data/traceroutes/traceroute_logs.txt", "a") as file: 
            file.write(f"Test completed: {testName}\n\n")
            for index, address in enumerate(addresses):
                deliveryRate = (
                    success[index] / attempts[index] * 100
                    if attempts[index] > 0
                    else 0.0
                )

                file.write(f"Address: {address}\n")
                file.write(f"Attempted traceroutes: {attempts[index]}\n")
                file.write(f"Successful traceroutes: {success[index]}\n")
                file.write(f"Delivery rate: {deliveryRate:.2f}%\n\n")
            file.write("------------------------------------\n")

__main__()



    

                            