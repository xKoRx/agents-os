---
type: project
schema_version: 1
owner: agent
root: false
status: completed
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge]]"
sprint: "[[A26Q2S7]]"
start: "2026-08-14"
due:
progress: 100
repo: github.com/xKoRx/symphony
jira:
prs:
aliases:
  - Echo Forge WFM Exporter Performance
  - WFM exporter latency
tags:
  - application/echoforge
  - area/echo
  - kind/project
  - tech/echo-forge
created: "2026-08-14"
updated: "2026-08-15"
---

# Echo Forge - Optimización de Latencia WFM Exporter

> [!info]+ Proyecto agente
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** [[A26Q2S7]] · **Parent:** [[Echo Forge]]

## 🎯 Objetivo

Implementar exactamente tres cambios en la tarea WFM de Echo Forge:

1. Corregir la doble ejecución de `EchoForgeWFMExporter`.
2. Ejecutar una estrategia por task Temporal, reutilizando el patrón normal de las demás tasks sin inventar otra arquitectura.
3. Mejorar los heartbeats para que informen estrategia, fase y progreso real.

La verificación y el rollout existen para demostrar esos tres cambios; no son alcance funcional adicional.

## 🚨 Invariante arquitectónica no negociable

> [!danger]+ 1 VM = 1 worker = 1 task
> Cada VM SQX aloja un worker. Cada worker atiende como máximo una task/activity a la vez (`MaxConcurrentActivityExecutionSize: 1`). Por diseño, nunca se ejecutan dos tasks simultáneas dentro del mismo worker ni compiten dos ejecuciones SQX por los mismos archivos locales.

- Temporal puede distribuir varias tasks entre varias VMs, pero cada worker las consume secuencialmente.
- `databanks/input`, `databanks/output`, `overview/` y `exporter.properties` pueden reutilizarse y limpiarse entre tasks porque el worker es serial.
- **No implementar locks, mutexes, semáforos, slots, colas host-locales, workspaces por request ni scopes de filesystem para proteger una concurrencia que no existe.**
- No introducir sticky workers, afinidad por host ni task queues por VM.
- Esta invariante solo puede cambiar mediante una decisión arquitectónica separada y aprobada explícitamente por el owner antes de aumentar la concurrencia del worker.
- Fuente canónica: [[2026-08-14-echo-forge-one-vm-one-worker-one-task]]. Evidencia previa: [[2026-07-31-task-local-dirs-input-output-only]].

## 📊 Estado actual

- **Cerrado por el owner (2026-08-15).** G5 accepted. C1-C3 en release `9.9.11`. Wave `example_flow_4` PASS (9 tasks WFM, 1 estrategia cada una, Evaluate OK, MT5 compile 7/7 backtest 7/7). Tests existentes de ProjectActivity corregidos (`write_exporter_properties`).
- Stager de cutover quedó hotfix-eado y desplegado en los cuatro hosts; ver [[stager-staged-without-runtime-request]].
- Código C1-C3 puede seguir en working tree de Symphony `master` (sin commit) si el owner no pidió push.

## Alcance congelado

### IN — solo estas tres modificaciones

- Una sola ejecución de `EchoForgeWFMExporter` por task.
- Una estrategia de entrada por task Temporal.
- Heartbeats periódicos con contexto dinámico.

### OUT — no agregar al proyecto

- Locks o cualquier protección de concurrencia dentro de un worker.
- `scope_id`, hashes de `wave+strategy`, workspaces o directorios por estrategia.
- Un layout MinIO nuevo como `strategies/<scope_id>/`.
- Ordenar, deduplicar o reinterpretar la lista de estrategias.
- Cambiar la identidad canónica de una estrategia.
- Rediseñar o cambiar la semántica del fan-in, retries, fallos parciales o la decisión de evaluar resultados parciales. El join mínimo de futures vigente requerido para completar el fan-out sí forma parte de C2.
- Obligar a reutilizar o reemplazar una activity concreta si el patrón mínimo existente permite ambas opciones.
- Crear `dynamic_heartbeat.go` como requisito; el archivo es un detalle de implementación.
- Agregar atributos OTel, dashboards o telemetría ajena al heartbeat solicitado.
- Exigir un canary multi-worker como nueva decisión arquitectónica.
- Cambiar timeouts, matriz WFM 6×9, plugin Java, evaluator, schema, selección o matemática WFM.

