from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from database import Base

# --- TENANT MIXIN (Reusable Code) ---
# Every table will now inherit this, automatically getting a tenant_id
class TenantMixin:
    tenant_id = Column(String, nullable=False, default="default-tenant")

# 1. Machine Table (Now with Tenant ID)
class Machine(Base, TenantMixin):
    __tablename__ = "machines"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# 2. Sensor Data Table (Now with Tenant ID)
class SensorData(Base, TenantMixin):
    __tablename__ = "sensor_data"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    machine_id = Column(String, ForeignKey("machines.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    vibration = Column(Float)
    rpm = Column(Float)

# 3. Predictions Table (Now with Tenant ID)
class Prediction(Base, TenantMixin):
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    machine_id = Column(String, ForeignKey("machines.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    failure_prob = Column(Float)
    is_anomaly = Column(Boolean, default=False)