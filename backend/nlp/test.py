import joblib
import pandas as pd


MODEL_PATH = "C:/Users/user/OneDrive/Desktop/Sih_hack/backend/nlp/nlp_model.pkl"
DATASET_PATH = "C:/Users/user/OneDrive/Desktop/Sih_hack/backend/nlp/network_configure.csv"


model = joblib.load(MODEL_PATH)

dataset = pd.read_csv(DATASET_PATH)


def predict_command(command):

    # Predict intent
    intent = model.predict([command])[0]

    # Prediction probabilities
    probabilities = model.predict_proba([command])[0]

    classes = model.classes_

    confidence = max(probabilities)

    # Find metadata for predicted intent
    matches = dataset[
        dataset["intent"] == intent
    ]

    if len(matches) > 0:

        parameter = matches.iloc[0]["parameter"]
        value = matches.iloc[0]["value"]

    else:

        parameter = "unknown"
        value = "unknown"

    return {
        "command": command,
        "intent": intent,
        "parameter": parameter,
        "value": value,
        "confidence": round(float(confidence), 4)
    }


if __name__ == "__main__":

    commands = [
        "ip ssh version 2",
        "transport input telnet",
        "enable ssh version 2",
        "enable centralized logging",
        "set system services ssh protocol-version v2",
        "random security command"
    ]

    for command in commands:

        result = predict_command(command)

        print("\nCommand:", command)
        print("Intent:", result["intent"])
        print("Parameter:", result["parameter"])
        print("Value:", result["value"])
        print("Confidence:", result["confidence"])