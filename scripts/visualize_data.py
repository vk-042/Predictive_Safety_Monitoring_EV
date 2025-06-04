import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('D:\Predictive_Safety_Monitoring_EV\data\ev_sensors.csv', parse_dates=['timestamp'])


# Set style
sns.set(style='whitegrid')

# Plot 1: Temperature Over Time
plt.figure(figsize=(12, 5))
sns.lineplot(x='timestamp', y='temperature_C', data=df)
plt.title('Temperature Over Time')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 2: Vibration Over Time
plt.figure(figsize=(12, 5))
sns.lineplot(x='timestamp', y='vibration_g', data=df)
plt.title('Vibration Over Time')
plt.xlabel('Time')
plt.ylabel('Vibration (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 3: Voltage Over Time
plt.figure(figsize=(12, 5))
sns.lineplot(x='timestamp', y='voltage_V', data=df)
plt.title('Voltage Over Time')
plt.xlabel('Time')
plt.ylabel('Voltage (V)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 4: Status Distribution
plt.figure(figsize=(6, 5))
sns.countplot(x='status', data=df)
plt.title('Normal vs Faulty Status Count')
plt.tight_layout()
plt.show()


