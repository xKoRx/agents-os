---
type: session
schema_version: 1
scope: session
created: "2026-10-31"
updated: "2026-10-31"
area:
project:
application:
entities: []
related: []
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-10-31-polymarket-w1o-fee-inventory-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Auditar en lectura offline la identidad de fee del mercado objetivo `5784455` y sus dos assets en el episodio exploratorio W1-j, pasándola por el `FeeResolverV1` existente, sin certificar la fee de settlement y sin tocar OOS, cuentas, credenciales, L ni parámetros.

## Contexto cargado

- Entidad [[Polymarket Engine — MVP]] y su continuidad (cierre W1-nR); notas de research W1-j (modo identity, gate OOS id-first) y W1-nR (tabla de fees con la metadata del objetivo no inspeccionada).
- Metadata autorizada del lote 3: `selection-manifest-identity.json`, `prepared-plan-identity.json`, `identity-evidence.json` (hashes verificados).
- Código: `internal/capture` (`OpenView` read-only), `internal/protocol` (parsers Gamma/CLOB/Market WS), `internal/regimes` (`FeeResolverV1`, reducer), `cmd/engine/clob_observe.go`, `cmd/researchpilot` (discovery y economics).
- Sin bootstrap adicional ni scouts nuevos: el stack de la sesión (14 ventanas verificadas) se reutilizó y el scouting fue `inline-fallback` con pack en `scout-pack.json`.

## Trabajo realizado

- Se escribió `cmd/feeinventory` (extractor offline) reutilizando `capture.OpenView` + los parsers existentes + `regimes.ResolveFee`: lee el journal, verifica la identidad del target contra el propio journal, separa las tres identidades de fee (declared/limit de mercado y de assets, trade-informed, settlement) y falla cerrado si la identidad no se confirma.
- Correcciones de semántica causal en las descripciones emitidas: el ancla `as_of_kickoff_K` es el estado **conocido hasta K** (no habilita decisiones anteriores ni fee retroactiva); `source_as_of_raw` (updatedAt/gst/timestamp de evento) se preserva crudo sin acreditar fee-effective-as-of ni vigencia; `known_at_utc` se deriva de `Envelope.ReceivedWall` como reloj observado de recepción, con `capture_seq` como prueba de orden/durabilidad y corte.
- Finding de revisión corregido: el agregado de lexemas trade-observados perdía el `asset_id` al aplanarse (dos assets pueden compartir lexema); se añadió `asset_id` a la fila y un test sintético que falla si se pierde la atribución o se mezclan conteos.
- Verificación: test focal `./cmd/feeinventory` **13 PASS** (exit 0), `gofmt` limpio, build exit 0; luego una única corrida del extractor sobre el episodio W1-j (sin reintentos, sin requests).
- Resultado medido: 9236 registros leídos, 0 errores de parseo, 102 observaciones fee relevantes; cap declarado 1000 bps (maker/taker) y `fees_enabled=true` en 8 lecturas; `fd`/`r` crudos; 78/78 trades con `fee_rate_bps="0"` (60 en un asset, 18 en el otro); declared → INTERVAL [0,1000], trade-informed → POINT 0 bps, settlement → NOT_CERTIFIED, `REAL_FEE_READY=false`.

## Artifacts creados o modificados

- Código: `cmd/feeinventory/main.go` (sha256 `39305a69…`) y `cmd/feeinventory/main_test.go` (sha256 `a473635c…`), commit local `7c9adaea59251b39ac1559db1ed63d4566996206` en `w0/offline-causal-replay-20261027`, sin push.
- Output del shot: `validated-baseline/w1-o-fee-inventory-20261031/` → `inventory.json` (sha256 `06da2780…`), `inventory.md`, `run-receipt.json`, `scout-pack.json`, `implementation-ready.json` y el binario `fee-inventory` (sha256 `231eebf8…`).
- Vault: `10-projects/Personal/Polymarket Engine/Research — Target Fee Inventory W1-o 2026-10-31.md` (nuevo), esta nota de sesión, `80-agents/journal/feedback/system-1/2026-10-31-polymarket-w1o-fee-inventory-feedback.md` (nuevo), `80-agents/journal/agent-runs/2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1o-fee-inventory.md` (nuevo), `80-agents/journal/logs/2026-10-31-polymarket-w1o-fee-inventory-entity-updated.md` (nuevo), más el delta acotado en `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` y `Polymarket Engine — MVP.md`.
- Feedback de scout ya materializado (dispatch `w1o-fees`): `80-agents/journal/feedback/system-1/2026-10-31-code-scout-w1o-fees-feedback.md`; no se duplicó.

## Memoria propuesta o creada

- Ninguna nota L0/L1 adicional más allá de este resumen y la nota de research; no se creó memoria interna nueva (no hubo continuidad interna que actualizar más allá del checkpoint del proyecto).

## Decisiones

- La fee declarada (cap 1000 bps, `fees_enabled=true`) y la fee trade-observada (`"0"` en 78/78 trades) se reportan como **identidades distintas**, sin fundirlas ni promediar.
- `POINT` en la identidad trade-informed **no** se lee como fee efectiva ni habilita `REAL_FEE_READY`; la identidad de settlement se declara `NOT_CERTIFIED` (gap U-02).
- El ancla `as_of_kickoff_K` describe lo conocido hasta K; no habilita decisiones anteriores ni aplicación retroactiva de fee.
- Nada se traslada desde W1-e u otros mercados: la evidencia de fee de los otros cuatro mercados no se usa en ninguna dirección.
- El `0` trade-observado se reporta como **observación de esos trades**, no como fee 0 del mercado.
- La decisión de L del Owner sigue pendiente y no bloquea este inventario.

## Pendiente

- Documentar el mapeo U-02 (`base_fee`↔`feeRate`↔settlement) con fuente pública del venue, o autorizar una captura exploratoria de `/fee-rate` por asset y de un `new_market` del target: es lo que permitiría mover `REAL_FEE_READY` (hoy `false`).
- Decidir el alcance del `fee_rate_bps = "0"` observado (comisión aplicada vs valor por defecto del emisor vs convención del venue).
- Cerrar la regla de L con el Owner (incluir o no el frame de señal en `ref`/`L`) en el próximo preregistro; no se cambió código ni parámetros.
