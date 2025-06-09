import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Log function
log_path = "data/log.csv"

def log_event(event_type, details):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "details": details
    }
    log_df = pd.DataFrame([log_entry])
    if os.path.exists(log_path):
        log_df.to_csv(log_path, mode='a', header=False, index=False)
    else:
        log_df.to_csv(log_path, index=False)

# Streamlit config
st.set_page_config(page_title="EV Safety Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'> Predictive Safety Monitoring for EV Systems</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>AI-powered anomaly detection for electric vehicle health</h4>", unsafe_allow_html=True)

# File upload and saving
uploaded_file = st.sidebar.file_uploader("Upload a new EV sensor CSV", type=["csv"])
os.makedirs("data", exist_ok=True)

if uploaded_file is not None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/ev_data_{timestamp}.csv"
    with open(filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    log_event("upload", f"{filename} uploaded")
    st.success(f"Custom dataset uploaded and saved as {filename}")
    df = pd.read_csv(filename)
else:
    df = pd.read_csv("data/ev_data_20250608_121022.csv")
    st.info("Using default EV sensor dataset.")

# Alert detection logic
def detect_alerts(df):
    alerts = []
    for i, row in df.iterrows():
        triggered = []
        if "Temperature" in row and row["Temperature"] > 80:
            triggered.append(f"High Temp: {row['Temperature']}°C")
        if "Voltage" in row and row["Voltage"] > 450:
            triggered.append(f"High Voltage: {row['Voltage']}V")
        if "Battery_Health" in row and row["Battery_Health"] < 30:
            triggered.append(f"Low Battery Health: {row['Battery_Health']}%")
        if triggered:
            alerts.append(i)
            log_event("alert", f"Row {i}: {', '.join(triggered)}")
    return df.loc[alerts]

alert_df = detect_alerts(df)
if not alert_df.empty:
    st.warning(f"{len(alert_df)} alert(s) detected!")
    st.dataframe(alert_df)
else:
    st.success("No alerts detected in the uploaded data.")

# Timestamp generation
if 'timestamp' not in df.columns:
    st.warning("'timestamp' column missing - generating dummy values.")
    df['timestamp'] = pd.date_range(start='2025-01-01', periods=len(df), freq='T')

# Generate alert level
if 'alert_level' not in df.columns:
    st.info("'alert_level' not found. Generating based on thresholds...")
    def assign_alert_level(row):
        if row.get('temperature_C', 0) > 75 or row.get('vibration_g', 0) > 0.25:
            return "Warning"
        return "Safe"
    df['alert_level'] = df.apply(assign_alert_level, axis=1)
    st.success("Alert levels generated!")

# Sidebar filters
if 'alert_level' in df.columns:
    st.sidebar.header("Filter by Alert Level")
    alert_filter = st.sidebar.multiselect("Select alert levels:", options=df['alert_level'].unique(), default=df['alert_level'].unique())
    filtered_df = df[df['alert_level'].isin(alert_filter)]
else:
    st.warning("'alert_level' column missing — filtering disabled.")
    filtered_df = df

# Temperature slider filter
if 'temperature_C' in df.columns:
    temp_min, temp_max = st.sidebar.slider("Temperature Range (°C)", float(df['temperature_C'].min()), float(df['temperature_C'].max()), (float(df['temperature_C'].min()), float(df['temperature_C'].max())))
    filtered_df = filtered_df[(filtered_df['temperature_C'] >= temp_min) & (filtered_df['temperature_C'] <= temp_max)]

# Data preview
st.subheader("Data Preview")
st.dataframe(filtered_df.head())

# Bar chart
st.subheader("Alert Level Distribution")
alert_counts = filtered_df['alert_level'].value_counts()
st.bar_chart(alert_counts)

# Pie chart
st.subheader("Alert Level Distribution (Pie)")
fig_pie, ax_pie = plt.subplots()
alert_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax_pie, colors=['green', 'orange', 'red'])
ax_pie.set_ylabel('')
st.pyplot(fig_pie)

# Time series plots
if 'timestamp' in filtered_df.columns:
    filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'], errors='coerce')
    filtered_df = filtered_df.dropna(subset=['timestamp']).sort_values(by='timestamp')
    subset_df = filtered_df.tail(1000)

    st.subheader("Sensor Trends")
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

    st.subheader("Temperature Over Time (Full Range)")
    fig, ax = plt.subplots()
    ax.plot(filtered_df['timestamp'], filtered_df['temperature_C'], label='Temperature (°C)')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature (°C)')
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation=45)
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    st.pyplot(fig)
else:
    st.warning("No 'timestamp' column found. Skipping time series plots.")

# Download filtered data
st.subheader("Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download as CSV", data=csv, file_name='filtered_ev_sensors.csv', mime='text/csv')
