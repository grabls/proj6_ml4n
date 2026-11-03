"""P1 — Solo utility iniziali: la sezione 1 e ancora da sviluppare.

Esistono soltanto caricamento Parquet, controlli minimi e codifica delle etichette.
TODO: analisi, tokenizer shell, rappresentazioni, tempo e gruppi di template.
Firme suggerite e requisiti in PLAN.md; esperimenti in notebooks/01_data.ipynb.
"""
from pathlib import Path
import numpy as np
import pandas as pd

LABELS = ("Persistence", "Discovery", "Defense Evasion", "Execution", "Impact", "Other", "Harmless")
SEED = 42


def load_dataset(path: str | Path = "data/ssh_attacks.parquet") -> pd.DataFrame:
    """Read Parquet with PyArrow, retaining original IDs and reference annotations."""
    frame = pd.read_parquet(path, engine="pyarrow")
    required = {"session_id", "full_session"}
    if missing := required - set(frame.columns):
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError("Dataset is empty")
    ids = frame["session_id"]
    if ids.isna().any() or ids.duplicated().any():
        raise ValueError("session_id must be nonmissing and unique")
    if ids.map(lambda value: isinstance(value, str) and not value.strip()).any():
        raise ValueError("session_id cannot be blank")
    if not frame["full_session"].map(lambda value: isinstance(value, str)).all():
        raise ValueError("full_session must contain nonmissing text")
    return frame


def encode_labels(values: pd.Series) -> np.ndarray:
    """Encode decoded label collections in LABELS order; reject serialized strings."""
    encoded = np.zeros((len(values), len(LABELS)), dtype=bool)
    for i, labels in enumerate(values):
        if not isinstance(labels, (list, tuple, set, frozenset, np.ndarray)):
            raise ValueError("Decode annotation collections explicitly; missing labels are not empty sets")
        names = list(labels)
        if any(not isinstance(name, str) or name not in LABELS for name in names):
            raise ValueError("Unknown or malformed reference labels")
        if len(set(names)) != len(names):
            raise ValueError("Duplicate reference labels")
        encoded[i] = [name in names for name in LABELS]
    return encoded
