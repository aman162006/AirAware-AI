

import joblib
import pandas as pd
from datetime import timedelta
from flask import Flask, render_template

app = Flask(__name__)

model = joblib.load("models/pm25_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict")
def predict():

    # Latest historical readings
    df = pd.read_csv("data/prepared_pm25.csv")

    latest = df.iloc[-1]

    next_time = pd.to_datetime(latest["datetime"]) + timedelta(minutes=15)

    features = pd.DataFrame([{
        "hour": next_time.hour,
        "day": next_time.day,
        "month": next_time.month,
        "day_of_week": next_time.dayofweek,
        "pm25_previous": latest["pm25"],
        "pm25_previous_2": latest["pm25_previous"],
        "pm25_previous_3": latest["pm25_previous_2"]
    }])

    # Generate AI prediction
    prediction = model.predict(features)[0]

    return render_template(
        "index.html",
        prediction=round(float(prediction), 2),
        prediction_time=next_time.strftime("%d %b %Y, %I:%M %p")
    )


if __name__ == "__main__":
    app.run(debug=True)
