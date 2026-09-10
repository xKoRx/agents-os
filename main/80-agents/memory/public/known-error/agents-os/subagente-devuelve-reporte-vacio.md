---
type: known_error
schema_version: 1
scope: global
created: "2026-09-09"
updated: "2026-09-09"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[delegacion-a-subagentes]]"
aliases:
  - subagente devuelve reporte vacío
  - subagent final report loss
  - subagent inactive for 600000ms
confidence: verified
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/global
  - project/agents-os
  - tech/agents-os
---

# Subagente termina sin entregar su reporte

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- El subagente termina con un acuse sin contenido ("audit complete") y el reporte pedido no aparece en ninguna parte.
- O muere con `inactive for 600000ms` sobre un prompt de investigación amplio.
- O queda ejecutando sin mensajes, archivos ni resultado atribuible, sin señal intermedia que distinga trabajo lento de agente detenido.

## Causa

- El output obligatorio no viaja en el mensaje final del subagente, y la superficie no garantiza entrega parcial. Un prompt con varias tareas heterogéneas alarga el tramo sin salida hasta cruzar la ventana de inactividad.

## Impacto

- La evidencia se pierde en silencio y se detecta tarde, cuando ya se decidió sobre un vacío. El costo medido por subagente muerto ronda los diez minutos, más la reejecución.

## Detección

- Comparar el mensaje final contra el output obligatorio declarado en el prompt. Un final que no contiene ese output es falla, no éxito, aunque el estado diga completado.

## Mitigación

- Retomar el mismo subagente y pedirle el reporte antes de reejecutar la tarea: en el caso observado la evidencia completa sí estaba y llegó al continuar.
- Para la siguiente delegación, partir el alcance en una o dos tareas y declarar que el output va íntegro en el mensaje final. Procedimiento completo en [[delegacion-a-subagentes]].

## Evidencia

- [[2026-08-26-zcode-subagent-final-report-loss-session-feedback]] — final vacío, evidencia recuperada al retomar; la propia nota pidió promover esto si reaparecía.
- [[2026-08-26-scout-subagent-timeouts-session-feedback]] — dos de tres subagentes muertos por inactividad.
- [[2026-09-09-crear-context-flink-session-feedback]] — reaparición catorce días después, sin heartbeat ni fallback atribuible.
