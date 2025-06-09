#  Predictive Safety Monitoring for EV Systems


A beginner-friendly AI project that performs real-time monitoring of Electric Vehicle (EV) health using anomaly detection and interactive dashboarding — deployed on Streamlit and AWS EC2

# Project Overview

This system analyzes EV sensor data (temperature, vibration, voltage, etc.) and uses an **Isolation Forest model** to detect anomalies. Based on rules and thresholds, it categorizes sensor behavior into **Safe**, **Warning**, or **Critical** states and displays everything in a real-time Streamlit dashboard.

# Features

-  Unsupervised anomaly detection using **Isolation Forest**
-  Visual plots of temperature and vibration over time
-  Rule-based tagging for alerts (custom logic)
-  Interactive filters and CSV export in dashboard
-  Deployable on AWS EC2, Streamlit Cloud, or locally
-  Designed for beginners but applies real-world concepts

# Tech Stack

- Python
- Pandas,Numpy
- Scikit-learn
- Matplotlib
- Streamlit

#  Project Structure

- app/ – Streamlit dashboard  
  - dashboard.py

  - data/ – Raw and processed CSV files  
    - ev_data_20250608_121022.csv  
    - ev_data_20250608_124017.csv  
    - ev_data_20250608_193947.csv

  - models/ – Trained ML models  
    - anomaly_model.pkl  
    - scaler.pkl

  - scripts/ – Custom logic and utilities  
    - train_model.py – Isolation Forest training  
    - alert_logic.py – Rule-based alert tagging  
    - visualize_data.py – Sensor visualizations  
    - visualize_alerts.py – Alert-level plots

- data images/ – Project screenshots   
  - status count.png  
  - temperature over time.png

- requirements.txt – Python dependencies  
- README.md – Project overview and instructions



---

##  How to Run Locally

```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # For Linux/Mac
.venv\Scripts\activate     # For Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app/dashboard.py


# Output Preview

![status count](data images/status count.png)  
![temperature trend](data images/temperature over time.png)
