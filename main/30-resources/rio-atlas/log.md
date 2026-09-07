# RIO Atlas — Bitácora

Append-only, cronológico. Formato: `## [YYYY-MM-DD] <op> | <detalle>` con `<op>` ∈ `ingest | query | lint`.

## [2026-08-10] ingest | Activación de RIO Atlas
- Se activó el dominio con `00-index.md`, mapas de sistema/integración y la herramienta [[rio-inspector]].

## [2026-08-11] ingest | Camino end-to-end de deploy
- Se agregó [[deploy-request-path]] y se corrigió el transporte del trigger: publicación a BigQueue con entrega HTTP push, no HTTP directo.

## [2026-08-11] lint | Auditoría base de AGENTS OS Fase 4
- Cobertura del índice completa; `00-index.md` y `log.md` reconciliados; Graphify reindexado sin contaminación de trash, archive ni JSON.

## [2026-08-12] ingest | Inventario de scopes backend RIO
- Se agregó [[scope-inventory]] desde dos fuentes resolubles: inventario live reconciliado con `fury list-infra` + `fury scopes status -j` y comportamiento scope-aware de los 10 repos backend. Baseline: 87 scopes, 84 activos, 3 inactivos y dos repos sin scopes propios; quedan abiertos tráfico/uso operacional y matriz de compatibilidad.

## [2026-08-12] lint | Validación posterior al inventario de scopes
- Contrato, lint estricto y gate sin findings nuevos; cobertura del índice completa; Graphify reindexado y corpus derivado sin trash, archive ni JSON.

## [2026-08-12] ingest | Inventario 3 parcial: consumidores BigQueue y ownership
- Se amplió [[scope-inventory]] con `fury services bigq consumers list`, `fury apps details` y `fury collab projects`: 21 scopes `used`, 62 `no-evidence`, 1 `retirement-candidate` y 3 `inactive`; los 10 repos pertenecen a `dps-rio` / `cross-dps-rio`. Quedan pendientes tráfico histórico, último mensaje, owner humano y dependencias.

## [2026-08-12] ingest | Inventario 4: matriz de compatibilidad scope-level
- Se agregó [[scope-compatibility-matrix]] cerrando el eslabón canal↔scope con `fury services bigq consumers list` por repo (39 consumidores; 38 running, 1 paused) y verificando bindings topic↔scope y rol producer/consumer en `application*.yml`. Hallazgo central: la compatibilidad se determina por `(canal, segmento Fury)`, no por el nombre del scope. Nuevos: clickhouse consume ambos triggers (cierra gap de integration-map), observability consume deployment-trigger, `consumer-prod` (flink) reforzado como retirement-candidate por ruta pausada redundante, y canal sin mapear `component-registry`.

## [2026-08-12] ingest | Segmentación Fury, estándar de naming y grid de scopes
- Se investigó la capability de segmentación de Fury con la CLI autenticada (`fury list-segments`: business segment `meli`, infra-segments `nonprod/nonsite/legacy/arg/bra/col/mex/rla/platform`) y las declaraciones `segment-id` en código. Nuevas notas canónicas: [[fury-segmentation-model]] (modelo + deuda legacy: 14 scopes tocan legacy) y [[scope-naming-standard]] (propuesta de gramática `lane[-role]`, grupos aislados alpha/beta/gamma/stage, segmento resuelto por perfil, mapa de migración). Entregable visual: `30-resources/grids/rio-scope-inventory.html` (top de apps por warnings, split prod/test, 87 scopes, tooltips). Nota: el MCP de Fury no quedó conectado en la sesión; se usó la CLI.

## [2026-08-12] lint | Auditoría de evaluación y propuesta de scopes
- Se revalidó `fury list-segments` y se corrigieron sobreafirmaciones: consumer `running` no prueba tráfico/uso; `(canal, segmento)` prueba routing pero no compatibilidad semántica; Fury no demuestra subsegmentos `nonprod-<lane>`; y las 14 marcas legacy son exposiciones potenciales por fila de scope, no recursos live contados. [[scope-naming-standard]] pasó a iteración 2 con gramática `lane[-role[-workload]]`, ejemplos no definitivos y manifiesto de bindings obligatorio; el grid quedó rotulado como snapshot no reproducible ni score de riesgo.

