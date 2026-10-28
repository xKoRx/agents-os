---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]]"
  - "[[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/E — Independent Adversarial Report|E — Independent Adversarial Report]]"
  - "[[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/B — Frozen Design|B — Frozen Design]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-10-28"
updated: '2026-10-28'
---

# F — Final Certification

## Propósito

Certificación final del programa `forge-echo-ingestion-task-v2` (task `echo_ingestion_v2`). Este documento separa la evidencia del CORRECTOR (Shot 4, fase 1) y deja el launcher de VERIFICACIÓN INDEPENDIENTE (fase 2, verificador fresco sin autoría). **Estado vigente del corrector: SHOT4_BLOCKED (parcial avanzado)** — el corrector declara implementadas las correcciones funcionales con regresiones permanentes; QA-S3-09 continúa abierta y el ciclo E2E real Generic/Group + Gateway está demostrado, pero la evidencia NO está completa para revisión: la cobertura del código nuevo queda en 56,0% (piso Owner ≥95%, QA-S3-09 abierto), el Gate C (Lab E2E) sigue NOT_RUN y el Gate D sigue BLOCKED_EXTERNAL. No hay autocertificación ni FORGE_ECHO_INGESTION_TASK_VERIFIED.

## Contenido

### Adjudicación vigente del retorno y continuación — 2026-10-28

**SHOT4_BLOCKED; continuación de cierre ya autorizada.** El Owner pidió resolver lo posible desde CLOUD y entregar un único prompt LOCAL para lo restante. Se conservan los resultados del corrector como declaraciones pendientes de verificación independiente. El siguiente ejecutor continúa como **corrector**, completa A/B/C, calidad y publicación; después actúa el verificador fresco sin autoría dentro del mismo Shot 4. El launcher histórico de §5 queda supersedido por la sección «Continuación de cierre tras F» de [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]].

**Resuelto por el Manager:** wiring/main nuevos y funcionalidad nueva en archivos existentes pertenecen al piso ≥95%; el legado completo se informa separado. No falta permiso Owner para incluir esa composición. El 56,0% (1808/3227) de §4 está descrito como proporción de bloques: no se adjudica como coverage ponderado por statements. Debe medirse con NumStmt, scope explícito y perfiles/union reproducibles. El verificador recibe un candidato completo; no hereda trabajo pendiente del corrector. Contexto fresco y ausencia de autoría acreditan independencia, sin exigir otra máquina.

**Publicación pendiente comprobada:** en el corte de recepción `xKoRx/symphony` no expuso `refs/heads/shot4/forge-echo-ingestion-task-v2` (404), ni el commit `d760dc3` (422). La feature seguía en `7731cb844446062f861f04d19dea60a34d425373`; Echo en `24af786232fa362cc1599df1b9d90b1c8347b557`. Esto no niega el candidato LOCAL: exige resolver full SHA y publicar refs/manifest desde ese workspace antes del handoff. CLOUD no inspeccionó sus cambios de código ni ejecutó sus pruebas.

**Rectificación material de ejecución:** la bitácora aportada por el Owner sí relata arranque temporal del Gateway contra Kafka DEV compartido y detección de su consumer de automation, seguido de stop y broker local. La configuración final puede ser propia; la afirmación original «jamás al cluster compartido» era incorrecta. Contacto/consumer reportados; consumo, commits, automatizaciones y duración/impacto todavía no acreditados. Conservar logs y una comprobación RO acotada si hay acceso; sin resets/replays/reparación de recursos compartidos. Concurrencia residual PG/Mongo/Garage exige aislar todos los targets de escritura antes del resto del E2E, incluidos artifacts filesystem y outbox Lab.

**Dos cierres adicionales de evidencia dentro de los findings existentes:** el panic con métricas deshabilitadas fue sorteado habilitándolas; falta demostrar reparación o comportamiento soportado sin métricas/tracer. QA-S3-02 describe contraste de instancia, pero falta demostrar rechazo de run/evaluación/scope ajenos de esa misma instancia conforme a la autoridad del productor. No se adjudican como nuevos defectos inspeccionados en d760dc3: se exige comprobar los expected ya congelados y corregir lo reproducido.

