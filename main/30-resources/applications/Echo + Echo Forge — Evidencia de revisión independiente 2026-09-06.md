---
type: source
schema_version: 1
status: active
area: "[[Echo]]"
source_url: "https://github.com/xKoRx/echo/tree/e25165ba2e57a86b7cdcbd78d44406f66fc9ba23/v3"
repo: "xKoRx/echo; xKoRx/symphony"
path: "v3/; sqx/"
author: "Revisión independiente"
captured: "2026-09-06"
aliases: []
tags:
  - kind/source
  - area/echo
created: "2026-09-06"
updated: "2026-09-06"
---

# Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06

## Referencia

- **Origen:** source local y heads remotos de `xKoRx/echo` y `xKoRx/symphony`; Echo productivo por SSH de lectura al host `192.168.31.71` y consultas Hasura `echo_prod` sobre PostgreSQL `echo` en `192.168.31.220`. Captura 2026-09-06, aproximadamente 19:25–19:34 UTC. Son observaciones de corte, no un monitor.
- **Consumidor:** [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]], complemento de [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]].
- **Seguridad de consulta:** `/v2/query`, operación `run_sql`, `source=echo_prod`, `read_only=true`; consulta `current_setting('transaction_read_only')` devolvió `on`, `current_database()` devolvió `echo`. Sólo SELECT y lectura de metadata. No se ejecutaron funciones de negocio, migraciones, comandos de trading, DDL/DML ni cambios de servicios. Credenciales leídas en memoria desde configuración existente; no se conservan valores ni dumps.

## Alcance

### R01 — Baseline independiente

Echo checkout limpio `e25165ba2e57a86b7cdcbd78d44406f66fc9ba23`; master remoto `04c16bd2bd7b69725560873950a5d6b067fd3a4f` por `git ls-remote`. El delta remoto documentado es tooling de readiness, no se hizo checkout/fetch. Symphony HEAD y master remoto `a10c26c887e4d203b403d2557e292ed773830b0e`; dirty previo preservado. No source edits, builds, tests que escriban caches, commits ni clones nuevos.

### R02 — Binarios y topología Echo, P actual

| Unidad | Evidencia | Límite |
|---|---|---|
| Core | systemd active; PID 110701; `/proc/110701/exe` SHA256 `447ac7c2e275ca1233043269919418fd4e150e01f2218c28c4e4baccc0fd806d`; coincide con archivo; buildinfo `e25165ba2e57a86b7cdcbd78d44406f66fc9ba23`, modified=false | Source del journal corresponde al proceso activo |
| Gateway | systemd active; PID 713; imagen activa SHA256 `4a25d7c708388475f7a2b4b2cb7ab99eaec4542f7a4c3b3e5215c0f39967a924`; buildinfo `0abdf7207f36b456a8b4e6c2ec3c3c0041e029df`, modified=false | `server.go` sin delta entre ese commit y checkout auditado |
| Lab worker | Binario SHA256 `2e168835d982c546d1b0a81afddaf40cc68f893d2a8ee52a309c5c71ca5a83fd`; buildinfo `c86c18dc847f1c3486ef640aaa0bc1fc23571677`, modified=true | No asignable a commit limpio exacto; source actual no prueba igualdad del binario |
| Lab timer | active; última ejecución observada 19:25:50 UTC; jobs terminaron 19:27:02; nuevas ejecuciones observadas después | Servicio batch inactive/dead entre runs es normal |
| Otras unidades | echo-functions y nginx active; nginx escucha puerto 80; no directiva auth_basic/allow/deny en site leído | No se auditó toda ACL de red ni todos los includes |
| Infra externa | Hasura `.48:8080`, fuentes `echo_prod` (77 tablas tracked) y `echo_test` (0); PostgreSQL `.220:5432` accesible | Kafka/StateFun/ETCD no recibieron queries en esta revisión; restore/runtime de esos subsistemas U |

Lectura posterior de Kronos Windows `.128`: un `sqx-mt5-worker.exe`, PID 42572, path de release `0.2.96`; ningún terminal64/metatester64/echo-bridge en la selección de procesos. Source de esa release limita MaxConcurrentActivityExecutionSize=1. Esto acota la afirmación de duplicación: hay gap de ownership en source y futura expansión, pero no se observó flota MT5 multi-host ni ejecución duplicada. El path no sustituye digest de imagen: no hubo recertificación de release. Primer intento PowerShell tuvo error de quoting; segundo, mediante EncodedCommand read-only, produjo este inventario.

### R03 — Exposición de control, P actual

