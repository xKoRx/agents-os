---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[A — Runtime CURRENT TARGET]]"
  - "[[F — SQL Migrations Ownership]]"
  - "[[G — Hasura UX Functional Spec]]"
  - "[[J — Shot 2 Implementation Package]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# I — Go API SQL Executable Spec

## Propósito

Mapa canónico ejecutable entre contratos Go, API, SQL, permisos y archivos de implementación para Shot 2. A–G conservan una sola autoridad por hecho; I resuelve sus interfaces sin duplicar sus DTOs, fórmulas o DDL. Todo CURRENT refiere exclusivamente a Echo runtime `feature/ef-runtime-pools@2ee61791deb3139be23e1c9be3708b1d41da8d6b`; Symphony `master@daded14cbe0bc85f6fafda8d079e94036f715b47` sólo aporta productor/ranker. Este documento es diseño y no autodeclara gate GOD, código aplicado ni prueba física.

## Contenido

### 1. Autoridad única y resolución de interfaces

| Frontera | Autoridad contractual | Entrada→salida y writer |
|---|---|---|
| Runtime/Signal/MM/master/journal | [[A — Runtime CURRENT TARGET]] §2–§7 | Owner runtime o writer journal→FactEnvelopeV2/crosswalk/economía fuente; PostgreSQL sólo proyecta. Master ReferenceEvent no se vuelve Signal técnico ni Operation ficticia |
| Universal ingest/Forge/provisión | [[B — Forge Ingestion Readiness]] §3–§10 | DTO SDK V2→receipt inmutable+binding/outbox/ACK/readiness; Echo traduce a sus stores. Forge conoce sólo SDK/API, nunca SQL Echo |
| Historia/economía/selección | [[C — Histories Revisions Economy]] §2–§8 | Snapshot completo→HistoryRevision inmutable+artifact+head CAS; fuentes alternativas se seleccionan explícitamente y no se suman |
| Curvas/métricas/worker | [[D — Curves Metrics Workers]] §2–§6 | Manifest pinneado+spec→bundle cuatro perfiles/metrics/contributions, cola/lease/fence/CAS; precisión fija24 versionada |
| Ranking compartido/cohort | [[E — Rankings Shared Go Parity]] §2–§6 | Métricas selladas→kernel único→snapshot cohorte completo; run/config particulares en membership, no en igualdad global |
| Persistencia/migraciones/DB grants | [[F — SQL Migrations Ownership]] | FKs/PKs scoped, orden067–074, runner checksum real, inventario legacy y views readonly |
| Lectura/auth/UX | [[G — Hasura UX Functional Spec]] | Identidad servidor→bundle de lectura pinneado→Hasura/Go→screener/detalle completo; mutations de negocio Echo |
| Pruebas independientes/gates | [[H — Test Matrix Independent Oracles]] | Oráculos, población/SLO/evidencia y blockers físicos; ningún PASS heredado |

El vocabulario público final conserva `execution_mode=SIMULATED|LIVE`, `run_mode=LIVE|BACKTEST|REPLAY`, `reference_role=REFERENCE|EXECUTION|NATIVE` y `reference_basis=ACTUAL|THEORETICAL|UNKNOWN` como ejes independientes de A. `History.role` usa el mismo rol; source_kind describe productor. `run_ref` de History transporta run_id canónico del runtime cuando existe; no se crea un run diferente por relectura. `config_revision` y digest pinnean binding, no se confunden con versión de feed ni con selection_revision. `runtime_operation_id` puede ser null. Ref execution de A identifica ciclo fuente; C lo conserva como `source_operation_id` y `correlation.source_operation_ref`, y calcula su operation_ref de representación bajo History. Crosswalk explícito SAME_ECONOMIC_FACT permite elegir representación sin duplicar economía. No usar UUID de fila journal, magic, nombre o timestamps como identidad universal.

