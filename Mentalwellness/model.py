import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Train a simple model
def train_model():
    df = pd.read_csv("data.csv")

    features = ["sleep_hours", "steps", "meditated", "journaled"]
    X = df[features]
    y = df["mood"]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model


# Predict next day's mood
def predict_next_mood(model, sleep, steps, meditated, journaled):
    input_df = pd.DataFrame([[
        sleep,
        steps,
        meditated,
        journaled
    ]], columns=["sleep_hours", "steps", "meditated", "journaled"])

    prediction = model.predict(input_df)[0]
    return round(prediction, 2)

