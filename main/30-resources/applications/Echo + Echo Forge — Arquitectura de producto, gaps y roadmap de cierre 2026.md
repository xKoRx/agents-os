---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources: ["[[Echo — Fuentes de arquitectura y producto 2026-09-06]]", "[[Echo Forge — Fuentes de arquitectura y producto 2026-09-06]]", "[[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]]"]
last_verified: "2026-09-06"
confidence: "high"
aliases: ["Echo + Echo Forge — Product Architecture, Gap Analysis and 2026 Completion Roadmap", "Echo Product Complete 2026", "Auditoría maestra Echo y Echo Forge 2026"]
tags: ["kind/resource", "area/echo"]
created: "2026-09-06"
updated: "2026-09-07"
---

# Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026

> [!info] Convergencia contractual — 2026-09-07
> [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]: disposición B, Echo SDK como autoridad del contrato compartido, dos tracks preparados y ningún nuevo TOP. Sustituye la propuesta de SDK externo; conserva arquitectura/Decisions ratificadas. Source Lab permite R AUTO money→pips→journal: no interpretar R del journal como prueba de base única en todo Lab.

## Síntesis vigente

**Delta de contratos/source 2026-09-06 (posterior a este corte):** [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] cierra el seam identity/version→ingestion→runtime→Reference→routing como propuesta I, con O1–O3 explícitas. Symphony HEAD/master reconfirmado `db8a022`: B1A `185825c`, B1B `ef65dd1` y B2 `db8a022` presentes; NEXT EXACT factory **C1**, sin nuevo deploy/cert físico. Temporal SQX declara v1.35.0, pero el workspace resuelve v1.44.1; no confundir pin declarado, build y binario desplegado. Las secciones de estado anteriores conservan su corte a10c26c. **Revisión de durabilidad 2026-09-07:** [[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]] ratifica el grafo y decide **B — FREEZE AFTER BOUNDED CORRECTIONS** (siete correcciones acotadas, ningún TOP; O1/O3 pasan a default técnico, O2 sólo catálogo CC).

**Revisión independiente 2026-09-06:** [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]] contiene errata material, Gap Register V2, alcance mínimo, alternativas y siete hitos de uso. Se corrigieron aquí hechos erróneos/supersedidos; las propuestas amplias restantes no se elevan a frozen.

1. **Madurez actual:** Forge Finalist Factory V1 conserva su cierre contractual; el ecosistema integrado todavía no es un producto autónomo. Echo posee runtime de copiado, journal y Lab Clean, no un lifecycle completo de inversión.
2. **Realidad revalidada independientemente:** core productivo `e25165ba`, Gateway `0abdf720`, Lab con build modificado; 2647 Reference actuales y 4388 Reference archivadas potencialmente recuperables. EA/versiones/continuidad aún U. La revisión independiente sí inspeccionó producción read-only; la auditoría inicial no.
3. **Mayor gap de producto:** identidad runtime + ingestión + observación forward atribuible + decisiones de elegibilidad/allocation/provisioning que cierren el loop.
4. **Mayor deuda técnica:** errores de journal absorbidos, identidad `magic_*`, API de control sin auth propia y analytics que pueden presentar datos incompletos o semánticamente engañosos.
5. **Mayor riesgo calendario:** el owner ya exige aproximadamente 3–6 meses de forward; quedan 116 días desde el corte hasta el 31-12. Seis meses nuevos no caben.
6. **2026 PRODUCT COMPLETE:** **YES WITH SCOPE** para una plataforma V1 Forex/MT5, con gates y automatización acotada; no hay evidencia para prometer una cartera nueva validada seis meses y operando dinero real antes de diciembre.
7. **Ruta mínima revisada:** cerrar exposición de control y persistencia del journal, terminar factory fiable en paralelo con recuperación histórica y captura versionada; ingestión individual y baseline pequeña; PortfolioVersion con selección/allocation y apply/ACK, sin framework general de Decisions.
8. **Límite:** resultados futuros, rentabilidad y elegibilidad no se garantizan por completar software. Cero candidatos elegibles es un resultado válido y debe dejar el capital sin asignar.

**Corte verificable:** 2026-09-06, America/Santiago. Recurso de arquitectura/producto reutilizable; no worklog ni autorización para implementar. El encargo del owner define el target. Los hallazgos describen source al commit indicado; el roadmap es una propuesta explícita, salvo contratos ya frozen. No se modificaron repos productivos, DB, EAs, migraciones ni despliegues.

