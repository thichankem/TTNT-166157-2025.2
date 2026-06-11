"""
Model 1 – NLP Symptom Extractor
================================
Takes a Vietnamese patient description and returns the list of symptom
features (out of the 135 the model was trained on) that appear in the text,
then hot-encodes them into a vector Model 2 can consume.

The feature vocabulary is taken directly from the trained model
(`feature_names_in_`), so the symptom names here always stay in sync with
the bundle in  model/naive_bayes_health_model.pkl.

Strategy
--------
1. Normalise text (lowercase, collapse whitespace, keep diacritics)
2. Scan for every symptom phrase using longest-match-first so multi-word
   phrases (e.g. "đau đầu dữ dội") win over their sub-strings ("đau đầu")
3. A small synonym table maps common everyday phrasings onto the canonical
   feature names (e.g. "nhức đầu" → "đau đầu")
4. convert_to_matrix() hot-encodes the matched features into a numpy vector
   aligned with the model's feature order
"""

import re
import unicodedata
import numpy as np

from services.chatbot_engine import get_feature_names


# ─────────────────────────────────────────────────────────────────────────── #
# Synonyms: everyday phrasing  →  canonical feature name (must be a real        #
# feature in the model). Helps catch wording the raw feature list misses.      #
# ─────────────────────────────────────────────────────────────────────────── #
_SYNONYMS: dict[str, str] = {
    "nhức đầu":        "đau đầu",
    "đau cổ họng":     "đau họng",
    "rát họng":        "đau họng",
    "viêm họng":       "đau họng",
    "ngạt mũi":        "nghẹt mũi",
    "chảy nước mũi":   "sổ mũi",
    "chảy mũi":        "sổ mũi",
    "buồn ói":         "buồn nôn",
    "nôn mửa":         "nôn",
    "ói":              "nôn",
    "đi ngoài":        "tiêu chảy",
    "ỉa chảy":         "tiêu chảy",
    "rét run":         "ớn lạnh",
    "lạnh run":        "ớn lạnh",
    "ớn lạnh":         "ớn lạnh",
    "tức ngực":        "đau ngực",
    "mệt":             "mệt mỏi",
    "uể oải":          "mệt mỏi",
    "đau bao tử":      "đau thượng vị",
    "đau dạ dày":      "đau thượng vị",
    "khó tiêu":        "đầy hơi",
    "chán ăn":         "chán ăn",
    "sốt cao":         "sốt cao",
    "sốt nhẹ":         "sốt nhẹ",
}


# ─────────────────────────────────────────────────────────────────────────── #
# Lazily-built keyword index (depends on the model's feature names)            #
# ─────────────────────────────────────────────────────────────────────────── #
_KW_PAIRS: list[tuple[str, str]] | None = None   # (normalised phrase, feature)
_SYMPTOM_INDEX: dict[str, int] | None   = None    # feature → column index


def _build_index() -> None:
    global _KW_PAIRS, _SYMPTOM_INDEX
    if _KW_PAIRS is not None:
        return

    features = get_feature_names()
    _SYMPTOM_INDEX = {s: i for i, s in enumerate(features)}

    pairs: list[tuple[str, str]] = []
    # Every feature phrase maps to itself
    for feat in features:
        pairs.append((feat.lower().strip(), feat))
    # Plus everyday synonyms (only if the target is a real feature)
    for phrase, feat in _SYNONYMS.items():
        if feat in _SYMPTOM_INDEX:
            pairs.append((phrase.lower().strip(), feat))

    # Longest phrase first so multi-word symptoms match before sub-strings
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    _KW_PAIRS = pairs


# ─────────────────────────────────────────────────────────────────────────── #
#                        Public API (used by main.py)                         #
# ─────────────────────────────────────────────────────────────────────────── #

def process_clinical_text(text: str) -> list[str]:
    """
    Extract symptom feature names from free-form patient text.

    Returns an ordered, deduplicated list of canonical feature names, e.g.
    ["đau đầu", "sốt cao", "ho khan", "ớn lạnh"]
    """
    if not text:
        return []

    _build_index()

    normalised = _normalise(text)
    found: list[str] = []
    seen: set[str]   = set()

    # Pass 1: full-diacritics match
    remaining = normalised
    for keyword, feature in _KW_PAIRS:
        if feature in seen:
            continue
        if keyword in remaining and _token_match(keyword, remaining):
            found.append(feature)
            seen.add(feature)
            remaining = remaining.replace(keyword, " " * len(keyword), 1)

    # Pass 2: accent-stripped fallback (texts typed without diacritics)
    remaining_stripped = _strip_accents(remaining)
    for keyword, feature in _KW_PAIRS:
        if feature in seen:
            continue
        kw_stripped = _strip_accents(keyword)
        if kw_stripped in remaining_stripped and _token_match(kw_stripped, remaining_stripped):
            found.append(feature)
            seen.add(feature)
            remaining_stripped = remaining_stripped.replace(
                kw_stripped, " " * len(kw_stripped), 1
            )

    return found


def convert_to_matrix(symptoms: list[str]) -> np.ndarray:
    """
    Convert a list of feature names to a (1 × N) hot-encoded numpy array
    using the model's feature order.
    """
    _build_index()
    n = len(_SYMPTOM_INDEX)
    vec = np.zeros((1, n), dtype=np.float64)
    for feat in symptoms:
        if feat in _SYMPTOM_INDEX:
            vec[0, _SYMPTOM_INDEX[feat]] = 1.0
    return vec


# ─────────────────────────────────────────────────────────────────────────── #
#                              Helper functions                                #
# ─────────────────────────────────────────────────────────────────────────── #

def _normalise(text: str) -> str:
    """Lowercase and collapse whitespace; keep Vietnamese diacritics."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _strip_accents(text: str) -> str:
    """Remove Vietnamese / Latin diacritics for fuzzy fallback matching."""
    _SPECIAL = str.maketrans({
        'đ': 'd', 'Đ': 'D',
        'ơ': 'o', 'Ơ': 'O',
        'ư': 'u', 'Ư': 'U',
    })
    text = text.translate(_SPECIAL)
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _token_match(keyword: str, text: str) -> bool:
    """Return True if *keyword* appears in *text* at a word boundary."""
    pattern = r"(?<![^\s,;.!?()])" + re.escape(keyword) + r"(?![^\s,;.!?()])"
    return bool(re.search(pattern, text))
