import json
import joblib
import pandas as pd
import paho.mqtt.client as mqtt
import numpy as np

# --- CONFIGURATION ---
BROKER = "localhost"
TOPIC = "factory/machines/sensor_data"
TENANT_ID = "tesla-gigafactory"

# --- LOAD MODELS ---
print("🧠 Loading AI Models...")
try:
    # Load Random Forest (Failure Classifier)
    rf_model = joblib.load(f"src/ai_engine/model_{TENANT_ID}.pkl")
    # Load Isolation Forest (Anomaly Detector)
    iso_model = joblib.load(f"src/ai_engine/model_anomaly_{TENANT_ID}.pkl")
    print("✅ Models Loaded Successfully!")
except FileNotFoundError:
    print("❌ Error: Models not found. Did you run train_model.py and train_anomaly.py?")
    exit()

# --- PREDICTION ENGINE ---
def analyze_data(payload):
    # 1. Prepare Data (Must match training format)
    # Create a DataFrame with one row
    data = pd.DataFrame([{
        'temperature': payload['temperature'],
        'vibration': payload['vibration'],
        'rpm': payload['rpm']
    }])

    # 2. Run Failure Prediction (Random Forest)
    # Returns [0] for Normal, [1] for Failure
    fail_pred = rf_model.predict(data)[0]
    
    # Get probability (Confidence level)
    # predict_proba returns [[prob_normal, prob_failure]]
    fail_prob = rf_model.predict_proba(data)[0][1] 

    # 3. Run Anomaly Detection (Isolation Forest)
    # Returns [1] for Normal, [-1] for Anomaly
    anomaly_pred = iso_model.predict(data)[0]

    # 4. PRINT RESULTS
    timestamp = payload['timestamp'].split('T')[1][:8] # Just get HH:MM:SS
    
    status = "🟢 NORMAL"
    if fail_pred == 1:
        status = "🔴 FAILURE PREDICTED!"
    elif anomaly_pred == -1:
        status = "⚠️ ANOMALY DETECTED"

    print(f"[{timestamp}] Machine: {payload['machine_id']} | {status}")
    print(f"   🌡️ Temp: {payload['temperature']} | 〰️ Vib: {payload['vibration']}")
    
    if fail_prob > 0.5:
        print(f"   🚨 Failure Probability: {fail_prob*100:.1f}%")
    print("-" * 40)

# --- MQTT SETUP ---
def on_connect(client, userdata, flags, rc):
    print(f"📡 Connected to MQTT Broker. Listening for {TENANT_ID}...")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        # Only analyze data for our tenant
        if payload.get("tenant_id") == TENANT_ID:
            analyze_data(payload)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.loop_forever()