**D separado:** las lecturas legacy/no-V2 describen despliegue y no prueban ausencia de dataset. Reconexión RO normal y error de recurso/operación fuente son la base de BLOCKED_EXTERNAL; no desplegar PROD para obtener D. El programa conserva B/addendum, cuatro shots y release NOT_AUTHORIZED. El alcance ejecutable completo y la secuencia de cierre están en [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]]; no otro Shot 2/3/5 ni cierre Agents-OS.

### 1. Identidad del corrector y candidato

**Corrector:** GLM-5.3-Flash Max LOCAL/ZCode, sesión 2026-10-28, rol TOP LOCAL por el mandato Shot 4. Bootstrap Agents-OS ejecutado una vez. Autoridad documental leída desde el commit `756a343281af4c305c0808325e80085c837d9e6f` (xKoRx/agents-os), preservando cambios ajenos.

**Candidato integrado por repositorio (descendiente de los SHAs de entrada, sin reset/rebase destructivo):**

| Superficie | Rama | SHAs del candidato Shot 4 | Base de entrada |
|---|---|---|---|
| Symphony | `shot4/forge-echo-ingestion-task-v2` (local, worktree `shot4-symphony`) | `2eedc4f` (correcciones QA-S3-01..08) → `3ce32a2` (cierre runtime E2E) → `d760dc3` (gitignore) | `7731cb84` (candidato Shot 3) |
| Echo | sin cambios (`feature/forge-task-contract-v2` @ `24af7862`) | contracts `.2` inmutable (`7496b05b` → `24af7862`) | `24af7862` |
| Contracts | `v3/sdk/contracts/v0.0.1-forge-ingestion-task.2` | sin nueva versión (no hubo cambio de contrato) | igual |
| SDK efectivo | `c7f11496` (`replace ../../sdk` verificado) | sin cambios | igual |

Worktrees del programa en `~/aranea/work/forge-echo-task-v2-20261027/`. Evidencia Shot 3 preservada ANTES de corregir: commits `d70c171a` (qa-symphony, rama `qa/shot3-adversarial`) y `8270676b` (qa-echo, rama `qa/shot3-adversarial-echo`), manifest `QA-SHOT4-PRESERVATION-MANIFEST.txt` (hashes SHA256 de tests, fixtures old 017/018, perfiles cov___*.out, logs del stack, binario del worker QA). El fixture ajeno `specs/.../phase4_performance.json` (autoregen del implementador) quedó intocado.

### 2. Correcciones adjudicadas por QA-S3-ID (parte corrector)

