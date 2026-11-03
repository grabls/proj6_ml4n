# Guida allo sviluppo — cosa fare, dove scriverlo e da dove partire

## Come usare il piano

Il PDF del professore definisce i risultati richiesti. Questo piano suggerisce come
arrivarci: **nomi, firme, librerie, ordine e suddivisione delle funzioni sono modificabili**.
Potete aggiungere, unire, rinominare o eliminare funzioni se trovate una soluzione più
chiara. Non serve implementare tutti i wrapper proposti: serve rispondere alla consegna.
Le firme sotto sono proposte documentali, non implementazioni o stub da creare in massa.

| Dove | Cosa scrivere |
|---|---|
| `src/data.py`, `supervised.py`, `clustering.py`, `bert.py` | Funzioni riutilizzabili della rispettiva sezione. Una prova può nascere nel notebook ed essere estratta dopo. |
| Quattro notebook | Scelte degli esperimenti, chiamate alle funzioni, impostazioni, grafici, risultati reali, commenti e interpretazione. |
| `tests/test_basic.py` | Piccoli controlli sul codice effettivamente implementato; estendere quando serve. |
| `TODO.md` | Checklist dei risultati richiesti, dipendenze e criteri di completamento. |
| Overleaf | Report finale: metodi, risultati, limiti. Template del professore quando disponibile; `report/README.md` contiene solo indicazioni e storico. |

Una funzione scritta non conclude una sezione: servono esperimenti, risultati e spiegazioni.

## Quanto codice serve davvero

**Potete partire scrivendo il codice direttamente nei notebook.** Una cella può
caricare dati, addestrare un modello, calcolare metriche o disegnare un grafico.
Quando una parte viene ripetuta o serve a un compagno, estraetela nel modulo `src/`
corrispondente e importatela. Non serve trasformare ogni cella in una funzione.
Esempio: il confronto di due esperimenti può restare nel notebook; un tokenizer
usato da P1 e P2 conviene condividerlo in `data.py`.

Le numerose firme sotto sono un **menu di possibili aiuti**, non un elenco di
funzioni obbligatorie. In particolare `make_vectorizer`, `make_classifier`,
`tune_classifier`, `load_encoder` e i riepiloghi possono essere semplici celle o
chiamate dirette alle librerie: non aggiungete wrapper che non aiutano a capire.

Per contenere il lavoro, distinguete:

- **Richiesto dal PDF:** due rappresentazioni con baseline count/TF-IDF; tre
  strategie di validazione; due similarità e almeno due algoritmi di clustering;
  encoder congelato contro fine-tuning parziale **oppure** completo; troncamento
  contro chunking; analisi, confronti, interpretazioni e discussioni indicate nella mappa.
- **Scelte vostre:** classificatore, encoder, algoritmi specifici, librerie,
  percentuali degli split, metriche motivate, budget e organizzazione del codice.
- **Non richiesto:** molti classificatori diversi, una grande ricerca esaustiva,
  fine-tuning sia parziale sia completo, tutte le combinazioni tra ogni opzione,
  cross-validation annidata o un framework di esperimenti. Una ricerca piccola
  e motivata basta come punto di partenza; i confronti essenziali del PDF restano.

Il PDF richiede di cercare buoni iperparametri, non impone una particolare procedura
di cross-validation. Potete usare training/validation fissi e tenere separato il
test. Se scegliete CV, applicate le cautele sui fold descritte sotto.
Digest e revisioni sono note di riproducibilità, non un sistema da sviluppare.
Non sono richiesti una web app, un servizio di deployment o un'interfaccia per
l'analista: scenario di deployment e rinvio possono essere studiati nel notebook.

## Stato reale: cosa è già fatto e cosa manca

| File | Già disponibile | Ancora da svolgere |
|---|---|---|
| `src/data.py` | `load_dataset`, `encode_labels`, `LABELS`, `SEED` | Tutta l'analisi, tokenizzazione, rappresentazioni, analisi temporale e template. **Sezione 1 da fare.** |
| `src/supervised.py` | `create_random_split`, semplice divisione casuale per ID | Split temporale/per gruppi, classificatori, tuning, metriche, errori e test finale. **Sezione 2 da fare.** |
| `src/clustering.py` | Solo docstring di orientamento | Tutta la sezione 3. |
| `src/bert.py` | Solo docstring di orientamento | Tutta la sezione 4. |
| Notebook | Import e traccia degli esperimenti | Nessun risultato sperimentale. |
| Test | Utility iniziali verificate nella precedente ristrutturazione | Non attestano il completamento del progetto scientifico. |

