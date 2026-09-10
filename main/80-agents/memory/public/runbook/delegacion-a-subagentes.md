---
type: runbook
schema_version: 1
scope: global
created: "2026-09-09"
updated: "2026-09-09"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[subagente-devuelve-reporte-vacio]]"
  - "[[agents-os-agent-run-register]]"
aliases:
  - delegación a subagentes
  - contrato de delegación
  - brief de subagente
confidence: verified
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/global
  - project/agents-os
  - tech/agents-os
---

# delegacion-a-subagentes

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Delegar lectura o auditoría a subagentes sin perder evidencia, sin matarlos por inactividad y sin que la cadena deforme los datos que se les entregaron.

## Precondiciones

- La tarea es de lectura o análisis acotable, no una decisión que deba tomar el agente principal.
- Existe una lista concreta de lo que se pide de vuelta; si no se puede enumerar el output, la tarea todavía no está lista para delegar.

## Procedimiento

1. Congelar antes de delegar todo dato que el subagente deba preservar sin reinterpretar (orden, identificadores, matriz de casos). Se entrega como material inmutable, no como contexto a resumir.
2. Acotar a una o dos tareas por subagente, con hints de ubicación (`path`, `file:line`, nombre de símbolo). Un prompt de cuatro o cinco tareas heterogéneas tiende a superar la ventana de inactividad de la superficie.
3. Declarar en el prompt el output obligatorio y su formato, y que ese output viaja **íntegro en el mensaje final** — no en archivos intermedios ni en un resumen.
4. Al recibir el resultado: si el mensaje final llega vacío o sólo con un acuse ("audit complete"), tratarlo como falla recuperable inmediata y pedir el reporte por continuación del mismo subagente antes de reejecutar la tarea.
5. Verificar antes de usar: contrastar dos o tres hallazgos contra la fuente. Un hallazgo de subagente no verificado no funda una decisión ni una escritura persistente.
6. Registrar la delegación fallida cuando no hubo contribución material: no se crea `agent_run` sin trabajo atribuible, pero el intento se anota en el feedback de la sesión para que el patrón sea contable.

## Validación

- El output obligatorio llegó completo en el mensaje final.
- Los datos congelados del paso 1 volvieron sin alteración.
- Al menos dos hallazgos verificados contra la fuente antes de actuar.

## Rollback / recuperación

- Si el subagente murió sin resultado, reintentar con el alcance partido en mitades antes de asumir que la tarea no es delegable. Si el segundo intento también muere, hacerla en el agente principal y anotarlo: el costo de la delegación ya superó su beneficio.

## Evidencia

- [[2026-08-26-scout-subagent-timeouts-session-feedback]] — dos de tres subagentes muertos por inactividad de 600s sobre prompts multi-parte.
- [[2026-08-26-zcode-subagent-final-report-loss-session-feedback]] — mensaje final vacío; la evidencia sólo llegó al retomar el mismo subagente.
- [[2026-09-09-crear-context-flink-session-feedback]] — dos subagentes sin mensajes, archivos ni resultado atribuible, sin señal para distinguir trabajo lento de agente detenido.
- [[2026-09-01-crear-context-review-remediation-session-feedback]] — el orden entregado se perdió al inicio de la cadena porque no se fijó una matriz inmutable antes de delegar.
