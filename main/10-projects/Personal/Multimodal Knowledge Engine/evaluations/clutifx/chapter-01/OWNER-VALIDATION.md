# OWNER-VALIDATION — Clutifx Chapter 01

**Estado: la comparación manual planned no es posible en esta corrida.** El engine no publicó ningún claim/relation/SKO (FATAL contractual @ w0003; ver `OMISSIONS.md`). No hay extracción canónica contra la cual validar el capítulo completo.

Lo único revisable del L1 son los **proposals NO committeados** de las 3 ventanas reconstruidas (00:00–00:42): respuestas del provider en el journal, rechazadas por el engine antes de publicar. Si el Owner quiere calibrar la calidad del modelo en esa franja corta, puede usar la tabla de abajo; su veredicto NO representa la extracción del capítulo.

## Tabla de validación (opcional, sólo franja 00:00–00:42)

| Interval | MKE extraction (proposals, NO canónico) | Owner verdict | Missing? | Wrong? | Notes |
|---|---|---|---|---|---|
| 00:00–00:14 (w0001) | 11 claims + 1 relation propuestos; detalles en `provider-requests.jsonl` (target `w0001`) | | | | |
| 00:14–00:35 (w0002) | 31 claims + 2 relations propuestos; detalles en `provider-requests.jsonl` (target `w0002`) | | | | |
| 00:35–00:42 (w0003) | 14 claims + 1 relation propuestos; run FATAL al commit por divergencia de `cl-chart-instrument-eurusd@1` con w0002 | | | | |
| 00:42–34:03.9 (w0004–w0130) | NO PROCESADO | | | | |

Columnas del Owner dejadas vacías a propósito; sin autoevaluación.

## Material de apoyo para el Owner

- `transcript.json` — transcript completo del capítulo (323 segmentos, id/start_ms/end_ms/text) para revisar el capítulo contra texto sin depender sólo del video.
- `review-evidence/` — los 24 frames de w0001–w0003 con `MANIFEST.json` (evidence id → timestamp).
- VIDEO original: `~/mke/course/ep01-intro.mp4` (no versionado).

## Qué se necesita para reintentar la validación completa

Una corrida full-chapter que llegue a publicación requiere resolver el bloqueo de identidad documentado en `OMISSIONS.md` (decisión Owner + Primary Manager; esta corrida no modificó producto ni diseño).
