---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[Echo — E-04 Forge Ingestion E1]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases:
  - Echo certification backlog
  - F-04 deferred certification
tags:
  - kind/doc
  - area/echo
  - project/echo
created: "2026-09-13"
updated: "2026-09-15"
---

# Echo + Echo Forge — Deferred Certification Backlog

## Propósito

Mantener en un carril único, ordenado y no ejecutado las certificaciones físicas y cross-lane que quedaron fuera del critical path de desarrollo de Echo/Echo Forge.

## Contenido

### Decisión de gestión congelada

La certificación física/de infraestructura se retira temporalmente del critical path de desarrollo mientras se construye el Aranea MCP Access Plane; no se waiva. `IMPLEMENTED != CERTIFIED`. No se cambia ningún contrato frozen, no se inventa evidencia y no se marcan PASS T2.11, T2.12 ni T2.13.

### Taxonomía de estado

| Estado | Significado | Evidencia mínima |
|---|---|---|
| PLANNED | Trabajo definido, no ejecutado | alcance y dependencias |
| IMPLEMENTED | Código/configuración materialmente implementado | diff y tests del scope |
| SOURCE VERIFIED | Fuente y contratos verificados | revisión/gates source |
| RELEASED | Artefacto publicado desde SHA autorizado | manifest y digest |
| DEPLOYED | Runtime objetivo ejecuta el artefacto autorizado | deployment proof |
| PHYSICALLY CERTIFIED | Receta real ejecutada sobre runtime físico | evidencia durable end-to-end |
| CROSS-LANE CERTIFIED | Handoff real aceptado por el lane consumidor | receipt y read-back |
| CLOSED | Todos los estados requeridos por la fase están satisfechos | veredicto final y referencias |

Los estados son dimensiones de evidencia; `CLOSED` nunca se deriva de `IMPLEMENTED` o `RELEASED` por sí solos.

### Estado de entrada

F-04: `IMPLEMENTED` y `SOURCE VERIFIED` en product SHA `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`, release `0.2.98` publicada; rollout Linux PASS; Windows bloqueado por policy del viewer MCP. F-04 no está `PHYSICALLY CERTIFIED`, `CROSS-LANE CERTIFIED` ni `CLOSED`. E-04 está `INTEGRATED`, pero T21/AC-37 y `FINAL CLOSED` siguen pendientes. F-05 conserva su split implementación/certificación.

### Backlog ordenado; no ejecutar en esta sesión

#### CERT-F04-01 — Forge physical chain / T2.12

- **Prerequisite product SHA/release:** F-04 `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` / `0.2.98`.
- **Prerequisite infrastructure:** Aranea Access Plane operacional y certificado para los targets de ejecución/observación y el control plane usado por el flujo.
- **Required MCP capabilities:** SSH viewer para identificar runtime; SSH operator/run-command en los hosts que ejecutan SQX/MT5; acceso scoped de observación/escritura al PG/Mongo/object-store del flujo; observación/control Temporal o capability equivalente autorizada; secretos permanecen fuera del agente.
- **Physical recipe:** desplegar y probar la release autorizada en los runtimes canónicos; ejecutar un flujo F-04 real con catálogo CC owner, compile MetaEditor/SQX, persistencia de EvaluationRef, readbacks, seal y handoff; no usar mocks como PASS.
- **Durable evidence:** release/deployment proofs, FlowRun/workflow IDs, Decision V2, allocation/readback, compile inputs/outputs/log, EvaluationRefs, StrategyVersion, HandoffManifest y delivery state.
- **PASS criteria:** el mismo SHA corre en los runtimes requeridos; el flujo real completa sin bypass; bytes, refs, allocation, seal y manifest son verificables y cardinality-safe. Hasta entonces: `PLANNED`/`BLOCKED BY INFRA`, no PASS.

#### CERT-F04-02 — Authentic Forge golden / T2.11

- **Prerequisite product SHA/release:** CERT-F04-01 PASS sobre `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` / `0.2.98`.
- **Prerequisite infrastructure:** mismo access plane y almacenamiento durable/exportable para todos los preimages referenciados por el flujo.
- **Required MCP capabilities:** lectura de evidencia Forge, artefactos y metadatos del control plane; transferencia segura de los bytes auténticos; no capability sintética ni fixture manual.
- **Physical recipe:** capturar desde la ejecución física el golden Forge completo: producer F-04 auténtico, StrategyVersion sellada, artefactos compile/readback, EvaluationRefs y manifest; preservar hashes y provenance.
- **Durable evidence:** fixture/preimages byte-exactos, SHA256/size, refs, producer identity, release manifest y enlace al run físico.
- **PASS criteria:** todos los bytes que el manifest/reference declara existen y verifican; producer es `echo-forge-handoff`; corpus no es copia de S0 ni fakeconsumer. No ejecutar ni marcar PASS ahora.

