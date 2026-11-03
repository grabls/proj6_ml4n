# Project checklist

P1–P4 are the four developers. Completion requires the stated evidence. Only the verified initial
utility checks are complete; scientific experiments remain open. PDF section numbers map to the local official assignment.

## Come leggere questa checklist

Per **dove scrivere ogni punto del PDF**, stato del codice e **firme suggerite**,
leggere [PLAN.md](PLAN.md). Le firme e il percorso sono modificabili: qui si spuntano
risultati dimostrati, non passaggi di una procedura obbligatoria. I numeri delle sezioni
seguono il PDF. Una utility presente non significa che la sezione sia completata.

## Shared setup

- [ ] **All — Confirm assignment logistics and analyst objective**
  - Depends on: None.
  - Done when: Official deadline and professor template obtained; deployment conditions, error priorities and compute budgets agreed with teacher.
- [ ] **P1 + All — Verify the available real Parquet dataset**
  - Depends on: Local file data/ssh_attacks.parquet (now present).
  - Done when: Private local file loads with pandas/PyArrow; schema, digest, ID type and reference encoding recorded; document the four actual columns and first_timestamp spelling; content validation remains open despite verified metadata.
- [ ] **All — Freeze lightweight shared conventions**
  - Depends on: Verified sample.
  - Done when: LABELS, seed, original IDs, missing-label policy, prediction row/column order and split-manifest format agreed and documented.

## Section 1 — P1: data and preprocessing

- [ ] **P1 — Decode and audit automatic reference annotations**
  - Depends on: Real dataset.
  - Done when: Set_Fingerprint physical encoding verified; collections validated; add/test a safe decoder only if actual encoding requires one; missing vs empty annotations distinguished; Harmless interpretation documented; original reference unchanged.
- [ ] **P1 — Describe shell text and annotation quality (PDF 1.1)**
  - Depends on: Decoded references.
  - Done when: Character lengths, defined token lengths, common elements, label frequencies/co-occurrences and label-set sizes plotted with denominators.
- [ ] **P1 — Analyze sessions and label composition over time (PDF 1.2)**
  - Depends on: Verified parsing/timezone of the real first_timestamp column.
  - Done when: Counted population and distinct-text frequency limitations explained; November 2019 honeypot upgrade considered.
- [ ] **P1 — Implement and explain shell tokenization (PDF 1.3)**
  - Depends on: Representative text sample.
  - Done when: Operators, options, paths, addresses, quoting and case have explicit policies and tested examples; ordinary-text tokenizer failures illustrated.
- [ ] **P1 — Compare two representations (PDF 1.4)**
  - Depends on: Tokenizer and training IDs from P2.
  - Done when: Count/TF-IDF baseline and a contrasting representation evaluated; normalization and preserved/discarded information explained; choices discussed with teacher.
- [ ] **P1 — Define label-free near-duplicate template groups (PDF 1.5)**
  - Depends on: Session texts.
  - Done when: Reproducible grouping rule and positive/negative examples supplied to P2; textual similarity not claimed as attacker/campaign attribution.

## Section 2 — P2: supervised multi-label classification

- [ ] **P2 — Build and audit three validation strategies (PDF 2.1)**
  - Depends on: P1 IDs/timestamps/template groups.
  - Done when: Random, chronological and group-separated manifests persisted; overlap, temporal ties, per-label support and deployment relevance documented; teacher consulted.
- [ ] **P2 — Compare classifiers and representations (PDF 2.2)**
  - Depends on: P1 representations and audited splits.
  - Done when: Multi-label model justified across representations/splits; imbalance handling and time features explained; population and information changes separated from representation gains.
- [ ] **P2 — Tune and select the classical pipeline (PDF 2.3)**
  - Depends on: Baseline runs.
  - Done when: Training-fold preprocessing and validation-only hyperparameters/thresholds recorded; micro/macro/per-label metrics, support and empty/small-positive cases reported with explicit undefined-metric policy.
- [ ] **P2 — Freeze deployment pipeline and evaluate final test (PDF 2.4)**
  - Depends on: Selected model and agreed deployment scenario.
  - Done when: Pipeline/settings frozen before test use; held-out results saved with IDs; representative errors and two text-supported failure patterns separate disagreements from suspected reference errors.

## Section 3 — P3: unsupervised behavioral clustering

- [ ] **P3 — Define two similarities (PDF 3.1)**
  - Depends on: P1 representations.
  - Done when: Main similarity and robustness alternative justified and discussed with teacher.
- [ ] **P3 — Run at least two clustering algorithms (PDF 3.2)**
  - Depends on: Chosen similarities and budget.
  - Done when: Distances, reduction, sampling, hyperparameters and noise treatment justified; represented sessions and bounded compute recorded.
