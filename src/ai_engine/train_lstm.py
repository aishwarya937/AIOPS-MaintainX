import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

TENANT_ID = "tesla-gigafactory"
MODEL_PATH = f"src/ai_engine/model_lstm_{TENANT_ID}.h5"
SCALER_PATH = f"src/ai_engine/scaler_{TENANT_ID}.pkl"

print("📂 Loading Data...")
df = pd.read_csv("src/ai_engine/training_data.csv")
data = df[['temperature']].values

# 1. Scale Data (LSTM needs data between 0 and 1)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# 2. Create Sequences (Look back 10 steps to predict next 1)
X, y = [], []
look_back = 10
for i in range(look_back, len(scaled_data)):
    X.append(scaled_data[i-look_back:i, 0])
    y.append(scaled_data[i, 0])

X, y = np.array(X), np.array(y)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# 3. Build LSTM Model
print("🧠 Building LSTM...")
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')

# 4. Train
print("🏋️ Training LSTM (This may take a moment)...")
model.fit(X, y, epochs=5, batch_size=32)

# 5. Save
print("💾 Saving LSTM Model & Scaler...")
model.save(MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)
print("🎉 LSTM Training Complete!")
