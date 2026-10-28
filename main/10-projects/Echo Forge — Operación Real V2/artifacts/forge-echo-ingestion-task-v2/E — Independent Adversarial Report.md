---
type: doc
schema_version: 1
status: active
area: '[[Echo]]'
related:
- '[[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|Echo Forge — Operación Real V2]]'
- '[[10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum|Forge Task — Contract Addendum]]'
aliases: []
tags:
- kind/doc
- area/echo
created: '2026-10-28'
updated: '2026-10-28'
---

# E — Independent Adversarial Report

## Propósito

**Estado vigente del programa: SHOT4_READY_WITH_ADJUDICATED_FINDINGS.** El Manager recibió esta revisión con hallazgos y alcance parcial; la adjudicación del 2026-10-28 figura primero en Contenido. El relato y los resultados originales del auditor se conservan debajo como evidencia atribuida, sin elevarlos a PASS global.

QA adversarial independiente (Shot 3) del candidato `forge-echo-ingestion-task-v2`, ejecutada por un verificador LOCAL fresco sin autoría de la implementación. El candidato está admitido con brechas conocidas (`SHOT3_READY_WITH_KNOWN_GAPS`); esta revisión confirma o falsifica los claims del implementador y registra defectos para Shot 4. No corrige producto ni hereda PASS. **Resultado: `FORGE_ECHO_TASK_ADVERSARIAL_REVIEW_COMPLETE`** — la revisión completó el alcance que declara, con 3 findings P1 reproducidos, gates A PARCIAL / B–C NOT_RUN (con smoke PG real) / D BLOCKED con evidencia auténtica parcial / E NOT_AUTHORIZED, y cobertura real por statements bajo el piso Owner.

## Contenido

### Adjudicación vigente del Manager — Shot 4 — 2026-10-28

**SHOT4_READY_WITH_ADJUDICATED_FINDINGS.** Se recibe E como revisión adversarial con hallazgos y alcance parcial, y se avanza directamente a Shot 4: correcciones completas y otro verificador LOCAL fresco dentro del mismo shot. No otra vuelta de Shot 2/3 ni Shot 5. El resultado REVIEW_COMPLETE declarado por el auditor no equivale a ejecución completa de O01–O24/EC-01–EC-08 ni a PASS del producto: su propia matriz mantiene numerosos parciales/NOT_RUN.

Refs remotas comprobadas al recibir: Symphony `7731cb844446062f861f04d19dea60a34d425373`, Echo `24af786232fa362cc1599df1b9d90b1c8347b557`, sin cambios respecto de los candidatos auditados. E recibido desde Agents-OS `124430da4deb8eb95e3121f970ea366adcffd289`, blob `a56a34865f3ccccb8a80a8c28e0c58e01641df7e`. La revisión gerencial corroboró acotadamente causas en la fuente de Symphony con especialistas; no volvió a ejecutar runtime ni convirtió los logs locales narrados en observaciones propias.

**Adjudicación de los nueve findings:**

| IDs | Severidad vigente | Trabajo obligatorio |
|---|---|---|
| QA-S3-05/06/08 | P1 | Catálogo y bootstrap efectivo data_only; Decision ausente como NULL/lineage legítimo; lifecycle completo en Generic y Group. |
| QA-S3-02/07 | P1 de integridad (reclasificados desde P2) | Rechazar identidad canónica ajena y resolver versión compatible por item en resolver/mapper y los tres version_mode. No se afirma corrupción remota ya ocurrida. |
| QA-S3-03 | P2 | Admitir moneda acreditada por el perfil sin declaración externa innecesaria; conservar estados/evidencia. |
| QA-S3-04 | P2 de contrato (reclasificado desde P3) | ExpectedVersionRef, binding digest y key por receta exacta, sellados antes del work-item; el efecto reportado es conflicto fail-closed, no overwrite demostrado. |
| QA-S3-01/09 | P2 de test/evidencia | Corregir test contradictorio sin relajar Validate; fijar perfiles/scope/denominador y alcanzar ≥95% de código nuevo con pruebas útiles. |

**Condiciones materiales del cierre:** el catálogo por sí solo no cierra 05 porque main bifurca a data_only antes del bootstrap durable. Registrar sólo begin_workflow_span no cierra 08: Generic/Group requieren más lifecycle. Corregir el primer helper de versión no cierra 07: mapper/activity y compatibilidad de todos los miembros deben usar autoridad por item. La 018 antigua ya registrada exige upgrade aditivo, sin editar de nuevo una migración aplicada ni borrar ledger/datos; el ledger actual sólo tiene version/applied_at, sin validación de checksum. El baseline 22f337ca contiene 017, no 018.

