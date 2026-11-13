"""P1 — Solo utility iniziali: la sezione 1 e ancora da sviluppare.

Esistono soltanto caricamento Parquet, controlli minimi e codifica delle etichette.
TODO: analisi, tokenizer shell, rappresentazioni, tempo e gruppi di template.
Firme suggerite e requisiti in PLAN.md; esperimenti in notebooks/01_data.ipynb.
"""
from pathlib import Path
import numpy as np
import pandas as pd
LABELS = ("Persistence", "Discovery", "Defense Evasion", "Execution", "Impact", "Other", "Harmless")

def load_dataset(path):
    df = pd.read_parquet(path)

    if {"full_session", "session_id"} - set(df.columns):
        raise ValueError("{full_session, session_i} are not present but they are mandatory")

    if not df["session_id"].is_unique:
        raise ValueError("IDs must be unique")

    return df


def split_tokenize(text: str) -> list[str]:
    """ First tokenization attempt : simple split of the full_session """
    return text.split()