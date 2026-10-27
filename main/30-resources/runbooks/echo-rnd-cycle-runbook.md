---
type: runbook
schema_version: 1
scope: project
created: '2026-10-28'
updated: '2026-10-27'
area: '[[Trading]]'
project: '[[Echo — I+D de Estrategias]]'
entities:
  - '[[Echo — I+D de Estrategias]]'
related:
  - '[[Echo I+D — Mapa de capacidades]]'
  - '[[30-resources/agents/skills/echo-rnd-manager/SKILL]]'
  - '[[30-resources/agents/skills/echo-futures-research-manager/SKILL]]'
  - '[[30-resources/agents/skills/imox-strategy-research/SKILL]]'
aliases:
  - ciclo I+D Echo
  - contrato de mandatos de investigación Echo
confidence: high
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/project
  - tech/agents-os
  - project/echo-rnd
  - action/research-cycle
---

# echo-rnd-cycle-runbook

## Propósito

Registrar, transferir y cerrar una unidad de investigación de Echo I+D con evidencia, autorización y continuidad verificables. Este runbook posee la mecánica documental de fichas, mandatos, retornos y mejoras. Los managers eligen prioridades y decisiones; los runbooks de mercado poseen ejecución y gates.

**Alcance de validación:** contrato documental y ensayos de recuperación/activación. No certifica comandos de backtest, flota, estrategia, proveedor ni producción. Reutilizar [[Echo I+D — Mapa de capacidades]] para resolver la operación técnica correspondiente.

## Precondiciones

- Programa y mercado identificados; último estado confirmado leído.
- Una autoridad para el estado del trabajo y una autorización compatible con el próximo paso.
- Celda(s) de cobertura o capacidad que las desbloquea identificadas.
- Fuentes/repos/recibos disponibles o faltantes declarados.
- Para ejecución: presupuesto, superficie, datos, SPECs y gates aplicables. Una autorización de organizar no autoriza lanzar motores.

## Procedimiento

### 1. Abrir o recuperar el trabajo

1. Buscar la ficha, campaña o proyecto existente por hipótesis, instrumentos, fuentes y artefactos. Reutilizarlo si posee la responsabilidad; crear sólo si el trabajo necesita identidad propia.
2. Para una nota nueva, materializar el tipo con `agents-os-entity-lifecycle` y su contrato vigente. No crear carpetas/proyectos para toda combinación de la matriz.
3. Registrar el mínimo que permite reproducir la decisión:

| Campo | Contenido verificable |
|---|---|
| Trabajo / Owner / manager | Identidad estable y planner único; un proyecto agent conserva su única tarea puente. |
| Celda(s) / contribución | Mecanismo/tesis, producto exacto, horizonte/contexto, fase; o capacidad habilitante y celdas beneficiarias. |
| Pregunta / hipótesis | Qué se espera observar, por qué merece investigación y qué no está demostrado. |
| Refutador / control | Resultado que cambiaría la decisión; comparación comparable en ventana, exposición, riesgo y costes cuando corresponda. |
| Fuente / spec | Referencias precisas y clasificación SOURCE/OP/HIP/UNRESOLVED; versión y reglas materiales. |
| Identidad técnica | Estrategia/variante/config/MM/Provider, dataset/calendario, source/build y revisiones de método/policy según el mercado. |
| Diseño / selección / evaluación | Períodos y datos ya vistos; intentos/adaptaciones previas, incluidos cambios manuales y de agentes. |
| Gates / presupuesto | Autoridades aplicables, entradas/salidas, recursos, máximo de intentos y paradas. |
| Estado / evidencia | Investigación, técnica, economía y aceptación como dimensiones separadas; refs de resultados. |
| Próxima acción | Responsable, dependencia, decisión y condición de reapertura si se aparca/rechaza. |

Una tabla de cobertura es vista del registro; no otra fuente de tareas o de métricas. Si la campaña ya posee campos equivalentes, enlazarlos en vez de copiar otro esquema.

### 2. Preparar la especificación y comprobar su trazabilidad

Para cada regla material, registrar una fila o referencia equivalente:

`source_or_hypothesis → operational_rule → effective_decision_point → fixture/counterexample → runtime_trace`.

- Separar condiciones obligatorias, opcionales y adaptaciones propias. Registrar desacuerdos con estado explícito.
- Fijar qué datos existen al momento de decisión, unidades, redondeo/ticks, ventanas, DST, precedencias, invalidación, expiración y salidas.
- Separar stop técnico/objetivo definido por la tesis de experimentos de MM/ejecución. No atribuir éstos a un curso si no están en la fuente.
- Verificar que parámetros y variantes alcancen el predicado efectivo. Serializar una configuración no prueba que cambie señales.
- Incluir positivo, negativo y caso límite que discriminen reglas; una imagen apoya inspección, no sustituye trazas deterministas ni fills reconciliados.
- Para una fuente multimodal, pedir a MKE únicamente las revisiones necesarias y usar su autoridad de claims. SUPPORTED significa fidelidad de extracción, no rentabilidad.