Toda semántica no mencionada se preserva tal como está. Si el código revela que uno de los tres cambios exige alterar una semántica OUT, el agente se detiene y devuelve el gate a revisión; no inventa la decisión.

## Contratos de implementación

### C1 — ejecución única

Para una task cuyo proyecto raíz ya es `EchoForgeWFMExporter`:

```text
preparar input y exporter.properties
→ ExecuteAndWait(EchoForgeWFMExporter) exactamente una vez
→ importar/validar resultados existentes sin volver a ejecutar SQX
→ publicar por el flujo vigente
```

El flujo genérico `proyecto A → exporter B`, cuando `A != B`, debe seguir funcionando.

### C2 — una estrategia por task

```text
evaluate_wfm recibe [S1, S2, ... Sn]
→ primer loop: despacha todas las tasks WFM y registra futures, sin esperar
→ segundo loop: espera/recoge los futures con correlación indexada
→ cada task recibe exactamente una estrategia
→ cada task ejecuta C1 y publica con el contrato vigente
→ continúa con la activity evaluate_wfm y su semántica actual
```

- No ordenar ni deduplicar; preservar orden y multiplicidad de entrada.
- No crear rutas, IDs, layouts, reglas de retry ni políticas de fallo nuevas.
- Usar la task queue normal. El paralelismo ocurre entre VMs; nunca dentro de un worker.
- Copiar el patrón existente de las demás tasks del pipeline y realizar el cambio mínimo.

### C3 — heartbeat con contexto

El heartbeat periódico debe reflejar el último estado real conocido, al menos:

```json
{
  "wave_key": "...",
  "strategy": "...",
  "phase": "executing_sqx",
  "attempt": 1,
  "elapsed_ms": 123456,
  "completed": 0,
  "total": 1
}
```

Fases mínimas: `preparing`, `executing_sqx`, `collecting_outputs`, `persisting`, `completed`. Los nombres pueden adaptarse al contrato existente, pero el ticker no puede volver a emitir un mensaje estático que pise el contexto vigente.

## ✅ Tareas

- [x] T0.1 Crear SPEC/CHANGE/RCA de los tres cambios y dejar explícita la invariante serial #owner/agent #type/spec #area/echo
- [x] T1.1 Revalidar PLAN/TASKS para exigir dispatch-all-before-wait sin incorporar alcance OUT #owner/agent #type/plan #area/echo
- [x] T2.1 Corregir la doble ejecución y probar los casos fixed exporter y `A != B` #owner/agent #type/dev #area/echo
- [x] T3.1 Partir WFM en una estrategia por task usando el patrón existente #owner/agent #type/dev #area/echo
- [x] T4.1 Emitir heartbeats periódicos con estrategia, fase, attempt y elapsed #owner/agent #type/dev #area/echo
- [x] T5.1 Ejecutar regresión focalizada, suite pertinente y preparar rollout reversible #owner/agent #type/test #area/echo

## Gates

| Gate | Estado | Criterio de salida | Acepta | Habilita |
|---|---|---|---|---|
| G0 | accepted | SPEC + CHANGE + RCA describen solo C1-C3 y la invariante serial | owner | F1 |
| G1 | accepted | PLAN/TASKS exigen dispatch-all-before-wait, trazabilidad completa y cero alcance OUT | owner | F2 |
| G2 | accepted | Fixed exporter ejecuta una vez y `A != B` conserva su comportamiento | owner | F3 |
| G3 | accepted | Cada task recibe exactamente una estrategia; no hay locks ni cambios semánticos extra | owner | F4 |
| G4 | accepted | Heartbeat periódico mantiene contexto dinámico correcto | owner | F5 |
| G5 | review | Tests/regresión PASS y diff contiene únicamente los tres cambios | owner | cierre humano |

## Paquetes autónomos

### Paquete autónomo Fase 0 — SPECIFY

**Misión exacta**

Crear la especificación durable de C1-C3 y el RCA de la doble ejecución, sin tocar código productivo.

**Precondiciones verificables**

