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
created: '2026-10-28'
updated: '2026-10-28'
---

# SHOT4 — Correction and Final Verification Mandate

## Propósito

Cerrar el programa `forge-echo-ingestion-task-v2` mediante **correcciones completas y después verificación final independiente dentro del mismo Shot 4**. La task es `echo_ingestion_v2`. Se recibe Shot 3 con findings y alcance parcial; no se devuelve a Shot 2, no se abre otra vuelta de Shot 3 ni se crea Shot 5.

**Estado vigente: SHOT4_BLOCKED; cierre e integración a pruebas autorizados según la primera sección del Contenido.** Estado histórico de entrada: SHOT4_READY_WITH_ADJUDICATED_FINDINGS. El diseño B y el addendum Echo permanecen congelados. Este mandato adjudica las nueve correcciones de E, sus criterios de cierre y la evidencia que aún falta. No declara el producto verificado ni concede release.

## Contenido

### Cierre final e integración E2E — 2026-10-28

**Mandato vigente del Owner:** terminar lo que falte, comprobar el candidato con una última verificación con correcciones e incorporarlo al linaje de Forge que participa en los E2E actuales. Se continúa el MISMO Shot 4. No se reabre Shot 2/3 ni se crea Shot 5. Este bloque supersede las instrucciones de cierre y los launchers anteriores que lo contradigan; B y el Contract Addendum siguen siendo las autoridades funcionales.

**Rol/superficie:** TOP LOCAL, integrador y corrector/coordinador. Necesita repos, Go, runtime local y canales RO soportados. Después interviene un verificador LOCAL de contexto fresco y sin autoría sobre el candidato final. Puede compartir máquina/harness con ownership claro; no compartir autoría de las correcciones que adjudica.

**Adjudicación de recepción: SHOT4_BLOCKED; integración a pruebas autorizada como candidato, cierre aún pendiente.** Se verificaron publicaciones y se inspeccionó fuente, no runtime desde CLOUD. El porcentaje 80,12% sigue siendo evidencia declarada del corrector; falta veredicto independiente publicado. El positivo Lab está incompleto respecto de B§11/14. Además se confirmó una desviación de source_instance_ref y la dependencia externa del SDK corregido. No basta con repetir el harness anterior ni con aumentar cobertura sin integrar la ruta actual.

#### 1. Entradas exactas y continuidad

Leer A, B, C, D, E, F y el Contract Addendum desde la revisión documental de este despacho. Bootstrap Agents-OS una vez por sesión nueva; en continuación caliente no repetirlo. Respetar AGENTS/contratos de cada repo. Mantener Agents-OS abierto, sin feedback/L0/L1 ni cierre de sesión.

Refs remotas verificadas al preparar este mandato:

| Superficie | Ref | SHA |
|---|---|---|
| Ingesta Symphony | shot4/forge-echo-ingestion-task-v2 | 0417330a9d1ab9c8639d8f449f6d65548382f0e1 |
| SDK con fix métricas | shot4/telemetry-optional-metrics | be85d144b7dfcc8e82941c2ee0de26082de60b85 |
| Forge E2E, linaje de certificación | codex/forge-cert-replay-oneshot | 36071d819b1532cade14ce06ad691d0d33856772 |
| Symphony master | master | dd4af7d05c03db9b39b5467b46e2c2c7d0c1fa19 |
| Echo baseline del programa | feature/forge-task-contract-v2 | 24af786232fa362cc1599df1b9d90b1c8347b557 |
| Echo master, contiene ese baseline | master | 347eee8bdab7f7628629af6383d1e45520815abd |
| SDK master, ancestro de be85d144 | master | c85594440f6755443ceb97ec4e333cd0ddb5b0ed |

Contracts .2: tag completo `v3/sdk/contracts/v0.0.1-forge-ingestion-task.2`, objeto 7496b05b6932517e1d51b757c42cf72dad2cc1bd, commit Echo 24af786232fa362cc1599df1b9d90b1c8347b557, subtree cb88aece4f04b648fd724568de3823604dc064ab. .1/.2 son inmutables.

Refrescar refs y preservar descendientes/cambios concurrentes. No resetear a los SHAs históricos. La línea real es 7731cb8 → d760dc3 → 0417330; F invirtió una descripción de ancestry. Workspace previo: `~/aranea/work/forge-echo-task-v2-20261027/`; evidencia s4c-stack y QA preservada d70c171a/8270676b. Recuperar el job/session/resultado del verificador anunciado en background antes de lanzar otro. La F recibida en Agents-OS 032095c6 todavía dice NO despachado y no contiene su veredicto: discrepancia documental, no prueba de que el proceso esté muerto. Si escribió correcciones/tests para subir el piso, registrar esa contribución como corrección y conservar una verificación posterior sin esa autoría.

#### 2. Integrar contra el Forge que se prueba ahora

El linaje cert-replay y el de ingesta divergen desde master: +58 y +15 commits respectivamente en el corte. El JSON E2E w12R declara execution_contract=dynamic-groups.v1. Verificar LOCAL, en lectura, rama/SHA, binarios/SDK efectivos, workflow/run IDs, queue/namespace, config, owners y estado de la corrida actual. Los commits dicen 0.4.2/w12R; no equivalen a readback runtime. Las instrucciones históricas de teardown/PIDs/restauración 0.3.2 en cert-replay pueden estar stale: no ejecutarlas contra procesos actuales.

Crear worktree y rama de integración propios desde el head fresco acreditado del linaje E2E, incorporando el candidato nativo mediante merge normal o commits trazables que preserven ambas historias. No sobrescribir la rama de otra sesión ni resolver conflictos eligiendo todos los archivos de un lado. Revisar los deltas concurrentes de workflows/config/main/stage_execution/migrator/dependencias; preservar Dynamic Groups y los fixes E2E existentes.

**Integración obligatoria:** el dispatcher compartido `sqx/workflows/task_dispatch.go` de cert36071d no contiene echo_ingestion_v2. Generic con ExecutionContract usa runRootTaskSequenceV2 y omite el switch legacy. Incorporar la task al camino raíz/grupo/anidado actual; preservar ExecutionScope, TaskPath estructural, TaskResult/accounting, carriers, selección y outputs por nombre, incluidos límites de grupo y ContinueAsNew aplicables. Conservar compatibilidad de Generic/Group legacy. Registrar capacidades sólo donde el contrato de bindings lo exige: no inventar un requisito de InputBindings para toda task ni una dependencia de SQCLI en ingesta. Probar configuración válida, admisión y ejecución de la nueva task por la ruta dinámica real.

