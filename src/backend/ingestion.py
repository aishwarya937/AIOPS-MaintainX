import json
import io
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from database import SessionLocal
from models import SensorData, Machine
from datetime import datetime
from minio import Minio
import redis

# --- CONFIGURATION ---
BROKER = "localhost"
TOPIC = "factory/machines/sensor_data"

# 1. CONNECT TO FREEZER (Data Lake / MinIO)
minio_client = Minio(
    endpoint="localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# 2. CONNECT TO COUNTER (Feature Store / Redis)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# --- THE CHEF'S LOGIC ---
def process_message(payload):
    # STEP A: Put in Freezer (MinIO)
    try:
        # Convert dict to JSON bytes
        json_data = json.dumps(payload).encode('utf-8')
        
        # Create a folder structure: tenant/machine/timestamp.json
        file_name = f"{payload['tenant_id']}/{payload['machine_id']}/{payload['timestamp']}.json"
        
        # Upload (FIXED: We now use named arguments bucket_name=, object_name=, etc.)
        minio_client.put_object(
            bucket_name="factory-data", 
            object_name=file_name,
            data=io.BytesIO(json_data),
            length=len(json_data),
            content_type="application/json"
        )
        print(f"☁️  MinIO: Saved {file_name}")
    except Exception as e:
        print(f"❌ MinIO Error: {e}")

    # STEP B: Put on Counter (Redis)
    try:
        # Key: "machine-001:latest" -> Value: The whole JSON
        redis_key = f"{payload['machine_id']}:latest"
        redis_client.set(redis_key, json.dumps(payload))
    except Exception as e:
        print(f"❌ Redis Error: {e}")

    # STEP C: Write in Log Book (Postgres)
    db = SessionLocal()
    try:
        # check if machine exists
        machine = db.query(Machine).filter(Machine.id == payload['machine_id']).first()
        if not machine:
            print("⚙️ Registering New Machine in DB...")
            new_machine = Machine(
                id=payload['machine_id'],
                tenant_id=payload['tenant_id'],
                name="Conveyor Belt",
                type="Rotary", 
                location="Floor 1"
            )
            db.add(new_machine)
            db.commit()

        # Save the reading
        reading = SensorData(
            tenant_id=payload['tenant_id'],
            machine_id=payload['machine_id'],
            timestamp=datetime.fromisoformat(payload['timestamp']),
            temperature=payload['temperature'],
            vibration=payload['vibration'],
            rpm=payload['rpm']
        )
        db.add(reading)
        db.commit()
        print("💾 DB: Saved Row")
            
    except Exception as e:
        print(f"❌ DB Error: {e}")
    finally:
        db.close()

# --- MQTT SETUP ---
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        process_message(payload)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = lambda c, u, f, rc: c.subscribe(TOPIC)
    client.on_message = on_message
    
    print("🚀 Enterprise Ingestion Service Started...")
    client.connect(BROKER, 1883, 60)
    client.loop_forever()