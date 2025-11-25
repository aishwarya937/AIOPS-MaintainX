import json
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from database import SessionLocal
from models import SensorData, Machine
from datetime import datetime

# --- CONFIGURATION ---
BROKER = "localhost"
PORT = 1883
TOPIC = "factory/machines/sensor_data"

# --- DATABASE HELPERS ---
def save_to_db(payload):
    db = SessionLocal()
    try:
        # 1. Ensure Machine Exists (Foreign Key Check)
        machine_id = payload['machine_id']
        machine = db.query(Machine).filter(Machine.id == machine_id).first()
        
        if not machine:
            print(f"⚙️ First time seeing {machine_id}. Registering it...")
            new_machine = Machine(
                id=machine_id, 
                name="Conveyor Belt Motor", 
                type="Rotary", 
                location="Floor 1"
            )
            db.add(new_machine)
            db.commit()

        # 2. Save the Sensor Reading
        reading = SensorData(
            machine_id=machine_id,
            timestamp=datetime.fromisoformat(payload['timestamp']),
            temperature=payload['temperature'],
            vibration=payload['vibration'],
            rpm=payload['rpm']
        )
        db.add(reading)
        db.commit()
        print(f"💾 Saved: {payload['temperature']}°C | {payload['vibration']}mm/s")
        
    except Exception as e:
        print(f"❌ Database Error: {e}")
    finally:
        db.close()

# --- MQTT CALLBACKS ---
def on_connect(client, userdata, flags, rc):
    print(f"✅ Ingestion Service Connected to MQTT (Result: {rc})")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        # Decode the JSON message
        payload = json.loads(msg.payload.decode())
        # Save it
        save_to_db(payload)
    except Exception as e:
        print(f"❌ Error processing message: {e}")

# --- MAIN LOOP ---
if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    print("🎧 Ingestion Service Started. Waiting for data...")
    client.connect(BROKER, PORT, 60)
    client.loop_forever()