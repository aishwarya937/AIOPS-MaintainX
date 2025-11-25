import time
import json
import random
import paho.mqtt.client as mqtt
from datetime import datetime

# --- CONFIGURATION ---
BROKER = "localhost"   # The Docker address
PORT = 1883            # The MQTT Port (Standard)
TOPIC = "factory/machines/sensor_data"
MACHINE_ID = "machine-001"

# --- CALLBACKS ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connected to MQTT Broker at {BROKER}:{PORT}")
    else:
        print(f"❌ Failed to connect, return code {rc}")

# --- MAIN SETUP ---
client = mqtt.Client()
client.on_connect = on_connect

print(f"🚀 Connecting to Broker {BROKER}...")
try:
    client.connect(BROKER, PORT, 60)
except Exception as e:
    print(f"❌ Connection Error: {e}")
    print("Is Docker running? Is the MQTT container up?")
    exit()

# Start background thread to handle network
client.loop_start()

print("🏭 IoT Simulator Started. Press Ctrl+C to stop.")

# --- DATA LOOP ---
try:
    while True:
        # 1. Generate Fake Data
        payload = {
            "machine_id": MACHINE_ID,
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": round(random.uniform(50.0, 90.0), 2),  # Random temp 50-90
            "vibration": round(random.uniform(0.0, 5.0), 2),      # Random vibration 0-5
            "rpm": random.randint(1000, 3000)                     # Random RPM
        }

        # 2. Convert to JSON
        message = json.dumps(payload)

        # 3. Publish to Topic
        client.publish(TOPIC, message)
        
        print(f"📤 Sent: {message}")
        
        # 4. Wait 2 seconds
        time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 Stopping Simulator...")
    client.loop_stop()
    client.disconnect()