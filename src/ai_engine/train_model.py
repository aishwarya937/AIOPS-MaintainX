import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Configuration
TENANT_ID = "tesla-gigafactory"
MODEL_PATH = f"src/ai_engine/model_{TENANT_ID}.pkl"

print(f"📂 Loading dataset for {TENANT_ID}...")
try:
    df = pd.read_csv("src/ai_engine/training_data.csv")
except FileNotFoundError:
    print("❌ Error: CSV not found.")
    exit()

print("🏷️  Labeling data...")
df['failure'] = 0
df.loc[(df['temperature'] > 80) | (df['vibration'] > 4.0), 'failure'] = 1

features = ['temperature', 'vibration', 'rpm']
X = df[features]
y = df['failure']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- HYPERPARAMETER TUNING (Grid Search) ---
print("🔍 Starting Hyperparameter Tuning (Grid Search)...")
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5]
}

rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

print(f"🏆 Best Parameters Found: {grid_search.best_params_}")

# Use the best model
best_model = grid_search.best_estimator_

print("📊 Evaluating Best Model...")
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")

print(f"💾 Saving model to '{MODEL_PATH}'...")
joblib.dump(best_model, MODEL_PATH)
print("🎉 Done!")