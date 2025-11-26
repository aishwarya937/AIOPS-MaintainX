import json
import io
import logging
import paho.mqtt.client as mqtt
from database import SessionLocal
from models import SensorData, Machine
from datetime import datetime
from minio import Minio
import redis
from schemas import SensorPayload # <--- The Validator

# --- LOGGING SETUP (Enterprise Standard) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system.log"), # Save to file
        logging.StreamHandler()            # Print to terminal
    ]
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
BROKER = "localhost"
TOPIC = "factory/machines/sensor_data"

# 1. CONNECT TO MINIO
minio_client = Minio(
    endpoint="localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# 2. CONNECT TO REDIS
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def process_message(payload):
    # --- STEP 0: VALIDATION ---
    try:
        # This checks if data format is correct. If not, it raises an error.
        validated_data = SensorPayload(**payload)
    except Exception as e:
        logger.error(f"❌ Invalid Data Format: {e}")
        return

    # --- STEP A: MINIO (Data Lake) ---
    try:
        json_data = json.dumps(payload).encode('utf-8')
        file_name = f"{payload['tenant_id']}/{payload['machine_id']}/{payload['timestamp']}.json"
        
        minio_client.put_object(
            bucket_name="factory-data",
            object_name=file_name,
            data=io.BytesIO(json_data),
            length=len(json_data),
            content_type="application/json"
        )
        logger.info(f"☁️  MinIO: Saved {file_name}")
    except Exception as e:
        logger.error(f"❌ MinIO Error: {e}")

    # --- STEP B: REDIS (Cache) ---
    try:
        redis_key = f"{payload['machine_id']}:latest"
        redis_client.set(redis_key, json.dumps(payload))
    except Exception as e:
        logger.error(f"❌ Redis Error: {e}")

    # --- STEP C: POSTGRES (DB) ---
    db = SessionLocal()
    try:
        machine = db.query(Machine).filter(Machine.id == payload['machine_id']).first()
        if not machine:
            logger.warning(f"⚙️ New Machine Detected: {payload['machine_id']}")
            new_machine = Machine(
                id=payload['machine_id'],
                tenant_id=payload['tenant_id'],
                name="Conveyor Belt",
                type="Rotary", 
                location="Floor 1"
            )
            db.add(new_machine)
            db.commit()

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
        logger.info("💾 DB: Saved Row")
            
    except Exception as e:
        logger.error(f"❌ DB Error: {e}")
    finally:
        db.close()

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        process_message(payload)
    except Exception as e:
        logger.error(f"Message Error: {e}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = lambda c, u, f, rc: c.subscribe(TOPIC)
    client.on_message = on_message
    
    logger.info("🚀 Enterprise Ingestion Service Started...")
    client.connect(BROKER, 1883, 60)
    client.loop_forever()