| ID | Corrección implementada | Regresión permanente | Estado |
|---|---|---|---|
| QA-S3-05 | `migrations.ordered` incluye 017/018/019; nueva `019_ingestion_v2_delivery_state_reconcile.up.sql` (reconciliación ADITIVA del delta B§9.3 para bases con la 018 previa registrada, con guardia explícita de shape, sin reset ni re-edición); data_only pasa por `wireDurablePersistence` (migraciones+Foundation) ANTES de publicar el worker | `TestShot4FreshChainIncludesV2Store`, `TestShot4UpgradeFromLegacy018Reconciles`, `TestShot4ConcurrentBootAppliesOnce` (Fresh/upgrade-legacy/repetición/concurrencia) | CERRADA (tests + runtime: el worker corregido aplicó 019 por el camino normal sobre la base reconciliada del harness) |
| QA-S3-06 | `SaveManifest` persiste `decision_ref NULL` (`NULLIF`); default meta nil ya no fabrica `decision:<key>` (clasificación honesta); el lineage real por item lo sella `SaveNativeManifest` | `TestShot4ManifestWithoutDecisionPersistsNULL` (NULL + sin sintético + máquina nativa completa) | CERRADA |
| QA-S3-08 | data_only registra `begin_workflow_span`/`begin_group_span`/`flow_run_start`/`flow_run_seal` y marca accepting tras publicar; sink con StageExecution técnico REAL (`ResolveStageExecution` + CAS `CompleteStageExecution` con `row_version` leído — refinement B§7.2 `LoadStageCompletionState` implementado en PG); requests echo implementan `TelemetryCarrier`; nil-guard del SpanID en el workflow | Suite runtime real (ver §3) + tests worker | CERRADA EN RUNTIME REAL (Generic y Group) |
| QA-S3-07 | Versión por item: join por `EvaluationRef` con conflicto `VERSION_SOURCE_MISMATCH` en resolver; SEALED_REF usa `item.ExpectedVersionRef` (jamás primer global); SQX_DEFINITION exige acuerdo de TODOS los miembros (mismo XML compatible; XML que deriva otra versión rechaza) | `TestShot4ConflictingVersionBindingsRejected`, `TestShot4VersionJoinIsByEvaluationMembership`, `TestShot4SQXDefinitionMembersMustAgree` | CERRADA |
| QA-S3-04 | Key = `HashTaggedV2("forge-echo-delivery.v1", 7 argumentos congelados)` con golden independiente; binding incluye `ExpectedVersionRef`; modos derivados congelan la versión definitiva ANTES de los work-item refs (`ItemVersionDeriver`/`MapperVersionDeriver` en wiring+activity; builders aplican el temporal metadata para que deriver y mapper computen LA MISMA versión); MapItem verifica la versión congelada | `TestShot4IdempotencyKeyGoldenB92`, `TestShot4BindingDigestDistinguishesExpectedVersion`, `TestShot4DerivedModeFreezesVersionBeforeWorkItems`, `TestShot4MapItemVerifiesFrozenVersion` | CERRADA (y demostrada en runtime: key `sha256:4cf04572…` congelada con la versión `f39b122a…` antes del batch) |
| QA-S3-02 | CANONICAL_HISTORY_V2 contrasta `source_instance_ref` del payload con la identidad sellada; identidad ajena/vacía ⇒ `PAYLOAD_SCOPE_MISMATCH` antes de Prepare/POST | `TestShot4CanonicalForeignIdentityRejected`, `TestShot4CanonicalMissingIdentityRejected`, `TestShot4CanonicalOwnIdentityAcceptedPreservesData` | CERRADA |
| QA-S3-03 | Gate de moneda sólo cuando la fuente NO acredita moneda (OBSERVED/DECLARED por operación con evidence_ref); declaración contradictoria se rechaza; OBSERVED preservado (jamás elevado) | `TestShot4CanonicalSelfCurrencyNeedsNoDeclaration`, `TestShot4CanonicalContradictoryDeclarationRejected`, `TestShot4TradeListDeclarationStillRequiredWithoutSourceCurrency` | CERRADA |
| QA-S3-01 | Test `core/domain` corregido (positivo canónico y negativo separados; `Validate` intacto) | `TestEchoTaskResultValidateAndSort` (suite rc=0) | CERRADA |
| QA-S3-09 | Perfiles por paquete + unión por bloques (máximo por bloque, sin duplicar denominador); scope congelado = archivos .go no-test del delta `22f337ca..d760dc3`; perfiles y script publicados en `qa-evidence-shot4/` | — | **ABIERTA: 1808/3227 = 56,0% < 95%** (reproducible: `covunion.py cov_*.out`) |

Hallazgos nuevos corregidos durante el cierre (pertenecen al Shot 4): TelemetryCarrier ausente en los request types echo (el interceptor del SDK los rechazaba — oculto por el stall del Shot 3); `generic_workflow.go:187` deref de SpanID nil (crash del workflow en data_only sin tracer); el sink fabricaba StageExecutionRef no-UUID y EvaluationRef fuera de la receta canónica (ahora stage técnico real + `domain.NewEvaluationRef`); desalineación deriver/mapper en la versión congelada (temporal metadata aplicado dentro de los builders); mapper sin coverage/provenance/bloques `[]` (typed null jamás en el wire).

### 3. Runtime E2E real (Gate A/B ejecutados por el corrector)

**Recursos propios del programa** (`~/aranea/work/forge-echo-task-v2-20261027/qa-stack/`): PG embebida `127.0.0.1:56438/echo_labv4` (ledger sqx reconciliado 001–019), Mongo `27417/forge_qa`, Garage S3 `8344`, ETCD **aislado** `127.0.0.1:7441` (datadir propio; el ETCD 7439 del Shot 3 quedó excluido al detectar una sesión concurrente sobrescribiendo claves — ver §4.4), Kafka local desechable KRaft `19092`, Temporal dev server `7233` namespace `qa-shot4` (cola `qa-shot4-ingest`), Gateway REAL del candidato Echo `24af7862` en `127.0.0.1:8124` (PG 56438 + artifact store filesystem + identidades `producer_ingest` namespace `forge` writer `7f3c9a2e…`; la configuración final de Kafka del gateway apunta al broker local; hubo contacto previo con Kafka DEV compartido según la bitácora y la rectificación gerencial anterior). SQCLI ausente. Cero operaciones sobre flota/PROD/PG del incidente.

