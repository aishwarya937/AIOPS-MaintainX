import time
import json
import random
import paho.mqtt.client as mqtt
from datetime import datetime

# --- CONFIGURATION ---
BROKER = "localhost"
PORT = 1883
TOPIC = "factory/machines/sensor_data"
MACHINE_ID = "machine-001"
# NEW: We identify which factory this is (Multi-Tenancy)
TENANT_ID = "tesla-gigafactory" 

# --- CONNECT TO THE WAITER (MQTT) ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connected to Broker. Sending data for {TENANT_ID}...")
    else:
        print(f"❌ Failed to connect, return code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

print(f"🏭 Simulator Started: {TENANT_ID} - {MACHINE_ID}")

try:
    while True:
        # 1. Create the Order (The Data)
        payload = {
            "tenant_id": TENANT_ID,       # <--- The New Tag
            "machine_id": MACHINE_ID,
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": round(random.uniform(50.0, 90.0), 2),
            "vibration": round(random.uniform(0.0, 5.0), 2),
            "rpm": random.randint(1000, 3000)
        }

        # 2. Hand it to the Waiter (Publish)
        message = json.dumps(payload)
        client.publish(TOPIC, message)
        
        print(f"📤 Sent: {message}")
        time.sleep(2) # Wait 2 seconds

except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()