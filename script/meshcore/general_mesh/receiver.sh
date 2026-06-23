cd ~
cd usra2026/script/meshcore/general_mesh

sudo systemctl restart systemd-timesyncd
python3 receiver.py