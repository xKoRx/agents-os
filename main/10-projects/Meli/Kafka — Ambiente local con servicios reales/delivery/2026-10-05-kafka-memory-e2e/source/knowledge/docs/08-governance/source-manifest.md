---
title: Manifiesto de fuentes
layer: L4
audience: [maintainers, engineering, agents]
last_verified: 2026-10-05
confidence: high
sensitivity: internal
---

# Manifiesto de fuentes

## Último corte integral integrado: 1 de octubre de 2026

Se consultaron los 25 `refs/heads/master` en `github.com` con `gh api graphql` el 01/10: 21 sin avance y cuatro deltas semánticos integrados — Playmaker, Frontend, ClickHouse CP y SDK Java. Copilot ya estaba al día por la actualización parcial del 29/09. Los anchors del corte integral de los cuatro repos apuntan al SHA de ese snapshot. La tabla registra el último corte integrado, no todos los heads GitHub observados después. El catálogo pasa de 673 a **689 IDs únicos**. [Detalle del refresh](refresh-2026-10-01.md).

## Auditoría focal Kafka del 1 de octubre

La primera consulta focal Kafka confirmó sin avance CP `f74e856ef3de881e2d504c6cb1ced573681c1058`, Playmaker `3cd0daf6e17841ab79381f1eb5e2bd014ad68bd1` y SDK Events `ad2c98b806cffb88b23513f87785932aa1707ea4`; es un snapshot histórico dentro del mismo día. Se corrigen enforcement, naming/params por provider, peek GCP, marcador KVS y alcance de tests/perfiles del mismo código; no se agregan IDs. El build Kafka depende de SDK Events 1.3.1, mientras el SDK master documentado es 1.5.0: no se declara compatibilidad, release ni E2E por ese único schema version. Implementaciones develop/work branch permanecen pendientes y no reemplazan esta tabla. [Evidencia y límites](kafka-canonical-audit-2026-10-01.md). El mismo SDK master descarta segment/buffering explícitos al reconstruir el ProducerBuilder; [fuentes del hallazgo](../03-services/rio-controlplane-kafka.md). La corrección en rama SDK no modifica estos SHAs canónicos ni acredita delivery BigQueue.

### Revalidación focal posterior: Playmaker Kafka

