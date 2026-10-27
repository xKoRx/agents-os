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
created: '2026-10-27'
updated: '2026-10-27'
---

# SHOT2 — Local Implementation Mandate

## Propósito

**Autorización documental — 2026-10-27:** el Owner autorizó explícitamente publicar íntegramente este paquete técnico en xKoRx/agents-os, con conocimiento de que el repositorio es público. La restricción de divulgación del intento anterior queda resuelta para este paquete. Agents-OS se actualiza directamente en master; esta autorización no habilita PROD, flota ni trading.

Mandato ejecutable para GLM-5.3-Flash Max LOCAL/ZCode después del gate de diseño. El prompt es una sola entrega; el Primary Manager conserva la adjudicación.

## Contenido

### Continuación vigente de Shot 2 — adjudicación del 2026-10-27

**Estado del manager: `SHOT2_INCOMPLETE`.** Se recibió el candidato `FORGE_ECHO_TASK_IMPLEMENTED_LOCAL_CANDIDATE`; la revisión de fuente no permite adjudicar `FORGE_ECHO_TASK_IMPLEMENTED_LOCAL`. El siguiente paso es terminar este mismo Shot 2 con el implementador LOCAL. Shot 3 no comienza todavía. Esta continuación no crea otro shot, no reabre el diseño y no sustituye al QA independiente.

Lee primero la sección **Adjudicación del Primary Manager** de [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/D — Implementation Evidence|D — Implementation Evidence]]. Sus hallazgos M01–M09 identifican defectos comprobados en el candidato y fijan resultados mínimos de corrección. B y el addendum siguen siendo la SPEC completa. Las afirmaciones del informe inicial permanecen como traza del ejecutor; no se elevan a PASS por haber sido publicadas.

#### Punto de partida y distribución

- Continúa sobre Symphony `feature/forge-echo-ingestion-task-v2@07c914251760a938293b7fa7fe4e6d7b4d330640` y Echo `feature/forge-task-contract-v2@2c66e9402ba96ff354681552587c895ec92f4a28`. Conserva ese trabajo y sus bases originales. Refresca sólo deltas posteriores, preserva trabajo concurrente y no resetees los candidatos ni regreses a una base anterior.
- El tag `v3/sdk/contracts/v0.0.1-forge-ingestion-task.1` está publicado y apunta a Echo `2c66e9402ba96ff354681552587c895ec92f4a28`. Es inmutable. Si cambias contratos, publica la siguiente versión de prueba libre, alinea pins/checksums y demuestra la versión efectiva con builds fríos independientes. No mover ni borrar el tag existente. El `exclude` actual se puede conservar si el grafo resuelto queda acreditado; por sí solo no prueba una descarga fría ni el consumidor efectivo.
- Acredita también el checkout efectivo de `xKoRx/sdk` (`c7f11496b6f681687c9e1e41a773a13295640351` según el ejecutor), sus replacements y el módulo padre. `GOWORK=off` no deshabilita reemplazos en go.mod. Registra `go list -m`/checksums, SHAs, fuente de build y binarios efectivamente usados sin publicar credenciales.
- La documentación se carga por el commit exacto del despacho, con fetch/git show si hace falta. El ZIP histórico no se usa. En la misma sesión conserva el bootstrap ya hecho; una sesión local nueva lo ejecuta una sola vez. No repitas Shot 1 ni busques otro diseño para suplir bugs ordinarios.

#### Terminación de producto dentro de este Shot 2