**Precisiones de evidencia:** 47,1% (2737/5806) y 80,4% (1037/1289) quedan como cifras reportadas, pendientes de reconstrucción de perfiles, pesos por archivo y unión coherente; no recálculo independiente del Manager. El piso aplica al código nuevo de la task, incluidas sus adiciones en archivos existentes, separando el diagnóstico del legado completo. M04 se conserva para los oráculos TradeList ejecutados; M08 para contratos/servicio probados. Lab/E2E siguen pendientes. F debe reconciliar el alcance O23 NOT_RUN/EC-05 servicio PASS mediante test IDs y readbacks concretos.

El stall con cero ActivityTaskStarted prueba falta de progreso observada; no identifica por sí solo ausencia de poller. La omisión de registros queda corroborada por fuente; el cierre exige historia/pending activities/errores, queues/pollers y binario/catálogo. Las lecturas D de ETCD legacy y PG sin tablas V2 describen despliegue, no ausencia de dataset fuente. La reconexión read-only normal ya estaba autorizada; falta completar el intento soportado o acreditar el recurso concreto bloqueado. «Sin operaciones PROD» se limita a sin mutaciones: E sí documenta lecturas RO.

**Gates vigentes:** A INCOMPLETE por defectos y evidencia; B/C NOT_RUN como E2E; D BLOCKED_EXTERNAL con observaciones auténticas parciales reportadas y dataset aún pendiente; E NOT_AUTHORIZED. Mantener todos los pendientes en Shot 4. Preservar/fijar los tests QA, fixtures, perfiles y logs locales antes de corregirlos; un test FINDING verde puede confirmar el bug y debe promoverse con expected contractual corregido.

**NEXT EXACT:** [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]]. Entrega final en F — Final Certification, con candidato integrado, findings/oráculos cerrados, Fresh/Upgrade, Generic/Group reales, Gateway/Lab, goldens y coverage reproducible; después verificación fresca sin autoría. No autocertificación ni PASS forzado por tener cuatro shots. Si persiste un bloqueo, Shot 4 lo reporta con causa/alcance concreto; no genera otro shot automáticamente. B y el addendum siguen congelados. Agents-OS permanece abierto, sin feedback/L0/L1; el PG compartido del incidente queda fuera de pruebas/cleanup/restauración.

### 1. Identidad del auditor independiente y manifest

**Auditor:** GLM-5.3-Flash Max LOCAL/ZCode, sesión fresca 2026-10-28, sin autoría del candidato (las worktrees del implementador no fueron modificadas; QA en worktrees propios `qa-symphony`/`qa-echo` sobre ramas `qa/shot3-adversarial(-echo)`). Bootstrap Agents-OS ejecutado una vez. Autoridad documental leída desde el vault local: B Frozen Design (§14), C Plan, D Evidence, Contract Addendum (§10), SHOT3 Mandate; commit documental indicado por el Manager.

**Manifest exacto (fuente → dependencias → build → runtime):**

| Superficie | Pin verificado | Verificación |
|---|---|---|
| Symphony | `feature/forge-echo-ingestion-task-v2@7731cb844446062f861f04d19dea60a34d425373` | Ref remota `origin` idéntica tras `git fetch`; linaje `22f337ca → 07c9142 → {42ca3d9 → b26be6d → 7731cb8}` sin divergencia (`git merge-base --is-ancestor` OK) |
| Echo | `feature/forge-task-contract-v2@24af786232fa362cc1599df1b9d90b1c8347b557` | Ref remota idéntica; descendiente de `2c66e940` y de la base `f93cd4f8` |
| Contracts tag | `v3/sdk/contracts/v0.0.1-forge-ingestion-task.2` | Objeto tag anotado `7496b05b6932517e1d51b757c42cf72dad2cc1bd` → commit `24af7862…`; subtree `cb88aece4f04b648fd724568de3823604dc064ab` |
| Contracts tag .1 | inmutable | Objeto `d24b17b217245c47a33cea810410da41cf6ad978` sin cambios |
| go.sum .2 | `h1:t60eoyOjwkkgDNxzkPwLvXYLgf/dFW4xwLuazfvx3u8=` | Presente en `sqx/go.sum`; `GOWORK=off go list -m` resuelve `v0.0.1-forge-ingestion-task.2` (descarga efectiva) |
| SDK efectivo | `xKoRx/sdk@c7f11496b6f681687c9e1e41a773a13295640351` | `replace ../../sdk` resuelve al checkout fijado; `go list -m` muestra `v0.0.0-20260921195648-c7f11496b6f6 => ../../sdk` |
| Toolchain | go1.27.1 linux/amd64 | Sin cambios locales |
| Build | `go build ./...` | Symphony rc=0 excluyendo `tools/` y `examples/` (redeclare/no-non-test pre-existentes en `22f337ca`, sin cambios en el delta — atribución verificada); Echo `v3/sdk` rc=0, `v3/gateway` rc=0; `go vet` de paquetes del delta rc=0 |
| Worker runtime | `qa-stack/sqx-worker` (58,9 MB) | Binario construido desde `qa-symphony/sqx/cmd/sqx-worker` |
| Delta no-commit ajeno | `specs/.../phase4_performance.json` modificado en la worktree del implementador | Fixture de benchmark autoregenerado (recorded_at 2026-10-28T01:58Z); no es producto; no se tocó |