**Migraciones:** cert-replay aporta 017_stage_execution_identity_v2 y 018_group_partition_runs; ingesta aporta 017_ingestion_v2_persistence, 018_ingestion_v2_delivery_state y 019_ingestion_v2_delivery_state_reconcile. El ledger usa el FILENAME COMPLETO, no el prefijo numérico; no hay colisión automática sólo por compartir 017/018. Preservar nombres/SQL ya aplicados, reconciliar ordered/dependencias y añadir reconciliación sólo cuando el shape la requiera. Verificar con PG propias: fresh boot normal, upgrade desde cada linaje histórico (incluida 018 antigua de 07c9142), conservación de filas, equivalencia de esquema y boots concurrentes. No borrar ledger, renumerar migraciones aplicadas ni usar DDL manual como evidencia del boot de producto.

Echo master ya contiene 24af7862 y 118 commits posteriores en el corte. No reintegrar ese baseline a ciegas ni hacer downgrade. Seleccionar el Echo efectivo compatible para la matriz final, conservar 24af como baseline reproducible y probar contra la revisión actual pertinente. No equiparar master con runtime desplegado.

#### 3. Corregir identidad y distribución del candidato

**QA-S3-02 reabierta en el subcaso de instancia configurada.** B§6.1/8.3 exige source_instance_ref de la identidad de productor configurada, sellada en SourceSnapshot. En 0417330, echoDestinationProfile sólo carga namespace/writer y echoSourceInstanceRef fabrica `task_output:<task>` o FlowRunRef según Source.Type. exact_evaluations/input_cohort terminan en `task_output:`. Ese valor participa en history_id y en la validación canónica.

Conectar la autoridad de configuración al snapshot/binding/mapper y fallar cerrado si falta; no derivarla de selector, carpeta ni task name. Prueba obligatoria: misma evaluación, TradeSet, versión, run y scope seleccionados por los cuatro modos conservan instancia configurada e identidad económica. Un payload de otra instancia que contradiga la instancia sellada rechaza antes de Prepare/POST. La key del selector puede tener su semántica propia; no exigir igualdad de keys que B no manda. Para manifests ya sellados, recovery conserva exactamente autoridad/key/body; no reescribirlos con la nueva identidad para eludir conflictos.

**Run canónico:** el código compara siempre payload.RunRef con member.FlowRunRef. Acreditar esa equivalencia sólo para el contrato productor que la declara. B§6.1 exige el run real del payload y prohíbe generalizar identidades. Cuando un contrato ya admitido permita un run económico distinto del FlowRun, probar ese positivo; si los contratos admitidos acreditan igualdad, probar esa autoridad y el rechazo tipado de contratos no soportados. Probar siempre run ajeno de la misma instancia y ausencia declarada conforme al contrato. No corregir el fixture cambiando run-1 por flow-1 para satisfacer una suposición ni quitar el contraste de identidad. Preservar decimales, operaciones, SourceEvidence, typed-null fix y oráculos M04.

**SDK y módulos:** raíz/sqx aún declaran c7f11496 y reemplazos ../sdk o ../../sdk; el fix está en be85d144. GOWORK=off no desactiva replace. Fijar require/version inmutable resoluble del fix y la resolución efectiva de TODOS los módulos consumidores. Si el layout del repo conserva replaces, publicar manifest/bootstrap que obtiene exactamente el SDK declarado y falla ante checkout divergente; demostrar además resolución limpia del módulo publicado sin dependencia accidental del sibling/cache. Usar la convención existente, sin reestructurar el monorepo. Verificar go list -m -json, go.sum, MVS/exclude contracts .2, shared-analytics y go version -m de los binarios. SDK master hoy es ancestro del fix; si el SDK operacional fuese un descendiente posterior, preservar ese avance e incorporar sólo el delta necesario. Repetir métricas/tracer apagados y encendidos con el SDK final.

#### 4. Completar calidad sobre el candidato integrado

El corrector termina los tests y arreglos antes de entregar al verificador. Recuperar covunion4.py/perfiles/manifiesto y auditar el scope contra el diff real. El 80,12%=1499/1871 sólo describe el delta Symphony declarado; con ese denominador fijo faltan al menos 279 statements cubiertos para 95%, no los 372 necesarios para 100%. Recalcular tras cada cambio material de fuente.

Mantener ≥95% por statements del código nuevo del programa con scope explícito por repositorio: task Symphony, addendum Echo, fix SDK y adaptaciones de integración. Incluir funcionalidad nueva en archivos existentes/wiring/main; separar legado ajeno y harness. No inventar 95% por archivo ni por cada repositorio, ni diluir la medición agregando legado cubierto. Matriz por repo/archivo y agregado inequívoco; archivos/rutas no ejercitados cuentan cero. NumStmt, unión de hits sólo entre bloques compatibles del mismo código/toolchain, sin duplicar denominadores, promedios de funciones ni selección de perfiles favorables. Instrumentar procesos/subprocess para boot/os.Exit; no excluirlos como no-unit-testeables. Publicar scripts y evidencia sanitizada reproducibles, sin binarios, secretos ni dumps.

Priorizar pruebas con expected y efectos observables: identidad/run, corrupción de mapper, límites, errores de resolver, entrega/recovery y boot/wiring. Confirmar que tests Mongo/PG/wiring no hicieron skip. Reutilizar regresiones útiles, sin tests vacíos que sólo inflan coverage. Atribuir fallos de legado al baseline E2E actual con mismo comando/config; no usar indiscriminadamente el antiguo 22f para absolver regresiones de la integración. No cerrar la sesión de corrección sólo por llegar a una cifra mayor que 80%.

#### 5. Última matriz funcional y Lab completa

Usar recursos propios o ownership lógico demostrado; s4c es una opción si está libre y su configuración efectiva corresponde al manifest. No tocar stores de otra sesión, el PG del incidente ni Kafka DEV compartido. Ejecutar el binario final integrado con Foundation/Temporal/Gateway reales. No repetir pruebas ya suficientes salvo para validar cambios relevantes o la nueva combinación.

Completar O01–O24 y EC01–EC08 con matriz de expected/actual, comando, exit, fixture/hash, fuente/binario/config, refs y readback. Casos mínimos críticos: raíz/grupo legacy y dinámicos/anidados; cuatro selectores y tres modos de versión; cero historia legítimo; economía por operación; SDK opcional; snapshot estable; conflictos; receipt estricto; dos workers; REPORT_PENDING y recovery sin reingesta. Para crash/timeout acreditar fronteras deterministas de snapshot, manifest, commit Echo y receipt; un SIGKILL mid-run genérico no sustituye POST que commiteó remotamente antes del timeout. Expected escrito antes de observar el resultado.

**Gate C:** mantener los positivos net=6/PF=2.5 y las insuficiencias honestas. Completar el requisito YA congelado en B§11/14: fixture suficiente con Q_i causal/moneda/FX/tiempo acreditados, cuatro perfiles y dos rankings pertinentes, targets/cohortes concretos y orden/valores esperados. Cero targets no demuestra ranking funcional. Readback de HistoryRevision→outbox→generación PUBLISHED→curvas/métricas/ranks/screener. Probar cero historias visible sin placeholder/curva/score; COMPLETE/PARTIAL/GAP, known_at/economic_at UNKNOWN y cortes temporales sin look-ahead. No convertir ausencia de datos en ceros, motivos vagos ni positivos simulados como auténticos.

