import pandas as pd
import numpy as np

WINDOW_SIZE = 10  # number of CAN messages per window


def load_and_prepare(csv_file, label):
    df = pd.read_csv(csv_file)

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Compute inter-arrival time (in seconds)
    df["inter_arrival"] = df["timestamp"].diff().dt.total_seconds()
    df["inter_arrival"].fillna(0, inplace=True)

    features = []

    for i in range(0, len(df) - WINDOW_SIZE, WINDOW_SIZE):
        window = df.iloc[i:i + WINDOW_SIZE]

        feature_row = {
            "mean_speed": window["speed"].mean(),
            "std_speed": window["speed"].std(),
            "max_speed": window["speed"].max(),
            "brake_rate": window["brake"].mean(),
            "steering_variance": window["steering"].var(),
            "mean_inter_arrival": window["inter_arrival"].mean(),
            "std_inter_arrival": window["inter_arrival"].std(),
            "label": label
        }

        features.append(feature_row)

    return pd.DataFrame(features)


if __name__ == "__main__":
    print("[PHASE 4] Feature extraction started")

    normal_df = load_and_prepare("data/raw/normal.csv", label=0)
    attack_df = load_and_prepare("data/raw/attack.csv", label=1)

    dataset = pd.concat([normal_df, attack_df], ignore_index=True)

    dataset.to_csv("data/processed/features.csv", index=False)

    print("[PHASE 4] Feature extraction completed")
    print(f"Total samples: {len(dataset)}")
