# 🛠 TECHNICAL SPECIFICATIONS: AIOPS-MaintainX

## 1. The Technology Stack
We will use the **"Modern Python AI Stack"**.

| Component | Technology | Why we chose it |
| :--- | :--- | :--- |
| **Language** | Python 3.9+ | Standard for AI and Backend. |
| **Frontend** | React.js (Vite) | Fast, modern, and high employability. |
| **Backend API** | FastAPI | Faster than Flask, auto-generates documentation. |
| **Database** | PostgreSQL | Robust Relational DB for users and tickets. |
| **IoT Message Broker** | Eclipse Mosquitto (MQTT) | Lightweight standard for IoT sensor data. |
| **AI/ML** | Scikit-Learn, TensorFlow/Keras | For Random Forest and LSTM models. |
| **Containerization** | Docker | To ensure it runs on any computer. |
| **Orchestration** | Docker Compose | To run Database + API + Frontend together easily. |

## 2. Tenant Model Strategy
**Decision:** Single Tenant / Shared Database.
*   Since this is a final year project, we will build a **Single Organization** view.
*   We will NOT build a SaaS platform for multiple different companies (too complex for 12 weeks).
*   All data lives in one database schema.

## 3. User Stories (Functional Requirements)
These are the features we must code.

### 👤 User: The Factory Manager
1.  **View Dashboard:** I want to see a live graph of machine vibration and temperature.
2.  **Receive Alerts:** I want a red warning on my screen if a machine is predicted to fail.
3.  **View Reports:** I want to see how many machines broke down last week.

### 🔧 User: The Maintenance Technician
1.  **Receive Tickets:** I want the system to auto-assign me a ticket when a machine is sick.
2.  **Update Status:** I want to mark a ticket as "In Progress" or "Resolved" after I fix the machine.
3.  **View SOP:** I want to see the Standard Operating Procedure (Instructions) for the specific error code.

## 4. Data Flow Architecture
1.  **Sensor** generates JSON data -> Sends to **MQTT Broker**.
2.  **Ingestion Service** listens to MQTT -> Saves to **Database**.
3.  **AI Service** reads recent data -> Predicts Failure Probability.
4.  If Probability > 80% -> **Backend** creates a Ticket in Database.
5.  **Frontend** polls Database -> Updates UI.