#### 6. Participar de los E2E y resolver D cuando sea posible

Además del fixture, aprovechar outputs reales ya COMPLETED/sellados del E2E actual como fuente read-only, por refs exactas: StageExecutionResult + Evaluation/TradeSet/MetricSet + artifact/hash/producer contract. No latest mutable, no carpeta como autoridad, no re-selección oculta. Ejecutar ingesta opt-in con IDs, namespace/cola, destino y stores propios. Puede cerrar D sin modificar la corrida física en curso. Guardar origen auténtico, cadena de custodia y readbacks sanitizados; si el perfil MT5 no tiene contrato soportado, devolver UNSUPPORTED_SOURCE_CONTRACT sin convertirlo silenciosamente en SQX.

Demostrar también un nuevo flujo opt-in por el dispatcher dinámico del candidato integrado. Se puede alimentar de carriers sellados propios; no necesita reiniciar la campaña física completa. Usar las interfaces existentes para la lectura autorizada. Si el conector Mongo expiró, hacer el refresh/reconexión soportado o utilizar un reader existente con autorización vigente; no eludir credenciales. Si la fuente auténtica sigue inaccesible, D=BLOCKED_EXTERNAL con recurso/operación/error exactos. Legacy/no-V2 sólo describe deployment. No FULL_CERTIFIED con fixtures.

#### 7. Verificador fresco y destino de integración

Congelar y publicar por push normal el candidato integrado y su matriz SDK/Echo/contracts; build frío y hashes. Después, verificador fresco sin autoría reconstruye ese candidato, escribe expected independientes y comprueba findings, cobertura y matriz crítica. Los tests del corrector son regresiones reutilizables, no su única autoridad de expected. Si descubre fallo, vuelve al corrector dentro del MISMO Shot 4; verificar el descendiente corregido antes de adjudicar. Si el despacho falla, guardar launcher/SHAs/error concreto; no declarar auditoría completada ni inventar resultado.

La petición actual autoriza preparar/publicar y probar la integración con la versión E2E de Forge. Usar rama de integración propia desde el target acreditado, con todo resuelto y commit verificable. Si la incorporación al target de pruebas puede realizarse por el procedimiento ordinario autorizado, sin activar despliegues/campañas ni alterar trabajo concurrente, efectuarla después de gates y releer head/ancestry. No pedir de nuevo permiso para worktrees, fixes, tests, push normal de candidato o preparar un PR/diff de integración. Si promover el target implica shared migrations, reemplazar binarios de la corrida en curso, branch protection o release/master aún no autorizado para ese efecto, completar primero candidato/PR y dejar únicamente esa acción concreta pendiente con razón/impacto. No force push ni bypass de protecciones. Master/release no se presume certificado por el éxito de la rama de pruebas; E sigue NOT_AUTHORIZED salvo autorización específica ulterior.

#### 8. Entrega única y registro honesto

Actualizar F con secciones separadas de corrector y verificador, SHAs finales/remotos, target E2E base/final, matriz de dependencias, identidad/migraciones, cobertura reproducible, A/B/C/D/E, refs auténticas usadas y estado de integración. No describir como único bloqueo la cobertura mientras falte evidencia o revisión. Conservar el reporte previo atribuible; corregir ancestry y precisión de Kafka: -1001 significa ausencia observable de offset en esa consulta, no prueba que nunca hubo commits/efectos. No abrir otra auditoría Kafka si no aparece evidencia nueva.

Actualizar C, continuidad y estados de Forge/Echo sin pisar otros workstreams; Agents-OS master directo con lectura reciente/conflicto optimista y readback. Registrar agent_run de la ejecución material. Entregar hechos concretos: qué corrigió, qué probó, qué se integró y dónde; cualquier pendiente externo con su acción exacta. No autocertificación del corrector. El cierre puede quedar READY_FOR_MANAGER_REVIEW con D bloqueado de forma demostrada, pero no VERIFIED/FULL_CERTIFIED por decreto. Mantener sesión Agents-OS abierta.

### Continuación previa tras F — 2026-10-28 (histórica; supersedida por el cierre final)

**Orden vigente del Owner: resolver los bloqueos posibles y continuar con un único despacho ejecutable.** Se continúa el mismo Shot 4, primero como corrector de lo pendiente y después con verificador fresco sin autoría. No reiniciar Shots 1–3 ni crear otro shot. El launcher inicial de F §5 queda supersedido: no trasladar al verificador una entrega aún pendiente de cobertura y Gate C.

El Manager recibió F y la bitácora completa del corrector. Las correcciones y el E2E Generic/Group+Gateway son resultados declarados por éste; no verificación independiente. La comprobación remota encontró la feature Symphony aún en `7731cb844446062f861f04d19dea60a34d425373`, sin ref `shot4/forge-echo-ingestion-task-v2` y sin resolución del commit `d760dc3` (404 de ref / 422 de commit); Echo sigue `24af786232fa362cc1599df1b9d90b1c8347b557`. El candidato avanzado permanece LOCAL según F. CLOUD no dispone del workspace KoR ni canales de runtime para publicarlo, medirlo o ejecutar Lab; no ha reconstruido código a partir del relato.

#### Decisiones de alcance ya resueltas

- **Coverage:** ≥95% rige statements del código nuevo de la task, incluida composición nueva en wiring/main y adiciones en archivos existentes. No falta decisión Owner para incluirlos. El legado completo se informa aparte; no se exige llevar todo generic_workflow histórico al 95% ni se permite excluir su delta nativo para mejorar el número.
- **Métrica:** F §4 cuenta 1808/3227 bloques. Ese 56,0% queda reportado como proporción de bloques, no adoptado como cobertura por statements. Calcular `sum(NumStmt de bloques cubiertos) / sum(NumStmt del scope)`; publicar conteos por archivo, perfiles/hashes, comandos y scope. Unir hits sobre bloques compatibles sin duplicar denominador. Regenerar medición coherente si difiere la segmentación; no elegir el perfil favorable ni el primer binario. Las rutas no ejecutadas conservan cero. Un runtime sin instrumentación no añade coverage.
- **Roles:** completar código, tests faltantes, Lab y evidencia del corrector antes de la verificación final. Independencia exige contexto fresco y ausencia de autoría; no exige otra máquina. Se puede usar el mismo harness identificado, con ejecución secuencial y ownership claro. Si no hay capacidad de lanzar otro agente LOCAL, entregar su launcher con pins publicados; no convertir esa limitación de despacho en un defecto del producto ni declarar verificación ejecutada.
- **D:** legacy en ETCD y ausencia de tablas V2 describen despliegue. No prueban ausencia de dataset Forge ni necesidad de desplegar en PROD. D sólo puede quedar BLOCKED_EXTERNAL por recurso/operación de fuente concretos inaccesibles tras el intento RO soportado. Ese bloqueo no impide cerrar A/B/C con fixtures ni preparar revisión gerencial con límites; no permite FULL_CERTIFIED.

