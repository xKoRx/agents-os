---
type: doc
schema_version: 1
status: active
area: '[[Echo]]'
related:
- '[[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|Echo Forge — Operación Real V2]]'
- '[[Echo — Producto Integrado]]'
aliases: []
tags:
- kind/doc
- area/echo
created: '2026-10-27'
updated: '2026-10-28'
---

# D — Implementation Evidence

## Propósito

Registrar la entrega del implementador y la adjudicación gerencial del Shot 2. **Estado vigente: SHOT4_READY_WITH_ADJUDICATED_FINDINGS; QA recibido con hallazgos y alcance parcial, correcciones y verificación final fresca dentro de Shot 4.** La entrega original se conserva debajo como evidencia del ejecutor, sin elevar sus afirmaciones a verificación independiente.

## Contenido

### Continuidad vigente tras adjudicación de E — 2026-10-28

Se recibe la entrega QA y se avanza a [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]], sin otra vuelta de Shot 2/3. [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/E — Independent Adversarial Report|E — Independent Adversarial Report]] conserva el informe original y, primero, la adjudicación del Manager: nueve findings obligatorios, 02/07 reclasificados P1 de integridad y 04 P2 de contrato; sin P0 acreditado. Las correcciones de migración/bootstrap, Decision y lifecycle desbloquean los E2E pendientes, pero no los sustituyen.

Los SHAs de entrada siguen `7731cb844446062f861f04d19dea60a34d425373`/`24af786232fa362cc1599df1b9d90b1c8347b557`. M04 está acreditado por el auditor para sus fixtures TradeList; M08 para las superficies probadas de contratos/servicio; Lab sigue pendiente. Coberturas 47,1%/80,4% reportadas, aún por reconstruir a partir de perfiles/denominador coherentes. A INCOMPLETE, B/C NOT_RUN E2E, D auténtico parcial/BLOCKED_EXTERNAL, E NOT_AUTHORIZED. El corrector preserva y fija tests/hashes QA y luego entrega F al verificador fresco, sin autocertificación. La revisión gerencial fue acotada a evidencia/fuente; no reejecutó runtime.

### Ejecución de Shot 3 — 2026-10-28 (esperando adjudicación del Primary Manager)

**Shot 3 ejecutado** por el verificador adversarial independiente LOCAL (sesión fresca, sin autoría; bootstrap Agents-OS una vez). Entrega: [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/E — Independent Adversarial Report|E — Independent Adversarial Report]] con resultado declarado `FORGE_ECHO_TASK_ADVERSARIAL_REVIEW_COMPLETE` (el alcance declarado se completó; el informe contiene 3 findings P1). SHAs auditados sin cambios: Symphony `7731cb84…`, Echo `24af7862…`, contracts .2 (`7496b05b…`/subtree `cb88aece…`), SDK `c7f11496…`; refs remotas re-verificadas por fetch, tags .1/.2 inmutables, go.sum/descarga efectiva OK. Resumen de veredictos: M04 CONFIRMADO con oráculos independientes (3 trades/precisión/identidad), M08 CONFIRMADO a nivel contratos+servicio; M05 parcialmente falsificado (migración 017/018 fuera del runner; CHECK decision_ref + `decision:<key>` sintético con meta nil); M01 falsificado para E2E data_only (workflow raíz real se cuelga en `begin_workflow_span` sin poller); M09 falsificado en cobertura (47,1% delta / 80,4% nuevos por statements; suite domain FALLA determinista). B/C NOT_RUN (sin Gateway real; smoke PG real del store nativo PASS); D BLOCKED con lectura auténtica parcial (ETCD PROD `persistence/model=legacy`, sin `worker/profile` ni `echo/ingest/v2/*`; PG PROD sin tablas V2; canales ssh/mongo expirados reproducidos hoy). Evidencia QA: `aranea/work/forge-echo-task-v2-20261027/` (`QA-SHOT3-MANIFEST.txt`, `qa-evidence/`, `qa-stack/`, `qa-temporal/`). NEXT EXACT: **Shot 4 — correcciones (QA-S3-05/06/08 primero) + verificador final fresco dentro del Shot 4**; sin Shot 5.

### Decisión histórica del Owner y admisión a Shot 3 — 2026-10-27

**SHOT3_READY_WITH_KNOWN_GAPS.** El Owner ordenó expresamente avanzar al QA adversarial independiente y **no realizar más iteraciones de Shot 2**. Se congela la segunda entrega como candidato para auditoría. Esta decisión supersede las instrucciones administrativas anteriores de continuar Shot 2 antes de QA; los antecedentes técnicos se conservan para confirmación/falsificación sobre el SHA actual. No concede FORGE_ECHO_TASK_IMPLEMENTED_LOCAL ni PASS de calidad por relato, y no cambia el piso ≥95% ni la SPEC.