Sin modificaciones ocultas de producto: el diff QA está confinado a (i) `sqx/core/forge/qa_shot3_adversarial_test.go`, (ii) `sqx/adapters/registry-postgres/qa_shot3_migration018_test.go` + `testdata/qa_shot3_old_01{7,8}.up.sql`, (iii) `sqx/qatools/qavertical/main.go` (harness de seed), (iv) `qa-echo/v3/sdk/contracts/qa_shot3_adversarial_test.go`. Evidencia voluminosa en `aranea/work/forge-echo-task-v2-20261027/qa-evidence/` y `qa-stack/`.

### 2. Preflight de aislamiento y recursos propios

| Recurso | Ownership QA | Evidencia |
|---|---|---|
| PG | `127.0.0.1:56438` `echo_labv4` (harness2, PID 170022, datadir del programa) | Reutilizada del programa; `sqx.*` bootstrap propio (brownfield+001-018); PG embebidas efímeras de `postgrestest` para suites/migraciones |
| PG incidente | `127.0.0.1:56437` (PID 163088, template compartido) | **EXCLUIDA**: sólo inspección de proceso/puerto; ninguna conexión, escritura, stop ni restauración |
| Temporal real | Dev server aislado `127.0.0.1:7233`, namespace `qa-shot3`, db `qa-temporal/dev.db` (CLI 1.3.0/server 1.27.1) | Levantado por QA; cero conexión a flota |
| ETCD QA | `127.0.0.1:7439` (etcd 3.5.14, datadir propio), claves bajo `/sqx-worker/development/` | Sólo servicio local; cero acceso de escritura a ETCD PROD |
| Mongo QA | `127.0.0.1:27417` (mongod 7.0.14, dbpath propio, base `forge_qa`) | Local |
| S3 QA | Garage 1.0.1 `127.0.0.1:8344` (MinIO community ya no distribuye binarios; S3-compatible sustituto documentado), buckets `sqx-strategies`/`forge-qa` | Sustitución registrada como límite, no como MinIO real |
| SQCLI | Ausente a nivel de máquina (`which sqcli` vacío) | Condición data_only demostrada |
| Flota/PROD | Sin operaciones | Nadie conectado a ETCD/PG/Mongo/MinIO de flota para suplir el harness |

Partes detenidas por riesgo concreto: ninguna. El único hallazgo de ejecución (QA-S3-08) se demostró con un workflow cancelado tras recolectar su historia; sin efectos sobre recursos ajenos.

### 3. Matriz O01–O24, EC-01–EC-08, M01–M09

Estados: PASS / FAIL / PARTIAL (subcasos separados) / NOT_RUN / BLOCKED. Comandos y perfiles: `qa-evidence/` y secciones 5–6.

#### 3.1 Oráculos B§14 (O01–O24)