#### Orden de ejecución del one-shot LOCAL

**1. Recuperar y fijar el candidato real.** Localizar `shot4-symphony` y la rama `shot4/forge-echo-ingestion-task-v2`; resolver el SHA completo de `d760dc3`, revisar estado/diff/ancestros y preservar cambios concurrentes. Si la rama avanzó, documentar el delta y elegir un descendiente coherente; no resetear a `7731cb8` ni rehacer los fixes. Preservar QA `d70c171a`/`8270676b` y sus manifests. Publicar mediante push normal sin force la rama candidata y las refs QA que correspondan; comprobar remote SHA y material reproducible. No subir binarios, datos, credenciales ni logs brutos. Mantener contracts .1/.2 inmutables; SDK esperado `c7f11496b6f681687c9e1e41a773a13295640351` con reemplazo efectivo verificado. Una rama sólo local no basta para el handoff fresco.

**2. Resolver la concurrencia real antes de escribir más.** La bitácora acredita otra sesión modificando ETCD y F reconoce PG/Mongo/Garage compartidos. ETCD propio no acredita por sí solo aislamiento de todo el flujo. Usar el toolkit existente y un identificador de ejecución; registrar ownership y config efectiva de cada store. Preferir una base PG propia con migraciones normales, base/colecciones Mongo propias, bucket/prefijo S3 propio, directorios propios de artifacts filesystem/salidas Lab y namespace/cola Temporal propios, además de ETCD y Kafka propios. Si un componente usa nombres/globales no aislables o comparte un recurso que puede ser reseteado por otra sesión, levantar una instancia propia. No matar, drenar, borrar ni reconfigurar procesos/datos de la otra sesión ni el PG del incidente. No crear una plataforma nueva de coordinación: manifest de recursos y ejecución serial en targets propios basta. Revalidar que Gateway, worker, Lab y tests apuntan efectivamente al mismo conjunto aislado.

**3. Registrar el contacto previo con Kafka DEV.** La bitácora relata arranque del Gateway contra brokers DEV compartidos, descubrimiento del consumer de `echo.automation-actions.v1`, detención y posterior Kafka local. F §3 decía «jamás al cluster compartido»; se rectifica esa frase. Está reportado el contacto/consumer; consumo, commits, duración y automatizaciones ejecutadas no están acreditados desde CLOUD. Conservar timestamps/logs y realizar una revisión acotada, read-only, de group membership/offsets y efectos identificables si existe acceso soportado. Sin reset de offsets, replay, borrado de topics, reinicios compartidos ni mensajes de prueba. Si no puede determinarse el impacto, registrar exactamente UNKNOWN y el dato faltante; continuar el cierre en el Kafka propio sin convertirlo en auditoría general. No repetir la afirmación de contacto cero.

**4. Completar correcciones y regresiones útiles.** Conservar los nueve criterios originales y los positivos M04. Dos puntos requieren cierre explícito según el retorno: (a) el panic `t.Activity=nil` con métricas deshabilitadas fue sorteado habilitándolas; probar la configuración soportada sin métricas/tracer y corregir el manejo opcional si persiste, con regresión; una opción habilitada no demuestra el cierre de la otra; (b) F sólo describe contraste de source_instance_ref para QA-S3-02: probar misma instancia con run/evaluación/scope ajenos y artifact válido, rechazo antes de Prepare/POST, además del positivo legítimo. No afirmar defecto inspeccionado en d760dc3 ni imponer `run_ref == EvaluationRef` universal: comprobar la autoridad real del productor. Cubrir DEFINITION_REF, versión/key por item, selectors/límite+1 en Mongo y workflow resolve→batch→finalize con resultados durables. Tests deben fallar ante comportamiento incorrecto; no reintroducir fakes que sólo devuelven el DTO recibido.

**5. Completar Gate C y los subcasos funcionales pendientes.** Reconstruir el candidato y fixtures en los targets propios. Repetir Generic y Group + Gateway/readback sobre el SHA final, mantener key estable para replay idéntico y demostrar no re-POST; usar intent/fixture nuevo cuando su semántica realmente cambie, sin variar XML/key para ocultar un conflicto de la misma intención. Ejecutar revisión exacta→outbox→worker Lab→generación→curvas/métricas/rankings/screener. El fixture de dos operaciones con Exposure UNKNOWN sirve para insuficiencias honestas; añadir el positivo con evidencia suficiente para los cálculos exigidos. Incluir cero historias y visibilidad sin curvas/ranking ficticios, coverage COMPLETE/PARTIAL/GAP y tiempo/moneda/Q_i/FX honestos. Cerrar también crash/commit remoto, Mongo caído tras Prepare, dos workers concurrentes, REPORT_PENDING, recibos adversariales y goldens que sigan parciales en O01–O24/EC-01–08. Un receipt+replay positivo no sustituye toda esa matriz.

**6. Alcanzar el piso con medición correcta.** Añadir tests de comportamiento/integración y, donde corresponda, instrumentación del runtime; no wrappers vacíos, tests espejo ni exclusiones oportunistas. El corrector resuelve ordinariamente harness, fixtures, dependencias y fallos locales dentro de este mismo one-shot. Finalizar con scope estable y ≥95% de statements del código nuevo, perfiles reproducibles y comparación de regresiones equivalentes. No detener la entrega por una decisión de scope que ya está adjudicada.

**7. Intentar D y entregar candidato completo.** Descubrir/reconectar canales RO por protocolo normal y buscar el dataset concreto PG/Mongo/artifacts/lineage; no elevar permisos ni reutilizar sesiones expiradas. Registrar error preciso si falta acceso. Actualizar F con una matriz única de hechos corregidos/probados/pendientes, full SHAs remotos, hashes de binarios/config/fixtures/perfiles, resultados A–E y recursos. Mantener separados resultados históricos y nuevos. A/B/C, calidad y publicación deben estar completos antes de READY_FOR_INDEPENDENT_VERIFICATION; D puede mantener bloqueo externo demostrado y E sigue NOT_AUTHORIZED.

**8. Verificador fresco dentro de Shot 4.** Si la superficie lo permite, despacharlo al candidato completo publicado con contexto fresco y sin autoría; si no, devolver el launcher exacto listo para otra sesión. Reconstruye y repite los cierres con expected independiente; revalida coverage, Lab, recovery y límites de D. No modificar producto durante su auditoría: si encuentra un defecto, el corrector lo corrige y se verifica el SHA nuevo dentro del mismo Shot 4. No autocertificación ni Shot 5 automático. Si una capacidad externa realmente impide continuar, dejar un único checkpoint con causa, recurso/error y acción necesaria, sin presentar trabajo implementable pendiente como una solicitud de permiso.

