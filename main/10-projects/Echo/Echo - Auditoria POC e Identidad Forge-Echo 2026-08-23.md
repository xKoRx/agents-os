---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo - Cierre del Lab y Limpieza del Journal]]"
  - "[[Echo Forge]]"
  - "[[Echo - Reporte de Estado Lab y Journal 2026-08-21]]"
  - "[[echo-forge]]"
aliases:
  - auditoria poc echo forge
  - echo forge identity audit
tags:
  - kind/doc
  - area/echo
  - project/echo
  - change/report
created: "2026-08-23"
updated: "2026-08-24"
cssclasses:
  - wide
---

# Echo - Auditoria POC e Identidad Forge-Echo 2026-08-23

## Propósito

- Auditoría adversarial de "equivalentes conceptuales al `magic_number=888111`" (atajos de POC tratados como contrato) en `xKoRx/echo` y `xKoRx/symphony`, con foco en identidad de estrategia, MagicNumber y el Golden Path Forge→Echo.
- Método: 5 frentes paralelos read-only + verificación directa del agente principal. Estado 2026-08-23; clone local de echo STALE (`309d4707`; origin/master = `e25165ba` confirmado; 3 archivos sucios locales aparentan duplicar contenido pusheado).
- **2026-08-24 — Pasada de alineamiento owner**: decisiones de dominio incorporadas (identidad canónica única Forge==Echo==journal, HOST_KEY solo creación, overwrite-in-scope como feature, MT5-first 64-bit, MagicNumber semántico + registry, versión≠identidad, GenericSQXWorkflow como flow activo, lifecycle DEMO permanente 3-6 meses antes de portfolio). Sección [[#ALINEAMIENTO OWNER Y TRIAGE 2026-08-24]] reclasifica los 116 registros originales sin borrar evidencia (estados: OWNER_CLARIFIED / NOT_A_DEFECT / DEPRECATED / LEGACY_BUT_LIVE / RECLASSIFIED / CONFIRMED / RESOLVED_UPSTREAM / SCHEDULED).

## Contenido

### A. Veredicto ejecutivo (v2, post-alineamiento)

- La cadena de identidad queda definida: existe UN `strategy_id` canónico e inmutable (= identidad de estrategia, nacida en Forge, aceptada por Echo en la ingesta); el MagicNumber es su identificador runtime MT5, ÚNICO, SEMÁNTICO, ESTABLE entre versiones y cuentas, con registry durable. La atribución física en cuentas demo fluye por el magic input del EA de estrategia observado por el reference EA (collector de toda la cuenta — comportamiento correcto bajo el modelo multi-estrategia).
- Tras filtrar arqueología: de 116 líneas crudas (112 hallazgos sustantivos + 4 INFO alineados) quedan **34 defectos reales de active path**, **5 grupos bloqueantes del Golden Path** (magic compartido, plumbing 64-bit, identidad canónica en journal, endpoint de ingesta inexistente en Generic + auth, pre-provision de catálogo) y 32 deudas de escala/diseño. Lo deprecated/stale/intencional/resuelto suma 33 y no entra al roadmap.
- El roadmap final: R0 → M0A Gate GO ∥ M0B ∥ S1 → **F0 Strategy Identity & MT5 Runtime Identity** → F1 Contract Closure → F2 DEMO Golden Path (Reference-only) → **ACUMULACIÓN 3–6+ meses** (serie temporal viva; segments DEMO→PRE_LIVE→LIVE cobra rol real) → A1 Execution Fidelity ∥ A3 Degradation Funnel → Portfolio Construction / Account Impact → Oracle.
- Corrección honesta post-owner: los CRITICAL F-06/F-07 eran features de storage deliberadas (overwrite solo dentro del mismo scope wave/config; el histórico relevante vive en otros scopes); el defecto residual es la disciplina de unicidad de `wave_key` (F-18/F-30) y el dedup-by-size (F-08). F-01 HOST_KEY afecta solo la creación inicial; la identidad se congela al nacer.

### B. Ground truth MT5/MagicNumber (verificado)

- MQL5 `request.magic` ulong/long 64-bit; POSITION_MAGIC/DEAL_MAGIC devuelven long; MQL4 int32. [EXTERNAL]
- Plumbing actual y dónde rompe el 64-bit: `echo.accounts.client_native_magic` YA es `int8` (001:822 ✓); `account_strategy_risk_policy.magic_number_override` es **int4** (001:1126 ✗); `EchoPersistence.mqh TradeMapRecord.magic_number` es **int** (mt5:17 ✗); casts `(int)` en mt5 reference (`reference_v3.mq5:166`) ✗. Cadena intermedia Go (ReferenceEvent/Kafka/domain) ya usa int64 ✓. Fix 64-bit = 3 puntos (struct MQL, columna policy, casts).
- EAs de Echo sin inputs de identidad (solo debug flags); identidad por pipe client_config (`native_magic` int64, `reference_strategy_id`) y por comando. Defaults triple-implementados (últimos 6 dígitos account_id).
- Reference EA = collector: loop `PositionsTotal()` sin filtro (dedup por ticket) — CORRECTO bajo modelo multi-estrategia por magic; el punto crítico es el mapping magic→strategy_id inequívoco, no filtrar.
- RobustRun inyecta `MagicNumber` como Variable makeExternal (default 888111, uno por wave, UUID fijo) ⇒ input del EA exportado generado por SQX; Symphony no genera OrderSend. El magic live de estrategias Forge autónomas = ese input.
- Magic sobrevive reinicios (metadata server-side); netting agrega posiciones por símbolo (cuenta demo hedging recomendada). [EXTERNAL]

### ALINEAMIENTO OWNER Y TRIAGE 2026-08-24

Decisiones aplicadas: (1) strategy_id canónico único e inmutable Forge==Echo==journal==Lab; magic≠identidad. (2) HOST_KEY participa solo en creación; identidad se congela. (3) Overwrite intra-scope es reemplazo explícito, no corrupción. (4) MT5-first sin techo int32. (5) MagicNumber semántico + registry UNIQUE (no excluyentes). (6) Strategy 1—N Versions; magic pertenece a la Strategy. (7) GenericSQXWorkflow = flow activo; Adaptive deprecated. (8) Lifecycle: finalista → Echo → DEMO permanente (nunca deja de correr) → 3–6 meses → elegible portfolio. (10) Collector-model valida el escaneo total. (11) NATIVE track separado del Golden Path.

Funnel: **116 crudas → 112 sustantivos → 78 activas tras filtro → 34 defectos reales active-path → 5 grupos bloqueantes GP** · scale-debt 32 · deprecated/stale/intencional/resuelto 33 · drift documental programado 6.

| IDs | Estado final | Justificación |
|---|---|---|
| F-01 | OWNER_CLARIFIED | HOST_KEY solo crea el id; filas adoptadas no mutan (adopt ON CONFLICT DO NOTHING verificado). Residual LOW: fork cross-host permitido por diseño |
| F-02 | CONFIRMED low | Recorte heurístico puede mutilar sufijo legítimo EN CREACIÓN; edge case menor |
| F-05 | NOT_A_DEFECT | Convergencia por request_id es idempotencia deliberada |
| F-06, F-07 | NOT_A_DEFECT (condicional) | Overwrite intra-scope = reemplazo explícito; condición: unicidad de wave_key por flow (ver F-18/F-30) |
| F-27 | UNKNOWN | Adapter uploader-minio posiblemente sin uso; verificar antes de actuar |
| F-11, F-12, F-13, F-16, F-17 | LEGACY_BUT_LIVE | Branches legacy junto al path durable; limpieza, no blocker. Verificar wiring de `apply_selected_run` durante F0 |
| F-19, F-28 | DEPRECATED | strategy_evaluations legacy Mongo / path adaptivo |
| F-21, F-37 | CONTRACT_GAP→F1 | mt5_deployments vacío y ausencia de publish no son defectos: son el feature pendiente NI-DL-1/NI-MP |
| F-26 | STALE | Tool ops |
| F-03 | CONFIRMED CRITICAL (active) | cfgID sprintf está EN GenericSQXWorkflow (`generic_workflow.go:33`) y watcher (`steps.go:276,325`): editar spec reusa config_id y muta config silenciosamente |
| F-04, F-08, F-09, F-10, F-15, F-18, F-24, F-30, F-36 | CONFIRMED (active) | SaveConfig sin digest · dedup-by-size · defaults silenciosos de stamping · magic compartido (GP) · colisión filename sanitizado · wave_key reuse · fechas deviation hardcodeadas · markers concurrentes · secrets commiteados |
| F-02,14,20,22,23,25,29,31,32,33,34,35,38 | SCALE_DEBT/DESIGN | Sin impacto GP; crecen con volumen |
| E-16, E-19 | RESOLVED_UPSTREAM | Fix broker fallback/provisioning ya en origin/master (c8aa59a4/e25165ba); verificar en R0 |
| E-01, E-05, E-17, E-20 | CONFIRMED (active) | magic_default garbage · bucket NATIVE colapsa manuales (decisión #11: bucket explícito excluido de Quality canónica) · autoprovision placeholders (mitigado por pre-provision en ingesta) · dual SoT de defaults (consolidar en F0) |
| E-07 | CONFIRMEDED HIGH — priorizado | Age-out 7 días pierde cierres: CRÍTICO para DEMO permanente (#8): series vivas de meses exigen cierres tardíos reportados |
| E-10 | CONFIRMED HIGH — pre-A | Sin aliases GOLD↔XAUUSD rompe joins cross-broker del funnel |
| E-03, E-04, E-06, E-12, E-14, E-15 | CONFIRMED — lote N-track | Skew binarios, truncamiento native-id, huérfanos de cierre, retry intent, calidad payload |
| E-02,08,09,11,13,18,21,22 | DESIGN/LOW | Incluye sellado COALESCE → clarificar en test C1 |
| P-05, P-16, P-17 | DEPRECATED | Jobs RFC-003 y path v0 |
| P-01 | CONFIRMED — mitigado en F2 | Pre-provision de strategy_definitions real en la ingesta convierte autoprovision en no-op |
| P-23, P-26 | CONTRACT_GAP→F1 | BuildIngestKey espera consumidor (la ingesta lo consume); TradeList sin orderId/magic/volumen/SL → anexo NI-EI-2 |
| P-06, P-07 | SCHEDULED M0A | Rollout compilado sin 042 · metadata Hasura sin ~20 objetos |
| P-12 | CONFIRMED HIGH — quick fix M0B | Delete UI de estrategia hace CASCADE de policies |
| P-04, P-08, P-09, P-10, P-11, P-18, P-24, P-25 | CONFIRMED — milestones | Lab upsert scope · HWM derivado · triple-default magic · kache tombstones · FK curvas/outcomes · race adopción · version dead-end (resuelve F0 versioning) · generation manual |
| P-02, P-03, P-13, P-14, P-15, P-19, P-20, P-21, P-22, P-27, P-28 | SCALE_DEBT/HARDENING | safeSegment · dedupe import por-batch · FK contradictorias · matviews stale · policy-history para recomputo histórico (relevant pre-portfolio) · refs sin reuso by-design · acople PK/unique · Mongo sin unique · metadata mutable · PutObject sin lock · CASCADE latente evidence |
| D-01 | REFRAME→F1 | El puerto EchoIngestor nunca existió en ningún path: es EL entregable F1, insertado en GenericSQXWorkflow tras `verify_robust_run_selected` (insertion point verificado: casos select_robust_run→apply_selected_run→mt5_exporter, sin echo_*) |
| D-02, D-03, D-04, D-05 | DEPRECATED | Promises/activities del Adaptive deprecado; no participan del diseño |
| D-06..D-10, D-13, D-20 | STALE_DOC | Catálogo SPECS y umbrales desactualizados |
| D-11, D-12, D-15, D-16, D-19, D-21 | SCHEDULED — ratificación C3/M0A | RFC-010 vs migraciones 045/056/060 · semántica conflict/ticket · thresholds gate 95 vs 99 · policy coverage (decisión owner pendiente) |
| D-17 | FEATURE_SCHEDULED | IMPORT path futuro (fuera V1) |
| D-22 | FEATURE_SCHEDULED — pre-portfolio | Writer de segments ahora RELEVANTE por lifecycle DEMO→PRE_LIVE→LIVE (#8); no bloquea F2 |
| D-25..D-28 | TERMINOLOGY→F1 | Un vocabulario de identidad sale del contrato F1 |

### C. Registro original 2026-08-23 (HISTORICAL — trazabilidad, estados vigentes en la tabla de triage)

#### C.1 Flujo Forge (F-xx)

```
F-01 | identity-core | sqx/core/domain/canonical_strategy_id.go:131-148 | canonical id depende de $HOST_KEY al crear: mismo archivo produce canonical distinto según host | CONFIRMED-DEFECT | HIGH → OWNER_CLARIFIED (creación-only)
F-02 | identity-core | canonical_strategy_id.go:136-147 | isLikelyHostKey mutila filenames legítimos con sufijo punteado cuando HOST_KEY seteado | POC-SHORTCUT | MEDIUM → CONFIRMED low (creación)
F-03 | config-identity | watcher/steps.go:325 + generic_workflow.go:33 | config_id sprintf sin contenido: edición de spec reusa config_id y muta config silenciosamente | CONFIRMED-DEFECT | CRITICAL (active)
F-04 | config-identity | postgres_registry.go:52-70 | SaveConfig ON CONFLICT DO UPDATE sin digest guard ni auditoría | CONFIRMED-DEFECT | HIGH (active)
F-05 | flow-identity | flow_run.go:112-135 + intake.go:47-59 | mismo legacy_request_id converge al mismo FlowRun aunque COMPLETED | DESIGN-DEBT → NOT_A_DEFECT (idempotencia deliberada)
F-06 | wave-collision | minio_storage.go:303-306 + paths.go | keys MinIO sin segmento de run: re-run mismo scope sobreescribe | CONFIRMED-DEFECT | CRITICAL → NOT_A_DEFECT (reemplazo explícito; condición wave_key única)
F-07 | upload-integrity | minio_uploader.go:187,266 | PutObject sin sha256 compare-before-overwrite (job_config/.cfx) | POC-SHORTCUT | HIGH → NOT_A_DEFECT (misma condición)
F-08 | dedup-by-size | minio_storage.go:214-234 | igual FILE SIZE = mismo contenido → estrategia distinta se dropea | CONFIRMED-DEFECT | HIGH (active)
F-09 | stamping | EchoForgeRobustRunExporter.java:49-52 | stamping per-wave con defaults silenciosos si falta .properties | CONFIRMED-DEFECT | HIGH (active)
F-10 | stamping | java:109-141 + robust_activity.go:653 | Magic 888111 compartido por wave (variable UUID fija) | POC-SHORTCUT | HIGH | GP:y (active — GP BLOCKER)
F-11 | stamping | robust_activity.go:683-686 | props global Windows compartido entre tasks | POC-SHORTCUT | HIGH → LEGACY_BUT_LIVE (rama legacy)
F-12 | selection-race | robust_activity.go:700-716 | pick por ModTime en databank compartida | CONFIRMED-DEFECT | HIGH → LEGACY_BUT_LIVE (durable physical no usa modtime)
F-13 | legacy-path | robust_activity.go:600-700 | ApplySelectedRun legacy vivo junto al durable | STALE → LEGACY_BUT_LIVE
F-14 | java-defaults | EchoForgeMT5Exporter.java:34-50 | props/output globales compartidos | POC-SHORTCUT | MEDIUM (scale debt)
F-15 | naming-collision | EchoForgeMT5Exporter.java:68 | filenames sanitizados colisionan y sobreescriben | POC-SHORTCUT | MEDIUM (active)
F-16 | legacy-bridge | runtime/config.go:592-624 | ranking→Retester por basename único | DESIGN-DEBT → LEGACY_BUT_LIVE
F-17 | legacy-writer | worker/steps/steps.go:2782-2806 | databank_metadata legacy en paths no-durables | STALE → LEGACY_BUT_LIVE
F-18 | mongo-uniqueness | adapter.go:589-598 | databank_metadata UNIQUE(wave_key,strategy_id): wave_key reusada pisa metadata | CONFIRMED-DEFECT | HIGH (validation gap active)
F-19 | mongo-uniqueness | evaluations :137-156 | strategy_evaluations UNIQUE(wave,strategy) choca con variant/sample | CONFIRMED-DEFECT | HIGH → DEPRECATED (colección legacy)
F-20 | pg-uniqueness | migrations/001:253-259 | UNIQUE(evaluation_ref): 1 Evaluation ↔ 1 StageExecution para siempre; sin reuso | DESIGN-DEBT | MEDIUM (by-design big-bang)
F-21 | dead-store | adapter.go:797-806 | mt5_deployments sin writers/readers | CONFIRMED-DEFECT | HIGH → CONTRACT_GAP (feature NI-DL-1)
F-22 | version-column | adopt_strategy.go:83,164-173 | version escrita una vez, nunca incrementada; correcciones dead-end | DESIGN-DEBT | MEDIUM → resuelve F0 versioning
F-23 | participation-roles | adopt_strategy.go:182-202 | REUSED/IMPORTED inalcanzables; REPROCESSED mal etiqueta | CONFIRMED-DEFECT | LOW
F-24 | hardcoded-window | generic_workflow.go:712,2167 | fechas deviation 2018-2019 hardcodeadas | POC-SHORTCUT | HIGH (active)
F-25 | single-symbol-config | input/example/config.json + wave_config.go:28-37 | wave ejemplo mono-símbolo; enum 8 símbolos hardcode | POC-SHORTCUT | MEDIUM (catálogo → base del CC del magic)
F-26 | symbol-leak | tools/insert_metadata.go:30-43 | tool hardcodea XAUUSD/H1 | STALE
F-27 | tf-fallback | uploader-minio/minio_uploader.go:144-152 | defaults H1/L silenciosos | POC-SHORTCUT | MEDIUM → UNKNOWN (uso del adapter por confirmar)
F-28 | adaptive-keys | worker/mt5_activities.go:200-217 | keys "<StrategyID>.mq5" sin scope; ex5Key descartado | POC-SHORTCUT | MEDIUM → DEPRECATED (path adaptivo)
F-29 | wave-type-juggling | adapter.go:113-118 | wave string vs int coerciones | DESIGN-DEBT | LOW
F-30 | export-run-overwrite | adapter.go:734-742 | export_runs ReplaceOne por (wave,stage,exporter) | CONFIRMED-DEFECT | HIGH (validation gap active)
F-31 | wave-report-uniqueness | adapter.go:813-817 | UNIQUE(wave,generated_at); sin versionado de reports | DESIGN-DEBT | LOW
F-32 | ea-exports | adapter.go:720-724 | ea_exports pisa registro previo por (wave,strategy,version) | DESIGN-DEBT | MEDIUM
F-33 | _SUCCESS | wfm/binding/persist.go:116-117 | ingestion legacy depende de _SUCCESS local sin marker remoto | DESIGN-DEBT | MEDIUM
F-34 | logical_type-decision | classification.go:202-260 | firma de indicadores alimenta grouping/rankings reales | DESIGN-DEBT | MEDIUM
F-35 | requestid-duality | watcher/steps.go:274 vs 423 | dos request ids por flow; joins no calzan | DESIGN-DEBT | LOW
F-36 | deployer-secrets | specs/FEAT-DEPLOYER-CROSS-PLATFORM-STAGER/ASSESSMENT.md | MINIO creds commiteados; etcd sin namespace | POC-SHORTCUT | HIGH (security)
F-37 | terminal-handoff-vacuum | artifact_runner.go:28-187 | pipeline termina en backtest evidence; publish/link pendientes | DESIGN-DEBT → CONTRACT_GAP (NI-MP)
F-38 | scale-matrices | adapter.go:24-33 | wfm_matrices BSON monolítico riesgo 16MB | DESIGN-DEBT | MEDIUM
```

#### C.2 Runtime Echo (E-xx)

```
E-01 | EA-ref | reference_v3.mq4:43,311,393 | literal "default" → pseudo-estrategia magic_default compartida | POC-SHORTCUT | MEDIUM (active)
E-02 | EA-ref | mq4:135-137 vs mq5:154 | GetEffectiveStrategyID int (MT4) vs long (MT5) | DESIGN-DEBT | LOW
E-03 | EA-ref | mq4:138-145 | double-prefix guard solo en binarios nuevos; viejos mintean magic_magic_X | STALE → CONFIRMED (skew binarios; cubre N1)
E-04 | EA-native-id | EchoOrderDetection.mqh:51-73 | trade_id sintético trunca account a 32 bits + tick bits16-31 | POC-SHORTCUT | MEDIUM (N-track)
E-05 | EA-native-id | EchoOrderDetection.mqh:89-94 | magic=0 → strategy_id literal NATIVE colapsa todos los manuales | POC-SHORTCUT | HIGH (decisión #11: bucket explícito fuera de Quality canónica)
E-06 | EA-close | execution_agent_v3.mq4:1379-1389 | close con strategy_id "" si stores fallan | CONFIRMED-DEFECT | MEDIUM (N-track)
E-07 | EA-close | execution_agent_v3.mq4:2018-2089 + CleanupOld(7) | MAX_CLOSE_AGE_DAYS=7 descarta cierres viejos → OPEN eterno | CONFIRMED-DEFECT | HIGH (PRIORITARIO bajo DEMO permanente)
E-08 | EA-close | execution_agent_v3.mq4:2008-2076 | closes demorados hasta reconexión | DESIGN-DEBT | LOW
E-09 | EA-close | execution_agent_v3.mq4:2380-2429 | protocolo por sentinel strings | POC-SHORTCUT | LOW
E-10 | EA-symbol | EchoCommon.mqh:130-165 | 6 sufijos hardcode; sin alias table; GOLD≠XAUUSD fragmenta | CONFIRMED-DEFECT | HIGH (pre-A3/funnel)
E-11 | EA-symbol | EchoCommon.mqh:100-127 | broker key = AccountCompany() texto libre | DESIGN-DEBT | MEDIUM
E-12 | EA-native | execution_agent_v3.mq4:497-517 | intent_sent antes de ACK; sin retry de encolados | DESIGN-DEBT | MEDIUM (N-track)
E-13 | EA-json | reference_v3.mq4:657-662 | SL/TP omitidos (no cero) cuando 0 | POC-SHORTCUT | LOW
E-14 | EA-close | execution_agent_v3.mq4:~1352 | side UNKNOWN; digits 5 fijo | POC-SHORTCUT | LOW
E-15 | EA-close | execution_agent_v3.mq4:~2320 | lot DoubleToString(lots,2) → 0.005→0.00 | POC-SHORTCUT | LOW
E-16 | Journal | trade_journal_repository.go:53-58 @HEAD | early-return sin broker pierde opens nativos por FK | CONFIRMED-DEFECT@HEAD → RESOLVED_UPSTREAM
E-17 | Journal | ensureJournalParentRows | placeholders side BOTH/timeframe M1 contaminan catálogo; irreversibles por DO NOTHING | POC-SHORTCUT | HIGH (mitiga F2 pre-provision)
E-18 | Journal | SaveOpen merge path | sellado vs COALESCE no especificado; conflictos ignorados | UNKNOWN → C1 test
E-19 | Bridge | pipe_handler.go:~1099 @HEAD | exec results sin broker fallback (close sí) | CONFIRMED-DEFECT@HEAD | CRITICAL → RESOLVED_UPSTREAM
E-20 | Bridge-handshake | reference_v3.mq4:303-395 | EA duplica defaults del bridge (dual SoT) | POC-SHORTCUT | MEDIUM (consolidar F0)
E-21 | EA-uuid | reference_v3.mq4:173-205 | UUIDv7 no-spec + ids sintéticos ba5e: dos regímenes | DESIGN-DEBT | LOW
E-22 | EA-platform | EchoOrderDetection mt4 vs mt5 | close_reason no comparable cross-plataforma | DESIGN-DEBT | LOW
```

#### C.3 Persistencia/constraints (P-xx)

```
P-01 | echo/sdk-postgres | trade_journal_repository.go:58-95 | FK RESTRICT fuerza autoprovision placeholder; mirror=fact; irremplazable | MIRROR | HIGH (mitiga F2 pre-provision)
P-02 | echo/sdk-lab | ids/ids.go:14-41 | safeSegment no inyectivo → posible merge de trades | DESIGN-DEBT | LOW-MEDIUM (scale)
P-03 | echo/lab-worker | 046:131-141 | dedupe import scoped al batch → duplicados cross-batch | UNIQ/IDEM | HIGH (scale; IMPORT sin uso aún)
P-04 | echo/lab-worker | canonical_repo.go:86-122 | upsert puede mover fila entre scopes del partial index → abort de batch | UNIQ | MEDIUM (active)
P-05 | echo/jobs | analytics_backfill_v1.sql:277 | source_type AS origin choca con CHECK por generación de schema | MIRROR | HIGH → DEPRECATED (job RFC-003)
P-06 | echo/scripts | rollout_v3_production_idempotent.sql | rollout compilado omite 042; 4 definiciones de source_type | MIRROR | HIGH (ops; revisar en M0A)
P-07 | echo/hasura | metadata/tables/*.yaml | ~20 objetos usados por front sin tracking | MIRROR | MEDIUM (M0A)
P-08 | echo/core | account_sync.go:550-617 | daily_hwm via GREATEST de snapshots: pérdidas subestiman HWM para siempre | DERIVED | MEDIUM
P-09 | echo/sdk+gateway | client_config.go:131 + accounts_repository.go:333 + hasura_handler.go:135 | default native_magic triple-implementado | DERIVED | MEDIUM (F0 consolida)
P-10 | echo/kache | account_configs.go:172-186 | tombstones memory-only; rebuild resucita borrados | DERIVED/IDEM | MEDIUM
P-11 | echo/lab | 046 DDL + outcomes_repo.go:41 | outcomes/curves sin FK a canonical; delete+insert race | UNIQ/FK | MEDIUM
P-12 | echo/front+db | strategies.js deleteStrategy + FK CASCADE 001:1134 | delete UI borra policies en cascada | FK | HIGH (quick fix M0B)
P-13 | echo/db | 001 RESTRICT vs CASCADE | reglas de delete contradictorias enmascaran split catálogo/observado | FK | MEDIUM
P-14 | echo/analytics | 043:362 + 056 | matviews leídas sin REFRESH wrapper visible | DERIVED | LOW
P-15 | echo/lab-worker | snapshots_segments.go:161-217 | risk policy histórica leída de fila vigente (sin history) | DERIVED | MEDIUM (pre-portfolio)
P-16 | symphony/pg | 001:31 + 005 | dual-model v0/v1 sin unicidad cruzada | UNIQ | HIGH → DEPRECATED (cleanup A6)
P-17 | symphony/pg | postgres_registry.go:114-141 | v0 DO UPDATE vs v1 DO NOTHING contradictorios | MIRROR/IDEM | MEDIUM → DEPRECATED (v0)
P-18 | symphony/pg | adopt_strategy.go:182-202 | race PRODUCED/is_origin sin FOR UPDATE; conflicto mal manejado | UNIQ/IDEM | MEDIUM (active)
P-19 | symphony/domain | persistence_identity.go:395-409 | refs embeden UUID de stage: cero reuso cross-wave | IDEM | MEDIUM (by-design)
P-20 | symphony/pg | stage_execution.go:175-180 | ON CONFLICT PK vs UNIQUE global acoplados | UNIQ | LOW
P-21 | symphony/mongo | evidence_indexes.go | collections de evidencia SIN unique indexes declaradas | UNIQ | MEDIUM (hardening)
P-22 | symphony/mongo | adapter.go:441-537 | databank_metadata mutable UNIQUE(wave,strategy) | DERIVED | LOW
P-23 | symphony/idem | contracts.go:355-359 | BuildIngestKey computada pero jamás consumida | IDEM | HIGH → CONTRACT_GAP (la consume F1)
P-24 | symphony/pg | grep repo | version nunca incrementa; correcciones dead-end | IDEM | MEDIUM (resuelve F0)
P-25 | symphony/pg | persistence_identity.go:216-279 | generation manual sin helper; mis-set duplica evidencia | IDEM | MEDIUM
P-26 | symphony/java | TradeIdentity.java:30-47 | trade_key incluye orderId NO emitido: irreproducible; sin magic/ticket/volumen/SL | IDEM | HIGH → anexo NI-EI-2
P-27 | symphony/minio | artifact_store.go:146 etc | PutObject incondicional sin object-lock | UNIQ | MEDIUM (hardening)
P-28 | symphony/pg | decision_store.go:67-118 | decision_evidence CASCADE latente; supersedes sin lifecycle | FK | LOW
```

#### C.4 Drift documentación↔implementación (D-xx)

```
D-01 | RFC-A §5.6/§7 promete port EchoIngestor + adapters/echo-api | no existe en ningún path | CRITICAL → REFRAME: entregable F1 en GenericSQXWorkflow
D-02 | adaptive_workflow.go:271-316 llama echo_ingest/link_demo_deployment/wave_report | activities sin registrar; workflow DEPRECATED | HIGH → DEPRECATED
D-03 | SPECS.md trata Adaptive como Spec-Active | código: "oficial es GenericSQXWorkflow" (adaptive_workflow.go:22-23) | HIGH → DEPRECATED
D-04 | SPEC GWT-6 cierra lineage con eslabón "echo" | solo Candidate.EchoRef; sin writer | MEDIUM → DEPRECATED (rediseña en F1)
D-05 | EchoStrategyRef vs echo_ref | nombres divergen | LOW → TERMINOLOGY
D-06 | SPECS stats 38/16 | real 49/23 | LOW → STALE_DOC
D-07 | Status Model 7 estados | catálogo usa estados indefinidos | MEDIUM → STALE_DOC
D-08 | ROBUST-SELECTION NORMAL "pendiente" | implementado y registrado | MEDIUM → STALE_DOC
D-09 | LINEAGE "(pendiente)" | strategy_lineage implementada | LOW → STALE_DOC
D-10 | WAVE-REPORTING "(pendiente)" | generate_report parcial bajo otro nombre | LOW → STALE_DOC
D-11 | RFC-010 "no se agregan columnas" | 045/056/060 añadieron 7 columnas escritas hoy | HIGH → SCHEDULED C3
D-12 | RFC-010 prohibe origin | 056 la reintrodujo y Go escribe | HIGH → SCHEDULED M0A (D1)
D-13 | RFC-010 taxonomy 2 errores | set real 4 | LOW → SCHEDULED C3
D-14 | RFC-010 7 métricas | emitidas verbatim | INFO (alineado)
D-15 | RFC-010 dup-OPEN mantiene hecho | código rechaza upsert completo | MEDIUM → SCHEDULED C3
D-16 | ticket_mismatch attrs/metric | error wrapped pelado | LOW → SCHEDULED C3
D-17 | RFC-010 backfill usa IMPORT | IMPORT sin implementación | MEDIUM → FEATURE_SCHEDULED
D-18 | CLOSE-sin-OPEN rechazado | conforme | INFO (alineado)
D-19 | RFC-009 coverage blocker ≥99% | gate bloquea <95% | HIGH → SCHEDULED M0A (semántica gate)
D-20 | lag recorded-event WARN>60s | SQL informativo sin threshold | MEDIUM → STALE_DOC
D-21 | RFC-009 tabla blockers | SQL difiere (policy_cov<80 warn, CURRENCY_MISMATCH extra) | LOW → SCHEDULED M0A
D-22 | RFC-009 segments TRAINING/PRE_LIVE/LIVE | nadie escribe lab_strategy_segments; default LIVE | HIGH → FEATURE_SCHEDULED (pre-portfolio; relevante por #8)
D-23 | INITIAL_VIRTUAL_CAPITAL 10000 | coincide curves.go:12 | INFO (alineado)
D-24 | screener/fn_lab_* nombres | 047 coincide | INFO (alineado)
D-25 | 5 identificadores de estrategia sin reconciliar | strategy_id SPEC vs StrategyRef UUID vs canonical filename vs journal string vs magic | HIGH → TERMINOLOGY (lo define F1)
D-26 | deployment_key vs PublishKey | doble nombre, entidad indefinida | MEDIUM → TERMINOLOGY
D-27 | "promoción" sin definición formal; PRD §2.4 | desconectado de PRE_LIVE→LIVE | MEDIUM → TERMINOLOGY (definir con lifecycle #8)
D-28 | wave_key/wave_id/Wave/request_id/token vocabularios | tres familias sin doc puente | LOW → TERMINOLOGY
```

### D. Identity lifecycle — CURRENT (flujo real, v2)

- Forge: SQX genera `.sqx` → cfgID sprintf sin contenido (generic_workflow.go:33 — mutación silenciosa posible) → canonical_strategy_id por normalización de FILENAME con HOST_KEY (solo creación; fila adoptada inmutable) → StrategyRef UUID `(config_id, canonical)` partial UNIQUE v1 → FlowRun (request_id/token) → StageExecutions/Evaluations/MetricSets/TradeSets (refs hash sin reuso cross-wave) → RobustRun estampa params + MagicNumber compartido de wave (888111) como Variable makeExternal ⇒ input del EA exportado → MQ5/EX5 → MinIO keys determinísticas por identidad lógica (overwrite intra-scope deliberado) → terminal SOLO backtest; publish/demo attach inexistente (features NI-MP/NI-DL pendientes).
- Echo: reference EA collector itera PositionsTotal(), lee POSITION_MAGIC del EA de estrategia y mintea trade_id UUIDv7 + strategy_id="magic_<n>" (fallbacks default/NATIVE) → bridge → planner match EXACTO contra policies (miss ⇒ drop) → mm_engine override magic para orden copiada → journal SaveOpen (COALESCE + autoprovision placeholder side=BOTH/timeframe=M1) → lab agrupa por strategy_id solo (+segmento default LIVE) → screener LEFT JOIN definitions (NULL names) → Daily Ops (filtro ACTIVE + ventana HWM).

### E. Identity lifecycle — TARGET (v2, con decisiones owner)

```text
Strategy (lógica; ej. entrada EMA / salida RSI)
   │  strategy_id CANÓNICO E INMUTABLE — asignado por FORGE al crear/adoptar la estrategia
   │  (canonical_strategy_id, formato verificado "<INSTRUMENT>_<L/S>_<TF>_<flow>_v<n>_Strategy_<x.y.z>[.<host>]");
   │  Echo RECIBE una identidad ya estable e inmutable (no la acuña);
   │  constraint: debe caber en varchar(64) del journal — validar/capacitar en F1
   ├── 1..N Version (params evolutivos v1→v2→v3; misma lógica, misma identidad)
   │      └── current_version puntero MUTABLE en el estado/catálogo de la estrategia (Echo);
   │          cada promoción agrega un PromotionRecord INMUTABLE (version, wave, decision, artifact)
   │      + linaje autoritativo de versiones en Forge (Decisions/Evaluations)
   ├── 1..1 MagicNumber SEMÁNTICO ÚNICO (pertenece a la Strategy; estable entre versiones y cuentas;
   │      asignado por registry Forge en promoción; nunca reutilizado)
   ├── provenance Forge (StrategyRef, wave_key, decision_ref, sha256 artifacts) — referenciado, no duplicado
   └── runtime bindings (Echo): policies(exec_account, strategy_id) + accounts config + mapping magic→strategy_id

Reference EA (collector de la cuenta demo) → magic observado → mapping → strategy_id canónico
   → trade_journal.strategy_id == strategy_id canónico (fase 2)
   → The Lab agrupa por la MISMA identidad que Forge y Echo
```

- Resolución de identidad en runtime (decisión owner): para toda estrategia NUEVA Forge→Echo, F0/F1 entregan al Reference collector el mapa `{magic_number → canonical strategy_id}` (client_config) de modo que resuelva MagicNumber → canonical ANTES de escribir el journal — el journal nace con el id canónico, sin transición `magic_<n>`. El prefijo `magic_*` queda exclusivamente LEGACY/HISTÓRICO: los trades previos se unen al mundo canónico vía alias en el registro de ingesta/mapping, sin backfill obligatorio. `magic_default`/placeholders desaparecen porque la ingesta pre-crea la definición real.
- Manual/native magic=0 → bucket explícito `NATIVE` (o `MANUAL`) excluido de Strategy Quality canónica, visible como DQ; decisión fina en N-track sin tocar el modelo canónico.
- **Lifecycles desacoplados (owner 2026-08-24)**: (i) *Strategy*: INGESTED → VALIDATING (forward) → PORTFOLIO_ELIGIBLE → IN_PORTFOLIO (0..N veces) / RETIRED — la identidad y su serie viven para siempre; (ii) *Deployment*: Reference DEMO permanente + Broker mirrors DEMO permanentes (0..N brokers) + deployments reales 0..N posteriores — entrar a real NO apaga los demos; (iii) *Portfolio Eligibility*: puerta de EVIDENCIA (~3–6 meses forward + mínimos de trades/DQ/no-degradación vs predicción), habilita a participar en construcción automática; nunca implica deploy automático. El vocabulario RFC-009 §13 NO mapea 1:1 a este lifecycle: DEMO y REAL coexisten permanentemente para la misma estrategia, así que un segmento exclusivo por estrategia no puede representar ambos. La semántica de `lab_strategy_segments` queda como DECISIÓN ANALÍTICA pre-P1 (candidatos: segmentos por deployment/rol de cuenta, o ventanas temporales por cuenta), no como estado exclusivo de Strategy; el writer (D-22) sigue agendado en el hito de acumulación pero su diseño se cierra antes de P1.

> [!warning] Delta 2026-08-24 — identidad V2 ya cortada en paralelo
> El track [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] cerró **DURABLE-STRATEGY-IDENTITY-V2-CUTOVER-NORMAL PASS/CLOSED** (`7c0b289` = origin/master): adopción vía `upsertStrategyV2`, unique parcial global WHERE `identity_model_version=2`, dominio elegido **MODEL 1 GENERATED_STRATEGY / SINGLE_ENTITY** (`_robust` colapsa al mismo id), autoridad generation-scoped y pinning/pureza del canonicalizer resueltos como prerequisito (G2B demostró que `<id>.zeus.sqx` producía dos business keys según HOST_KEY; los tokens `.zN/.hN/.kN` son cohort token del Builder, jamás identidad semántica). Impacto en este doc: (1) valida empíricamente la aclaración owner #2; (2) la parte "identidad" de F0 YA está en ejecución en ese track — **F0 se acota a MagicNumber estándar/registry/stamping/plumbing 64-bit/mapping**; (3) secciones CURRENT/D describen el estado @`4af9d087` (pre-cutover) y quedan como línea base histórica. Próximo exacto de ese track: V2-E2E-CERTIFICATION-NORMAL, luego G3 fork contract / G4 reconciliación brownfield.

### F. MagicNumber — estándar propuesto (semántico + registry, KISS)

- Formato decimal 10 dígitos `YYMMCCQQQQ`: YY año (26), MM mes (08), CC código de catálogo de símbolos (2 dígitos; tabla registrada en Forge extendiendo `supportedInstruments` — ej. 10=XAUUSD, 20=EURUSD…; base F-25), QQQQ secuencia mensual por símbolo (0001–9999).
- Ejemplo concreto: XAUUSD, agosto 2026, primera promovida → `26` `08` `10` `0001` = **2608100001**.
- Asignación: en la promoción (tras Decision `OPTIMIZER_SELECTION`), transaccional en registry Forge `sqx.strategy_magic(strategy_canonical_id UNIQUE, magic UNIQUE, status ACTIVE|RETIRED, assigned_at, decision_ref)`; contador por slot (YYMM,CC) con row-lock; overflow >9999/mes/símbolo ⇒ fail-closed (capacidad ~9.999×99×12×~87 años ≈ 1.0×10^9).
- Rango: 10 dígitos SIEMPRE excede int32 (≥2.6×10^9) ⇒ **requiere el plumbing 64-bit (decisión #4)**: EchoPersistence.magic_number int→long, `magic_number_override` int4→int8, eliminar casts `(int)` en mt5. Compat MT4 futura: exigiría esquema compacto separado o rango dedicado < 2^31 — documentado, no condiciona V1.
- Semántica para humanos/debug en logs de MetaTrader; la fuente de verdad SIEMPRE es el registry (lookup, no parsing).
- Lifecycle: inmutable; estable entre versiones de la misma Strategy; compartido cross-cuenta (agregación correcta en Lab); RETIRED jamás reutiliza número; re-compilación/redeploy conservan magic (binding = registro + checksum ex5).
- Migración 888111: waves ya compiladas se rigen por single-strategy-per-chart (SPEC v1) hasta re-stamp; golden path parte con allocation nueva.

### G. Modelo de dominio Forge↔Echo (hechos → storage mínimo)

- Hechos a recordar para siempre: (1) identidad canónica ↔ provenance Forge ↔ magic — registros de ingesta/promoción INMUTABLES y append-only Echo-side, uno por promoción (`strategy_canonical_id, version, wave_key, magic, decision_ref, sha256 artifacts, timestamps`) que CONSUMEN la idempotency key `(wave_key, strategy_id, version)` hoy huérfana (P-23). (2) Binding runtime — YA tiene storage correcto: policies (copy matrix, valid_until soft-retire) + accounts; no se crea tabla deployments en Echo (NI-DL-1 puede responder desde facts + mt5_deployments Forge-side). (3) Versiones — linaje autoritativo en Forge; el puntero `current_version` es MUTABLE y vive en el estado/catálogo de la estrategia (lado Echo), nunca dentro del registro de ingesta inmutable.
- Duplicación prohibida: métricas/evidencia de Forge no se copian (refs + sha256 alcanzan); strategy_definitions permanece espejo autoprovisionado, no autoridad (y con pre-provision en ingesta recibe filas REALES con nombre).

### H. Patrones transversales (lecciones)

- Identidad derivada de presentación (filenames/free-text) como clave de storage — mitigado por congelar-at-nacer + registry.
- Determinismo por omisión de run-id: feature de routing, riesgo solo si wave_key no es única por flow (validar en intake = fix barato).
- Claves de idempotencia computadas sin consumidor — el Golden Path las consume.
- Defaults silenciosos donde corresponde fail-closed (stamping props, H1/L, side BOTH/M1, LIVE-default segments).
- Stores sin constraints que el dominio supone (Mongo evidence, mt5_deployments, outcomes sin FK).

### I. ROADMAP MAESTRO — FREEZE DEFINITIVO 2026-08-24

> [!success] Freeze
> Correcciones de consistencia aplicadas (asignación de strategy_id en creación/adopción Forge; resolución MagicNumber→canónico pre-journal sin transición `magic_<n>` para estrategias nuevas; semántica de segments como decisión analítica pre-P1; wording canónico en Users). Parche final post-review: `current_version` vive como puntero mutable en el estado/catálogo de la estrategia; los registros de ingesta/promoción son inmutables y append-only, uno por promoción. DAG y decisiones congelados; cada milestone se diseña en profundidad justo antes de ejecutarse.

```text
M0 FOUNDATION CLOSURE (R0 repo reconcile + Gate GO + security mínimo + cleanup M0B)
   │
   ▼
F0 IDENTITY FOUNDATION (magic YYMMCCQQQQ + registry + stamping único + plumbing
   │                     64-bit + mapping fase 1; identidad lógica ya corre en V2 track)
   ▼
F1 FORGE↔ECHO CONTRACT (ingesta + provenance + idempotencia + auth; insertion Generic)
   │
   ▼
F2A ATTRIBUTION GOLDEN PATH ──────────────── arranca EL RELOJ de validación SQ
   ▼
F2B BROKER MIRROR GOLDEN PATH (1 broker) ─── arranca evidencia EF por trade
   ▼
F3 DEMO NETWORK (mirrors permanentes N brokers, mirroring automático, runbook demos)
   │
   ▼  ACUMULACIÓN (corre desde F2A/F2B; F3 puede terminar después)
   ├── A0 Strategy Quality (monitor forward continuo, Reference-only)
   ├── A1 Execution Fidelity (dashboards (strategy,broker,symbol) construibles ya)
   ▼
EVIDENCE GATE: ~3–6 meses calendario + mínimos trades/DQ/no-degradación vs predicción
   ▼
P1 PORTFOLIO ELIGIBILITY ──► P2 AUTOMATIC PORTFOLIO CONSTRUCTION
   ▼
P3 REAL DEPLOYMENT / ACCOUNT IMPACT ──► A3 DEGRADATION / FEEDBACK ──► ORACLE
```

Dependencias corregidas vs propuesta owner: el reloj de 3–6 meses arranca en F2A (no espera F2B/F3); A0 no es milestone nuevo sino monitor sobre outcomes REFERENCE-only ya operativos + join de provenance; A1 puede construirse durante la acumulación porque los datos existen desde F2B; el Gate depende de calendario+evidencia, no de F3 completo. Los demos NUNCA se apagan al entrar a real.

Tracks paralelos: SECURITY/OPERABILITY · CLEANUP/DEPRECATION BURN-DOWN · PLATFORM CONVERGENCE · USERS/OWNERSHIP (diseño) · NATIVE CORRECTNESS.

#### DAG v2 previo (histórico)

```text
R0 repo reconcile (fetch; diff dirty vs origin; confirma E-16/E-19 upstream)
   │
M0A Canonical Journal / Gate GO (G1 fix gate + D1 DROP origin/comment + matview
   │    + metadata Hasura + ratificar FAILED + decisión semántica coverage)
   ├── M0B cleanup Etapa 10 (paralelo, no bloquea) ── incluye quick-fix P-12 (CASCADE guard)
   ├── S1 seguridad (rotaciones + auth base gateway — prerrequisito de exponer ingesta)
   ▼
F0 Strategy Identity & MT5 Runtime Identity
   (registry semántico YYMMCCQQQQ + stamping magic único en RobustRun +
    plumbing 64-bit: persistence long, override int8, sin casts +
    consolidación defaults + decisión versioning + mapping magic→canónico fase 1)
   ▼
F1 Forge↔Echo Contract Closure
   (NI-EI-1/2 + NI-DL-1 dueño Echo Core; endpoint de ingesta en GenericSQXWorkflow
    tras verify_robust_run_selected; consume idempotency key; varchar(64) check;
    anexo trade-list orderId/magic/volume/SL; vocabulario único de identidad)
   ▼
F2 Forge→Echo DEMO Golden Path (1 estrategia, Reference-only, attach manual,
   ingest pre-provisiona strategy_definitions real)
   ▼
ACUMULACIÓN 3–6+ meses (serie temporal viva; N-track EA fixes — E-07 prioritario;
   writer de segments DEMO/PRE_LIVE antes de portfolio)
   ├── A1 Execution Fidelity (v_trade_execution_delta)
   ├── A3 Degradation Funnel (observacional; requiere E-10 símbolos + P-26 anexo)
   ▼
Portfolio Construction / Account Impact (segments + policy history P-15)
   ▼
Oracle
```

### J. F1 — NEED-INFO a cerrar (v2)

- NI-EI-1: endpoint/auth/schema/idempotencia; payload con `strategy_id` canónico inmutable + `allocated_magic` + `version`; respuesta `echo_strategy_ref` estable; inserción en GenericSQXWorkflow (punto: post `verify_robust_run_selected`, previo a `mt5_exporter`).
- NI-EI-2: historial de trades con orderId/ticket, magic, volume y SL/risk por trade (prerrequisito funnel A3).
- NI-DL-1: link deployment; respuesta derivable de facts (policies/accounts) + mt5_deployments Forge-side.
- NI-MP-1: spike attach desatendido (deploy manual aceptable para F2).
- Definiciones formales: promoción, finalista→DEMO→elegible (lifecycle #8), y vocabulario único D-25..28.

### K. Golden Path — F2A / F2B / F3

- **F2A Strategy Attribution Golden Path** — 1 estrategia Forge (con su canonical strategy_id ya asignado al crearse/adoptarse): magic semántico asignado y estampado → attach manual del ex5 en la cuenta Reference DEMO → ingest idempotente en Echo (ingest record + definición real + mapa `{magic→canonical}` entregado vía client_config) → reference EA collector resuelve MagicNumber → canonical strategy_id ANTES de escribir el journal (journal nace con id canónico, sin `magic_<n>`) → outcome en Lab → reverse provenance completo hacia wave/decision_ref/sha256 sin parsear filenames. **Arranca el reloj SQ.**
- **F2B Broker Mirror Golden Path** — el mismo trade: Echo copier → 1 cuenta DEMO de un broker → pata EXECUTION en journal → primera reconciliación Reference vs Execution (`v_trade_execution_delta`). **Arranca la evidencia EF.**
- **F3 Demo Network** — mirrors permanentes configurados para N brokers, mirroring automático y operación continua (incluye runbook de renovación de demos). La acumulación de meses corre desde F2A/F2B; F3 puede cerrar después sin detenerla.
- Validación incluida en F2A: una segunda estrategia en la misma cuenta con magic distinto no colisiona. Fuera de alcance: portfolio real, automation de publish, feedback loop.

#### Prueba mínima original (histórico, absorbida por F2A/F2B)

- 1 estrategia: F0 asigna magic semántico → RobustRun estampa → compile → attach MANUAL del ex5 (input magic) en chart de cuenta demo multi-estrategia-ready → Echo ingest idempotente (consume key, crea ingest record + strategy_definitions REAL) → reference EA collector detecta posición por ticket, magic → mapping fase 1 → journal strategy_id resoluble a canónico → lab_canonical → outcome en screener → reverse completo hacia wave/decision_ref/sha256 sin parsear filenames.
- Éxito adicional: segunda estrategia en la misma cuenta demo con magic distinto NO colisiona (valida el estándar). Fuera de alcance: automation publish, execution copy, portfolio.

### L. Analytics target — dos problemas distintos, cuatro vistas (v3)

- **A0 Strategy Quality / Live Validation** — pregunta: ¿la estrategia sigue funcionando out-of-sample cuando corre forward fuera de los datos de su creación? Es validación DE LA ESTRATEGIA (defensa contra overfitting, curve fitting, regime dependence). Base exclusiva: Reference forward (outcomes REFERENCE-only ya operativos) contrastada contra la predicción Forge (funnel). Por naturaleza requiere calendario (3–6 meses) + suficientes trades. No mezcla jamás métricas de copiado en sus scores (RFC-009 §9.6.1).
- **A1 Execution Fidelity** — pregunta: ¿qué tan bien Echo/broker REPRODUCE cada señal? Es validación DEL COPIADOR+broker. Datos: pares Reference↔Execution vía `v_trade_execution_delta` (entry/exit slippage, latencia, missed/rejected, spread impact, fill/lot/risk deviations, close timing, ΔR). NO espera meses: se acumula por trade desde el primer mirror. Granularidad recomendada: primaria **(strategy_id, broker_id, symbol)** en ventanas móviles; `account` es atributo que pertenece a Account Impact (P3); `strategy_version` como slice de drift; `period` para tendencia; `execution_policy` como atributo del copy config. Global EF = agregación ponderada entre brokers, construida DESPUÉS de la primaria broker-specific.
- **Account/Broker Impact (P3)** — ¿en qué infraestructura funciona mejor o peor? Comparaciones longitudinales sobre historial acumulado (cuenta × policy × MM × broker).
- **A3 Degradation Funnel** — Forge predicted → Reference forward → broker execution → real portfolio. Observacional; prerrequisitos: A0+A1+provenance+E-10 símbolos normalizados+P-26 anexo; ventanas calendario solapadas; sin grupo control en V1.
- **Broker Demo Mirrors desde día 1 — EVALUADO: KEEP (dirección correcta)** — Reference DEMO canónica + mirrors DEMO permanentes por broker acumulan SIMULTÁNEAMENTE evidencia SQ (reloj) y EF (por trade) sin capital real. Consecuencias aceptadas: policy row por cuenta espejo (config operacional explícita — NO auto-provisioning, D3 sigue en pie), volumen journal ×N brokers (trivial para el stack), y un runbook de renovación de cuentas demo (los brokers las expiran) en el track de operabilidad.

### M. Decisiones owner restantes (pos-alineamiento)

- (1) Confirmar formato `YYMMCCQQQQ` y el catálogo de códigos CC de símbolos.
- (2) Semántica del check policy_coverage del gate (corregir query vs sembrar master policies).
- (3) Superficie/auth del endpoint de ingesta (gateway endurecido vs servicio mínimo).
- (4) Bucket para magic=0 manual: mantener literal NATIVE vs renombrar MANUAL y excluir de outcomes.

### N. Orden de ejecución (3 iteraciones)

- Iteración 1: R0 (reconciliar clone + verificar fixes upstream) + G1 + correr gate corregido + abrir respuestas NEED-INFO (borrador F1).
- Iteración 2: M0A completo (migración origin/comment + matview + Hasura metadata + GO documentado + ratificaciones C3) + S1 rotaciones.
- Iteración 3: F0 diseño/impl registry + stamping + plumbing 64-bit + mapping fase 1; spec lote N-track EA (E-07 primero); cierre F1.

### NORTH STAR — ECHO FOREX COMPLETE

- Sistema fully automated, robust, scalable, observable y maintainable para **Forex**, capaz de: generar estrategias → validar robustez → promover → correr forward demo → evaluar Strategy Quality → evaluar ejecución cross-broker → construir portfolios automáticamente → desplegarlos/gestionarlos → monitorear degradación → retirar/reoptimizar estrategias → preservar provenance completa de punta a punta.
- Alcance vigente: **FOREX**. **FUTURES = proyecto futuro independiente** (otras tecnologías/soluciones); prohibido introducir abstracciones cross-asset prematuramente "por si acaso".

### USERS / OWNERSHIP — IMPORTANT, NON-CRITICAL NOW

- Objetivo: diseño listo durante el año; sin implementar multi-tenancy ahora. Lectura recomendada: es un problema de **ownership más que de tenancy** (plataforma compartida con estrategias/runs/portfolios separados por usuario; aislamiento duro no requerido en V1).
- Entidades que eventualmente llevan `owner_id`: strategies (Forge + Echo ingest record), forge runs/configs (heredan de la estrategia), portfolios, deployments y accounts (si terceros traen sus propias cuentas demo). Lab gana filtro opcional por owner. Nada de esto bloquea ni contradice el modelo actual.
- Decisiones presentes ya compatibles por diseño: strategy_id canónico globalmente único (registry), auth token-per-client en la ingesta, contratos sin supuestos mono-usuario. Regla YAGNI: NO añadir columnas owner hoy; mantenerlas triviales de agregar (FKs centralizadas en las entidades listadas).

### PLATFORM CONVERGENCE — progresivo

- Meta: dejar de sentirse como dos sistemas ("Echo" y "Symphony") y ser **un solo ecosistema Echo** con fronteras limpias: Forge (dominio cuantitativo) · Runtime/Core (copiado) · Bridge · Gateway/API · Lab (analítica) · Front · shared SDK/contracts. No implica monorepo.
- Vehículo existente verificado: el repo `xKoRx/sdk` ya transporta tipos de contrato cruzados (ej. parser del trade-manifest) — es el lugar natural del contrato compartido.
- Primer paso concreto: que el contrato F1 nazca como artefacto compartido (spec + tipos + cliente generado) consumido por symphony y echo; después naming consistente y eliminación de duplicación contractual (PRD §17 vs SPEC vs RFC).

### CLEANUP / DEPRECATION BURN-DOWN — progresivo, no bloqueante

- Alcance: borrar código realmente muerto, archivar RFCs/SPECS stale (D-06..D-10), marcar deprecated lo deprecated (Adaptive, rutas legacy), retirar scripts que no deben ejecutarse (stage0_audit, compilados duplicados), reducir dual models tras certificación V2, alinear vault con código.
- Exit criterion eventual: **un agente nuevo no puede confundirse entre las tres generaciones arquitectónicas**.
- Regla: IMPORTANT ≠ CRITICAL PATH; solo toca el critical path cuando un legacy afecte directamente el active path.

### M. Decisiones owner restantes (post-freeze)

- (1) Catálogo de códigos CC del estándar magic (`YYMMCCQQQQ`). (2) Semántica del check `policy_coverage` del gate. (3) Superficie/auth del endpoint de ingesta (gateway endurecido vs servicio mínimo). (4) Bucket para magic=0: mantener `NATIVE` vs renombrar `MANUAL`. (5) Criterios cuantitativos exactos del Evidence Gate — se diseñan al llegar a P1.
- Resueltas por owner en esta pasada: separación SQ≠EF, mirrors día-1 (KEEP), F2A/F2B/F3, triple lifecycle, elegibilidad≠deploy, freeze del roadmap maestro.

## Fuentes

- Verificación read-only 2026-08-23 (agente principal + 6 subagentes) sobre `~/go/src/github.com/xKoRx/echo` (@309d4707 + dirty diff; origin/master=e25165ba vía ls-remote) y `~/go/src/github.com/xKoRx/symphony` (@4af9d087).
- Spot-checks propios: canonical_strategy_id.go (HOST_KEY creación-only), paths.go (keys sin run-segment, comentario de diseño), ids.go safeSegment, reference_v3.mq5:861-878 (collector sin filtro), EchoPersistence.mqh (int magic), execution_agent_v3.mq4 MAX_CLOSE_AGE_DAYS/CleanupOld(7), strategies.js deleteStrategy + CASCADE 001:1134.
- Verificación 2026-08-24 (alineamiento): cmd/sqx-worker/main.go:344-350 (workflows registrados; Generic activo), generic_workflow.go:405-704 (casos select_robust_run/verify_robust_run_selected/apply_selected_run/mt5_exporter; sin echo_*), generic_workflow.go:33-36 (cfgID sprintf), activities/watcher/steps.go:276,325 (sprintf duplicado), 001_schema_baseline.up.sql:822 (client_native_magic int8) y :1126 (override int4), adopt_strategy.go (ON CONFLICT DO NOTHING — identidad no muta post-creación).
- [EXTERNAL]: tipos/límites MQL4/MQL5, preservación server-side del magic, efecto netting.