H/D fijan matemática y evidencia. Fact source numeric(38,18) queda exacta; derivados usan `derived-fixed24-half-even.v1` con límites/cotas/boundary de D, display12 separado. No fracciones compuestas de tamaño ilimitado ni float en economía. Shared kernel de E sí usa binary64 desde calc_HE24 conforme a su frontera numérica sellada. API serializa dinero/cálculo como strings; JS sólo presenta. No introducir distinta precisión en SQL.

### 2. Servicios Go y transacciones

| Servicio/paquete TARGET | Contrato de aplicación | Unidad durable / error |
|---|---|---|
| `sdk/contracts` V2 + `contracts/wire` | Tipos B/C, Validate/Canonicalize/HashTagged actuales extendidos por unions de recetas; encoder compartido producer/server | Rechazar unknown/duplicate/trailing/UTF8 inválido; errors con JSON pointer. `H=wire.HashTagged`, `D=wire.Digest`; no otra codificación |
| `sdk/execution` | Scope/Correlation/FactEnvelopeV2/CycleRiskSeal/EconomicMovement y errores de A | Sin DB/ETCD/engine dentro del contrato. Owners actuales son únicos emisores autorizados |
| `gateway/internal` StrategyIngestionService | Authenticate→validate→artifact write-ahead→registry/history/receipt/dirty+outbox commit→202 | Receipt lookup precede CAS. Fallo previo commit revierte aceptación completa; fallo publicación/readiness posterior se reconcilia independiente |
| `sdk/postgres` RuntimeBindingRepository + gateway reconciler | Desired binding revision→outbox exacto→ACK aplicado→readiness B | No READY desde Kafka ack/cache highwatermark. ACK incarnation/lease/recovery real y gate nuevo OPEN |
| `sdk/execution/correlation` y dueños A | SourceIdentity+binding aplicado→cycle/crosswalk sellado | Mismo source key/payload converge; distinto digest quarantine/conflicto. Sin merge heurístico |
| `futures-projector` + history relay | Fact inbox→projection+history-dirty outbox commit→offset | Watermark/fact ID/digest/effect_index; todos kinds incluyendo DRAIN_REFUTATION y stop_price; fill sin padre queda staged |
| `sdk/postgres` HistoryServiceV2 | Snapshot acumulado completo y CAS→N+1 rows+artifact refs+receipt+dirty | Nunca append a N sellada ni ReplaceHistory V1. Review/corrección por C; SET acumulado no sólo último ciclo |
| `sdk/lab/analyze` | Timeline+CurveFactory+MetricFactory puros de D | Sin red/reloj/config mutable; profile registry encola automáticamente todos los perfiles. Missing evidencia es estado económico, no excepción técnica |
| `sdk/lab/ranking` + `v3/shared-analytics/{ranking,metricinput}` | Adapter valida MetricSet→kernel MinMaxV1→cohort writer | Kernel stdlib-only único; adapter hace fingerprints/wire. Sin clone en Symphony/SQL/front |
| `sdk/postgres` AnalysisRepository + `lab-worker` | Claim lease/fence→freeze manifest→compute fuera locks→validate deps+publish bundle/CAS | Worker vencido no publica; cambios desired no se pierden. Missing económico publica estado terminal; error técnico mantiene anterior |
| `sdk/postgres` ReadBundleRepository + gateway BundleService | RR corto crea read_bundle_rows de generaciones/cohorte publicadas→keyset | Query/sort/owner/namespace pinneados; HMAC Go, ordinal sellado y child reads con generación exacta |
| `sdk/postgres` SelectionService/StaticCompositionService | Comando operador con inputs exactos+CAS→revision/digest+dirty en misma tx | No SQL/Hasura write desde cliente; no live allocation ni I2 |

Todos los writers/publicadores usan el orden determinista de locks de F, receipts/constraints y fences; comprobación de vector y cambio de pointer pertenecen a la MISMA transacción protegida. No SELECT de validación seguido de UPDATE desprotegido. Runtime checkpoint/egress preserva semántica StateFun vigente, no se sustituye por una transacción PostgreSQL. Backpressure/admisión/deadlines de B protegen runtime existente; no workers/bulk ilimitados.

