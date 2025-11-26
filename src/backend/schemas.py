from pydantic import BaseModel, Field
from datetime import datetime

class SensorPayload(BaseModel):
    tenant_id: str
    machine_id: str
    timestamp: str
    temperature: float = Field(..., ge=-50, le=200) # Temp must be between -50 and 200
    vibration: float = Field(..., ge=0)             # Vibration cannot be negative
    rpm: int = Field(..., ge=0)                     # RPM cannot be negative