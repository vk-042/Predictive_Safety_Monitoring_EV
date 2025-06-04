import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('D:\Predictive_Safety_Monitoring_EV\data\ev_sensors_alerts.csv')

# Plot count of each alert level
sns.set(style='whitegrid')
sns.countplot(x='alert_level', data=df, palette='Set2')

plt.title('Alert Level Distribution')
plt.xlabel('Alert Level')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