Agents-OS se actualiza en master con concurrencia/readback, sin cierre de sesión, feedback/L0/L1 ni cuota inventada. No release, flota, campañas ni mutaciones PROD. El mandato original y B/addendum conservan autoridad; esta sección resuelve el alcance y orden de los pendientes de F sin abrir otro programa.

### 1. Roles, autoridad y secuencia

**Fase de corrección:** ROLE TOP LOCAL por mandato específico Owner; GLM-5.3-Flash Max mediante ZCode, función implementador. Necesita repos, builds, stores y runtime de harness propios. Puede resolver detalles de implementación y pruebas dentro de la SPEC, con KISS/YAGNI/SOLID y reutilizando los adapters existentes. No necesita una decisión Owner para registrar activities comunes, corregir SQL, preparar Gateway/Lab o reparar su harness aislado.

**Fase de verificación:** otro GLM LOCAL fresco, sin autoría de las correcciones, función verificador final. Reconstruye el candidato y ejecuta oráculos propios; no toma como certificación el relato del corrector. Si el entorno permite un subagente local con contexto fresco y acceso real, puede despacharse directamente; si no, se entrega un launcher exacto para otra sesión. No afirmar que fue ejecutado si sólo se preparó el prompt. Ambas fases pertenecen a Shot 4.

Bootstrap Agents-OS una sola vez por sesión. Refrescar refs y leer desde el commit documental exacto indicado por el Manager, preservando cambios ajenos. Autoridades: B — Frozen Design (§§3–9, 11–16), Contract Addendum, C — Four Shot Delivery Plan, E — Independent Adversarial Report y esta adjudicación. D conserva la historia de implementación. No depender de ZIP, no reiniciar arquitectura ni confundir esta task nueva con la integración Ingestion V2 anterior.

### 2. Candidato de entrada y alcance de la adjudicación

| Superficie | Pin de entrada |
|---|---|
| Symphony | `feature/forge-echo-ingestion-task-v2@7731cb844446062f861f04d19dea60a34d425373` |
| Echo | `feature/forge-task-contract-v2@24af786232fa362cc1599df1b9d90b1c8347b557` |
| Contracts | `v3/sdk/contracts/v0.0.1-forge-ingestion-task.2`, tag objeto `7496b05b6932517e1d51b757c42cf72dad2cc1bd` → Echo anterior; subtree `cb88aece4f04b648fd724568de3823604dc064ab` |
| SDK efectivo esperado | `c7f11496b6f681687c9e1e41a773a13295640351`; verificar el checkout que resuelve `replace ../../sdk` |
| Antecedente para upgrade | Symphony `07c914251760a938293b7fa7fe4e6d7b4d330640`, con 018 original |
| Bases para atribución | Symphony `22f337ca434549c492b2d402fd158e23ac4758a8`; Echo `f93cd4f80085e328f9176c1215e42e6c8e0b2404` |
| Informe E recibido | Agents-OS `124430da4deb8eb95e3121f970ea366adcffd289`, blob E `a56a34865f3ccccb8a80a8c28e0c58e01641df7e` |

El Manager comprobó refs de producto sin cambios y revisó acotadamente las causas de los findings con especialistas de la misma superficie/modelo. No ejecutó de nuevo los repros LOCAL ni certificó runtime desde CLOUD. E aporta reproducciones reportadas y matriz de límites: A incompleto, B/C NOT_RUN, D auténtico parcial, E release NOT_AUTHORIZED. Su resultado REVIEW_COMPLETE describe el alcance declarado; no acredita todos los oráculos del mandato Shot 3.

Se conservan los nueve IDs. **QA-S3-02 y QA-S3-07 se adjudican P1 de integridad**, por aceptación de identidad ajena y selección de versión sin compatibilidad; no se afirma que haya corrupción remota ya persistida. **QA-S3-04 pasa de P3 a P2**, por incumplimiento de receta/idempotencia con conflicto fail-closed. Todos los findings son obligatorios para cerrar, cualquiera sea la etiqueta.

### 3. Recuperar evidencia y preparar la ejecución

Antes de corregir, localizar las worktrees `qa-symphony`/`qa-echo`, `qa-evidence`, `qa-stack`, `qa-temporal` y `QA-SHOT3-MANIFEST.txt` del workspace del programa `forge-echo-task-v2-20261027`. E nombra archivos locales pero no fija commit QA ni hashes de todos los activos. Conservar el delta exclusivo de pruebas/harness en un commit identificable y un manifest de hashes de tests, fixtures, SQL antiguo, perfiles y logs. No atribuir una ref remota hasta verificarla. El tamaño del binario no sustituye su hash; marcar cualquier identidad histórica que no pueda reconstruirse.

Promover los tests útiles a regresiones permanentes. Un `*_FINDING` puede pasar porque comprueba que el bug existe: conservar el fixture y hacer que la regresión exija el expected contractual correcto. No dar el finding por cerrado sólo porque su reproducer queda verde. Los scripts de seed y boot son candidatos al toolkit existente, sin crear otro framework.

Reutilizar recursos propios después de verificar paths reales/symlinks, listeners/PIDs actuales, PG `data_directory` y base, namespace/colas Temporal, colecciones y buckets/prefijos. El stack reportado incluye Temporal real, PG, Mongo, ETCD y Garage como sustituto S3; conservar esa distinción y demostrar las operaciones del adapter. No llamarlo MinIO real. El template compartido `lab-v4-shot4-20261021/pgdata` del incidente queda excluido de pruebas, cleanup, stop y restauración. Su reparación no es requisito para avanzar en recursos propios.

No PROD/trading/flota/campañas, migraciones shared, reemplazo de SQX/plugins, resets destructivos ni despliegue compartido. Forge conserva un ambiente operacional único; usar candidate/harness propio, sin inventar Forge DEV. Un riesgo concreto de ejecución insegura detiene el escenario afectado; el resto seguro continúa. Gateway y Lab del harness sí forman parte del trabajo autorizado.

### 4. Correcciones adjudicadas y oráculos de cierre

Orden de desbloqueo: QA-S3-05 → 06 → 08; después resolver conjuntamente autoridad de versión/key (07/04), identidad/moneda (02/03), test contradictorio (01) y cobertura/evidencia (09). Completar pruebas y E2E antes de devolver el candidato al verificador.

#### QA-S3-05 — P1: migraciones y bootstrap nativo

El catálogo `ordered` termina en 016. Además `main.go` bifurca a `runDataOnlyEchoWorker` antes de `wireDurablePersistence/migrations.Apply`; agregar entradas al catálogo sin conectar/verificar la ruta efectiva no cierra el finding. El puente DDL manual de QA permitió investigar, pero no acredita arranque limpio del producto.

