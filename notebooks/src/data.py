"""P1 — Solo utility iniziali: la sezione 1 e ancora da sviluppare.

Esistono soltanto caricamento Parquet, controlli minimi e codifica delle etichette.
TODO: analisi, tokenizer shell, rappresentazioni, tempo e gruppi di template.
Firme suggerite e requisiti in PLAN.md; esperimenti in notebooks/01_data.ipynb.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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


def heat_map_section2(labels_ts):
    # share of sessions with each label, per week 'How many sessions (upon 100) contain the lable'
    #  --> every week goes from Monday to Sunday and is labeled with Sunday
    weekly_share = labels_ts.resample("W").mean() 

    fig, ax = plt.subplots(figsize=(12, 3.5), layout="constrained")
    sns.heatmap(weekly_share.T, cmap="viridis", vmin=0, vmax=1, ax=ax,
                cbar_kws={"label": "Share of sessions"},
                xticklabels=weekly_share.index.strftime("%Y-%m-%d"))
    ax.set(xlabel="Week", ylabel="", title="Weekly share of sessions with each label")
    ax.tick_params(axis="x", labelsize=7, rotation=90)
    plt.show()