| ID | Estado | Evidencia / justificación |
|---|---|---|
| O01 | PARTIAL | Resolver exact_evaluations por bindings: unit del candidato rc=0 + lectura (memberships selladas, jamás filename). NO con dataset Full Precision real (sin fuente auténtica completa) |
| O02 | PARTIAL | Rename a `resultados_finales_2027`: suite runtime del candidato (rename O02) rc=0; namespace por BuildMinIOPath leído; sin E2E con tramo productor |
| O03 | PARTIAL | CANONICAL_HISTORY_V2 decodifica con presupuesto (QA06 PASS) pero el contraste de identidad exigido por B§6.3 NO existe (QA-S3-02). Otro productor E2E NOT_RUN |
| O04 | NOT_RUN | Dos labels iguales con refs distintas: requiere carga real de identidad PG + estrategia; no ejecutado |
| O05 | PARTIAL | Dos evaluaciones de una estrategia → 1 item/2 evalRefs (unit del candidato rc=0); múltiples MetricSets sin selector → ambiguo (lectura); runtime NOT_RUN |
| O06 | PARTIAL | REQUIRED sin TradeSet → HISTORY_REQUIRED y IF_AVAILABLE sin TradeSet → histories=[]/NO_HISTORY (unit candidato rc=0 + QAE02 lado Echo); registro visible real NOT_RUN (gate B) |
| O07 | PASS (unit) | TradeSet con conteo discrepante → PAYLOAD_SCOPE_MISMATCH; scope de registro discrepante → rechazo; moneda ausente con trades → CURRENCY_EVIDENCE_MISSING (units del candidato rc=0 + QA04 duplicados + QA05 EMPTY) |
| O08 | PARTIAL | Mongo evaluación ausente → preflight contado; MinIO size mismatch → ARTIFACT_DIGEST_MISMATCH (fetchVerified, leído + smoke); PG↔Mongo extranjero runtime NOT_RUN |
| O09 | PASS (unit) | QA01 independiente: PARTIAL_NET + Commission/Fee/Swap/OtherCosts UNKNOWN, exposure UNKNOWN, sin Q_i/FX fabricados |
| O10 | PARTIAL | Mismo sello idéntico converge en PG real (smoke QA); SaveManifest misma key/digest converge (leído); replay E2E completo NOT_RUN |
| O11 | PARTIAL | BeginAttempt escribe UNKNOWN durable ANTES del POST con contadores reales (smoke PG real QA: 1,2); crash de proceso y GET tras commit NOT_RUN |
| O12 | NOT_RUN | Timeout POST con commit remoto: requiere Gateway real |
| O13 | PARTIAL | 401/403 conservan UNKNOWN y GET-antes-de-POST por lectura del adapter; unidad fake del candidato rc=0; real NOT_RUN |
| O14 | NOT_RUN | Dos workers concurrentes: advisory lock/insert-once leídos; no ejecutado |
| O15 | PARTIAL | Misma key + request_digest distinto → conflicto local sin HTTP (lectura SaveManifest + fake unit candidato); PG real no ejercitado |
| O16 | PARTIAL | Receipt ajeno/altered/ghost/digest malo rechazado por `ValidateNativeIngestionReceiptV2` (QAE03 + units del candidato rc=0); readback real NOT_RUN |
| O17 | PARTIAL | Pin/tag/checksum/descarga efectiva verificados; corpus golden del contrato corre en el consumidor (suite contracts rc=0) y Symphony consume .2 con build frío rc=0; goldens cruzados completos con corpus de ingesta REAL NOT_RUN |
| O18 | **FAIL (P1)** | Worker data_only REAL arranca sin SQCLI con Foundation completa (Temporal/PG/Mongo/S3) y poller en cola propia (PASS). Pero un workflow raíz Generic REAL se cuelga: `begin_workflow_span` queda `ActivityTaskScheduled` en `qa-shot3-ingest` sin poller que la reclame (0 ActivityTaskStarted; historia en `qa-stack/O18_dataonly_stall_history.txt`) — QA-S3-08 |
| O19 | PARTIAL | Suites `activities/worker` y `workflows` FALLAN idénticamente en baseline `22f337ca` (51 fallos MT5/ambientales, diff vacío vs candidato) — sin regresión nueva demostrada; semántica de carriers/selection sin cambios de producto |
| O20 | PASS | QAE04: mismo XML ⇒ mismo DefinitionContentDigest; XML cambiado ⇒ nueva versión; trailing/campo desconocido rechazados; borde exacto 262144 PASS / 262145 DEFINITION_TOO_LARGE; suite sqx-definition del candidato rc=0 (duplicado/corrupto) |
| O21 | PARTIAL | QA03: corrección del mismo run conserva history_id; CREATE_ONLY→REVISION_REQUIRED por validator/protocolo PUT (lectura + suite Echo); runtime real NOT_RUN |
| O22 | NOT_RUN | Lab real (outbox→worker→curvas): depende de B |
| O23 | NOT_RUN | Read model sin historia en PG real del lado Echo (contracts QAE02 PASS; servicio no ejercitado) |
| O24 | PASS | Aislamiento demostrado: todos los targets propios (§2); PG incidente intocado; cero operaciones sobre flota; rechazo de STALL como evidencia sin efectos |