#### CERT-E04-01 — Echo cross-lane golden / T21

- **Prerequisite product SHA/release:** golden auténtico CERT-F04-02 y Echo E-04 integrado en `a99f9a63354bbe72219d1e590bb93757ed08e45e` o release posterior explícitamente verificada.
- **Prerequisite infrastructure:** runtime Echo desplegado y observable; endpoint de promotions alcanzable desde el producer; PG/artifact store/read surface disponibles.
- **Required MCP capabilities:** observación del runtime Echo y HTTP; lectura scoped del resultado/receipt; acceso de evidencia PG/artifacts según el runbook; no admin secret reutilizado.
- **Physical recipe:** enviar el manifest auténtico por `POST /api/v1/forge/promotions`, verificar `INGESTED`, recuperar por GET by-key y repetir el lookup idempotente sin activar/provisionar/capitalizar.
- **Durable evidence:** request/body digest, HTTP status, receipt, mapping/version/promotion rows, artifact hashes y GET by-key outcome.
- **PASS criteria:** Echo acepta exactamente el golden auténtico, persiste una única proyección consistente, devuelve receipt/read-back estable y no produce efectos fuera de E-04. T21/AC-37 permanece OPEN hasta ejecutar esto.

#### CERT-F04-03 — Real Echo join / T2.13

- **Prerequisite product SHA/release:** CERT-F04-02 PASS, CERT-E04-01 PASS, Forge `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` / `0.2.98` y Echo runtime del E-04 integrado.
- **Prerequisite infrastructure:** ambos runtimes observables/operables por el Access Plane, rutas Forge→Echo habilitadas y control plane con evidencia durable.
- **Required MCP capabilities:** capabilities CERT-F04-01 más observación HTTP/Echo y read-back de receipt/rows; ninguna sustitución por fakeconsumer.
- **Physical recipe:** repetir un run Forge real desde Finalist/StrategyVersion hasta `POST` real y `GET by-key` en Echo, conservando la cadena de identidad y hashes.
- **Durable evidence:** run IDs, release/deployment proofs, manifest/body digest, receipt `INGESTED`, read-backs y no-effects.
- **PASS criteria:** handoff real→receipt real→lookup real converge exactamente una vez y los artefactos se pueden inspeccionar. Hasta entonces, join `DEFERRED`.

#### CERT-F05-01 — Cohesive release/deployment proof

- **Prerequisite product SHA/release:** F-01/F-02/F-03 integrados y F-04 implementación revisada; candidato cohesivo posterior a `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`.
- **Prerequisite infrastructure:** release/deployment proof para cada runtime objetivo y observación suficiente para separar código, binario y proceso.
- **Required MCP capabilities:** source/release/deployment read-back; operator sólo donde la receta lo requiera; no cerrar con marcadores legacy.
- **Physical recipe:** publicar desde la rama autorizada, verificar manifest/digest y demostrar que cada runtime ejecuta el mismo release antes de cualquier FULL golden.
- **Durable evidence:** release manifest, SHA/blob equality, deployment proofs, runtime identity y matriz de superficies tocadas.
- **PASS criteria:** release cohesivo trazable a source autorizado y runtime; no mezclar binario viejo con HEAD nuevo.

#### CERT-F05-02 — FULL authentic golden and result surfaces

- **Prerequisite product SHA/release:** CERT-F05-01 PASS y CERT-F04-02/CERT-F04-03 según el alcance del release.
- **Prerequisite infrastructure:** SQX/licencia válida, MetaEditor, runtimes Forge/Echo y acceso durable a result surfaces.
- **Required MCP capabilities:** ejecución/observación de todos los runtimes incluidos, control-plane evidence y lectura de result surfaces; nada sintético para el veredicto físico.
- **Physical recipe:** ejecutar la campaña FULL real con matriz determinística, cómputos largos, cancellation/retry/drain sólo donde el delta lo exige, y golden/result surfaces inspeccionables.
- **Durable evidence:** campaign/run IDs, per-stage evidence, finalistas, artifacts, warnings/funnel, result surfaces, cancellation/recovery proof y golden refs.
- **PASS criteria:** factory usable y explicable; zero finalists honesto sigue siendo resultado válido, pero no se declara PRODUCT CAPABILITY sin la evidencia requerida.

