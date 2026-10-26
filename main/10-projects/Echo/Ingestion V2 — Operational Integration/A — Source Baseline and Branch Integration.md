---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[F — Decision Register]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-26"
---

# A — Source Baseline and Branch Integration

## Propósito

Fijar el baseline efectivo, los deltas y la integración segura del nuevo workstream dentro de Echo. La inspección de fuente no certifica ejecución.

## Contenido

### A1. Corte verificado y autoridad

Inspección read-only del 2026-10-26. Se contrastaron HEAD local, limpieza del checkout y `git ls-remote --heads` del remoto. No se ejecutaron builds, suites, migraciones, procesos de producto ni conexiones a infraestructura operacional. Los nombres se consultaron también mediante GitHub; los SHAs proceden de Git, no de una nota histórica.

| Repositorio / rama | SHA completo efectivo | Papel |
|---|---|---|
| xKoRx/echo · `lab-v4/shot4-integration` | `b2b3ebfe3337b3b44034c5be3bf00b8379c8f1ce` | Única base Echo del workstream y destino obligatorio del incremento endpoint |
| xKoRx/echo · `feature/ef-runtime-pools` | `0e17c4d3f1179cde709f923c8dd28e8cd853afc9` | Referencia concurrente; NO base ni destino de integración autorizado |
| xKoRx/symphony · `lab-v4/shot4-symphony` | `a0c68d154b733049c97bf46e69c4629078d40c05` | Candidato Forge para adapter V2 y paridad; no prueba de despliegue |
| xKoRx/agents-os · `master` al comenzar | `57f8f37ed4a3ce20fc6044ed066bc6e5bfacbf34` | Documentación directa en master; commit de entrega posterior identificable por change_log |

Ancestro común de las dos ramas Echo: `ac0621a1917a9ecbed50b3daed4add1518ffc71d`. `rev-list --left-right --count` da **125 commits exclusivos The Lab / 64 runtime**. `feature/lab-v4-ingestion-v2` no existía en remoto al observar; verificar otra vez al crear. Los tres checkouts de producto estaban limpios. No se modificó ninguno.

### A2. Cómo leer CURRENT

`EXISTS_AND_VERIFIED` en esta tabla significa existencia, llamada y comportamiento **comprobados por lectura en el SHA indicado**, no PASS funcional nuevo. `EXISTS_UNVERIFIED` significa código presente cuya ejecución efectiva no está acreditada. `PARTIAL` y `CONFLICTING` tienen un delta demostrado; `MISSING` se limita a la superficie buscada. Evidencia histórica del Shot4 no se extrapola a producción ni a otra rama. Owners son responsabilidades de módulo para GLM, no personas supuestas.

Todos los localizadores Echo siguientes son relativos a xKoRx/echo@b2b3ebf; Symphony a xKoRx/symphony@a0c68d1. Los nombres TARGET de B son diseño explícito y no símbolos encontrados.