#### 3.2 EC-01–EC-08 (addendum §6)

| ID | Estado | Evidencia |
|---|---|---|
| EC-01 | PASS | QAE01: campo anidado desconocido, trailing y decimales no canónicos (`1.50`, `1e2`) rechazados por `DecodeHistoryInputV2`; decoder puro (cero writes por construcción) |
| EC-02 | PARTIAL | Suite contracts rc=0 (headDigest/unchanged con conteos reales); replay E2E real NOT_RUN |
| EC-03 | PARTIAL | Suite contracts rc=0 (existing_ref conserva temporalidad); E2E real NOT_RUN |
| EC-04 | PARTIAL | Validator de enums/suma por historia en contracts; suite rc=0; E2E real NOT_RUN |
| EC-05 | PASS (nivel Echo) | QAE02 (MISSING→NO_HISTORY; NOT_REQUESTED→HISTORY_NOT_REQUESTED; AVAILABLE+0 inconsistente) + suite `sdk/postgres` completa rc=0 sobre PG QA propia (registro sin historia con persistencia/readback del servicio) |
| EC-06 | PARTIAL | Suite postgres rc=0; casos específicos COMPLETE/PARTIAL/GAP con misma economía no ejercitados explícitamente |
| EC-07 | PARTIAL | `FilterKnownAt` corregido (leído) y suite rc=0; UNKNOWN→epoch0/look-ahead no ejercitados como casos nominales |
| EC-08 | PASS | Pin .2 (tag/objeto/subtree/go.sum/descarga), receipt compartido en contracts con scope nativo, source_evidence tipada, cold builds de ambos consumidores rc=0 |

#### 3.3 Claims M01–M09 del implementador sobre el SHA actual

| ID | Veredicto | Detalle |
|---|---|---|
| M01 | PARCIALMENTE CONFIRMADO | La composición del worker real construye TODAS las dependencias (Resolver/Mapper/Identity/SnapshotSink/TaskReportSink/destino ETCD) — el worker arrancó fail-closed sólo cuando faltó config. PERO el workflow Generic en data_only no puede completar ninguna tarea: `begin_workflow_span` sin poller (QA-S3-08). El claim «Flow durable demostrable en ambas rutas» queda FALSIFICADO para data_only E2E |
| M02 | PARCIAL | Units del resolver rc=0 (2 evals → 1 item, preflight contado, task_output vacío = config error). Snapshot rehidratado por REF y outputsByName verificados por lectura; sin runtime (bloqueado por QA-S3-08) |
| M03 | PARCIAL | OUTPUT/STRATEGY_SQX exacto (0/1/>1) y SEALED_REF por binding del item verificados por lectura + units; hallazgo QA-S3-07 (primer version_ref gana sin conflicto); DEFINITION_REF con artifact real NOT_RUN runtime |
| M04 | **CONFIRMADO** | QA01–QA05 independientes: UNA operación por trade con ID/lado/tiempos/importes EXACTOS (0.001 / −12345.678901234 / 0, sin agregación ni redondeo), exposure UNKNOWN, PARTIAL_NET/UNKNOWN×4, tuple stage/variant/sample/result/cell en history_id, corrección estable, duplicado rechazado, conteos verificados, EMPTY→HISTORY_REQUIRED, NONE sin recorrida. El defecto original del primer candidato está corregido en este SHA |
| M05 | PARCIALMENTE FALSIFICADO | Orden FK Prepare→BindSourceBinding correcto en smoke PG real; PERO (a) el runner no aplica 017/018 (QA-S3-05), (b) SaveManifest sin Decision viola el CHECK (manda '' en vez de NULL) y (c) meta nil en el wiring real fabrica `decision:<key>` sintético prohibido por B§9.3 (QA-S3-06) |
| M06 | PARCIALMENTE CONFIRMADO | Smoke PG real: BeginAttempt UNKNOWN durable, UNKNOWN→INGESTED converge, INGESTED no se pisa (error tardío), BeginAttempt terminal rechazado, contadores reales, bytes canónicos exactos leídos de PG; validator de receipt endurecido (QAE03). Ciclo Temporal de reintentos/backoff con presupuesto: NOT_RUN (workflow colgado por QA-S3-08) |
| M07 | NO VERIFICADO RUNTIME | Finalize→TaskReportSink (write-once Foundation) por lectura; units del candidato rc=0; persistencia real de reporte NOT_RUN |
| M08 | CONFIRMADO (contratos/servicio) | QAE01–QAE04 + suites `contracts` y `sdk/postgres` completas rc=0 sobre PG QA: SourceEvidence validada siempre, wrapper `payload_artifact` congelado, HistoryRefV2 recomputado, SQX dispatch en frontera con borde 262144/262145, snapshots con enums cerrados. Lab runtime (curvas/screener) NOT_RUN |
| M09 | FALSIFICADO EN PARTE | «Suites rc=0» falso: `core/domain` FALLA determinista (QA-S3-01). «68,0% promedio de 85 funciones» no adoptado; coverage real por statements: **delta 47,1%** (2737/5806), **archivos nuevos 80,4%** (1037/1289) — ambos bajo el piso Owner 95%. D tenía razón en el bloqueo ssh/mongo (verificado) pero existían canales RO adicionales operativos (etcd/postgres) que el implementador no usó |