#### CERT-F05-03 — Final Factory V2 closure

- **Prerequisite product SHA/release:** CERT-F05-01 y CERT-F05-02 PASS; cross-lane PASS cuando el release incluya Echo join.
- **Prerequisite infrastructure:** todos los runtimes/capabilities requeridos siguen observables durante la campaña.
- **Required MCP capabilities:** conjunto certificado de F04/F05 y read-back de evidencia final.
- **Physical recipe:** ejecutar la matriz final de release, confirmar no-regresiones del delta y emitir el manifest de certificación de Factory V2.
- **Durable evidence:** cert manifest, release/source/runtime mapping, golden refs, unresolved accepted debt y veredictos por gate.
- **PASS criteria:** sólo entonces F-05 puede marcar `PHYSICALLY CERTIFIED`/`CLOSED`; no recertifica B1A/B1B/B2 sin delta.

### Dependencias y clasificación de trabajo restante

| Trabajo | Clase | Decisión |
|---|---|---|
| F-04 T2.11/T2.12/T2.13 | C — HARD BLOCKED | Requiere ejecución física, golden auténtico y/o runtime cross-lane; queda deferred, no waived. |
| F-05 implementación/pre-cert: matriz release, result/read surface y checklist de conformance | A — CAN CONTINUE NOW | Tiene valor real y usa contratos/fixtures existentes sin afirmar certificación. |
| F-05 release/physical/FULL golden/cierre | B — CAN IMPLEMENT BUT CANNOT CERTIFY | La preparación y el tooling avanzan; el veredicto necesita CERT-F05-01…03. |
| E-04 T01–T20 | A — CAN CONTINUE NOW | Ya está integrado; no se reabre. |
| E-04 T21/AC-37 | C — HARD BLOCKED | Exige golden Forge auténtico y join real; synthetic S0/fakeconsumer no satisfacen el gate. |
| E-02 implementation/verification | B — CAN IMPLEMENT BUT CANNOT CERTIFY | No depende de T2.11–T2.13; conserva su PHYSICAL_PARTIAL y gates propios. |
| E-05 implementation/corrections | B — CAN IMPLEMENT BUT CANNOT CERTIFY | No depende de T2.11–T2.13; su cierre actual depende de S0 erratum/control-plane evidence y su propia verificación. |
| E-06 Reference enrollment and binding | B — CAN IMPLEMENT BUT CANNOT CERTIFY | El diseño/implementación puede avanzar; read-back y primera observación requieren runtime físico. |
| E-07 Raw facts, DEAL and coverage | B — CAN IMPLEMENT BUT CANNOT CERTIFY | Puede avanzar con fixtures; offline/restart/partial/late-cost certification requiere observación real. |
| E-08 Routing, EconomicCommand and risk reservation | B — CAN IMPLEMENT BUT CANNOT CERTIFY | Source/shadow puede avanzar; crash/UNKNOWN/reservation certification requiere runtime. |
| E-09 Execution copy and reconciliation | B — CAN IMPLEMENT BUT CANNOT CERTIFY | Puede implementarse; Execution Fidelity PHYSICAL requiere Reference/Execution real. |
| E-10 Strategy Quality and eligibility | A — CAN CONTINUE NOW | Quality/eligibility puede avanzar con fixtures, coverage explícita y abstención; no depende de golden Forge físico. |
| E-11 PortfolioVersion shadow | A — CAN CONTINUE NOW | Selection/allocation shadow determinista puede avanzar con fixtures y CASH; no toca dinero real. |
| E-12 Apply/rebalance/replacement/retirement | B — CAN IMPLEMENT BUT CANNOT CERTIFY | La implementación DEMO puede avanzar; PHYSICAL DEMO requiere runtime real y ACK/recovery. |
| E-13 Front/read/ops and V1 closure | B — CAN IMPLEMENT BUT CANNOT CERTIFY | Read/ops surfaces pueden avanzar; PRODUCT CAPABILITY/restore requiere evidencia física. |

### Delta de readiness por certificación de accesos — 2026-09-15b (GAP-ECHO-004 CLOSED)

Actualiza el delta anterior tras instalar el owner seed en `.71` y recertificar el viewer `echo-runtime-prod` end-to-end. **No cambia ninguna clase A/B/C ni ejecuta gates productivos.**

