import random
from datetime import datetime, timedelta
from database import SessionLocal
from models import Machine, SensorData

# Configuration
TOTAL_RECORDS = 5000
MACHINE_ID = "machine-001"
TENANT_ID = "tesla-gigafactory" # <--- The new requirement

def generate_history():
    db = SessionLocal()
    print(f"🚀 Generating {TOTAL_RECORDS} records for {TENANT_ID}...")

    try:
        # 1. Ensure Machine Exists
        machine = db.query(Machine).filter(Machine.id == MACHINE_ID).first()
        if not machine:
            new_machine = Machine(
                id=MACHINE_ID, 
                tenant_id=TENANT_ID,
                name="Conveyor Belt", 
                type="Rotary", 
                location="Floor 1"
            )
            db.add(new_machine)
            db.commit()

        # 2. Generate Data loop
        data_buffer = []
        start_time = datetime.utcnow() - timedelta(days=30)

        for i in range(TOTAL_RECORDS):
            current_time = start_time + timedelta(minutes=10 * i)
            
            # Simulate "Normal" behavior
            temp = round(random.uniform(55.0, 75.0), 2)
            vib = round(random.uniform(0.5, 3.0), 2)
            rpm = random.randint(1400, 1600)

            # Simulate "Glitch" (Anomaly) every 100th record
            if i % 100 == 0:
                temp += random.uniform(20.0, 30.0)
                vib += random.uniform(2.0, 5.0)

            record = SensorData(
                tenant_id=TENANT_ID, # <--- Saving the Tenant
                machine_id=MACHINE_ID,
                timestamp=current_time,
                temperature=temp,
                vibration=vib,
                rpm=rpm
            )
            data_buffer.append(record)

            # Save in chunks
            if len(data_buffer) >= 500:
                db.add_all(data_buffer)
                db.commit()
                data_buffer = []
                print(f"   Saved {i} records...")

        if data_buffer:
            db.add_all(data_buffer)
            db.commit()

        print("✅ SUCCESS: Historical data generated!")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_history()