GET sin autenticación del front `.71` entrega `/assets/index-DFXoR0hQ.js`, SHA256 `03d8d42da578e630c5a49b7e843dfd93e8724a6aa49671461145041838ec7250`. Contiene el literal de header admin y el mismo secret que fue aceptado por Hasura para lectura de metadata y SQL. Resultado booleano verificado, secreto no reproducido. Prueba exposición y vigencia dentro de la red alcanzable; no prueba exposición pública a Internet ni explotación. No se enviaron POST a close/republish ni otras mutaciones para demostrar impacto. Source del Gateway activo conecta esos handlers sin middleware de auth propio.

### R04 — Journal y catálogo, P actual

| Scope | Filas | Estrategias | Inicio recorded mínimo | Último hecho recorded | Otros |
|---|---:|---:|---|---|---|
| REFERENCE / ECHO | 2647 | 136 | 2026-06-02 01:54:09 UTC | 2026-09-04 17:30:01 UTC | 2592 con R, 55 sin risk_pips; 2647 con profit_net y costes no-NULL; 0 OPEN |
| EXECUTION / ECHO | 426 | 10 | 2026-06-02 05:10:33 UTC | 2026-09-03 13:08:00 UTC | 2 OPEN desde 2026-06-04; 52 sin risk_pips |
| EXECUTION / NATIVE | 104 | 12 | 2026-08-21 06:00:21 UTC | 2026-09-03 13:00:03 UTC | Todos sin risk_pips; no calidad R canónica |

152 strategy_definitions; 150 con nombre, 140 con wave no vacío, 136 con config no vacío. `config` es un identificador corto en las filas observadas, no evidencia de parámetros/binario histórico. 48 cuentas: 17 ACTIVE, 20 ARCHIVED, 11 INACTIVE. Las 17 ACTIVE son PROP en metadata (10 MT4, 7 MT5); PROP no prueba dinero real. Las 2647 Reference unen a siete cuentas DEMO MT4, INACTIVE y client_account_role NULL. Ninguna cuenta tiene client_reference_strategy_id. No convertir estado administrativo INACTIVE en ausencia de captura ni tipo MT4 de catálogo en certificación de EA histórico.

351 policies, todas sin expiry vencida al corte; cobertura por `(reference account,strategy)` de esas policies = 0/2647. No implica que falte policy de ejecución ni invalida automáticamente profit_pips/risk_pips del journal. Magics del journal entre 132906134 y 260104012, ninguno fuera de int32. Un magic 132906134 corresponde a tres strategy_id en EXECUTION, 88 filas: mapping sólo por magic global es ambiguo en ese scope; las References observadas tienen un magic y una cuenta por estrategia. `magic_number_override` PG sigue integer.

2505 Reference no tienen ninguna fila Execution emparejada; esto NO significa 2505 órdenes perdidas: falta el conjunto de destinatarios esperados histórico. Ninguna Execution/ECHO carece de Reference por trade_id en esta consulta. Las dos filas OPEN viejas son discrepancias a reconciliar; no se consultó el broker, por tanto no se afirma posición física abierta.

### R05 — Schema y Lab, P actual

Journal tiene `origin`; strategy_id varchar(64), trade_id varchar(60), account_id varchar(32); UNIQUE trade/account; roles/sources/side y lot positivo validados. `profit_net` y `r_multiple` son GENERATED; R usa profit_pips/risk_pips. No existe tabla identificable como migration/schema_version en information_schema: no se certifica una secuencia exacta de migraciones aplicadas por inferirla de columnas. Contratos de 043/045 y FAILED son visibles; `origin` conserva drift.

3123 canonical trades; 2647 outcomes en lecturas de generación completa, todos Reference por join. En otra lectura durante actividad del timer, GROUP BY outcomes totalizó 2620 (2565 WARN + 55 DEGRADED), y volvió a 2647 sin cambiar el total Reference: evidencia de variación visible durante recompute, coherente con delete/repopulate source; no prueba pérdida permanente. 10696 snapshots, cero strategy_version_id no-NULL. 0 segmentos; 0 strategy_portfolios/versiones; 3 portfolios de cuentas; 0 live_health_snapshots; 0 account_equity_snapshots; 0 raw_trade_events. 8437 raw_trade_imports sí existen (R07).