### 4. Gates separados

| Gate | Estado | Alcance real de esta revisión |
|---|---|---|
| A — Functional Contract | **PARCIAL** | Build/vet rc=0; units del candidato + 15 tests QA propios (11 forge + 4 Echo) PASS; smoke PG real del store nativo (máquina de entrega) PASS; migración 018 Fresh/Upgrade real PASS con 3 hallazgos P1; temporal real con worker data_only real. Bloqueos: QA-S3-05/06/08 y cobertura |
| B — Echo Ingestion E2E | **NOT_RUN** (Gateway real) | Sin Gateway real del harness. Contratos y validator verificados por tests; smoke PG real de la máquina nativa; falta request E2E con receipt y readback |
| C — The Lab E2E | **NOT_RUN** | Depende de B; suite `sdk/postgres` rc=0 es evidencia general, no el gate |
| D — Authentic Forge Source | **BLOCKED (evidencia parcial auténtica)** | Canales `aranea-ssh` y `aranea-mongo-forge-ro` expirados (`session not found`; reproducido hoy, no re-inicializables bajo este mandato). Lecturas auténticas logradas por canales soportados: ETCD PROD (`/sqx-worker/certw12/persistence/model` = **legacy**; **no existe** `worker/profile`; sin claves `echo/ingest/v2/*`) y PG PROD (schema `echo` **sin tablas V2** — `strategy_ingestion_receipts` ausente). La evidencia completa (Mongo/MinIO/evaluaciones Forge) sigue sin leerse; nada fabricado |
| E — Release/Deploy | **NOT_AUTHORIZED** | Sin cambios |

Sintético nunca etiquetado auténtico: el smoke usa fixtures etiquetados `qa-*` sobre recursos propios; D separa lectura PROD de fixture.

### 5. Cobertura reproducible, regresión y límites

**Cobertura por statements del scope delta (no promedio de funciones):** perfiles `-coverprofile` por paquete (13 paquetes), fusionados por binario de test y deduplicados por bloque; scope = 19 archivos `.go` no-test del diff `22f337ca..7731cb8`.

- **Scope delta completo: 47,1%** (2737/5806 statements).
- **Sólo archivos NUEVOS (13): 80,4%** (1037/1289).
- Detalle por archivo (nuevos): sink 82,1% · activity 53,9% · http_ingress_v2_native 62,4% · ingestion_v2_native 73,3% · sqx-definition 70,6% · trade-list binding 61,8% · domain 67,6% · forge resolver 62,8% · forge mapper 60,6% · echo_ingestion_task 61,3% · **echo_children 0,0% · echo_ingestion_wiring 0,0% · echo_ingestion_workflow 0,0%** (los tres cero: sin suite propia; wiring quedó ejercitado en runtime real por esta QA, workflows tiene el fallo pre-baseline).
- Modificados pre-existentes en el denominador: `generic_workflow.go` 41,9% (2829 statements — domina el denominador del 47,1%), `config.go` 75,2%, `mt5_task_config.go` 87,9%, `main.go` 1,3%.
- **El piso Owner ≥95% NO se cumple en ninguna lectura.** Los perfiles están en `qa-evidence/cov___*.out`; comando de repro en §6. La contribución QA (15 tests nuevos) no altera la adjudicación: el déficit residual va a Shot 4 sin inflar tests espejo.

**Regresión y atribución:** los 51 fallos de `activities/worker` y `workflows` son IDÉNTICOS en baseline `22f337ca` (diff de nombres de test vacío) — ambientales/MT5, no del delta. El fallo de `core/domain` SÍ es del delta (QA-S3-01). `magic-readback` gate auténtico existe en baseline sin cambios (fixture `SQX_AUTHENTIC_FIXTURE` ausente en esta máquina).

