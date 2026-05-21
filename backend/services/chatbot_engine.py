"""
Model 2 – Random Forest Disease Predictor
==========================================
Loads the trained model bundle and predicts the most likely disease(s)
given a hot-encoded symptom vector.
"""

import os
import pickle
import numpy as np

# ─── Path to the saved model bundle ─────────────────────────────────────── #
_MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "model", "random_forest_health_model.pkl"
)

# ─── Lazy-loaded globals ─────────────────────────────────────────────────── #
_bundle: dict | None         = None
_rf                          = None
_label_encoder               = None
_disease_name_map: dict      = {}
_symptoms_list: list[str]    = []


def _load_model() -> None:
    global _bundle, _rf, _label_encoder, _disease_name_map, _symptoms_list

    if _bundle is not None:
        return  # already loaded

    path = os.path.abspath(_MODEL_PATH)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file not found: {path}\n"
            "Please run  python train_model.py  first."
        )

    with open(path, "rb") as f:
        _bundle = pickle.load(f)

    _rf               = _bundle["model"]
    _label_encoder    = _bundle["label_encoder"]
    _disease_name_map = _bundle.get("disease_name_map", {})
    _symptoms_list    = _bundle.get("symptoms_list", [])


def predict_from_vector(vector: np.ndarray) -> dict:
    """
    Predict disease from a hot-encoded symptom vector.

    Parameters
    ----------
    vector : np.ndarray
        Shape (1, N) as returned by convert_to_matrix().

    Returns
    -------
    dict with keys:
        "prediction"  – str  : Vietnamese name of most-likely disease
        "disease_code"– str  : raw disease code
        "confidence"  – float: probability of top prediction (0-1)
        "top_3"       – list : up to 3 dicts {"disease", "code", "probability"}
        "total_symptoms_detected" – int
    """
    _load_model()

    if vector.sum() == 0:
        return _empty_result()

    # Build a DataFrame with named columns so sklearn doesn't warn about
    # missing feature names (model was trained on a DataFrame)
    import pandas as pd

    n_features = _rf.n_features_in_
    if vector.shape[1] != n_features:
        aligned = np.zeros((1, n_features), dtype=np.float32)
        cols = min(vector.shape[1], n_features)
        aligned[0, :cols] = vector[0, :cols]
        vector = aligned

    feature_names = _symptoms_list[:n_features]
    if len(feature_names) < n_features:
        feature_names += [f"__pad_{i}" for i in range(n_features - len(feature_names))]
    df_input = pd.DataFrame(vector, columns=feature_names)

    # ── Probability estimates ────────────────────────────────────────────── #
    proba   = _rf.predict_proba(df_input)[0]        # shape (n_classes,)
    classes = _label_encoder.classes_               # disease code strings

    # Sort descending
    order     = np.argsort(proba)[::-1]
    top_codes = [classes[i] for i in order[:3]]
    top_probs = [float(proba[i]) for i in order[:3]]

    top_3 = [
        {
            "disease":     _disease_name_map.get(code, code),
            "code":        code,
            "probability": prob,
        }
        for code, prob in zip(top_codes, top_probs)
    ]

    best_code = top_codes[0]
    best_name = _disease_name_map.get(best_code, best_code)

    return {
        "prediction":              best_name,
        "disease_code":            best_code,
        "confidence":              top_probs[0],
        "top_3":                   top_3,
        "total_symptoms_detected": int(vector.sum()),
    }


def _empty_result() -> dict:
    return {
        "prediction":              "Không xác định được bệnh",
        "disease_code":            "unknown",
        "confidence":              0.0,
        "top_3":                   [],
        "total_symptoms_detected": 0,
    }