**Lectura rápida futura:** estado [[#2. Current State Map]] → límites y autoridades [[#4. Entity / authority map]] → deuda [[#15. Debt register consolidado]] → plan [[#17. Roadmap ejecutable hasta diciembre]] → acción [[#23. NEXT EXACT]]. La segunda pasada modificó requisitos de los milestones, no sólo la lista de riesgos.

### Disciplina de evidencia

| Marca | Significado |
|---|---|
| **S** | PROVEN IN SOURCE: implementación/schema/test inspeccionados; no prueba deploy ni uso físico. Los IDs Fxx/Exx resuelven en [[#Evidencia y provenance]]. |
| **P** | PROVEN IN PHYSICAL / PRODUCTION EVIDENCE: artefacto o acta con identidad concreta de una ejecución. Se distingue evidencia primaria conservada de certificación reportada en el vault; ninguna equivale a una recertificación de hoy. |
| **D** | OWNER/FROZEN DECISION: decisión owner o contrato explícitamente frozen; no se cuenta como implementación. Un SPEC propuesto sin aprobación es I, no D. |
| **I** | INFERENCE: conclusión o diseño recomendado derivado de lo anterior. |
| **U** | UNKNOWN / REQUIRES AUDIT: no se pudo probar en el alcance; ausencia de coincidencias no demuestra inexistencia global. |

## 1. Baseline, alcance y evolución que hay que preservar

| Repositorio | Commit inspeccionado | Estado y alcance |
|---|---|---|
| `xKoRx/symphony` | `a10c26c887e4d203b403d2557e292ed773830b0e` | HEAD/master y master remoto consultado coinciden. Pool local MT5 incorporado. Hay dirty ajeno en fixtures/config/manifest/specs: preservado; no usado como release authority. |
| `xKoRx/echo` | `04c16bd2bd7b69725560873950a5d6b067fd3a4f` | Master remoto inspeccionado en clone aislado. Checkout habitual seguía en `e25165ba2e57a86b7cdcbd78d44406f66fc9ba23`; único delta entre ambos: sintaxis del readiness check. El source de runtime descrito coincide. |
| `xKoRx/sdk` | `c85594440f6755443ceb97ec4e333cd0ddb5b0ed` | SDK externo usado por Forge; no confundir con `echo/v3/sdk`. Pin de módulo y reemplazo local contrastados. |
| `xKoRx/stager` | `083dff2806cdc133a43a48ff461bca242d3129d1` | Contrato one-shot, verificación SHA/size y CURRENT/PENDING; no posee el dominio de jobs. Inspección acotada. |
| `xKoRx/api-core`, `api-persist`, `mde` | `e8dfd108671232ed8cc006a98c9b8d9e7fa223e9`, `dcc7e2b032a459701f7b2baf279bd5775b578c9c`, `c62b3c286bff099242a61c03b36bbaeea5c37759` | Rutas inspeccionadas: signals/trades/candles/documents; no endpoint Finalist Ingestion en esas rutas. No se los propone como dueño por llamarse “core”. Vigencia productiva U; master remoto no contrastado para estos auxiliares. |

**P reportada, no ejecutada aquí:** release Forge `0.2.96` en `3b0737c1efe153f1f72eec40465fd1aa883887d0`, SDK anterior exacto; cuatro workers convergidos, MT5 6180. Campaign `0ac51a05-7bd8-49a8-a130-4c4e205d7084` produjo ocho estrategias nuevas en dos waves, cero finalistas, terminó por MAX_WAVES_REACHED y fue redelivered sin duplicar. Esto certificó replenishment/identidad/stop/result/replay, **no supply no vacío ni calidad económica**. El cierre V1 no se borra; tampoco se extiende al target V2. [P01]

Dos FULL posteriores, FlowRunRefs `8088ef7c-6e49-4ce6-a5ac-b8b6b0fbe90a` y `162e7878-5b80-487f-bd5e-d0e7cde3a3a7`, llegaron a tres Final Reretester/Compile cada uno; seis backtests murieron por timeout de 45m sobre 2016-01-04→2026-06-05. El preflight registrado confirma seis TradeSetRefs durables exactos; `trade_lists` legacy vacío no implica ausencia de baseline. Evidencia reportada P02, no nueva consulta a MinIO/Temporal. No hay autorización para un tercer FULL en esta misión.

Echo V1/V2 son históricos según su constitución; esta auditoría usa `v3/`. El Lab Clean no es la arquitectura antigua RFC-003/Strategy Lab V3: migración 052 elimina parte de ella. Tampoco `AdaptiveSQXWorkflow` es el Generic activo: su llamada `echo_ingest` y sus mocks no prueban una integración real. [E01–E05, F04]

## 2. Current State Map

Bandas de madurez cualitativas: **alta** = núcleo source y evidencia física acotada; **media** = implementación usable con límites; **baja** = tablas/stubs/contratos sin loop certificado; **nula** = sin implementación encontrada en el path activo. No son porcentajes de esfuerzo restante.

| Capability / target | Implementación actual y evidencia | Madurez | Estado | Blocker de producto |
|---|---|---|---|---|
| Builder autónomo + replenishment | Identidad de batch/generación, waves frescas y stop durable [F01,F08,P01] | Alta V1 | DONE contractual | Yield económicamente útil y Golden no vacío V2 |
| Clasificación por familia/comportamiento | Firma de indicadores y snapshots por logical type [F05] | Media sintáctica | PARTIAL | Familia de variantes y comportamiento/correlación no se deducen de firma |
| Retest/Optimizer/WFM/robust/Apply | Bindings durables, Decision OPTIMIZER_SELECTION, fanout Final Reretester [F02,F03,P02] | Alta núcleo | DONE acotado | Runtime SQX largo, provenance de dataset y renovación de parámetros |
| Export/compile/backtest físico | EX5/HTM, parser 6090/6140/6180, normalize/reconcile [F06,F09,P03] | Media | PARTIAL | Ownership global, retry/drain, timeout killer, slots sin cert física |
| SQX↔MT5 fidelity | MetricSets/TradeSets/Score shadow, comparability explícita [F06] | Alta analítica | DONE acotado | V1 la usa indirectamente como admisión |
| Finalist membership | Promotion toma TopProjection; Result cross-check exige igualdad [F07] | Alta V1 | WRONG SEMANTICS target | V2 implementada + gate instrument/timeframe requested |
| Campaign/Result | Stop/replenishment/results exactos [F07,F08,P01] | Alta V1 | DONE V1 / PARTIAL V2 | Rank nullable, result/output versions y cap físico=4 |
| Ingestión Forge→Echo | SPEC bloqueada; Adaptive mock; Gateway sin ruta [F04,E01] | Nula | MISSING | Contrato compartido, owner Echo, identidad/magic/auth |
| Catálogo/identidad Echo | strategy_definitions descriptiva, autoprovision FK y `magic_*` EA [E06,E07] | Baja | WRONG SEMANTICS target | Registry + versiones + mapping antes del journal |
| Copiado live Reference→Execution | Kafka/StateFun/MM/Bridge/EA, policies, estados cuenta [E08,E09] | Media | PARTIAL | ACK ambiguity, restore/replay, riesgo agregado y safety gates |
| Journal de hechos | Unique trade/account, conflictos y tiempos event/recorded [E10] | Media | PARTIAL | Error absorbido; CLOSE sin OPEN; ventanas EA 7d |
| Execution Fidelity | `v_trade_execution_delta` INNER JOIN y funciones analíticas [E11] | Baja-media | PARTIAL | Universo esperado, missing/extra, fills, versiones y clocks |
| Strategy Analytics | Lab Clean Reference-only, R/money/curvas/snapshots [E02,E03] | Media | PARTIAL | DQ/recompute, clocks, histórico de policy y denominadores |
| Strategy Quality/forward vs Forge | Live health antiguo compara ventanas adyacentes; imports stub [E04,E12] | Baja | MISSING target | Expectation versionada, enrollment, captura y evidencia temporal |
| Degradación/régimen | Flags/status analíticos; no loop durable verificado [E03,E12] | Baja | PARTIAL | Políticas calibradas, causas separadas, Decisions |
| Account/broker/prop analytics | Snapshots, rulesets, jobs Account Lab, daily HWM [E09,E13] | Media | PARTIAL | Intraday equity, reset calendarios, conciliación broker/cashflows |
| Portfolio construction | Account groups + portfolios analíticos versionados [E14] | Baja-media | PARTIAL | Jobs dependen de tablas eliminadas; pesos ≠ riesgo real |
| Rebalance/replacement automático | Dry-run SQL con steps, recomendaciones; no actuator productivo probado [E15] | Baja | MISSING target | Eligibility, allocation, lifecycle transaccional y compensación |
| Front/control | Vue/Hasura, Lab Clean + legacy, admin mutations [E16] | Media | PARTIAL | Lecturas rotas/stale, auth/roles y read models Forge |
| Operación unattended | OTel, Stager, drain local, checkpoints y retry [F10,E17] | Media componentes | PARTIAL | DR conjunto, incidentes/reprocessing, cutover/fleet/retención |
| Seguridad/control | Gateway mux+CORS `*`; cliente web usa admin secret Hasura [E01,E16] | Baja | PARTIAL / P0 | Auth/authz/control plane, rotación y verificación de exposición |

## 3. Target end-state architecture

**I, propuesta evolutiva.** Mantener PostgreSQL/MongoDB/MinIO/Temporal en Forge y PostgreSQL/Kafka/StateFun/Bridge/MT5 en Echo. No migrar todo a un bus, motor de workflow o monorepo único. Temporal orquesta cómputo/transferencias; Kafka transporta hechos y comandos; ninguno define por sí solo autoridad económica.

```text
OWNER INTENT + config/dataset/build/policy versions
  → Forge Campaign → Generic Flow → Builder → classify/early select
  → Retest → Optimize/WFM → RobustSelection Decision → Apply
  → Final Reretester → MT5 export/compile/physical backtest
  → structural reconcile → FinalistPromotion V2 Decision
       ├→ fidelity Score/warnings → ranking/projection (read/recommend)
       └→ immutable finalist manifest + exact historical evidence refs
             → Echo Ingestion API → ingestion receipt / canonical registry
                  ├→ StrategyVersion + magic binding + PromotionRecord
                  ├→ Expectation binding / validation enrollment
                  └→ read model: INGESTED, readiness explicit

Reference DEMO permanente ← provisioning/attach + physical binding ACK
  → collector maps magic → canonical Strategy + observed version
  → raw durable event → journal/reference facts
       ├→ Reference Forward → Strategy Quality metrics → Validation Decision
       └→ routing/allocation snapshot → MM → commands → Broker/Execution EA
                  → ACK/deals/positions → execution facts → reconciliation
                  → Execution Fidelity metrics/diagnostics → broker actions

eligible candidate snapshot + constraints + market/account facts
  → PortfolioSelection Decision → RiskAllocation Decision → PortfolioVersion
  → provisioning intent → account/policy/EA ACK → Activation Decision
  → monitoring → reduce/pause/replace/rebalance Decision → version N+1
      (Reference y mirrors continúan; cash/no replacement es outcome válido)

ALL FACTS → versioned analytics publication → read models → Front READ/OBSERVE
ALL DECISIONS → immutable evidence links + effect ledger + human audit
OPERATIONS → liveness, data freshness, broker reconciliation, DR, kill controls
```

**Fronteras:** ingestión recibe y registra; provisioning prepara bindings; activation habilita una versión ya verificada; allocation decide exposición. La existencia de una fila/EX5/score no autoriza ninguna de las otras tres. La unidad de servicio física puede seguir siendo Gateway/core/lab-worker; las fronteras lógicas no obligan a crear un microservicio por concepto.

**Storage:** Forge PG = control/identidad/Decisions; Mongo = evidence inmutable/MetricSets/TradeSets metadata/Score/RankingSnapshot; MinIO = bytes verificados. Echo PG = facts/registry/receipts/Decisions/read models; sus grandes evidencias históricas se consumen por contrato de artefactos con refs y digest, no SELECTs sobre DB de Forge. Guardar derivados nuevos de Echo no equivale a copiar toda la evidencia de Forge. La retención de cada artefacto referenciado por un portfolio activo debe sobrevivir a la retención del Flow/Temporal history.

## 4. Entity / authority map

| Entidad | Owner e identidad | Store / writer actual | Readers / lifecycle y autoridad target |
|---|---|---|---|
| Strategy Forge | Registry Forge; StrategyRef UUID, canonical_strategy_id V2 global | PG `sqx.strategies`; adopción V2 [F01] | Workflows/evidence; identidad creada una vez, no filename recalculado ni magic |
| Generated strategy/version | Misma Strategy para evolución de parámetros según owner; evidencia de ejecución concreta | Versiones/artefactos/evaluations existen; registro de versión cross-system incompleto [D01,F03] | `current_version` puede ser puntero de catálogo; facts siempre fijan versión concreta |
| Runtime Magic | Forge registry según freeze; único/estable/no reciclado | Registry `strategy_magic` propuesto, no encontrado en migraciones; Apply recibe magic explícito [F03,E07] | EA collector resuelve magic→canonical; magic≠StrategyRef; 64-bit E2E |
| FlowRun | Forge; UUID + FlowIntentToken/RunIntentKey | PG flow_runs; intake/dispatcher [F01] | Snapshot config y contract; no “latest wave” |
| StageExecution | Forge; UUID + identidad stage/task/subject/inputs/generation | PG stage_executions/results/producer outputs [F02] | START/RUNNING/seal/terminal; sólo resultados sellados cuentan |
| Evaluation | Producer contract + StageExecution + subject/scope digest | Mongo evaluations, immutable put [F02] | Una evaluación no es una strategy ni estado runtime |
| MetricSet | Evaluation + scope/catalog/calculator/formula digest | Mongo metric_sets [F02,F06] | Native/derived tipados; missing no es cero; unidades obligatorias |
| TradeSet | Evaluation/scope/parser/schema; metadata + payload ref | Mongo trade_sets + MinIO [F02,F06] | Historia física normalizada; no inferir desde `trade_lists` legacy |
| Artifact | Producer/exact store/bucket/key/size/SHA256 | MinIO write-once/verify; PG registra namespace/output [F02,F09] | Bytes inmutables, ETag no es digest de negocio |
| Score | Subject+algorithm/version/params/input refs | Mongo scores [F06] | COMPUTED/NOT_COMPARABLE/INVALID_INPUT; nunca lifecycle por sí solo |
| RankingSnapshot | Cohort+config+algorithm+inputs exactos | Mongo ranking snapshots [F05,F07] | Orden/TopProjection; no membresía V2 |
| Decision Forge | DecisionRef; policy/config/evidence binding | PG decisions + decision_evidence [F07] | OPTIMIZER_SELECTION y FINALIST_PROMOTION; histórico V1 no se reescribe |
| Campaign | CampaignRef + intent token | PG campaigns/waves/finalists/stop evaluations [F08] | target unique StrategyRef, stop explícito; recompone supply, no cartera |
| Ingestion/PromotionRecord | Echo acepta canonical externo; receipt por request+digest | **MISSING** [F04,E01] | Immutable recibo/version/provenance; no asigna dinero ni despliega |
| Strategy Echo | Identidad canónica Forge; mirror descriptivo | strategy_definitions con writer Hasura y journal autoprovision [E06] | Hoy múltiples writers con responsabilidades distintas; registry authoritative debe preceder al mirror |
| Reference | EA collector + Strategy/Version/observation binding | ReferenceEvent en Kafka; journal role REFERENCE [E08,E10] | Es operación observada de Reference, no señal ideal pre-broker; una serie canónica por enrollment |
| Execution | command ID + trade ID + account + fill/deal identity | StateFun/Bridge/EA + journal role EXECUTION [E08,E10] | 0..N ejecuciones por Reference; deal/fill ledger y expected routing incompletos |
| Account/Broker | Echo account ID/broker ID; connection role separado | PG + snapshot/cache + Hasura/auto-provision [E06,E09] | ACTIVE de UI no sustituye estado operativo/opens permitidos |
| Policy actual | (account_id,strategy_id), version/valid_until | PG account_strategy_risk_policy; Hasura/webhook/cache [E09] | Config mutable, no archivo histórico de decisiones; sellar applied policy por comando |
| Lab canonical/outcome | Echo; journal source ID / canonical trade ID | PG lab_*; recompute [E02] | Reference-only outcomes probado; preservar source kind/role y corregir ids no inyectivos |
| Validation/Eligibility | Echo; StrategyVersion+Expectation+observation+cutoff+policy | Legacy health table existe; **Decision target MISSING** [E12] | Resultado UNKNOWN/INSUFFICIENT separado de FAIL; vigencia explícita |
| Portfolio cuentas | Echo UI; portfolios.id | PG portfolios + portfolio_accounts [E14] | Grupo de monitorización; conservar nombre/vista, no convertirlo en allocation |
| Portfolio estrategias | Echo; strategy_portfolios + version UUID | PG 039, Hasura permite modificar allocations [E14] | Versión publicada inmutable; versión borrador editable; cuentas/mandato/riesgo enlazados |
| Allocation / Activation | Echo; version+account+strategy version+risk intent | Sólo pesos analíticos y policies de ejecución hoy [E09,E14] | Decisions y effects faltantes; no usar peso como lote sin riesgo/margen |
| Runtime binding | Echo posee intención de operación; EA/broker confirma estado observado | Accounts+policies existentes, vínculo versión/EX5 observado incompleto | Conservar storage mínimo frozen; facts de provisioning/ACK pueden vivir en ledger, no exigir tabla deployments por anticipación |

**Identidades y alcance de colisiones:** `StrategyRef` UUID≠canonical_strategy_id largo≠`magic_123`≠ticket≠trade_id. No truncar para caber en varchar(64), ni generar una identidad Echo competidora. Verificar longitudes máximas y contratos de todos los readers antes de ampliar aditivamente. `CanonicalTradeIDJournal` reemplaza caracteres por `_`: strings arbitrarios pueden colisionar, pero no se probó reachability para el alfabeto legal actual y la consulta productiva no encontró colisiones. Guard/encoding inyectivo antes de ampliar inputs; no migrar todas las keys ni elevarlo a P0 actual por posibilidad teórica. [E06,E07,E18]

**Versión + magic estable:** un magic por Strategy no identifica cuál versión abrió una posición. Necesita binding temporal al EX5/param digest y captura por trade. Si v1 y v2 corren simultáneamente con el mismo magic en la misma cuenta, no hay mapping unívoco con el contrato actual; prohibir esa combinación o aportar identidad de instancia antes del primer rolling upgrade. [I derivada de D01/E07]

## 5. Forge completion assessment

### Qué está construido y qué significa su cierre

El Generic activo ya tiene la arquitectura durable que faltaba en el POC: identidad V2, FlowRun/stages, productores sellados, contratos Apply/Final Reretester, reconcile MT5, scores/snapshots/Decisions y Campaign. Reescribir eso no reduce la deuda principal. Los antiguos findings de sobrescritura/dedupe/legacy se deben revalidar por wiring; no reciclar los 112 hallazgos de agosto como si siguieran vivos. El preflight de seis TradeSets demuestra por qué un grep vacío en una colección legacy no prueba pérdida de datos. [S F01–F09; P02]

**Después de B+C1+C2+D+release+certificaciones, sí puede ser una factory física V2 acotada; no toda la fábrica autónoma de supply económicamente diverso ni el ecosistema completo.** Gaps adicionales concretos:

| Gap | Evidencia / impacto | Contrato a cerrar |
|---|---|---|
| Identidad runtime y versionado exportable | Apply exige magic configurado, no lo asigna globalmente; Java aún posee fallback histórico [F03] | Registry único + stamping verificable + `StrategyVersion/EX5` binding; no acusar al path durable de usar siempre 888111 |
| Diversidad real | Clasificación por firma/indicadores [F05] | `family_id`/derivation lineage + behavior features; family policy en selección portfolio, no filtro invisible de Promotion |
| Expectation reusable | Hay TradeSets/WFM/MetricSets, no Expectation portable [F06,F04] | Contrato independiente de fidelity con coverage y condiciones de entrenamiento/evaluación |
| Data provenance | Config/código/artifact hashes no certifican por sí solos histórico de ticks, spread, sesiones o revisiones vendor | Snapshot de dataset/build/broker/feed/timezone/settings o `UNVERIFIED_DATASET`; reprocesar exacto vs repetir con datos actualizados deben distinguirse |
| Recovery cross-store | PG stage puede quedar RUNNING después de resolve y error reconcile [F06]; escrituras PG/Mongo/MinIO no son transacción global | Reconciler con refs exactas, seal publication, missing vs unavailable; sin “latest” ni repetir cómputo si evidencia verificada existe |
| Retry/drain flota | Slot local no deduplica LogicalJobID global; timeout mata cómputo sano [F10,D02] | B frozen: CAS ETCD no-TTL + singleton + fencing + árbol físico + reuso HTM; liveness≠muerte |
| Recursos caros | max_waves/Builder cap existen; no presupuesto unificado probado [F08] | Admisión por cuota/costo/storage, fair scheduling y backlog; presupuesto detiene nuevas admisiones, no mata tácitamente un job sano |
| Reoptimización programada | Optimizador existe; `future_reoptimization_date` sólo intención de ingest [F04] | Nueva versión con nueva evidencia, no reemplazo mutable silencioso; auto-renovación avanzada diferible |
| Read/inspect | Result exacto es buen contrato; UI factory/campaña/cohort no encontrada integrada | API read-only + timeline/funnel/warnings; SQX Pool/viewer VM aislada es SHOULD |
| Suficiencia de supply | Zero-supply y max_waves son resultados válidos [P01] | Distinguir completed/computationally valid/target met/eligible for investment; yield medido y presupuesto explícito |

**Certificación V2 mínima:** 3 slots con compile/backtest compartiendo pool; cancel slot-scoped; crash de worker; pérdida de heartbeat; partición entre hosts y ETCD; unknown build cuarentena local; drain sin matar job sano; retry después de HTM durable; cohorte lógica > slots y > antiguo cap=4; V1 replay/result intactos; V2 NOT_COMPARABLE válido permanece finalista; requested instrument/timeframe incorrectos bloquean candidato; cero finalistas honesto; FULL real con al menos un finalista y artifacts verificados. Tests locales no sustituyen ninguno de los casos físicos.

## 6. Forge→Echo ingestion assessment y contrato mínimo

**S:** Gateway Echo V3 no expone ingestión; la SPEC Forge declara NEED-INFO de API/auth/schema, contiene dependencias antiguas a deviation filter y su idempotency key wave+strategy+version no está cerrada con StrategyRef/Promotion V2. `echo_ingest` del Adaptive sólo tiene DTO/callsite y mock encontrado; no adapter HTTP ni activity productiva registrada equivalente. `lab-worker` imports retorna nil como stub. [F04,E01,E04]

**Owner recomendado, I:** módulo de dominio de ingestión del lado Echo servido inicialmente por Gateway endurecido. Reusar proceso y PostgreSQL; extraer servicio independiente sólo si aislamiento de permisos/ciclo de despliegue lo exige. Forge llama API; jamás escribe DB Echo. Contrato compartido versionado en `xKoRx/sdk` o artefacto generado compatible con ambos SDKs; no importar core de Echo en Forge.

### “Ingested Strategy” tiene que significar esto

**Mínimo revisado I:** POST individual síncrono + PromotionRecord como receipt; batch cliente por elemento. Estados async sólo si latencia lo demuestra. No son dependencias obligatorias de V1. Se conserva key owner y digest, ver companion §5.

En una transacción local Echo existe: identidad canónica aceptada, StrategyVersion concreta, recibo inmutable de promoción con origen/digest, metadata descriptiva real, binding magic/canonical coherente y manifest de evidencia verificable. Estado de recursos/evidence listo o pendiente se expone por separado. **No existen por implicación cuenta asignada, EA adjunto, routing de copias, elegibilidad, activation ni capital.** El default de settings o una FK autoprovisionada no cumplen el contrato.

| Aspecto | Propuesta contractual I para TOP F1 / M3 |
|---|---|
| Request | `contract_version`, `idempotency_key`, `payload_digest`, source instance, canonical_strategy_id, identity_model_version, StrategyRef, StrategyVersionRef, magic binding, PromotionDecisionRef/version, FlowRunRef/CampaignRef opcional, ArtifactRefs exactos, typed evaluation/metric/tradeset refs, ranking opcional, warnings, expectation readiness |
| Autoridad de membresía | Decision FINALIST_PROMOTION V1 histórica o V2 nueva validada según su versión. No regenerar membership leyendo TopProjection, ni usar un score mínimo oculto |
| Idempotencia de operación | V1 revisada: key owner `(wave_key, canonical_strategy_id, version)` con namespace productor, digest y PromotionDecisionRef vinculada; misma key/contenido retorna mismo PromotionRecord, conflicto rechaza. No cambiar key frozen sin contrato explícito |
| Dedupe de entidad | Unique por identidad canónica externa; nuevo receipt de otra wave no crea otra Strategy. Una reoptimización sólo agrega versión cuando cambia artefacto/config semántica, preservando lineage |
| BWC | Aceptar/mantener identificador de idempotencia histórico si ya se acordó, pero añadir binding de digest/Decision; no reinterpretar recibos V1 |
| Artefactos | Referencias verificadas por API/artifact access protocol; no SQL interservicio ni URL efímera como identidad. Autorización, retención y renovación de acceso separadas del SHA. El consumidor descarga a storage propio sólo por necesidad operativa con mismo digest |
| Historial | No reinsertar SQX/MT5 como live journal. Import/read pipeline idempotente por TradeSetRef+parser+trade key, source/historical scope explícitos; no duplicar entre batches |
| Transactionality | V1 revisada: registry+PromotionRecord atómicos después de verificación acotada; consultar key tras timeout. Outbox sólo si hay publicación requerida. Async/saga en mismo registro se añade si latencia real lo exige; no XA |
| Batch | Diferido: V1 usa cliente que itera por ítem idempotente. Si volumen justifica batch, conservar outcomes por ítem; no inventar entidad de receipt batch ni placeholder para cero finalistas |
| Errores | Contrato/identity/digest conflict definitivo; 429/5xx/unavailable retryable con backoff y respeto Retry-After. Timeout ambiguo se resuelve consultando receipt antes de reenviar. 401/403 generan incidente de credenciales/permisos, no loop infinito |
| Response/read | `receipt_id`, canonical_strategy_id, version, outcome CREATED/ALREADY_ACCEPTED/CONFLICT/REJECTED/PENDING, exact missing refs y query result URL/ID; listar por Promotion/Campaign |
| Auth | Identidad de servicio específica con scope de ingestión; authz por operación/source/artifact. Nunca admin secret de Hasura en Forge ni UI |
| Zero-finalist | Forge result puede ser COMPLETED con target no logrado; Echo recibe cierre/no-op o no recibe ítems. Métrica factory no cuenta ingestión vacía como éxito de supply |

**Certificación:** 1 finalista real→registro→Reference trade→reverse provenance; resend exacto y concurrente; mismo canonical en dos promociones; mismo key/distinto digest; version nueva; dos ítems y falla parcial; HTM/EX5 missing vs checksum conflict vs permiso denegado; crash tras commit antes de HTTP response; 0 finalistas; `NOT_COMPARABLE` aceptado sin rank; artefactos de otra Strategy rechazados. Ensayar todos sin activation/capital involuntarios.

## 7. Echo lifecycle y Reference truth

**Actual S:** strategy_definitions contiene descriptor, no estado de lifecycle ni versión operativa. Accounts/policies controlan ejecución; account status de monitorización y estado cliente son conceptos distintos. Lab emite CANDIDATE/WATCH/INSUFFICIENT_DATA, no una transición del registry. No hay prueba de un state machine único DISCOVERED→RETIRED. [E03,E06,E09]

**D owner existente:** Strategy INGESTED→VALIDATING→PORTFOLIO_ELIGIBLE, posible pertenencia a 0..N portfolios, y retirement; Reference DEMO y broker mirrors permanecen al pasar a real. Mantenerlo. No meter “DEMO/REAL” en un enum exclusivo de Strategy ni interpretar `lab_strategy_segments` como deployment. [D01]

| Frontera | Entidad / condición | Acción autorizada | Lo que todavía no implica |
|---|---|---|---|
| Discovered | Candidate/Promotion conocida en Forge | Leer/evaluar manifest | Ingestión |
| Ingested | Receipt + identidad/version/refs aceptadas | Registry consultable; preparar observación | Provisioning |
| Provisioned | Assignment técnico, binario/params y cuenta preparados | Comprobar EA/broker binding | Opens habilitados/capital |
| Validating | Enrollment con Reference binding verificado | Acumular forward de esa versión | Elegibilidad por elapsed time solamente |
| Eligible | Decision Evidence Gate vigente por mandato | Entrar al candidate set | Selección ni activation |
| Assigned | PortfolioVersion/Allocation Decision fija estrategia y cuenta | Preparar routing/riesgo | Ejecución hasta ACK |
| Active | Activation con preconditions y ACK de versión/policy | Ejecutar nuevas aperturas según mandato | Todas las estrategias/versiones activas en todas las cuentas |
| Paused | New opens bloqueados por scope | Seguir reconciliando/cerrando riesgo existente | Liquidación inmediata automática |
| Quarantined | Identidad/facts/ejecución no confiables | Investigación/recovery | “Estrategia perdedora” |
| Degraded | Quality o execution diagnóstico tipado | Decisión reduce/pause/review según causa | Retirement automático por score genérico |
| Retired | Registry/policy evita nueva admisión | Drenar exposures; conservar facts | Borrar datos/reutilizar magic/apagar toda Reference sin política |

### Lineage Reference → Execution

El Reference EA observa operaciones de la cuenta; genera trade_id y strategy_id basado hoy en magic. Bridge acepta `reference_event` y alias `trade_intent` por el mismo handler, produce `echo.reference-events.v1`. StateFun lo consume por separado para planner y journal. Eso **no son dos OPEN semánticos**; son dos consumidores del mismo hecho. La unique `(trade_id,account_id)` y merge/conflict protegen doble entrega, pero no certifican exact-once de efecto broker ni preservación ante fallo de DB. [E07,E08,E10]

`ReferenceEvent.Price` es ejecución de la cuenta Reference, no precio teórico previo a OrderSend. Comparar Echo/broker contra ella mide reproducción relativa; no prueba fidelidad total al algoritmo/mercado ideal. Para reconstruir intención exacta, preservar raw envelope y versión de productor, inputs de EA, mapping/runtime binding, requested SL/TP/volumen/symbol, timestamps y la policy/routing snapshot aplicada. El journal mínimo conserva hechos seleccionados; no basta como archivo del comando completo. [E08]

Casos CLOSE anterior a OPEN y NATIVE: hay síntesis de OPEN nativo desde CloseResult si trae hechos necesarios, no un recovery general. Su existencia no legitima inventar apertura ni copiar ese patrón a Reference. Guardar hecho tardío/dead-letter y reconciliar antes de evaluar. Los manuales permanecen separados de Quality canónica. El collector de toda cuenta es válido bajo modelo multi-estrategia; el defecto es mapping ambiguo, no el escaneo. [E07,E10,D01]

## 8. Execution Fidelity blueprint

**Pregunta:** qué tan bien Echo y el broker reprodujeron la Reference bajo la policy realmente autorizada. Medible desde trade 1 como observación; la confianza de una agregación requiere N/tiempo. **No usarla como Strategy Quality ni confundirla con SQX↔MT5.**

`v_trade_execution_delta` es una base útil: join por trade_id, REFERENCE/EXECUTION, delta de entrada, diferencia temporal y PnL/pips. Su INNER JOIN **omite missing y extra**, carece de expected recipient set, no normaliza por side/pip value/risk/fees y no fija portfolio/policy/version. Ninguna ausencia en esa vista demuestra que no faltaron ejecuciones. [S E11]

| Capa | Datos / producto a construir |
|---|---|
| Raw facts | Reference event, routing recipients y razones de exclusión, command/attempt, timestamps send/receive/ACK/fill, requested/filled volume, broker order/deal/position IDs, partial fills, commissions/swap/currency, rejected/cancel/close facts, symbol/tick mapping version |
| Pairing | `(trade_id, recipient_account_id, allocation_version, command_kind)` más fills 1:N. Estados EXPECTED/PENDING/FILLED/PARTIAL/REJECTED/MISSING/EXTRA/NOT_REQUESTED/UNKNOWN. Deadline de ACK ≠ certeza de no-fill |
| Métricas por operación | entry/exit signed adverse delta por side y tick/pip; timing vector; fill ratio; costes; direction/symbol mismatch; holding delta; PnL difference normalizada a risk/lot y currency. Conservar también valores raw |
| Agregados | Por broker/account/strategy version/instrument/session/build/policy; trade count, p50/p95/tails, coverage/missing/rejected/extra; ventanas N trades/7d/30d/90d configurables; denominador = recipients esperados, no sólo pairs exitosos |
| Warnings | CLOCK_UNVERIFIED, SYMBOL_MAP_MISSING, POLICY_UNKNOWN, PARTIAL_UNRESOLVED, STALE_SNAPSHOT, COMPARISON_SIZE_MISMATCH; ningún NULL pasa a “0 slippage” |
| Score | Opcional por objetivo/mandato, algoritmo versionado; empezar con vector y coverage. No promediar dirección invertida o operación extra hasta esconderlas |
| Decision | Mismatch estructural/duplicate/exceso de exposición puede disparar quarantine; degradación agregada puede pausar broker/assignment o reducir exposición. La Strategy Reference puede seguir healthy |
| Read model | Trade comparison + execution coverage grid + broker quality con watermark, reasons, sample and policy/build; drilldown a command y broker facts |

**Certificación semántica:** Reference buena/Execution mala; Reference mala/Execution fiel; lotes deliberadamente distintos; delay configurado vs demora extra; rejection esperado vs perdido; SL/TP offsets explícitos; cierre autónomo de Execution vs close replicado; partial fill; command retry con ACK perdido; extra execution huérfana. Medir intención aplicada y outcomes, no castigar toda diferencia configurada como bug.

## 9. Strategy Quality / Live Validation blueprint

**Actual:** Lab Clean usa sólo Reference para outcomes, buena separación que se conserva. Pero `ComputeSubScores` llama `edge_score` a coverage de R y `risk_score=1-edge`; `ResolveStrategyStatus` usa 50/100 trades, 30/90 días, 80% coverage y 0.85 DQ. Esas son reglas implementadas de aptitud analítica, **no prueba de edge ni política aprobada de inversión**. [S E02,E03]

Live health 038 compara ventanas adyacentes del histórico Echo, no una expectativa Forge fijada antes del forward; su job depende de `strategy_reference_outcomes` retirado por 052. Tener columnas distribution_shift/DD percentile no prueba inferencia live operativa. Imports están stub. [S E04,E12]

### Expectation artifact propuesto

**Amplitud evolutiva I, no prerequisito completo de V1.** El mínimo operativo es baseline previa con identidad/versión/refs/unidades/períodos, enrollment y métricas compatibles; seasonality, regímenes y catálogo completo se difieren. Ver [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan#5. Minimum Usable Trading System V1]].

`StrategyExpectation@1` = identity/version + hash de config/EA/params + producer/formula versions + evidence refs + cohort selection context. Se sella **antes** de iniciar el forward usado para validarlo. Incluye:

- Universo temporal exacto y sample IS/OOS/WFM/final reretester/MT5; periods configurados separados de observed trades; dataset/feed/broker/build/settings/timezone/calendario/currency/PNL basis; unidades y cobertura.
- Trade frequency distribuida por exposure time/sesión/seasonality; distribución de net returns/R, DD de curva y rachas, expectancy, PF/win rate/duración. MAE/MFE sólo si hubo captura verificada; no reconstruir intratrade desde OPEN/CLOSE.
- Evidencia WFM y universo de candidatos/tuning para describir selección múltiple; percentiles/bandas y limitaciones, no prometer que un promedio backtest es forecast calibrado.
- Expectativas por régimen únicamente con definición reproducible y datos disponibles a tiempo; ausencia = UNKNOWN, no categoría inventada.
- `allowed_comparisons`, `unsupported_metrics`, `quality_flags`, `minimum_observation_policy_ref`, provenance de cálculos y `sealed_at`. Reference versus Forge no requiere que las fechas se superpongan, requiere condiciones comparables y forward verdaderamente posterior a selección.

**Evidence Gate:** inputs son Expectation exacta, enrollment, watermark/facts snapshot, edad/calendario/trades válidos, exposure coverage, DQ y criterios versionados. Outputs `INSUFFICIENT_EVIDENCE / VALIDATING / ELIGIBLE / WATCH / DEGRADED / QUARANTINED`, scope de mandato y expiry. Política estadística calibrada contra historia y posteriormente validada forward; no inventar thresholds a partir de los ejemplos 7/30/90d/6m. La preferencia owner 3–6 meses existe y debe convertirse en criterios explícitos, no degradarse a 50 trades por conveniencia de fecha.

**Falla no es una sola cosa:** pérdida compatible con la distribución esperada; degradación económica; cambio de régimen; falta de señales por desconexión; cambio de dataset/config; error de atribución; broker mala ejecución. Primero DQ/liveness/identity, después evaluación económica. Registrar abstención y causa. Una alarma de régimen V1 puede iniciar review, no necesariamente retirar.

**Captura mínima inmediata:** binario/params/version/magic binding, enrollment start UTC, Reference raw OPEN/MODIFY/CLOSE y broker IDs, timestamps servidor/evento/recibido/recorded y calidad de reloj, riesgo al OPEN/costs, heartbeat/session availability, instrument specs/calendar y cuenta/broker role. Además quotes/equity en exposición para DD intraday y MAE/MFE si se quieren usar en 2026. Conservar períodos sin trades y fallos: sin denominador de observación no se puede medir frequency decay.

**Version changes:** una reoptimización cambia la expectativa y puede reiniciar o segmentar evidencia. No combinar v1/v2 ni mover retrospectivamente el cutoff para mejorar el score. La Reference permanente permite seguir midiendo aunque una allocation real esté pausada; no apagarla por bajo PnL para maquillar supervivencia.

## 10. Analytics blueprint

### Contrato transversal de cálculo/publicación

**Fact:** observación con productor/identidad/event time/received time; no juicio. **Metric:** función de facts con unidades, window, sample y versión; no permiso. **Score:** transformación paramétrica de métricas y coverage; etiqueta de comparabilidad explícita. **Decision:** política aplicada a evidencia exacta, con outcome/reason/scope/efectos. Una view o cron puede calcular métricas; no debe ser el único sitio donde se decide allocation.

Todo snapshot nuevo que alimente Decisions fija `as_of`, `[from,to)`, event-time basis, input watermark/generation, eligible source cohort, observation coverage, formula/catalog version, currency/risk basis, parameter digest y exclusion reasons. Separar report calendar windows de rolling last-N trades. Una view latest puede servir navegación; la Decision persiste la referencia exacta, no el query que mañana devuelva otra fila.

**Current pitfalls S:** Lab usa tiempos recorded para curvas/duración/segments; 30D/90D se anclan al último close, no a hoy; risk policy se busca en fila mutable vigente según updated_at/valid_until; recompute borra scopes y repuebla en pasos separados. Esto permite congelar una “última ventana saludable”, cambiar DQ histórico al editar policy y exponer publicación parcial. Versionar salida/cutoff y publicar un generation pointer sólo cuando toda la generación esté completa. No modificar silenciosamente los dashboards históricos Lab Clean. [E02,E03,E19]

| Dominio | Raw sources y MetricSets | Ventanas / agregación | Score, warnings y Decisions | Read model / consumer |
|---|---|---|---|---|
| Factory | Flow/stage times+statuses, Campaign/Promotion, queue/admit/slot telemetry, artifact bytes, failures por reason | Cohort completo y por stage/type/build; waiting vs computing vs drain; produce→robust→physical→finalist | Yield, rerun cost y TIME_TO_QUERYABLE_FINALISTS; warnings de stalled/zero-supply; Campaign Stop sigue dueño | Factory overview, funnel denominators, Campaign result y capacity; owner/factory planner |
| Strategy | Reference outcomes por version/enrollment; R/net money, returns, PF, expectancy, DD, win/loss, holding, MAE/MFE si observado | N-trades y time windows; activo/inactivo; sesiones y total observation time; currency/risk consistent | Coverage no se llama edge; quality score opcional tras calibración; Eligibility/LiveValidation con abstención | Screener, detail curves, forward-vs-Expectation, evidencia de exclusiones; portfolio selector |
| Execution | Expected recipients, commands, ACK/deals, Reference+Execution facts | Trade 1, luego account/broker/symbol/policy/build/session tails | Vector fidelity, missing/extra; Broker/Assignment Pause/Quarantine | Execution comparison, broker diagnostics; operaciones/risk |
| Account | Broker snapshots, deals, cashflows/deposits/withdrawals, equity/margin/intraday HWM, positions | Trading day calendar y UTC; realized vs unrealized; since activation y daily limit period | Headroom, margin, exposure y rule coverage; AccountRisk/Kill decision | Watchtower/Daily Ops incluyendo actividad de cuentas hoy inactivas según vista; guard/owner |
| Broker / prop firm | Account facts + broker versions/specs/quotes + ruleset firmado/configurado | Por firma/servidor/cuenta/session/build y reset calendar | Fill reliability, fees, reject taxonomy; no mezclar rule breach con alpha; regla contractual versionada | Broker quality y constraint compliance; eligibility por destination |
| Portfolio | Miembros/versiones/riesgo asignado, series sincronizadas de retorno/equity, fills reales y exposure | Por PortfolioVersion, actual vs intended; rebalance intervals; rolling correlation y DD overlap | DD/exposure/correlation/headroom, turnover y drift; Selection/Rebalance/Replacement policies | Composition, version diff, risk attribution, counterfactual y audit de decisiones |
| Operations | Queue lag, Kafka offsets, input gaps, job watermarks, ETCD ownership, worker epochs, storage/checkpoint/release health | Latencia y freshness por boundary; ventana incidentes y soak | No score global verde; separar disponibilidade, correctness e integridad | Alertas accionables, dead letters, orphan work, repair effects; on-call |

### Reglas semánticas necesarias

- No sumar PnL de varias divisas como si fuera USD. V1 puede ser USD-only con rechazo explícito de otros scopes; ampliar FX requiere rates/cashflows/effective times y método de retorno.
- `profit_net = profit_gross + commission + swap` sigue correcciones 057/058; signos y units deben viajar. R de dinero y R de pips son bases distintas; no comparar sin marcar normalización. Capital virtual Lab no es account equity real.
- Drawdown de portfolio se calcula sobre **curva agregada sincronizada** y exposures, no promedio ponderado de max DD individuales (job portfolio legacy usa blend). Correlación de trades por ordinal no equivale a correlación por tiempo; días sin posición≠datos ausentes.
- Sharpe/Sortino sólo si frecuencia/annualization y retornos sincronizados están definidos; no sobre lista irregular de PnL por trade. PF indefinido por cero pérdidas no es 0 ni razón para admisión automática.
- DQ alto con retornos negativos no es edge alto; DQ bajo no es pérdida económica. Suprimir naming engañoso o declarar legacy en UI hasta versionar fórmulas.
- Roles/sources/cuentas/versiones deben estar en el dataset aunque el screener agregue por Strategy. Una estrategia en dos References duplicadas necesita enrollment canónico, no sumar dos veces la misma señal.
- Tiempos recorded son útiles para observabilidad y “lo sabido a T”; event-time validado es necesario para duración/mercado/régimen. Guardar ambos y el offset/uncertainty. MetaTrader distingue tiempo de servidor/local y el tester equipara relojes: verificar conversión específica, no restar tres horas globalmente. [Documentación MQL5](https://www.mql5.com/en/book/common/timing/timing_local_server)

### Publicación y APIs de lectura

Reusar `lab-worker` y funciones puras; agregar jobs versionados para Quality/Fidelity y adapters a `lab_*`, retirando los SQL legacy sólo después de migrar consumidores. PG basta para V1: no existe evidencia que justifique otro data warehouse. Publicación con `RUNNING/COMPLETE/FAILED`, generation/input digest, watermark y last successful generation; front marca stale/partial y Decision exige generación completa. Recompute idempotente con snapshot isolation o staging+swap; el borrado visible antes de repoblar no puede alimentar una rebalance.

Endpoints/read models mínimos: Registry/Version+receipt; FlowRun/Campaign exact; finalists/warnings/ranking separados; Reference enrollment coverage; per-trade pairing y missing grid; validation timeline; account risk/headroom; portfolio versions/allocations/effects; incidents/dead letters. Hasura puede servir estas proyecciones con role read-only; mutaciones de lifecycle deben pasar por servicio de dominio con invariantes.

## 11. Portfolio blueprint: de selección a operación

**Actual S:** dos dominios de portfolio existen. `echo.portfolios` agrupa cuentas para UI. `strategy_portfolios`, `strategy_portfolio_versions`, allocations y constraints de 039 son portfolios analíticos de estrategias. 040 propone fit y 041 dry-run dinámico; no hay prueba de que materialicen assignments/activation reales. La “inmutabilidad” de versión es un comentario SQL: Hasura permite actualizar weights y borrar versiones/allocations. Los jobs leen tablas eliminadas por 052. [E14,E15,E16]

**Target I:** Portfolio es un mandato versionado de estrategias y exposición sobre un conjunto explícito de cuentas, con constraints y objetivo; no sólo un set ni un deployment. PortfolioVersion es una selección/allocation aprobada inmutable. Su implementación física puede estar PARTIALLY_APPLIED aunque la decisión exista; no confundir intended portfolio con observed exposure.

| Concepto / interface | Inputs | Output durable e invariantes |
|---|---|---|
| Portfolio identity/mandate | Owner, universo Forex, cuentas, currency, objetivo, capacidad autorizada, rulesets | ID estable; mandato versionado. Reusar strategy_portfolios y extender contratos, sin convertir account groups |
| StrategyEligibility | StrategyVersion/Expectation + forward evidence + DQ/freshness + destino | Eligibility Decision con expiry y restricciones; no auto-admitir todo finalista o CANDIDATE del Lab |
| Candidate set | Receipts/versiones elegibles a cutoff, exclusions/reasons | Snapshot íntegro con elegibles y excluidos; control de survivorship/replay |
| Diversification | Family/derivation lineage, instrumentos/side/timeframe, exposures y series alineadas | Features/correlation con ventanas/min overlap/confianza. Bloquear unknown crítico o limitarlo; diez variantes no son diez fuentes independientes |
| Selection | Candidate snapshot + mandate + constraints + selection policy/version | Decision seleccionada con reasons y alternativas; algoritmo determinista simple V1 antes de optimizer avanzado |
| Risk allocation | Selected set + account equity/margin/headroom + ruleset + constraints globales | Importes/riesgo/exposure por strategy-account y reservas para in-flight commands. Normalized weight≠lote ni garantía de pérdida máxima |
| PortfolioVersion | Selection + Allocation refs, effective time, predecessor | Versión nueva inmutable; unique active intent por scope, CAS/preconditions. Draft puede editarse; published no |
| Provisioning | Versión aprobada, magic/version/EX5/params, assignments y cuenta | Effects ledger con intent/ACK/error; config aplicada y read-back. No marcar activo por POST 200 o copia de archivo |
| Activation | Todos los ACK/health/eligibility/risk gates vigentes | Activation Decision y efectos por cuenta; expected recipients para los trades posteriores |
| Rebalance | Clock/cambio material + new facts + policy + coste/turnover | Nueva versión y plan de transición; destino puede ser cash. Hysteresis/cooldown y límites de churn versionados |
| Replacement | Retirement/degradation + candidatos válidos + headroom | NO_REPLACEMENT, CASH o reemplazo con reason. No bajar Evidence Gate por falta de supply |
| Pause/retire | Diagnóstico causal/mandato | Scope strategy-version/account/broker/portfolio; new opens off, política de posiciones existentes separada |
| Audit | Decisions + facts + commands + physical acknowledgements | Replay de selección/asignación; explicación del estado y de effects parciales; ninguna dependencia de latest |

### Rebalance no es sustituir una lista

Secuencia V1: congelar snapshot→proponer N+1→validar constraints con facts frescos→reservar capacidad→bloquear opens de assignments salientes cuando corresponda→conciliar posiciones existentes→aplicar nuevas policies/bindings→ACK exactos→activar N+1→liberar reservas. Una falla entre pasos deja `PARTIALLY_APPLIED` y acciones compensatorias explícitas. No “rollback” un trade ejecutado borrando la fila o reaplicando N; ese efecto requiere cerrar/reducir o mantener exposición bajo una decisión distinta.

Evitar doble allocation cuando varias estrategias o portfolios comparten cuenta. El per-trade calculator actual no arbitra riesgo simultáneo: dos requests válidos pueden exceder headroom combinado. Una autoridad de reserva por cuenta y un guard en el punto de envío deben validar configuración/equity freshness; comprobación antes del enqueue solamente no evita la carrera. Separar reference sizing de real allocation. [I basada en E08,E09,E14]

La automatización mínima 2026 puede seleccionar determinísticamente candidatos elegibles con límites de familia/símbolo/exposición y equal-risk acotado por mandato, generar N+1 y manejar reducción/pausa/reemplazo. Optimización sofisticada de pesos, aprendizaje de regímenes y reoptimización continua de parámetros quedan SHOULD/POST; no sacrificar coherencia de versión ni risk safety para agregarlos.

## 12. Decision architecture y riesgo

**Delimitación V1 independiente:** PromotionRecord puede ser receipt+versión; baseline es un manifest; selección/allocation/rebalance quedan en PortfolioVersion y activation/pause en commands/transitions auditados. Sólo se separa entidad por lifecycle/autoridad/idempotencia independiente. La tabla amplia no obliga a un framework nuevo: [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan#7. Arquitectura simplificada y entidades]].

### Decisions existentes vs necesarias

| Decision | Estado actual | Nueva autoridad mínima |
|---|---|---|
| OPTIMIZER_SELECTION / FinalistPromotion | PG immutable en Forge [F07] | Mantener tipos; Promotion V2 additive/BWC |
| Campaign stop/replenishment | Policies/evaluations durables [F08] | Mantener target y max_waves, separar budget de concurrencia |
| Ingestion acceptance | API/receipt ausente | Receipt técnico de validación/idempotencia; no necesita Score/DecisionPolicy económica |
| Strategy live validation | Status/health analítico parcial [E03,E12] | Policy+Expectation+cutoff+evidence, verdict/uncertainty/expiry |
| Eligibility / degradation | No Decision domain encontrada | Eligibility por versión/mandato; degradation causa y scope; retirada no vive en SQL view |
| Portfolio selection / allocation | SQL recomendaciones y dry-run [E15] | Decisions separadas de portfolio metrics, con candidate snapshot/reasons |
| Activation / pause / retire | Config/state/actions actuales [E09] | Decisión y actor, approval/authorization context, expected effects, applied effects |
| Replacement / rebalance | Steps dry-run, no lifecycle operativo probado [E15] | N→N+1, no-op válido, recovery/compensation |
| Operador override/emergency | Endpoints/automation [E01,E09] | Registro inmutable de actor, scope, motivo, expiración, preconditions/result |

Envelope recomendado: `decision_id/type`, subject(s), previous version, policy ID/version/config digest, evidence refs+snapshot/input digest, as_of/watermark, outcome/reasons/uncertainty, author/actor, effective_at/expires_at, supersedes link y effect IDs. Echo no necesita forzar cada lookup/config read a “Decision”; usar el modelo sólo donde hay admisión, exposición, transición o responsabilidad material.

**Replay semántico:** verificar misma decisión con mismos inputs/código/policy; replay operativo es otra cosa y no debe reenviar órdenes. Read model reproduce el ledger. Auditoría debe distinguir `DECIDED` de `APPLIED`, `REJECTED`, `PARTIALLY_APPLIED`, `ABORTED` y `SUPERSEDED`.

### Riesgo: qué existe y qué falta

S: hay `FixedRiskConfig.Amount`, sizing por SL/tick value y comisión, min lot y settings por account/strategy; no aparece 2% como invariante de ese calculator. Hay account state/whitelist, automations de daily loss y rulesets. D: 2% del planteamiento es una configuración/hipótesis histórica, nunca se convierte aquí en regla universal. [E09]

| Scope | Actual | Gap V1 obligatorio |
|---|---|---|
| Per trade | Sizing/fixed risk/lot offsets/commission | Capturar policy y specs aplicados, freshness, reject si min lot excede budget, fill/slippage reconciliation |
| Strategy | Config por cuenta | Budget compartido por estrategia/version; exposures ya abiertos y comandos en vuelo |
| Account | Equity/margin/HWM/rulesets + alert/close automation | Reservas atómicas, guard pre-send y reconciliación; broker disconnect/currency/market-session; no asumir snapshot presente |
| Portfolio | Weights/constraints analíticas | Exposure real agregado, concentración/family/correlated risk, turnover, cash y conflictos interportfolio |
| Prop firm | Reglas configurables y daily loss evaluator | Semántica exacta por ruleset versionado: timezone/reset/DST, equity vs balance, trailing vs fixed, realised/unrealised/costs; evidencia de conformance por cuenta, no una regla universal |
| Broker execution | Errores y snapshots | Missing/extra/partial/ACK incierto, reject taxonomy y emergency close verificado |

El kill switch debe poder bloquear nuevas aperturas con prioridad sobre un rebalance y dejar cerrar/reconciliar posiciones. “Emergency close” requiere ACK y posterior comparación con broker: una llamada exitosa al Gateway no prueba cuenta plana. La indisponibilidad de analytics impide **nuevas decisiones de riesgo** con datos stale, pero no debe impedir reconciliación/cierres ni forzar liquidación global por defecto.

## 13. Operación, fiabilidad, capacidad y deuda de datos

### Capacidades probadas y límites

- Forge tiene lifecycle controller de admission/drain, Job Object Windows, Stager, parser allowlist, replay/physical smoke previos; conservarlos. B agrega ownership global, no sustituye lease local. En contrato no-TTL, partición sacrifica disponibilidad: no existe auto-takeover seguro gratuito. El producto debe observar y escalar OWNED_ELSEWHERE sin duplicar. [F10,D02,P01]
- Echo usa Kafka/StateFun; config production en repo declara AT_LEAST_ONCE, checkpoint cada 60s, dos checkpoints retenidos en path local. Mount/replicación externa y estado real de restore son U. No afirmar exactly-once de trades por usar Flink; side effect broker/PG exige idempotencia y conciliación propios. [E17]
- Journal errors pueden sólo loguearse y retornar nil. DB outage no obliga retry de mensaje con ese handler; DLQ/recovery durables no aparecen en ese path. P0 antes de autonomía y antes de confiar el calendario al sistema. [E10]
- EA conserva journals/maps/queue con CleanupOld(7) y omite cierres >7d. Retención de comando no debe borrar mapping de posición aún abierta ni hechos aún no reconciliados. Reinicio o desconexión prolongada requieren replay desde broker y reconciliación. [E07]
- Recompute Lab tiene delete/rebuild por scope, snapshots mutables y policy mutable; no publicar eso como evidencia inmutable de una Decision. Distinguir última generación completa de progreso y revisar crash entre delete/upsert. [E19]

### Arquitectura operacional mínima

| Subsistema | Contrato / certificación |
|---|---|
| Release/fleet | Manifest+SHA+SDK/schema/EA/parser compatibility; read-back de binarios activos, queues y epochs. Feature branch no crea release productivo; cert usa release única tras merge |
| Drain | Cerrar admisión, dejar terminar owned work; contar procesos físicos además de Activity counters; PENDING cutover sólo cuando resource free. Trabajo de meses exige capacidad de recambio y política explícita para parche urgente |
| Retry/reprocessing | Transient vs deterministic; operation ID/digest; receipt query tras timeout; durable DLQ con reason+source offset+payload ref; replay de hechos nunca implica replay de órdenes |
| Stuck/orphans | Diferenciar logical RUNNING con proceso muerto, proceso vivo con Activity terminal, HTM durable sin seal y seal con objeto missing. Repair por identidad exacta y evidencia, no scan por ModTime |
| Backup/DR | PG + Mongo + MinIO + ETCD ownership + Kafka/StateFun + EA local stores/config/version bindings; manifest de punto consistente o compensable; restore aislado y comparación de exposiciones con broker antes de opens |
| Artifact lifecycle | Retención por reachable evidence/active portfolio y audit horizon; no GC por edad de workflow. Integrity scrub y permisos; missing/auth/unavailable separados |
| Capacity | Logical cohort y budgets de negocio independientes de slots físicos. Admission queue, fairness, slots Ready/Busy/Quarantined, utilization/queue age, storage growth y cuotas; no reintroducir cap=slots como cardinalidad |
| Emergencia | Account/broker/strategy/portfolio scoped new-opens-off, close policy, ACK+broker snapshot; excepción operador con actor/razón; out-of-band recuperación documentada |
| Calendar ops | Market sessions, DST, reset prop, expiración demo/licencia/credenciales, rollover/swap/triple-swap, maintenance/reboot, vacaciones fin de año; captura/alarma antes del vencimiento |

### Indicadores y SLO

| Indicador | Uso |
|---|---|
| TIME_TO_QUERYABLE_FINALISTS | North Star factory; separar tiempo total vs cola/cómputo/seal/query y resultado zero-supply. No fijar una cota universal para backtests de meses |
| Finalist→receipt READY | SLI de frontera ingestión; retries/partial por cohort y freshness |
| Ingested→observed Reference / observed→eligible | Funnel; segundo incluye latencia estadística, no outage por defecto |
| Expected execution→observed outcome | SLI crítico por cuenta/broker con missing/extra y ACK ambiguity |
| Fact→journal durable / journal→complete analytics generation | SLI de integridad y freshness; gap de datos y delayed processing separados |
| Eligible→portfolio / version decided→applied | Funnel y latencia de reconciliación, no forzar uso si mandato no permite |
| Evidence coverage / clock quality / reference uptime | Gates de inferencia/eligibilidad; no promediar hasta ocultar cuenta rota |
| Ownership conflicts, stuck stages, DLQ age, unbacked refs, restore age | Operación accionable |

Fijar números de SLO sólo después de medir baseline y definir tolerancia del mandato. **Gates de correctness no negociables:** ningún double physical job por LogicalJobID; ninguna apertura sin autorización/policy vigente; ningún mismatch identity silently accepted; ninguna Decision basada en generación incompleta. Eso no equivale a prometer cero interrupciones de red.

## 14. Security / control assessment

**Verificación actual S:** `v3/gateway/internal/server.go` enruta close-positions, webhooks y admin/republish directamente mediante mux envuelto sólo en CORS. CORS sigue `*`. Búsqueda en handlers productivos no encontró middleware auth/jwt/token validator; auth de proxy externo es **U**, no se asume ausente o presente en deploy. `front/src/services/graphql/client.js` envía `x-hasura-admin-secret` tanto para acceso GraphQL como parte del modelo cliente; si ese secret está configurado en el browser, el usuario del browser lo obtiene. Metadata admin permite mutaciones de portfolio. [E01,E16]

**P0 actual confirmado por revisión independiente:** el bundle servido contiene un secret administrativo vigente, aceptado por Hasura; red interna alcanzable probada, exposición Internet U. No se probaron mutaciones. **Antes de capital y exposición de front:** authn/authz obligatorias por endpoint, actor/service identity y scopes; separar operador lectura, operador control y servicio de ingestión. El frontend READ/OBSERVE no porta admin secret. CORS restrictivo es complemento, no autenticación. Webhooks deben autenticar fuente y validar versión/idempotency/size. Revalidar en el punto de efecto: ocultar botón no es permiso.

Hay credenciales operacionales en documentación de repos inspeccionada; no se copian sus valores a este recurso. Clasificación S exposición en archivos, U de vigencia/explotación. Rotación/verificación de historial y reducción de permisos son trabajo S1/ops autorizado por una misión separada, no ejecutado aquí. No convertir el simple hecho de red privada en control de producción.

**Control de artefactos ejecutables:** validar EX5/params/build/source linkage, integridad de transferencia, permisos y destino; separar viewer VM/SQX GUI de flota de producción. Un artefacto íntegro criptográficamente puede ser el binario equivocado para esa StrategyVersion: verificar binding semántico además de SHA. Los agentes de coding no deben poder activar capital por tener permiso de publicar un build.

## 15. Debt register consolidado

El triage ejecutable y reachability por cada ID están en [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan#3. Gap Register V2 — todos los gaps materiales]]. Las etiquetas históricas siguientes describían severidad en el target unattended, no incidentes productivos actuales; no sumarlas como 32 blockers previos al primer uso. **P0** bloquea capital/autonomía; algunos bloquean también la calidad de la captura. **P1** bloquea producto/automación o recuperación; **P2** crecimiento/UX; **P3** limpieza. Disposición siempre aditiva/acotada salvo retiro de legacy ya probado sin lectores.

| ID / categoría | Evidencia y componente | Impacto actual → futuro | Bloquea | Disposición / cierre verificable |
|---|---|---|---|---|
| D-01 P0 data-loss | E10, TradeJournalFn handlers retornan nil tras SaveOpen/Close error | Puede faltar ledger pese a mensaje consumido → Decisions sesgadas y posiciones sin conciliación | M0,M3,M7 | Persist retry/DLQ/inbox; DB outage+replay sin duplicar ni perder hechos |
| D-02 P0 identity | E07/F03, `magic_*`, registry no implementado | Catálogo auto-provisionado no une Forge → forward no atribuible | M2,M4 | Canonical mapping+magic registry y alias legacy; Golden source→trade→source |
| D-03 gate identity / FUTURE_MIGRATION_RISK | E07, magic int en persistence MT5, override int4 | Truncamiento de estándar semántico >int32 → asociación incorrecta | M2 | Plumbing 64-bit entero y exactitud JSON/client; test+EA físico con valor >2^31 |
| D-04 P0 execution safety / CURRENT_PRODUCTION_REACHABLE | E01,E16 y evidencia independiente R03: secret servido y aceptado por Hasura | Control administrativo expuesto en red alcanzable → pause/close/republish/allocation sin scope | M0,M6,M7 | Auth/authz/roles/secret rotation y negativo físico contra endpoints |
| D-05 safety gate / CURRENT_REACHABLE; producción cross-host U | F10,D02, lease sólo local/Acquire por slot | Retry puede ocupar otro slot/host mientras owner vive | M1 | B CAS no-TTL+fencing+singleton; partición/retry/crash reales |
| D-06 P0 execution safety | E08/E09, ausencia config permite opens BWC; policy+snapshots asíncronos | Risk decisions con state ausente/stale → opens no autorizados | M3,M6 | Safety guard fail-closed para nuevo contrato; policy revision/expiry/freshness+ACK |
| D-07 P0 execution safety | E08,E17, at-least-once + comandos/side effects | ACK perdido/replay puede duplicar orden; idempotencia local no prueba atomicidad broker | M3,M7 | Failure injection entre fill/journal/ACK, reconciliar uncertain antes de retry |
| D-08 P0 operational data | E07, MAX_CLOSE_AGE_DAYS/CleanupOld(7) | Pérdida/rechazo de cierres viejos → journal/exposure fantasmas tras outage | M3,M7 | Retener open/unacked hasta reconciliación; restore tras >7d simulado |
| D-09 P0 risk aggregate | E09,E14; sizing local, sin reserva global observada | Órdenes simultáneas respetan riesgo individual pero exceden cuenta/portfolio | M6 | Reservation+headroom authority; dos opens concurrentes y carrera rebalance/kill |
| D-10 P0 identity-version | D01,E07: magic estable, eventos sin binding de StrategyVersion | Tras update no se sabe qué EA generó trade → calidad y replay falsos | M2,M4,M6 | Immutable binding/effective interval/ACK por posición; excluir simultaneidad ambigua |
| D-11 P1 semantics | F07, Promotion/Result TopProjection-bound | Finalista físico no comparable desaparece → supply vacío oculto | M1,M2 | C1+C2 V2, warnings no destructivos y structural requested-identity gate |
| D-12 P1 capacity | F10, WithTimeout sobre mt5.timeout y cap=4 | Cómputo sano aborta y backlog se interpreta como negocio | M1 | Long-running B, SQX D, cap superseded+BWC, budget separado |
| D-13 P1 capability | F04,E01,E04 | Ingestión sólo intent/stub → fábrica desconectada | M2 | API/receipt/refs/idempotencia/batch/auth/partial físicamente certificado |
| D-14 P1 capability/calendar | E12,D01 | No Expectation/enrollment auditable → diciembre sin ventana útil | M2,M4,M7 | Sellar expectativa y comenzar captura canónica ahora; no backfill ficticio |
| D-15 P1 semantics | E02,E19,D01 | recorded timeline, default LIVE, window anclada último close → drift/regime/frequency engañosos | M4,M5 | Analytics V2 con event/knowledge time, observation scope/cutoff y stale explicit |
| D-16 P1 authority | E09,E19; policy mutable buscada a closedAt | Recompute cambia DQ de historia → Decision irreproducible | M3,M4 | Sellar applied policy/risk al OPEN y archive de versiones; no policy “latest” |
| D-17 P1 analytics | E03 ComputeSubScores/ResolveStrategyStatus | Coverage llamado edge, status por count/time → selección de estrategia perdedora con alta DQ | M4,M5 | Renombrar legacy y DecisionPolicy explícita; separar cobertura de calidad |
| D-18 P1 integration | E05,E12,E15 | Jobs health/portfolio leen tablas que 052 elimina → features presentes en schema pero no operativas | M4,M5 | Port a Lab Clean con contrato correcto, inventario reader/writer y cert física |
| D-19 P1 publication | E19 recompute delete→upsert separado | Partial visible o crash elimina derivados → selección/alerta con cohort incompleto | M4,M6 | Generation publish atómico+watermark, injection después de delete/antes de publish |
| D-20 P1 pre-automation / FUTURE_MIGRATION_RISK | E14,E16; allocation UPDATE permitido | “Versión inmutable” editable → historia portfolio cambia | M5,M6 | Draft/published, immutable versions, domain mutation API+effect ledger |
| D-21 P1 fidelity | E11 INNER JOIN sin expected recipients | Sólo pares exitosos medidos → missing/extra invisibles | M3,M4 | Routing snapshot y pairing íntegro con unknown/partial |
| D-22 P1 portfolio maths | E15 weighted max-DD legacy | No representa DD de cartera → riesgo subestimado | M5 | Series temporal agregada, calendar/missingness/cashflows, comparación manual pequeña |
| D-23 P1 operations | F06 reconcile comentario RUNNING residual, P01 residuos históricos | Terminal lógico≠seal completo → queries bloqueadas/repair manual | M1,M7 | Reconciler por IDs y estados, dead-letter terminal; no blanket rerun |
| D-24 P1 DR | E17 file checkpoints; restore conjunto U | Backup aislado no garantiza posiciones/ownership consistentes | M0,M7 | Restore drill aislado PG/Mongo/MinIO/ETCD/EA/Kafka con broker read-back |
| D-25 P1 risk calendar | E09,E13,D01 | Rulesets/HWM no certifican prop conformance ni demo lifetime | M3,M7 | Capture reset/clock/specs, expiración demo/credenciales y ejercicios calendario |
| D-26 P1 evidence | F06/F09, artifact refs presentes; dataset exacto U | Repetir backtest no reproduce baseline si vendor history cambió | M2,M4 | Dataset/config/build provenance y niveles exact replay/recompute/new evaluation |
| D-27 P2 identity | E18 CanonicalTradeIDJournal safeSegment | Colisiones válidas bajo normalización → merge de canonical trades | M4 antes de ampliar IDs | Tuple hash/encoding inyectivo+BWC; dirigir caso adversarial, no backfill masivo |
| D-28 P2 capacity | F08 sin quotas unificadas observadas | Saturación por large cohorts/storage → tiempo a finalists y forward infra compiten | M1,M7 | Medir costo/capacidad y admisión; capacity independiente por factory/reference |
| D-29 P2 UX | E16 dual Lab/legacy + F07 CLI exacta | Front engaña por stale/rotura → operador usa señales incorrectas | M4,M7 | Read-only surfaces watermark/unknown y retire lectores rotos |
| D-30 P3 cleanup | F04/E05/verifications antiguas, application wiki desactualizada | Agente confunde intent con implementation → trabajo repetido | No critical path salvo efecto vivo | Entrypoints/links a este recurso, deprecations explícitas; no reescribir todo |
| D-31 gate identity/recovery / FUTURE_MIGRATION_RISK; crash actual U | E07, TradeMapRecord binario con int magic, FileWriteStruct y WriteAll con FILE_WRITE | Widening in-place o crash de escritura puede invalidar mappings → orphan/duplicate trade tras update | M2,M3,M7 | Versionar formato del archivo, migrador/readers compatibles, atomic replace/checksum y backup; cert restart con posiciones abiertas |
| D-32 P1 execution semantics | E07, extracción de historial agrega profit/costs pero asigna price/volume por deal de entrada/cierre | Multi-fill/netting no equivale a una pareja simple → pairing/volumen/price erróneos | M3,M4,M7 | Declarar account mode permitido, conservar deal facts y ponderación; hedging-only V1 si no se certifica netting/reversal |

Los P0 de riesgo broker no se “resuelven” ejecutando unit tests. Un harness puede probar determinismo/modelo; el gate incluye broker/EA físico, ACK perdido y reconstrucción de estado. El producto puede operar sólo en demo mientras esos gates estén abiertos.

## 16. Definition of Done 2026: bounded Product Complete V1

**Alcance revisado:** el mínimo propuesto y la escalera de uso están en el companion §5/§8; auto DEMO y REAL aprobada son niveles distintos. Este DoD amplio inicial no obliga a construir todas sus entidades separadamente ni a detener captura por analytics avanzada.

**MUST COMPLETE IN 2026** para declarar *plataforma integrada V1*: Forex, MT5-first, un operador, cuentas/destinos certificados y moneda base V1 definida; factory durable V2 con supply no vacío físicamente probado; ingestión idempotente; canonical Strategy/version/magic de punta a punta; Reference DEMO y mirrors persistentes; journal recuperable; Execution Fidelity desde trade 1; Expectation/forward/eligibility con abstención; analytics correctos y freshness; selección/allocation/portfolio versions; pause/rebalance/replacement o cash con razones; provisioning+activation con ACK y risk guard; auth/control/read-only front; alertas y restore drill. Todos los P0 cerrados en el scope habilitado.

**DoD física de plataforma:** una cohorte real producida por Forge y recibida en Echo; al menos una estrategia observada en Reference y una cuenta mirror con reverse provenance completo; decisiones sobre datasets sellados; una transición N→N+1 y un pause/recovery con zero unexpected opens/duplicates; fallo parcial y no replacement manejados; restauración aislada que reconstruye facts/Decisions/refs y compara estado broker; operador puede explicar cada estado desde UI+ledger.

**DoD de operación con capital:** adicional y no sustituible por lo anterior: candidatos cumplen Evidence Gate owner-approved con historia suficiente y comparable, cuenta/ruleset vigente físicamente certificado, mandate/capital autorizados y provisioning/risk/safety gates cerrados. Si no hay candidatos suficientes, la plataforma puede completar software con outcome CASH/INSUFFICIENT_EVIDENCE; **no declarar “robust dynamic live portfolio con dinero” ni “producto económico completo”**. La aceptación del alcance de plataforma versus cartera financiada es decisión owner O-01.

**SHOULD COMPLETE IN 2026:** familias+behavior features iniciales, correlación robusta con unknown handling, diagnóstico simple de régimen shadow, account/broker/portfolio views completas, SQX viewer pool en VM dedicada, alertas de renovación DEMO y tareas de reoptimización propuestas sin activation automática. Se convierten en MUST si el mandato real depende de ellas.

**POST-2026 / DEFERRED:** seis meses de forward de nuevas estrategias de septiembre; ML de régimen/optimizer dinámico sofisticado; múltiples propietarios/tenancy; Futures/cross-asset (proyecto separado según owner); UI editor de estrategias; GUI de reejecución completa; soporte MT4 al estándar magic 64-bit; FX multi-currency si V1 se acota a USD; auto-takeover MT5 no-TTL; reoptimización/autodeploy perpetuo sin nuevas validaciones. No usar “extensibilidad” para meter estas abstracciones ahora.

## 17. Roadmap ejecutable hasta diciembre

**Revisión de prioridad vigente:** [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan#9. Roadmap verdadero — siete hitos con valor]] reduce el mínimo de producto, incorpora evidencia actual/archivo histórico y clasifica gates por uso. La tabla amplia siguiente se conserva como mapa evolutivo inicial; no exige serializar todo ni construir cada Decision para V1.

**Plan I, no estimación comprometida de capacidad.** Ocho milestones con solapamiento. Fechas son ventanas objetivo y puntos de decisión; el owner no declaró throughput/equipo ni duración máxima de jobs. Una factory que necesita meses por job tiene critical path distinto: medirlo en M0/M1. El hilo de captura no espera a toda la UI ni a toda la factory.

| Hito / ventana objetivo | Goal y por qué existe | Autoridades de entrada → salida | Dependencias / contratos | Superficies de implementación | Certificación y producto usable / unblock |
|---|---|---|---|---|---|
| **M0 — Baseline, capture contract y safety gates**; 6–13 sep | Evitar otro roadmap sobre checkout/DB/EA distintos y comenzar reloj útil | Heads/actas/DB read-only/EA inventory/owner D01 → authority map vivo, dataset baseline, capture/enrollment contract, risk register priorizado | Sin dependency de FULL. TOP read-only precisa producción/clock/64-bit/policy; decisiones O-01/O-02 | Inventario scripts/gates, Gateway auth plan, journal recovery spec, telemetry/capture schema | Readiness exacta con gaps visibles; pruebas de no-mutación. Habilita implementación paralela, no capital. No usar “gate GO” falso si origin/policy siguen pendientes |
| **M1 — Reliable physical Factory V2 + Golden**; sep→oct, depende de cómputo | Corregir safety/semántica sin destruir cierre V1 | a10c26c + frozen B/C1/C2/D + fixtures/evidence → release única, three-slot cert, Promotion/Result V2, FULL con finalists | B ownership/long-running; C1 structural membership; C2 Campaign BWC; SQX D; source merge antes de release. Efecto actual cap=4 superseded | MT5 allocator/worker/process/lifecycle, Generic/reconcile/promotion/result/campaign, migrations additive, SQX timeouts | Matriz física §5 y V1 replay. Usable: supply queryable no vacío + costo/latencia observables. Unblocks integración final M2 y factory continuous supply |
| **M2 — Identity, ingestion y Reference enrollment**; contratos desde 6 sep, thin slice antes de 20–30 sep si supply permite | Iniciar forward atribuible y conectar dominios | StrategyRef/canonical/version + Promotion exacta + magic registry + Expectation → receipt/registry real/immutable binding+Reference enrollment | Contrato puede construirse con fixtures; cert requiere finalista físico válido. No necesita esperar UI/portfolios; no rebajar Promotion ni reconstruir identidad ficticia | SDK shared contract, Forge client/registry/stamping, Echo Gateway+PG, MT5 64-bit/mapping, provisioning ACK/runbook inicial, historical adapter | Full duplicate/conflict/partial matrix §6; physical >int32, EX5 sha read-back, trade canon y reverse provenance. Reference-only abre reloj; mirror agrega EF. Si se pierde sep, mover eligibility target |
| **M3 — Recoverable execution facts y risk controls**; sep→oct | Que captura/copias sobrevivan fallos y el guard proteja opens | Raw Reference/commands/deals/policies/Account specs → journal recuperable, expected routes, pairing base, applied policy/risk snapshots | M0 contract; comparte IDs de M2. No esperar 90 días. Auth antes de mutaciones remotas | Bridge/StateFun journal/planner/MM/EA journals, SDK repos/envelopes, DLQ/inbox, account guard/ACK/reconcile | DB outage, out-of-order CLOSE, duplicate, uncertain broker ACK, >7d restore, state absent/stale, kill/pre-send race. Usable: mirrors observables/recoverables; unblocks M4/M6 |
| **M4 — Analytics/Expectation/Validation V1**; sep→nov; evaluación económica hasta dic o después | Separar métricas, confianza y decisiones; no perder meses de evidencia | Published facts+Expectation+enrollment+clock quality → complete generations, EF/SQ read models, Validation/Eligibility Decisions | M2 IDs/capture, M3 facts readiness; lógica con fixtures ahora, cert forward por calendario. Legacy jobs no autoridad | Lab-worker/sdk formulas+PG jobs/schema, generation publication, expectation producer/adaptor, Decision store, Hasura views | Fixtures transparentes+recompute invariance; Reference-only; missing/extra; negative-PnL/high-DQ; clock delay; stale data; new version resets; rolling last-N/time. Usable: owner entiende calidad/ejecución y elegibles explícitos; M5 |
| **M5 — Portfolio construction y shadow**; oct→nov | Elegir conjunto/riesgo reproducible antes de mandar efectos | Candidate snapshot+eligibility+aligned curves+mandate/rulesets → Selection/Allocation Decisions y immutable PortfolioVersion | Interfaces desde M0/M2; shadow con synthetic/recorded fixtures; live eligibility depende M4. No optimizer sofisticado primero | Existing 039–041 evolve, Lab Clean adapters, family features, series correlation, risk reservations model, read-only diff | No eligible→cash, duplicate families, non-overlap, concentration, currency mismatch, weighted-DD counterexample, replay deterministic. Usable: portfolio propuesto/shadow; M6 |
| **M6 — Automated lifecycle con efectos controlados**; nov→primera mitad dic | Cerrar decide→provision→ACK→activate→monitor→replace/rebalance | M5 Decisions + fresh account state + authorization → applied N/N+1, effect ledger, pause/recovery | M3 safety/auth/reconciliation, M4 usable evidence, M5 version model; ninguna transición automática de capital sin gates | Echo domain API/worker orchestration, policies+EA bindings/read-back, reservations, event outbox/effect reconciler | Partial apply, crash mid-transition, reference good/broker bad, strategy degradation, stale metrics, candidate gone, shared-account conflict, kill priority. Usable: loop DEMO automático; capital sólo si DoD adicional |
| **M7 — Product certification, hardening y scope acceptance**; 1–31 dic con freeze antes del cierre | Validar enero unattended y declarar exactamente qué quedó usable | Todas las outputs + production inventory + forward age/coverage → certification manifest, runbooks/alerts/restore proof, declared supported scope | Empieza drills en sep; merge final M1–M6. Calendar Gate no se omite por fecha | Deployment matrices, operator control/read UI, backup/restore/replay tooling, evidence retention, telemetry/alert routing | End-to-end cohort y N→N+1 reales, crash/partition/restore, zero unknown exposure, no hidden manual step. Firma de scope; software puede PASS con eligible=0, cartera financiada NO_GO |

### Critical path y puntos de corte

```text
PATH FÍSICO: B ownership + C1/C2 + SQX D → release → slots/cancel/retry/drain cert → FULL no-vacío → M2 cert
PATH CALENDARIO: identidad + Expectation + verified enrollment → forward continuo 3–6m + N/coverage → Eligibility → live portfolio cert
PATH CONTROL: journal recovery + auth + policy snapshots + account guard/reservations → applied portfolio lifecycle → DR/soak
MERGE (todos los gates, sin bypass): M1/M2 facts + M3 safety + M4 eligibility + M5 selection → M6 effects → M7 aceptación
```

No priorizar tres meses de UI mientras el reloj forward está apagado. Si ya existe una finalista V1 válida, se puede habilitar su observación por contrato BWC; no presumir que existe (la Campaign certificada tuvo cero). Si no existe, M1 manda para nueva evidencia canónica. La captura de cohortes legacy empieza igual para EF/ops y sólo sirve para Quality canónica cuando se prueba retrospectivamente identidad/version/config/selection cutoff sin fabricar provenance.

**Gates de fecha:** antes de 30 sep, inventario de candidatos y fecha más temprana posible de eligibility; a fines de oct, retirar del MUST toda feature que no cierre un P0 o la integración mínima; a mediados de nov, si no hay M3/M5 demo cert, reducir alcance de automation a fail-safe pause + proposal/cash y declarar M6 incompleto; en dic, ninguna feature nueva sustituye cert/restore/soak. Si eso impide la definición aceptada de Product Complete, marcar NO_GO y no renombrar el recorte como completo.

## 18. Parallel workstream map

Paralelismo de trabajo diseñado para futuras misiones; esta auditoría no despachó subagentes ni inició implementación.

| Workstream | START NOW / estado | Blocked por | Inputs → outputs | CAN RUN IN PARALLEL / merge point |
|---|---|---|---|---|
| FORGE FACTORY | START NOW: B exacto; C1/C2/D con contratos congelados | Cert física espera merge/release; FULL espera safety | a10c26c+D02/D03 → release/cert/finalists | Coding mientras slots viejos computan; merge controlado en Generic/worker/SDK compartidos; M1→M2 |
| FORGE→ECHO INGESTION | START NOW: TOP boundary+fixtures+schema | Acceptance real espera manifest/finalista; auth/identity | Promotion+Strategy/version → receipt/API/client | Independiente de Windows; M2 |
| ECHO DOMAIN / LIFECYCLE | START NOW: registry/magic/64-bit/binding/receipts | Catálogo CC y contrato owner; ninguna espera por 3m | D01+schemas → mapping+version/state contracts | Coordinar SDK con ingestion; M2/M6 |
| EXECUTION FIDELITY | START NOW: expected routes/raw facts/recovery | Cert depende mirror/broker disponible; applied policy | Journal/commands/ACK → pairing/metrics | Capturar en mirrors mientras FULL corre; M3/M4 |
| STRATEGY QUALITY / LIVE VALIDATION | START NOW: Expectation/enrollment/capture | Eligibility calendar+trade count+DQ | Forge history+Reference → validation evidence/Decision | Ventanas corren mientras se desarrolla todo lo demás; M4→M5/M7 |
| ANALYTICS | START NOW: reader/writer map, formulas/generation/window contract | Semántica reloj y source scopes antes de publicar | Raw facts+catalog → trustworthy read models | Mocked sealed fixtures durante physical cert; M4 |
| PORTFOLIO | START NOW: domain/constraints/shadow interfaces | Applied risk waits M3; actual candidate set waits M4 | Eligible snapshot+mandate → Decision/version | No necesita workers SQX; M5→M6 |
| FRONT / READ MODELS | START NOW: read-only layouts/API contracts/watermarks | Real data wiring según M1–M5; admin secret removal antes de uso | Read models → visible state and drilldown | Usar fixtures, no crear nueva autoridad client-side; M7 |
| OPERATIONS / RELIABILITY | START NOW: inventory/backup/restore/auth/failure harness | Destructive drills sólo en ambiente autorizado; production cert final | runtime/config/DB manifest → recovery proof | Usar lab aislado, no consumir workers del Golden; M0/M3/M7 |

**Conflictos de integración:** B/D/C1 pueden tocar Generic/lifecycle; shared SDK ingestion/magic afecta ambos repos; analytics/portfolio comparten migraciones/read models. Asignar ownership por contrato y small merges; “paralelo” no autoriza cambios divergentes de los mismos tipos. Certificaciones MT5 no bloquean diseño Echo ni la observación Reference: pools/hosts separados para factory, viewer y live/reference.

## 19. Calendar-latency dependencies

| Capability | Latencia irreductible / límite conocido | MINIMUM DATA CAPTURE MUST START NOW | Qué se puede desarrollar después |
|---|---|---|---|
| Strategy Quality | D01: aproximadamente 3–6 meses + trade coverage. Desde 6 sep: 3m≈6 dic; 6m≈6 mar 2027. Desde 30 sep: 3m≈30 dic | Enrollment/identity/version/Expectation pre-forward, raw events/risk/costs/clocks y coverage de observación | UI, bands/DecisionPolicy calibrada, automation. Tiempo no suple falta de trades |
| Low-frequency strategies | N trades puede tardar más que 90d; depende de frecuencia real | No-trade observation intervals+sessions/heartbeat; no contar días offline como señales ausentes | Policy de mínimo efectivo; no asegurar eligibility por calendario |
| Broker Execution Fidelity | Hechos desde trade 1; tails y outages por broker/session necesitan exposición temporal | Expected recipients, ACK/deals, rejected/partial/missing, spread/spec/build/routing | Score/diagnósticos/UI; no extrapolar broker A→B ni DEMO→REAL sin evidencia |
| Account/prop limits | Reset diario, DST, fin de semana, rollover y drawdown intraday | Equity/margin/positions/HWM basis/ruleset+clock/reset timestamps; ledger de cashflows | Views/allocator. Boundary calendars se pueden simular ahora y luego observar |
| Régimen/correlación | Cobertura de regímenes/correlated drawdowns no se fabrica en semanas | Series alineadas con valid market data/gaps, family y exposures; expectation conditioning fijada | Modelos avanzados POST; ausencia de régimen futuro permanece incertidumbre |
| MAE/MFE/intraday risk | No reconstruibles exactamente desde trades cerrados | Quote path/equity/exposure sampling con rate/quality explícitos | Métricas y dashboard. Sin captura, declarar no disponible |
| Reoptimización/version drift | Nueva versión requiere nueva comparación/cohort | Hash EX5/params y activation/rollout intervals, binding al OPEN | Rotation policies; no reciclar evidencia de versión anterior como nueva |
| Reliability / restore | Soak y eventos raros; fin de año acorta disponibilidad operacional | Incidents, raw offsets, outcomes, retention metrics, restore manifests y demo expiries | Alert tuning, runbooks finales; drills pueden empezar antes de features |
| Long FULL MT5/SQX | Runtime depende de ticks/years/hardware y no tiene timeout de negocio | Duración/CPU/memory/storage/queue/slot/phase/build y progress facts no destructivos | Capacity model; no esperar a diciembre para descubrir que un backtest tarda meses |

**Conflicto material con horizonte:** con los datos disponibles no hay prueba de cohortes canónicas que ya lleven seis meses. Bajo exigencia estricta de seis meses para todas, **cartera financiada completa 2026 = NO**. Bajo rango owner de tres a seis y evidencia suficiente por tipo, **posible para la cohorte que se enrole en septiembre**, todavía no garantizado. El software de abstención/cash puede estar listo para el resto.

## 20. Next 30 days — 6 sep a 6 oct

| Periodo | CAN BUILD NOW | SHOULD AUDIT NOW | MUST START por calendario | CAN WAIT |
|---|---|---|---|---|
| 6–13 sep | B MT5; C1/C2 contrato/slices; ingestion shared schema; journal retry/DLQ design; auth boundary | M0 master↔DB↔EA inventory, clocks/risk/roles, magic registry/stamping, exposure y backups, readiness `origin` actual | Raw Reference/mirror captura y enrollment manifest; inventory real de candidatos y datasets | Optimizer portfolio, GUI viewer, editor |
| 14–20 sep | Registry/magic/64-bit/mapping, receipts, expected routes y applied-policy facts; source integration factory | Gate de identidad EX5/params, turnover de demos, no template placeholders; SQL legacy readers | Thin Reference canonical slice y un mirror por destino prioritario si hay candidate válido; fijar Expectation | Front de control/mutaciones, nueva tenancy |
| 21–27 sep | Factory release/cert slots + V2; FULL si gates pasan; canonical historical adapter; analytics generation/window V2 | Casos no comparables estructuralmente válidos vs mismatch; restore y replay isolated | Registrar fallos/sin-trades/currency/clock coverage; continuar demos aunque no haya score | Calibrar política “óptima” con pocos datos |
| 28 sep–6 oct | Ingestion Golden y forward read model; M3 pairing/failure recovery; portfolio shadow contract | Confirmar fecha eligibility más temprana y capacidad; reducir alcance si cohorte aún no inició | Report durable de coverage por enrollment y blockers; no iniciar reloj retroactivamente | Automatizar real allocation antes de risk/eligibility cert |

**Salida obligatoria a 6 oct:** gates y fallas conocidos por versión; factory V2 cerrada o blocker concreto con runtime estimado; al menos intento de Golden de ingestión con identidad verificada; captura canónica en marcha si supply existe; plan de eligibility basado en fechas reales; P0 owners técnicos y surfaces; portfolio/analytics contracts implementables. Si Reference no puede iniciar, priorizar reparar su causa por encima de nuevos features de factory/front.

## 21. KEEP FROZEN / SUPERSEDE / TOP REQUIRED

### KEEP FROZEN

- Foundation PG control + Mongo evidence + MinIO artifacts, sin retorno legacy/dual-path; refs tipados y write-once verify. La antigua autorización de overwrite intra-scope no autoriza sobrescribir artifacts durables actuales. [F02,F09,D04]
- Identity V2 global, GENERATED_STRATEGY / SINGLE_ENTITY: no nueva Strategy por `_robust` ni host al releer; FlowRun/stage/evaluation/version separados. [F01,D01]
- SQX un job físico por máquina; MT5 one worker process por máquina y one physical job por slot. No aplicar slots MT5 a databanks SQX. [D02]
- Build allowlist exacta 6090/6140/6180; unknown fail-closed/quarantine por slot. [F06,D02]
- Campaign Stop/Replenishment/Builder supply identity, zero-supply honesto, Result V1 histórico y replay. [F08,P01]
- Reference permanente y mirrors DEMO; SQ≠EF; eligibility≠deployment; canonical strategy única; magic estable con registry; MT5-first; Forex scope y Futures separado. [D01]
- Journal mínimo de facts: metrics/correlations fuera; native separado; no backfill cosmético de historia para ocultar lineage. [E10,D01]

### Contratos supersedidos, con historial/BWC

| PREVIOUS CONTRACT / por qué existía | NEW EVIDENCE → IMPACT | SUPERSEDED BY / RECOMMENDATION | BWC / HISTORICAL STATUS |
|---|---|---|---|
| FinalistPromotion V1 = TopProjection; materializar una selección rankeada | Period mismatch owner-válido da NOT_COMPARABLE y supply vacío; Result exige igualdad [F07,D03] | V2 structural membership; score/warnings/rank optional. Gate requested instrument/timeframe antes de ampliar cohort | Policy 1.0.0/output/result v1 legibles e inmutables; nuevos v2; Campaign nullable rank; no rewriting Decisions |
| MT5 one-job-per-machine; proteger instalación única | Portable slots independientes y backlog largo [F10,D02] | Slot pool V2 + singleton worker + compile/backtest mismo pool | SQX sigue serial; MT5 legacy single-slot sólo composición BWC, no permiso para duplication |
| Campaign hard cap 4 como safety | Cardinalidad de negocio≠capacidad física; slots/ownership la protegen [F08,F10,D02] | Quitar como safety al certificar V2; budget owner-configured separado | Históricos y snapshots conservan regla con la que se ejecutaron; no cambiar conteos pasados |
| mt5.timeout manda kill; corregía loop timeout infrastructure previo | FULL 6/6 mueren por cálculo sano de 45m [P02] | Long-running B; deprecación observable, heartbeat/cooperative cancel y finite technical horizon con recovery probado | Campos históricos se interpretan con contract version; no convertir un 45m viejo en nuevo budget sin versión |
| Lease local basta; simplificaba una sola instalación | Temporal retry puede despachar en otro host/slot sin muerte OS [F10,D02] | ETCD persistent CAS no-TTL global + local lease; V3 prohíbe takeover cross-host dentro de Symphony, incluso manual/admin. Fence externo y recuperación fuera de banda requieren operador | NORMAL A sigue PASS para exclusividad local; incompleto/superseded como garantía de flota; B original reemplazado |

### Challenges nuevos: EVIDENCE → IMPACT → ALTERNATIVE → RECOMMENDATION

| Challenge | Evidence → impact | Alternative → recommendation / estado |
|---|---|---|
| Lab recorded-time para toda analítica | E02/E19 + drift broker reportado: delay/replay mueve ventanas/duración y default LIVE | Conservar recorded para knowledge/freshness; nueva evaluación por event-time validado + clock uncertainty. **TOP requerido**, no cambiar historia silenciosamente |
| Fila policy actual como readiness histórica | E19 elige updated_at/valid_until; nueva policy puede invalidar trade antiguo | Capturar applied policy en OPEN/command y history append-only. Conservar lookup legacy sólo para legacy UI; **TOP M0/M3** |
| No nueva tabla deployments como simplificación | D01 accounts/policies bastan para binding operacional; E07 no version binding físico; automation necesita ACK/effects | Mantener cuentas/policies, agregar ledger de binding/activation facts con immutable version/EX5, sin imponer servicio/tabla deployments. **TOP de version attribution**, elección física de storage después |
| 3–6m vs Dec31 | D01 y calendario dejan 116 días; no cohorte 6m probada | Scope de plataforma y Gate por cohortes con evidence suficiente, restante POST. **Owner O-01**, no reducir umbral en secreto |
| Mínimo journal con errores absorbidos | E10 pierde oportunidad de replay si DB falla, estructura mínima no cubre raw evidence | Conservar journal mínimo; raw inbox/DLQ+recovery aparte, no añadir derivadas al ledger. **TOP failure semantics** |
| EdgeScore=coverage e “inmutabilidad” de portfolio declarativa | E03/E14/E16 permiten mala interpretación y mutación de historia | Versionar nombres/policy y publication state; domain mutation + immutable published versions. **M4/M5 requerido** |
| Broad “unattended” con ETCD no-TTL | D02 prohíbe auto-takeover seguro; un host perdido deja ownership bloqueado | Preservar safety y alerts; V3 exige fence externo y recuperación fuera de banda, sin takeover API/manual dentro de Symphony. No prometer cero intervención bajo particiones; futura TOP sólo si owner exige failover automático |

## 22. Owner decisions genuinely requiring input

No se pide decidir de nuevo CAS/slots/finalist V2 ni cuestiones que source ya resolvió. Estas opciones son de producto/mandato; su implementación se diseña en TOP.

| ID / DECISION | WHY NOW | OPTIONS / TRADEOFF | RECOMMENDATION |
|---|---|---|---|
| O-01 — Qué aceptación 2026 se exige | Calendar path manda hoy | Plataforma integrada gateada vs cartera financiada validada; si seis meses estrictos para nuevas cohortes, mover objetivo económico a 2027 | Aceptar dos gates separados; plataforma 2026 y dinero sólo por elegibilidad real, sin maquillar NO_GO |
| O-02 — Mandato V1, cuentas/destinos, moneda y capital autorizado | Risk/prop/fidelity requieren scope concreto | USD + destinos MT5 certificados acotados vs varias divisas/brokers/prop rulesets simultáneos; breadth aumenta cert/capture | Un mandato pequeño y explícito; preservar Forex/MT5-first; no inventar porcentajes/umbrales |
| O-03 — Evidence Gate por cohorte/familia | Debe saberse si 3m bastan para alguna familia; no calibrar ex post | Rango 3–6m con mínimo trades/coverage vs seis meses para todo; prudencia versus fecha | Fijar requisitos antes de mirar forward y admitir INSUFFICIENT_EVIDENCE; seis meses nuevos se difieren |
| O-04 — Grado de autonomía y respuesta ante degradación | M6 necesita saber efectos permitidos | Proponer/manual approval; auto-pause/reduce; auto-replace/rebalance dentro de mandato | Auto-protección y cash por defecto; replacement sólo con candidato/mandato válidos, todo durable y con override auditado |
| O-05 — Posiciones existentes al pause/retire | Pausa y liquidación tienen coste/riesgo distinto | Mantener hasta salida de estrategia, cerrar ordenadamente, emergencia inmediata por safety | Separar económico de safety; definir por mandato y prop ruleset; no hacer cierre global implícito |
| O-06 — Presupuesto y capacidad | Backtests sin deadline pueden ocupar flota meses; capture no debe competir | Límite de admisión/coste/storage y spare host vs financiar más slots/hosts | Reservar capacidad Reference/mirrors independiente y budget de admisión; jamás convertir N slots en N finalistas |
| O-07 — Catálogo CC de magic semántico | El estándar ya fue elegido; faltan códigos canónicos | Ratificar catálogo de símbolos/overflow rules; cambiar estándar reabre freeze | Mantener `YYMMCCQQQQ`+registry único; resolver catálogo y validar 64-bit; no parsing de magic como identidad |
| O-08 — Política de evidencia/operación legacy | Readiness origin/policy y cohortes `magic_*` afectan confianza | Mantener visible y excluido de canonical Quality vs migración certificada con provenance | Mantener historia visible/alias; migrar sólo si correspondencia exacta se prueba. Daily Ops debe poder mostrar actividad real aunque account deje ACTIVE |

Gateway endurecido vs servicio de ingestión independiente es una recomendación arquitectónica que puede cerrar el TOP con evidencia; sólo requiere owner si cambia superficie de exposición, operación o presupuesto. Naming NATIVE/MANUAL y limpieza UI no bloquean el critical path.

## 23. NEXT EXACT

1. **Siguiente del critical path físico vigente:** `ECHO-FORGE-MT5-LONG-RUNNING-GLOBAL-OWNERSHIP-RETRY-DRAIN-V2-NORMAL-B1`, después de revalidar HEAD/contrato; TOP V2 cerró como diseño y V3 supersede takeover/cancelación, con B1 y B2 pendientes. Ver [[2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3]]. No repetir esa TOP ni correr otro FULL antes de B+C1/C2/D+release/cert. El preflight TradeList reportado está resuelto; verificar sus exact refs si otra misión lo necesita, no volver al adapter legacy por un cero en `trade_lists`.
2. **Mejor workstream independiente inmediato:** `ECHO-CANONICAL-REFERENCE-ENROLLMENT-AND-FORWARD-CAPTURE-V1-TOP`, cubriendo magic 64-bit→canonical/version binding, Expectation+enrollment y raw evidence recovery. Luego NORMAL fino de captura/atribución; su objetivo es comenzar calendario, no construir todo Analytics.
3. **TOP que más reduce incertidumbre sistémica:** `ECHO-FORGE-TO-ECHO-BOUNDARY-AND-LIVE-AUTHORITY-V1-TOP`: inspección read-only production de schema/gate/EA/Hasura/proxy, dueño Echo/API/auth, contratos receipt/identity/version/magic/Expectation, modelo Reference real, risk policy history y expected routes. Entrega schemas/interfaces/error matrix/cert plan cerrados; no reabrir Foundation.
4. **Qué NO trabajar todavía:** allocator matemático sofisticado, UI editor, tenancy, Futures, ranking fidelity para admisión, nuevo big-bang de persistencia, live real autodeploy sin gates, auto-takeover ETCD o otro FULL bajo timeout/cap viejo. Esos trabajos no eliminan hoy la falta de identidad/forward/safety.

## 24. Segunda pasada adversarial — enero 2027, dinero y sistema unattended

**Método:** después de construir arquitectura/roadmap, revisar la cadena desde los efectos económicos hacia atrás, suponiendo particiones, restore, cambio de versión, datos incompletos y operador ausente. Los siguientes hallazgos se incorporaron a los gates de M0–M7 y al debt register; no son una lista genérica para “ver después”. Son escenarios I excepto source marcado.

| Escenario / fallo que un primer roadmap de features puede omitir | Brecha concreta | Revisión aplicada al plan |
|---|---|---|
| Misma Strategy/magic, v1 mantiene posición y v2 ya genera señales | Magic estable no identifica versión, strategy_id tampoco [D01,E07] | M2 exige binding al OPEN y artifact/params; M6 drena/segmenta versiones y prohíbe overlap ambiguo por cuenta |
| Fix magic 64-bit despliega un struct nuevo sobre el archivo binario anterior | FileRead/WriteStruct depende del layout; “cambiar int a long” no es migración BWC [S E07] | Agregado D-31: M2 exige formato versionado+conversión validada; M7 reinicia con posiciones abiertas y mappings previos |
| Cuenta MT5 netting mezcla dos estrategias del mismo símbolo o hay fills múltiples | Extraction de deals conserva agregados pero price/volume por asignación, y magic no arbitra exposición compartida [S E07] | Agregado D-32: M3 define modo soportado y deal-level attribution; M7 excluye netting del scope hasta cert específica |
| Broker ejecuta, proceso cae antes del ACK local | Retry de command puede crear segunda posición, tests idempotentes normales no lo prueban | M3/M7 injectan caída en frontera fill/ACK y concilian con deals; “unknown” bloquea resend ciego |
| CLOSE llega antes que OPEN por tópicos independientes | Journal rechaza y absorbe; NATIVE synthesis no cubre Reference [E08,E10] | M3 añade pending/quarantine durable/replay con hechos; no basta ordenar por trade_id dentro de un tópico |
| Dos portfolios reservan el mismo headroom | Sizing por trade y weight sum no coordinan cuenta [E09,E14] | M6 requiere una autoridad de reservas por cuenta, in-flight exposure y serialización de activation |
| Publicación Lab cae después de delete | Datos vacíos parecen degradación o candidatos desaparecidos [E19] | M4 generation swap y M6 no decide sobre parcial/stale; mantiene última completa con watermark visible |
| Última trade ocurrió hace meses pero snapshot 30D sigue verde | Ventana actual anclada maxClosedAt [E03] | M4 as_of real y coverage de observación/no-signal; estrategia quieta vs collector offline distinguibles |
| Portfolio PnL luce bien, prop equity intraday viola límite | Sólo closes/curva virtual no observan floating drawdown | M0 captura intraday, M3 rule clock/guard y M5 allocation por headroom; no usar DD ponderado |
| Factory offline o todos los candidatos se degradan juntos | Automatización “siempre reemplaza” necesita supply inexistente | M5/M6 NO_REPLACEMENT/CASH; factory falta no relaja Quality ni crea finalist dummy |
| Nuevo broker/régimen no visto se trata como cubierto | EF DEMO A no certifica cuenta REAL B ni régimen futuro | M4/M7 coverage por destino/versión/mandato y UNKNOWN; no transferir certificados por nombre de broker |
| Reference DEMO expira o deja de emitir durante semanas | No-trades puede confundirse con decay, evidencia futura irrecuperable | M0 enrollment+uptime, M7 renewal calendar/capacity; mirrors y reference independientes de factory maintenance |
| Restore PG a ayer, Mongo/MinIO a hoy, ETCD ownership distinto | Domain refs resuelven parcialmente; se podría reactivar versión vieja o duplicar MT5 | M7 restore conjunto + deny new opens hasta broker reconciliation; no borrar CAS no-TTL sin probar muerte |
| Misma Reference capturada por dos collectors | Dos UUID distintos son dos trades válidos sintácticamente, duplican Quality/routing | M2 enrollment/single active observation binding, duplicate source account/position detection; no arreglar sólo UNIQUE trade_id |
| Imported backtest aparece como LIVE por default segment | Puede aparentar meses de forward y pasar gate [E04,E19] | M2 source semantics y M4 explicit enrollment/cutoff; imports jamais LIVE por default; no aceptar flags insuficientes como autorización |
| Reoptimize mirando forward y luego reutilizarlo como OOS | Sesgo de selección, aunque todos los digests sean correctos | Expectation sealed_at y selection cutoff; nueva versión/revalidation; M4 candidate history, no “best retrospective window” |
| Job de meses impide desplegar parche urgente | Drain frozen espera fin; seguridad y disponibilidad compiten | M1/M7 spare capacity y patch policy con cancel explícito si owner lo decide; no deadline encubierto por deploy |
| Kill switch compite con activation/rebalance | Una policy retrasada puede reabrir cuenta pausada | M6 fencing/revision monotónica y prioridad del safety state; ACK viejo no reactiva nuevo state |

### Matriz causal de degradación requerida

| Observación | Clasificación correcta | Respuesta V1 |
|---|---|---|
| Finalista no puede ingresar | Boundary/infra/contract, no mala Strategy | Retry o reject técnico con receipt/reason; conservar finalist |
| Duplicate ingest / Strategy twice | Redelivery vs identity conflict | ACK mismo receipt; conflicto mismo key/distinto digest; no nueva Strategy |
| Reference sin Execution | NOT_REQUESTED vs PENDING/MISSING/REJECTED según routing snapshot | Investigar transporte/broker; no bajar Quality |
| Execution sin Reference | Extra u orphan evidence, quizá Reference delayed | Suspender nuevos efectos del scope si safety; reconcile antes de atribuir |
| Broker disconnect/account disabled | Operational/routing state | No opens nuevos; preservar órdenes en vuelo y reconciliar; clocks de observación marcan gap |
| Reference pierde y Execution reproduce fielmente | Strategy Quality/regime, no EF mala | Evaluación por Expectation; policy puede reducir/pausar; no umbral inventado |
| Reference healthy y Execution empeora | EF/broker/policy issue | Aislar account/broker/assignment; mantener Reference y candidata |
| Correlation spikes/member retired | Portfolio constraint change | Nueva versión/risk; cash si no replacement válido |
| Regime change con poca evidencia | UNKNOWN/diagnóstico, no predicción automática fiable | Shadow/review o exposure cap de mandato |
| Factory offline | Supply availability | Operar mandato existente si seguro; no depender de factory para cerrar posiciones |
| Echo offline/metrics delayed | Freshness/execution safety | EA broker risk protections + reconcile al volver; no rebalance con stale analytics |

## Límites y contradicciones

En la auditoría inicial no se corrieron workflows, backtests ni queries productivas. La revisión independiente posterior sí ejecutó lecturas de Echo/Hasura/PG, metadata, binarios y logs; ver [[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]]. No hizo mutaciones productivas ni nuevas certificaciones físicas. La evidencia P del vault está fechada y preserva IDs; su runtime actual requiere M0. Se inspeccionaron contratos/rutas/call paths críticos y tests focales, no una prueba exhaustiva de todos los archivos de siete repos. “MISSING” significa ausencia en el camino activo inspeccionado, con alcance de búsqueda explícito; schemas con nombre prometedor se clasificaron PARTIAL si faltaba productor/certificación.

La revisión de source posterior al primer roadmap agregó dos gates: migración del formato binario EA al ampliar magic y account mode/fill attribution (D-31/D-32). También confirmó que `SnapshotsRepo.ReplaceByScope` sí tiene transacción local; D-19 se refiere a la publicación multietapa/cross-scope de recompute y no acusa a ese reemplazo individual de carecer de transacción. EA sí aplica `ConfigAllowsOpens` y whitelist antes de OrderSend; D-06 exige freshness/versión coherentes, no ignora esa protección existente.

La Resource Wiki de aplicaciones decía entrega por API y un invariante genérico one-VM-one-job; son descripciones históricas que no prueban ingestión ni impiden la excepción MT5 ya frozen. Los VERIFICATION antiguos de Foundation/scoring contienen estados de slices anteriores; actual source/cutovers y actas posteriores prevalecen. El checkout habitual de Echo estaba stale; esta nota usa el master remoto `04c16bd`. No se corrigieron en silencio proyectos ni contratos frozen.

“Producto completo” no elimina intervención de excepción: ETCD no-TTL prohíbe takeover automático inseguro y el capital necesita mandato humano inicial. Si se exige literalmente cero intervención ante partición, seis meses de todas las nuevas estrategias y todos los brokers, el resultado 2026 es NO; el recorte V1 de §16 debe ser aceptado explícitamente. Ningún valor cuantitativo propuesto aquí es consejo de asignación financiera o regla nueva de prop firm.

## Evidencia y provenance

Fuentes canónicas de esta síntesis: [[Echo — Fuentes de arquitectura y producto 2026-09-06]] y [[Echo Forge — Fuentes de arquitectura y producto 2026-09-06]]. Los locators siguientes son relativos al repo y a los commits de §1; se conservan símbolos/migraciones para recuperar la evidencia sin depender de líneas que cambian. La navegación del workspace se resuelve mediante [[echo-go-workspace]].

### Source ledger — Forge

| ID | Repositorio + path / símbolo | Qué respalda |
|---|---|---|
| F01 | `xKoRx/symphony`: `sqx/core/domain/persistence_identity.go` (`NewFlowRunIdentity`, `NewStageExecutionIdentity`); `sqx/adapters/registry-postgres/adopt_strategy.go` (`upsertStrategyV2`); migrations `005_strategy_identity_versioned_uniqueness`, `006_strategy_identity_v2` | Strategy/Flow/stage identidades diferentes, uniqueness V2 global y BWC |
| F02 | `sqx/adapters/registry-postgres/migrations/001_durable_persistence_foundation.up.sql`, `007_output_namespace_ownership.up.sql`, `008_stage_producer_outputs.up.sql`; `sqx/adapters/metadata-mongo/evidence_store.go` (`NewEvidenceStore`, `PutEvaluation/MetricSet/TradeSet/Score`); `evidence_documents.go`, `evidence_indexes.go` | PG control; Mongo immutable majority+journal + primary/majority reads; refs/producer seals |
| F03 | `sqx/workflows/generic_workflow.go`; `sqx/activities/worker/durable_apply_selected_run.go`, `durable_select_robust_run.go`; `sqx/adapters/apply-selected-run/binding/contract.go` (`EffectiveConfig`); `sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeRobustRunExporter.java` | Pipeline activo/Apply typed magic requerido; fallback Java histórico no suficiente para atribuir defecto al durable |
| F04 | `specs/FEAT-SQX-ECHO-INGESTION/SPEC.md`; `sqx/core/adaptive/contracts.go`; `sqx/workflows/adaptive_workflow.go`, `adaptive_mocks_test.go`; búsqueda productiva `ActEchoIngest/EchoIngest` | Ingestión conceptual bloqueada, callsite/mocks no adapter real; SPEC drift de deviation/identity |
| F05 | `sqx/core/classification/classification.go` (`BuildSignature`, `ClassifyAndRank`, `groupBySignature`); `sqx/activities/worker/classification_snapshot_activity.go`; `sqx/core/domain/classification_snapshot.go`, `ranking_snapshot*.go`; Mongo classification/ranking stores | Clasificación y rankings durables, firma lógica no familia económica |
| F06 | `sqx/activities/worker/mt5_reconcile_activity.go` (`Execute`); `mt5_score_shadow_activity.go`; `sqx/adapters/mt5/report/parse.go`, `crosscheck.go`; `normalization/`; `binding/reretester_baseline.go`; `sqx/core/evaluation/`; `sqx/adapters/mt5/scoring/score.go` | Parser/normalización/reconcile, typed refs, Scope/baseline, comparability/fidelity, potencial RUNNING residual |
| F07 | `sqx/activities/worker/rank_snapshot_activity.go` (`validatePromotionSnapshot`, `buildFinalistPromotionDecision`, `promotionFinalists`); `sqx/core/forge/result.go` (`parsePromotionConfig`, `crossCheckPromotion`); `sqx/adapters/registry-postgres/decision_store.go`; migrations 004,009,010 | Promotion V1 ranking-bound, durable Decisions y read surface exacta |
| F08 | `sqx/core/domain/forge_campaign.go`; `sqx/workflows/forge_campaign_workflow.go`; `sqx/core/forge/campaign_result.go`; `sqx/adapters/registry-postgres/forge_campaign*.go`; migrations 011–013; `generic_workflow.go` (`MaxCampaignMT5BacktestChildrenPerGeneric`) | Stop target/max_waves, replenishment, identities, hard-cap actual 4 |
| F09 | `sqx/adapters/storage-minio/durable_artifacts.go` (`VerifyArtifactStream`, `ProbeDurableArtifact`, `FetchDurableToPath`); `sqx/adapters/storage-minio/artifact_store.go`; SDK MinIO write-once contrato; `sqx/core/domain/artifact_paths.go` | Size/SHA, exact key, immutable refs, no ETag como identidad; missing vs transport |
| F10 | `sqx/adapters/mt5/slot.go` (`LogicalJobIdentity.LogicalJobID`), `slot_allocator.go` (`Acquire`, `Release`); `artifact_runner.go` (`Backtest`, `context.WithTimeout`); `sqx/adapters/cmd-executor/process_windows.go`; `sqx/core/lifecycle/controller.go`; `sqx/workflows/mt5_artifact_workflow.go`; `sqx/cmd/sqx-mt5-worker/main.go` | Pool local, identity sin attempt/slot, timeout killer vigente, OS lifecycle y límites de safety |

### Source ledger — Echo

Todos los paths E corresponden a `xKoRx/echo@04c16bd2bd7b69725560873950a5d6b067fd3a4f`.

| ID | Path / símbolo | Qué respalda |
|---|---|---|
| E01 | `v3/gateway/internal/server.go` (`NewServer`, `corsMiddleware`), `close_handler.go`, `republish_handler.go`; búsqueda auth productiva en gateway | Rutas reales; sin ingestion ni auth propia encontrada; CORS `*` |
| E02 | `v3/lab-worker/internal/builders/recompute.go` (`recomputeOneStrategy`, `journalRowToCanonical`, `canonicalToOutcome`); `repo/canonical_repo.go` (`ListReferenceJournalCanonical`); `repo/trade_journal_lab_repo.go`; migration 046 | Lab canónico/outcomes Reference-only, recorded timeline y dataquality |
| E03 | `v3/sdk/lab/metrics/metrics.go` (`ComputeStrategySnapshot`, `ComputeSubScores`, `ResolveStrategyStatus`); `v3/lab-worker/internal/builders/materialize_snapshots.go` (`snapshotWindowsFor`) | R/money, coverage como edge, thresholds actuales y maxClosedAt window |
| E04 | `v3/lab-worker/internal/jobs/ingest_canonical_imports_stub.go` (`RunIngestCanonicalImportsStub`); migration 046 (`lab_import_*`) | Import schema no equivale a ingestion histórica ejecutada |
| E05 | `v3/sdk/postgres/migrations/052_drop_strategy_analytics_v3_legacy.up.sql` | Drop de outcomes/snapshots/virtual-equity legacy y readers parciales |
| E06 | `v3/sdk/postgres/migrations/001_schema_baseline.up.sql` (`strategy_definitions`, `accounts`, policies); `trade_journal_repository.go` (`ensureJournalParentRows`) | Descriptores sin lifecycle, varchar(64), FK autoparents BOTH/M1, multiple writers |
| E07 | `v3/clients/mt5/reference_v3.mq5` (`GetEffectiveStrategyID`); `execution_agent_v3.mq5` (ExecuteOrder handler, MAX_CLOSE_AGE_DAYS, CleanupOld y deal extraction); `EchoPersistence.mqh` (`TradeMapRecord`, `TradeMapper.WriteAll`); baseline magic_number_override int4 | Magic/string identity, persistence int32/layout, local idempotencia, TTL recovery y fill semantics |
| E08 | `v3/sdk/domain/reference_event.go` (`ReferenceEvent`, `NewCalculateRiskReq`, `CoreCommand`); `v3/bridge/internal/reference_pipe_handler.go`; `v3/core/internal/functions/execution_planner.go`; `v3/core/deploy/flink-statefun/production/module.yaml` | ReferenceEvent/trade_intent alias, fanout, expected-route ausencia durable observada, tópicos separados |
| E09 | `v3/sdk/domain/execution_policy.go`; `v3/sdk/mm/fixed_risk.go`; `v3/sdk/postgres/execution_policies_repository.go`; `v3/core/internal/functions/mm_engine.go`, `execution_planner.go`; `v3/core/internal/automation/evaluator.go` | Sizing por risk amount, cache/valid_until, broker fallback condicionado, state/whitelist, daily loss evaluator |
| E10 | `v3/core/internal/functions/trade_journal.go` (`handleReferenceOpenWithTelemetry`, `handleExecutionCloseWithTelemetry`, error handlers); `v3/sdk/postgres/trade_journal_open.go`, `trade_journal_close.go`, `trade_journal_repository.go`; `v3/sdk/domain/trade_journal.go`; migrations 043/045/057/060 | Fact merge/conflict/unique, errors retornan nil en handlers, NATIVE synthesis, event/recorded y net-profit |
| E11 | `v3/sdk/postgres/migrations/043_trade_journal_canonical_minimal.up.sql` (`v_trade_execution_delta`, línea 330 al corte; funciones de pairing/KPIs); migration 034 | INNER JOIN, dimensiones/deltas realmente calculados; missing/extra no cubiertos por esa view |
| E12 | `v3/sdk/postgres/migrations/038_strategy_live_health_v1.up.sql`; `v3/sdk/postgres/jobs/live_health_v1.sql` | Historical/live adyacentes; dependency a strategy_reference_outcomes; no Expectation Forge |
| E13 | `v3/sdk/postgres/jobs/account_lab_v1.sql`; migrations 036/037/056; `v3/core/internal/functions/account_sync.go`; automation evaluator | Account analytics y daily HWM; boundaries reales a certificar |
| E14 | baseline `portfolios/portfolio_accounts`; `v3/sdk/postgres/migrations/039_portfolio_lab_manual_v1.up.sql` | Dos portfolios distintos, versiones/allocations/constraints analíticas; sum weights trigger |
| E15 | `v3/sdk/postgres/migrations/040_portfolio_fit_assisted_v1.up.sql`, `041_portfolio_dynamic_dryrun_v1.up.sql`; jobs `portfolio_lab_v1.sql`, `portfolio_fit_v1.sql`, `portfolio_dynamic_dryrun_v1.sql` | Fit/dry-run implementados SQL; weighted DD y dependencies retiradas; no actuator live probado |
| E16 | `v3/front/src/router/index.js`; `services/graphql/client.js`, `strategyLabClean.js`, `portfolioLabV3.js`, `journal.js`; `lens/providers/strategyLabCleanProvider.js`, `strategyLensProvider.js`; `v3/hasura/metadata/tables/strategy_portfolio_lab.yaml`, `lab_clean.yaml` | Front/Hasura actual, cliente admin secret, weights mutable, dual readers |
| E17 | `v3/core/deploy/flink-statefun/production/flink-conf.yaml` y `module.yaml` | AT_LEAST_ONCE/checkpoint/local paths/restart y tópicos reales del repo; deploy vivo U |
| E18 | `v3/sdk/lab/ids/ids.go` (`safeSegment`, `CanonicalTradeIDJournal`, `CanonicalTradeIDImport`) | Canonical ID no inyectivo e import batch/row identity |
| E19 | `v3/sdk/lab/segments/segments.go`; `lab/riskpolicy/riskpolicy.go`; `v3/lab-worker/internal/repo/snapshots_segments.go` (`ReplaceByScope`, risk/segment repos); `builders/recompute.go`; `materialize_snapshots.go` | default LIVE, policy mutable/history insuficiente; snapshot individual transaccional vs multistage publication |

### Decisiones y evidencia física conservada

| ID | Fuente canónica | Clase / alcance |
|---|---|---|
| D01 | [[Echo - Auditoria POC e Identidad Forge-Echo 2026-08-23]]: ALINEAMIENTO OWNER 2026-08-24, dominio/magic/Reference permanente/F2A-F2B y post-freeze decisions | D; fuente de requisitos accepted, sus findings antiguos sólo se reutilizan después de contraste S |
| D02 | [[2026-09-06-echo-forge-mt5-execution-model-v2]] + [[2026-09-06-echo-forge-mt5-global-physical-ownership-v2]] + [[2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3]] | D frozen con supersesión V3; NORMAL A local source S; B1/B2 sin implementar al corte |
| D03 | [[2026-09-06-echo-forge-finalist-model-v2]] + [[2026-08-30-echo-forge-finalist-promotion-v1]] | D frozen / evolutionary BWC; new contract ≠ deployed V2 |
| D04 | `xKoRx/symphony/.agents/rules/14-durable-foundation-only.md`; [[2026-08-19-echo-forge-a6-big-bang-supersedes-a5]]; [[2026-08-27-durable-artifact-plane-write-once-integration-slice2]] | D + source F02/F09; persistence support actual prevalece sobre freeze previo intra-scope legacy |
| P01 | [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]: checkpoint 2026-09-05 RELEASE-0.2.96-AND-FINALIST-FACTORY-V1-FINAL-PHYSICAL-RECERT; Campaign/Run IDs en §1 | P reportada en acta; no nueva reproducción. Migration013/fleet/parser/zero-supply/replenishment/replay |
| P02 | Evidencia consolidada de dos FULL y preflight, localizable por FlowRunRefs exactos de §1; [[2026-09-06-echo-forge-mt5-execution-model-v2]] preserva fallas físicas; [[2026-09-06-echo-forge-finalist-model-v2]] preserva corrección semántica | P reportada; seis TradeSets completos según preflight consultado, sin queries propias a stores; baseline no se confunde con legacy trade_lists |
| P03 | `xKoRx/symphony/specs/FEAT-SQX-MT5-PIPELINE-ARTIFACTS/evidence/owner-run/`: `backtest-summary.json`, `compile-summary.json`, `.htm`, `tester.ini`; parser fixtures/corpus tests | P primaria conservada + S parser; run agosto demuestra HTM real relativo y real-ticks reportado, no certifica por sí solo slots/ownership/V2 |
| P04 | [[Echo - Cierre del Lab y Limpieza del Journal]] y [[Echo - Reporte de Estado Lab y Journal 2026-08-21]] | P reportada de agosto: Lab productivo y policy coverage/clock/legacy gaps; no se presentan esas cantidades como inventario septiembre |

La documentación oficial complementa semántica de plataforma, no prueba implementación local: [Temporal — Activity failures/timeouts](https://github.com/temporalio/documentation/blob/main/docs/encyclopedia/detecting-activity-failures.mdx) confirma retry tras timeout/heartbeat; [MQL5 — Local and server time](https://www.mql5.com/en/book/common/timing/timing_local_server) y [TimeGMT](https://www.mql5.com/en/docs/dateandtime/timegmt) describen relojes del tester. La decisión B usa el comportamiento del SDK pinneado: una página latest no sustituye auditar ese pin.

### Verificación realizada en esta auditoría

- Git read-only: estado/HEAD/origin tracking, consulta `ls-remote` master de Echo y Symphony; clone aislado Echo master y diff contra checkout local. El único delta Echo fue readiness SQL; Symphony remoto coincidió con a10c26c. No fetch/checkout/reset de repos de trabajo originales.
- Echo `v3/sdk`: `GOWORK=off go test -mod=readonly ./lab/... ./domain ./mm` **PASS**, nueve paquetes con tests y `lab/domain` sin tests. No DB productiva ni EA físico en esos tests.
- Symphony: `go test -mod=readonly ./sqx/core/forge ./sqx/core/domain ./sqx/adapters/mt5/report ./sqx/adapters/mt5/scoring` **PASS (cached)**. Valida coherencia del conjunto local, no equivale a recertificación física ni a ejecutar suite amplia.
- No se aplicaron comandos de bootstrap que escriben source/formatean/aplican metadata; el modo READ ONLY del owner prevalece. No se corrió Hasura metadata apply, go fmt, migrations, release ni deploy.
- Materialización canónica Resource/Sources/change_log y lint dirigido del vault se registran en [[2026-09-06-echo-forge-auditoria-producto-2026]].