### 3. API V2 canónica

Base `/api/v2`, JSON estricto, Bearer scoped B/G, sin namespace libre. Mutaciones usan `Idempotency-Key` y cuerpo normalizado persistido; error `{code,retryable,field_or_ref,request_id}`. `expected_revision/expected_digest` del body son CAS obligatorio; si falta precondición body devuelve428. `If-Match` es header complementario opcional y, si aparece, porta el digest esperado y debe coincidir con el body; discrepancia400. Replay conocido se resuelve antes de CAS. Aceptación202 confirma commit; no READY implícito. GET ajeno404. Las rutas nuevas son TARGET y no se atribuyen al server.go actual.

| Método/recurso | Request/response de autoridad | Grant / implementación |
|---|---|---|
| POST `strategy-ingestions` | B StrategyIngestionV2→receipt202/200 | `strategy:ingest`; handler V2 y servicio único B/C |
| GET `strategy-ingestions/{receipt_id}`; GET `strategy-ingestions/by-key/{key}` | B receipt scoped con accepted refs inmutables y observed snapshots identificados | Mismo namespace+writer o operador autorizado; no UUID-only lookup |
| PUT `strategy-versions/{version_ref}/histories/{history_id}` | C snapshot completo+CAS→202/200 unchanged/replay | Writer fijado o adapter interno exacto; history ID URL no autoriza writer ajeno |
| GET mismo recurso | C head/coverage/retained revisions; `writer` filtro sólo si principal puede leerlo | Metadata sin adoptar head para datos ya pinneados |
| POST `strategy-versions/{version_ref}/operational-bindings` | B OperationalRequestV2→binding desired/readiness | `operational:provision:<profile_ref>`; no cuentas libres en body |
| GET `operational-bindings/{binding_ref}/readiness` | B desired/applied scope/gates/valid_until | Read grant específico, leases reales |
| PUT `lab/strategy-versions/{version_ref}/selection` | C SelectionRevision con expected revision/digest→receipt+new revision | `lab:selection:write`; Preview validado por el mismo servicio, sin side effects hasta comando |
| POST `lab/static-compositions`; PUT `lab/static-compositions/{ref}` | C StaticComposition+D11; creación expected0, update CAS exacto→receipt/target | `lab:composition:write`; miembros exactos, weights/no double economic fact |
| POST `lab/analysis-targets` | D spec con target_ref/kind/input manifest/profile or registered ranking context y defaults expandidos→target/desired_seq | `lab:analysis:write`; sólo registry IDs/config validada; no arbitrary plugin/code |
| POST `lab/analysis-targets/{ref}/retry` | `{expected_desired_seq,expected_manifest_digest}`→receipt/state | `lab:analysis:retry`; no cambiar spec/revisiones ni desbloquear permiso económico |
| GET `lab/mutation-receipts/by-key/{key}` | Receipt universal de selección/composición/analysis con action/resource/digest/resultado original | Namespace+principal/writer original, mismo scope idempotencia de B; recuperación de outcome incierto |
| GET `lab/profile-catalog`; GET `lab/ranking-contexts` | D/E descriptors/contextos publicados+estado deseado | `lab:read`; no fórmulas en JS |
| POST `lab/read-bundles`; GET `lab/read-bundles/{ref}/page` | G query allowlist→bundle/rows/cursor firmado | `lab:read`; lectura materializada, sin grant write |
| GET `lab/read-bundles/{ref}/strategies/{strategy_ref}` y hijos G | Detail pin+points/operations/daily/distribution/histories/copies, movements por operación | Namespace+bundle owner+referencias de generación; límites G |

