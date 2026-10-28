---
type: doc
schema_version: 1
status: active
area: '[[Echo]]'
related:
- '[[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|Echo Forge — Operación Real V2]]'
- '[[10-projects/Echo/Echo — Producto Integrado|Echo — Producto Integrado]]'
aliases: []
tags:
- kind/doc
- area/echo
created: '2026-10-27'
updated: '2026-10-27'
---

# SHOT3 — Independent Adversarial QA Mandate

## Propósito

Ejecutar la revisión adversarial independiente del candidato `forge-echo-ingestion-task-v2` en LOCAL y entregar evidencia reproducible para Shot 4. **Decisión explícita del Owner del 2026-10-27: avanzar a Shot 3, sin más iteraciones de Shot 2.** Las sospechas ordinarias y los pendientes declarados se verifican aquí; las correcciones de producto se realizan en Shot 4, seguido de otro verificador fresco dentro de ese mismo shot.

**Estado de entrada: `SHOT3_READY_WITH_KNOWN_GAPS`.** La admisión habilita la auditoría. No concede PASS a A/B/C/D, no declara cumplido el 95% ni certifica las afirmaciones M01–M08 del implementador. El diseño y el contrato permanecen congelados.

## Contenido

**ROLE:** TOP LOCAL, según mandato Owner. **Modelo/surface:** GLM-5.3-Flash Max mediante ZCode, contexto fresco, sin autoría de la implementación. **Work function:** verificador adversarial independiente. **Necesidades:** repos/builds, MCP soportado, harness y servicios locales aislados. El Primary Manager CLOUD adjudica el informe. Si esta sesión implementó el candidato, no es independiente: este mandato se ejecuta en otra sesión fresca.

### Autoridad vigente y carga de contexto

El Owner corrigió expresamente la secuencia después de recibir la segunda entrega: no desea otra vuelta de Shot 2 y quiere que Shot 3 confirme o falsifique las sospechas. Esta decisión supersede las instrucciones administrativas anteriores «continuar Shot 2 antes de QA» de C, D y SHOT2. No borres sus evidencias históricas ni conviertas la admisión a QA en certificación.

En sesión fresca ejecuta bootstrap Agents-OS una sola vez; si ya está hecho, conserva ese bootstrap. Lee desde el commit documental exacto indicado por el Manager, mediante fetch/git show si el checkout está atrasado y preservando cambios ajenos. No dependes de ZIP. Autoridades:

- `main/10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/B — Frozen Design.md`, especialmente §14 O01–O24.
- `.../C — Four Shot Delivery Plan.md`, estado vigente y cuatro shots.
- `.../D — Implementation Evidence.md`, decisión vigente, segunda entrega y antecedentes M01–M09. Las correcciones narradas son claims del implementador; los defectos del SHA anterior son antecedentes para falsificar en el SHA actual.
- `main/10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum.md`, incluido §10 y EC-01…EC-08.
- A Source Authority selectivamente para lineage/productores; Symphony CONSTITUTION/rules y Environment Contract aplicables. No releer campañas ajenas ni reiniciar arquitectura.

### Candidato congelado para QA

| Superficie | Pin exacto |
|---|---|
| Symphony | `feature/forge-echo-ingestion-task-v2@7731cb844446062f861f04d19dea60a34d425373` |
| Echo | `feature/forge-task-contract-v2@24af786232fa362cc1599df1b9d90b1c8347b557` |
| Contracts | `github.com/xKoRx/echo/v3/sdk/contracts v0.0.1-forge-ingestion-task.2` |
| Tag Git contracts .2 | `v3/sdk/contracts/v0.0.1-forge-ingestion-task.2`, objeto `7496b05b6932517e1d51b757c42cf72dad2cc1bd` → Echo `24af786232fa362cc1599df1b9d90b1c8347b557` |
| Subtree contracts .2 | `cb88aece4f04b648fd724568de3823604dc064ab` |
| go.sum contracts .2 | `h1:t60eoyOjwkkgDNxzkPwLvXYLgf/dFW4xwLuazfvx3u8=`; comprobar descarga efectiva |
| SDK efectivo esperado | `xKoRx/sdk@c7f11496b6f681687c9e1e41a773a13295640351`; verificar el checkout que resuelve `replace ../../sdk` |
| Candidatos anteriores, para atribución | Symphony `07c914251760a938293b7fa7fe4e6d7b4d330640`; Echo `2c66e9402ba96ff354681552587c895ec92f4a28` |
| Bases históricas, para regresión | Symphony `22f337ca434549c492b2d402fd158e23ac4758a8`; Echo `f93cd4f80085e328f9176c1215e42e6c8e0b2404` |

