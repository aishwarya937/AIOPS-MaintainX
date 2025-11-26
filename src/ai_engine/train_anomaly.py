import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

# Configuration
TENANT_ID = "tesla-gigafactory"
MODEL_PATH = f"src/ai_engine/model_anomaly_{TENANT_ID}.pkl"

# 1. Load Data
print(f"📂 Loading dataset for {TENANT_ID}...")
try:
    df = pd.read_csv("src/ai_engine/training_data.csv")
except FileNotFoundError:
    print("❌ Error: CSV not found.")
    exit()

# 2. Select Features
# Anomaly detection doesn't need labels (y), only features (X)
features = ['temperature', 'vibration', 'rpm']
X = df[features]

# 3. Train Isolation Forest
# contamination=0.05 means we expect about 5% of data to be anomalies (glitches)
print("👻 Training Isolation Forest (Anomaly Detector)...")
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(X)

# 4. Test it immediately
# -1 means Anomaly, 1 means Normal
df['anomaly'] = model.predict(X)
anomalies = df[df['anomaly'] == -1]

print(f"📊 Analysis Complete:")
print(f"   Total Records: {len(df)}")
print(f"   Anomalies Found: {len(anomalies)}")
print("\nExample Anomalies Detected:")
print(anomalies.head())

# 5. Save the Model
print(f"💾 Saving model to '{MODEL_PATH}'...")
joblib.dump(model, MODEL_PATH)
print("🎉 Done!")