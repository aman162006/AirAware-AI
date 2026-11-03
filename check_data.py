
import pandas as pd

df = pd.read_csv("data/gomti_nagar_pm25.csv")

df["datetime"] = pd.to_datetime(df["datetime"])

print("TOTAL RECORDS:", len(df))

print("\nDATE RANGE:")
print("Start:", df["datetime"].min())
print("End:", df["datetime"].max())

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nPM2.5 STATISTICS:")
print(df["pm25"].describe())

print("\nDUPLICATE RECORDS:", df.duplicated().sum())

print("\nFIRST 5 RECORDS:")
print(df.head())

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))

plt.plot(df["datetime"], df["pm25"])

plt.title("Gomti Nagar PM2.5 Historical Readings")
plt.xlabel("Date")
plt.ylabel("PM2.5 (µg/m³)")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("data/pm25_graph.png")

plt.show()
