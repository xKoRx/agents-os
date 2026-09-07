---
type: decision
scope: public
created: 2026-07-26
updated: 2026-07-26
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[EchoForgeTradeListExporter]]"
entities:
  - "[[TradeListArtifactWriter]]"
  - "[[TradeManifestRepository]]"
  - "[[ProjectActivity]]"
related:
  - "[[Echo Forge - Cierre de Etapa 4]]"
  - "[[Echo Forge - Cierre de Etapa 4]]#Fase 3 (T3.1-T3.7)"
aliases:
  - trade-list-package-complete
  - mongo-unique-scope-natural
  - nonretryable-trade-error
  - import-from-minio
confidence: verified
source_session: 2026-07-26-g3-rework-t3.7
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - tech/sqx
  - tech/minio
  - tech/mongo
  - tech/temporal
  - tech/idempotency
  - tech/contract
  - scope/public
---

# Trade list — paquete completo, índice Mongo único, error tipado NonRetryable, import desde objeto remoto

## Contexto

G3 (F3 de `[[Echo Forge - Cierre de Etapa 4]]`) rechazó el primer cierre del paquete
§8.4 con seis blockers: la mitad Symphony/Go del contrato estaba cubierta en
aspectos unitarios pero el wiring completo (subir paquete MinIO completo,
índice Mongo anti-colisión, taxonomía Temporal cableada, import real desde
el remoto) tenía gaps. Cada gap, además, era visible como "2/3" en el
handoff aunque el veredicto era "FAIL".

## Decisión

Cierra los seis blockers con cambios estructurales — no parches cosméticos:

1. **Paquete MinIO completo (R2)** — `UploadScopeArtifacts` sube, en cada
   llamada idempotente, tres objetos bajo la misma base key:
   `trades.v1.ndjson.gz` (gzip del NDJSON canónico), `trade-manifest.v1.json`
   (envelope JSON con `manifest + encoded_at_utc + encoding_strategy`), y
   `_SUCCESS` (cuerpo vacío). El sidecar y el sentinel NO se asume que se
   suben "aguas abajo" del writer; el propio writer es responsable de
   cerrar el paquete.

2. **Size mismatch → re-upload (R4)** — el switch de 3 ramas en
   `UploadScopeArtifacts` clasifica el match contra el remoto sólo como
   noop cuando (a) ETag coincide por SHA-256 o (b) los tamaños coinciden en
   modo large sin digest. Cualquier divergencia cae al camino de
   `PutObject` (re-upload). Ningún tamaño distinto se traduce en
   `ErrTradeContract`.

3. **Índice Mongo único sobre scope natural completo (R3)** —
   `TradeListRepository.EnsureIndexes` crea `uniq_scope_natural_v1`
   (`wave + request + run + strategy + stage + variant + result + cell +
   sample`) y `wave_stage_variant` como secundario para `ListByWave`. El
   filtro de `UpsertManifest` ya usaba los 9 campos — ahora el índice
   subyacente coincide.

4. **Import desde el objeto remoto (R5)** — `import_trade_list` deja de
   leer el archivo local; llama `caps.TradeArtifactReader.DownloadNDJSON`
   (que verifica SHA-256 contra `ref.ArtifactSHA256`) y decodifica el
   archivo descargado. `pipeline.Capabilities` gana `TradeArtifactReader`
   además del ya existente `TradeArtifactWriter`.

5. **`act_upsert_trade_list` registrado (R1)** — `cmd/sqx-worker/main.go`
   registra la activity standalone con `activity.RegisterOptions{Name:
   "act_upsert_trade_list"}`. `ProjectActivity.UpsertTradeList` envuelve
   errores contract en `*nonRetryableTradeError` preservando
   `errors.Is(err, sqxcore.ErrTradeContract)`. El wrap es reversible: si
   el workflow declara ese type en `NonRetryableErrorTypes`, Temporal
   respeta la regla; si no, `errors.Is` sigue funcionando en cualquier
   caller (tests incluidos).

6. **`*nonRetryableTradeError` es type wrapper (R1 finer point)** — el
   wrap se eligió tipo de dato, no string. `NonRetryableErrorTypes` exige
   tipo, no mensaje; comparar contra `"core: trade contract violation"`
   (string del sentinel) es frágil si el logger prepende `[feature=…]`.