Implementar el camino normal y trazable de schema requerido por data_only, con fallo antes de publicar si falta o falla la preparación obligatoria. Mantener cambios aditivos, verificar ordinal libre real y colisiones antes de asignarlo; no incorporar migraciones ajenas de otros workstreams.

La 018 original de `07c9142` carece de la nulabilidad/índice parcial presentes en la 018 de `7731cb8`. Una base que ya registró el nombre antiguo no se actualiza editando otra vez el archivo. Conservar SQL publicado/aplicado y resolver el upgrade mediante una ruta aditiva. Este ledger tiene `version`/`applied_at`, no validación de checksum: conservar hashes de SQL en el manifest de evidencia sin inventar una protección que el runner no posee. El baseline `22f337ca` contiene 017, no 018; se rectifica esa generalización de E.

Demostrar sobre bases propias: Fresh por la ruta normal del producto; upgrade desde 001–016 con filas de control; upgrade con 017 y 018 originales ya aplicadas/registradas y filas legacy; repetición y concurrencia de boot/aplicación. Ledger y datos previos permanecen. Las tablas/constraints/índices finales permiten Prepare, aceptación y recovery. Si se reutiliza el harness que aplicó 017/018 sin ledger, identificar ese estado y reconciliarlo con comprobación explícita de schema; no usarlo como sustituto del upgrade verdadero ni esconder drift con IF NOT EXISTS ciego.

#### QA-S3-06 — P1: Decision opcional y lineage real

Decision ausente es legítima en el intent nativo. Persistir NULL, no string vacío, y eliminar la fabricación de `decision:<key>`. No obligar al usuario a inventar una Decision para ejecutar la task. La composición debe aportar metadata/lineage acreditados por el item o fallar de manera tipada cuando falte un dato obligatorio; un callback genérico no puede inventarlos.

Cierre en Fresh y Upgrade: manifest nativo sin Decision persiste NULL; la entrega funciona con metadata real; una Decision legítima conserva la guardia legacy y unicidad aplicables; dos intents incompatibles para el mismo par legacy fallan sin POST; replay idéntico converge. Items distintos conservan sus propias autoridades. Mantener Prepare antes de BindSourceBinding y propagar errores SQL antes de HTTP. No reparar silenciosamente decisiones sintéticas en recursos ajenos.

#### QA-S3-08 — P1: lifecycle completo en data_only

La composición data_only registra tres activities de ingesta, pero Generic/Group solicitan otras superficies comunes: spans y, con Foundation durable, FlowRunStart/Seal. Completar el wiring efectivo sin cargar SQCLI. No cerrar únicamente registrando `begin_workflow_span`, sembrando SpanID para evitarlo o quitando FlowRunRef/intent para saltar Foundation.

Ejecutar el binario real corregido, sin SQCLI, con Generic raíz y Group hijo: lifecycle/start/span → resolve → batch → finalize → seal; StageExecution y reporte persistidos con ACK; receipt y readback reales. Repetir con restart, cancelación y fallo según el contrato. Comprobar perfil inválido fail-closed, ausencia de dependencias obligatorias y dos destinos con endpoints/scopes propios; no permitir fallback silencioso a physical.

Para diagnosticar el stall conservar historia cruda, pending activities/attempts/último error, namespace/queues, pollers de workflow y activity, catálogo de registros y hash del worker. Cero ActivityTaskStarted acredita falta de progreso observada; por sí solo no prueba ausencia de poller ni una causa única. Ningún worker physical ajeno debe rescatar las activities faltantes.

#### QA-S3-07 — P1: versión por item y compatibilidad

Eliminar la selección de primera versión en resolver **y mapper**. En el candidato, `expectedVersionRefForItem` toma la primera compatible por filtro incompleto, `expectedVersionRefOf(req)` toma el primer VersionRef global, la activity pasa el source completo y `buildSQXDefinition` retorna con el primer OutputSQX. Corregir sólo un helper deja viva la clase de defecto.

Cierre: una estrategia con varias evaluaciones compatibles produce un item con todas; versiones incompatibles producen VERSION_SOURCE_MISMATCH antes de red, sin dividir el item ni cambiar counts. Permutar bindings/miembros conserva resultado o rechazo. Dos estrategias de igual display con versiones distintas permanecen separadas, también cuando el binding omite la aserción opcional StrategyRef: el join usa la EvaluationRef y su pertenencia acreditada.

Cubrir SEALED_REF, SQX_DEFINITION y DEFINITION_REF. Todos los miembros del item deben acreditar una versión compatible. Mismo XML exacto en ZIP distinto es compatible; XML que deriva otra versión dentro del mismo item falla. No exigir que todo el cohort comparta una versión ni seleccionar un sello/definición global por posición.

#### QA-S3-04 — P2: receta congelada y momento de sellado

Aplicar exactamente B§9.2: binding con ExpectedVersionRef y campos semánticos, digest tagged compartido; key con `HashTaggedV2`, tag `forge-echo-delivery.v1` y los siete argumentos explícitos destination_id, namespace, writer, forge_strategy_ref, expected_version_ref, source_binding_digest y mapping_version. La influencia transitiva de namespace/writer dentro de otro digest no equivale a la receta wire.

B§8.1.3 exige versión definitiva, binding digest y key determinados antes de devolver work-item refs, incluidos los modos derivados. No completar la versión después de haber congelado una key incorrecta. Golden independiente debe verificar bytes/digest/key; permutar refs o cambiar retry/reloj/FlowRun consumidor no cambia la intención; cambiar versión o scope la cambia conforme a receta. `request_digest` no entra en la key para eludir conflicto de misma intención con cuerpo distinto.

Recovery de manifests ya preparados conserva sus bytes/key/scope sellados; no rehashear una intención previa al reintentar porque cambió el algoritmo. Mantener HistoryID estable para corrección del mismo run y CREATE_ONLY→REVISION_REQUIRED donde corresponda. Verificar key, manifest y expected del receipt concordantes en los tres version_mode.

#### QA-S3-02 — P1: identidad canónica acreditada

CANONICAL_HISTORY_V2 debe contrastar pertenencia/source identity del payload con el binding y las fuentes seleccionadas, además de decodificar sintaxis/hash. Un artifact válido de otro productor/run no puede aceptarse sólo porque su DTO valida. No sustituir IDs del payload por los esperados para forzar aceptación ni degradar corrupción a ausencia bajo IF_AVAILABLE.

Cierre: payload válido con identidad acreditada conserva todos sus datos; mismo fixture con identidad/scope ajenos y hash/size correctos rechaza antes de Prepare/POST. La comparación sigue la autoridad del productor; no imponer `run_ref == EvaluationRef` universal a todo productor canónico porque esa igualdad exista en SQX TradeList. Falta de evidencia necesaria produce error tipado, sin inferencia por nombre/carpeta.

