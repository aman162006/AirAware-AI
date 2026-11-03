
import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAQ_API_KEY")

url = "https://api.openaq.org/v3/sensors/12235985/measurements"

headers = {
    "X-API-Key": api_key,
    "Accept": "application/json"
}

all_records = []
page = 1
max_pages = 100

while page <= max_pages:

    params = {
        "datetime_from": "2025-01-01T00:00:00Z",
        "datetime_to": "2026-11-03T23:59:59Z",
        "limit": 1000,
        "page": page
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=90
        )

        response.raise_for_status()
        data = response.json()

        records = data.get("results", [])

        if not records:
            break

        all_records.extend(records)

        print("Page:", page, "| Total:", len(all_records))

        if len(records) < 1000:
            break

        page += 1
        time.sleep(1)

    except requests.exceptions.RequestException as error:
        print("Connection problem:", error)
        print("Saving downloaded data before stopping...")
        break

if all_records:
    rows = []

    for item in all_records:
        rows.append({
            "datetime": item["period"]["datetimeFrom"]["utc"],
            "pm25": item["value"]
        })

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["datetime"])
    df = df.sort_values("datetime")

    df.to_csv("data/gomti_nagar_pm25.csv", index=False)

    print("\nData saved successfully!")
    print("Total unique records:", len(df))
    print("First date:", df["datetime"].iloc[0])
    print("Last date:", df["datetime"].iloc[-1])

else:
    print("No records available to save.")