- **GAP-ECHO-004 → CLOSED:** owner seed instalado (identidad dedicada `echo-dev` uid/gid 1001, sudo DENIED; key `echo-dev.pub` del plane en `authorized_keys`) y viewer `echo-runtime-prod` certificado desde Daedalus real: identity PASS (`echo-dev@echo`, sin sudo), initialize/tools-list PASS, listeners 80/9080/9090/8080/8090, negative `run-command` → POLICY_DENIED MUST DENY, leak CLEAN. Runtime observado: `echo-gateway` (PID 713) y `echo-core` (PID 110701) RUNNING como `kor`, `echo-functions` (StateFun) RUNNING; **Bridge NOT_DEPLOYED** (registrado con evidencia; no se levanta).
- **E-02:** el gate físico Gateway pasa de BLOCKED-pending a **observación SSH directa PASS** (procesos/listeners/identity); sigue sin control verbs (restart = PROD, fuera de scope). `E02_PHYSICAL_CERTIFICATION_BLOCKED` se mantiene por sus gates propios (Hasura DEV roles/hook, Kafka PublishSync/redelivery, Flink restart/recovery), todos con capability certificada disponible para ejecutarse.
- **CERT-F04-01/CERT-F04-02 (F-04 T2.12/T2.11):** el prerrequisito de observación del runtime Echo queda **completo por vía directa** (viewer SSH) además de la observabilidad. Sigue `BLOCKED BY INFRA` por Temporal/equivalente.
- **CERT-E04-01 (E-04 T21/AC-37):** sigue `HARD BLOCKED` (clase C) por golden Forge auténtico + join real; el prerrequisito de observación runtime ya no es gap.
- **Condición de acceso vigente:** todas las capabilities requeridas del Access Plane están operacionales y certificadas (viewer runtime incluido). El trigger de reactivación de este backlog queda **abierto**; la limitación conocida del viewer es de cobertura (sin systemctl/docker/curl productivo, journal propio únicamente) — los logs productivos siguen por `aranea-observability-ro`.
- **Deuda separada no bloqueante:** host key ED25519 de `.71` idéntica a `sqx-zeus` (clon sin regenerar); rotación owner-side opcional con actualización de `trustedHostKey` del perfil en el mismo cambio.

### Delta de readiness por certificación de accesos — 2026-09-15 (gaps stale reconciliados)

Actualiza el delta 2026-09-14 tras el cierre H1/H2, la certificación `aranea-observability-ro` (:3009, PASS 12/12 + consumer PASS) y la resolución del target runtime Echo. **No cambia ninguna clase A/B/C ni ejecuta gates productivos.**

- **Gaps stale eliminados:** Hasura DEV/PROD (`aranea-hasura-dev-admin`/`aranea-hasura-prod-ro`), Kafka DEV (`aranea-kafka-dev-admin`) y Flink DEV (`aranea-flink-dev-admin` + `docker-echo-dev-operator`) están **certificados y operativos** desde 2026-09-12/13 — los GAP-ECHO-001/002/003 de la matriz de 2026-09-14 eran históricamente stale. Observabilidad PROD (GAP-ECHO-007) queda cubierta por `aranea-observability-ro`.
- **E-02:** sus verificaciones físicas pendientes contra Hasura-DEV/Kafka/Flink **ya tienen capability certificada para ejecutarse** (siguen sin ejecutarse: no se corrieron en esta sesión). `etcd`/tokens reales siguen `NOT_OBSERVED` (sin capability). Clase B se mantiene; `E02_PHYSICAL_CERTIFICATION_BLOCKED` ahora depende sólo de ejecutar esas verificaciones y del target Gateway.
- **E-02 Gateway physical:** target real resuelto — `.211` muerto; runtime vivo = PROD `192.168.31.71` (`prod.echo.gateway.lab.aranea`, `/health` 200). Viewer SSH `echo-runtime-prod` staged; verificación SSH pending owner key install. Observación vía `aranea-observability-ro` operativa (logs `service=echo-core` `env=production` en vivo).
- **CERT-F04-01/CERT-F04-02 (F-04 T2.12/T2.11):** el prerrequisito de observación del runtime Echo queda **parcialmente cubierto por observabilidad** (logs/metrics PROD en vivo); la observación directa SSH queda pendiente de la única owner action (instalar `echo-dev.pub` del plane en `.71`). Sigue `BLOCKED BY INFRA` por Temporal/equivalente.
- **CERT-E04-01 (E-04 T21/AC-37):** sigue `HARD BLOCKED` (clase C); el prerrequisito de observación runtime queda parcial (observabilidad sí, SSH viewer pending).
- **CERT-F04-03 / CERT-F05-01…03:** sin cambio; dependen de los gates anteriores.
- **Condición de acceso vigente:** H1/H2 RESOLVED; el trigger de reactivación de este backlog queda **abierto sólo para la certificación SSH viewer sobre `.71`** (post owner action) — el resto de capabilities requeridas ya está operacional.