1. **Camino nativo real.** Completa la composición del worker, puertos de identidad/evidencia/artefactos, resolución del `source.task` seleccionado, snapshot y rehidratación por ref. El perfil data_only debe poder ejecutar las activities y wrappers que Generic/Group efectivamente necesitan, con namespace/cola/targets propios verificados y sin SQCLI. Una configuración inválida del perfil no debe activar por fallback el worker físico. Persiste el resultado de task y StageExecutionResult; `REPORT_PENDING` debe ser recuperable y distinguirse del outcome remoto.
2. **Fuente, definición y fidelidad.** Usa el StageExecutionRef Foundation válido y su protocolo PG/CAS; recupera el snapshot ya sellado antes de volver a seleccionar. Conserva varios EvaluationRefs de una StrategyRef, sus errores por miembro y la versión compatible. Resuelve OUTPUT/STRATEGY_SQX y DEFINITION_REF desde la autoridad exacta; SEALED_REF se liga al miembro correcto. Valida children/scope/result_key/artefactos/hash/conteos y conserva metadata/MetricSets reales. No uses el primer binding global como identidad del cohort.
3. **Historias fieles.** Cada operación fuente conserva su identidad, importe y evidencia temporal/side/scope aplicables. No agregues todos los trades en una operación ni impongas redondeo a dos decimales. No inventes exposición FLAT, cobertura, moneda ni tiempos. Aplica realmente NONE/IF_AVAILABLE/REQUIRED y emite `histories: []` cuando corresponda. Historia canónica y TradeList deben acreditar su scope y presupuestos; el HistoryID y los digests usan la receta completa congelada, sin alias por carpeta ni recorte arbitrario. XML exacto se conserva como artifact separado según B.
4. **Entrega durable y receipt.** Corrige conjuntamente Prepare/binding/FK, bytes canónicos y scope sellado, relectura PG, BeginAttempt, reconciliación GET, estados terminales y transacciones de receipt/refs. Una excepción SQL nunca se convierte en éxito. El retry conserva key/body/versión y no vuelve a Mongo después de Prepare. Reconstruye el expected completo desde el manifest duradero y aplica un único validador compartido de receipt en POST/GET: scope, productor, versión, digest, conjunto de historias, refs/revisión/conteos/source_evidence y snapshots semánticos. El código nativo debe aceptar su propio receipt válido con historias y rechazar uno ajeno o incompleto. Preserva INGESTED; UNKNOWN puede converger a INGESTED validado; no confundir receipt inválido con rechazo autoritativo del request.
5. **Consumidor y Lab.** Integra las validaciones compartidas de SourceEvidence y del manifest SQX en la ruta que recibe el request. Persiste bytes canónicos reales de historias/metadata y acredita sus refs con readback, reutilizando el port mínimo ya indicado. El constructor `art != nil` no sustituye ese trabajo. Lleva cobertura, estado de moneda y tiempos desconocidos hasta el consumidor final del cálculo y screener; añadir campos que nadie lee no cierra EC-06/07. Registro sin historia queda visible y con insuficiencia honesta.

No interpretes M01–M09 como una reducción del alcance: ejecuta la vertical completa y cierra los defectos que afloren dentro de este mandato. Los problemas de wiring, compilación, contrato, fixtures, persistencia o harness son trabajo ordinario del implementador. Si una limitación técnica obliga a pausar la sesión, deja checkpoint inequívocamente parcial dentro de Shot 2 y continúa; no rebautices la pausa como implementación completa ni transfieras esos pendientes al auditor.

#### Evidencia exigida antes de devolver el candidato

- **Gate A completo:** tests propios de los caminos nuevos y negativos críticos, oráculos B O01–O24 y addendum §10 con expected/actual trazables, configuración de Flow ejecutada, fresh+upgrade de migraciones en bases propias, replay/restart/concurrencia y regresiones relevantes. La atribución a baseline de fallos históricos requiere comandos y logs comparables; no exime las pruebas nuevas.
- **Gates B y C ejecutados:** Temporal real, PG/Mongo/MinIO, Gateway y Lab del harness aislado. Demostrar ingesta con historias y sin historias, receipts/readback de revisiones exactas y derivados/insuficiencia. Incluir caída de Mongo después de Prepare, commit+timeout, GET 404 temporal, cancelación, dos ejecutores y errores de persistencia. Guardar evidencias reproducibles de la ruta por el worker real, no sólo llamadas directas al adapter o al mapper.
- **Coverage del código nuevo ≥95%:** publicar denominador, paquetes/archivos, comandos, perfiles y exclusiones justificadas; ningún porcentaje sin artefacto. Añadir goldens cruzados de bytes/errores/refs/digests de SourceEvidence/receipt/manifest desde el módulo efectivamente distribuido, con expected independiente del serializer que se prueba.
- **Gate D:** realizar el intento read-only autorizado de fuente auténtica. Si falta acceso/evidencia, registrar recurso exacto, prueba del bloqueo y qué parte pudo observarse. Tiempo consumido o un bug implementable no son `BLOCKED_EXTERNAL`. No generar campañas ni mover flota para fabricar un PASS.
- **Gate E:** permanece NOT_AUTHORIZED; no merge/release/deploy operativo ni trading. El tag de prueba no cambia esa frontera.