2592 outcomes tienen flags MISSING_SEGMENT_RANGE y MISSING_RISK_POLICY_ROW; 55 añaden MISSING_RISK_PIPS. Jobs recompute/curves/snapshots: 26161 SUCCEEDED por tipo en la primera lectura, error_count=0; cuatro recomputes RUNNING históricos hasta 2026-08-12, además de ejecución corriente. code_version reporta 0.0.1, no commit. `strategy_reference_outcomes` y `lab_out_strategy_metric_snapshots` no existen. `cron.job` no existe en esta DB: el estado de pg_cron descrito en agosto no quedó confirmado para septiembre.

### R06 — Logs actuales, P acotada

`journalctl -u echo-core --since 2026-09-01` legible: 1654 líneas al corte. Conteos por mensaje JSON: reference open conflict 169; reference close conflict 173; execution open conflict 43; execution close conflict 46; execution account validation failed/skipping 218; MM calculation failed 22; instrument snapshot nil 20; position delete failed 22; position upsert failed 7; account bulk update failed 7. Son mensajes, no incidentes ni trades únicos. Conflictos pueden ser rechazos correctos; causalidad requiere inputs/existing facts. No hubo inyección de outage ni se cuantificó pérdida de journal.

### R07 — Archivo anterior recuperable, P preservada

`echo.raw_trade_imports`: batch único, source_type ECHO_TRADE_JOURNAL_BACKFILL, PROCESSED, importado 2026-05-04 19:21:37 UTC; todos tienen payload_hash y source_trade_key. Payload usa vocabulario legacy account_type=REFERENCE/EXECUTION y origin; nunca equipararlo automáticamente al schema actual.

| Grupo payload | Filas / estrategias | Fechas de evento declaradas | Created_at preservado |
|---|---|---|---|
| ECHO / REFERENCE | 4388 / 130 | 2025-12-02 → 2026-05-04 | Desde 2025-12-04 01:24:41 UTC |
| ECHO / EXECUTION | 2650 / 125 | 2025-12-03 → 2026-05-04 | Desde 2025-12-04 |
| NATIVE / EXECUTION | 1399 / 36 | 2025-12-18 → 2026-05-04 | Desde 2025-12-23 |

125 strategy_id del archivo Reference reaparecen en Reference actual (4027 filas históricas); 4388 hashes y source_trade_keys Reference distintos. Igualdad del ID no demuestra igualdad del binario/config entre períodos. Falta prueba de continuidad mayo→junio, initial risk y selección anterior a observación. El timestamp created_at está preservado dentro de payload, no certificado como inmutable desde diciembre. Fecha de evidencia de preservación independiente segura: import del 4 de mayo. Fecha candidata de observación legacy: desde 4 de diciembre, condicionada a certificar origen del timestamp; fecha de evento del 2 de diciembre sola no basta.

### R08 — Cohortes por fecha mínima actual

Definición reproducible: agrupar las estrategias Reference por `min(opened_at_recorded)::date`. Cada fila incluye todas las estrategias con esa fecha mínima; no se infiere familia económica desde el magic.

| Primera observación recorded | Estrategias | Trades actuales | Sin R |
|---|---:|---:|---:|
| 2026-06-02 | 36 | 978 | 32 |
| 2026-06-03 | 2 | 47 | 0 |
| 2026-06-04 | 7 | 165 | 15 |
| 2026-06-05 | 2 | 72 | 7 |
| 2026-06-09 | 4 | 70 | 0 |
| 2026-06-10 | 1 | 16 | 0 |
| 2026-06-11 | 13 | 151 | 0 |
| 2026-06-12 | 2 | 40 | 0 |
| 2026-06-14 | 7 | 113 | 0 |
| 2026-06-15 | 19 | 360 | 1 |
| 2026-06-17 | 27 | 418 | 0 |
| 2026-07-01 | 1 | 18 | 0 |
| 2026-07-03 | 3 | 36 | 0 |
| 2026-07-05 | 3 | 40 | 0 |
| 2026-07-06 | 3 | 42 | 0 |
| 2026-07-22 | 4 | 69 | 0 |
| 2026-08-05 | 1 | 6 | 0 |
| 2026-08-07 | 1 | 6 | 0 |

Conteos por estrategia: mínimo 6, mediana 18, máximo 56; 119/136 tienen menos de 30 trades. Esto es descripción, no threshold de elegibilidad. Primera fecha de evento actual 2026-06-01; una fila tiene discrepancia event/recorded mayor que un día. No adelantar automáticamente el inicio a esa fecha.

Archivo Reference agrupado por primera fecha `payload.created_at`: 2025-12-04: 1 estrategia/340 trades; 12-08: 1/13; 12-09: 4/144; 12-10: 35/1388; 12-11: 50/1542; 12-12: 20/437; 12-15: 2/67; 12-16: 1/71; 12-17: 1/42; 12-18: 10/308; 12-19: 1/4; 12-27: 1/1; 2026-01-02: 1/3; 01-12: 1/19; 04-06: 1/9. Son cohortes de recuperación, no fecha forward aprobada.