### Delta de readiness por certificación de accesos — 2026-09-14

Fuente: [[ACCESS-CERTIFICATION]] (run 2026-09-14, veredicto `ACCESS_CERTIFICATION_PARTIAL`). Este delta **no cambia ninguna clase A/B/C ni cierra carriles**; registra qué superficies de acceso quedaron verificadas físicamente y qué gaps siguen bloqueando cada gate.

- **Verificado y disponible para gates físicos:** PostgreSQL PROD-RO y DEV-RW (DML sin DDL en DEV), MongoDB forge RO/RW, Kafka DEV admin (con `delete_topic` eventual — post-condición obligatoria de cleanup), Flink DEV control-plane read, SSH operator sobre SQX/MT5/docker-echo-dev (identidades re-verificadas).
- **E-02:** sus verificaciones físicas pendientes contra `psql`/Kafka/Flink/Hasura-DEV ya tienen capability certificada para ejecutarse; `etcd`/tokens reales siguen `NOT_OBSERVED` (sin capability). Clase B se mantiene.
- **CERT-F04-01/CERT-F04-02 (F-04 T2.12/T2.11):** bases de acceso re-verificadas; siguen `BLOCKED BY INFRA` por la ausencia de observación del runtime Echo y de capability Temporal/equivalente autorizada. Prerrequisito nuevo explícito: capability de observación del host Echo runtime (192.168.31.71:8090, visto en webhooks Hasura).
- **CERT-E04-01 (E-04 T21/AC-37):** sigue `HARD BLOCKED`; el mismo prerrequisito de observación del runtime Echo es el gap dominante. Clase C se mantiene.
- **CERT-F04-03 / CERT-F05-01…03:** sin cambio; dependen de los gates anteriores.
- **E-05…E-13:** sin cambio de clase; para sus futuros gates físicos queda disponible la superficie DEV certificada arriba, y quedan nombrados como `REQUIRED_LATER`: observación runtime Echo, etcd, observabilidad (OBS3), Temporal (T5), Kafka/Flink PROD.
- **Condición de acceso vigente:** el trigger de reactivación de este backlog **sigue cerrado** hasta resolver H1 (credenciales expuestas por `export_metadata`), H2 (boundary viewer SSH no aplicado) y la capability de observación del runtime Echo.

### Próxima tarea única recomendada para NORMAL

**F-05-I — Cohesive release/read-surface preparation.** Repo `xKoRx/symphony`; nueva rama `codex/f05-release-prep`; baseline exacto `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`; autoridad `Echo Forge — Factory V2 Completion` F-05 y contratos F-01…F-04/S0 frozen. Implementar sólo la matriz determinística de release, la preparación de result/read surfaces y la conformance checklist sobre outputs ya existentes; mantener fixtures explícitamente sintéticas, no publicar release productiva desde la rama y no ejecutar T2.11/T2.12/T2.13. Completion: tests/source checks verdes del scope, SHA/release/provenance reproducibles, read surfaces inspectables, cero cambios a contratos frozen y ningún gate físico marcado PASS.

### Trigger de reactivación

Activar este backlog cuando las capabilities requeridas del Aranea MCP Access Plane estén operacionales y certificadas, y los runtimes objetivo sean observables y operables por la policy correspondiente. En ese momento ejecutar estrictamente CERT-F04-01 → CERT-F04-02 → CERT-E04-01 → CERT-F04-03 → CERT-F05-01 → CERT-F05-02 → CERT-F05-03; no usar una fecha calendario ni saltar gates.

## Fuentes

- [[Echo Forge — Factory V2 Completion]] y [[Echo Forge — F-04 Magic allocation, version seal and handoff]]: F-04/F-05 scope, SHA, release, T2.11–T2.13 y evidencia histórica.
- [[Echo — Producto Integrado]] y [[Echo — Live Platform V1]]: DAG E-01…E-13, E-04 T21/AC-37 y reglas de paralelismo.
- [[Echo — E-04 Forge Ingestion E1]]: E-04 INTEGRATED, T21 POST-INTEGRATION, synthetic ≠ cross-lane golden.
- [[AGENT-PLATFORM - MCP Access Plane]] y [[aranea-agent-dev]]: capabilities/policy de acceso Aranea y límite de no inventar autoridad.
- Decisión explícita del owner en esta sesión: desarrollo continúa; certificación física se difiere, no se waiva.