Il dataset locale ora è presente: `data/ssh_attacks.parquet`. Nell'audit sono stati
letti solo i metadati: **233.035 righe**, quattro colonne:
`session_id` (int64), `full_session` (string), `first_timestamp` (string),
`Set_Fingerprint` (lista di stringhe).
**Usare `first_timestamp`: il PDF scrive `firsts_timestamp`.** Il PDF dice cinque
colonne ma ne elenca quattro; il file ne ha quattro. Qualità e contenuto sono da analizzare.

`load_dataset` legge il file e controlla ID/testi, senza pulizia o analisi.
`encode_labels` codifica collezioni già decodificate, senza verificare la correttezza
scientifica delle annotazioni. Lo schema permette di provare direttamente
`encode_labels(df['Set_Fingerprint'])`: verificare prima valori mancanti e nomi reali.
Un decoder di stringhe serve solo se emerge davvero una codifica diversa.

## Mappa completa della consegna

Ogni riga indica cosa produrre nel notebook e poi spiegare nel report. Le funzioni
riutilizzabili stanno nel modulo dello stesso proprietario.

| PDF | Chi / modulo / notebook | Evidenza richiesta |
|---|---|---|
| 1.1 | P1 / `data.py` / `01_data.ipynb` | Lunghezze caratteri/token definiti, elementi comuni, frequenze e co-occorrenze delle etichette, dimensioni dei label-set. |
| 1.2 | P1 / stessi file | Sessioni e composizione etichette nel tempo; popolazione contata, limiti dei testi distinti come frequenza di attacco, upgrade honeypot di novembre 2019. |
| 1.3 | P1 / stessi file | Politica per operatori, opzioni, path, indirizzi, quoting e case; esempi di perdita informativa con tokenizer ordinario. |
| 1.4 | P1 con P2 / `01_data.ipynb`, confronti predittivi anche in `02_supervised.ipynb` | Due rappresentazioni, almeno una count/TF-IDF; normalizzazione, informazione conservata/persa e discussione col docente. |
| 1.5 | P1 con P2 / `data.py` / `01_data.ipynb` | Gruppi di template senza etichette, esempi e controesempi; similarità testuale non dimostra stessa campagna/autore. |
| 2.1 | P2 / `supervised.py` / `02_supervised.ipynb` | Random, temporale e separazione per template; overlap, supporti, deployment plausibile e confronto col docente. |
| 2.2 | P2 / stessi file | Classificazione multi-label, confronto rappresentazioni/split; sbilanciamento, eventuali feature temporali, diversa popolazione/informazione disponibile. |
| 2.3 | P2 / stessi file | Tuning e prestazioni; supporti, etichette frequenti/rare e casi senza o con pochissimi positivi. |
| 2.4 | P2 / stessi file | Scenario scelto, pipeline congelata, test finale, errori rappresentativi e due pattern di fallimento; disaccordo distinto da sospetto errore del riferimento. |
| 3.1 | P3 / `clustering.py` / `03_clustering.ipynb` | Due similarità/rappresentazioni, principale e controllo di robustezza, discusse col docente. |
| 3.2 | P3 / stessi file | Almeno due algoritmi; distanze, riduzione, campionamento, iperparametri, rumore, budget e sessioni rappresentate. |
| 3.3 | P3 / stessi file | Selezione per qualità interna/stabilità/obiettivo senza etichette; confronto gruppi sotto ricampionamento o normalizzazione alternativa. |
| 3.4 | P3 / stessi file | Proiezione motivata e limiti, sessioni rappresentative e pattern discriminanti; word cloud solo accessorie. |
| 3.5 | P3 / stessi file | Conteggi e prevalenze multi-label con denominatori chiari, dimensioni, copertura e rumore. |
| 3.6 | P3 / stessi file | Stesso intent-set in gruppi diversi e gruppi con intent-set diversi; famiglie più fini con esempi e controesempi. |
| 4.1 | P4 / `bert.py` / `04_bert.ipynb` | Encoder preaddestrato adatto al testo shell, versione/provenienza e confronto col docente. BERT è una possibilità. |
| 4.2 | P4 / stessi file | Encoder congelato + testa addestrata contro fine-tuning parziale/completo; budget comune, parametri addestrabili, architettura, loss, attivazione e ottimizzatore. |
| 4.3 | P4 / stessi file | Troncamento contro chunking con tokenizer reale, aggregazione per sessione, chunk della stessa sessione nella stessa partizione. |
| 4.4 | P4 con P2 / `04_bert.ipynb`, baseline da `02_supervised.ipynb` | Confronto con baseline classica più forte su stessi ID, etichette e informazioni ammissibili; anche test finale. |
| 4.5 | P4 / `bert.py` / `04_bert.ipynb` | Errori per lunghezza/pattern/supporto e regola automatica di rinvio delle sessioni ambigue a un analista. |

