from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import joblib
from datetime import datetime
import warnings
from sklearn.exceptions import DataConversionWarning

# === Warning Suppression ===
# Suppress non-critical warnings related to feature names
warnings.filterwarnings(action='ignore', category=UserWarning)

# === Load Pre-trained Model and Scaler ===
# These were saved after the training phase using joblib
model = joblib.load("anomaly_model.pkl")
scaler = joblib.load("scaler.pkl")

# Define feature names used in training (must match exactly)
feature_names = ["protocol", "src_port", "dst_port", "length"]

# === Packet Feature Extraction Function ===
def extract_features(packet):
    """
    Extracts numerical features from a network packet:
    - protocol: encoded as 0 (OTHER), 1 (TCP), 2 (UDP)
    - source port
    - destination port
    - packet length
    Returns a list of extracted features.
    """
    if IP in packet:
        proto = 0  # Default: OTHER
        src_port, dst_port = 0, 0

        if TCP in packet:
            proto = 1
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
        elif UDP in packet:
            proto = 2
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport

        length = len(packet)
        return [proto, src_port, dst_port, length]

    return None  # Skip non-IP packets

# === Anomaly Detection Function ===
def detect(packet):
    """
    Called by sniff() for each incoming packet.
    Extracts features, scales them, and uses the trained model to detect anomalies.
    Prints an alert if an anomaly is detected.
    """
    features = extract_features(packet)
    if features:
        # Convert list to DataFrame for scaler compatibility
        features_df = pd.DataFrame([features], columns=feature_names)

        # Apply standard scaling using the trained scaler
        X_scaled = scaler.transform(features_df)

        # Predict using the Isolation Forest model
        prediction = model.predict(X_scaled)

        # Output alert if the packet is predicted as an anomaly (-1)
        if prediction[0] == -1:
            print(f"[ALERT] Anomaly detected at {datetime.now().isoformat()} → {features}")

# === Live Packet Sniffing Entry Point ===
print("[*] Starting live anomaly detection... Press Ctrl+C to stop.")

# Start sniffing network traffic and apply `detect` to each packet
# store=0 prevents storing packets in memory (saves RAM)
sniff(prn=detect, store=0)
