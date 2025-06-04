import pandas as pd

df = pd.read_csv('D:\Predictive_Safety_Monitoring_EV\data\ev_sensors_with_anomaly.csv')

# Define alert level function
def get_alert_level(row):
    if row['temperature_C'] > 80 or row['vibration_g'] > 0.35:
        return 'Critical'
    elif row['temperature_C'] > 70 or row['vibration_g'] > 0.3:
        return 'Warning'
    else:
        return 'Safe'

df['alert_level'] = df.apply(get_alert_level, axis=1)


df.to_csv('D:\Predictive_Safety_Monitoring_EV\data\ev_sensors_alerts.csv', index=False)


print("Alert levels added!")
print(df[['timestamp', 'temperature_C', 'vibration_g', 'anomaly', 'alert_level']].head(25))
