from sqlalchemy import func
from database import SessionLocal
from models import SensorData, Machine

def check_db():
    db = SessionLocal()
    try:
        # 1. Count Total Rows
        row_count = db.query(SensorData).count()
        print(f"\n📊 TOTAL RECORDS IN DB: {row_count}")

        # 2. Show the latest 5 readings
        print("\n🔍 LATEST 5 READINGS:")
        readings = db.query(SensorData).order_by(SensorData.timestamp.desc()).limit(5).all()
        
        for r in readings:
            print(f"   🕒 {r.timestamp} | 🌡️ Temp: {r.temperature}°C | 〰️ Vib: {r.vibration}")

        # 3. Check Machines
        machine_count = db.query(Machine).count()
        print(f"\n🏭 MACHINES REGISTERED: {machine_count}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db()