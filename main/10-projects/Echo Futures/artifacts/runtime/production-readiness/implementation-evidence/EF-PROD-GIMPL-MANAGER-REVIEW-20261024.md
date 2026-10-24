---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — Runtime Pools]]"
  - "[[EF-PROD-GOD-05-MANAGER-ADJUDICATION]]"
  - "[[EF-PROD-GOD-03-IMPLEMENTATION-PLAN]]"
  - "[[EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-24"
updated: "2026-10-24"
---

# EF-PROD — Manager G-IMPL Review (2026-10-24)

## Propósito

Una **revisión consolidada** del candidato GLM B1–B3, sin rediseño GOD ni nuevos shots FEFB. Primary Manager GPT-6 revisó source remoto y evidencias del Submanager; no ejecutó tests ni accedió a runtime, terminal, Kafka, ETCD o StateFun.

## Contenido

### Dictamen

**G-IMPL = BLOCKED — FINAL_INTEGRATION_CLOSURE**, sobre `xKoRx/echo feature/ef-runtime-pools@602dfcadb113224e76fa631415eb8009eaa6e201` (SHA remoto reconfirmado).

Se conserva el trabajo válido: delta integrado, siete especialistas ONE-SHOT y dos defectos W6-D1/D2 corregidos, 78 paquetes Go OK y siete fallos heredados reportados, C# harnesses y pruebas de baseline según evidencia local. No significa que esas pruebas se re-ejecutaron por Manager. F01–F09 no se reabren para rediseño; se exige cerrar las fronteras operativas de la entrega como UNA corrección de integración dentro de B3. G-ENV/G-FEED/G-REC/G-SIM/PROD siguen NO AUTORIZADOS.

### Hallazgos agrupados y acciones de cierre

**GI-01 — P0 / Kafka egress M1 con schema incorrecto (source confirmado).** Tanto `v3/core/deploy/flink-statefun/develop/module.yaml` como `production/module.yaml` escriben seis veces `deliverySemantic: exactly-once` como scalar. El contrato oficial Apache StateFun 3.2 Kafka egress declara `deliverySemantic:` objeto con `type: exactly-once` y `transactionTimeout` (consultar schema efectivo/JAR antes de fijar unidades). Un comentario del YAML no acredita transacciones. Corregir ambos manifests, dejar un verificador de schema previo al despliegue contra runtime/JAR versionado e incluir comprobación L3 aislada de commit/abort/read_committed/espera checkpoint, tamaño y timeout. No desplegar hasta demostrar la configuración aplicada. Referencia: https://nightlies.apache.org/flink/flink-statefun-docs-release-3.2/docs/modules/io/apache-kafka/

**GI-02 — P0 / RecoveryControl aún no tiene recorrido operacional obligatorio.** `v3/core/internal/runtimecontrol/` contiene `Submitter.PlanStart/Restore`, pero `v3/core/cmd/` sólo posee `echo-core` y `echo-functions`; no se encontró una entrada de despliegue invocando ese submitter. La evidencia GLM difiere el CLI a G-ENV. Sin integración verificable del único submitter con el mecanismo que realmente levanta Flink, el autor antiguo podría seguir iniciando un job sin restore. Además, `submitter.checkOffsetWindows` retorna éxito cuando `OffsetWindow == nil`, aunque C-KAFKA-1 exige comprobar retención de TODOS los offsets de un restore. El `ManifestLoader` cableado en Core es `FileObjectStore` limitado a `file://`, mientras GOD-02 propone almacenamiento independiente S3-compatible. Elegir e implementar UNA vía compatible: control del deployment actual y almacenamiento de manifests/objetos realmente accesible, con Kafka offsets obligatorios o denegación clara. En laboratorio aislado demostrar `submit→restored state+offsets` y `missing/incompatible→BLOCKED`. No nuevo daemon/orquestador. Verificar que no haya ruta de submission paralela. La RCA original E01 puede seguir `UNRESOLVED` si la clase entera de fallo queda cerrada por pruebas reales, sin inventar causalidad.

**GI-03 — P1 / Ready sólo describe una parte del runtime, no su autoridad efectiva.** En `v3/core/cmd/echo-core/recovery_plane.go` `readinessInput` fija `MarketKnown:false` y deja `PermitsIssued:false` sin lectura de fuente. `refreshReadinessLoop` crea un `ReadyInput` UNA vez fuera del ticker y lo reutiliza en cada iteración; un cambio en attestation/permit/freshness no refresca esos datos. En `v3/core/internal/runtimecontrol/readiness.go`, `snap.Ready` no depende de market_fresh. Es correcto fail-closed ahora, pero **no acredita el circuito de readiness/arming final** exigido por GOD-02/05. Conectar al estado del stream/gate y permiso reales o, si la arquitectura separa `/ready` (liveness de operaciones) de `NEW_RISK_ELIGIBLE`, documentar y probar que el último salto rechaza stale/unknown aunque `/ready` llegue a true. Cada poll debe reconstruir la lectura; guard singleton no reemplaza market/account readiness.

**GI-04 — GAP DE VERIFICACIÓN / QA del SHA final.** La matriz muestra porcentajes por archivo, incluidos `observations` 94.2%, `producer` 92.6% y `publisher` 91.3%, pero no un numerador/denominador global reproducible del **código nuevo completo** conforme GOD-03 `>=95%`; no promediar porcentajes ni excluir guardas por llamarlas defensivas. Publicar profiles/scripts/diff y ratio global, además de race baseline documentada. W6 fue interrumpido antes del dictamen final y el submanager finalizó las verificaciones; exigir re-review independiente fresco sobre **SHA final con merge Owner**, sin cambiar código desde ese verificador. Tests CI/integration de module config, C# wiring y recovery con negative controls deben detectar que GI-01/GI-02 no estaban acreditados.

### Alcance y continuidad

Un **único bloque correctivo GI-01..04 dentro de B3**, owner SUBMANAGER GLM LOCAL, aprovechando **workflow nativo de ZCode** con agentes de config/lifecycle/readiness y verificador read-only en worktree independiente. Concurrencia máx. 2 workers con archivos disjuntos, un solo integrador, pruebas red→green, sin invocar otro GOD. No volver a ejecutar suites enormes salvo áreas afectadas y barrido final del SHA; no fragmentar entregas al Owner. Si los tests L3 aislados no son accesibles, cerrar sólo source y G-IMPL permanece blocked con evidencia precisa; no proclamar recuperación física. Todos los commits source en rama runtime por FF, cero force/rebase ajeno; Agents-OS master por delta, readback.

**Continuación después del cierre:** manager adjudica G-IMPL → G-ENV/G-REC aislados (incluidos job restart/checkpoint, Kafka transaccional, PG outbox) y G-FEED Ninja integrado feed-only con Owner → G-SIM por permiso Owner → G-PROD por alcance real/cuentas/protección. Ningún permiso de LIVE/PROD derivado de esta revisión.

### Estado de entorno

**No deploy, no órdenes, sin autorización de SIM/LIVE, PROD NO-GO.** El F1 DEV existente no se modifica en esta revisión. El proceso de GLM no debe tocar procesos compartidos, grupos/offsets Kafka del Owner, credenciales, ETCD económico o el terminal Ninja.
