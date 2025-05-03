# CIS602 Anomaly-Based Intrusion Detection System (Spring 2025)

## 📌 Overview
This project implements a real-time anomaly-based network intrusion detection system (NIDS). It collects benign network traffic, trains an Isolation Forest model on it, and then uses the trained model to detect anomalous (potentially malicious) behavior during live monitoring.

---

## 🗂️ Repository Structure
├── data_collection/
│ └── two_day_collector.py # Collects network traffic and saves to CSV every 10 min
│
├── preprocessing/
│ └── preprocess.py # Cleans, transforms, and scales the collected data
│
├── model_training/
│ ├── train_model.py # Trains Isolation Forest model
│ ├── scaler.pkl # Saved StandardScaler
│ └── anomaly_model.pkl # Trained Isolation Forest model
│
├── detection/
│ └── live_detector.py # Real-time detection script using saved model and scaler
│
├── utils/
│ └── merge_csv_files.py # Combines multiple CSV logs into one file
