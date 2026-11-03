# Report and restructuring record

Write the final report in Overleaf using the professor's LaTeX template when it is
provided. No template was present during restructuring. Use the four assignment
sections, with measured methods/results, limitations and a shared reproducibility
description; this note is not a replacement LaTeX template. Jupyter holds experiments.
No experimental results have been fabricated.

## Preservation and simplification

The original assignment PDF is unchanged. No real dataset or report template was
found. No research data or experimental outputs were removed. The unused `data/raw/`,
`data/processed/`, `results/` and `experiments/` contained only .gitkeep files; those
placeholders were also backed up, then the unused directories were removed. Create
`results/` when experiments actually produce outputs. Existing notebook cells had no results.

Before edits, all source, tests, notebooks, configs, documentation, scripts,
README, .gitignore, .env.example and pyproject.toml were saved byte-for-byte in
a verified local archive outside the project (see the cleanup note below). Every archived
file was hash-verified before its original was replaced. The archive preserves the original uncommitted work outside the project.

- Nested `src/ml4n_ssh/` was replaced by four direct modules, with no install/build step.
- Parquet loading, ID/text validation and seeded random splitting were adapted to
  pandas/plain ID lists. Integer dataset IDs are now accepted without coercion.
- Label validation now uses a plain fixed tuple and explicit array encoding; raw
  annotation encoding still requires inspection of the real file.
- Protocols, dataclasses, typed configuration hierarchy, YAMLs, mock pipeline,
  duplicate interface stubs and smoke scripts were removed from the active layout.
- Five architecture documents were consolidated into README, PLAN and TODO.
- Four notebooks were rebuilt with assignment-specific experiment TODOs and no outputs.
- Six test/fixture files were replaced by one minimal suite for retained behavior.
- Old detailed contract tests remain in the backup; their container APIs are retired.
- `clustering.py` and `bert.py` intentionally contain ownership/scope docstrings only:
  these two requested workstream files will grow when actual functions are needed.
- `data/README.md` is the only extra note: it records the missing dataset and the
  assignment's schema/annotation caveats. Local caches, build and unused environment folders
  were later removed; recreate an environment following README instructions.

## Verification

Before refactoring: **26 passed**, using existing local pytest dependencies and an
explicit workspace temporary directory. An initial default-temp run had 21 passed
and 5 setup errors because the environment could not create temporary directories;
the explicit workspace directory resolved those errors.

After refactoring: **16 passed in 2.36s** (`tests/test_basic.py`). All four notebook
setup cells also executed successfully from both the repository root and the
notebooks directory (eight setup executions). All notebook code cells compile.
Real-dataset loading cannot be verified until the real dataset is supplied; Parquet
round trips use small synthetic fixtures. No training or expensive analysis was run.

## Local cleanup

Removed .localdeps, .localinstall, .pytest_cache, .tmp, the unused .venv, build
and Python bytecode caches. The backup was copied and SHA-256 verified before
cleanup. Its local location is:

C:/Users/camma/.codex/visualizations/2026/11/03/01a1a11c-9181-79d0-80c1-64c69e4033bf/before-simplification-20261103.zip

## Audit di comprensibilita

PLAN.md ora mappa tutti i punti del PDF ai file e propone firme modificabili.
README, docstring e notebook distinguono utility gia presenti da sezioni ancora
interamente da sviluppare. La checklist riguarda risultati, non un ordine obbligatorio.
Il dataset e ora presente; metadati verificati: 233.035 righe, quattro colonne,
first_timestamp (non firsts_timestamp), Set_Fingerprint lista di stringhe. Le note
sull'assenza del dataset sopra descrivono lo stato alla ristrutturazione precedente.
Nessun algoritmo o risultato scientifico e stato aggiunto durante questo audit.
