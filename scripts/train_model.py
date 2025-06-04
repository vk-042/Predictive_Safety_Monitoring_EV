import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib


df = pd.read_csv('D:\Predictive_Safety_Monitoring_EV\data\ev_sensors.csv')

# Drop non-numeric or label columns
X = df.drop(columns=['timestamp', 'status'])

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Isolation Forest
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(X_scaled)

# Save model and scaler
joblib.dump(model, 'D:\Predictive_Safety_Monitoring_EV\models\anomaly_model.pkl')
joblib.dump(scaler, 'D:\Predictive_Safety_Monitoring_EV\models\scaler.pkl')

df['anomaly'] = model.predict(X_scaled)
df['anomaly'] = df['anomaly'].map({1: 'Normal', -1: 'Anomaly'})  # Predict anomalies (-1 = anomaly, 1 = normal)

df.to_csv('D:\Predictive_Safety_Monitoring_EV\data\ev_sensors_with_anomaly.csv', index=False)

print("Model trained and saved successfully!")
print(df['anomaly'].value_counts())