## [2026-08-12] ingest | Fuente de verdad Fury y reporte de scopes iteración 2
- Se reemplazó el baseline parcial por el service graph read-only completo: 88 runtimes, 85 activos, 50 legacy/26 nonprod/12 nonsite, 40 consumers BigQueue, 12 sinks HTTP pausados y 3 worker groups activos. `rio-controlplane-signals/bq-consumer-nonprod` explica el cambio 87→88 y `consumer-prod-nonsite` queda confirmado `nonsite` de punta a punta. `~/fuentes/rio-inspector/rio-scopes.json` genera [[scope-inventory]] y el HTML; se eliminó la clasificación genérica de uso y el score.

## [2026-08-12] lint | Spec funcional, QA visual y reindex
- [[scope-naming-standard]] quedó reestructurada como Functional Specification con contrato, user stories, acceptance criteria, E2E, riesgos y rollout. El grid pasó QA en navegador (88 cards, filtros, Web sin binding artificial, leyenda accesible y caso nonsite correcto); lint strict y Graphify update terminaron sin deuda nueva.

## [2026-08-12] ingest | Reporte por aplicación, Fury routes y configuración por scope
- `rio-scopes.json` subió a schema v2 y separa hechos (`fury`, `runtime_segment`, `bindings`, `route`, resolución de config) de datos procesados (`operational`, estados de config, flags/track de naming y resúmenes por app). El corte mantiene 88 scopes: 22/23 BQ con consumer activo, 0/15 Streams con sink activo, 3/3 WQ con worker group y 42/42 Web con Fury route. Config: 30 bundled + artifact, 41 bundled, 11 Fury-only y 6 base-only. El grid ahora enumera scopes concretos que requieren decisión y conecta el baseline con el objetivo de nomenclatura.

## [2026-08-12] ingest | Config Orchestrator y target state segmentado
- Se corrigió la mezcla entre archivos del repo y Fury Config: schema v3 compara `application_config_version` desplegada con latest `APPROVED` de Config Orchestrator (42/88 con release; 39 current, 2 diferentes, 1 deployed no expuesta) y guarda `code_config` aparte. `rio-scope-policy.json` propone 68 scopes base + 6 condicionales: prod→nonsite y alpha/beta/gamma/stage→nonprod, sin segmentos en el nombre. Los 15 Streams sin sink activo quedan marcados `*`; Secrets/KVS se reservan como `not_collected`.

## [2026-08-19] ingest | Propuesta completa y piloto KMS de segmentación
- Se aclaró la autoridad del naming: RIO define `<environment>-<role>[-<qualifier>]` y Fury agrega siempre `-<segment>` al nombre materializado. La propuesta del grid se alineó con selección independiente `frontend/backend`, header de scope hacia Fury routes y topic compartido con tag `scope:<x>`; se eliminó la afirmación obsoleta de que BigQueue no filtra por valor. `rio-controlplane-kms/test` queda como piloto por la obligación del 2026-09-09, con target `alpha-api-nonprod`, bridge `test-nonprod` sólo si Fury lo exige y un blocker de código: desacoplar Spring profile del último token `nonprod/nonsite`.

## [2026-08-25] ingest | Idempotencia de deployments y KVS en los CPs
- Se agregó [[playmaker-deployment-idempotency-and-cp-kvs]] con comparación de Kafka, Flink, ClickHouse y Fury. Decisión: el KVS de los CPs deduplica el mismo `deployment_id`, pero no reemplaza el claim del avance de batch ni el invariante global de un deployment activo por service en Playmaker; ClickHouse conserva un gap de claim distribuido y Fury usa natural key + `specHash` en su dominio.

## [2026-08-25] lint | Ingesta CP/KVS con reindex degradado
- La cobertura dirigida confirmó que la página nueva está en el catálogo; seis páginas antiguas del Atlas permanecen sin fila y se conservaron como deuda preexistente. `graphify-obsidian update` quedó bloqueado por 11 errors y 6 warnings de frontmatter en skills/memorias no relacionadas con este cambio.

## [2026-08-25] ingest | Hotfix del listener y refactor durable de avance de batches
- Se actualizó [[playmaker-deployment-idempotency-and-cp-kvs]] con la decisión en dos tracks: hotfix sin schema/estados/CPs mediante mutex KVS en `BatchCompletedEventListener`, espera con backoff y detección `already_materialized` por deployments del group; luego refactor durable con tópico externo, publicación recuperable y lógica atómica/consistente. `ComponentRun.DISPATCHING` quedó deprecated/superseded.