`SelectionRevision` y `StaticComposition` usan structs exactos C. Comando V2 adicional de selección contiene `{expected_revision,expected_digest,selection}`; crear selección usa expected0/null y no exige If-Match previo; actualizar exige CAS body; If-Match opcional debe coincidir si se aporta. Scope selection por namespace/version_ref; resolution múltiple entre versiones requiere seleccionar version_ref explícito y queda en read bundle. `AnalysisTargetRequest={target_ref,target_kind,spec,input_manifest,expected_desired_seq,expected_manifest_digest}`; nuevo target expected0/null; actual requiere CAS, no reemplaza current. Respuestas mutables de control siempre incluyen observed_at. Cuerpos de lectura no pueden activar/provisionar nada.

Errores comunes:400 wire/header mismatch/cursor inválido,401 auth,403 grant,404 scoped,409 idempotency/identidad/cursor query conflict,412 precondition stale,428 missing precondition,413 tamaño,415 encoding,422 invalid economics/profile/config/sort incompatible,429 capacidad,503/504 indisponible/deadline. Ausencia Q_i o perfil no comparable válido retorna aceptación+status, no 422 inventado. Después de timeout GET receipt antes de retry mismo key/body; nunca key nueva para esquivar conflicto. Límites/retries exactos B para ingesta/provisión y G para lectura.

### 4. Mapa SQL y permisos

Secuencia adjudicada: `067_lab_v4_migration_foundation`, `068_lab_v4_registry_recipes`, `069_lab_v4_runtime_bindings`, `070_lab_v4_execution_projections`, `071_lab_v4_history_revisions`, `072_lab_v4_analysis_generations`, `073_lab_v4_ranking_cohorts`, `074_lab_v4_read_models`; nombres de archivo definitivos y DDL son los de F. No reutilizar numeración/nombres del freeze antiguo ni editar066 aplicada. F define runner mínimo con bytes/checksum por archivo y transacción DDL+ledger; autoescritura del checksum en migración no cuenta como validación. Sin retiro destructivo en074.

| Familia F | Servicio writer / lectura pública |
|---|---|
| Registry existente extendido/receipts | B application service; no segundo catálogo de estrategias |
| Bindings/config outbox/config ACKs | B reconciler y ACK consumer autenticado; vista readiness no prueba venue |
| execution.* y source correlations | Projector/servicio de correlación A; conservar historial de ciclos/run y scope de fills, sin reemplazar runtime |
| Histories/revisions/operations/movements/change entries/selections/compositions | C application services; retención write-once y head CAS; artifact store append-only |
| analysis_targets/generations/dependencies/attempts + outputs | D worker fenced; perfiles completos mismo bundle |
| ranking headers/membership/extrema/components/entries/pointers | E publisher cohorte; invalidación de toda partición afectada |
| read_bundles/read_bundle_rows + lab.v4_* | G BundleService con snapshot corto; Hasura SELECT-only y filtros server session |

No FK sólo por ID local sin namespace/parent scoped. No cast de timestamp de precisión fuente a microsegundos para calcular digest/orden; conservar canonical timestamp y causal fields C aunque auditoría SQL use timestamptz. Valores exactos fuente38,18, derivados76,24+status/reasons/bounds, display12; redondeo en Go, SQL valida límites sin recalcular economía. Tablas de snapshots no se patch-ean por corrección; punteros/control sí cambian protegidos.

DB roles y GRANT/REVOKE de F se validan con usuarios reales del harness. Rol SQL de projector no ingesta/provisiona; writer history no modifica runtime; worker sólo derivados; Hasura sólo SELECT de views allowlist y sin secretos. Hasura frontend roles V4 lab_readonly/lab_config_operator de G son distintos de DB roles; source echo_lab_v4 usa login SELECT-only V4 sobre misma DB, separado del sourcelegacy. Session owner es owner_principal_ref, page50/max200 y permiso201. Legacy tables/functions/grants/event triggers se inventarían por objeto/consumer antes de cambiar; no supresión masiva ni `{}` persistente en nuevas views. El builder `v3/hasura/scripts/build_lab_v4_metadata.py` recibe export JSON completo+sourcelegacy explícito+fragments V4 y genera candidato preservando objetos no owned; falla si source/login/rol faltan o hay conflicto de nombres. No exporta ni escribe secrets. Los tests comparan objetos legacy antes/después y validan metadata consistency en Hasura propio; apply sólo harness. Aplicar en compartido necesita ownership/ventana independiente.