El Manager verificó por API que Symphony avanzó tres commits y Echo uno respecto de la entrega anterior, sin divergencia. El tag .1 conserva el objeto `d24b17b217245c47a33cea810410da41cf6ad978`; .1/.2 son inmutables. La comprobación remota de refs no es cold build ni prueba runtime. Congela un manifest de fuentes, módulos, replacements, toolchain, binarios y configuración efectiva. Si las ramas avanzaron, informa el delta y prueba estos SHAs; no cambies silenciosamente de candidato.

### Frontera de ejecución y trabajo permitido

Puedes crear pruebas adversariales, fixtures etiquetados, fault injection y scripts mínimos de harness, y arrancar los servicios de prueba necesarios en recursos propios aislados. Reutiliza el harness y toolkit existentes cuando su ownership esté demostrado. **Temporal real puede levantarse como dev server o servicio/container local soportado con versión fijada**; su ausencia inicial no obliga a devolver trabajo a Shot 2. No conectes el worker a Temporal/ETCD de flota para suplirlo.

Antes de escribir o arrancar un worker registra endpoints, namespaces/colas, paths reales y symlinks, PID/listener, `SHOW data_directory`, bases/schemas, colecciones y bucket/prefijo. Demuestra que el candidato y las suites usan esos targets y bloquea el acceso accidental a los ajenos. Inspecciona los tests con seed/DDL antes de ejecutarlos. Forge mantiene un ambiente operacional único; aquí se usan recursos propios de candidate/harness, sin inventar Forge DEV. Echo usa harness/DEV autorizado.

El implementador reporta PG propia en `harness2/pgdata`, puerto 56438; verifica su estado actual, no heredes PIDs del informe como prueba. El template `lab-v4-shot4-20261021/pgdata`, puerto reportado 56437, pertenece al incidente y queda excluido de las pruebas y del cleanup. No restaurar, borrar, detener ni reparar ese recurso bajo este mandato. Su alcance permanece reportado, no certificado por esta admisión; no condiciona los casos seguros en un harness aislado.

No modificar código de producto, migraciones aplicadas, contratos ni expected del producto para producir PASS. Conserva los SHAs auditados; desarrolla los tests en un worktree/rama de QA identificable o overlay con diff exclusivo de pruebas/harness. Un bug de producto se reproduce y registra para Shot 4. Puedes reparar el propio harness de prueba, identificando la diferencia y sin simular la función productiva que se quiere verificar.

No PROD, trading, campañas, flota, migraciones shared, resets/force push, reemplazo de SQX/plugins ni release. Si aparece un riesgo grave **concreto** de afectar recursos ajenos o ejecutar sin aislamiento, suspende ese escenario antes de la acción y continúa las pruebas seguras. Un P1 funcional reproducible en recursos descartables es un finding para Shot 4, no una orden de repetir Shot 2.

### Método adversarial y niveles de evidencia

Fija expected y fixture hashes antes de observar el output. Usa fuentes de verdad independientes del mapper/serializer bajo prueba; un fake que devuelve el mismo DTO recibido no prueba fidelidad ni interoperabilidad. Conserva casos positivos y negativos, con conteos de cero efectos remotos antes de POST cuando corresponde.

Distingue unit/fake, integración con stores reales, Temporal testenv y servidor/worker Temporal real. Los gates B/C requieren Gateway/PG/artifact store/Lab reales del harness y readback de la revisión exacta. Cuando un fallo temprano impida un E2E, registra el fallo y prueba las capas restantes mediante entradas controladas identificadas; eso no transforma esas pruebas parciales en E2E completo.

Produce una matriz de **todos O01–O24 y EC-01…EC-08**, más los checks siguientes. Por subcaso usa PASS, FAIL, BLOCKED o NOT_RUN con justificación; vincula M01–M09 como confirmado, falsificado o pendiente sobre el candidato actual. No heredes ni el PASS del implementador ni los P1 del candidato anterior.

### Oráculos prioritarios: fuente y fidelidad

