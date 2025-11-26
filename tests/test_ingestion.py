import sys
import os
# Allow python to find the backend folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backend')))

from models import SensorData
from datetime import datetime

def test_data_structure():
    """
    Test if our Data Model handles Multi-Tenancy correctly.
    """
    print("🧪 Testing SensorData Model...")
    
    reading = SensorData(
        tenant_id="test-factory",
        machine_id="test-machine",
        timestamp=datetime.utcnow(),
        temperature=65.5,
        vibration=2.1,
        rpm=1500
    )

    assert reading.tenant_id == "test-factory"
    assert reading.temperature == 65.5
    print("✅ Unit Test Passed: Data Model is valid.")

if __name__ == "__main__":
    test_data_structure()