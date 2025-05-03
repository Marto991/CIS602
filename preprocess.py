import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle

# === File paths ===
input_file = "merged_network_data.csv"
output_file = "preprocessed_data.csv"
scaler_file = "scaler.pkl"

# === Function: Load and Clean Data ===
def load_and_clean_data(filepath):
    """
    Loads network traffic CSV, converts data types, and handles missing values.
    Converts categorical features into numeric format (one-hot or label encoding).
    """
    df = pd.read_csv(filepath)

    # Replace missing or non-numeric ports with -1 (e.g., for ICMP or malformed packets)
    df["src_port"] = pd.to_numeric(df["src_port"], errors="coerce").fillna(-1).astype(int)
    df["dst_port"] = pd.to_numeric(df["dst_port"], errors="coerce").fillna(-1).astype(int)
    df["length"] = pd.to_numeric(df["length"], errors="coerce").fillna(0).astype(int)

    # Drop unnecessary fields if needed (e.g., timestamp, IPs)
    df = df.drop(columns=["timestamp", "src_ip", "dst_ip"])

    # One-hot encode the protocol column (TCP, UDP, OTHER)
    df = pd.get_dummies(df, columns=["protocol"])

    return df

# === Function: Scale Features ===
def scale_features(dataframe):
    """
    Applies standard scaling (zero mean, unit variance) to the dataset.
    Saves the scaler object for consistent use in real-time detection.
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(dataframe)

    # Save the scaler for live detection
    with open(scaler_file, "wb") as f:
        pickle.dump(scaler, f)

    return scaled_data

# === Main Preprocessing Pipeline ===
def preprocess():
    """
    Full preprocessing pipeline: Load, clean, encode, scale, and save the transformed data.
    """
    print("[*] Loading and preprocessing data...")
    df = load_and_clean_data(input_file)
    X_scaled = scale_features(df)

    # Save the scaled data to CSV for model training
    pd.DataFrame(X_scaled).to_csv(output_file, index=False)
    print(f"[+] Preprocessed data saved to: {output_file}")
    print(f"[+] Scaler saved to: {scaler_file}")

# === Entry Point ===
if __name__ == "__main__":
    preprocess()
