# 🏛 SYSTEM DESIGN: AIOPS-MaintainX

## 1. High-Level Architecture
Data flows from Left (Edge) to Right (Dashboard).

```text
[ EDGE LAYER ]          [ CLOUD/BACKEND LAYER ]                  [ USER LAYER ]
+-------------+         +----------------+    +-------------+    +------------+
|  IoT Client | ------> |  MQTT Broker   | -> |  Ingestion  | -> |     DB     |
| (Simulator) |  (Pub)  |  (Mosquitto)   |    |  Service    |    | (Postgres) |
+-------------+         +----------------+    +-------------+    +------------+
                                                     |
                                                     v
                                              +-------------+
                                              |  AI Engine  |
                                              | (Prediction)|
                                              +-------------+
                                                     |
                                                     v
                                              +-------------+    +------------+
                                              | API Service | -> | React App  |
                                              |  (FastAPI)  |    | (Dashboard)|
                                              +-------------+    +------------+

2. Database Schema (PostgreSQL)
We need 4 main tables.
🏭 Table: machines
Stores info about the factory equipment.
id (PK): UUID
name: String (e.g., "Conveyor Belt Motor")
type: String (e.g., "Rotary")
location: String (e.g., "Floor 1")
created_at: Timestamp
📡 Table: sensor_data
Stores the raw IoT readings (Huge table).
id (PK): UUID
machine_id (FK): Link to machines table
timestamp: DateTime
temperature: Float
vibration: Float
rpm: Float
🧠 Table: predictions
Stores what the AI thinks.
id (PK): UUID
machine_id (FK): Link to machines table
timestamp: DateTime
failure_prob: Float (0.0 to 1.0)
is_anomaly: Boolean
🎫 Table: maintenance_tickets
Stores the work for technicians.
id (PK): UUID
machine_id (FK): Link to machines table
title: String (e.g., "High Vibration Alert")
status: Enum ("OPEN", "IN_PROGRESS", "RESOLVED")
priority: Enum ("LOW", "HIGH", "CRITICAL")
technician_id: String (Assigned User)