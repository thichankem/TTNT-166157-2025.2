from pathlib import Path
import numpy as np
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "random_forest_health_model.pkl"

_model = joblib.load(MODEL_PATH)


def predict_from_vector(input_vector: np.ndarray) -> dict:
    if input_vector.ndim == 1:
        input_vector = input_vector.reshape(1, -1)

    probabilities = _model.predict_proba(input_vector)[0]
    classes = _model.classes_
    prediction = _model.predict(input_vector)[0]

    top_3_idx = np.argsort(probabilities)[-3:][::-1]
    top_3 = [
        {
            "disease": str(classes[i]),
            "probability": float(probabilities[i]),
        }
        for i in top_3_idx
    ]

    return {
        "prediction": str(prediction),
        "confidence": float(np.max(probabilities)),
        "top_3": top_3,
    }
