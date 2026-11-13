"""P2 — Solo split casuale: la sezione 2 e ancora da sviluppare.

Non ci sono classificatori, tuning, metriche o risultati.
TODO: split temporale/per gruppi, modelli multi-label, confronto ed errori.
Firme suggerite in PLAN.md; esperimenti in notebooks/02_supervised.ipynb.
"""
from collections.abc import Sequence
import numpy as np
import pandas as pd
from .data import SEED


def create_random_split(
    session_ids: Sequence[int | str], *, seed: int = SEED,
    validation_fraction: float = 0.2, test_fraction: float = 0.2,
) -> dict[str, list[int | str]]:
    """Return disjoint stable ID lists; this baseline is not stratified or temporal."""
    ids = list(session_ids)
    if any(not isinstance(value, (str, int, np.integer)) or isinstance(value, (bool, np.bool_)) for value in ids):
        raise ValueError("Session IDs must be integers or strings")
    if any(isinstance(value, str) and not value.strip() for value in ids) or pd.Index(ids).has_duplicates:
        raise ValueError("Session IDs must be unique and nonblank")
    if not (0 < validation_fraction < 1 and 0 < test_fraction < 1 and validation_fraction + test_fraction < 1):
        raise ValueError("Fractions must be positive and leave training data")
    n_test = max(1, int(len(ids) * test_fraction))
    n_val = max(1, int(len(ids) * validation_fraction))
    if n_test + n_val >= len(ids):
        raise ValueError("Too few sessions for three nonempty partitions")
    order = np.random.default_rng(seed).permutation(len(ids))
    shuffled = [ids[i] for i in order]
    return {"train": shuffled[n_test + n_val:], "validation": shuffled[n_test:n_test + n_val], "test": shuffled[:n_test]}