1. **Operaciones preservadas.** Dos o más trades con IDs, lados y tiempos distintos, ganancias/pérdidas/cero y decimales con precisión mayor a dos posiciones. Comprobar una operación por trade, presencia/valor exactos conforme al contrato numérico fuente, sin agregación/redondeo arbitrario, sin FLAT ni desglose CommSwap/Q_i/FX fabricados. Verificar MetricSets reales, unidades, ausencias y provenance del productor; source metrics permanecen separados de Lab. Incluir un test manual cuyo expected no salga del serializer candidato.
2. **Identidad y scopes.** FULL/OOS, result_key y cell_key distintos dentro de una evaluación producen historias distintas conforme a la receta; una corrección del mismo run conserva history_id y CREATE_ONLY devuelve REVISION_REQUIRED. Dos estrategias con igual display name y bindings versionales diferentes no se mezclan. Varias evaluaciones compatibles de una estrategia se conservan; incompatible/ambigua falla sin latest implícito.
3. **Políticas y corrupción.** REQUIRED sin TradeSet falla sin POST; IF_AVAILABLE degrada sólo ausencia acreditada; NONE omite economía deliberadamente. TradeSet presente corrupto, moneda no acreditada, hijo de otra evaluación/estrategia/flow, counts/hash/size/result_key discrepantes y payload excesivo fallan de forma localizada. Cero observado se distingue de ausencia. CANONICAL_HISTORY valida también identidad/scope y límite de descompresión.
4. **Definiciones y otro productor.** SQX exacto: mismo XML en otro ZIP conserva versión ANALYTIC; XML cambiado cambia identidad; ZIP/XML duplicado/corrupto/trailing/exceso falla. DEFINITION_REF y CANONICAL_HISTORY funcionan desde productor tipado sin SQX, sin degradarse al constructor SQX. SEALED_REF se liga al item correcto; todas las evaluaciones de la estrategia acreditan una versión compatible.
5. **Foundation y routing.** Usar PG/Mongo/MinIO reales para selección/snapshot/readback. Verificar identidad Foundation y enlace StageExecutionResult, snapshot previo a red y recuperación sin reseleccionar. Renombrar routing a `resultados_finales_2027` mantiene la semántica; si se usa el tramo metadata productor, cubrir ese tramo y sus stage/variant explícitos, etiquetando por separado cualquier productor fixture.

### Oráculos prioritarios: orquestación y entrega

1. **Worker real.** Generic y Group en data_only, sin SQCLI instalado, recorren lifecycle → resolve → batch → finalize; registrar actividades, FlowRun/StageExecution y resultado persistido. Perfil/destino inválido, dependencia ausente o task física fallan antes de publicar. Dos destinos usan sus propios endpoints/scopes.
2. **Fuente nombrada.** A → B → ingesta `source.task=A` consume A, aunque current sea B. Repetir en root/group, input inicial, scopes con nombres repetidos y referencias futuras/ausentes. Historial Temporal y snapshot deben demostrar los conjuntos esperados de refs.
3. **Fresh y upgrade verdadero de migración018.** El diff remoto demuestra que 018 fue modificada entre entregas. En dos bases propias prueba la cadena candidata Fresh y la actualización desde el candidato `07c9142` con su 018 original ya aplicada y filas de control. Conserva ledger/checksums. Ejecuta Prepare/aceptación/recovery también sobre Upgrade. Un rechazo de checksum o un esquema antiguo omitido es finding reproducible; no borrar ledger, cambiar checksums, reaplicar artificialmente la 018 editada ni resetear para llamarlo upgrade. Un fallo de Upgrade no impide el resto del QA seguro sobre Fresh. Las migraciones Echo001–086 no sustituyen esta prueba Symphony.
4. **PG-first y caída de Mongo.** Tras ACK de Prepare, cortar Mongo y reiniciar/reintentar por refs. Manifest/key/body/scope se cargan desde PG antes de releer fuente; el delivery y receipt/refs convergen sin Mongo. UNKNOWN usa GET primero; INGESTED no hace otro POST. Al recuperar Mongo, REPORT_PENDING se persiste sin otra ingesta ni nueva selección.
5. **Crash, ambigüedad y concurrencia.** Gateway real con proxy/fault hook: commit remoto y pérdida de respuesta; crash después de BeginAttempt; GET404/error/auth scope cambiado; dos entregas de la misma key/body; misma key/body distinto. Una ingestión lógica y receipt convergente, estado/refs atómicos, sin downgrade por error tardío. Los contadores corresponden a llamadas reales. Receipt ausente/ajeno/alterado no acredita aceptación y tampoco prueba por sí solo rechazo económico.
6. **Resultados y budgets.** Cohort con delivered/rejected/pending/unknown, CONTINUE y FAIL_AFTER_BATCH, lentitud/cancelación/heartbeats/timers/backoff. Verificar ecuación de conteos, límites y persistencia Foundation con ACK; FAIL_AFTER_BATCH sólo después del reporte. Inyectar fallo de reporte luego de aceptación PG y demostrar recuperación sin reingesta. No admitir un struct retornado como prueba de reporte durable.

