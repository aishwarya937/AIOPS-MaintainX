from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from database import Base

# Table 1: Machines
class Machine(Base):
    __tablename__ = "machines"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Table 2: Sensor Readings (IoT Data)
class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    machine_id = Column(String, ForeignKey("machines.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    vibration = Column(Float)
    rpm = Column(Float)

# Table 3: AI Predictions
class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    machine_id = Column(String, ForeignKey("machines.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    failure_prob = Column(Float)
    is_anomaly = Column(Boolean, default=False)