| ID / capacidad | Estado | Owner y fuente efectiva | Contrato vigente / delta congelado |
|---|---|---|---|
| G01 HTTP real / auth | EXISTS_AND_VERIFIED | Gateway: `v3/gateway/internal/server.go`, `lab_v4_gateway.go`, `v2_wire.go`; `cmd/echo-gateway-harness/main.go` | NewServer monta V2 con PG/config y devuelve503 sin dependencias. Roles/scopes resueltos server-side. Harness reutiliza el router productivo. Endurecer rutas exactas, PUT estricto y fallo de artifact store; gate físico NOT_RUN aquí. |
| G02 DTO y versión | PARTIAL | SDK contracts `strategy_ingestion_v2.go`, `strategy_history_v2.go`, `wire/hash.go` | DTO V2 y recetas existen. `declared_version_ref` sólo se valida sintácticamente; `DefinitionContentDigest` existe pero registry no lo compara. Evidencia temporal UNKNOWN no cabe en los tres strings obligatorios de VersionDefinition. B2/B3. |
| G03 receipt / tx / registry | PARTIAL | SDK PG `strategy_history_v2_service.go`, `strategy_history_v2_put.go`, `strategy_ingestion_v2_registry.go` | Receipt snapshot durable, llave scoped, tx y outbox reales. Artifact nil se tolera; filesystem escribe al nombre final; metadata apunta digest sintético sin bytes; locks de historias no se ordenan pese al comentario. SQX/native reinsert idéntico por key nueva produce409 y se descartan dependency_artifacts con `[]`. B3/B4. |
| G04 definición / Magic | EXISTS_AND_VERIFIED | Registry anterior; migraciones `068_lab_v4_registry_recipes`, `076_lab_v4_w1_repairs` | `strategy_definitions`, runtime links, instrumentos y terna Magic nullable existen. Primera asignación protegida por `fn_v4_assign_magic_allocation`; no inventar otro registry. Falta conectarla al provisioning certificado sin mutar fingerprints de recibos históricos. B2/B5. |
| G05 historias N→N+1 | EXISTS_AND_VERIFIED | `strategy_history_v2_put.go`, migraciones071/076/081 | CAS/replay, revisiones completas e inmutables, temporal evidence y dirty existen. Auditar wrapper JSON, lock global y metadata por versión para evitar last-writer-wins entre historias. No rehacer modelo económico. |
| G06 profile / binding | PARTIAL | `runtime_binding_repository.go`, `lab_v4_gateway.go` | No resolver durable de DeploymentProfile hallado. Provision inserta accounts `source_system=harness`, usa LIVE/SIMULATED constantes, config `{profile,version_ref}`, digest sin config completa, targets del cliente. CreateBinding mueve head sin CAS. B5 reemplaza esos atajos, no la tabla. |
| G07 instalación / ACK | PARTIAL | `runtime_config_supervisor.go`, `runtime_ack_repository.go`; Core `cmd/echo-core/main.go` | Supervisor existe pero main lo instancia con installer nil. Claim global, ACK de targets por un mismo owner, lease15s sin renovación tras DELIVERED, ACK activa incarnation entrante, readiness puede aceptar head ausente/sustituido. B6. |
| G08 consumidores | EXISTS_UNVERIFIED | `v3/sdk/kache/account_configs.go`, `strategy_configs.go`; `v3/core/internal/functions/strategy_config.go`; `v3/bridge/internal/pipe_handler.go` | Cache Kafka y StateFun config lookup existen; Bridge SendConfigUpdate→SendClientConfig existe. Enviar no acredita aplicación ni checkpoint. Adaptar estas rutas; no un config system paralelo. |
| G09 ingress reference | CONFLICTING | `v3/core/internal/functions/master_observation.go`; `v3/core/deploy/flink-statefun/develop/module.yaml` | Busca cuenta+Magic activo sin namespace/source-instance/instante; sintetiza source-instance y event ID; rutas paralelas hacia planner, observation y legacy journal. B7 fija owner único y envelope exacto. |
| G10 journal canónico | PARTIAL | `master_observation_service.go`, `trade_journal_owner_tx.go`, `trade_journal.go` | Owner SaveOpenTx/SaveCloseTx y receipt/intake/cycle/outbox atómicos existen. cycleExists ignora scope; secuencia fija OPEN1/CLOSE2; management/correcciones incompletos. Conservar journal y añadir fencing/correlación exacta. |
| G11 copy / MM / nuevo riesgo | PARTIAL | `execution_planner.go` doProcessReferenceEvent; `runtime_readiness_gate.go`; Core main WithNewRiskGate | Planner usa config/policies/MM existentes, pero ruta reference carece gate V2. Gate nativo elige binding por strategy y `LIMIT1`, insuficiente con varios runs/cuentas. B7/B8: autoridad pinneada y gate último envío. |
| G12 journal→history | CONFLICTING | `master_observation_service.go` DrainJournalOutbox/HistoryFromJournal | El drain resuelve una identidad con LIMIT1 para filas del namespace y marca todos sus pendientes; usa POST de registro sintético y no snapshots N+1 acumulativos. Además se llama sincrónicamente desde MasterObservationFn. B9 elimina mezcla/pérdida y dependencia analítica. |
| G13 analytics y ranking | EXISTS_AND_VERIFIED | `v3/lab-worker/cmd/labv4-worker/main.go`, `internal/workers/analysis_worker_v4.go`; SDK `lab`, `postgres/lab_*`; `v3/shared-analytics` | Loop real relay/claim/compute/publish/ranking, cuatro perfiles, dos presets, generations y cohortes existen. Reutilizar y probar nuevos inputs; no motor nuevo. |
| G14 UI / Hasura | EXISTS_AND_VERIFIED | `v3/front/src/composables/useLabV4Bundle.js`; `services/graphql/labV4Runtime.js`; `components/lab/v4/{StrategyScreenerV4Table,StrategyDashboardV4,StrategyLabV4Tab}.vue`; `v3/hasura` | Read bundles, screener/dashboard y permisos V4 existen; probar coherence N/N+1/roles en harness. No export/apply ciego de metadata compartida. |
| G15 Forge V2 | PARTIAL | Symphony `sqx/adapters/echo-handoff/http_ingress_v2.go` y test; `sqx/adapters/registry-postgres/strategy_version.go`; `sqx/activities/worker/forge_seal_handoff.go` | NewHTTPIngressV2 sólo tiene callers de test en búsqueda Go. Store opcional, manifest previo no compara digest, receipt no se valida íntegro, errores de Update ignorados. CanonicalJSONV2Digest y DigestCanonicalBytesV2 comparten la misma receta; conservarla y comprobar parity del body. Reusar store/flujo durable existente con adapter V2; no nueva campaña. B10. |
| G16 autenticidad Forge | BLOCKED_EXTERNAL | SHOT4_FINAL_HANDOFF / INDEPENDENT_FINAL_REVIEW | Falta copia auténtica autorizada con trade list y lineage; no inferir existencia actual ni pedir fixture falso. Bloquea sólo certificación AUTH_FORGE/E2E auténtica, no diseño ni harness sintético. |