### 5. Archivos/superficies exactas de Shot 2

Rutas relativas al repo indicado; crear archivos nuevos dentro de estos paquetes sólo para contratos/servicios/tests listados. No autoriza cambiar backtester, campañas, extracción en curso, sync del vault ni runtime desplegado. La lista incluye superficie dependiente mínima, no permiso de refactor general.

| Repo | Archivos existentes a modificar y archivos nuevos permitidos | Propósito |
|---|---|---|
| Echo | `v3/sdk/contracts/{strategy_history.go,strategy_ingestion_v2.go,strategy_history_v2.go,runtime_binding_v1.go}` y tests asociados; `contracts/wire` validadores existentes | B/C DTO/decoder/recipes compartidos, no wire duplicado |
| Echo | `v3/sdk/execution/{contracts,correlation,accounting}` nuevos; `sdk/futures/domain/{signal,fanout,operation}.go`; `sdk/futures/strategy/fanout.go`; `sdk/futures/operation/{engine,engine_inputs,mm,runtime,wire,evidence}.go`; `sdk/futures/accounting/ledger.go`; `sdk/futures/gerardmm`, `sdk/futures/strategies/tgmm` emisores concretos | Sidecar/version/run/QI/economía/facts A, sin nueva evaluación ni motor |
| Echo | `v3/core/internal/functions/{futures_operation,trade_journal,execution_planner,strategy_config}.go`; `core/internal/{futuresruntime,config_cache.go}`; `core/cmd/echo-core/main.go`; `sdk/statefun`; module YAML existente que declare nuevos kinds/config | Integración owner/checkpoint/ACK/gate/recovery; source-only, sin apply compartido |
| Echo | `v3/bridge/internal/pipe_handler.go`; `sdk/domain/{reference_event,trade_close,trade_journal,client_config}.go`; `sdk/postgres/{trade_journal_repository,execution_policies_repository,strategy_identity_repository,strategy_version_repository}.go` | Correlación fuente/moneda/costos/config y persistencia B/A |
| Echo | `v3/futures-projector/core/projector`, `adapters/{pgstore,kafka}`; tests asociados | Inbox/fact v2/replay/conflicto/outbox/offset; no borrar066 |
| Echo | `v3/toolkit/cmd/apply-migration/main.go` y tests del runner; `v3/sdk/postgres/migrations/067*` a `074*` exactos F; nuevos `migration_runner_v4.go`, `strategy_ingestion_v2_service.go`, `strategy_history_v2_service.go`, `runtime_binding_repository.go`, `runtime_ack_repository.go`, `runtime_outbox_repository.go`, `lab_selection_service.go`, `lab_static_composition_service.go`, `lab_analysis_repository.go`, `lab_ranking_repository.go`, `lab_read_bundle_repository.go` y tests asociados | Implementar unidades durables anteriores con adapter pgx existente; F dueño nombres/DDL |
| Echo | `v3/sdk/lab/{analyze,ranking,history}` nuevos paquetes/archivos necesarios y tests; `sdk/analytics/adapter/journal.go` y `lab-worker/internal/repo/trade_journal_lab_repo.go` para corte controlado a V2; `lab-worker/internal/{builders,workers}` y `lab-worker/cmd` loop registrado | C/D/E servicios/reducer/worker; ninguna migración del backtester |
| Echo | `v3/shared-analytics/go.mod`, `ranking`, `metricinput`, `testdata/ranking`; `v3/sdk/{go.mod,go.sum}`; `go.work` sólo incorporación explícita a tests locales cuando no certifique distribución | Módulo puro único, pin prerelease E, sin tocar namespace sdk/analytics existente |
| Echo | `v3/gateway/internal/{server,auth_middleware,hasura_auth_hook}.go`, nuevos `strategy_ingestion_v2_handler.go`, `runtime_binding_handler.go`, `runtime_binding_reconciler.go`, `lab_v4_query_handler.go`, `lab_v4_command_handler.go`, `lab_v4_hasura_action.go`, `lab_v4_cursor.go`, config ETCD vía SDK y wiring `gateway/cmd` | Montaje real de todas las rutas/auth/read bundle/commands; tests a la ruta real, no handler sin montar |
| Echo | `v3/hasura/metadata/tables/lab_v4_runtime.yaml`, `metadata/actions.yaml`, `metadata/actions.graphql`, source V4 `metadata/databases/echo_lab_v4.yaml`, nuevo `scripts/build_lab_v4_metadata.py` y fixture/export sanitizado+tests del candidato | SELECT scoped + query action G; ensamblar metadata completa sin perder consumers existentes |
| Echo | `v3/front/src/views/LabView.vue`, `router/index.js`, `lens/lensRegistry.js`, `services/{config,session_tokens}.js`, `services/graphql/client.js`; nuevos `services/graphql/labV4Runtime.js`, `services/labV4Commands.js`, `composables/useLabV4Bundle.js`, `components/lab/v4/{StrategyLabV4Tab,StrategyScreenerV4Table,StrategyDashboardV4,LabV4HistorySelection,LabV4Operations,LabV4Calendar,LabV4CopyComparison,LabV4StaticComposition}.vue` y tests Vue/servicios | G completo; reutilizar presentadores puros vigentes sin heredar backend V3 ni recalcular economía |
| Symphony | `sqx/adapters/echo-handoff/http_ingress.go` y nuevo `http_ingress_v2.go`; `sqx/core/forge/handoff_producer.go`; `sqx/core/capabilities` DTO port V2; `sqx/adapters/registry-postgres` manifest/delivery V2 y migración siguiente a max vigente; `sqx/core/domain/ranking_snapshot_per_type.go`; `sqx/{go.mod,go.sum}` y tests asociados | Productor SDK Echo, receipt recovery/readiness y wrapper kernel compartido; no SQL Echo ni flota |

