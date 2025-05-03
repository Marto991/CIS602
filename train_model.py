import pandas as pd
import pickle
from sklearn.ensemble import IsolationForest

# === File paths ===
input_file = "preprocessed_data.csv"
model_file = "anomaly_model.pkl"

# === Function: Train Isolation Forest ===
def train_model():
    """
    Trains an Isolation Forest model on the scaled dataset.
    Saves the trained model to a .pkl file for use during live anomaly detection.
    """
    print("[*] Loading preprocessed data...")
    X = pd.read_csv(input_file)

    # Initialize Isolation Forest
    model = IsolationForest(
        n_estimators=100,         # Number of trees in the forest
        contamination=0.01,       # Assumed proportion of anomalies in the data
        max_samples='auto',       # Number of samples to draw per tree
        random_state=42
    )

    print("[*] Training Isolation Forest model...")
    model.fit(X)  # Fit the model on the entire dataset

    # Save the trained model
    with open(model_file, "wb") as f:
        pickle.dump(model, f)

    print(f"[+] Model training complete. Model saved to: {model_file}")

# === Entry Point ===
if __name__ == "__main__":
    train_model()