### A3. Divergencia material con runtime

En runtime@0e17c4d se inspeccionaron `v3/core/cmd/echo-core/recovery_plane.go` (readiness reconsulta permits/market freshness y no presume arming), `v3/futures-bridge/internal/permit/permit.go` (último salto, revocation epoch, TTL≤1s y fallo cerrado), y diferencias de los módulos de ownership, observation/recovery y configuración. Runtime añade `echo-runtime-control`, recovery attestors, owner continuity, fxpermit, journalfs y autoridad de cuentas del futures-projector. The Lab contiene correcciones de Gateway, registro, workers/read bundles y tests que runtime no hereda automáticamente.

**Colisión SQL concreta:** runtime `081_futures_account_authority.up.sql` y The Lab `081_lab_v4_wperf_history_maintain.up.sql`. Última migración candidata The Lab: `083_lab_v4_fix3_metric_values_bundle`. El mismo número no identifica el mismo cambio. No renumerar ni editar bytes de migraciones ya aplicadas; una futura reconciliación necesita ledger/checksum por linaje y plan forward explícito.

Convergencia futura, fuera de estos cuatro shots: refrescar ambos SHAs y migración ledger; matriz de ownership por Core/Bridge/SDK/StateFun/projector; conservar conjunction de binding readiness **y** recovery/permit/market freshness; conciliar identidades/epochs y migraciones mediante cambios mínimos revisados; probar ambos caminos en harness; gate independiente de integración runtime, después autorización de despliegue/cutover. El PASS del endpoint jamás permite saltar estos gates. No tocar extracción Forge, runtime paralelo ni cuentas compartidas.

### A4. Protocolo de rama e integración temprana