Si un desacuerdo puede cambiar operaciones, no enviarlo ambiguo al implementador. Conservar la pregunta y el owner que debe resolverla.

### 3. Emitir un mandato acotado

Completar antes del dispatch; usar el formato equivalente del proyecto técnico si ya existe:

```text
WORK_ID / MARKET / COVERAGE_CELLS:
WORK_FUNCTION / CAPABILITY_ROLE / SURFACE / TOOL_NEED:
OBJECTIVE / WHY_THIS_QUESTION:
CURRENT_TASK_STATE / PRIOR_ARTIFACTS_AND_VIGENCY:
CANONICAL_AUTHORITIES / SOURCE_AND_BASELINE_REFS:
ACCEPTED_OWNER_DECISIONS / OPEN_DECISIONS:
INPUTS / SPEC / DATA_IDENTITY:
SCOPE / EXCLUSIONS:
EXECUTION_AUTHORIZATION / RESOURCE_BUDGET / STOP_CONDITIONS:
EXPECTED_EVIDENCE / APPLICABLE_GATES:
RETURN_TO / WRITE_AUTHORITY:
METHOD_REVIEW: evidence-based delta or NO_DELTA
```

- Worker: una entrega acotada y recuperable. Submanager: una pregunta que necesita coordinación/contexto propio. Manager de mercado: continuidad de su línea; no un worker infinito.
- Entregar al worker sólo las autoridades necesarias. No pedirle reconstruir todo el programa ni resolver requisitos materiales ocultos.
- Evitar writers concurrentes sobre el mismo fichero. Cada worker escribe su entrega; el integrador actualiza el planner y las vistas compartidas.
- Usar subagentes directos sólo cuando estén disponibles. En otra superficie, emitir el prompt completo y esperar evidencia de retorno, sin afirmar que el trabajo se ejecutó.
- Antes de motores, confirmar preflight/capacidad con el owner técnico. Cloud, Daedalus y Hefesto son superficies según necesidad, no fases obligatorias.

### 4. Recibir y adjudicar evidencia

Requerir:

```text
WORK_ID / REFERENCES / EFFECTIVE_INPUTS:
RESULT: complete | partial | blocked
EVIDENCE_PRODUCED_AND_VERIFIED:
CONFORMANCE: source/spec/code/execution; first divergence if any
TECHNICAL_GATES: exact gate + receipt + version + status
ECONOMIC_PHASE_AND_OUTCOME: measured | projected | not_evaluated
ATTEMPTS_AND_NEGATIVES: conserved refs + causes
LIMITATIONS / UNKNOWNS:
RECOMMENDATION_AND_ALTERNATIVE:
METHOD_DELTA: evidence + proposed change + regression case | NO_DELTA
NEXT_ACTION / OWNER_DECISION:
```

1. Comparar identidad y fuentes con el mandato. Un proceso terminado o un archivo existente no prueba el outcome.
2. Separar fidelidad de fuente, determinismo de spec, conformidad de implementación, ejecución, economía y aceptación.
3. Clasificar la salida sin colapsar dimensiones:

| Dimensión | Ejemplos; manda el vocabulario del mercado |
|---|---|
| Investigación | nueva, en estudio, inconclusa, refutada, aparcada, candidata a revisión |
| Técnica | no implementada, G1/G2/etc. PASS/FAIL, datos faltantes, defecto, ejecución parcial |
| Economía | no evaluada, negativa en la muestra, factible bajo supuestos, challenge observado, funded observado, retiro observado |
| Owner | pendiente, aceptada con referencia, rechazada con motivo |

4. Si la evidencia cambia de identidad o policy, invalidar sólo lo dependiente y conservar las versiones antiguas. No repetir una corrida bit-idéntica con recibo vigente por rutina.
5. Si la conclusión es negativa, conservar condiciones, datos vistos, refutador y disparador de reapertura. No abrir otra búsqueda de parámetros sobre el mismo resultado sin hipótesis y registro nuevos.
6. Si falta evidencia física, declarar el límite y el menor encargo que lo resuelve. No convertir un análisis Cloud en prueba LOCAL.
7. Elevar aceptación al Owner cuando le pertenece. Un manager puede rechazar evidencia inválida o pedir reparación; no aceptar su propio gate de producto.

### 5. Actualizar y elegir la siguiente investigación

1. Actualizar primero la ficha/planner dueño, después la vista de cobertura que enlaza su evidencia.
2. Registrar aprendizaje, coste observado si existe y qué decisión cambia. No inventar un porcentaje de cobertura global ni una estimación de throughput.
3. Aplicar la decisión: continuar, corregir, aparcar, rechazar o presentar candidata. Si se corrige, identificar regla/versión/gate afectados y límite de la nueva ronda.
4. Mantener la siguiente pregunta preparada y las alternativas útiles, priorizadas por el manager; no materializar un backlog cartesiano.
5. Al manager global devolver sólo delta de la línea, capacidad, bloqueo transversal y decisión requerida. El planner de mercado sigue siendo autoridad.
6. Antes de terminar la sesión, verificar que otro agente puede recuperar el estado, las decisiones, la evidencia y la próxima acción. El cierre completo sólo se invoca si el Owner lo pidió.

