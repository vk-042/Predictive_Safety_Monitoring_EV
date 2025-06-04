import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title(" Predictive Safety Monitoring for EV Dashboard")

df = pd.read_csv('D:\Predictive_Safety_Monitoring_EV\data\ev_sensors_alerts.csv')

# Sidebar filters
st.sidebar.header("Filter by Alert Level")
alert_filter = st.sidebar.multiselect("Select alert levels:", options=df['alert_level'].unique(), default=df['alert_level'].unique())

filtered_df = df[df['alert_level'].isin(alert_filter)] # Apply filter

temp_min, temp_max = st.sidebar.slider(
    "Temperature Range (°C)",
    min_value=float(df['temperature_C'].min()),
    max_value=float(df['temperature_C'].max()),
    value=(float(df['temperature_C'].min()), float(df['temperature_C'].max()))
)
filtered_df = filtered_df[
    (filtered_df['temperature_C'] >= temp_min) & (filtered_df['temperature_C'] <= temp_max) # Apply filter
]   

# Show data preview
st.subheader("Data Preview")
st.dataframe(filtered_df.head())

# Alert count bar chart
st.subheader("Alert Level Distribution")
alert_counts = filtered_df['alert_level'].value_counts()
st.bar_chart(alert_counts)

# Pie chart: Alert level distribution
st.subheader("Alert Level Distribution (Pie)")
fig_pie, ax_pie = plt.subplots()
alert_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax_pie, colors=['green', 'orange', 'red'])
ax_pie.set_ylabel('')  # Hide Y label
st.pyplot(fig_pie)

st.subheader("Sensor Trends")

# Safely convert and sort the timestamps
filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
filtered_df = filtered_df.sort_values(by='timestamp')

subset_df = filtered_df.tail(1000)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Temperature Over Time**")
    fig1, ax1 = plt.subplots()
    ax1.plot(subset_df['timestamp'], subset_df['temperature_C'], color='orange')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature (°C)')
    st.pyplot(fig1)

with col2:
    st.markdown("**Vibration Over Time**")
    fig2, ax2 = plt.subplots()
    ax2.plot(subset_df['timestamp'], subset_df['vibration_g'], color='purple')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Vibration (g)')
    st.pyplot(fig2)

# Line plot: Temperature over time
st.subheader("Temperature Over Time")
fig, ax = plt.subplots()
filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])
filtered_df = filtered_df.sort_values(by='timestamp')
ax.plot(filtered_df['timestamp'], filtered_df['temperature_C'], label='Temperature (°C)')
ax.set_xlabel('Time')
ax.set_ylabel('Temperature (°C)')
ax.legend()

plt.setp(ax.get_xticklabels(), rotation=45) 
ax.xaxis.set_major_locator(plt.MaxNLocator(6))

st.pyplot(fig)


st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download as CSV",
    data=csv,
    file_name='filtered_ev_sensors.csv',
    mime='text/csv'
)
