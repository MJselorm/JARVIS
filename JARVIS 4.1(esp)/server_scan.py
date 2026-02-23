import subprocess
import re

TARGET_MAC = "94-54-c5-b7-06-54".lower()

# Run arp command
result = subprocess.check_output("arp -a", shell=True).decode()

# Split into lines
lines = result.splitlines()

esp_ip = None

for line in lines:
    line = line.lower()
    if TARGET_MAC in line:
        # Extract IP address using regex
        match = re.search(r"\d+\.\d+\.\d+\.\d+", line)
        if match:
            esp_ip = match.group()
            break

if esp_ip:
    print("ESP32 IP Found:", esp_ip)
else:
    print("Device not found")
    
# Save the IP address to a file for later use