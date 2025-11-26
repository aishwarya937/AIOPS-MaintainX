from database import engine, Base
from models import Machine, SensorData, Prediction

def init_db():
    print("🚀 Connecting to Docker Database...")
    try:
        # This command translates Python classes to SQL "CREATE TABLE" commands
        Base.metadata.create_all(bind=engine)
        print("✅ SUCCESS: All tables (Machines, SensorData, Predictions) created!")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    init_db()
    
    