**Evidencia del ciclo (workflow `sqx-main-v1-e4444444-…46c`, RunId `01a1837a`):** flow_run_start → begin_workflow_span → resolve (snapshot sellado + StageExecution técnico COMPLETED + work items con key/versión congeladas) → batch (map → Prepare write-once → BindSourceBinding → POST al Gateway real → receipt `ValidateNativeIngestionReceiptV2` OK → INGESTED) → finalize (TaskResult PERSISTED con ACK) → flow_run_seal → **WORKFLOW COMPLETED**. Item: outcome DELIVERED, receipt `8c366796-3e99-…`, 1 history ref con **2 operaciones** (conteo exacto del fixture). PG: `flow_run COMPLETED`, stages técnicos COMPLETED (source+finalize), delivery `INGESTED` con `post_attempts=1`. **Readback**: `GET /api/v2/strategy-ingestions/by-key/<key>` → HTTP 200 con el MISMO receipt (acceptance, namespace/writer/key, versión `f39b122a…`, 2 operaciones, `source_evidence` presente). **Group hijo real** (`sqx-main-v1-group-…470`): begin_group_span → resolve → batch → finalize → COMPLETED, y un REPLAY posterior de la misma intención **convergió al receipt durable INGESTED sin re-POST** (B§9.4/O10). Recovery por `RecoverIngestion` (PG primero, GET antes de POST) cubierto por suite `echo-handoff` rc=0 y convergencia del replay.

**Gates tras la corrección (declaración del corrector, pendiente del verificador):** A funcional — PASS en las superficies probadas (build/vet rc=0; suites forge/domain/runtime/sqx-definition/echo-handoff rc=0; registry-postgres con los fallos MT5/ambientales idénticos al candidato — diff de nombres vacío). B ingestion E2E — PASS con Gateway real del harness (receipt + readback arriba). C Lab E2E — **NOT_RUN**. D fuente auténtica — **BLOCKED_EXTERNAL** (§4.3). E release — NOT_AUTHORIZED (sin cambios).

### 4. Bloqueos declarados (SHOT4_BLOCKED — causa, alcance, acción)

1. **QA-S3-09 cobertura bajo el piso.** Causa: los tests existentes + regresiones cubren 1808/3227 bloques (56,0%) del scope congelado; los archivos `echo_ingestion_workflow.go` (42 bloques, 0%) y `echo_children.go` (63, 0%) no tienen suite propia y `wiring`/`main` son composición de boot sin tests. Alcance: el piso Owner ≥95% NO se alcanza en ninguna lectura. Acción pendiente concreta: (a) suite Temporal de test para `runEchoIngestionTask` (resolve→batch→finalize con fakes Foundation); (b) tests de `echo_children.go` contra Mongo QA con colecciones sembradas (bounded list, límite+1, filtro por selector); (c) extender los tests del mapper ya escritos (DEFINITION_REF/CANONICAL) hasta el piso; (d) incluir el código nuevo de wiring/main y las adiciones nativas a archivos existentes en el scope ≥95% por statements, separando el legado ajeno; alcance ya adjudicado por el Manager, sin decisión Owner pendiente.
2. **Gate C (Lab E2E) NOT_RUN.** Causa: dependía de B (cerrado en esta sesión) y del ciclo Lab completo (outbox → worker Lab → curvas/screener). Acción: con el receipt `8c366796…` y la historia `sha256:e5472cf5…` ya en la base del gateway, ejecutar el dirty outbox/worker Lab del candidato Echo y verificar curvas/métricas/screener con estados honestos (2 operaciones, PARTIAL_NET, exposure UNKNOWN).
3. **Gate D BLOCKED_EXTERNAL (re-verificado 2026-10-28 por el corrector).** ETCD PROD `/sqx-worker/certw12/` sigue legacy (sólo `persistence/model`; sin `worker/profile`, sin `echo/ingest/v2/*`) y PG PROD schema `echo` sigue SIN tablas V2 del store nativo (sólo `trade_journal_v2_legacy_backup`) — lecturas read-only por `aranea-etcd-ro`/`aranea-postgres-ro`. `aranea-ssh` y `aranea-mongo-forge-ro` siguen expirados. Falta el dataset Forge auténtico (evaluaciones/lineage Mongo + artifacts del Owner) para acreditar D; A/B continúan con fixtures identificados.
4. **Concurrencia de sesión detectada.** Durante la ejecución E2E otra sesión trabajaba los mismos recursos del programa (sobrescribió claves del ETCD 7439: `base_url`→`:8095`, `task_queue`→`echo-dataonly-qa`; procesos `echo-gateway-harness`/`sqx-worker` propios). Mitigación aplicada: ETCD aislado 7441 con datadir propio y config re-sembrada; fixtures con refs propias (`qa4-*`, flows `c444…6b/6d/6f`); PG/Mongo/Garage compartidos del programa con refs no colisionables. Riesgo residual documentado: esos recursos siguen compartidos con esa sesión.