#### QA-S3-03 — P2: suficiencia de moneda por perfil

Un CANONICAL_HISTORY_V2 que ya acredita moneda OBSERVED no requiere una declaración externa adicional. Fuente sin moneda necesaria exige evidencia/declaración válida; si existe historia pero la moneda es insuficiente, IF_AVAILABLE no puede fingir ausencia de historia. Preservar OBSERVED/DECLARED y evidence_ref; no sobrescribir moneda contradictoria ni elevar DECLARED a OBSERVED.

Cierre: fuente canónica válida sin declaration pasa; fuente que no acredita moneda y no tiene declaración falla; declaración legítima produce estado DECLARED; NONE omite economía sin exigir moneda ni recorrer trades. Conservar los oráculos positivos de M04: una operación por trade, precisión del contrato fuente, IDs/lados/tiempos y costes/Q_i/FX/Exposure honestos. No agregar operaciones ni redondearlas para acomodar el cálculo.

#### QA-S3-01 — P2 de test/evidencia

Corregir el test que ordena los items y luego espera rechazo por orden. Separar positivo canónico, negativo no canónico y prueba del sort; no relajar Validate. Reproducir el fallo de `7731cb8`, después la suite `core/domain` completa verde en el SHA corregido. No reescribir el historial de D para convertir retroactivamente su claim de suites en PASS.

#### QA-S3-09 — P2 de cobertura/evidencia

E reporta 2737/5806=47,1% en archivos tocados y 1037/1289=80,4% en archivos nuevos. Son cocientes reportados, no cobertura recalculada por el Manager. Faltan pesos por archivo, hashes/perfiles y procedimiento reproducible; seleccionar el primer binario tras encontrar segmentaciones distintas no demuestra unión correcta. Reconciliar dentro de Shot 4, sin pedir otra entrega de Shot 3.

El piso sigue siendo **≥95% del código nuevo de la task**, con scope congelado y justificado. Incluir funcionalidad nueva insertada en archivos preexistentes; no omitirla para mejorar el número. Separar ese scope, los archivos nuevos y el diagnóstico de archivos completos tocados; todo el legado de generic_workflow no se convierte por sí solo en el denominador del gate.

Publicar SHA/toolchain/tags/config, comandos, perfiles crudos con hashes y tabla de statements cubiertos/totales por archivo. Combinar hits sólo sobre un universo compatible de bloques, sin duplicar denominador; diferencias de segmentación requieren resolver/regenerar medición coherente, no escoger el perfil favorable. Incluir rutas no ejecutadas con cero. Runtime sin instrumentación demuestra comportamiento, no coverage. Las pruebas deben verificar comportamiento y negativos, sin tests espejo para inflar el porcentaje. El verificador reproduce scope, suma y resultado final.

### 5. Completar A/B/C y oráculos pendientes

Cerrar los findings de arranque desbloquea el resto de la verificación; no lo sustituye. Mantener la matriz O01–O24 y EC-01–EC-08 con todos los subcasos, estado, fixture/hash, expected independiente, actual, comando/exit, refs/digests/readback y SHA exacto. No heredar PASS de un unit como PASS de una ruta real.

- **Fuente y resolución:** Generic y Group; A→B→ingesta source.task=A; input inicial y output_cohort con ownership COMPLETED; snapshot Foundation durable y rehidratación por ref; etiquetas iguales, multieval, rename en todo tramo productor utilizado; CANONICAL/DEFINITION_REF con productor válido sin SQX; REQUIRED/IF_AVAILABLE/NONE, ausencia frente a corrupción y límites de payload.
- **Entrega real:** PG-first antes de HTTP y recuperación sin Mongo después de Prepare; Gateway confirma pero se pierde respuesta; crash después de BeginAttempt; GET antes de POST en UNKNOWN, INGESTED sin nueva red; 401/403/404/receipt ajeno; misma key con cuerpo distinto; dos workers concurrentes; refs/estado atómicos, contadores/budgets/heartbeats/cancelación correctos. Conservar key/body y evitar doble ingestión o downgrade por error tardío.
- **Reporte:** resultado Foundation con ACK real y conteos consistentes, CONTINUE/FAIL_AFTER_BATCH después del reporte, REPORT_PENDING recuperable al volver Mongo sin nueva ingesta ni selección.
- **Gate B:** request producido por la task → Gateway real del harness → PG/artifact store → receipt estricto → GET-by-key/by-id y readback exactos. Recuperar bytes de accepted body, historia y metadata; comprobar hash y contenido de forma independiente. Goldens cruzados fijos en ambos consumidores del mismo módulo distribuido, incluyendo errores, digests, SourceEvidence y techo canónico SQX 262144/262145.
- **Gate C:** revisión exacta → outbox → worker Lab → generación → curvas/métricas/rankings/screener que la evidencia permite. Casos positivos con datos suficientes y negativos de insuficiencia; netos 10, −4 y 0 contribuyen una vez y suman 6; costes/Q_i/FX no inventados, moneda y estados preservados. Misma economía con COMPLETE/PARTIAL/GAP, known_at y economic_at UNKNOWN, cortes AS_KNOWN y metadata no redeclarada. No transformar tiempo desconocido en epoch/conocido siempre.
- **Cero historias:** registro/version/source evidence visibles en detalle y screener sin History/Revision/outbox/curva/score/rank ficticios. Distinguir NO_HISTORY de HISTORY_NOT_REQUESTED y elección de evidencia cuando hay varios receipts. Resolver con test IDs la diferencia de alcance entre O23 NOT_RUN y EC-05 servicio PASS de E; conservar evidencia específica sin extrapolarla.

M08 queda confirmado sólo en las superficies probadas de contratos/servicio. Lab sigue pendiente. La ausencia de findings Echo en los casos ejecutados no exime B/C; si se reproduce un defecto de esas fronteras, corregirlo en el linaje Echo de este programa y verificarlo dentro de Shot 4.

Atribuir regresiones históricas sólo con comando/config/fixture equivalentes en baseline. Los 51 fallos MT5 y el fixture auténtico ausente son atribuciones reportadas; no excusan fallos nuevos ni permiten omitir rutas nativas. Revisar suites con seed/DDL antes de ejecutarlas para conservar aislamiento.

### 6. Gate D separado: fuente auténtica

ETCD legacy, ausencia de worker/profile/claves nativas y ausencia de tablas V2 describen el despliegue observado por QA. No prueban ausencia de dataset Forge ni justifican desplegar la task en producción. D exige fuente real con identidad PG, evaluaciones/lineage Mongo, artifacts/hashes y configuración acreditada.