- [ ] **P3 — Select clusters without reference labels (PDF 3.3)**
  - Depends on: Clustering candidates.
  - Done when: Internal quality, stability and objective drive frozen selection; comparison under resampling/alternative normalization documented before label inspection.
- [ ] **P3 — Visualize and interpret selected clusters (PDF 3.4)**
  - Depends on: Frozen clustering selection.
  - Done when: Projection and limitations justified; representative sessions and discriminative command/context patterns support descriptions; word clouds only supplementary.
- [ ] **P3 — Analyze multi-label composition (PDF 3.5)**
  - Depends on: Frozen clusters and P1 references.
  - Done when: Raw counts, explicitly normalized prevalences, cluster sizes, coverage and noise included.
- [ ] **P3 — Explain behavioral families beyond intents (PDF 3.6)**
  - Depends on: Interpreted clusters.
  - Done when: Examples show one intent set across distinct groups and multiple intent sets within one group; cautious finer-family descriptions have examples and counterexamples.

## Section 4 — P4: contextual language models

- [ ] **P4 — Select and document a pretrained encoder (PDF 4.1)**
  - Depends on: Shell examples and compute budget.
  - Done when: Shell suitability, exact model revision and training provenance documented; choice discussed with teacher.
- [ ] **P4 — Compare frozen encoder/head and fine-tuning (PDF 4.2)**
  - Depends on: P1 labels and P2 shared training/validation IDs.
  - Done when: Frozen plus partial/full fine-tuning compared under common data/compute budget; trainable parameters, head, loss, activation and optimizer recorded.
- [ ] **P4 — Compare truncation and chunking (PDF 4.3)**
  - Depends on: Actual selected tokenizer.
  - Done when: Bounded experiment uses tokenizer lengths, documented aggregation, same-parent chunk isolation and whole-session evaluation.
- [ ] **P4 + P2 — Compare with strongest classical baseline (PDF 4.4)**
  - Depends on: Selected contextual/classical pipelines.
  - Done when: Same sessions, references, admissible information and metrics used; validation and final test results reported; compute costs recorded.
- [ ] **P4 — Analyze errors and analyst referral (PDF 4.5)**
  - Depends on: Contextual predictions.
  - Done when: Errors related to length, patterns and label support; ambiguity/referral rule selected on validation and evaluated separately with coverage/quality tradeoff.

## Integration

- [ ] **All — Integrate modules and notebooks**
  - Depends on: Implemented section experiments.
  - Done when: Reusable functions reside in four modules; each notebook runs with its documented inputs in the shared environment with real outputs and no duplicated complex code.
- [ ] **P2 + P4 — Audit scientific comparability and leakage**
  - Depends on: Frozen manifests/pipelines.
  - Done when: Session and label alignment verified; transforms fitted in training folds; chunks/groups isolated appropriately; test untouched during selection; transductive work identified.
- [ ] **All — Save reproducibility records**
  - Depends on: Actual experiments.
  - Done when: Seeds, dataset digest, manifests, settings, code/dependency/model versions, sampling coverage and compute logs accompany results; private data stays outside Git.

## Testing

- [x] **All — Verify initial project utilities**
  - Depends on: Restructured skeleton.
  - Done when: Imports, Parquet loading, label order, seeded split and notebook structure pass basic tests; actual run recorded in report/README.md.
- [ ] **P1 + P2 — Extend tests when preprocessing and splits exist**
  - Depends on: Real implementations.
  - Done when: Representative shell handling, missing/invalid data, leakage and random/temporal/group split invariants pass; no tests claim unimplemented algorithms work.
- [ ] **P3 + P4 — Test implemented cluster/contextual output alignment**
  - Depends on: Real implementations.
  - Done when: IDs/shapes, noise conventions, chunk isolation and session aggregation checked on small fixtures without expensive model downloads in basic tests.

## Report and delivery

- [ ] **All — Write the four report sections in Overleaf**
  - Depends on: Professor template and measured results.
  - Done when: Each section covers methods, results, uncertainty, limitations and all mapped PDF requirements; figures include units/denominators and reference-agreement terminology.
- [ ] **All — Record suspected annotation issues separately**
  - Depends on: Inspected disagreements.
  - Done when: Text-supported examples and uncertainty documented without silently changing benchmark/test labels.
- [ ] **All — Audit and deliver**
  - Depends on: Integrated notebooks/tests/report.
  - Done when: Every checklist item reviewed with evidence; reproducibility instructions validated; final PDF and required submission artifacts prepared against confirmed deadline.
