"""Small tests for the working skeleton, without real data or model downloads."""
import importlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from src.data import LABELS, encode_labels, load_dataset
from src.supervised import create_random_split

ROOT = Path(__file__).resolve().parents[1]


def test_imports_and_notebooks():
    for name in ("data", "supervised", "clustering", "bert"):
        importlib.import_module(f"src.{name}")
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    assert [p.name for p in notebooks] == ["01_data.ipynb", "02_supervised.ipynb", "03_clustering.ipynb", "04_bert.ipynb"]
    for path in notebooks:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        assert notebook["nbformat"] == 4
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                assert not cell["outputs"]
                compile("".join(cell["source"]), str(path), "exec")


def test_parquet_round_trip(tmp_path):
    path = tmp_path / "sessions.bin"
    pd.DataFrame({"session_id": [1, 2], "full_session": ["whoami", "pwd"],
                  "Set_Fingerprint": [["Discovery", "Execution"], []]}).to_parquet(path)
    frame = load_dataset(path)
    assert frame.session_id.tolist() == [1, 2]
    encoded = encode_labels(frame.Set_Fingerprint)
    assert encoded.shape == (2, 7)
    assert encoded.dtype == np.bool_
    assert encoded[0, LABELS.index("Discovery")]
    assert encoded[0, LABELS.index("Execution")]
    assert not encoded[1].any()


@pytest.mark.parametrize("frame", [
    pd.DataFrame({"wrong": [1]}),
    pd.DataFrame({"session_id": [1], "full_session": [None]}),
    pd.DataFrame({"session_id": [1, 1], "full_session": ["ls", "pwd"]}),
    pd.DataFrame({"session_id": [None], "full_session": ["ls"]}),
    pd.DataFrame({"session_id": [], "full_session": []}),
])
def test_bad_dataset(tmp_path, frame):
    path = tmp_path / "invalid.parquet"
    frame.to_parquet(path)
    with pytest.raises(ValueError):
        load_dataset(path)


@pytest.mark.parametrize("labels", [None, "Discovery", ["Unknown"], ["Discovery", "Discovery"]])
def test_invalid_annotations(labels):
    with pytest.raises(ValueError):
        encode_labels(pd.Series([labels]))


def test_random_split():
    ids = list(range(12))
    split = create_random_split(ids)
    assert split == create_random_split(ids)
    flattened = sum(split.values(), [])
    assert len(flattened) == len(set(flattened)) == len(ids)
    assert set(flattened) == set(ids)
    assert all(split.values())


@pytest.mark.parametrize("ids", [[1, 2], [1, 1, 2], ["", "a", "b"], [None, 1, 2]])
def test_invalid_split(ids):
    with pytest.raises(ValueError):
        create_random_split(ids)