### R09 — Source revalidado

| Repo/path relativo | Hallazgo comprobado |
|---|---|
| Echo `v3/core/internal/functions/trade_journal.go:100,176` | Invoke retorna nil; handlers absorben fallos de persistencia. Hay error retornado en wrapper repo, no llega al ack boundary |
| Echo `v3/sdk/postgres/trade_journal_open.go`, `trade_journal_close.go` | Unique/conflict/merge de hechos existen; no llamar pérdida a todo conflicto |
| Echo `v3/clients/mt5/reference_v3.mq5:133,619`; `EchoPersistence.mqh:17,47,711` | magic_*; cast int; binario sin envelope versionado; WriteAll y CleanupOld por edad sin comprobar posición viva |
| Echo `v3/clients/mt5/execution_agent_v3.mq5:1739–1863,2202` | Guards estado/whitelist y dedupe por command_id sí existen; broker Buy/Sell precede g_Journal.Add; ventana de crash no resuelta por dedupe posterior |
| Echo `v3/sdk/mm/fixed_risk.go`; `core/internal/functions/mm_engine.go` | Validación de snapshots/SL/specs y cálculo por trade; no reserva agregada probada en este path |
| Echo `v3/sdk/lab/ids/ids.go` | safeSegment no inyectiva en strings arbitrarios; cero colisiones en tuplas actuales consultadas; no P0 productivo demostrado |
| Echo `v3/lab-worker/internal/builders/recompute.go:160–214` | DeleteOutcomes, DeleteCanonical y UpsertBatch separados; no transacción común. SnapshotsRepo sí tiene transacción individual |
| Echo `v3/gateway/internal/server.go`; front graphql client; metadata portfolio | Sin auth de dominio en Gateway; admin browser; mutabilidad de allocations. Portfolio de estrategias productivo vacío |
| Symphony `sqx/adapters/mt5/slot_allocator.go:109`; `artifact_runner.go:140`; `workflows/mt5_artifact_workflow.go:72–95` | Local lease sin CAS global; timeout mata proceso; opciones Temporal finitas vigentes; B1/B2 no implementados en HEAD |
| Symphony `sqx/activities/worker/rank_snapshot_activity.go:298–371`; `core/forge/result.go` | Promotion V1 depende TopProjection; V2 sigue diseño |

Los locators E01–E19/F01–F10 del master completan la navegación. Esta revisión priorizó call paths con impacto material; no recertifica todo el monorepo ni los tests del autor anterior.

## Notas de provenance

- **R10, D:** [[2026-09-06-echo-forge-mt5-global-physical-ownership-v2]] y checkpoint exacto del proyecto declaran TOP PASS/CLOSED; [[2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3]] lo supersede en takeover/cancelación y fija B1/B2 pendientes. ETCD non-TTL+CAS, lease local y singleton permanecen; token no es fence físico. No takeover cross-host dentro de Symphony, ni manual/admin.
- **R11, P reportada:** [[2026-09-04-release-0-2-92-physical-c3-closure]] prueba una finalista C3; [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] contiene cierre 0.2.96 y Campaign `0ac51a05-7bd8-49a8-a130-4c4e205d7084` con cero finalistas y replenishment/replay. No concluir «nunca existieron finalistas» desde esa última Campaign. Los FULL posteriores fallaron seis backtests por 45m; no se lanzó otro.
- **R12, D:** [[Echo - Auditoria POC e Identidad Forge-Echo 2026-08-23]], alineamiento owner 24-08: canonical único, magic estable asignado Forge, MT5 sin techo int32, versiones, Reference/mirrors permanentes; históricos magic_* por alias, no reescritura masiva.
- **R13, metodología externa:** [NIST, intervalos para proporciones pequeñas](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm) y [Bailey et al., Probability of Backtest Overfitting](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf). Apoyan incertidumbre explícita y control de selección; no fijan políticas de trading para este owner.

## Lifecycle

Fuente fechada de observaciones sanitizadas; no nuevo contrato frozen. No suplanta las fuentes anteriores ni convierte absence de versión en prueba de inutilidad económica. Estado broker, EA compilado/config exactos de siete References, semántica broker MT4→MT5, historial de selección y continuidad mayo→junio siguen U. Esas limitaciones se convierten en gates concretos del companion, no en nuevas certificaciones inventadas.