#### Incidente del template PG y aislamiento

El ejecutor reportó DROP y repoblado parcial del template compartido `lab-v4-shot4-20261021/pgdata`, base `echo_labv4_s4`. La afirmación de impacto acotado no fue verificada desde CLOUD. Mantén el incidente explícito, conserva logs y determina mediante lectura el DataPath real, PID/listener, `SHOW data_directory`, bases/schemas afectados, ownership, usuarios concurrentes y estado actual. Un puerto distinto no demuestra otro PGDATA.

Acredita igualmente que el harness propio `harness2/` no comparte ese directorio ni otros targets. No reutilices ni ejecutes DROP, recreación o restauración del template compartido bajo el permiso de esta task. Prepara una recuperación concreta y preservadora; si requiere escribir recursos de otro workspace o propietario, devuelve esa única acción con evidencia y autorización específica necesaria. Continúa el trabajo autorizado en recursos propios. No declares el incidente cerrado porque la base era desechable o reconstruible.

#### Entrega única al manager

Actualiza D con SHAs completos y URLs verificadas, manifest de dependencias/build/runtime, Flow probado, matriz M01–M09 y O01–O24, gates A–E, coverage/goldens, logs de repro y resultado, incidentes y recursos propios conservados/retirados. Separa la evidencia del ejecutor de cualquier futura verificación independiente. Actualiza estado de proyecto/continuidad/change_log y registra el segmento según las herramientas canónicas de Agents-OS, siempre master directo, preservando concurrencia. No cierres Agents-OS ni generes feedback/L0/L1.

Devuelve `FORGE_ECHO_TASK_IMPLEMENTED_LOCAL_CANDIDATE` sólo cuando la terminación y la evidencia exigidas estén reunidas. El Primary Manager adjudica y después despacha Shot 3 a un GLM LOCAL fresco. El verificador final independiente continúa reservado dentro de Shot 4.

### Mandato original — continúa vigente

**ROLE:** TOP LOCAL, según mandato Owner. **Modelo:** GLM-5.3-Flash Max mediante ZCode. **Work function:** implementador e integrador ONE-SHOT. El Primary Manager CLOUD conserva adjudicación y continuidad de los cuatro shots. No eres QA independiente de tu implementación.

### Identidad del programa y rectificación del despacho

**Program ID: `forge-echo-ingestion-task-v2`.** Programa nuevo de la task nativa configurable `echo_ingestion_v2`, gestionado en Echo Forge. Sus cuatro shots son propios de esta funcionalidad.

| Programa | Entrega y estado | Relación |
|---|---|---|
| Echo / Ingestion V2 — Operational Integration | Endpoint, contratos, registry/historias, adapter/persistencia/CLI productor; cuatro shots anteriores ejecutados, VERIFIED_WITH_FINDINGS histórico | Dependencia y baseline. Sus reportes siguen vigentes para su alcance. |
| Forge / forge-echo-ingestion-task-v2 | Resolver fuentes durables → construir DTO → task declarativa Temporal → entrega/recovery → Echo/Lab | Programa nuevo. Diseño adjudicado; candidato Shot 2 recibido y adjudicado INCOMPLETE: continuar su terminación. |

Symphony 22f337ca y Echo f93cd4f8 son resultados consolidados del programa anterior y bases intencionales del nuevo. Crear una feature desde esos commits conserva trabajo verificado; no exige volver a b2b3ebfe/a0c68d1, borrar código ni reejecutar la implementación anterior.

El primer despacho local no pudo cargar el ZIP ni estas autoridades, que aún no estaban publicadas. Esa ausencia fue real; la clasificación posterior como campaña duplicada/stale fue una inferencia incorrecta entre programas distintos. El Owner autorizó después la publicación íntegra. El despacho vigente lee estas rutas desde un commit remoto verificado y no depende de un ZIP.

