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

def load_dataset(path):
    df = pd.read_parquet(path, engine="pyarrow")

    indispensabili = {"full_session", "session_id"}

    if indispensabili - set(df.columns):
        raise ValueError("Colonne indispensabili mancanti")

    if not df["session_id"].is_unique:
        raise ValueError("ID non univoci")

    return df


def tokenize_shell(text: str) -> list[str]:
    return text.split()
#prima versione basic molto chill che tokenizza sugli spazi