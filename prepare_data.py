
import pandas as pd

# Load historical data
df = pd.read_csv("data/gomti_nagar_pm25.csv")

# Convert datetime
df["datetime"] = pd.to_datetime(df["datetime"])

# Sort data by date
df = df.sort_values("datetime").reset_index(drop=True)

# Extract time-based features
df["hour"] = df["datetime"].dt.hour
df["day"] = df["datetime"].dt.day
df["month"] = df["datetime"].dt.month
df["day_of_week"] = df["datetime"].dt.dayofweek

# Previous PM2.5 readings
df["pm25_previous"] = df["pm25"].shift(1)
df["pm25_previous_2"] = df["pm25"].shift(2)
df["pm25_previous_3"] = df["pm25"].shift(3)

# Remove rows with missing previous readings
df = df.dropna().reset_index(drop=True)

# Save prepared dataset
df.to_csv("data/prepared_pm25.csv", index=False)

print("Feature preparation successful!")
print("Total prepared records:", len(df))
print("\nPrepared data:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())