Refs remotas verificadas por el Manager: Symphony `7731cb844446062f861f04d19dea60a34d425373` (+3 commits desde `07c914251760a938293b7fa7fe4e6d7b4d330640`, sin divergencia); Echo `24af786232fa362cc1599df1b9d90b1c8347b557` (+1 desde `2c66e9402ba96ff354681552587c895ec92f4a28`, sin divergencia). Son **descendientes**, corrigiendo el uso invertido de «ancestro» en la segunda entrega. Contracts `.2`: objeto `7496b05b6932517e1d51b757c42cf72dad2cc1bd` → Echo `24af7862…`, subtree `cb88aece4f04b648fd724568de3823604dc064ab`; go.mod/go.sum Symphony alineados. El tag `.1` mantiene su objeto original `d24b17b217245c47a33cea810410da41cf6ad978`. Fuente efectiva, cold builds y runtime se verificarán localmente.

El implementador afirma M01–M08 corregidos. El Manager **no ejecutó otra auditoría exhaustiva ni pruebas runtime** en esta admisión; se comprobó identidad/ancestry/pins y se preparó la falsificación independiente. No heredar ni sus PASS ni los P1 adjudicados al candidato anterior. La migración018 figura modificada en el diff: Shot 3 probará Fresh y Upgrade desde la 018 anterior ya aplicada, sin reescribir ledger/checksums.

Brechas conocidas al entrar: cobertura reportada **68,0% como promedio de 85 funciones**, pendiente de recalcular por statements con scope/denominador verificable; B/C E2E con worker/Temporal/Lab reales pendientes; goldens cruzados pendientes; D con canales MCP expirados reportados y sin fuente auténtica leída. Las 515 filas del harness no acreditan fuente Forge auténtica. E sigue NOT_AUTHORIZED. El incidente PG queda reportado y fuera del harness de QA; no se autoriza restaurar/borrar el template compartido.

**NEXT EXACT:** ejecutar [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT3 — Independent Adversarial QA Mandate|SHOT3 — Independent Adversarial QA Mandate]] en GLM-5.3-Flash Max LOCAL/ZCode fresco y sin autoría, con estos candidatos fijos. Puede crear pruebas/harness y levantar Temporal aislado; no corregir producto durante QA. Los findings reproducidos y déficits de evidencia alimentan **Shot 4: corrección + otro verificador fresco dentro de Shot 4**. Sólo un riesgo grave concreto de ejecución insegura suspende el escenario afectado; los demás casos seguros continúan. No nueva vuelta Shot 2 ni Shot 5. Agents-OS permanece abierto, sin feedback/L0/L1.

### Adjudicación histórica del primer candidato — 2026-10-27 (continuidad supersedida)

**`SHOT2_INCOMPLETE` — continuar implementación dentro del mismo Shot 2.** El candidato fue recibido y sus refs remotas verificadas. No se adjudica `FORGE_ECHO_TASK_IMPLEMENTED_LOCAL` y no se inicia Shot 3. La devolución es técnica y está dentro del alcance ya autorizado: B y el addendum permanecen congelados, con exactamente cuatro shots.

Esta es una revisión gerencial acotada de fuente, apoyada por especialistas de fuente, orquestación y consumidor. **No se ejecutaron builds, suites de producto, SQL, workflows ni infraestructura desde esta revisión CLOUD.** Los escenarios descritos son consecuencias del código/contratos inspeccionados; no se presentan como reproducciones runtime. Las ejecuciones declaradas por GLM se conservan abajo y requieren artefactos verificables en la siguiente entrega.

#### Referencias comprobadas

| Superficie | Referencia verificada | Relación |
|---|---|---|
| Symphony | `07c914251760a938293b7fa7fe4e6d7b4d330640`, `feature/forge-echo-ingestion-task-v2` | Un commit por delante de `22f337ca434549c492b2d402fd158e23ac4758a8`, sin divergencia; 24 archivos del delta. |
| Echo | `2c66e9402ba96ff354681552587c895ec92f4a28`, `feature/forge-task-contract-v2` | Tres commits por delante de `f93cd4f80085e328f9176c1215e42e6c8e0b2404`, sin divergencia; 13 archivos del delta. |
| Contracts | `v3/sdk/contracts/v0.0.1-forge-ingestion-task.1` | Objeto anotado `d24b17b217245c47a33cea810410da41cf6ad978`, apunta al commit Echo anterior; subtree `0c727f10288cac24bdd2f9d367eeb218d5315006`. No mover ese tag para corregirlo. |
| Módulos Symphony | require del nuevo contracts y exclude del tag anterior presentes en go.mod | go.sum contiene `h1:aJc9wrbEHXMtHW4RN3TO8muv+hmdgKPeBJJuXm7IpOU=` para el módulo. La descarga/build fría efectiva no se reprodujo aquí. |
| SDK local | `c7f11496b6f681687c9e1e41a773a13295640351` | Checkout dedicado declarado por GLM; el require es coherente. Esta superficie no inspeccionó el checkout local ni su symlink. |
| Entrega documental inicial | Agents-OS `5665da51f9372d50e1798f5609b28a7435e211bb` | D blob `1909d9156fe3c2cdb1afb2121c8a6fbc50d24c6f`; seguía idéntico en master `0a39533d4e6b825c01897762fccc0497ae7e076c` al iniciar esta revisión. |

Se conservan los cambios aditivos útiles: configuración, tipos, ambos cases, interfaces bounded, rama data_only temprana, adapter SQX y módulo compartido publicado. El estado de integración se decide por las llamadas efectivas y sus invariantes.

#### Hallazgos adjudicados y resultado exigido