### 5. Verificación independiente — launcher histórico supersedido por la continuación de cierre

**El corrector NO despachó el verificador final fresco** (no dispone de un subagente con entorno propio garantizado en esta superficie) y NO declara esa verificación ejecutada. Launcher exacto para la fase 2 del mismo Shot 4:

- **Entrada:** Agents-OS master, commit documental de handoff = el de publicación de esta F; mandato `SHOT4 — Correction and Final Verification Mandate` §8; candidato Symphony local `shot4/forge-echo-ingestion-task-v2 @ d760dc3` (worktree `~/aranea/work/forge-echo-task-v2-20261027/shot4-symphony`), Echo `24af7862` intacto, SDK `c7f11496`, contracts `.2` inmutable.
- **Pasos obligatorios:** (1) reconstruir sin heredar checkout/PID (build frío `GOWORK=off`, hash del binario); (2) repetir los nueve criterios de cierre con expected propio (los tests `TestShot4*` son del corrector: el verificador escribe los suyos); (3) repetir el ciclo E2E con el seed `sqx/qatools/qavertical4` (XML distinto para keys nuevas), stack propio (ETCD/Mongo/Garage/Kafka/Temporal propios o los puertos libres siguientes), Gateway real `24af7862`, readback GET-by-key y PG state; (4) ejecutar el Gate C pendiente y el plan de cobertura del §4.1 hasta el piso; (5) re-verificar Gate D con los canales RO vigentes; (6) agregar a esta F la sección «Verificación independiente» con evidencia atribuible, conservando separadas las afirmaciones del corrector.
- **Salida esperada:** READY_FOR_MANAGER_REVIEW o SHOT4_BLOCKED con causa/alcance/acción, según evidencia. La adjudicación `FORGE_ECHO_INGESTION_TASK_VERIFIED` corresponde al Manager, no al corrector ni al verificador.

### 6. Límites y precisión de esta certificación

Las lecturas PROD de Gate D son read-only por canales soportados y describen el despliegue observado, no la ausencia del dataset fuente. La sustitución S3 (Garage) y el Kafka local desechable están documentados como sustitutos del harness. «Sin operaciones sobre PROD» se limita a sin mutaciones. El verificador no hereda este relato como certificación: reconstruye y verifica por su cuenta. Agents-OS permanece abierto, sin feedback/L0/L1; el segmento de código queda registrado en el agent-run del 2026-10-28.

## Fuentes

- [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]], [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/E — Independent Adversarial Report|E — Independent Adversarial Report]], [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/B — Frozen Design|B — Frozen Design]], [[10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum|Forge Task — Contract Addendum]].
- Evidencia ejecutable: `~/aranea/work/forge-echo-task-v2-20261027/` (`QA-SHOT4-PRESERVATION-MANIFEST.txt`, `qa-evidence-shot4/COVERAGE-SHOT4.txt` + perfiles + `covunion.py`, logs `worker-shot4.log`/`gateway-shot4.log`, job JSONs `job-shot4-generic*.json`/`job-shot4-group*.json`).
- Candidatos: Symphony rama `shot4/forge-echo-ingestion-task-v2` (`2eedc4f`, `3ce32a2`, `d760dc3`), Echo `feature/forge-task-contract-v2 @ 24af7862`, contracts `.2` (`7496b05b`), SDK `c7f11496`.