El master GitHub de Playmaker avanzó a [0c83575c54cb198d238be7d83f3b4d8de27abbc8](https://github.com/melisource/fury_rio-playmaker/commit/0c83575c54cb198d238be7d83f3b4d8de27abbc8). Se revalidaron únicamente transporte local de deployments, entities de Kafka, contexto/DTO, resultados, Service PEEK y la diferencia de autorización frente a develop. `local-integration` de deployments ya está en ese master; acciones Kafka locales, KVS dedicado y selección real de Service PEEK siguen preparados sólo en el checkpoint `1b4b8e1554c37357e4b39e1860be6ad43f9aa640`. El [registro focal](kafka-canonical-audit-2026-10-01.md#revalidación-focal-del-nuevo-master-playmaker) fija paths, líneas y Git blob IDs. Las fuentes `3cd0daf6` reutilizadas para esa frontera tienen blob idéntico verificado; las demás conservan alcance histórico del corte integral. La tabla no se repinea porque esta revisión no auditó el resto de Playmaker. El delta añade sólo pm.kafka.entity-inheritance y pm.local-integration.kafka-deployments: catálogo Playmaker 131/corpus 691. El corte integral histórico conserva 689; no convierte preparación en ejecución y el negocio completo permanece NOT_EXECUTED.

## Corte anterior: actualización parcial del 29 de septiembre de 2026

Se reconsultaron las 25 fuentes en `github.com` el 29/09: 22 sin avance y tres deltas nuevos respecto del corte del 28/09. Este cambio integra **sólo Copilot**, con sus dos archivos modificados de deployment. Playmaker (`2e5f0b22c7f5afeb09402d43514159a686cee672`) y Frontend (`791f79dd8050e1432bdc5c936539b22dbaa4e35d`) permanecen **pendientes de integrar**: sus filas conservan el último SHA documentado, no el head nuevo. No interpretar esta tabla como una certificación de frescura total. [Evidencia y pendientes](refresh-2026-09-29.md).

## Corte del 28 de septiembre de 2026

Se consultó `commits/master` de las 25 fuentes directamente en `github.com`: 22 conservan el SHA y tres avanzaron. Collector y Catalog sólo modifican CODEOWNERS; Fury incorpora acciones start/stop, teardown observable y detección de drift outbound. Las referencias técnicas activas de esos tres repos apuntan al SHA de este corte. Ver [detalle del refresh](refresh-2026-09-28.md). La auditoría previa de los 22 repos sin delta sigue siendo aplicable al mismo código; no se presenta como una nueva ejecución de sus tests.

La [revalidación de septiembre](refresh-2026-09-23.md) integró los 18 deltas iniciales de las 25 fuentes y KMS al cierre del 24: 19 deltas revisados y seis repos sin cambios. Roster SIG: 25 apps; SDK Events relacionado y connector sin código canónico. La revisión independiente posterior abarcó 663 IDs y 58 fronteras; correcciones documentales no certifican seguridad ni despliegue. Los artefactos y resultados de evaluación se mantienen en [docs/10](../10-evaluations/README.md); el cierre semántico de fuentes no equivale al cumplimiento de las respuestas.

Commits inspeccionados en el último corte integral integrado. Las fichas L2 conservan archivos fijados a esos SHAs; la revalidación focal posterior de Playmaker se registra arriba y no declara vigente todo su catálogo. El 2 de septiembre de 2026 se resolvieron 18 repositorios; el 8 de septiembre se revalidó el roster autenticado de SIG, se resolvieron los siete repositorios nuevos y se reauditó el SDK Go porque su `master` había avanzado. Las refs se consultaron explícitamente en `github.com`; no se usaron ramas default implícitas ni refs locales como fuente de vigencia.

| App/repositorio | Rama auditada | Commit verificado |
|---|---|---|
| `fury_ads-signals-collector-api` | master | `a1891f014d68b8d39169d3ad760dd9644fd5ada0` |
| `fury_rio-e2e-ui` | master | `88080c3e916c196eabf0703cbea7b4ac65506847` |
| `fury_rio-e2e-ltp` | master | `8475528fdc2e02fa659a763281f924ee092126e2` |
| `fury_rio-controlplane-flink` | master | `d196951dc6332769e9e60a2b54dfb19cbc60811c` |
| `fury_rio-controlplane-signals` | master | `055cc225186a2bbabb4fff6daa3605bdf5fd09ff` |
| `fury_rio-controlplane-observability` | master | `ad602127c33fe6aac375ad8382186c92f3572c69` |
| `fury_rio-controlplane-clickhouse` | master | `50de0f8e091f7bcf028981d54487d8003c849b43` |
| `fury_signals-sdk-node-js` | master | `0f4edf00268a3c2206abe68b1fb6e20919029637` |
| `fury_rio-kc-signals-to-gcs` | master | `7ab5a6c3d7056693881854ce783cf67a98ff34ab` |
| `fury_ads-signals-sdk-go` | master | `329809d30a108ddf22259dfed697f139c9d9f7a4` |
| `fury_signals-sdk-python` | master | `dadfc0d5a6479ec4e8959afe994552cb88bd0db6` |
| `fury_signals-sdk-java` | master | `96408638b734c73723f58baccf93871ddd9d0f8b` |
| `fury_ads-signals-catalog` | master | `c6ac1321f66c021cee36066ca8c07c638b4f787d` |
| `fury_rio-controlplane-fury` | master | `d760e56ae13c150121d3930577a2945571fb67e6` |
| `fury_signals-sdk-sandbox-python` | master | `544412593cc41bf63a2be7d20b23b14f58bcb4ee` |
| `fury_rio-controlplane-kms` | master | `3d098bb8f534d301ec695ffafb91fcca419886ed` |
| `fury_rio-playmaker` | master | `3cd0daf6e17841ab79381f1eb5e2bd014ad68bd1` |
| `fury_rio-flink-sql` | master | `6ad953217fbaf5b741b938bcbaf0f309f1d92824` |
| `fury_rio-controlplane-kafka` | master | `f74e856ef3de881e2d504c6cb1ced573681c1058` |
| `fury_rio-copilot` | master | `922baf9feb3fcce9f0de5e154a77be9a40310401` |
| `fury_ads-signals-frontend` | master | `268c86d826515350fa447964f63b44289a6f012c` |
| `fury_rio-materializer` | master | `670e5ed9b684ea3b984642dd4efeaba667ce5f2a` |
| `fury_dps-rio-docs` | master | `3d72acbe288c56316f6585a74e56aa387c445f86` |
| `fury_rio-entity-service` | master | `25b34c73b97327ad2f247689dd5e660e0d209b5b` |
| `fury_rio-sdk-events` (relacionado) | master | `ad2c98b806cffb88b23513f87785932aa1707ea4` |

## Excepción

`rio-connector-kafka-clickhouse` aparece en el inventario SIG de Spellbook, pero `fury get` no resolvió la app y no apareció un repositorio canónico en la organización consultada. Confianza sobre su operación actual: **baja**. No usar su nombre para inferir un flujo en producción.

## Inventario de origen y frescura

La consulta autenticada del proyecto Spellbook `SIG` revalidó el 24 de septiembre de 2026 el mismo conjunto de 25 apps del 8/09 (sin altas/bajas): `ads-signals-collector-api`, `rio-e2e-ui`, `rio-controlplane-flink`, `rio-controlplane-signals`, `rio-controlplane-observability`, `rio-connector-kafka-clickhouse`, `rio-controlplane-clickhouse`, `signals-sdk-node-js`, `rio-kc-signals-to-gcs`, `rio-entity-service`, `ads-signals-catalog`, `rio-controlplane-fury`, `signals-sdk-sandbox-python`, `rio-e2e-ltp`, `rio-controlplane-kms`, `rio-playmaker`, `rio-flink-sql`, `rio-controlplane-kafka`, `rio-copilot`, `ads-signals-frontend`, `rio-materializer`, `dps-rio-docs`, `fury_signals-sdk-python`, `fury_signals-sdk-java` y `fury_ads-signals-sdk-go`.

De esas 25 apps, 24 tienen repositorio canónico resoluble. `fury_signals-sdk-python` es la fuente de verdad del SDK Python; `signals-sdk-sandbox-python` se conserva sólo como ejemplo secundario y no se mezclan sus contratos. `fury_rio-sdk-events` es una fuente relacionada, no una membresía SIG. `rio-connector-kafka-clickhouse` conserva membresía confirmada, pero sigue sin código canónico resoluble y por eso permanece como excepción de baja confianza. `rio-frontend` legado no se usa como fuente ni forma parte del scope documental.

Registro histórico: los siete repositorios incorporados y el SDK Go se verificaron contra `master` canónico el 8 de septiembre. La auditoría de los otros repositorios corresponde al 2 de septiembre; sus SHAs no se declaran refrescados por la sola revalidación del roster.

Registro histórico de la auditoría del 2 de septiembre (no estado del refresh actual): ocho HEAD no cambiaron desde su manifiesto previo: E2E UI, SDK Node, Catalog, sandbox Python, Kafka CP, Materializer, Entity Service y SDK Events. Los otros diez se auditaron por entrypoints, registries, tests y contratos: Signals volvió a incorporar deployment/actions/KVS; Observability incorporó OTel tag sync; Fury añadió destinos BigQueue/KVS e identidad fan-in; KMS consolidó register/deliver/OTT; ClickHouse añadió ownership KVS, acciones start/stop de materialized views y un preload temporal de credenciales; SDK Go incorporó un cascade REST-only para señales sin destino Kafka; Playmaker y Frontend cerraron la consulta moderna de logs, y el routing base de Playmaker de aquel snapshot enviaba los tres tipos Signals al fallback Materializer REST (becd61f0, revisado el 23 de septiembre, vuelve a seleccionarlos por BigQueue); Flink añadió enriquecimiento CloudWatch allowlisteado para fallas AWS y control de retries Nexus —el runtime reason genérico sigue siendo sensible y puede loggearse y persistirse cuando cabe, sin duplicarlo en el reason enriquecido—; Collector añadió signals inactivas, endurecimiento GCS y observabilidad de recovery. La existencia en código no acredita flags, bindings ni estado productivo.

No se persisten tokens, cookies ni respuestas completas del proyecto. Una renovación de sesión sólo debe usarse de forma efímera para refrescar este manifiesto.

### Checkpoints candidatos, no canónicos (2026-10-01)

Actualización focal de evidencia del 02/10: T23 está checkpointed en `eee5b90`; T24/T25/T26 son snapshots de autoría con hashes, no un nuevo master ni prueba de wiring productivo efectivo. La verificación live de EntityService quedó bloqueada por Zero Trust y por HTTP 400; no prueba target ausente. El protocolo rootv3 de journals/generaciones/cleanup sigue PENDING_PEER. Las tablas de fuentes canónicas y las demás fronteras conservan su corte integrado.

SDK Events `97146e9fde6cb2d947b7978ba2ba2491d11f06b5` sobre master `ad2c98b806cffb88b23513f87785932aa1707ea4` corrige el ProducerBuilder; Playmaker `1b4b8e1554c37357e4b39e1860be6ad43f9aa640` sobre develop `7673f4bffc286f0f24d4214938df53c4c5eb9c38` prepara transporte y gate Kafka real. Son commits de trabajo locales pendientes de integración/release, no evidencia de integración del slice completo ni ejecución E2E. El transporte local de deployments de Playmaker sí está ya en master `0c83575`; los adapters de acciones/KVS/Service PEEK real de ese checkpoint siguen pendientes. Ver el [runbook candidato](../04-troubleshooting/kafka-real-e2e.md).

Kafka CP checkpoint actual `eee5b9091b332a975c78823679a1e99b517632bc` (commit local candidato), rama `feature/kafka-real-e2e`, base develop `4302481c69300074a85ea5eb051a27bbd505cdce`. Incorpora T21/schema mínimo 1 y T23/metadata wire antes del executor/claim; no activa Validator global. El corte versionado mantiene **351 filas: 297 FULL preparados,26 PARTIAL y28 NONE**, todas NOT_EXECUTED para la capacidad completa. La regresión T23 pasó con 804 tests/0 fallos/0 errores/0 skips Java25, tres familias compiladas y bootJar; el primer full de 804 tests con cuatro fixtures positivos incompletos queda preservado como FAIL. T24 aporta cuerpos nuevos posteriores al corte, aún pendientes de peer; no se reclasifican las diez filas PM NONE sólo por esa autoría. [Fuentes y límites T23–T26](kafka-canonical-audit-2026-10-01.md#preparación-t23t26-y-límites-de-la-evidencia). KVS403, EntityService/managed/runner y verificación de cleanup impiden certificar el negocio. No reemplaza master `f74e856e`.

Snapshot histórico T21 CP `f80ea19421518251515aae768d020f574ad255bb`: 722 tests unitarios, matriz 351/299 FULL preparados/24 PARTIAL/28 NONE y peer 4 red→25 green. Ese corte antecede T23; no es metadata del checkpoint actual.

Snapshot histórico previo CP `0d8e1fedd0fd6db8907b1c810dbad9d22c296312`: matriz 341 y regresión 712; se conserva como corte anterior, no metadata del checkpoint actual. La revalidación focal Playmaker añade dos IDs canónicos al corpus (691) sin revalidar el resto del catálogo.


Suplemento candidato posterior02/10: [corte de implementación acotada](kafka-canonical-audit-2026-10-01.md#corte-posterior-de-implementación-y-verificación-acotada--0210). Source RootV4.1 freeze29 `2be8b9deead072c1d8b8373ed8e4b7052b5073deb263d0965a12c2dbdafd2944`; OneTest final `ef816608d673c4a9e7cb0cd7a7de813b7a9f6fd776263f52982476b51ae6ff57`, peer `c9819dd8a29f50804bc6e471058b1a3da2e47270d77c7777123b60c7ce3e62fb`. No cambios de SHA canónico ni IDs. CP822unit/compile3 y preparación revisada304/29/18 siguen WORK_BRANCH_PENDING,351NOT_EXECUTED; Root y matriz PASS_SOURCE_NEUTRAL_PEER_ONLY/PASS_PREPARATION_PEER_ONLY. Refresco GitHub reciente403; no últimoHEAD/despliegue afirmado. Evidence vive en CP `meli/features/20261001-real-e2e/evidence/`; los receipts backend requeridos no existen todavía.


Receipt posterior: freeze agregado Root29 SHA256 `23409c2bc593f8373a419255e4c00b08747f8d01f2499a95e17755795f50b0b1`; peer r2 independiente `dd28a38d2419f35ec5a8aa2f19b01d78b6e0233b0e087f944564d4c598d6c30d`; peer de preparación de matriz `b5360b1d397aa7f693a2b188a258ad4070fb87ff2b542bcea8348004bde954a2`. El core V4.1 histórico conserva el finding de owner PID y los dos fallos del driver; r2 los cierra sólo en fuente/controles neutrales. Dos corridas del autor y dos independientes nuevas pasan14casos/159checks sin cambiar47aserciones/14casos/plazos. No se certifica SDK productivo, backend ni E2E completo.


### Candidato local en memoria — 2026-10-05

La última decisión del owner elimina Fury Sandbox como gate del E2E local CP y deja el ecosistema para después. CP `feature/kafka-e2e-memory@7615b210e5b70667912b956c2f27cc0d1ebc80eb` parte de `7f1720d950446638ff9b15a0e4e167f3e8e26e43`; [diff de la rama de trabajo](https://github.com/melisource/fury_rio-controlplane-kafka/compare/7f1720d950446638ff9b15a0e4e167f3e8e26e43...7615b210e5b70667912b956c2f27cc0d1ebc80eb). `e2e/local.sh` y `e2e/run.sh` sin argumentos seleccionan `localKafkaE2eTest`, perfiles `local,real-e2e,memory-e2e`, cinco brokers reales/RF1–5 y resultados Kafka reales, con reportes `build/local-e2e/<RUN_ID>/`. El `KvsClient` en memoria tiene create/CAS/versiones asignadas localmente/TTL por instancia; restart pierde estado y dos JVMs no comparten claims. Primera corrida física: 343 invocaciones, 309 fallos, 34 PASS y 0 skips; cinco brokers saludables y metadata interna, host Kafka inaccesible. Gate físico BLOCKED y replay limpio final pendiente. Los 845 unitarios PASS, reproducidos independientemente desde clon limpio inicial (65 clases, cero fallos/errores/skips; log SHA256 `11b5532664724e9202d30c138537c2d833b34e357743fd5caf275f9d3fa5c9f5`), y 49 controles independientes PASS no certifican negocio. Matriz local 356: 5 PASS unit/config, 226 BLOCKED por host Kafka, 125 NOT_EXECUTED fuera de selección. Workflow local implementado/NOT_EXECUTED. No acredita KVS Fury, ecosistema, OAuth, BigQueue ni CI corporativa. [Comandos, fuentes y límites](../04-troubleshooting/kafka-real-e2e.md#corte-local-de-trabajo--0510).

El suplemento documental CP `4c66d0d5ca77e1de4aef5b08c9e601921eb60a9b` actualiza únicamente `e2e/LOCAL.md` y `evidence/local-memory-2026-10-05.md`; el core `7615b21` permanece intacto. Esta fecha verifica únicamente el delta candidato; no es un refresh de masters ni de las 25 fuentes. La tabla canónica y las evidencias históricas Sandbox conservan sus SHAs y estados. No se agregan feature IDs.
