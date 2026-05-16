from pathlib import Path
from typing import List
import pandas as pd
import numpy as np
import re
from difflib import SequenceMatcher

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MAPPING_PATH = DATA_DIR / "symptoms_mapping.csv"
TRANSFORMED_DATA_PATH = DATA_DIR / "transformed_dataset.csv"

_df_mapping = pd.read_csv(MAPPING_PATH)
_df_transformed = pd.read_csv(TRANSFORMED_DATA_PATH)
_symptom_cols = [
    col.strip()
    for col in _df_transformed.columns
    if col not in ["Unnamed: 0", "Disease", "Disease_code"]
]
_df_transformed.columns = [c.strip() for c in _df_transformed.columns]

_weights_dict = {}
for col in _symptom_cols:
    non_zero = _df_transformed[col][_df_transformed[col] > 0]
    _weights_dict[col] = int(non_zero.mode()[0]) if not non_zero.empty else 1


def fuzzy_match_score(s1: str, s2: str) -> float:
    return SequenceMatcher(None, s1, s2).ratio()


def process_clinical_text(text: str, threshold: float = 0.85) -> List[str]:
    text_clean = text.lower()
    text_clean = re.sub(r"[,\.\?!\(\)]", " ", text_clean)

    detected_en_symptoms = []
    for _, row in _df_mapping.iterrows():
        vn_term = str(row["vi"]).lower().strip()
        en_term = str(row["en"]).strip()

        if re.search(r"\b" + re.escape(vn_term) + r"\b", text_clean):
            detected_en_symptoms.append(en_term)
            continue

        words = text_clean.split()
        for i in range(len(words)):
            for length in [1, 2, 3]:
                if i + length <= len(words):
                    sub_phrase = " ".join(words[i : i + length])
                    if fuzzy_match_score(sub_phrase, vn_term) > threshold:
                        detected_en_symptoms.append(en_term)
                        break

    return list(dict.fromkeys(detected_en_symptoms))


def convert_to_matrix(detected_list: List[str]) -> np.ndarray:
    vector = np.zeros(len(_symptom_cols), dtype=int)
    for sym in detected_list:
        if sym in _symptom_cols:
            idx = _symptom_cols.index(sym)
            vector[idx] = _weights_dict.get(sym, 1)
    return vector
