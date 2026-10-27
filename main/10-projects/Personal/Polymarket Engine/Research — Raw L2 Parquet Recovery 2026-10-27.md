---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
  - "[[Research — Historical L2 Forensic Validation 2026-09-21]]"
  - "[[Research — Historical Data Acquisition ADDENDUM 2026-09-21]]"
aliases:
  - "Raw L2 Parquet Recovery 2026-10-27"
tags:
  - kind/doc
  - tech/polymarket
  - topic/research-ops
created: "2026-10-27"
updated: "2026-10-27"
---

# Research — Raw L2 Parquet Recovery 2026-10-27

## Propósito

- Registrar el shot W1-a del 2026-10-27: recuperación exacta de los dos Parquet raw v3 de PendulumFlow (horas `2026-09-01T21` y `T22`) que el cierre W0 dejó como brecha abierta (manifiestos verificados, sin HEAD de objetos ni descarga). Resultado del shot: downloader puntual implementado en el paquete W1-a y ejecución **BLOCKED** por el gate de permisos de la superficie; nada fue descargado ni hasheado localmente. Este informe no certifica integridad local, reconstrucción del histórico, código ni rendimiento, ni declara edge, rentabilidad ni causalidad reproducida.

## Contenido

- **Autoridad y límites vigentes:** mandato del Owner del 2026-10-27 (registrado en §18 de [[Polymarket Engine — Continuidad Five-POC 2026-09-20]]): se reabre sólo ingeniería/research offline; el freeze `PROJECT_FROZEN_OWNER_2026_09_23` permanece como historia de producto. Sin transacciones, conexión a cuentas, wallet, fondos, firma, órdenes, activación live, despliegue, push/merge/publicación ni compra. El OOS (ATL 3901955 y SEA 3901953, kickoff 22:45Z) sigue sellado y no fue leído. Daedalus no autorizado y no accedido por ninguna ruta.
- **Verificado físicamente en esta sesión (ZCode × GLM-5.3-Flash, sess_92fef7f2-4f4c-492e-8937-3d0c5cc3f28a):** host `sqx-ulab-hefesto-0` (comando `hostname`); volumen destino con 73 GiB libres; `validated-baseline/w1-a/` vacío al inicio; re-lectura de los manifiestos W0 en `validated-baseline/w0/archive-manifest-check/` (`summary.md`, `t21.meta.json`, `t22.meta.json` y manifiestos saneados), que registran HTTP 200 con TLS por defecto, `served_verbatim=true`, `layout=union-event-sorted-v1`, `row_count` 80010651 / 53564796, `bytes` 866445402 / 595930005 y `sha256` `ee4c5add…` / `5cd4e6b1…`, con `published_urls` vacío. El preflight de red de Luna (HEAD T21 resuelto a `dl.pendulumflow.com` con `Content-Length: 866445402`; HEAD T22 con 429) es declaración del lanzador, no una re-verificación de esta sesión.
- **Implementación (creada, no ejecutada):** `validated-baseline/w1-a/recover_exact_raw.py` materializa el downloader puntual autorizado por el mandato: re-obtención y copia exacta de ambos manifiestos con validación de campos publicados (`served_verbatim`, `layout`, filas, bytes, sha256, `file`); revalidación HEAD de ambos objetos registrando status, redirección final, tipo, longitud, ETag y `Retry-After` observados; descarga secuencial streaming a `.part` con `CHUNK = 1024 * 1024` y `response.read(CHUNK)` con SHA-256 incremental; promoción al nombre final sólo si tamaño y hash medidos coinciden exactamente; política de no-sobrescritura con reuse-and-verify y parada ante conflicto; un único intento diferido ante 429 respetando `Retry-After` (tope 300 s, nunca un bucle); checkpoint recuperable y cierre ordenado ante SIGINT; e inspección footer-only de metadatos Parquet (pyarrow o duckdb) sin cargar filas, con `NOT_RUN` motivado si no hay herramienta. Entradas: sólo los cuatro URL del mandato; TLS verificado por defecto; escrituras sólo dentro de W1-a.
- **Ejecución: BLOCKED (causa precisa):** el scope de permisos Bash de la superficie denegó el comando autorizado exacto `python3 /home/kor/Documents/Codex/2026-10-27/task-2/validated-baseline/w1-a/recover_exact_raw.py` (también en su variante relativa desde el checkout) con el mensaje `Outside W0, Polymarket project, required Agents-OS instruction, or canonical closeout scope`, mientras que el materializador canónico del vault sí pasó y las herramientas Write/Edit hacia W1-a funcionaron. En la primera mitad de la sesión el cliente de permisos estuvo ausente y toda operación mutadora fue denegada. Siguiendo la instrucción explícita del lanzador no se hicieron bucles de reintento por permisos: se cerró BLOCKED. Los cuatro URL autorizados no fueron accedidos por esta sesión.
- **Integridad por objeto: NOT_RUN.** Para `2026-09-01T21.parquet` y `2026-09-01T22.parquet` no hay bytes ni SHA-256 medidos localmente en este shot; los valores publicados (866445402 y 595930005 bytes; `ee4c5add7d23cda375beaeafa0833969059e3d7ad0c5bf246d20b4eb9316c4d3` y `5cd4e6b10bba51f9d54d6ac16637a1009b7ef824c4ed21b4fdaadf8787925dd9`) provienen de los manifiestos remotos observados por W0 y del mandato, no de verificación local. No existe `recovery-manifest.json` ni copias nuevas de manifiesto: el paquete W1-a contiene sólo el script.
- **Procedencia y límites de lo histórico:** recuperar estos dos Parquet raw no recupera el directorio histórico `hist-acq-20260921`, ni `rs-v03`, ni `pe001`; siguen sin evidencia local de recuperación. El ADDENDUM 2026-09-21 ([[Research — Historical Data Acquisition ADDENDUM 2026-09-21]]) informó mismatch BBA 66–85% y `L2_SNAPSHOT_ONLY` usando un reconstructor aditivo sin deletes; la revisión forense posterior ([[Research — Historical L2 Forensic Validation 2026-09-21]]) lo corrigió con semántica upsert/delete size=0 por asset y orden venue-time, con BBO 0/628 intervalos y 514/516 de acuerdo contra la traza `best_bid_ask`. Esa corrección no certifica el código actual, la reconstrucción íntegra del histórico ni rendimiento, y no habilita economía certificada ni live.
- **Siguiente paso causal concreto:** (1) el lanzador agrega a los settings scoped la entrada Bash exacta del downloader y re-despacha este shot W1-a (el script es idempotente: reuse-and-verify, promoción por tamaño+SHA y `recovery-manifest.json` nuevo); (2) con ambos Parquet verificados localmente, replay temporal offline del cohort (deletes size=0, verificación BBO por snapshot, ventana de incidente venue 22:30–22:40Z marcada) antes de elegir como máximo dos hipótesis; (3) `rs-v03`/`pe001` requieren su propia evidencia de recuperación con MANIFEST/SHA256SUMS y mapeo. Los gates humanos (elegibilidad, cuenta, fondos, riesgo, arming, live) siguen cerrados.

## Fuentes

- Mandato W1-a del Owner del 2026-10-27 (vía lanzador) y §18 de [[Polymarket Engine — Continuidad Five-POC 2026-09-20]].
- `validated-baseline/w0/archive-manifest-check/`: `summary.md`, `t21.meta.json`, `t22.meta.json`, `t21.manifest.sanitized.json`, `t22.manifest.sanitized.json` (observaciones W0, atribuidas a esa sesión).
- [[Research — Historical L2 Forensic Validation 2026-09-21]] y [[Research — Historical Data Acquisition ADDENDUM 2026-09-21]].
- Manifiestos remotos `https://archive.pendulumflow.com/v3/2026-09-01/21/manifest.json` y `.../22/manifest.json` y objetos `2026-09-01T21.parquet` / `2026-09-01T22.parquet` (no accedidos por esta sesión debido al bloqueo; preflight de red atribuido a Luna).
- Registros de esta sesión: [[2026-10-27-polymarket-w1a-raw-recovery-summary]], [[2026-10-27-polymarket-w1a-raw-recovery-session-feedback]], [[2026-10-27-zcode-glm-5.3-flash-polymarket-w1a-raw-recovery]], [[2026-10-27-polymarket-engine-entity-updated]].
