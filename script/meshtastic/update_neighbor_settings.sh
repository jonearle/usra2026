cd ~
cd usra2026
source venv/bin/activate

meshtastic --set neighbor_info.enabled true
sleep 15

meshtastic --set neighbor_info.update_interval 300
sleep 15

meshtastic --set neighbor_info.transmit_over_lora true
sleep 15

meshtastic --info
