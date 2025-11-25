# 🚀 PROJECT CHARTER: AIOPS-MaintainX

## 1. Executive Summary
**AIOPS-MaintainX** is an AI-driven Industrial IoT system designed to predict machine failures before they happen. It uses sensor data (Temperature, Vibration, RPM) to forecast breakdowns and automatically triggers maintenance workflows, reducing downtime and manual operational costs.

## 2. Project Scope (What we are building)
### ✅ In-Scope (We WILL do this)
1.  **IoT Edge Simulator:** A Python script to generate realistic sensor data (simulating a factory machine).
2.  **Data Ingestion Pipeline:** Using MQTT (Message Queue) to send data to the Cloud.
3.  **AI Engine:**
    *   **Anomaly Detection:** Unsupervised learning (Isolation Forest) to find weird patterns.
    *   **Failure Prediction:** Deep Learning (LSTM) to predict *when* it will fail.
4.  **Automated Workflow:** If AI detects a fault -> System auto-creates a Ticket.
5.  **User Interface:**
    *   **Manager Dashboard:** React.js app to see live health and charts.
    *   **Technician View:** To see assigned tickets and close them.

### ❌ Out-of-Scope (We will NOT do this)
1.  Connecting to physical hardware (Arduino/Raspberry Pi) - *We are using simulation to save cost.*
2.  Video/Computer Vision monitoring.
3.  Complex billing or payment gateways.

## 3. KPIs (Key Performance Indicators)
We consider this project "Successful" only if:
1.  **Model Accuracy:** The LSTM model achieves >85% accuracy on the test dataset.
2.  **System Latency:** The time from "Sensor Reading" to "Dashboard Alert" is < 5 seconds.
3.  **Automation Rate:** 100% of detected anomalies must trigger a ticket without human clicking a button.

## 4. Risks & Mitigation Strategies
| Risk | Probability | Mitigation Strategy |
| :--- | :--- | :--- |
| **Lack of Real Data** | High | Use the NASA Turbofan Jet Engine dataset or generate synthetic physics-based data. |
| **AI Model Overfitting** | Medium | Use "Early Stopping" and "Dropout" layers in our Neural Network. |
| **Cloud Costs** | Medium | Use Free Tier (AWS/Google) and local Docker containers where possible. |
| **Complexity Overload** | High | Stick strictly to the MVP (Minimum Viable Product) timeline. |
[ MACHINE (Simulator) ] 
       |
       v
[ IOT GATEWAY (MQTT) ] ---> [ DATABASE (Storage) ]
       |
       v
[ AI ENGINE (Model) ] 
       |
    (If Break Predicted?)
       |
       v
[ BACKEND API ] ---> [ CREATE TICKET ]
       |
       v
[ DASHBOARD (React) ]
