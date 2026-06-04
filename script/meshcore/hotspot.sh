while true; do
    ping -c 1 8.8.8.8 || echo "Hotspot Connection Lost"
    sleep 15
done