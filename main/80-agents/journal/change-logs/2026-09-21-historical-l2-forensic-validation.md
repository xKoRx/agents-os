# Change log — Historical L2 Forensic Validation (2026-09-21)

Sesión: one-shot `HISTORICAL_L2_FORENSIC_RESULT` sobre el dataset `hist-acq-20260921` (sin código engine modificado ni publicado; Sports Week intacto; OOS sellado).

## Cambios Sistema 2 (vault)

- Nueva nota: `10-projects/Personal/Polymarket Engine/Research — Historical L2 Forensic Validation 2026-09-21.md` (materializada con `materialize_schema_note.py`, tipo `doc` — el tipo `research` del addendum previo no está contratado). Contiene causa demostrada del drift, categorías de discrepancia con ejemplos reproducibles, resolución utilizable, veredicto PE-005-R1, benchmark de cadena completa, estado de almacenamiento y decisión `L2_RECONSTRUCTIBLE`.
- Parche correctivo: `Research — Historical Data Acquisition ADDENDUM 2026-09-21.md` — callout de corrección forense tras la intro (supersa hallazgo #6 y etiqueta `L2_SNAPSHOT_ONLY` en su fundamentación; el resto queda como registro histórico).
- Continuidad: `Polymarket Engine — MVP.md` — bullet nuevo al tope de `## 📊 Estado actual` (`L2_RECONSTRUCTIBLE`) y entrada nueva de bitácora (`HISTORICAL_L2_FORENSIC_RESULT`) sobre la entrada de adquisición (que quedó intacta tras reparación de edición).

## Cambios fuera del vault

- Workspace forense nuevo (fuera de VAULT_ROOT, regla constitución 12): `~/aranea/work/hist-l2-forensic-20260922/` — scripts `recon.py` (variantes sort/semántica), `drill.py` (residuos), `bba_check.py` (cross-validación + witness/skew), `cut_states.py` (30 cortes corregidos, digest `c5f3b52b…`); `data/cohort_full.ndjson` (89.718 eventos, 2h completas, 7 tipos de evento con campos de witness, derivado de parquets con sha verificado); `results/` (variantes v1-v8, `SAMPLE_REQUESTS.md` con solicitudes PMData/polymarketdata.co, `cut_states_upsert.json`).

## Decisiones registradas

- Decisión de datos: `L2_RECONSTRUCTIBLE` para era v3 bajo protocolo obligado (upsert, per-asset, venue-time, verificación por snapshot, incidente 22:30-22:40Z marcado). El `SNAPSHOT_ONLY` del addendum queda supersado en su fundamentación; sin compra necesaria para L2 del era v3.
- Almacenamiento: MinIO homelab operativo pero NO autorizado para este dataset (sin bucket/policy polymarket; freeze `STORAGE-ORGANIZATION-FREEZE` de BACKUP-DR activo) → preservación local única; raw re-descargable (sha=publicador); derivados sin segunda copia (bloqueo exacto documentado en la nota forense §6).
- Muestras multi-proveedor: solicitudes preparadas, no enviadas (PMData requiere cuenta owner; polymarketdata.co contacto enterprise); sin compras ni condiciones aceptadas.

## Evidencia clave (hashes/números)

- BBO mismatch: 0/628 (2h) y 0/536 (ventana); profundidad exacta 92,04%/97,39%; bba cross-val 514/516 (99,61%).
- Cert original vs correcto: 117/138 vs 0/69 (19a016da); `levels_diff` cert 1.191-2.072 vs modelo aditivo 1.242-2.148.
- Residuo real: 50/628 intervalos con 1-2 niveles divergentes (66 niveles); ejemplo BUY 0.02 `1fc6d5c6` 15.290,55→30,55 sin delta (21:45:38Z→21:49:36Z).
- Dedup: 0 duplicados; `sequence` collector-local (2,81e14 vs 5,3e16); arrival skew books p50 43 ms / máx 674 s.
- Cadencia snapshot: mediana 13,5-67,4 s, máx 7,8-13,7 min; incidente venue restart CLOB 22:30→23:54Z (manifests + /audit del archive).