## P1 — Dati, testo shell e rappresentazioni

**Primo passo:** caricare il file, guardare un campione, controllare annotazioni e
parsing/timezone di `first_timestamp`. Non serve aspettare gli altri per farlo.

Già disponibili in `src/data.py`:

```python
load_dataset(path: str | Path = 'data/ssh_attacks.parquet') -> pd.DataFrame
encode_labels(values: pd.Series) -> np.ndarray
```

Possibili funzioni da aggiungere nello stesso file:

```python
# TODO 1.3: una sessione -> token shell secondo regole esplicite.
def tokenize_shell(text: str) -> list[str]: ...

# TODO 1.4, opzionale: solo se confrontate testo raw e normalizzato.
def normalize_shell(text: str) -> str: ...

# TODO 1.1: tabella per sessione con ID, caratteri e numero di token.
def describe_sessions(sessions: pd.DataFrame) -> pd.DataFrame: ...

# TODO 1.1: frequenze, co-occorrenze e dimensioni dei label-set.
def summarize_labels(y: np.ndarray) -> dict[str, pd.DataFrame]: ...

# TODO 1.2: aggregati temporali con periodo, popolazione e denominatori dichiarati.
def summarize_over_time(sessions: pd.DataFrame, y: np.ndarray,
                        *, frequency: str) -> pd.DataFrame: ...

# TODO 1.4: trasformatore NON ancora addestrato; fit sui training fold a cura dell'utilizzatore.
def make_vectorizer(*, representation: str, **options) -> object: ...

# TODO 1.5: Series indicizzata per session_id, valori group_id; niente etichette in input.
def group_templates(sessions: pd.DataFrame, *, rule: str, **options) -> pd.Series: ...
```

`object` è un tipo provvisorio per un oggetto di libreria ancora da scegliere, non
una classe da inventare. Una volta scelta la libreria, precisate il tipo o usatela
direttamente. Le analisi usate una sola volta possono restare nel notebook.

**Passaggio agli altri:** ID originali, politica di testo/etichette, costruttori delle
rappresentazioni; a P2 anche gruppi di template. Non consegnare una TF-IDF adattata
su tutti i dati per valutare un classificatore. Documentare anche come viene definita
o stimata la regola dei gruppi: nessuna selezione guidata dalle etichette.

## P2 — Classificazione multi-label

**Primo passo:** progettare split e metriche e provare una baseline sul testo grezzo.
`create_random_split` divide gli ID: non addestra e non valuta alcun modello.

Firma già presente in `src/supervised.py`:

```python
create_random_split(session_ids: Sequence[int | str], *, seed: int = SEED,
                    validation_fraction: float = 0.2,
                    test_fraction: float = 0.2) -> dict[str, list[int | str]]
```

Possibili funzioni da aggiungere:

```python
# TODO 2.1: train prima di validation prima di test; definire date uguali/mancanti.
def create_temporal_split(sessions: pd.DataFrame, *, validation_fraction: float = 0.2,
                          test_fraction: float = 0.2) -> dict[str, list[int | str]]: ...

# TODO 2.1: ogni gruppo interamente in una partizione.
def create_group_split(sessions: pd.DataFrame, groups: pd.Series, *, seed: int = 42,
                       validation_fraction: float = 0.2,
                       test_fraction: float = 0.2) -> dict[str, list[int | str]]: ...

# TODO 2.1: copertura, overlap, date/gruppi e supporti per etichetta.
def audit_split(sessions: pd.DataFrame, y: np.ndarray,
                split: dict[str, list[int | str]], *, groups: pd.Series | None = None) -> pd.DataFrame: ...

# TODO 2.2: pipeline testo -> rappresentazione -> classificatore multi-label.
def make_classifier(vectorizer: object, *, model: str, **options) -> object: ...

# TODO 2.3: possibile helper se scegliete CV; non obbligatorio.
# In alternativa confrontate poche impostazioni su training/validation fissi nel notebook.
def tune_classifier(pipeline: object, train_texts: pd.Series, y_train: np.ndarray,
                    *, search_space: dict, cv: object, scoring: str) -> object: ...

# TODO 2.3–2.4, condivisibile con P4: decisioni booleane (N,7) -> metriche e supporti.
def evaluate_multilabel(y_true: np.ndarray, y_pred: np.ndarray) -> dict: ...

# TODO 2.4: tabella ID/testo/riferimento/predizione per ispezionare i disaccordi.
def inspect_errors(sessions: pd.DataFrame, y_true: np.ndarray,
                   y_pred: np.ndarray) -> pd.DataFrame: ...
```

