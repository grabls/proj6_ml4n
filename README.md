# ML4N — SSH Shell Attacks

University research project for four students: predict session intent sets, discover
behavioral families, and compare classical models with a contextual encoder such as
BERT. Algorithms and experimental results are not implemented yet.

## Da dove iniziare

Leggete prima [PLAN.md](PLAN.md): contiene lo stato reale, la mappa di ogni punto
della consegna verso modulo/notebook/report e firme di funzioni **suggerite e modificabili**.
[TODO.md](TODO.md) tiene traccia dei risultati richiesti, non di un ordine obbligatorio.

**Le sezioni 1 e 2 non sono svolte:** `data.py` contiene solo caricamento/codifica
delle etichette; `supervised.py` contiene solo una utility di split casuale.
Non ci sono modelli addestrati o risultati. P3 e P4 hanno solo file di orientamento.

Scrivete esperimenti, grafici e commenti nei notebook; spostate in `src/` le funzioni
riutilizzabili quando servono. Il report finale si scrive in Overleaf. Potete cambiare
funzioni, metodi e percorso di sviluppo, coordinando gli output usati dagli altri.

## Layout and ownership

| Owner | Reusable code | Experiment notebook |
|---|---|---|
| P1 — Data and preprocessing | `src/data.py` | `notebooks/01_data.ipynb` |
| P2 — Supervised multi-label | `src/supervised.py` | `notebooks/02_supervised.ipynb` |
| P3 — Behavioral clustering | `src/clustering.py` | `notebooks/03_clustering.ipynb` |
| P4 — Contextual models | `src/bert.py` | `notebooks/04_bert.ipynb` |

`data/` holds private data; `tests/test_basic.py` checks the initial utilities.
`report/README.md` explains report preparation. The original assignment PDF is at
the repository root. `PLAN.md` gives the six-week provisional roadmap; `TODO.md`
is the requirement checklist. Owners update their tasks with evidence of completion.

## Install and run

Use Python 3.11 or newer. From the repository root, in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q --basetemp=.tmp/pytest
python -m jupyterlab
```

On macOS/Linux activate with `source .venv/bin/activate` instead. No editable install
or package build is needed: import `src.data` from the repository root. Notebooks
also locate the root when Jupyter starts in `notebooks/`. Select the same environment
as the notebook kernel. P4 installs torch/transformers when the model is selected;
record their versions and compute environment then.

Put the real Parquet file at `data/ssh_attacks.parquet` (present locally, ignored by Git):

```python
from src.data import load_dataset
sessions = load_dataset("data/ssh_attacks.parquet")
```

Data is ignored by Git. The real timestamp column is `first_timestamp`, despite
the spelling in the assignment. See `data/README.md` before interpreting annotations.
No expensive data analysis or model download is performed by setup or tests.

## Shared conventions

Preserve original integer/string session IDs. Use `src.data.LABELS` for the seven
columns and `SEED = 42` by default. Share split manifests as dictionaries of
train/validation/test ID lists; select rows by IDs, never by incidental row positions.
For each validation strategy P2 freezes one manifest shared with P4. Predictions
use explicit session IDs, `(N, 7)` boolean decisions and `(N, 7)` numeric scores in
LABELS order. Record whether scores are margins or probabilities and how thresholds
were selected. No container framework is needed.

Fit learned preprocessing only on training folds. Keep test data out of tuning;
keep every session's chunks in its partition. Save the seed, split, settings,
dataset digest, code revision and library/model versions with real experiment outputs.

## Git collaboration

Create a branch such as `git switch -c feature/p1-data`, keep changes focused on
your module/notebook, and open a pull request. Run tests before merging; coordinate
changes to labels, split conventions and shared files with the affected owners.
Do not commit raw logs, private predictions or notebook outputs containing sessions.
Jupyter is for experiments; reusable functions belong in the four modules; the final
report is written in Overleaf using the professor's template when supplied.
