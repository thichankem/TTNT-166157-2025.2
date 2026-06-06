"""
Model 1 – NLP Symptom Extractor
================================
Takes a Vietnamese (or mixed) patient description and returns a list of
recognised symptom codes that Model 2 (Random Forest) can consume.

Strategy
--------
1. Normalise text (lowercase, strip accents optionally for fallback)
2. Scan for every keyword in SYMPTOM_KEYWORDS using longest-match first
3. Return the deduplicated list of symptom codes
4. convert_to_matrix() hot-encodes the codes into a numpy vector aligned
   with SYMPTOMS_LIST (the feature order used during training)
"""

import re
import unicodedata
import numpy as np

from data.diseases_symptoms import SYMPTOMS_LIST, SYMPTOM_KEYWORDS


# ─────────────────────────────────────────────────────────────────────────── #
# Pre-compute a sorted keyword list: longer phrases checked before substrings #
# ─────────────────────────────────────────────────────────────────────────── #
_KW_PAIRS: list[tuple[str, str]] = []   # (normalised_keyword, symptom_code)

for _symptom_code, _kw_list in SYMPTOM_KEYWORDS.items():
    for _kw in _kw_list:
        _KW_PAIRS.append((_kw.lower().strip(), _symptom_code))

# Sort by keyword length descending so multi-word phrases match before
# their sub-strings (e.g. "sốt cao" before "sốt")
_KW_PAIRS.sort(key=lambda x: len(x[0]), reverse=True)

# Fast lookup: symptom code → index in SYMPTOMS_LIST
_SYMPTOM_INDEX: dict[str, int] = {s: i for i, s in enumerate(SYMPTOMS_LIST)}


# ─────────────────────────────────────────────────────────────────────────── #
#                        Public API (used by main.py)                         #
# ─────────────────────────────────────────────────────────────────────────── #

def process_clinical_text(text: str) -> list[str]:
    """
    Extract symptom codes from free-form patient text.

    Parameters
    ----------
    text : str
        Raw input, e.g.
        "Tôi bị đau đầu, sốt cao 39 độ, ho khan và ớn lạnh 3 ngày nay"

    Returns
    -------
    list[str]
        Ordered, deduplicated list of symptom codes, e.g.
        ["headache", "high_fever", "dry_cough", "chills"]
    """
    if not text:
        return []

    normalised = _normalise(text)
    found_codes: list[str] = []
    seen: set[str]         = set()

    # Work on a mutable copy so we can mask already-matched regions
    remaining = normalised

    # Pass 1: full diacritics match
    for keyword, symptom_code in _KW_PAIRS:
        if symptom_code in seen:
            continue
        if keyword in remaining and _token_match(keyword, remaining):
            found_codes.append(symptom_code)
            seen.add(symptom_code)
            remaining = remaining.replace(keyword, " " * len(keyword), 1)

    # Pass 2: accent-stripped fallback (handles texts typed without diacritics)
    remaining_stripped = _strip_accents(remaining)
    for keyword, symptom_code in _KW_PAIRS:
        if symptom_code in seen:
            continue
        kw_stripped = _strip_accents(keyword)
        if kw_stripped in remaining_stripped and _token_match(kw_stripped, remaining_stripped):
            found_codes.append(symptom_code)
            seen.add(symptom_code)
            remaining_stripped = remaining_stripped.replace(
                kw_stripped, " " * len(kw_stripped), 1
            )

    return found_codes


def convert_to_matrix(symptoms: list[str]) -> np.ndarray:
    """
    Convert a list of symptom codes to a (1 × N) hot-encoded numpy array
    using the fixed feature order defined by SYMPTOMS_LIST.

    Parameters
    ----------
    symptoms : list[str]
        Output from process_clinical_text()

    Returns
    -------
    np.ndarray  shape (1, len(SYMPTOMS_LIST)), dtype float32
    """
    vec = np.zeros((1, len(SYMPTOMS_LIST)), dtype=np.float32)
    for code in symptoms:
        if code in _SYMPTOM_INDEX:
            vec[0, _SYMPTOM_INDEX[code]] = 1.0
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
    """
    Remove Vietnamese / Latin diacritics for fuzzy fallback matching.
    Handles special Vietnamese characters (đ, ơ, ư) that NFKD does not
    automatically decompose into ASCII base characters.
    """
    # Characters that have no NFKD decomposition to ASCII
    _SPECIAL = str.maketrans({
        'đ': 'd', 'Đ': 'D',
        'ơ': 'o', 'Ơ': 'O',
        'ư': 'u', 'Ư': 'U',
    })
    text = text.translate(_SPECIAL)
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _token_match(keyword: str, text: str) -> bool:
    """
    Return True if *keyword* appears in *text* at a word boundary.
    Vietnamese words are separated by spaces; we also allow punctuation
    as a boundary.
    """
    # Allow match at start/end of string or adjacent to non-alphanum chars
    pattern = r"(?<![^\s,;.!?()])" + re.escape(keyword) + r"(?![^\s,;.!?()])"
    return bool(re.search(pattern, text))