Si el archivo vigente organiza wiring en otra unidad del mismo paquete, GLM registra mapeo equivalente antes del cambio; no inventa un API diferente ni abre superficies de campañas/backtester. Cambios a tests existentes siguen PR/test-change rules del repo; agregar regresiones nuevas críticas primero y no borrar asserts para elevar coverage. Dependencia prerelease exacta E: `github.com/xKoRx/echo/v3/shared-analytics v0.0.1-lab-v4-shot2.1`, tag `v3/shared-analytics/v0.0.1-lab-v4-shot2.1`, todavía no publicado en Shot 1. Distribución requiere cold-cache/GOWORK=off sin replace local del módulo; ningún pin SHA futuro inventado.

### 6. Contrato de evidencia y resultado

Shot 2 debe devolver source SHA/delta/manifest por repo, versiones efectivas de módulo, checksum migraciones/metadata, tests críticos y coverage≥95% nuevo, oráculos D/E/H, captura del recorrido G y prueba auténtica aislada Forge→readiness→master→journal→History→curvas→ambos rankings→Hasura→UI. SQL setup de tests es desechable propio; fuente auténtica conserva provenance y scope, jamás fixture presentado como integración real. Artefacto/permiso externo ausente se registra BLOCKED_EXTERNAL con evidencia mínima, no omite implementación funcional. I1 completo incluye selección/copia/D11/screener/detalle; sólo gates físicos requieren acceso externo. Root/GOD emite gate final del paquete, no I.

## Fuentes

- A–H enlazados en §1, únicos owners contractuales.
- [[J — Shot 2 Implementation Package]] para secuencia/owners/aceptación y [[0 — Shot 1 Gate and Baseline]] para adjudicaciones GOD.
- Evidencia de código CURRENT: A[E01–E20], B§1, C§1, D§1, E§1 y G§1, todos SHA-pinned; no se repite aquí la prosa de investigación.