**Límites reales:** sin Gateway Echo real → B/C no ejecutados; sin Mongo/MinIO auténticos → D incompleto; sustitución S3 (Garage) documentada; el workflow data_only no alcanzó el case echo_ingestion_v2 en runtime, por lo que resolver/snapshot/report REAL permanecen NOT_RUN aunque su lógica esté unit-verificada.

### 6. Findings para Shot 4

Formato: ID · severidad · frontera · reproducción mínima · owner · test de cierre.

| ID | Sev | Frontera (archivo/función) | Defecto y repro | Owner | Cierre |
|---|---|---|---|---|---|
| QA-S3-05 | **P1** | `sqx/adapters/registry-postgres/migrations/runner.go` (`ordered`) | `migrations.Apply` sobre base nueva deja `sqx.handoff_manifests_v2` INEXISTENTE: `ordered` lista 001–016; 017/018 (presentes desde baseline/07c9142/7731cb8) jamás se aplican ni quedan en ledger (16 entradas). El worker data_only real de esta QA sólo funcionó porque el harness QA aplicó 017/018 a mano. Repro: `go test -run TestQAShot3Migration018RunnerOmits017And018_FINDING ./adapters/registry-postgres/` | Implementador (Shot 4) | Test existente pasa cuando `ordered` incluya 017/018 y `handoff_manifests_v2` exista tras Apply |
| QA-S3-06 | **P1** | `sqx/adapters/registry-postgres/ingestion_v2_persistence.go` (`SaveManifest`, default de `NewControlPlaneIngestionPersistenceV2`) + `cmd/sqx-worker/echo_ingestion_wiring.go:85,106` | Dos mitades de un mismo defecto B§9.3: (a) meta sin Decision ⇒ INSERT manda `decision_ref=''` y viola `handoff_manifests_v2_decision_ref_check` (debe mandar NULL); (b) wiring real pasa `meta=nil` ⇒ default fabrica `decision:<key>` sintético (prohibido; y las intents nativas quedan bajo un Decision falso). Repro: `go test -run TestQAShot3Migration018FreshChainAndNativePGSmoke ./adapters/registry-postgres/` (log OBSERVADO QA-S3-06a/06b) | Implementador | Smoke con meta sin Decision persiste NULL; con meta nil falla fail-closed en composición (o meta real por item), y no existe fila con `decision:qa-*` |
| QA-S3-08 | **P1** | `sqx/cmd/sqx-worker/echo_ingestion_wiring.go` (`runDataOnlyEchoWorker`) vs `sqx/workflows/generic_workflow.go` (instrumentación/lifecycle) | Worker data_only real registra Generic/Group + 3 activities, pero el workflow raíz programa `begin_workflow_span` (core/lifecycle) en la cola y NADIE la reclama ⇒ el workflow queda colgado indefinidamente antes de llegar a cualquier tarea. Evidencia runtime: workflow `62ae3055-12ab-475f-907c-d9848b210d61` (ns qa-shot3): 1 `ActivityTaskScheduled` (begin_workflow_span), 0 `ActivityTaskStarted`; historia en `qa-stack/O18_dataonly_stall_history.txt` | Implementador | Un workflow raíz echo_ingestion_v2 completo sobre Temporal real en data_only (registrar la superficie lifecycle/instrumentación que los workflows solicitan, o gate que no la programe), con StageExecution COMPLETED y reporte durable |
| QA-S3-02 | P2 | `sqx/core/forge/echo_ingestion_map.go` (`mapCanonicalHistoryV2`) | CANONICAL_HISTORY_V2 no contrasta la identidad del payload canónico con el binding (parámetro `identity` sin uso): un payload con `source_instance_ref`/`run_ref` de OTRO productor se acepta tal cual. Repro: `TestQA07CanonicalForeignIdentityAccepted_FINDING` | Implementador | El mismo fixture debe rechazar PAYLOAD_SCOPE_MISMATCH/identity |
| QA-S3-03 | P2 | `sqx/core/forge/echo_ingestion_map.go` (`MapItem`, gate de moneda) | El gate exige `currency_declaration` también cuando el perfil CANONICAL_HISTORY_V2 trae moneda acreditada en el propio payload (`MoneyV2.CurrencyStatus=OBSERVED`): fuente válida se rechaza `CURRENCY_EVIDENCE_MISSING`. Repro: `TestQA08CanonicalSelfCurrencyStillDemandsDeclaration_FINDING` | Implementador | Ese fixture mapea sin declaration (el gate aplica sólo cuando la fuente no acredita moneda) |
| QA-S3-07 | P2 | `sqx/core/forge/echo_ingestion.go` (`expectedVersionRefForItem`, `bindingOf`) | Dos bindings de la misma estrategia con `version_ref` distinto: el resolver devuelve el PRIMERO sin `VERSION_SOURCE_MISMATCH` (B§4.1 paso 9). Repro: `TestQA11ConflictingVersionBindingsFirstWins_FINDING` | Implementador | El caso debe fallar el item con VERSION_SOURCE_MISMATCH |
| QA-S3-04 | P3 | `sqx/core/forge/echo_ingestion.go` (`bindingOf`, `IdempotencyKeyV1`) | Desviación de receta B§9.2: `ExpectedVersionRef` queda vacío en el binding (dos intents con distinta versión comparten digest/key) y la key usa concatenación propia con 4 componentes en vez de `HashTaggedV2` con los 8 congelados (namespace/writer quedan cubiertos sólo transitivamente vía digest; verificado `TestQA10`). Consecuencia práctica: segunda versión ⇒ mismo key ⇒ conflicto fail-closed, no identidad de intento propia | Implementador | Digests/keys recalculados con la receta congelada; `TestQA09` debe ver keys distintos |
| QA-S3-01 | P2 (evidencia) | `sqx/core/domain/echo_ingestion_test.go` (`TestEchoTaskResultValidateAndSort`) | Test del propio candidato autocontradictorio (ordena a orden canónico y espera rechazo) ⇒ suite `core/domain` FALLA determinista (5/5): el claim D «suites rc=0» es falso en este SHA. El producto (`Validate`) está correcto según diseño | Implementador | Test corregido (asignar items SIN ordenar para el caso negativo); suite rc=0 |
| QA-S3-09 | P2 (cobertura) | Delta completo | Coverage real 47,1% delta / 80,4% nuevos (§5); tres archivos nuevos en 0,0% (children/wiring/workflow) | Implementador | Plan por statements hasta ≥95% de archivos nuevos con denominador publicado |