1. Shot2 registra repo remoto, status limpio, worktrees, ramas existentes y SHAs remotos. Fetch sólo refs necesarias; verifica que base contiene b2b3ebf mediante ancestry. Si base avanzó, revisa su diff y adapta el delta compatible; no fija un HEAD viejo sobre trabajo ajeno. Si perdió ese linaje, detiene integración con evidencia específica, sin inventar otra base.
2. Crea checkout limpio y rama `feature/lab-v4-ingestion-v2` desde el HEAD remoto **actual** de `lab-v4/shot4-integration`. Si el nombre existe: reutilizar sólo si ownership y linaje del mismo trabajo están probados; de lo contrario elegir sufijo nuevo y registrarlo. No reset/stash cambios ajenos. Guardar `BASE_SHA` y árbol limpio.
3. Implementa únicamente incremento E (C2), con commits autocontenidos. No comenzar código operacional pendiente en esa rama antes del gate. SQL sólo si necesario, aditivo y con ledger runner. Test real Gateway+PG+artifact store con perfiles REGISTER_ONLY; PROVISION_REFERENCE aún no implementado responde503 explícito antes de cualquier escritura, nunca PROVISIONING ficticio. Esa restricción transitoria queda visible y se elimina al completar binding.
4. Obtiene `ECHO_INGESTION_V2_ENDPOINT_INTEGRATION_PASS` según C1 sobre `ENDPOINT_SHA`; publica evidence manifest fuera del vault y resumen compacto. Si baseline ya cumple todo el gate tras prueba efectiva, registra PASS sobre BASE_SHA y ningún merge ficticio. La lectura de este Shot1 **no** otorga ese PASS; G02/G03 muestran delta real.
5. Refresca destino inmediatamente. Si no cambió, `ENDPOINT_SHA` debe descender del destino y contener sólo commits E. En checkout de integración limpio y propio, incorpora con fast-forward (`merge --ff-only`); push normal al destino. Si cambió, fusiona primero el nuevo destino en la rama de trabajo sin reescribir commits; resuelve sólo conflictos propios, inspecciona diff completo y vuelve a ejecutar gate/regresiones afectadas. Después destino debe ser ancestro; repetir fetch/fast-forward. Rechazo non-fast-forward obliga refrescar/reverificar; jamás force-push.
6. Si existen commits ajenos intercalados, no usar cherry-pick ciego ni cambiar destino. Comparar parent graph y diff contra destino; demostrar que todos los commits propuestos son E+destino. Si no es demostrable, conservar trabajo en rama y reportar conflicto concreto; no integrar un parcial.
7. Registra `BASE_SHA`, `ENDPOINT_SHA`, destino antes/después, SHA realmente publicado y hash del evidence manifest; `ls-remote` y ancestry confirman integración. El hito se cumple **antes** de continuar provisioning/copy/analytics/UI. Sin deploy.
8. Sincroniza la rama de trabajo por fast-forward al destino integrado verificado. Registra `RESUME_BASE_SHA`. Sólo entonces empieza los demás incrementos; cada uno completo con su gate. Final Shot2 entrega candidate y diferencias integradas/no integradas exactas. No hay integración autorizada a runtime ni master de Echo.

Rollback de código = revert nuevo revisado en rama adecuada, sin borrar historia. Migraciones con datos se corrigen forward; deshabilitar la ruta propia conserva receipts/evidencia. No down destructivo. Documentación Agents-OS siempre directo master y push normal, sin PR ni cierre de sesión.

### A5. Límites heredados

Las **49 filas H01–H49** de SHOT4_FINAL_COVERAGE_MATRIX contabilizan 48 PASS/1 FAIL histórico (H45 prepare bundle). QA-01 es transversal y separado, coverage histórico ~85.8%/~85.2% menor que95%; encabezados antiguos 47/49 mezclaron denominadores. AUTH_FORGE sigue excepción de autenticidad; installer nil es defecto implementable, no recurso externo. Este workstream no reabre Shot4 anterior ni concede no-regresión por inferencia: C exige repetir H afectados en el nuevo SHA y señalar toda degradación. H45 no cambia budget para parecer verde.


## Fuentes

- Mandato Owner 2026-10-26; [[F — Decision Register]] D25/D26.
- [[A — Source Baseline and Branch Integration]] contiene los SHAs y localizadores efectivos.
- Contratos compatibles de `10-projects/Echo/The Lab/V4 — Runtime Integration/` y [[Echo + Echo Forge — Environment Contract]].
