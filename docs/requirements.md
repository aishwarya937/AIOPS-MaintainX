 Project Requirements Specification

## 1. Functional Requirements (What the system does)

### A. Data Ingestion (The Ears)
- System must accept real-time data from IoT sensors (MQTT/HTTP).
- Data points: Vibration, Temperature, Sound, Power Usage.
- Frequency: Data sent every 1 second per machine.

### B. Data Processing & AI (The Brain)
- **Anomaly Detection**: Detect outliers using Isolation Forest.
- **Failure Prediction**: Predict breakdown probability (0-100%) using LSTM.
- **Latency**: Inference must happen within 2 seconds of receiving data.

### C. Automated Workflow (The Hands)
- Create a maintenance ticket automatically if Failure Probability > 80%.
- Assign ticket to the technician with the lowest current workload.
- Send push notification to Technician Mobile App.

## 2. Non-Functional Requirements (Quality attributes)
- **Scalability**: Support up to 100 machines concurrently.
- **Reliability**: System uptime 99.9%.
- **Security**: API Key authentication for all IoT devices.

## 3. User Roles
- **Admin**: Configures machines and thresholds.
- **Technician**: Receives tasks and updates status (Fixed/Pending).