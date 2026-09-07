---
type: known_error
scope: application
created: "2026-07-28"
updated: "2026-07-28"
area: "[[Echo]]"
project: "[[Echo Forge]]"
project_sub: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[echo-forge]]"
entities:
  - "[[forge.wfm_runs]]"
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[Echo Forge - Cierre de Etapa 4]]"
  - "[[trade-list-exporter-minio-prefix-mismatch-robust-sqx]]"
aliases:
  - E11000 duplicate key wfm_runs
  - wfm_runs dup key wave_key strategy_id
  - import_metadata duplicate strategy
confidence: verified
source_session: 2026-07-28-echo-forge-flow41-relaunch-wfm-mongo-dup
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/echo-forge
  - app/echoforge
  - area/echo
  - kind/known-error
  - project/echo-forge
  - project/echoforge
  - scope/application
  - tool/strategyquant
  - store/mongodb
---

# `forge.wfm_runs` colisiona por `(wave_key, strategy_id)` en re-run del flow 41

> La causa **no** es `_SUCCESS` faltante ni `IndexOutOfBoundsException` del
> exporter Java: es una colisión de índice único en Mongo al consolidar
> `wfm_runs` dentro del paso `import_metadata` del sub-flow `project`.

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- En el log del worker (Zeus, `symphony-worker.service`):
  ```
  ERROR Activity error ... ActivityType project Attempt 1
  Error error en paso import_metadata: error al guardar corridas WFM
  para estrategia NDX_L_H1_example_flow_41_v1_Strategy_4.1.22.k0:
  error al guardar wfm_runs para key
  test_ATR,RANGE,TRUERANGE_CLOSE,HIGH,LOW,OPEN_ATR,RANGE,TRUERANGE_NDX_L_H1_example_flow_41_v1_Strategy_4.1.22.k0:
  write exception: write errors: [E11000 duplicate key error collection:
  forge.wfm_runs index: wave_key_1_strategy_id_1
  dup key: { wave_key: "test",
              strategy_id: "NDX_L_H1_example_flow_41_v1_Strategy_4.1.22.k0" }]
  ```
- La actividad `project` queda en retry (`Attempt 2`); el flujo principal
  sigue `Running` pero no avanza hasta que Mongo acepte el `InsertOne`.
- Aparece sólo cuando se **re-ejecuta** el mismo `(strategy, wave)` después
  de una corrida previa que dejó el documento en `forge.wfm_runs`.
- **No** se observan trazas de `IndexOutOfBoundsException`, ni de
  `TradeExtractionException(CONTRACT, ...)` ni de ausencia de `_SUCCESS`.

## Causa raíz

El paso `import_metadata` del sub-flow `project` llama a una consolidación
que hace `InsertOne` sobre `forge.wfm_runs` con clave única
`(wave_key, strategy_id)`. La lógica asume que la corrida previa limpió
su documento; en `wave=test` (la usada por los flows de smoke) no hay
limpieza, así que la primera escritura del re-run choca con el documento
heredado y Mongo devuelve `E11000`.

Sub-flujo afectado en este incidente:
`ATR,RANGE,TRUERANGE_CLOSE,HIGH,LOW,OPEN_ATR,RANGE,TRUERANGE-chunk-0`,
WID `sqx-main-00_configs-v1-NDX-H1-L-1785294794`, RunID
`019fabdc-af83-779d-b274-f17e49db294c`, ActivityID `149`.

## Por qué parecía un bug del exporter Java

Las dos corridas anteriores del mismo flow fallaron con `_SUCCESS` ausente
en `/home/kor/sqx/user/projects/EchoForgeTradeListExporter/tradelist` y
con `IndexOutOfBoundsException` en `TradeExtractionService.java:181`. Esos
fallos **se resolvieron** sincronizando `~/sqx/user/extend/Snippets/SQ/CustomAnalysis/`
y reconstruyendo `~/sqx/user/libs/EchoForgeAutomator.jar`. En el re-run
del 2026-07-28 23:13Z el exporter ya no rompe: la cadena SQX corre entera
(Builder → Overview → Classify/Rank → Retester), el exporter escribe
`export_run.json` y los logs `trade_list_*.log`, y sólo se cae al cierre,
en la consolidación Mongo.

Conclusión: el síntoma cambió pero la causa raíz nunca fue `_SUCCESS`.
Mantenerse alerta: si un fallo del exporter reaparece, validar primero
Snippets+libs antes de asumir idempotencia Mongo.

## Mitigación (recomendada)

Tres caminos, de menos a más invasivo:

1. **Limpieza quirúrgica Mongo** (operativa, no de código):
   ```js
   db.wfm_runs.deleteOne({
     wave_key: "test",
     strategy_id: "NDX_L_H1_example_flow_41_v1_Strategy_4.1.22.k0"
   })
   ```
   Luego cancelar el workflow en Temporal o esperar a que el `Attempt 2`
   pegue con el documento ya borrado.

2. **Upsert en lugar de Insert** en la consolidación `wfm_runs`:
   - Cambiar la llamada a `UpdateOne(..., upsert=true)` con filtro
     `(wave_key, strategy_id)`.
   - Idempotencia natural: re-runs sobrescriben sin `E11000`.
   - Requiere SDD previo en `sqx/core/.../import_metadata` y bump de
     versión del worker.

3. **Versionar `strategy_id`** incluyendo timestamp o `run_id` del wf
   principal para que cada corrida tenga clave única. Cambio de contrato;
   afecta también a los consumidores que lean `wfm_runs` por id estable.

Recomendación operativa para Etapa 4: aplicar (1) para destrabar el
re-run actual, y abrir SDD para (2) antes de declarar cierre.

## Detección

- En `journalctl -u symphony-worker.service`, buscar:
  `E11000 duplicate key error collection: forge.wfm_runs`.
- En Temporal: `ActivityType project` con `LastFailure.Message`
  conteniendo `forge.wfm_runs` y `wave_key_1_strategy_id_1`.
- En Mongo: `db.wfm_runs.getIndexes()` debe mostrar el índice
  `wave_key_1_strategy_id_1` único.

## Solución estructural pendiente

- **SDD sobre idempotencia en `import_metadata`**: owner pendiente.
  Alcance: pasar de `InsertOne` a `UpdateOne(..., upsert=true)` para
  `forge.wfm_runs` (y revisar colecciones hermanas: `forge.export_runs`,
  `forge.workflow_metadata`).
- **Política de limpieza de `wave=test`**: si se mantiene el modo smoke,
  definir un TTL o job de purge para documentos `wfm_runs` con
  `wave_key="test"` y `created_at` > 7 días.

## Evidencia

- Sesión: `2026-07-28-echo-forge-flow41-relaunch-wfm-mongo-dup`
  (transcript en agent-transcripts).
- WID afectado:
  `sqx-main-00_configs-v1-NDX-H1-L-1785294794`,
  RunID `019fabdc-af83-779d-b274-f17e49db294c`,
  ActivityID `149`.
- Snapshot Temporal: `ActivityType project, Attempt 2, LastFailure =
  E11000 ... wave_key_1_strategy_id_1`.
- Log de Zeus (`journalctl -u symphony-worker.service --since
  "2026-07-28 23:15:00"`): contiene el `activity.error` exacto arriba.
- Antecedente (mismo síntoma en la superficie, distinta causa):
  `trade-list-exporter-minio-prefix-mismatch-robust-sqx`.