Il modello lo scegliete voi. La divisione 60/20/20 è un default modificabile, non
una richiesta della consegna. Se usate CV, rifate il fit delle trasformazioni dentro
ogni fold e rispettate l'impostazione temporale/per gruppi quando pertinente.
Concordate metriche micro/macro/per-label, supporti, casi indefiniti e gestione dello
sbilanciamento. Soglie e iperparametri si scelgono senza usare il test.

**Passaggio a P4:** manifest degli ID, politica di valutazione e soglie, baseline
selezionata e risultati allineati. Ogni strategia ha il proprio manifest; P2 e P4
condividono quello usato nel confronto. Non servono gli stessi manifest per strategie diverse.

## P3 — Clustering e famiglie comportamentali

**Primo passo:** definire due idee di similarità e un budget su un campione dichiarato.
Non si selezionano cluster per imitare gli intenti: le etichette si guardano dopo.

Possibili funzioni in `src/clustering.py`:

```python
# TODO 3.1–3.2: X dalle rappresentazioni P1 o da alternative motivate.
# Assegnazioni (N,) e oggetto stimato; dichiarare valore di rumore.
def cluster_sessions(X: object, *, algorithm: str, seed: int = 42,
                     **options) -> tuple[np.ndarray, object]: ...

# TODO 3.3: qualità interna; gestire rumore, cluster unico e budget del calcolo.
def evaluate_clusters(X: object, cluster_ids: np.ndarray) -> dict[str, float]: ...

# TODO 3.3: Series sugli stessi ID; allineare gli ID comuni nei ricampionamenti.
# I numeri dei cluster sono arbitrari: non confrontarli con uguaglianza diretta.
def compare_clusterings(first: pd.Series, second: pd.Series) -> dict[str, float]: ...

# TODO 3.4: coordinate (N,2); il grafico non dimostra la qualità del clustering.
def project_sessions(X: object, *, method: str, seed: int = 42,
                     **options) -> np.ndarray: ...

# TODO 3.4 e 3.6: esempi rappresentativi e pattern con criterio esplicito.
def describe_clusters(sessions: pd.DataFrame, X: object,
                      cluster_ids: np.ndarray) -> pd.DataFrame: ...

# TODO 3.5: solo dopo selezione; conteggi, prevalenze, dimensioni e rumore.
def summarize_cluster_labels(cluster_ids: np.ndarray, y: np.ndarray) -> dict[str, pd.DataFrame]: ...
```

Nel notebook confrontate almeno due algoritmi, due similarità, stabilità e
interpretazione. Evitate matrici complete di distanze su tutto il dataset senza
stimare i costi. Se cambiate campione/normalizzazione, dichiarate sessioni rappresentate
e modalità di confronto. Distinguete analisi transduttiva da valutazione induttiva.

**Consegna agli altri/report:** assegnazioni con ID, copertura/rumore, selezione,
figure e famiglie supportate da esempi e controesempi, senza attribuzioni non dimostrate.

## P4 — Encoder contestuali, incluso BERT

**Primo passo:** verificare encoder/tokenizer e budget. Potete farlo mentre P2 prepara
la baseline; i confronti scientifici attendono split e politica etichette condivisi.

Possibili funzioni in `src/bert.py`:

```python
# TODO 4.1: encoder/tokenizer della stessa revisione, provenienza registrata.
def load_encoder(model_name: str, *, revision: str) -> tuple[object, object]: ...

# TODO 4.3: tabella chunk con session_id e token; policy = truncation o chunking.
# Gestire token speciali/overlap e tenere i chunk nella partizione del genitore.
def prepare_inputs(sessions: pd.DataFrame, tokenizer: object, *, policy: str,
                   max_length: int, stride: int = 0) -> pd.DataFrame: ...

# TODO 4.2: encoder congelato o fine-tuning; selezione sulla validation, mai sul test.
# Input di training/validation con label allineate; motivare il peso delle sessioni lunghe.
def train_contextual(encoder: object, train_inputs: pd.DataFrame,
                     validation_inputs: pd.DataFrame, *, mode: str,
                     seed: int = 42, **options) -> object: ...

# TODO 4.3: righe chunk, session_id e sette score nell'ordine LABELS.
def predict_chunks(model: object, inputs: pd.DataFrame) -> pd.DataFrame: ...

# TODO 4.3–4.4: una riga per sessione; specificare significato score e aggregazione.
def aggregate_session_scores(chunk_scores: pd.DataFrame, *, method: str) -> pd.DataFrame: ...

# TODO 4.5: flag per ID; regola e soglia scelte sulla validation.
def flag_for_review(session_scores: pd.DataFrame, *, rule: str,
                    threshold: float) -> pd.Series: ...
```

