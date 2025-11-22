# Data Model Hierarchy

We will follow a hierarchical "Tenant" structure.

1. **Organization** (The Company, e.g., "Tesla")
   └── 2. **Factory** (Physical Location, e.g., "Giga Texas")
       └── 3. **Production Line** (Section, e.g., "Assembly Line A")
           └── 4. **Machine** (The Asset, e.g., "Robotic Arm #5")
               └── 5. **Sensor** (The Input, e.g., "Vibration Sensor X")
                   └── 6. **Telemetry Data** (The Values: Timestamp, Value, Unit)

## Unique Identifiers (IDs)
Every piece of data will need these tags:
- `org_id`
- `factory_id`
- `machine_id`
- `sensor_id`