### 6. Mejora controlada de skills y procedimientos

Aplicar a todas las funciones del programa, incluidas fuentes, implementación, backtest y QA. Cada retorno informa delta o NO_DELTA; una skill no se autoedita por obligación.

1. Capturar un fallo reproducido, fricción real o aprendizaje que cambie decisiones futuras. Distinguir defecto del producto, del dato, del procedimiento o de su uso.
2. Resolver la autoridad dueña. Estado va al proyecto; comportamiento del agente a skill; operación mecánica a runbook; invariantes ejecutables al repo técnico.
3. Proponer el menor cambio con evidencia, caso positivo, contraejemplo/adyacente y criterio de aceptación. Enlazar la revisión anterior usada por experimentos.
4. Clasificar autorización:
   - claridad, routing, trazabilidad y recuperación dentro de políticas aceptadas: aplicar según el mandato vigente, con validación;
   - gates, riesgo/MM, presupuesto, proveedor, instrumentos activos, dependencia de datos, autonomía, producción o automatización: obtener decisión Owner antes de cambiar.
5. Para una skill, aplicar `agents-os-skill-authoring`: metadata canónica, activación positiva/negativa/adyacente, forward-test realista, lint y change_log. Para producto, remitir al owner técnico; no editar código como efecto lateral de un feedback.
6. Incrementar revisión o conservar ref Git del método. No reinterpretar retroactivamente evidencia anterior.
7. Actualizar mapa/índice sólo si cambió responsabilidad, activación o handoff. Evitar una nueva skill si basta corregir la autoridad existente.
8. Validar en el siguiente uso relevante y conservar una vía de reversión. Si no hay delta durable, registrar NO_DELTA y seguir investigando.

### 7. Publicación, conflictos y recuperación

- Leer la revisión vigente antes de publicar. Aplicar sólo el delta autorizado; nunca sobrescribir trabajo concurrente.
- Agents-OS usa `master`, sin force-push. Si el head cambió, reconciliar fuentes afectadas y revalidar antes de actualizar.
- Verificar el estado remoto y el contenido material; distinguir publicación GitHub de réplica física local y de indexación Graphify.
- Si una publicación falla, conservar los archivos y el punto exacto de recuperación; no decir que está sincronizada.
- Si un resultado es inválido, marcarlo con causa/sucesor, no borrar evidencia negativa.
- Rollback documental: revertir únicamente el cambio de esta operación mediante un nuevo cambio auditable; no resetear historia ni evidencia ajena.

## Validación

Antes de declarar la unidad lista:

- [ ] Tiene una pregunta, celdas/capacidad, autoridad y próximo responsable.
- [ ] Fuente/spec/identidad/presupuesto se distinguen de una autorización de ejecución.
- [ ] Existe refutador y se declara qué datos se usaron para seleccionar.
- [ ] La evidencia respalda cada transición; no se confunde ejecución con éxito.
- [ ] Estados científico, técnico, económico y Owner son independientes.
- [ ] Retornos conservan fallos, desconocidos, delta metodológico y próxima acción.
- [ ] Hay un único planner y vistas enlazadas; no existen writers ambiguos.
- [ ] Se validan schema y referencias de los archivos tocados.
- [ ] Publicación y lectura de recuperación verificadas, o bloqueo declarado.

Los ensayos documentales de este runbook comprueban recuperación y límites de autoridad. Las operaciones físicas siguen requiriendo su validación técnica real.

## Vocabulario mínimo

| Término | Identidad |
|---|---|
| Familia | Conjunto relacionado por mecanismo/comportamiento económico; los límites pueden solaparse. |
| Tesis | Afirmación falsable sobre una condición de mercado y su efecto. |
| Estrategia | Reglas operacionales que convierten esa tesis en decisiones. |
| Variante | Cambio semántico de reglas que requiere identidad y evidencia propias. |
| Configuración | Valores concretos de una spec; cambiar parámetros no crea por sí mismo otra familia. |
| MM | Dimensionamiento y gestión de riesgo/operación/cuenta, separado de la señal. |
| Campaña | Experimento con identidades, datos, perfiles, presupuesto, método y objetivo congelados. |
| Run / intento | Ejecución física identificada; un retry no borra el intento anterior. |
| Celda | Pregunta localizada en mecanismo, producto, contexto y fase; no combinación vacía de parámetros. |

## Autoridades enlazadas

- [[Echo I+D — Mapa de capacidades]]: responsabilidades y procedimientos existentes.
- [[IMOX — Registro de campañas]]: contrato y matriz Forex, prevalece en sus campos técnicos.
- [[30-resources/runbooks/echo-futures-strategy-qualification-runbook|Qualification Futures]]: admisión, G0–G5, recursos y recibos.
- [[80-agents/skills/agents-os-agent-project-workflow/SKILL|Proyectos delegados]], [[80-agents/skills/agents-os-skill-authoring/SKILL|Autoría]], [[80-agents/skills/agents-os-session-close/SKILL|Cierre]].
