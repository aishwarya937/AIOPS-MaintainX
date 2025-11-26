import pandas as pd
from sqlalchemy import create_engine, text

# 1. Setup Connection
# Note: Connecting to the Enterprise DB on port 5433
DATABASE_URL = "postgresql://admin:password123@127.0.0.1:5433/maintainx"
engine = create_engine(DATABASE_URL)

def export_dataset(tenant_id):
    print(f"🔄 Connecting to Database for Tenant: {tenant_id}...")
    
    # 2. SQL Query with Multi-Tenant Filter
    # We select only data belonging to the specific factory
    query = text("SELECT * FROM sensor_data WHERE tenant_id = :tid ORDER BY timestamp ASC")
    
    # 3. Load into Pandas
    print("📥 Downloading records...")
    df = pd.read_sql(query, engine, params={"tid": tenant_id})
    
    # 4. Validation
    if len(df) < 100:
        print("❌ ERROR: Not enough data! Did you run seed_data.py?")
        return

    print(f"📊 Loaded {len(df)} records for {tenant_id}.")
    
    # 5. Save to CSV
    output_file = "src/ai_engine/training_data.csv"
    df.to_csv(output_file, index=False)
    
    print(f"✅ SUCCESS: Dataset saved to '{output_file}'")
    print(df.head())

if __name__ == "__main__":
    # We specify which factory we are training for
    export_dataset("tesla-gigafactory")