### Oráculos prioritarios: Echo, contratos y Lab

1. **Corpus distribuido/goldens.** Construir corpus fijo para ambos consumidores sobre contracts .2 descargado: bytes, digests, refs y errores con expected independiente. SourceEvidence válido y negativos de schema, hijo ajeno, ref repetida con digest contradictorio entre evaluaciones, orden, value/availability, campo anidado desconocido y decimal no canónico. Verificar el wrapper payload_artifact y que el envelope rechaza antes de SQL/artifact writes aun con digest exterior válido.
2. **Receipt y cero historias.** REGISTER_ONLY con `histories: []`, MISSING/NO_HISTORY y NOT_REQUESTED/HISTORY_NOT_REQUESTED. Ausente/null falla. Receipt, GET-by-key/by-id, versión/metadata y screener/detalle deben ser coherentes, sin History/Revision/outbox/score/rank/curva ficticios. Segunda evidencia para la misma versión exige selección explícita o alternativas; no latest por reloj. Validar en POST/GET scope/productor/key/digest/versión/conjunto y facts por historia/source-evidence/snapshots; expected nativo incompleto debe rechazarse.
3. **Manifest SQX en Gateway.** XML exacto/byte cambiado, hash interno incorrecto con digest exterior correcto, trailing, campos desconocidos y límite canónico completo 262144/262145 bytes incluidos wrapper/escapes. Los negativos fallan antes de persistir. Otro schema legítimo definition-v1 conserva su contrato; el dispatch SQX no lo invalida.
4. **Economía y moneda.** Summaries 10, −4 y 0 acreditados contribuyen una vez y suman 6; movimientos no duplican ese neto. CommSwap combinado, costes desconocidos y ausencia Q_i/FX mantienen insuficiencia donde corresponde. OBSERVED/DECLARED/UNPROVEN conservan estado/evidencia hasta el cálculo; no hay comparabilidad multimoneda inventada ni elevación de DECLARED a OBSERVED.
5. **Cobertura y tiempo.** Misma economía con COMPLETE/PARTIAL/GAP interno y observed_through distintos debe tener cobertura/bins/elegibilidad justificados por evidencia. Min/max de actividad no acredita COMPLETE. UNKNOWN economic_at no se vuelve epoch0; UNKNOWN known_at no se trata como conocido siempre en AS_KNOWN; hechos posteriores al corte se excluyen. ExistingRef sin redeclaración conserva temporalidad. Verificar la revisión pinneada, no una cabeza mutable posterior.
6. **Artifacts y Lab real.** Recuperar accepted_body_artifact y canonical_artifact de historia/metadata, verificar bytes/hash independientes y contenido exacto. Store fallido impide commit, aunque pueda quedar objeto huérfano por write-ahead. Demostrar outbox → worker → generación → curvas/perfiles posibles → métricas/ranking/screener; incluir suficiencia positiva y ausencia honesta. No declarar cuatro curvas completas cuando falten datos que las acrediten.

### Cobertura, regresión y gate D

El implementador reportó **68,0% como promedio de 85 funciones**, bajo el piso. Eso no queda adoptado como cobertura Go validada. Captura coverprofiles, scope de archivos/paquetes nuevos, exclusions y statements; deduplica bloques al combinar perfiles y calcula `statements cubiertos / statements totales` del scope. No promedies porcentajes por función ni excluyas caminos nuevos porque requieran E2E. Mantén visible el requisito Owner ≥95%. QA puede añadir pruebas valiosas y medir su contribución; el déficit residual se adjudica a Shot 4, sin abrir otra vuelta de Shot 2 ni inflar tests espejo para alcanzar el número.

