"""
Training script for Random Forest disease diagnosis model.

Pipeline:
  1. Load disease-symptom knowledge base
  2. Generate synthetic training data (hot-encoded symptom vectors)
  3. Train Random Forest classifier
  4. Save model bundle to model/random_forest_health_model.pkl

Run: python train_model.py   (from the backend/ directory)
"""

import os
import sys
import pickle
import random

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

sys.path.insert(0, os.path.dirname(__file__))
from data.diseases_symptoms import SYMPTOMS_LIST, DISEASES

random.seed(42)
np.random.seed(42)

SAMPLES_PER_DISEASE  = 120   # synthetic patients per disease
SYMPTOM_PRESENCE_MIN = 0.55  # min fraction of characteristic symptoms present
SYMPTOM_PRESENCE_MAX = 0.95  # max fraction
NOISE_PROB           = 0.05  # probability of a random non-disease symptom being set


def generate_training_data() -> tuple[pd.DataFrame, pd.Series]:
    """
    For every disease, create SAMPLES_PER_DISEASE synthetic patient rows.
    Each row is a hot-encoded vector over SYMPTOMS_LIST.
    """
    symptom_index = {s: i for i, s in enumerate(SYMPTOMS_LIST)}
    disease_codes  = list(DISEASES.keys())
    n_symptoms     = len(SYMPTOMS_LIST)

    rows, labels = [], []

    for disease_code in disease_codes:
        info = DISEASES[disease_code]
        # Keep only symptoms that exist in our master list
        char_symptoms = [s for s in info["symptoms"] if s in symptom_index]

        for _ in range(SAMPLES_PER_DISEASE):
            vec = np.zeros(n_symptoms, dtype=np.float32)

            # Randomly include a subset of characteristic symptoms
            frac   = random.uniform(SYMPTOM_PRESENCE_MIN, SYMPTOM_PRESENCE_MAX)
            k      = max(1, int(len(char_symptoms) * frac))
            chosen = random.sample(char_symptoms, k)
            for s in chosen:
                vec[symptom_index[s]] = 1.0

            # Add a small amount of noise (unrelated symptoms)
            for i in range(n_symptoms):
                if vec[i] == 0 and random.random() < NOISE_PROB:
                    vec[i] = 1.0

            rows.append(vec)
            labels.append(disease_code)

    X = pd.DataFrame(rows, columns=SYMPTOMS_LIST)
    y = pd.Series(labels, name="disease")
    return X, y


def train_and_save():
    print("=" * 60)
    print("Disease Diagnosis - Random Forest Training")
    print("=" * 60)
    print(f"  Diseases  : {len(DISEASES)}")
    print(f"  Symptoms  : {len(SYMPTOMS_LIST)}")
    print(f"  Samples   : {len(DISEASES) * SAMPLES_PER_DISEASE}")
    print()

    # ── 1. Generate data ────────────────────────────────────────────────────
    print("[1/4] Generating synthetic training data ...")
    X, y = generate_training_data()

    # ── 2. Encode labels ────────────────────────────────────────────────────
    print("[2/4] Encoding labels ...")
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    # ── 3. Train / test split ────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.15, random_state=42, stratify=y_enc
    )

    # ── 4. Train Random Forest ──────────────────────────────────────────────
    print("[3/4] Training Random Forest ...")
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=4,
        min_samples_leaf=2,
        max_features="sqrt",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    acc    = accuracy_score(y_test, y_pred)
    print(f"       Test accuracy : {acc * 100:.2f}%")

    # Top-5 feature importances
    importances = pd.Series(rf.feature_importances_, index=SYMPTOMS_LIST)
    top5 = importances.nlargest(5)
    print("       Top-5 important symptoms:")
    for sym, imp in top5.items():
        print(f"         {sym:<35} {imp:.4f}")

    # Full classification report (concise)
    print()
    print("       Macro-avg F1 / Precision / Recall:")
    report = classification_report(y_test, y_pred,
                                   target_names=le.classes_,
                                   output_dict=True)
    macro = report["macro avg"]
    print(f"         Precision {macro['precision']:.3f} | "
          f"Recall {macro['recall']:.3f} | "
          f"F1 {macro['f1-score']:.3f}")

    # ── 5. Save model bundle ─────────────────────────────────────────────────
    print("[4/4] Saving model ...")
    model_dir = os.path.join(os.path.dirname(__file__), "model")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "random_forest_health_model.pkl")

    # Build Vietnamese name mapping for inference
    disease_name_map = {
        code: info["name_vi"]
        for code, info in DISEASES.items()
    }

    bundle = {
        "model":            rf,
        "label_encoder":    le,
        "symptoms_list":    SYMPTOMS_LIST,
        "disease_name_map": disease_name_map,
    }
    with open(model_path, "wb") as f:
        pickle.dump(bundle, f)

    size_mb = os.path.getsize(model_path) / 1_048_576
    print(f"       Saved -> {model_path}  ({size_mb:.1f} MB)")
    print()
    print("Training complete!")
    print("=" * 60)


if __name__ == "__main__":
    train_and_save()
