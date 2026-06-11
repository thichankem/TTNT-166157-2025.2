"""
Model 2 – Disease Predictor (Naive Bayes)
=========================================
Loads the trained Naive Bayes bundle produced by the ChanDoanBenh_ML project
and predicts the most likely disease(s) given a symptom vector.

The bundle is a dict with two keys:
    "model"          – a fitted scikit-learn classifier (GaussianNB)
    "label_encoder"  – the LabelEncoder whose classes_ are the *Vietnamese*
                       disease names (e.g. "Viêm phổi", "Sốt xuất huyết").

Because the labels are already clean Vietnamese names, no extra code→name
mapping is needed and the API never exposes raw codes or percentages.
"""

import os
import pickle
import numpy as np

# ─── Path to the saved model bundle ─────────────────────────────────────── #
_MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "model", "naive_bayes_health_model.pkl"
)

# ─── Lazy-loaded globals ─────────────────────────────────────────────────── #
_bundle: dict | None      = None
_model                    = None
_label_encoder            = None
FEATURE_NAMES: list[str]  = []   # the 135 Vietnamese symptom features, in order


def _load_model() -> None:
    global _bundle, _model, _label_encoder, FEATURE_NAMES

    if _bundle is not None:
        return  # already loaded

    path = os.path.abspath(_MODEL_PATH)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")

    with open(path, "rb") as f:
        _bundle = pickle.load(f)

    _model         = _bundle["model"]
    _label_encoder = _bundle["label_encoder"]

    # Feature order the model was trained on (Vietnamese symptom phrases)
    FEATURE_NAMES = list(getattr(_model, "feature_names_in_", []))


def get_feature_names() -> list[str]:
    """Return the ordered list of symptom feature names the model expects."""
    _load_model()
    return FEATURE_NAMES


def predict_from_vector(vector: np.ndarray) -> dict:
    """
    Predict disease from a hot-encoded symptom vector.

    Parameters
    ----------
    vector : np.ndarray
        Shape (1, N) aligned with FEATURE_NAMES, as built by convert_to_matrix().

    Returns
    -------
    dict with keys:
        "prediction"              – str  : Vietnamese disease name (top-1)
        "confidence"              – float: probability of the top prediction (0-1)
        "top_3"                   – list : up to 3 {"disease", "probability"}
        "total_symptoms_detected" – int
    """
    _load_model()

    if vector.sum() == 0:
        return _empty_result()

    import pandas as pd

    n_features = len(FEATURE_NAMES)
    # Align the incoming vector to the model's feature count just in case
    if vector.shape[1] != n_features:
        aligned = np.zeros((1, n_features), dtype=np.float64)
        cols = min(vector.shape[1], n_features)
        aligned[0, :cols] = vector[0, :cols]
        vector = aligned

    df_input = pd.DataFrame(vector.astype(np.float64), columns=FEATURE_NAMES)

    # ── Probability estimates ────────────────────────────────────────────── #
    proba   = _model.predict_proba(df_input)[0]   # shape (n_classes,)
    classes = _label_encoder.classes_             # Vietnamese disease names

    # Sort descending and keep the top 3
    order = np.argsort(proba)[::-1]
    top_3 = [
        {"disease": str(classes[i]), "probability": float(proba[i])}
        for i in order[:3]
    ]

    return {
        "prediction":              str(classes[order[0]]),
        "confidence":              float(proba[order[0]]),
        "top_3":                   top_3,
        "total_symptoms_detected": int(vector.sum()),
    }


def _empty_result() -> dict:
    return {
        "prediction":              "Không xác định được bệnh",
        "confidence":              0.0,
        "top_3":                   [],
        "total_symptoms_detected": 0,
    }