Reejecuta regresiones pertinentes, incluido el delta compartido en contracts/history/runtime binding y los workflows existentes. Atribuye fallos a baseline sólo con comando/config/fixture equivalentes sobre el SHA apropiado; un fallo histórico no exonera otro defecto nuevo. Si el candidato no compila o no arranca, conserva el bloqueo reproducible, revisa las capas aún comprobables y entrega el alcance real de auditoría; no corrijas producto para ocultarlo.

Gate D está pendiente de fuente auténtica. El implementador reportó MCP expirado (`session not found`) y un conteo de 515 receipts del harness: **ese conteo no acredita fuente Forge auténtica**. En la sesión fresca descubre/reinicializa sólo los canales soportados por su protocolo normal, con acceso read-only autorizado; no reutilices IDs expirados ni eleves permisos. Si no hay acceso, registra recurso, capability, error y parte observada; BLOCKED_EXTERNAL de D no bloquea A/B/C con fixtures identificados. No crear campaña/export físico ni mover flota para fabricar D. El incidente PG sólo recibe lectura acotada si hace falta comprobar aislamiento; su restauración queda fuera del mandato.

### Informe de salida y siguiente shot

Persiste **`E — Independent Adversarial Report.md`** en este mismo directorio Forge, con materializador/template canónicos. Código de tests, fixtures, logs y evidencia voluminosa van en sus repos/workspaces de QA; Agents-OS conserva manifest, localizadores, hashes, conclusiones y continuidad, en master directo con protección de concurrencia.

Entrega una única revisión con:

1. Identidad del auditor independiente y manifest exacto de source→dependencies→build→runtime; refs remotas de candidato y QA; no modificaciones de producto ocultas.
2. Preflight de aislamiento y recursos propios, incluidos Temporal real y prueba sin SQCLI; incidentes o partes detenidas por riesgo concreto.
3. Matriz O01–O24/EC-01…08/M01–M09 con fixture/hash, expected independiente, actual, comando/exit, refs/digests/readback y estado por subcaso.
4. Gates A/B/C/D/E separados. E sigue NOT_AUTHORIZED. D sintético nunca se etiqueta auténtico.
5. Coverage reproducible, goldens, regresión/atribución y límites reales; no inferir un PASS global de suites parciales.
6. Findings con ID estable, severidad, frontera/archivo/función, reproducción mínima, impacto, expected/actual, owner de corrección y test de cierre. P0 es riesgo grave acreditado; P1 rompe contrato/capacidad, P2/P3 según impacto demostrado. Separar producto, harness, ambiente/acceso y evidencia.
7. Paquete directo para **Shot 4: correcciones y luego verificador final fresco dentro del mismo shot**. Conservar pruebas valiosas como PERMANENT_REGRESSION/E2E_CANDIDATE/HARNESS_TOOLKIT_CANDIDATE/DISPOSABLE_REPRODUCER según su uso; no crear otro toolkit por nombre.

Resultado `FORGE_ECHO_TASK_ADVERSARIAL_REVIEW_COMPLETE` sólo si la revisión completó el alcance que declara; puede contener findings bloqueantes y gates FAIL. Si quedan casos inaccesibles, reporta REVIEW_INCOMPLETE/BLOCKED con matriz exacta; no inventes ejecución ni solicites automáticamente una nueva vuelta de Shot 2. El Manager adjudicará el alcance y llevará el trabajo al Shot 4 según la orden Owner. La preparación CLOUD de este mandato no cuenta como Shot 3 ejecutado.

No cerrar Agents-OS, no generar feedback/L0/L1 ni tocar cuota por estimación. Registra el segmento de QA según las reglas canónicas y deja la continuidad abierta. No hay Shot 5.

## Fuentes

- Orden Owner de avanzar a Shot 3 sin más iteraciones de Shot 2, 2026-10-27 (America/Santiago).
- [[B — Frozen Design]], [[C — Four Shot Delivery Plan]], [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/D — Implementation Evidence|D — Implementation Evidence]] y [[Forge Task — Contract Addendum]].
- [Symphony candidato](https://github.com/xKoRx/symphony/commit/7731cb844446062f861f04d19dea60a34d425373), [Echo candidato](https://github.com/xKoRx/echo/commit/24af786232fa362cc1599df1b9d90b1c8347b557) y [tag contracts .2](https://github.com/xKoRx/echo/tree/v3/sdk/contracts/v0.0.1-forge-ingestion-task.2/v3/sdk/contracts).