- Leer este proyecto y confirmar `G0=pending`.
- Confirmar la invariante en `VAULT_ROOT/80-agents/memory/public/decision/symphony/2026-08-14-echo-forge-one-vm-one-worker-one-task.md`.
- Inspeccionar el flujo real que llama `ExecuteAndWait` y el workflow `evaluate_wfm`.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Echo Forge/agentes/Echo Forge - Optimización de Latencia WFM Exporter.md`.
- Reglas SDD y SPECs WFM vigentes del repo Symphony.

**Decisiones**

- Congelar únicamente C1-C3.
- Registrar que la serialización del worker es arquitectura vigente, no un riesgo que esta feature deba resolver.

**Implementación paso a paso**

1. Documentar el call graph que produce las dos ejecuciones.
2. Especificar la preparación previa al único `ExecuteAndWait`.
3. Especificar una estrategia por task sin cambiar orden, multiplicidad ni contratos remotos.
4. Especificar el heartbeat contextual mínimo.
5. Ejecutar el verificador de SPEC y dejar los artefactos en Review.

**Archivos esperados**

- SPEC, CHANGE y RCA dentro de la feature correspondiente en Symphony.

**No tocar**

- Código Go/Java productivo, timeouts, retries, layouts de storage y evaluator WFM.

**Spikes permitidos**

- Solo lectura o pruebas existentes para confirmar nombres y call graph.

**Tests y asserts**

- Verificador SDD PASS.
- Búsqueda textual confirma que la SPEC no prescribe locks, scopes ni layouts nuevos.

**Entregables/Gate G0**

- SPEC + CHANGE + RCA en Review, trazables a C1-C3.

**Handoff**

- Actualizar T0.1, G0, progreso y bitácora. No iniciar F1 sin aceptación.

### Paquete autónomo Fase 1 — PLAN/TASKS

**Misión exacta**

Convertir la SPEC aceptada en un plan de cambios mínimos y tareas ejecutables.

**Precondiciones verificables**

- G0 aceptado.
- SPEC/CHANGE/RCA verificadas.
- Releer `VAULT_ROOT/10-projects/Echo Forge/agentes/Echo Forge - Optimización de Latencia WFM Exporter.md` y comprobar que OUT no cambió.

**Lectura obligatoria**

- Artefactos SDD aceptados.
- Tests existentes de pipeline, workflow y heartbeat.

**Decisiones**

- Elegir el menor conjunto de archivos y funciones que implementa C1-C3.
- Reutilizar patrones existentes; no crear frameworks ni abstracciones anticipatorias.

**Implementación paso a paso**

1. Mapear cada requisito a código y prueba.
2. Separar tareas de ejecución única, estrategia/task y heartbeat.
3. Exigir un loop que despache y registre todos los futures antes de un segundo loop de `Get`, preservando correlación indexada y paridad Generic/Group.
4. Revisar el plan contra la lista OUT.

**Archivos esperados**

- PLAN y TASKS de la feature.

**No tocar**

- Código productivo o infraestructura.

**Spikes permitidos**

- Inspección focalizada para resolver ubicaciones exactas de cambios.

**Tests y asserts**

- Verificador PLAN/TASKS PASS.
- Trazabilidad completa C1-C3; ninguna tarea para locks, scopes, layouts, fan-in nuevo u OTel.

**Entregables/Gate G1**

- PLAN/TASKS aceptables y diff previsto acotado.

**Handoff**

- Actualizar T1.1, G1, progreso y bitácora. No iniciar F2 sin aceptación.

### Paquete autónomo Fase 2 — Corregir doble ejecución

**Misión exacta**

Garantizar un solo `ExecuteAndWait` cuando la task ya ejecuta el fixed exporter WFM.

**Precondiciones verificables**

- G1 aceptado.
- Worktree auditado y cambios ajenos identificados.
- Contrato C1 visible en `VAULT_ROOT/10-projects/Echo Forge/agentes/Echo Forge - Optimización de Latencia WFM Exporter.md`.

**Lectura obligatoria**

- Implementación y tests de `execute_sqx`, `import_metadata`, builder y configuración WFM.
- SPEC/PLAN/TASKS aceptados.

**Decisiones**

- Preparar input y properties antes de ejecutar.
- Evitar la segunda ejecución solo cuando raíz y exporter representan el mismo proyecto fijo.

**Implementación paso a paso**

1. Escribir primero tests que cuenten invocaciones.
2. Reordenar la preparación necesaria antes del único execute.
3. Convertir el paso posterior en consumo/importación de resultados ya producidos para el caso fixed.
4. Preservar el flujo genérico `A != B`.

**Archivos esperados**

- Archivos mínimos del builder/steps y sus tests, según PLAN.

**No tocar**

- Plugin Java, timeouts, concurrencia del worker, storage layout o evaluator.

**Spikes permitidos**

- Ninguno salvo una prueba de call count aislada.

**Tests y asserts**

- Caso WFM fixed: `ExecuteAndWait` count = 1.
- Caso `A != B`: comportamiento previo preservado.
- Properties disponibles antes de la ejecución WFM.

**Entregables/Gate G2**

- Fix y tests focalizados PASS.

**Handoff**

- Actualizar T2.1, G2, progreso y bitácora con archivos y comandos exactos.

### Paquete autónomo Fase 3 — Una estrategia por task

**Misión exacta**

Hacer que la exportación WFM despache y procese exactamente una estrategia por task Temporal.

**Precondiciones verificables**

- G2 aceptado.
- La ejecución única está cubierta por tests.
- Confirmar en `VAULT_ROOT/80-agents/memory/public/decision/symphony/2026-08-14-echo-forge-one-vm-one-worker-one-task.md` que no corresponde implementar exclusión local.

**Lectura obligatoria**

- Workflow `evaluate_wfm`, DTOs y patrón vigente de tasks por elemento.
- Contratos remotos y storage actualmente usados por WFM.

**Decisiones**

- Cada elemento recibido produce una task con una sola estrategia.
- Preservar orden, multiplicidad, retry, fallo y publicación actuales.

**Implementación paso a paso**

1. Añadir pruebas para N inputs y payload unitario por task.
2. Aplicar el patrón de despacho existente del pipeline.
3. Adaptar la ejecución para preparar solo la estrategia del payload.
4. Mantener exactamente el contrato remoto y la continuación actual del workflow.

**Archivos esperados**

- Workflow/DTO/activity mínimos definidos por PLAN y sus tests.

**No tocar**

- Concurrencia del worker, locks, scopes, orden/dedupe, layout MinIO, políticas de retry o semántica de fallos parciales.

**Spikes permitidos**

- Ninguno; copiar el patrón existente más cercano.

**Tests y asserts**

- N estrategias recibidas producen N tasks.
- Cada payload contiene exactamente una estrategia.
- Orden y duplicados de entrada se preservan.
- El diff no contiene locks, semáforos, hashes de scope ni paths nuevos por estrategia.

**Entregables/Gate G3**

- Partición por task implementada con tests PASS y sin alcance extra.

**Handoff**

- Actualizar T3.1, G3, progreso y bitácora; enumerar cualquier semántica preservada.

### Paquete autónomo Fase 4 — Heartbeats con contexto

**Misión exacta**

Hacer que cada heartbeat periódico describa la estrategia y fase realmente activas.

**Precondiciones verificables**

- G3 aceptado.
- Existe una estrategia única en el contexto de cada task.
- Contrato C3 disponible en `VAULT_ROOT/10-projects/Echo Forge/agentes/Echo Forge - Optimización de Latencia WFM Exporter.md`.

**Lectura obligatoria**

- Manager/ticker de heartbeat y llamadas actuales desde steps.
- Tests Temporal de heartbeat existentes.

**Decisiones**

- Mantener el último estado contextual en una estructura segura para el ticker.
- Implementar en los archivos existentes cuando sea suficiente.

**Implementación paso a paso**

1. Añadir tests que reproduzcan el mensaje estático sobrescribiendo hitos.
2. Incorporar wave, estrategia, fase, attempt, elapsed y progreso conocido.
3. Actualizar el estado al cambiar de fase.
4. Verificar cancelación y cierre del ticker sin goroutine leaks.

**Archivos esperados**

- Implementación de heartbeat existente y tests; archivo nuevo solo si PLAN demuestra necesidad.

**No tocar**

- OTel, dashboards, timeouts Temporal o reglas de retry.

**Spikes permitidos**

- Ninguno.

**Tests y asserts**

- Heartbeats sucesivos conservan estrategia y fase vigentes.
- `attempt` y `elapsed_ms` avanzan correctamente.
- Ticker se detiene al completar/cancelar.

**Entregables/Gate G4**

- Heartbeat contextual implementado y pruebas PASS.

**Handoff**

- Actualizar T4.1, G4, progreso y bitácora con un ejemplo de payload real.

### Paquete autónomo Fase 5 — Verificación y rollout

**Misión exacta**

Demostrar que el diff contiene solamente los tres cambios y que no rompe los contratos existentes.

**Precondiciones verificables**

- G2-G4 aceptados.
- Worktree y base de comparación identificados.
- Lista OUT disponible en `VAULT_ROOT/10-projects/Echo Forge/agentes/Echo Forge - Optimización de Latencia WFM Exporter.md`.

**Lectura obligatoria**

- Diff completo, SPEC/PLAN/TASKS, tests y runbook de despliegue vigente.

**Decisiones**

- Verificar proporcionalmente al riesgo sin convertir el rollout en una feature nueva.
- Revertir el release completo si falla un criterio de aceptación.

**Implementación paso a paso**

1. Auditar el diff contra IN/OUT.
2. Ejecutar tests focalizados y suite pertinente.
3. Verificar race/leaks si el heartbeat usa goroutines.
4. Ejecutar el procedimiento de rollout ya existente y observar una task WFM.
5. Registrar evidencia de una ejecución SQX, payload unitario y heartbeats contextuales.

**Archivos esperados**

- Artefactos de verificación/handoff de la feature; sin componentes productivos nuevos.

**No tocar**

- Arquitectura de workers, infraestructura, layouts, timeouts, Java o evaluación WFM.

**Spikes permitidos**

- Ninguno.

**Tests y asserts**

- Fixed exporter count = 1.
- N inputs = N tasks y una estrategia por payload.
- Heartbeats muestran estrategia y fase reales.
- Regresión pertinente PASS.
- Búsqueda/diff confirma ausencia de locks, scopes, layouts y decisiones no solicitadas.

**Entregables/Gate G5**

- Verificación aceptable, evidencia de rollout y rollback documentado.

**Handoff**

- Marcar T5.1 y G5, mover la tarea puente como máximo a Review y esperar aceptación humana.

## Despachos copiables

**Despacho Fase 0**

Trabaja F0 de [[Echo Forge - Optimización de Latencia WFM Exporter]]. Crea únicamente SPEC + CHANGE + RCA para C1-C3. La arquitectura es `1 VM = 1 worker = 1 task`; no propongas locks, scopes ni cambios OUT. Valida SDD, actualiza el proyecto y detente en G0.

**Despacho Fase 1**

Trabaja F1 solo si G0 está aceptado. Crea PLAN/TASKS mínimos y trazables a C1-C3. Reutiliza patrones existentes, excluye toda la lista OUT, actualiza el proyecto y detente en G1.

**Despacho Fase 2**

Trabaja F2 solo si G1 está aceptado. Corrige la doble ejecución, prepara properties antes del execute único y conserva `A != B`. Añade tests de call count, actualiza el proyecto y detente en G2.

**Despacho Fase 3**

Trabaja F3 solo si G2 está aceptado. Implementa una estrategia por task copiando el patrón vigente. Preserva orden, duplicados y semánticas actuales. No hay concurrencia dentro del worker: cero locks/scopes/layouts nuevos. Actualiza el proyecto y detente en G3.

**Despacho Fase 4**

Trabaja F4 solo si G3 está aceptado. Mejora el heartbeat periódico con wave, estrategia, fase, attempt, elapsed y progreso. No agregues OTel ni cambies timeouts/retries. Actualiza el proyecto y detente en G4.

**Despacho Fase 5**

Trabaja F5 solo si G4 está aceptado. Audita que el diff contenga solo los tres cambios, ejecuta regresión y rollout vigente, registra evidencia y mueve la tarea puente como máximo a Review. No cierres la tarea humana.

## 📆 Bitácora

- **2026-08-14** — Proyecto creado a partir del diagnóstico de latencia WFM y la doble ejecución confirmada.
- **2026-08-14** — Scope corregido por el owner a tres cambios: bug de ejecución doble, una estrategia por task y heartbeats con contexto.
- **2026-08-14** — Rechazado y supersedido el plan que inventó locks, scopes, layouts, dedupe y semánticas de fan-in/fallo. Se restablece la arquitectura real `1 VM = 1 worker = 1 task`, se enlaza su decisión canónica y se reduce el proyecto a seis gates: dos de SDD, tres de implementación y uno de verificación.
- **2026-08-14** — F0 y F1 ejecutadas por instrucción explícita del owner. Symphony incorpora `specs/FEAT-SQX-WFM-EXPORT-EXECUTION/{SPEC.md,PLAN.md,TASKS.md}`, CHANGE-001 y RCA-001; auto-revisión SDD y `git diff --check` PASS. No se tocó código productivo ni tests, se preservó el worktree compartido y G1 queda en Review antes de F2.
- **2026-08-14** — Revisión crítica final contra `master`/`origin/master` `17a4b2e`. El código confirmó el patrón vigente de dos loops en `evaluate_wfm`, `evaluate_strategy`, `verify_wfm_evaluated`, `select_robust_run` y sus caminos Group, además del default SDK `MaxConcurrentActivityExecutionSize=1`. SPEC/CHANGE/RCA quedaron inequívocos: despachar todas las `project`/`wfm_exporter` activities antes de cualquier `Get`, luego join indexado sin rediseño semántico de fan-in. G0 permanece accepted; T1.1/G1 vuelven a pending para revalidar PLAN/TASKS en la próxima sesión. No hubo cambios productivos.
- **2026-08-14** — F1 revalidada por instrucción del owner. PLAN/TASKS eliminaron el baseline obsoleto y la propuesta de helper; ahora modifican directamente los bloques Generic/Group con un loop de despacho sin `Get` seguido por join indexado, incluyen completion order invertido y mantienen fail-fast/retries/resultados parciales. `git diff --check` y verificación estructural manual PASS; T1.1 completa, G1 en Review y cero código productivo/tests modificados.
- **2026-08-14** — F2 implementada por despacho explícito del owner (G1 accepted). Builder inserta `write_exporter_properties` antes de `execute_sqx` cuando raíz y exporter resuelven al mismo proyecto; `import_metadata` omite prep/ExecuteAndWait en el caso fijo y conserva A != B. Tests nuevos de orden y call count PASS junto con la regresión de pipeline/steps. G2 en Review; F3 no iniciada.
- **2026-08-14** — F3 implementada por despacho explícito del owner (G2 accepted). `evaluate_wfm` en Generic y Group despacha N activities `project` unitarias, registra futures sin `Get` y junta por índice; duplicados, fail-fast y `passedKeys` se conservan. Tests nuevos PASS; G3 en Review; F4 no iniciada. Resumen: [[2026-08-14-echo-forge-wfm-exporter-latency-f3-summary]].
- **2026-08-14** — F4 implementada por despacho explícito del owner (G3 accepted). `HeartbeatManager` agrega snapshot dinámico BWC; `ProjectActivity` lo usa sólo en `wfm_exporter` con fases reales. Suites `-race` PASS; G4 en Review; F5 no iniciada. Resumen: [[2026-08-14-echo-forge-wfm-exporter-latency-f4-summary]].
- **2026-08-14** — F5 iniciada por despacho explícito del owner (G4 accepted). T5.1 en curso: regresión focalizada, auditoría de diff y troubleshooting de tests existentes desfasados por F2.
- **2026-08-14** — F5 completa. VERIFICATION PASS para C1-C3. TEST_CHANGE_REQUEST abierto para dos tests existentes de overview_exporter. Rollout live no publicado (Stager 0.2.42; `deploy_release.sh` dispara wave completa). G5 en Review; tarea puente humana movida a Review. Resumen: [[2026-08-14-echo-forge-wfm-exporter-latency-f5-summary]].
- **2026-08-15** — Owner cierra el proyecto. Rollout `9.9.11` + wave `example_flow_4` PASS; G5 accepted; tarea puente padre a Done. Cutover Stager documentado en [[stager-staged-without-runtime-request]].

## 🔗 Links

- [[Echo Forge]]
- [[echo-forge]]
- [[2026-08-14-echo-forge-one-vm-one-worker-one-task]]
- [[2026-07-31-task-local-dirs-input-output-only]]
- [[2026-08-14-echo-forge-wfm-exporter-slow-summary]]
- [[2026-08-14-echo-forge-wfm-export-spec-final-review-summary]]
- [[2026-08-14-echo-forge-wfm-plan-tasks-revalidation-summary]]
- [[2026-08-14-echo-forge-wfm-f2-implementation-summary]]
- [[2026-08-14-echo-forge-wfm-exporter-latency-f3-summary]]
- [[2026-08-14-echo-forge-wfm-exporter-latency-f4-summary]]
- [[2026-08-14-echo-forge-wfm-exporter-latency-f5-summary]]
- [[echo-forge-wfm-troubleshooting]]
- `github.com/xKoRx/symphony + specs/FEAT-SQX-WFM-EXPORT-EXECUTION/`