Anche qui potete usare direttamente gli strumenti della libreria. Rendete espliciti
testa multi-label, loss, attivazione, ottimizzatore, parametri addestrabili e budget.
Logits/margini non sono probabilità; aggregazione e conversione score→decisioni
vanno dichiarate. Riutilizzate le metriche P2; valutate per sessione, non per chunk.
Per il rinvio ad analista misurate copertura/qualità: incertezza non dimostra errore
del riferimento. Confrontate congelato/fine-tuning e truncation/chunking sotto budget.

**Consegna:** revisioni/settings, confronti e test sugli stessi ID della baseline P2,
costi ed errori rispetto a lunghezza, pattern e supporto delle etichette.

## Poche convenzioni per lavorare insieme

| Oggetto | Convenzione iniziale |
|---|---|
| Sessioni | DataFrame con ID originali; mantenere relazione ID↔testo. |
| Etichette | `y` booleano `(N,7)` nell'ordine `src.data.LABELS` e delle sessioni. Mancante non significa insieme vuoto. |
| Split | Dizionario `train`, `validation`, `test` di ID; salvare manifest. |
| Feature | Matrice densa/sparsa e ID delle righe conservati a parte; fit nei soli dati ammessi. |
| Predizioni | ID, score `(N,7)`, decisioni booleane `(N,7)`; significato score e soglie documentati. |
| Cluster | ID e gruppo; rumore, esclusioni e copertura dichiarati. |
| Riproducibilità | Seed iniziale 42 modificabile, digest dataset, manifest, settings, revisioni codice/librerie/modelli e costi. |

Esempio già eseguibile dalla radice con dipendenze installate:

```python
from src.data import load_dataset, encode_labels
from src.supervised import create_random_split

sessions = load_dataset()
y = encode_labels(sessions['Set_Fingerprint'])
split = create_random_split(sessions['session_id'].tolist())
# Solo caricamento, codifica e divisione. Nessun modello addestrato.
```

Se filtrate o riordinate `sessions`, riallineate `y`: NumPy non conserva gli ID.
Non eseguite il testo delle sessioni. Le annotazioni automatiche sono un riferimento
fisso: riportate accordo con il riferimento, sospetti errori a parte senza relabeling
silenzioso del test. Harmless non significa che la sessione complessiva sia benigna.

## Sviluppo parallelo e sei settimane indicative

P1 fornisce presto un campione verificato; P2 può partire da testo grezzo e metriche;
P3 lavora su similarità e campioni dichiarati; P4 verifica encoder e compute.
P1/P2 si coordinano su template e fit delle feature senza attendere la fine delle
rispettive sezioni. P3 non aspetta il classificatore; P4 aspetta la baseline solo
per il confronto finale. Usate fixture sintetiche per prove tecniche, non risultati scientifici.

Cambiare firme, algoritmo o organizzazione è normale: avvisate chi usa i vostri
output e aggiornate i documenti quando utile. Potete tenere codice esplorativo nel
notebook o aggiungere un modulo se emerge un bisogno concreto. Restano da coprire
il PDF e i confronti col docente su rappresentazioni, split, similarità, encoder,
scenario di deployment ed errori prioritari.

Scadenza ufficiale non confermata: settimane relative all'avvio, da adattare.

| Settimana | Traguardo possibile |
|---|---|
| 1 | Campione/schema verificati; obiettivo, deadline, template, budget e scelte iniziali col docente. |
| 2 | Analisi/tokenizer/rappresentazioni in corso, split auditati, pilot clustering/encoder. |
| 3 | Baseline classiche, due clustering pilota, encoder congelato con testa addestrata. |
| 4 | Tuning, stabilità cluster, fine-tuning e confronto input lunghi entro budget. |
| 5 | Scelte congelate prima del test, valutazione finale, confronto P2/P4 ed errori. |
| 6 | Notebook riproducibili, report Overleaf, revisione checklist e consegna. |

Create `results/` quando ci sono output reali: salvate manifest/settings e condividete
solo artefatti adatti. Ogni proprietario scrive metodo, risultati e limiti nel report;
tutti rivedono insieme l'intero progetto. Il template LaTeX non è ancora disponibile.
