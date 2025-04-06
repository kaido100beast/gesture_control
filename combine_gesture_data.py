import pandas as pd
import glob
import os

combined_data = []

csv_files = glob.glob("*.csv")
for file in csv_files:
    if file == "gesture_data.csv":
        continue  # skip the output file

    label = os.path.splitext(os.path.basename(file))[0]
    df = pd.read_csv(file)

    # Add a new column for label
    df["label"] = label
    combined_data.append(df)

# Combine all dataframes
final_df = pd.concat(combined_data, ignore_index=True)

# Save to CSV
final_df.to_csv("gesture_data.csv", index=False)
print("✅ All gesture data combined into 'gesture_data.csv' with proper labels.")