Si la sesión GLM anterior escribió una memoria que marca este encargo como stale/duplicado, rectificar específicamente esa conclusión conservando la traza y enlazando este mandato. No borrar ni invalidar los reportes históricos de Ingestion V2. La ubicación local exacta de esa marca no fue verificada desde CLOUD; no se afirma haberla modificado remotamente.

**Prueba de alcance en Symphony 22f337ca:** `HTTPIngressV2.Ingest` recibe un DTO ya construido; `sqx/cmd/echo-ingest-v2/main.go` lee ECHO_INGEST_V2_INPUT y decodifica ese JSON. En cambio, los switches de `runGenericSQXWorkflow` y `GroupSQXWorkflow` en `sqx/workflows/generic_workflow.go` no tienen case echo_ingestion_v2, y `sqx/cmd/sqx-worker/main.go` no registra su activity. TaskSpec.Type es string: que pueda deserializar un nombre no significa que el runner lo soporte. Las fuentes exactas están en A y B.

## /goal

Implementar y demostrar localmente la nueva task nativa `echo_ingestion_v2` según el diseño congelado: origen configurable → identidad/evidencia exactas → DTO compartido → manifest durable → HTTP V2 → receipt/readback de Echo → derivados honestos de The Lab.

Terminar con un candidato integrado y reproducible, código real, wiring real, pruebas y evidencia. Estado de entrega: `FORGE_ECHO_TASK_IMPLEMENTED_LOCAL_CANDIDATE`, con gates A/B/C/D separados. El manager adjudicará `FORGE_ECHO_TASK_IMPLEMENTED_LOCAL`. No declarar certificación independiente ni FULL_CERTIFIED.

Resuelve internamente los defectos ordinarios: inspeccionar → implementar → probar → corregir → repetir los gates afectados → entregar un solo paquete completo. No devuelvas al Owner microtareas ni decisiones internas de nombres/paquetes. La implementación aditiva de este programa ya está autorizada; no solicites permiso para rehacer desde cero la campaña anterior, porque no es el encargo.

## /authorities

Si esta sesión ya completó el bootstrap, conserva ese bootstrap y carga sólo las autoridades nuevas. En una sesión fresca, ejecuta bootstrap Agents-OS una sola vez desde `main/AGENTS.md` y `main/80-agents/skills/agents-os-bootstrap/SKILL.md`. Resuelve el vault y los workspaces por sus autoridades; no clones repos de código dentro del vault.

Lee estas autoridades desde el commit remoto exacto indicado en el despacho del Primary Manager y registra ese SHA. Si el checkout local no tiene los archivos, usa fetch y lectura por git show del commit indicado, preservando modificaciones locales. No busques un ZIP por todo el disco ni sustituyas esta SPEC por el antiguo documento D de Echo. Autoridades de este programa:

- `main/10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/A — Source Authority Report.md`.
- `.../B — Frozen Design.md`.
- `.../C — Four Shot Delivery Plan.md`.
- `.../evidence/Contract Source Review.md`, selectivamente para verificar los findings.
- `main/10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum.md`.
- Las notas activas de Echo Forge y Echo, el `F — Decision Register` vigente y `Echo + Echo Forge — Environment Contract`.

En Symphony aplica `CONSTITUTION.md`, `.agents/rules/00-engineering-principles.md`, `02-architecture-independencia-modulos.md`, `03-configuracion-etcd.md`, `13-dynamic-workflow-folders.md`, `14-durable-foundation-only.md` y sus dependencias de desarrollo/verificación. Usa los contratos/SPEC del programa como autoridad; A y el reporte de contratos describen CURRENT, B y el addendum describen TARGET.

La orden específica del Owner prevalece sobre defaults de skills: exactamente cuatro shots; este es sólo Shot 2; GLM-5.3-Flash Max LOCAL implementa; no cierre Agents-OS ni feedback sin orden explícita.

## /baseline

CURRENT_TASK_STATE:

- Nueva task declarativa: NOT_IMPLEMENTED al freeze.
- Source forensics y arquitectura: completados y adjudicados en B; reabrir sólo contradicción material demostrada.
- Symphony: `lab-v4/shot4-symphony@22f337ca434549c492b2d402fd158e23ac4758a8`.
- Master Symphony observado: `dd4af7d05c03db9b39b5467b46e2c2c7d0c1fa19`, ancestro de la base V2; no reemplaza esa base.
- Echo: `lab-v4/shot4-integration@f93cd4f80085e328f9176c1215e42e6c8e0b2404`.
- Adapter/persistencia existentes: `HTTPIngressV2`, `IngestionPersistenceV2`, ControlPlane V2, migración 017, CLI `sqx/cmd/echo-ingest-v2`.
- El tag consumido `v3/sdk/contracts/v0.0.1-lab-v4-shot2.1` apunta a `52f8d509e0e9127a9f263f02d76565dae508a2f6` y **diverge del contrato candidato**. Hay que resolverlo, no mantener el pin como criterio de éxito.
- Baseline Ingestion V2 fue VERIFIED_WITH_FINDINGS histórico; no demuestra esta task ni remite los hallazgos nuevos.

Refresca refs/worktrees y revisa sólo deltas materiales. Crea/reutiliza ramas de ownership propio desde los linajes indicados; nombre sugerido Symphony `feature/forge-echo-ingestion-task-v2`, Echo `feature/forge-task-contract-v2`. Si un nombre ya existe, demuestra ownership o elige uno identificable. Preserva commits y cambios ajenos. No reset, force push, cherry-pick ciego ni integración general de Dynamic Groups/Runtime. No promover a master/deploy por inercia.

Para sostener que esta task ya existe debes demostrar sobre el SHA concreto su configuración tipada, aceptación del TaskSpec, dispatch Generic/Group, activities registradas, resolución automática de evidencia y resultado durable. La presencia del adapter/CLI o un reporte Shot 4 de otro programa no demuestra esa capacidad. Si encuentras un delta parcial nuevo, consérvalo/reutilízalo y completa el alcance.

## /frozen

- KISS, YAGNI, SOLID, clean code; cambios aditivos y acotados.
- `folder/source_folder` son routing opaco. Prohibido deducir stage, productor, versión, evaluación, métricas o provenance de nombres o posición en el array.
- Reutiliza TaskSpec/TaskSource, carriers, StageExecutionResult, stores y resolvers; no ETL framework ni nuevo modelo paralelo de configuración.
- PG posee identidad/control; Mongo durable posee Evaluation/MetricSet/TradeSet; MinIO posee bytes. `databank_metadata/export_runs` no acreditan por sí solos la evaluación final.
- Un único contrato Go desde Echo: DTO, decoder, validator, canonicalización, digest y receipt. Forge → Echo Contracts; nunca Echo → Symphony internals.
- Un solo cliente de ingesta: extender/corregir el existente. No structs ni serializer copiados.
- The Lab calcula curvas/métricas/rankings. Las métricas SQX son evidencia fuente.
- Registro analítico separado de readiness y trading. Scope nativo REGISTER_ONLY según B; ninguna orden ni habilitación.
- Cero timestamps, moneda, costes, Q_i, historia o ciclos inventados. Ausencia no equivale a cero. IF_AVAILABLE no silencia corrupción/ambigüedad/contradicciones.
- Una definición ANALYTIC extraída del XML SQX no acredita ejecución MT5. El hash del archivo .sqx completo no sustituye la definición.
- Retry conserva identidad, key y body. UNKNOWN_RECEIPT requiere reconciliación; no es rechazo.
- La task data-only funciona sin abrir ni exigir SQCLI.

## /scope

Entrega todos los frentes de B dentro de este shot:

1. Fuente configurable y cohort exacto, selección determinista de children de evidencia y validación de terminalidad/lineage.
2. Definición/versión mediante recetas existentes y adapter mínimo del XML acreditado; preservar los bytes XML observados como artifact con hash/ref separados del manifest y de la receta. Metadata y métricas fuente tipadas, valores/ausencias reales y artefactos verificados. Una sola versión compatible por StrategyRef dentro de la task.
3. Historias a partir de trades reales acreditados; múltiples fuentes/scopes conservados; políticas REQUIRED/IF_AVAILABLE/NONE; CREATE_ONLY y REVISION_REQUIRED según B, sin IDs nuevos para eludir conflictos.
4. Extensiones mínimas de productores/read ports necesarias para el camino del Retester y otro productor válido. Verificar Evaluation dentro del StageExecutionResult completado, OUTPUT/STRATEGY_SQX exacto y children de la misma evaluación/estrategia/flow/scope. Conservar result_key acreditado hoy perdido por el TradeSet durable; quitar sólo el guard FinalReretester es insuficiente. Sin acoplar semántica a folder names.
5. Task → runtime/workflow → Activity → puertos/adapters → resultado durable, composición data-only en el worker existente, config ETCD/startup y resultados por estrategia.
6. Snapshot fuente/manifest antes de red, destino/scope sellados, canon/digest, work-item refs y key preservados por Temporal. Recovery carga primero PG, sin reconstruir desde Mongo después de Prepare; persiste receipt/refs atómicos aunque el reporte Foundation quede REPORT_PENDING. Convergencia concurrente y error de reporte separado de outcome remoto.
7. Addendum Echo: registro sin historia, source evidence tipada/readback, receipt compartido y validación estricta, fix del revision digest al reutilizar historia y preservación de evidencia en el loader Lab.
8. Módulo contracts publicado como versión de prueba inmutable, pins alineados y builds fríos independientes. No publicar una versión productiva limpia desde feature.
9. Harness integrado y oráculos del diseño, con regresiones relevantes.

El workstream paralelo Runtime publicó Echo `2daa58daddfbebaf57e2d1c934a25ec644bf0a94` y Symphony `3dfaa5facb96fcc297c062c46ca77085f882cc1c`. No fusionarlo entero. Revisar/reutilizar el write-ahead de artifacts de HistoryInput y metadata en `strategy_history_v2_service.go`/`strategy_history_v2_put.go` mediante port mínimo; exigir artifact store real en la ruta certificada. Contracts, HTTP adapter, persistencia V2 y Lab loader permanecen iguales en los archivos comparados. Echo 087–091 ya existen en ese otro linaje: prevenir colisión antes de asignar migraciones.

No crear DDL, endpoints o infraestructura si el contrato existente basta. Toda migración es aditiva, con identidad/checksum/lineage y prueba fresh+upgrade sobre bases propias. Detecta colisiones con migraciones de workstreams paralelos antes de elegir número; no edites migraciones históricas aplicadas.

## /execute

Puedes coordinar especialistas locales ONE-SHOT con ownership de paquetes claro. Estabiliza primero la interfaz compartida y después paraleliza lo independiente. Conserva el contexto del coordinador local limpio; pide resultados compactos con refs.

Antes de cada ejecución física, demuestra aislamiento: procesos, listeners, base/schema/colecciones, bucket/prefijo, namespace/cola Temporal, ETCD y owner reales. Usa recursos propios del harness y mecanismos existentes. No crees Forge DEV. Echo usa DEV/harness. No hagas suites amplias con posibilidad de escribir ETCD real; inspecciona los seed tests y bloquea egress/targets ajenos.

Lee fuentes auténticas existentes sólo con permisos read-only autorizados. No despaches flota ni crees campañas para fabricar datos de certificación. Si la fuente autorizada no está disponible, demuestra el recurso/bloqueo exacto y continúa A/B/C con fixtures tipados y etiquetados. Un defecto de código o wiring es responsabilidad de este shot, no un bloqueo externo.

No tocar trading real, Echo PROD, servicios compartidos, workers productivos, campañas activas, estrategias en extracción, instalaciones/plugins SQX de flota, datasets oficiales ni migraciones de bases compartidas. No guardar secretos en Flow JSON, Git, reportes ni Agents-OS. Cualquier configuración funcional nueva se carga por el mecanismo ETCD aprobado; el Flow sólo expresa intención y referencias lógicas.

## /verify

Ejecuta pruebas y entrega expected/actual para los oráculos B/addendum. Como mínimo:

- Fuente Full Precision acreditada y misma fuente renombrada a `resultados_finales_2027`; semántica/identidad invariantes. Si se utiliza el tramo productor metadata, el rename cubre ese tramo completo y corrige allí stage=Folder con stage/variant explícitos.
- Otro productor válido; estrategia individual y cohort; mismo display name con StrategyRefs distintos; varias evaluaciones sin latest implícito.
- Metadata exacta del resultado seleccionado; MetricSet/TradeSet faltante, múltiple, inválido, de otra estrategia o de otra evaluación con igual StrategyRef; discrepancia de hashes/conteos/refs/result_key y artifact fuente distinto del binding.
- REGISTER_ONLY sin historia y readback visible; IF_AVAILABLE sólo ante ausencia; REQUIRED falla antes de POST si falta evidencia; cero trades observado diferenciado de no export.
- Moneda/costes/Q_i/FX/tiempos/cobertura desconocidos, costes combinados y parciales preservados sin invención.
- Mismo key/body, key/body conflict, crash antes/después de manifest, POST commit+timeout, GET 404 y recuperación posterior, restart, caída Mongo después de snapshot y dos executions simultáneas.
- Receipt incompleto/ajeno/corrupto, history set/digests/counts incorrectos; GET y POST aplican la misma validación; errores de persistencia no producen éxito.
- Historia existente idéntica con nueva key devuelve revision_digest correcto; contenido corregido produce REVISION_REQUIRED de forma explícita, sin loops ni nueva identidad arbitraria.
- Nuevo SDK descargado desde origen autorizado, checksum y subtree correctos; builds fríos de ambos consumidores, GOWORK=off y sin replace-only de contracts; goldens de bytes/errores/refs/digests con expected independiente. Acreditar también xKoRx/sdk efectivo: GOWORK=off no desactiva replace ../../sdk; fijar su checkout exacto o usar su versión inmutable.
- Temporal real del harness y wiring completo; registry/StrategyVersion/HistoryRevision/receipt/readback; outbox→Lab worker→curvas/perfiles→métricas→rankings/screener y estados de insuficiencia.
- No-regresión de workflows existentes y no-interferencia física. Conservar criterios históricos sin mover budgets.

Funcionalidad crítica primero; código nuevo ≥95% coverage con denominador honesto. No arreglar tests debilitando expected. Un resultado verde propio sólo acredita el candidato de Shot 2.

## /reuse

Conserva tests/probes/harnesses deterministas en su owner existente. Clasifica los activos en PERMANENT_REGRESSION, E2E_CANDIDATE, HARNESS_TOOLKIT_CANDIDATE o DISPOSABLE_REPRODUCER. No crear otro toolkit por nombre. No convertir una consulta source en certificado de runtime.

## /improve

Registra candidatos de mejora repetible sólo si están demostrados; NONE es válido. No amplíes este shot a edición de skills, proceso global o feedback no solicitado.

## /close

No cierres Agents-OS. No crees feedback/L0/L1. Mantén continuidad del programa.

Persiste `D — Implementation Evidence.md` en el mismo directorio Forge, enlazando código y evidencia voluminosa en sus repos/workspaces. Usa skills/templates/materializador del vault. Actualiza proyecto, checkpoint y change_log consolidado en Agents-OS **master directamente**, sin PR ni rama. La divulgación íntegra de este paquete fue autorizada explícitamente por el Owner; conserva los límites sobre secretos y permisos de infraestructura. Registra el segmento con agents-os-agent-run-register; no autoaceptes tu gate.

Handoff único al Primary Manager:

1. Estado exacto y SHAs finales de Symphony/Echo/contracts, ramas, ancestry y source/build manifests.
2. Qué quedó conectado y operativo en el harness; ejemplo de Flow validado.
3. Matriz A/B/C/D/E con evidencia; D bloqueado sólo si está demostrado; E sin autorización.
4. Oráculos con expected/actual, conteos, digests, receipts y readback.
5. Regresiones, coverage, findings residuales y clasificación producto/ambiente/evidencia.
6. Artefactos persistidos y commit documental remoto verificado; citar sólo SHAs comprobados.
7. Recursos propios terminados/conservados, cleanup por ownership y negativos de no-interferencia.
8. Entrada exacta del QA independiente Shot 3.

Si aparece una contradicción material con el freeze, explica evidencia y alternativa mínima al manager. Los bugs ordinarios, problemas de build, tests y wiring se resuelven dentro de este mandato. No entregues una lista de instrucciones para que el Owner termine la implementación.

## Fuentes

- [[B — Frozen Design]], [[C — Four Shot Delivery Plan]] y [[Forge Task — Contract Addendum]].
- Mandato Owner del 2026-10-27; candidato local recibido y continuidad del mismo Shot 2 adjudicada en D.
