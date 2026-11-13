# Dataset locale

Il dataset reale e presente in `data/ssh_attacks.parquet` ed e ignorato da Git.
`src.data.load_dataset()` lo legge con pandas/PyArrow; accetta anche un altro percorso.
Non eseguire mai il testo delle sessioni.

## Schema verificato dai soli metadati

- 233.035 righe; `session_id`: int64; `full_session`: string.
- **`first_timestamp`: string**, non `firsts_timestamp` indicato nel PDF.
- `Set_Fingerprint`: lista di stringhe, riferimento multi-label fornito.

Il PDF dice cinque colonne ma ne elenca quattro: il file ne ha quattro.
Il parsing dei timestamp, timezone, valori mancanti e qualita dei contenuti restano
compiti P1. La verifica dello schema non equivale a un'analisi del dataset.

`encode_labels(df["Set_Fingerprint"])` accetta collezioni gia decodificate;
verificare nomi reali e mancanti prima dell'uso. Non serve introdurre un decoder di
stringhe se il formato reale non lo richiede. Mancante non significa insieme vuoto.
Le annotazioni automatiche sono un benchmark fisso: riportare accordo col riferimento,
separando sospetti errori senza modificarlo silenziosamente. Harmless non indica
che la sessione complessiva sia benigna. ID e ordine LABELS devono essere preservati.

Per la divisione del lavoro e le funzioni suggerite leggere PLAN.md.