Redescubrir/reconectar canales read-only soportados por su protocolo normal, ya autorizado en Shot 3; no reutilizar IDs expirados ni elevar permisos. Identificar recurso y operación que faltan. Si el dataset sigue inaccesible, D queda BLOCKED_EXTERNAL con evidencia parcial explícita; A/B/C continúan con fixtures identificados. No usar el conteo del harness ni claves de despliegue como reemplazo de la fuente. No crear campañas ni export físico para fabricar D.

La frase histórica de E «sin operaciones sobre PROD» se entiende como ausencia de mutaciones: el mismo E describe lecturas RO para D. Conservar esa precisión sin borrar su evidencia.

### 7. Entrega del corrector y publicación

Entregar un candidato integrado por repositorio, descendiente de los SHAs de entrada, con pruebas permanentes y manifest reproducible. No reset/rebase destructivo ni merge general de Runtime/Dynamic Groups. Mantener tags contracts .1/.2 inmutables. Si contracts cambia, publicar la versión de prueba siguiente disponible, alinear consumidores y demostrar descarga/build frío efectivo con GOWORK=off y SDK exacto; si no cambia, conservar .2.

Crear **F — Final Certification.md** en este directorio mediante template/materializador canónicos. En la primera parte registrar correcciones por QA-S3-ID, diffs/SHAs, tests/fixtures/hashes, Fresh/Upgrade, config/runtime, cobertura, goldens, gates y recursos. Estado del corrector: SHOT4_CORRECTIONS_READY_FOR_INDEPENDENT_VERIFICATION únicamente cuando el candidato y la evidencia están completos para revisión; no autocertificación.

Código/tests/evidencia voluminosa en sus repos/workspaces; Agents-OS contiene localizadores, hashes, conclusiones y continuidad. Publicación documental en master directo con lectura reciente y protección de concurrencia. No secretos ni logs brutos en notas. Mantener abierto Agents-OS, sin feedback/L0/L1; registrar el segmento por las reglas canónicas. No inventar consumo de cuota.

### 8. Mandato del verificador final fresco — segunda fase del mismo Shot 4

Leer este mandato, B/addendum, E histórico y la primera parte de F desde el commit documental de handoff. Congelar los SHAs finales publicados y reconstruir módulos/binarios/config sin confiar en un checkout o PID heredado. Registrar identidad independiente y confirmar que no implementó esos cambios.

Repetir los nueve criterios de cierre con expected propio, luego los oráculos críticos y las partes de A/B/C que Shot 3 dejó parciales/NOT_RUN. Fresh y Upgrade pasan por el producto corregido sin puentes DDL; Generic y Group alcanzan task y reporte reales; conflictos de identidad/version/key y moneda tienen positivos/negativos; recovery/concurrencia, Gateway/Lab, corpus cruzado y cobertura se verifican sobre el mismo candidato final. La reutilización del stack no exime revalidar aislamiento y source→build→runtime.

Agregar a F una sección de **verificación independiente**, con evidencia y límites atribuibles a este verificador; conservar separadas las afirmaciones del corrector. Si el producto cambia después de verificarlo, esa comprobación no certifica el nuevo SHA. Los defectos acotados que aparezcan pertenecen al cierre de Shot 4, conservando autor/verificador separados y revalidando el delta; no crear nuevos shots ni enviar una cadena de microentregas al Owner.

Salida al Manager: READY_FOR_MANAGER_REVIEW si A/B/C, correcciones, goldens y piso de cobertura están acreditados; D PASS o bloqueo externo demostrado explícitamente; E release continúa NOT_AUTHORIZED. La adjudicación `FORGE_ECHO_INGESTION_TASK_VERIFIED` corresponde al Manager contra esa evidencia y su alcance, no al corrector. D bloqueado impide afirmar FULL_CERTIFIED o fuente auténtica completa.

Si persiste un defecto implementable, A/B/C sin ejecutar o cobertura bajo el piso, devolver **SHOT4_BLOCKED** con causa, reproducción, alcance y acción pendiente concretos. No llamar externo a código pendiente por tiempo consumido, ni forzar PASS para respetar cuatro shots. No hay Shot 5 automático. La entrega técnica no cierra la sesión Agents-OS.

## Fuentes

- [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/B — Frozen Design|B — Frozen Design]], [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/C — Four Shot Delivery Plan|C — Four Shot Delivery Plan]], [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/D — Implementation Evidence|D — Implementation Evidence]], [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/E — Independent Adversarial Report|E — Independent Adversarial Report]], [[10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum|Forge Task — Contract Addendum]] y [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT3 — Independent Adversarial QA Mandate|SHOT3 — Independent Adversarial QA Mandate]].
- Orden Owner: exactamente cuatro shots, QA adversarial en Shot 3 y corrección/verificador fresco dentro de Shot 4; sin más iteraciones de Shot 2. Retorno LOCAL de Shot 3 recibido el 2026-10-28.
- Symphony `7731cb844446062f861f04d19dea60a34d425373`: [resolver](https://github.com/xKoRx/symphony/blob/7731cb844446062f861f04d19dea60a34d425373/sqx/core/forge/echo_ingestion.go), [mapper](https://github.com/xKoRx/symphony/blob/7731cb844446062f861f04d19dea60a34d425373/sqx/core/forge/echo_ingestion_map.go), [activity](https://github.com/xKoRx/symphony/blob/7731cb844446062f861f04d19dea60a34d425373/sqx/activities/worker/echo_ingestion_activity.go), [runner](https://github.com/xKoRx/symphony/blob/7731cb844446062f861f04d19dea60a34d425373/sqx/adapters/registry-postgres/migrations/runner.go), [persistencia](https://github.com/xKoRx/symphony/blob/7731cb844446062f861f04d19dea60a34d425373/sqx/adapters/registry-postgres/ingestion_v2_persistence.go), [main](https://github.com/xKoRx/symphony/blob/7731cb844446062f861f04d19dea60a34d425373/sqx/cmd/sqx-worker/main.go), [wiring](https://github.com/xKoRx/symphony/blob/7731cb844446062f861f04d19dea60a34d425373/sqx/cmd/sqx-worker/echo_ingestion_wiring.go), [bootstrap durable](https://github.com/xKoRx/symphony/blob/7731cb844446062f861f04d19dea60a34d425373/sqx/cmd/sqx-worker/persistence.go), [workflows](https://github.com/xKoRx/symphony/blob/7731cb844446062f861f04d19dea60a34d425373/sqx/workflows/generic_workflow.go).
- [018 original en 07c9142](https://github.com/xKoRx/symphony/blob/07c914251760a938293b7fa7fe4e6d7b4d330640/sqx/adapters/registry-postgres/migrations/018_ingestion_v2_delivery_state.up.sql) y [018 candidata en 7731cb8](https://github.com/xKoRx/symphony/blob/7731cb844446062f861f04d19dea60a34d425373/sqx/adapters/registry-postgres/migrations/018_ingestion_v2_delivery_state.up.sql).