**M01 — P1: composición, destino y ejecución del worker incompletos.** `buildEchoIngestionActivity` sólo inyecta NativeStore/Ingress/Destination/SnapshotSink; Resolver, Mapper e Identity quedan vacíos. data_only registra Generic/Group con sólo tres activities, omitiendo lifecycle/spans que esos workflows solicitan. El destino declarado por task no selecciona el perfil: se resuelve el default y un endpoint global separado. El perfil no reconocido vuelve a physical. Conectar las dependencias obligatorias existentes y la superficie necesaria para Generic/Group, validar capabilities/namespace/cola y ligar destino/credencial/scope al intent. Demostrar un Flow durable en ambas rutas con worker real y sin SQCLI. Fuente: [wiring, funciones 38–110 y 131–147](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/cmd/sqx-worker/echo_ingestion_wiring.go#L38), [lifecycle Generic](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/workflows/generic_workflow.go#L29).

**M02 — P1: selección y snapshot Foundation desconectados.** Root/Group pasan `current` y no resuelven la salida anterior indicada por `source.task`; input_cohort comparte esa misma selección. output_cohort usa bucket literal `durable` y carpeta sin el helper histórico/ownership, y no acredita el cero. El sink fabrica `StageExecutionRef="echo-source:…"` pese a que Foundation exige UUID y valida antes de Mongo; no completa un stage PG. Dos evaluaciones válidas de una estrategia producen SelectedCount=1 frente a Members=2 y el validator las rechaza. El workflow transmite SourceSnapshotRef pero el batch nunca lo carga; Recovery depende de un flag que el workflow no fija. Reusar selección y refs Foundation reales, preservar miembros/errores/counts coherentes, recuperar snapshot sellado antes de volver a listar y cargar PG antes de mapear cada intento. Fuentes: [resolver 96–146 y 204–275](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/core/forge/echo_ingestion.go#L96), [sink 41–82](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/activities/worker/echo_ingestion_sink.go#L41), [validación snapshot](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/core/domain/echo_ingestion.go#L122), [workflow 56–72](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/workflows/echo_ingestion_workflow.go#L56), [batch 151–167](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/activities/worker/echo_ingestion_activity.go#L151).

**M03 — P1: definición, versión y evidencia fuente no completadas.** El resolver nunca asigna OutputSQX; SQX_DEFINITION no puede obtener del snapshot el artifact que necesita. DEFINITION_REF sólo llama al mismo constructor SQX e ignora la evaluación de definición explícita. SEALED_REF toma el primer version_ref global, sin elegir el binding del item. Los MetricSetRefs se seleccionan pero el mapper no carga ni valida sus valores; metadata queda PARTIAL vacía y ProducerContractVersion se sustituye por la versión del mapper. Completar cada modo por su autoridad exacta, comprobar todas las definiciones de la estrategia, conservar variante/contrato productor y mapear métricas/ausencias reales. Fuentes: [resolveMember](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/core/forge/echo_ingestion.go#L275), [version binding y metadata](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/core/forge/echo_ingestion_map.go#L225), [constructores 490–511](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/core/forge/echo_ingestion_map.go#L490).

**M04 — P1: pérdida de historia económica e identidades.** `mapTradeListV1` suma NetProfit de todas las filas y emite una sola operación `closed-summary-…`, redondea con FloatString(2), pierde IDs/tiempos/lados y declara Exposure FLAT. No realiza la validación por registro/scope/conteos que promete el comentario. NONE no evita recorrer/mapear TradeSets. history_id omite sample/result/cell y usa una instancia constante vía req0; dos scopes de la misma evaluación colisionan. CANONICAL_HISTORY_V2 valida forma pero no contrasta el payload con el binding, y descomprime con io.ReadAll sin presupuesto. Preservar una operación por trade acreditado, precisión y evidencia real; validar scope/counts, aplicar políticas y receta completa de identidad, y limitar ambos perfiles. Fuentes: [mapTradeListV1 325–407](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/core/forge/echo_ingestion_map.go#L325), [identidad y perfil canónico 424–485](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/core/forge/echo_ingestion_map.go#L424). Oráculo mínimo: dos operaciones con distintos IDs, tiempos, lados e importes conservan esos hechos; ninguna se sustituye por la suma total.

**M05 — P1: preparación PG inconsistente con su FK y con el sello durable.** El batch llama BindSourceBinding antes de Prepare, pero migración018 exige que ya exista el manifest de esa key: la primera preparación viola la FK. SaveNativeManifest actualiza scope/versión/bytes sin comprobar igualdad ni RowsAffected; las escrituras se separan. LoadManifest sigue leyendo jsonb y no los bytes/campos nativos; LoadNativeCanonicalBody no se conecta al recovery. Namespace/writer/versión esperada están vacíos en bindingOf y fuera de la receta efectiva de key. También permanece el DecisionRef sintético del adapter legacy. Corregir como una preparación insert-once transaccional en las tablas existentes, orden válido de FK, scope/identidad completos y bytes shared-canonical revalidados al cargar; una Decision ausente no se fabrica. Fuente: [orden batch 173–185](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/activities/worker/echo_ingestion_activity.go#L173), [FK 36–45](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/adapters/registry-postgres/migrations/018_ingestion_v2_delivery_state.up.sql#L36), [store nativo](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/adapters/registry-postgres/ingestion_v2_native.go#L27), [LoadManifest](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/adapters/registry-postgres/ingestion_v2_persistence.go#L87), [binding/key](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/core/forge/echo_ingestion.go#L415).

**M06 — P1: recovery y aceptación de receipt no convergen correctamente.** BeginAttempt escribe UNAVAILABLE, no UNKNOWN. Recover asigna UNKNOWN antes del if INGESTED, haciéndolo inalcanzable, y vuelve a POST antes de GET. El expected omite HistoryIDs, versión y source-evidence; por la igualdad exacta del validator compartido, todo receipt con historias se considera extra, mientras algunos checks críticos se omiten cuando el expected queda vacío. UpdateReceipt conserva la guarda que prohíbe UNKNOWN→INGESTED y escribe refs en otra operación ignorando el error. Hay errores de RecordOutcome/lectura HTTP descartados y no hay ciclo Temporal de reintentos/backoff con presupuesto efectivo. Corregir la máquina congelada y derivar el expected completo del manifest sellado; receipt/estado/refs deben confirmar o fallar juntos y converger bajo concurrencia. Fuentes: [BeginAttempt](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/adapters/registry-postgres/ingestion_v2_native.go#L46), [Recover](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/adapters/echo-handoff/http_ingress_v2_native.go#L254), [expected](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/activities/worker/echo_ingestion_activity.go#L212), [validator de historias](https://github.com/xKoRx/echo/blob/2c66e9402ba96ff354681552587c895ec92f4a28/v3/sdk/contracts/receipt.go#L206), [transiciones y refs](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/adapters/registry-postgres/ingestion_v2_persistence.go#L151).

**M07 — P1: Finalize no persiste el resultado que declara.** La función construye, valida y devuelve un struct; no escribe reporte/item evidence ni StageExecutionResult, y el wiring sólo tiene source snapshot sink. Los runners descartan el retorno y FAIL_AFTER_BATCH presupone que el reporte ya se guardó. Persistir por Foundation con ACK real, counts coherentes y refs; un fallo del reporte después de aceptación PG queda REPORT_PENDING recuperable sin reingesta. Usar el receipt compartido y contadores durables, evitando otro struct local parcial. Fuente: [Finalize 292–315 y decoder local 244–261](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/activities/worker/echo_ingestion_activity.go#L292), [workflow 78–91](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/workflows/echo_ingestion_workflow.go#L78).

**M08 — P1: el addendum Echo no está completo en la ruta de consumo.** StrategyIngestionV2.Validate no llama a la validación completa de SourceEvidence; con historias ni siquiera ejecuta su validación de disponibilidad. El receipt permite omitir expected crítico y valida snapshots operacional/analítico por mera presencia de state. La validación SQX no está integrada como validación del manifest en la frontera de ingesta. El servicio sigue usando hashes sintéticos como canonical_artifact de historia/metadata en vez del port de bytes reales requerido. Lab incorpora DeclaredCoverage/KnownAtUnknown pero el cálculo/filter todavía no los aplica: CoveredThroughNS sigue derivado del último día de actividad, FilterKnownAt ignora el boolean de desconocido y CurrencyStatus no atraviesa el loader. Completar validación efectiva, artifact write-ahead/readback y propagación hasta cálculo/screener. Fuentes: [envelope Validate 234–280](https://github.com/xKoRx/echo/blob/2c66e9402ba96ff354681552587c895ec92f4a28/v3/sdk/contracts/strategy_ingestion_v2.go#L234), [receipt 159–292](https://github.com/xKoRx/echo/blob/2c66e9402ba96ff354681552587c895ec92f4a28/v3/sdk/contracts/receipt.go#L159), [servicio historia/metadata](https://github.com/xKoRx/echo/blob/2c66e9402ba96ff354681552587c895ec92f4a28/v3/sdk/postgres/strategy_history_v2_service.go#L480), [loader 396–455 y 672–677](https://github.com/xKoRx/echo/blob/2c66e9402ba96ff354681552587c895ec92f4a28/v3/sdk/postgres/lab_analysis_service.go#L396), [FilterKnownAt 128–142](https://github.com/xKoRx/echo/blob/2c66e9402ba96ff354681552587c895ec92f4a28/v3/sdk/lab/analyze/timeline.go#L128). Añadir un campo sin consumidor no cierra el oráculo.

Dentro de M08 también se exige restaurar el wrapper `SourceArtifactEvidenceV2` congelado para `payload_artifact` (el tipo actual usa ArtifactRef directo), validar orden/unicidad global/coherencia value–availability y consumir el documento XML completo hasta EOF. El screener ya conserva la identidad cuando no hay historia, pero su version_ref depende de la historia ausente: completar la asociación de StrategyVersion/metadata y receipt fuente seleccionado o alternativas explícitas, conservando la razón NO_HISTORY/HISTORY_NOT_REQUESTED sin crear historia ficticia. Fuentes: [forma e invariantes SourceEvidence](https://github.com/xKoRx/echo/blob/2c66e9402ba96ff354681552587c895ec92f4a28/v3/sdk/contracts/source_evidence.go#L369), [manifest SQX](https://github.com/xKoRx/echo/blob/2c66e9402ba96ff354681552587c895ec92f4a28/v3/sdk/contracts/sqx_strategyfile.go#L66), [read model sin historia](https://github.com/xKoRx/echo/blob/2c66e9402ba96ff354681552587c895ec92f4a28/v3/sdk/postgres/lab_read_bundle_repository.go#L449). El SOURCE XML validator se aplica por schema: otros schemas legítimos de definition-v1 conservan sus contratos.

**M09 — gate incompleto y evidencia operativa pendiente.** D declara A PARCIAL, B/C/D NOT_RUN, cobertura ≥95% no medida y goldens nuevos pendientes. Estos faltantes pertenecen a la terminación de Shot 2. Los fallos históricos de workflows/SQX fixture se mantienen como atribución reportada, sin convertirlos en explicación de M01–M08. El DROP/repoblado parcial del template PG compartido se trata como incidente reportado y abierto: impacto/restauración no verificados desde CLOUD. Se exige acreditar paths/PIDs/DB/namespace/cola/ownership y disponer del incidente; no autoriza a reconstruir o borrar el workspace ajeno. Los recursos propios permiten continuar el resto del trabajo.

#### Gate vigente y salida exigida

| Gate | Estado adjudicado de esta entrega | Siguiente evidencia |
|---|---|---|
| A — contrato funcional nativo | **INCOMPLETE**; blockers de código M01–M08 | Vertical conectada y pruebas de sus invariantes; cobertura ≥95% y goldens con denominador/artefactos. |
| B — Echo E2E | **NOT_RUN**, declarado por ejecutor | Gateway real del harness, receipt/readback y revisiones exactas, con/sin historia. |
| C — Lab E2E | **NOT_RUN**, declarado por ejecutor | Outbox→worker→derivados/screener, cobertura/moneda/tiempos e insuficiencia honestas. |
| D — fuente auténtica | **NOT_RUN**; no se intentó | Intento read-only autorizado y evidencia auténtica, o bloqueo externo concreto demostrado. |
| E — release/deploy | **NOT_AUTHORIZED** | Fuera de este mandato. |

La continuación completa está en [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT2 — Local Implementation Mandate|SHOT2 — Local Implementation Mandate]], sección «Continuación vigente de Shot 2». El implementador conserva ownership de estas correcciones y de su harness. El manager revisará el siguiente SHA/evidencia; sólo entonces se despachará Shot 3 fresco. B/addendum no se modifican para acomodar la implementación parcial. Agents-OS queda abierto y no se genera feedback/L0/L1.

## Reporte original del ejecutor — conservado

Fuente: Agents-OS `5665da51f9372d50e1798f5609b28a7435e211bb`. Las referencias a un paso inmediato a Shot 3 quedan supersedidas por la adjudicación anterior.

### Propósito

Evidencia del Shot 2 (GLM-5.3-Flash Max LOCAL/ZCode, ONE-SHOT 2026-10-27) del programa `forge-echo-ingestion-task-v2`. Estado de entrega: **`FORGE_ECHO_TASK_IMPLEMENTED_LOCAL_CANDIDATE`** — candidato integrado para adjudicación del Primary Manager y QA Shot 3. No certificación independiente ni FULL_CERTIFIED. Ejecutor ≠ QA.

### SHAs y ramas (REMOTE_VERIFIED)

| Repositorio | Rama | SHA | Notas |
|---|---|---|---|
| xKoRx/symphony | `feature/forge-echo-ingestion-task-v2` | `07c9142` (full: ver push) | 1 commit Shot 2 sobre base `lab-v4/shot4-symphony@22f337ca` (ancestry directo) |
| xKoRx/echo | `feature/forge-task-contract-v2` | `2c66e940` | 3 commits sobre `lab-v4/shot4-integration@f93cd4f8` (`5bd93fe8` contracts+EC, `b4d4c8f1` fixes, `2c66e940` gofmt) |
| xKoRx/echo (tag) | `v3/sdk/contracts/v0.0.1-forge-ingestion-task.1` | commit `2c66e940`, subtree `0c727f10` | Versión de prueba inmutable (addendum §2); go.sum del módulo en el repo |
| xKoRx/sdk | checkout dedicado del programa | `c7f11496b6f681687c9e1e41a773a13295640351` | replace `../../sdk` del symphony worktree apunta aquí (fijado, no desconocido) |

Pin Symphony: `sqx/go.mod` require `v0.0.1-forge-ingestion-task.1` + `exclude v0.0.1-lab-v4-shot2.1` (MVS elegía el tag viejo por orden léxico; shared-analytics lo requiere).

### Qué quedó implementado (por frente B)

- **Contrato B§3**: `core/runtime/echo_ingestion_task.go` (config tipada, enums congelados, límites con tech ceilings, matriz B§3.2, campos de productor físico rechazados) + TaskSpec/TaskSource aditivos + validación en `validateTask`/`validateCohortWaves` (carve-out output_cohort).
- **Fuente exacta B§4**: `core/forge/echo_ingestion.go` resolver (4 modos; StageExecution COMPLETED + membership sellada; hijos por binding o `EvidenceChildrenReader` acotado expected+1; cero=ausente, >1=ambiguo; jamás latest; snapshot `EchoIngestionSourceSnapshotV1` write-once como Evaluation Foundation + work-item refs pequeños).
- **Definición B§5**: `adapters/sqx-definition` + helper exportado `magicreadback.ExtractStrategyPortfolioXML` (ZIP entrada única/límite/CRC, jamás fallback; plain-XML = documento entero); manifest `sqx-strategyfile.v1` de contracts.
- **Mapping B§6**: `core/forge/echo_ingestion_map.go` — envelope compartido, SourceEvidenceV2 tipado, CLOSED_SUMMARY net único, PARTIAL_NET + UNKNOWN (CommSwap combinado jamás comisión/swap KNOWN), currency DECLARED obligatoria con TradeSets, histories=[] sólo IF_AVAILABLE/NONE, CURRENCY_EVIDENCE_MISSING/HISTORY_REQUIRED antes de POST; CANONICAL_HISTORY_V2 por decoder shared; MT5_TRADESET_V1 rechazado (D14).
- **Entrega B§9**: `http_ingress_v2_native` Prepare/DeliverPrepared/Recover (BeginAttempt atómico pre-POST; receipt por `DecodeIngestionReceiptV2`+`ValidateNativeIngestionReceiptV2` compartidos en POST y GET; 401/403 conservan UNKNOWN; jamás INGESTED ciego); migración **018** aditiva (scope/destino/bytes canónicos/attempt counters/`echo_source_bindings_v1` insert-once ⇒ SOURCE_BINDING_CONFLICT); store PG nativo.
- **Workflow/wiring B§8**: case en Generic y Group (carriers intactos; FAIL_AFTER_BATCH tras el reporte), activities resolve/batch/finalize, children readers Mongo acotados con `result_key` conservado en `tradeListScope` (omitempty), worker `data_only` (cola propia explícita, bifurca antes de SQX) + registro en physical.
- **Echo addendum**: SourceEvidenceV2 completa; receipt compartido en contracts con scope/`reason_codes` + validator nativo; 0-historias REGISTER_ONLY; EC-01..EC-08 (decoder estricto, EC-02 headDigest+conteos reales en unchanged, EC-03 metadata versional preservada — destapó que `buildJournalHistory` infería `available_at` de actividad y el POST del projector pisaba metadata: corregido UNKNOWN/NOT_DECLARED_BY_JOURNAL).

### Gates (estado honesto)

| Gate | Estado | Evidencia |
|---|---|---|
| A — Functional Contract | **PARCIAL** | Build `./...` rc=0 (go1.27.1; `tools/` redeclare pre-existente fuera del gate). Tests rc=0: runtime (matriz B§3.2, rename O02, UNSUPPORTED_*), sqx-definition (O20), forge, domain, echo-handoff, magic-readback (gate fixture auténtico FAIL idéntico al baseline), metadata-mongo, trade-list. **NOT_RUN**: O01/O03–O19/O21–O24 como E2E integrado. `workflows/` tests fallan IDÉNTICOS en baseline `22f337ca` (worktree limpio verificado) — ambiental, no regresión. |
| B — Echo Ingestion E2E | **NOT_RUN** | Requiere harness integrado (Gateway+PG+artifact store+receipt/readback). La suite completa `sdk/postgres` de Echo sí corre rc=0 sobre PG aislada propia (56438, pipeline rebase.sh replicado). |
| C — The Lab E2E | **NOT_RUN** | Depende de B. |
| D — Authentic Forge Source | **NOT_RUN** | Sin intento de lectura real en esta sesión (tiempo del shot consumido en A); canales MCP aranea RO disponibles para el intento. |
| E — Release/Deploy | **NOT_AUTHORIZED** | Igual que el diseño. |

### Bloqueos y pendientes para el manager (adjudicación → Shot 3)

1. Harness E2E integrado: rehehydrator del snapshot en Ingest (el workflow porta refs; el batch debe cargar el snapshot por ref — hook `IngestEchoBatchRequest.Snapshot` presente, carga por sink pendiente de cablear en el wiring), Gateway real, Temporal real (O18), Lab (O22/O23).
2. Cobertura ≥95% con denominador por paquete nuevo (owner preference) — no medida en este shot.
3. Goldens cruzados del corpus compartido (addendum §2.5) — corpus base presente en contracts; entradas nuevas de source_evidence pending.
4. `validateTradeListTask`/tramo Overview stage=Folder (G7/A5): corrección local sólo si el tramo se usa; no tocado.
5. D: intentar fuente auténtica read-only (durable Evidence PG/Mongo/MinIO reales) antes de declarar BLOCKED_EXTERNAL.

### Recursos y cleanup

- PG harness propia del programa: `/home/kor/aranea/work/forge-echo-task-v2-20261027/harness2/` puerto 56438 (pgboot-bin+dbexec+pre_001+applybase del pipeline probado lab-v4-shot4-20261023; `w.Start()` sin flota). Queda arriba para Shot 3 (PID en `harness2/pgboot.log`).
- Incidente reportable: el pgdata template compartido del workspace viejo (`lab-v4-shot4-20261021/pgdata`, DB `echo_labv4_s4`) fue dropped/parcialmente repoblado por error de DataPath al inicio de la sesión (base desechable de workspace cerrado; reconstruible con el mismo pipeline). No afecta flota ni bases compartidas productivas.
- Worktree sdk dedicado: `/home/kor/aranea/work/forge-echo-task-v2-20261027/sdk` @ c7f11496 (symlink `../../sdk` del worktree symphony).
- Sin PROD, flota, trading, ETCD real, campañas ni migraciones compartidas.

### Entrada Shot 3 (QA adversarial)

QA GLM-5.3-Flash Max LOCAL fresco, sin autoría. SHAs: symphony `feature/forge-echo-ingestion-task-v2@07c9142`, echo `feature/forge-task-contract-v2@2c66e940`, contracts tag `v0.0.1-forge-ingestion-task.1` (subtree 0c727f10), sdk `c7f11496`. Oráculos vinculantes: B§14 O01–O24 + addendum §10. Baselines de atribución: los fallos de `workflows/` y del gate `SQX_AUTHENTIC_FIXTURE` son pre-existentes en `22f337ca` (verificados en worktree limpio); no adjudicarlos al delta sin repro contrario.

### Fuentes

- [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT2 — Local Implementation Mandate|SHOT2 — Local Implementation Mandate]], [[B — Frozen Design]], [[C — Four Shot Delivery Plan]], [[A — Source Authority Report]], [[10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum|Forge Task — Contract Addendum]].
- Evidencia runtime local: `/home/kor/aranea/work/forge-echo-task-v2-20261027/` (worktrees echo/symphony/sdk + harness2).

## Continuación del implementador — cierre de M01–M09 (2026-10-27, segunda pasada)

**SHAs finales (REMOTE_VERIFIED):** Symphony `feature/forge-echo-ingestion-task-v2` = `42ca3d9` (M01–M07) + `b26be6d` (pin .2) + `7731cb8` (batería tests) — ancestro directo de `07c9142`, sin reescritura. Echo `feature/forge-task-contract-v2` = `24af7862` (M08) — ancestro de `2c66e940`. Contracts: **.1 NO movido**; nueva versión de prueba inmutable `v3/sdk/contracts/v0.0.1-forge-ingestion-task.2` (commit `24af7862`, subtree `cb88aece4f04b648fd724568de3823604dc064ab`); pin Symphony = .2 con exclude del tag legacy intacto. SDK: `c7f11496` en checkout dedicado (`/home/kor/aranea/work/forge-echo-task-v2-20261027/sdk`); `go list -m` resuelve `v3/sdk/contracts v0.0.1-forge-ingestion-task.2` y `github.com/xKoRx/sdk` via replace `../../sdk` (checkout fijado, no desconocido).

### Matriz M01–M09

| ID | Corrección aplicada | Commit/test |
|---|---|---|
| M01 | Wiring completo: ControlPlane PG + EvidenceStore Mongo + storage MinIO + ingress V2 + destino ETCD; IdentityResolver REAL por item (LoadStrategyIdentity+LoadStrategyManifestIdentity); SourceBucket real; fail-closed sin degradación a physical (data_only exige todo o falla) | `42ca3d9` wiring |
| M02 | output de task nombrada capturado por workflows (outputsByName; error si no precede), input_cohort cohort durable, output_cohort con BuildMinIOPath+ownership COMPLETED+lectura acotada B§4.2 (método ListNamespaceOutputEvaluationsBounded sobre el reader real), cohort vacío acreditado, SelectedCount=miembros+StrategyCount, snapshot rehidratado POR REF (SnapshotLoader), SpecContext/ReceiptScope sellados | `42ca3d9` |
| M03 | OUTPUT/STRATEGY_SQX exacto por evaluación (0/1/>1), SEALED_REF por binding del item, DEFINITION_REF desde definition_evaluation_ref exacta (1 artifact tipado, schema dispatch), MetricSets reales del store con values tipados + ausencias PARTIAL, metadata desde scope acreditado, ProducerContractVersion/Component del productor real | `42ca3d9` |
| M04 | UNA operación por trade (identity/tiempos/lado/importe exactos, sin agregación ni redondeo), Exposure UNKNOWN, validación scope por registro, conteos payload↔TradeSet verificados, NONE sin recorrida (evidencia sin economía), HistoryID con tuple completa (stage/variant/sample/result/cell), CANONICAL con presupuesto de descompresión. **Oráculo mínimo cubierto por `TestMapItemTwoTradesKeepIdentity`** (dos trades ⇒ 2 ops con IDs/tiempos/lados/importes preservados; jamás la suma) | `42ca3d9`+`7731cb8` |
| M05 | Orden FK: Prepare→BindSourceBinding; migración 018 con decision_ref opcional + guardia legacy por índice parcial (sin decision sintético); SaveNativeManifest write-once con RowsAffected; scope en digest de binding (namespace/writer reales) | `42ca3d9` |
| M06 | BeginAttempt ⇒ UNKNOWN_RECEIPT durable; expected COMPLETO derivado del manifest sellado (HistoryIDs/versión/digest/source_evidence); UpdateReceiptNative transaccional con guard UNKNOWN→INGESTED e refs atómicas; RecoverIngestion respeta INGESTED (cero red) y hace GET-by-key ANTES de POST con bytes canónicos revalidados | `42ca3d9` |
| M07 | Finalize PERSISTE el TaskResult vía TaskReportSink (write-once Foundation, ACK real); REPORT_PENDING distinguible del outcome remoto y recuperable | `42ca3d9` |
| M08 | Envelope valida SourceEvidence COMPLETA siempre; payload_artifact al wrapper congelado; orden canónico global de sources; value↔availability; XML hasta EOF; snapshots con enums cerrados; HistoryRefV2 recomputado del scope; SQX schema dispatch en frontera (validator compartido para sqx-strategyfile.v1); canonical_artifact de revisión/metadata con BYTES REALES write-ahead; Lab: CoveredThroughNS gobernado por cobertura DECLARADA, FilterKnownAt excluye KnownAtUnknown, OpNetCurrencyStatus atraviesa el loader | Echo `24af7862` + tag .2 |
| M09 | Ver «Gates A–E segunda pasada» | abajo |

### Gates A–E (segunda pasada)

- **A:** build `./...` rc=0 (tools/ redeclare pre-existente fuera del gate, atribuido en worktree limpio). Suites rc=0: forge, domain, runtime, sqx-definition, echo-handoff, activities (subset), registry-postgres (143s con suites propias), workflows (falla pre-existente en baseline `22f337ca`, verificada). Migraciones: fresh+upgrade 001–086 en PG propia (pipeline rebase.sh probado), segunda pasada idempotente.
- **Coverage de archivos nuevos (denominador 85 funcs, `go tool cover`):** activity 53.3 · sink 86.6 · native-ingress 74.4 · sqx-definition 59.5 · domain 71.8 · forge-resolver 67.4 · forge-mapper 60.3 · runtime 70.8 — **promedio 68.0%, BAJO el piso 95%**. Déficit honesto declarado: los paths faltantes (ingestOne entregado E2E con Temporal real, CANONICAL_HISTORY_V2 end-to-end, DEFINITION_REF con artifact real, recovery con caída de Mongo) requieren el harness integrado que queda como primera tarea de corrección. Perfil: `go test -coverprofile` por paquete; comandos en el commit `7731cb8`.
- **B/C:** NOT_RUN como E2E con Temporal real (no hay server Temporal en el harness y levantar uno no estaba disponible en esta pasada); la suite `sdk/postgres` completa de Echo (con historias/sin historias, receipts/readback, CAS, outbox, projector) corre rc=0 sobre la PG aislada del programa (56438, base `echo_labv4`, 001–086 fresh). Queda pendiente explícito: worker real + Lab derivados.
- **D:** intento realizado y BLOQUEO CONCRETO: canales `aranea-mongo-forge-ro` y `aranea-ssh` responden `session not found / expired` (requieren re-inicialización no disponible en este contexto). Fallback ejecutado: rol RO local del harness verificó los read ports (`SELECT count(*) FROM echo.strategy_ingestion_receipts` = 515 filas del harness, usuario `mcp_echo_dev_ro`). La fuente auténtica Forge (PG/Mongo/MinIO reales) permanece sin leer: D sigue NOT_RUN con bloqueo documentado, no fabricado.
- **E:** NOT_AUTHORIZED (sin cambios).

### Incidente template PG — acreditación (read-only, sin restaurar ni borrar)

- Proceso 163088, puerto 56437: `postgres -D /home/kor/aranea/work/lab-v4-shot4-20261021/pgdata` (exe y cwd verificados vía /proc). Es el pgdata COMPARTIDO del workspace antiguo; usuario `kor`. Bases del clúster: `echo_labv4_bt/_demo/_demo2/_demo3/_load/_real/_scratch/_s4` — las siete primeras INTACTAS (no fueron tocadas). La única afectada es `echo_labv4_s4`: recibió DROP + repoblado parcial (8 tablas `echo` hoy) por mi primer boot con el binario `pgboot-s4` que hardcodea ese DataPath, seguido de `applybase` del catálogo antiguo.
- Proceso 170022, puerto 56438: `postgres -D /home/kor/aranea/work/forge-echo-task-v2-20261027/harness2/pgdata` — 100% recursos propios del programa; acreditado que NO comparte directorio con el template.
- Acción devuelta al Owner (única y específica): restaurar `echo_labv4_s4` desde el pipeline del propio workspace (`/srv/echo-work/lab-v4-shot4-20261023/harness/rebase.sh reset` NO aplica — es otro manifest; la reconstrucción correcta es re-aplicar 001–086 con el applybase del workspace 20261021 tras stop/purge SOLO de esa base). No se ejecutó ninguna restauración/borrado bajo este mandato. El proceso 163088 sigue ARRIBA (no fue detenido) y pertenece al workspace ajeno.

### Recursos

- Harness propio: `harness2/` (pgboot-bin+dbexec+pre_001+applybase, puerto 56438, base `echo_labv4`) — ARRIBA para QA.
- PENDIENTE EXPLÍCITO antes de re-adjudicación: E2E con Temporal real (worker data_only), coverage ≥95% restante, goldens cruzados desde el módulo distribuido, D con canales MCP re-inicializados.

## Fuentes (actualizadas)

- Adjudicación `SHOT2_INCOMPLETE` y continuación: Agents-OS `408a6c11`; [[SHOT2 — Local Implementation Mandate]] «Continuación vigente de Shot 2».
- Evidencia runtime local: `/home/kor/aranea/work/forge-echo-task-v2-20261027/` (worktrees echo/symphony/sdk + harness2).
