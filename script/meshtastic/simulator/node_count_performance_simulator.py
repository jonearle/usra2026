import subprocess

num_nodes_list = [3, 5, 8, 10, 12, 15, 20, 30, 50, 75, 100] 
repeitions = 20

for num_nodes in num_nodes_list:
    for i in range(0, repeitions):
        subprocess.run([
            "python", 
            "/Users/Jon/Meshtasticator-GeoJSON/loraMesh.py", 
            "--polygon", str(num_nodes), "--no-gui"
            ],
            cwd="/Users/Jon/Meshtasticator-GeoJSON",
            check=True)