Ningún finding P0 (ningún riesgo grave acreditado a recursos ajenos).

### 7. Paquete directo para Shot 4

**Correcciones (orden sugerido):** QA-S3-05 → QA-S3-06 → QA-S3-08 (desbloquean boot/E2E), luego QA-S3-02/03/07/04, QA-S3-01, plan de cobertura QA-S3-09; después el verificador final fresco dentro de Shot 4 con B/C Gateway real y Lab.

**Activos QA clasificados:** `qa_shot3_adversarial_test.go` (forge) y `qa_shot3_adversarial_test.go` (contracts) → **PERMANENT_REGRESSION** (promover en Shot 4); `qa_shot3_migration018_test.go` (+fixtures old_017/018) → **PERMANENT_REGRESSION**; `qatools/qavertical` (seed) → **HARNESS_TOOLKIT_CANDIDATE**; stack QA (scripts/boot de etcd/mongo/garage/temporal en `qa-stack/`) → **HARNESS_TOOLKIT_CANDIDATE**; workflow stall `O18_dataonly_stall_history.txt` → **DISPOSABLE_REPRODUCER** de QA-S3-08 hasta corrección. No se creó otro toolkit con nombre distinto.

**Evidencia:** manifest `QA-SHOT3-MANIFEST.txt`; perfiles `qa-evidence/cov___*.out`; historias Temporal y logs `qa-stack/`; SHAs de producto auditados intactos (`7731cb84`/`24af7862`/`c7f11496`; tags .1/.2 inmutables).

## Fuentes

- [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT3 — Independent Adversarial QA Mandate|SHOT3 — Independent Adversarial QA Mandate]], [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/B — Frozen Design|B — Frozen Design]] §14, [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/C — Four Shot Delivery Plan|C — Four Shot Delivery Plan]], [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/D — Implementation Evidence|D — Implementation Evidence]], [[10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum|Forge Task — Contract Addendum]].
- Ejecución QA local 2026-10-28: `aranea/work/forge-echo-task-v2-20261027/` (worktrees `qa-symphony`/`qa-echo`, `qa-stack/`, `qa-temporal/`, `qa-evidence/`, `QA-SHOT3-MANIFEST.txt`).
- Canales read-only PROD: `aranea-etcd-ro` (claves `/sqx-worker/certw12/*`, `/echo/development/*`) y `aranea-postgres-ro` (schema `echo`); `aranea-ssh` y `aranea-mongo-forge-ro` expirados (`session not found`, 2026-10-28).
