---
type: resource
status: active
area: "[[Personal]]"
created: 2026-07-08
updated: 2026-08-08
aliases:
  - sdd-prompts-pack-v4
  - prompts-v4
tags:
  - resource
  - vibe-coding
  - prompts
---

# Echo V3 — SDD Prompts Pack (v4-SDD)

Este paquete contiene los **Prompts Maestros de la Versión 4 (v4-SDD)** para Symphony. Están optimizados para copy-paste directo, siendo agnósticos a la feature mediante la parametrización de `{FEATURE_ID}`.

Cada prompt referencia de forma explícita y obligatoria las directrices de `CONSTITUTION.md`, `AGENTS.md` y las reglas del ciclo SDD.

---

## Índice de Prompts
- [Echo V3 — SDD Prompts Pack (v4-SDD)](#echo-v3--sdd-prompts-pack-v4-sdd)
  - [Índice de Prompts](#índice-de-prompts)
  - [1. prompt-sdd-create-spec.md](#1-prompt-sdd-create-specmd)
  - [2. prompt-sdd-verify-spec.md](#2-prompt-sdd-verify-specmd)
  - [3. prompt-sdd-plan-and-tasks.md](#3-prompt-sdd-plan-and-tasksmd)
  - [4. prompt-sdd-verify-plan-tasks.md](#4-prompt-sdd-verify-plan-tasksmd)
  - [5. prompt-sdd-implement.md](#5-prompt-sdd-implementmd)
  - [6. prompt-sdd-verify-implementation.md](#6-prompt-sdd-verify-implementationmd)

---

## 1. prompt-sdd-create-spec.md

```markdown
# 1. prompt-sdd-create-spec.md

[ROLE]
Actúa como mi **Coordinator (arquitecto-autor)** en Symphony.
Carga tus instrucciones de personalidad de:
- `.agents/rules/personalities/coordinator/arquitecto-autor.md`
y respeta las directrices de gobernanza de:
- `CONSTITUTION.md`
- `AGENTS.md`
- `.agents/rules/08-sdd-governance.md`

[CONTEXTO]
- **Feature ID**: `{FEATURE_ID}`
- **Catálogo de Features**: @specs/SPECS.md
- **Descripción de la Capacidad**: {CAPABILITY_DESCRIPTION}

[TAREA: CREAR E ITERAR LA SPEC CANÓNICA]
1. Crea el directorio `specs/{FEATURE_ID}/` si no existe.
2. Redacta y escribe en disco el archivo **`specs/{FEATURE_ID}/SPEC.md`** como una especificación funcional completa, durable y madura (`CAPABILITY_SPEC`).
3. Si existe una especificación preliminar o alias en `docs/prd/`, actualízalo para que sirva de redirección/alias no canónico hacia la nueva SPEC canónica (sigue el formato estándar de redirección).

[REQUISITOS FUNCIONALES A DETALLAR]
{DETAILED_FUNCTIONAL_REQUIREMENTS}

[RESTRICCIONES FÍSICAS CRÍTICAS]
- **NO modifiques ningún código de producción ni tests** en este paso (frontera estricta de la fase SPECIFY).
- **NO crees PLAN.md ni TASKS.md** todavía.
- Sigue las reglas de no-I/O y determinismo conceptual.

---

[HANDOFF DE ENTREGA]
Una vez generados los archivos, emite en el chat el siguiente bloque de handoff:
<<<PROMPT_NEXT_AGENT_START
[Para: Coordinator (arquitecto-revisor)]
[ROLE]
Actúa como mi **Coordinator (arquitecto-revisor)** en Symphony.
Carga tus instrucciones de personalidad de:
- `.agents/rules/personalities/coordinator/arquitecto-revisor.md`
y las reglas canónicas en:
- `CONSTITUTION.md`
- `AGENTS.md`
- `.agents/rules/08-sdd-governance.md`
- `.agents/rules/11-verify-spec.md`

[INPUTS]
- **Feature ID**: `{FEATURE_ID}`
- **SPEC a Evaluar**: @specs/{FEATURE_ID}/SPEC.md
- **RFC de Referencia**: {RFC_PATH_OR_N_A}

[TAREA: AUDITORÍA DE CALIDAD (verify-spec)]
Realiza un análisis riguroso y destructivo del documento `specs/{FEATURE_ID}/SPEC.md` evaluando los siguientes puntos de control:

1. **Aislamiento de Fase (Fronteras)**:
   - Asegúrate de que la SPEC **no contenga mezcla de código**, planes de tareas atómicas ni SQL detallado de base de datos.
   - Verifica que no se mencionen rutas de archivos físicos a modificar de producción o tests (esto pertenece a PLAN).
2. **Durabilidad y Rigor Conceptual**:
   - Confirma que la SPEC describe la capacidad a largo plazo, no problemas transitorios de la iteración.
   - Verifica si la estructura JSON/Go conceptual está completamente definida, incluyendo las reglas de negocio de los parámetros.
3. **QA-Ready (Criterios de Aceptación)**:
   - Revisa que existan escenarios claros escritos en formato **Given-When-Then** que cubran caminos felices (valores válidos) y caminos extremos o de fallo.

[VEREDICTO]
Clasifica tus observaciones en severidades: **BLOQ / MAY / MEN / INFO**.
- Si existe al menos un hallazgo de severidad **`[BLOQ]`** (fugas físicas, acoplamientos, mezcla de fases, falta de GWT), declara el estado global como **`NOT_READY`** para bloquear la transición.
- Si el plan técnico es seguro y las tareas son completamente atómicas, emite el veredicto **`READY`**.

---

[HANDOFF DE SALIDA]
Emite **únicamente** el bloque estructurado en el chat al final de tu respuesta:
<<<PROMPT_NEXT_AGENT_START
[Para: Coordinator (arquitecto-autor)]
[SPEC VERIFY] status: READY | NOT_READY
Feature: {FEATURE_ID}
Artifact Type: CAPABILITY_SPEC
Blocking Findings (BLOQ):
  - [BLOQ] <Detalle de la inconsistencia o mezcla de fase encontrada>
Major Findings (MAY):
  - [MAY] <Puntos de mejora conceptuales o de contrato>
Next Step: <Indicar corrección requerida o autorizar transición a la fase PLAN>
<<<PROMPT_NEXT_AGENT_END
<<<PROMPT_NEXT_AGENT_END
```

---

## 2. prompt-sdd-verify-spec.md

```markdown
# 2. prompt-sdd-verify-spec.md


```

---

## 3. prompt-sdd-plan-and-tasks.md

```markdown
# 3. prompt-sdd-plan-and-tasks.md

[ROLE]
Actúa como mi **Coordinator (arquitecto-autor)** en fase **PLAN** y **TASKS** para Symphony.
Carga tus instrucciones de personalidad de:
- `.agents/rules/personalities/coordinator/arquitecto-autor.md`
y respeta las reglas en:
- `CONSTITUTION.md`
- `AGENTS.md`
- `.agents/rules/08-sdd-governance.md`
- `.agents/rules/09-sdd-phase-permissions.md`

[CONTEXTO]
- **Feature ID**: `{FEATURE_ID}`
- **SPEC Canónica Aprobada**: @specs/{FEATURE_ID}/SPEC.md
- **RFC de Referencia**: @docs/prd/SQX_Adaptive_E2E_Pipeline_RFC.md

[OBJETIVO DE LA SESIÓN]
Traducir las reglas y el esquema conceptual definidos en la SPEC en la estrategia técnica física de archivos (`PLAN.md`) y en su checklist de tareas atómicas (`TASKS.md`).

[RESTRICCIONES FÍSICAS CRÍTICAS]
- **NO modifiques ningún código de producción ni tests** en este paso (frontera de fase PLAN/TASKS).
- **Allowed Files Guardrail**: Los archivos permitidos de producción deben acotarse estrictamente al módulo/paquete de la feature.
- **Prohibición de Infraestructura Real**: El plan de impacto y las tareas deben estructurarse de modo que la implementación (inicialmente mock-first si lo exige la SPEC) sea 100% testeable mediante la suite de tests unitarios o testsuite correspondiente, sin depender de infraestructuras externas reales.

[TAREA 1: GENERAR EL PLAN DE IMPACTO]
Genera en disco el archivo **`specs/{FEATURE_ID}/PLAN.md`** detallando:
1. **Allowed Files**: Archivos permitidos para modificación.
2. **New Files**: Rutas exactas de archivos a crear.
3. **Prohibited Files**: Archivos intocables (tests de regresión base, configs de CI).
4. **Firma de contratos físicos**: structs y firmas de funciones en Go, APIs públicas y payloads JSON.
5. **Estrategia de Rollback técnico** y plan de reversión ante fallos.
6. **Verification Gates**: Tests unitarios requeridos e instrumentación de telemetría (OTel).

[TAREA 2: GENERAR EL CHECKLIST DE TAREAS]
Genera en disco el archivo **`specs/{FEATURE_ID}/TASKS.md`** desglosando la implementación en tareas de desarrollo atómicas. Cada tarea debe cumplir:
- Ser auto-contenida e incremental.
- Definir de forma obligatoria su sección **`Allowed Files`** (subconjuntos estrictos del PLAN).
- Establecer el comando de prueba local exacto (ej: `go test -run TestName`).

---

[HANDOFF DE SALIDA]
Una vez generados los archivos en disco, emite en el chat el siguiente bloque:
<<<PROMPT_NEXT_AGENT_START
[Para: Coordinator (arquitecto-revisor)]
[ROLE]
Actúa como mi **Coordinator (arquitecto-revisor)** en Symphony.
Carga tus instrucciones de personalidad de:
- `.agents/rules/personalities/coordinator/arquitecto-revisor.md`
y las reglas en:
- `CONSTITUTION.md`
- `AGENTS.md`
- `.agents/rules/08-sdd-governance.md`
- `.agents/rules/09-sdd-phase-permissions.md`
- `.agents/rules/02-architecture-independencia-modulos.md`

[INPUTS]
- **Feature ID**: `{FEATURE_ID}`
- **SPEC Aprobada**: @specs/{FEATURE_ID}/SPEC.md
- **PLAN Técnico**: @specs/{FEATURE_ID}/PLAN.md
- **TASKS Checklist**: @specs/{FEATURE_ID}/TASKS.md

[TAREA: AUDITORÍA DE PLAN & TASKS]
Realiza un análisis destructivo e independiente del diseño técnico y el desglose de tareas, evaluando los siguientes puntos de control:

1. **Cumplimiento Físico de Fase (Fronteras)**:
   - Confirma que **no se ha modificado ni creado ningún código de producción ni tests** en el repositorio durante la creación de estos planes (la fase de codificación está estrictamente bloqueada).
2. **Minimización de Impacto y Aislamiento**:
   - Revisa la sección `Allowed Files` del PLAN. ¿Los archivos Go marcados para edición están lo más acotados posible?
   - Verifica que archivos comunes del contenedor de dependencias (`internal/di/container.go`) o similares se mantengan fuera del plan de impacto si no son estrictamente necesarios.
3. **Calidad y Atomicidad de las Tareas**:
   - Revisa `TASKS.md`. ¿Cada tarea individual cuenta con su propia lista acotada de `Allowed Files` (que debe ser un subconjunto estricto del PLAN)?
   - ¿Cada tarea posee un comando de verificación local independiente (ej: `go test -run TestName`)?
4. **Trazabilidad con los Outcomes del SPEC**:
   - Asegúrate de que el diseño técnico propuesto en el PLAN cubra el 100% de la lógica descrita en la SPEC y los escenarios funcionales Given-When-Then.

[VEREDICTO]
Clasifica tus hallazgos en severidades: **BLOQ / MAY / MEN / INFO**.
- Si existe al menos un hallazgo de severidad **`[BLOQ]`** (fugas de archivos, acoplamientos, falta de atomicidad de tareas o inconsistencia con la SPEC), declara el estado global como **`NOT_READY`** para bloquear la transición.
- Si el plan técnico es seguro y las tareas son completamente atómicas, emite el veredicto **`READY`**.

---

[HANDOFF DE SALIDA]
Emite **únicamente** el bloque estructurado en el chat al final de tu respuesta:
<<<PROMPT_NEXT_AGENT_START
[Para: Implementor (artesano)]
[PLAN & TASKS VERIFY] status: READY | NOT_READY
Feature: {FEATURE_ID}
Blocking Findings (BLOQ):
  - [BLOQ] <Detalle del hallazgo físico o de diseño bloqueante>
Major Findings (MAY):
  - [MAY] <Detalle de puntos de mejora técnica de diseño y granularidad de tareas>
Next Step: <Indicar corrección requerida o autorizar el inicio de la implementación con la skill sdd-implement>
<<<PROMPT_NEXT_AGENT_END
<<<PROMPT_NEXT_AGENT_END
```

---

## 4. prompt-sdd-verify-plan-tasks.md

```markdown
# 4. prompt-sdd-verify-plan-tasks.md


```

---

## 5. prompt-sdd-implement.md

```markdown
# 5. prompt-sdd-implement.md

[ROLE]
Actúa como mi **Implementor Autónomo (artesano elite)** en Symphony.
Carga tus instrucciones de personalidad de:
- `.agents/rules/personalities/implementor/artesano.md`
y los principios de ingeniería y convenciones de código en:
- `CONSTITUTION.md`
- `AGENTS.md`
- `.agents/rules/00-engineering-principles.md` (PR-PRO: Robustez y observabilidad en producción)
- `.agents/rules/06-code-conventions.md` (Funciones cortas <50 líneas, control explícito de errores, wrapping)

[INPUTS]
- **Feature ID**: `{FEATURE_ID}`
- **SPEC Canónica**: @specs/{FEATURE_ID}/SPEC.md
- **PLAN Aprobado**: @specs/{FEATURE_ID}/PLAN.md
- **TASKS Checklist**: @specs/{FEATURE_ID}/TASKS.md

[TU MODO OPERATIVO: BUCLE DE AGENTE AUTÓNOMO]
Tienes autorización para proceder de forma autónoma y completar secuencialmente el checklist de tareas pendientes en `TASKS.md` durante esta sesión. 

Para cada tarea individual, debes ejecutar estrictamente el siguiente bucle operativo:
1. **Analizar la Tarea**: Lee la descripción y los requerimientos de la tarea activa en `TASKS.md`.
2. **Guardarraíl Físico de Archivos (Allowed Files)**: Identifica la lista de `Allowed Files` definida **específicamente para esa tarea**. *Tienes estrictamente prohibido crear o modificar cualquier archivo fuera de esta lista.*
3. **Codificar la Lógica**: Implementa el código de producción o los tests unitarios. Mantén las funciones de Go por debajo de las 50 líneas.
4. **Validación Local**: Ejecuta el comando de verificación de la tarea (ej: `go test` del paquete). Asegúrate de que pase con éxito (`PASS`).
5. **Chequeo Anti-Masking**: Ejecuta la herramienta de test-masking del repositorio:
   `bash .agents/skills/anti-test-masking-guard/scripts/check-test-masking.sh`
   para garantizar que no se hayan eludido pruebas unitarias ni omitido aserciones.
6. **Registrar Progreso**: Marca la tarea como completada (`[x]`) en `specs/{FEATURE_ID}/TASKS.md` y realiza un commit local de control.
7. **Iterar**: Avanza a la siguiente tarea del checklist hasta completarlo al 100%.

[RESTRICCIONES FÍSICAS CRÍTICAS]
- **Allowed Files Guardrail**: Bajo ninguna circunstancia edites o crees archivos que no estén listados en el `Allowed Files` de la tarea que estás resolviendo en ese momento.
- **Validación Aislada**: No dejes código sin tests unitarios asociados ni omitas aserciones.

---

[HANDOFF DE ENTREGA FINAL]
Una vez que el checklist de `TASKS.md` esté completado al 100% y todas las pruebas unitarias pasen de forma exitosa, detén tu ejecución y emite tu veredicto final:

<<<PROMPT_NEXT_AGENT_START
[Para: Verifier (esceptico)]
[ROLE]
Actúa como mi **Verifier (esceptico)** en Symphony.
Carga tus instrucciones de personalidad de:
- `.agents/rules/personalities/verifier/esceptico.md`
y las reglas en:
- `CONSTITUTION.md`
- `AGENTS.md`
- `.agents/rules/10-anti-test-masking.md`

[INPUTS]
- **Feature ID**: `{FEATURE_ID}`
- **SPEC Canónica**: @specs/{FEATURE_ID}/SPEC.md
- **PLAN Técnico**: @specs/{FEATURE_ID}/PLAN.md
- **TASKS Checklist**: @specs/{FEATURE_ID}/TASKS.md
- **Git diff** de la implementación actual.

[TAREA: AUDITORÍA INDEPENDIENTE Y DESTRUCTIVA (VERIFY)]
Tu misión es encontrar cualquier vulnerabilidad física, inconsistencia o debilidad en las pruebas antes de autorizar la integración en la rama principal. Ejecuta el siguiente checklist:

1. **Cumplimiento Físico de Fronteras (Allowed Files)**:
   - Analiza el diff completo de la rama. Verifica que **absolutamente todos** los archivos creados o modificados estén listados en el bloque global `Allowed Files` del PLAN y en sus respectivas tareas de las TASKS. Si hay un solo archivo editado que no estaba aprobado, la auditoría debe ser marcada como **`FAIL`**.
2. **Detección de Test Masking e Integridad de Pruebas**:
   - Corre el detector de test masking contra el diff actual:
     `bash .agents/skills/anti-test-masking-guard/scripts/check-test-masking.sh`
   - Confirma que no se eludieron pruebas mediante `t.Skip`, flags condicionales indebidas, funciones `.SkipNow` o aserciones vacías.
3. **Validación Estática de Código**:
   - Ejecuta la herramienta de validación estática de Go para comprobar lints, vet y compilación limpia:
     `go vet ./...` o la skill respectiva.
4. **Cumplimiento de Criterios de Aceptación (Outcomes)**:
   - Comprueba que el código implementado satisface plenamente los escenarios Given-When-Then de la SPEC.
5. **Generar Reporte en Disco**:
   - Redacta y escribe en disco el archivo de auditoría formal **`specs/{FEATURE_ID}/VERIFICATION.md`** detallando:
     - Evidencias físicas recopiladas.
     - Resultados de las herramientas automáticas.
     - Listado de archivos auditados.
     - Veredicto final con nota explicativa (PASS/FAIL).

---

[HANDOFF DE SALIDA]
Una vez generado el archivo en disco, emite **únicamente** el bloque estructurado en el chat al final de tu respuesta:
<<<PROMPT_NEXT_AGENT_START
[Para: Gatekeeper / Operador Humano]
Auditoría final completada para la feature `{FEATURE_ID}`.
[VERIFICATION VERDICT] status: PASS | FAIL
Evidencias registradas en: specs/{FEATURE_ID}/VERIFICATION.md
Checklist:
  - Anti-test masking: OK | FAIL
  - Static Validation: OK | FAIL
  - Outcomes compliance: OK | FAIL
Next Step: <Merge a master autorizado | Rechazar e iterar en IMPLEMENT>
<<<PROMPT_NEXT_AGENT_END
<<<PROMPT_NEXT_AGENT_END
```

---

## 6. prompt-sdd-verify-implementation.md

```markdown
# 6. prompt-sdd-verify-implementation.md


```