## Rationale

- **Paquete completo en una sola llamada**: si `uploadCompanions` falla a
  mitad, `UploadScopeArtifacts` retorna transient; la activity Temporal
  reintenta, vuelve a subir los companions idempotentes sin duplicar el
  NDJSON (éste ya está idempotente), y cierra el paquete sin ventana de
  inconsistencia.
- **Sin `ErrTradeContract` por tamaño**: el tamaño puede divergir por
  exports anteriores truncados o por cambios legítimos en el plugin;
  clasificar esto como contrato significa "no se puede arreglar", lo que
  miente sobre el sistema. Re-upload y verificación SHA-256 al read es la
  verdad técnica.
- **Índice natural completo**: ya se filtraba por los 9 campos; sin el
  índice único Mongo permite inserts paralelos que violan la
  idempotencia del upsert. La opción `wave+strategy+stage` era un atajo
  que rompía multi-run/multi-variant/multi-sample.
- **Import desde MinIO (no local)**: si un workflow fue interrumpido entre
  upload e import, el local puede haber sido borrado por cleanup;
  leerlo validaría un archivo que el remoto no tiene. Descargar y
  verificar SHA-256 contra `ref.ArtifactSHA256` cierra la cadena
  end-to-end.
- **Doble entrypoint registrado + wrap por type**: el patrón
  "método en ProjectActivity + RegisterActivityWithOptions" replica la
  convención que `cmd/sqx-worker/main.go` ya usa para las otras
  activities; no introducir un archivo `trade_list_activity.go` separado
  evita una superficie de DI nueva. El wrap `*nonRetryableTradeError`
  separa "el workflow sabe que no debe reintentar" de "el código de
  negocio clasifica el error".

## Consecuencias

- **Positivas**: paquete siempre completo (NDJSON + manifest + sentinel);
  re-upload por size mismatch bajo la misma key; sin colisiones por run/
  variant/sample en Mongo; import que valida lo subido, no un archivo
  local posiblemente stale; Temporal recibe un type estable para su retry
  policy.
- **Operacional**: tests `storage-minio` subieron a 7 PASS, sin `t.Skip`
  (placeholder `TestE2E_Stat_WithFakeMinIO` reemplazado por comentario
  trazable al handoff, no por un test vacío). Cobertura:
  `pipeline/builder`, `steps/trade_lists`, `project_activity_trade_list`,
  `storage-minio/trade_lists`, `metadata-mongo/trade_lists`,
  `core/trades`, `core/capabilities`, `core/errors` — todas verdes
  (`GOWORK=off go test`).
- **Negativas / gaps declarados honestamente (R-A/R-C, TB-2)**:
  - `WorkflowOptions.NonRetryableErrorTypes` con `*nonRetryableTradeError`
    en el lado workflow no se aplica en esta iteración (queda en `TB-2`).
    El wrap ya cubre el camino activity; cubre el workflow sólo si el
    caller lo declara explícitamente.
  - Smoke SQX Build 142 real (defer desde G2) sigue diferido.
  - Round-trip Mongo real con docker-compose (CI) sigue diferido.

## Alternativas descartadas

- **Subir manifest y `_SUCCESS` en steps separados del pipeline**: el
  step que sube NDJSON nunca sabría si el paquete quedó completo.
  Rompe la atomicidad observada y permitiría que un workflow
  interrumpido dejara NDJSON sin sentinel.
- **Tamaño distinto → `ErrTradeContract`**: clasifica como bug
  permanente un fallo temporal (export interrumpido, gzip truncado).
  Re-upload + verificación SHA al read es la verdad.
- **Índice Mongo parcial sobre `wave+strategy+stage`**: cubre el caso
  feliz pero permite colisiones reales entre run_id/variant/sample_type/
  cell_key distintos — el plan §8.4 advertía este DoD.
- **Import desde archivo local**: ya justificado arriba (cleanup
  windows pueden borrar el archivo entre upload e import). El download
  desde MinIO + verificación SHA es la verdad.
- **Wrap de NonRetryableError por string (texto del sentinel)**: frágil
  ante cualquier transformación que pade el log o el bug tracker;
  comparar por type wrapper es estable y extensible (cualquier nueva
  category de error se materializa como type nuevo).
