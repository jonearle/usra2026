import subprocess

nodes = ["!6c73daa0", '!dadfb0cc']

for node in nodes:
    result = subprocess.run(["meshtastic", "--dest", node, "--request-telemetry"])