---
type: learning
schema_version: 1
scope: global
created: "2026-09-09"
updated: "2026-09-14"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[deployment-proof]]"
  - "[[e2e-gated-validation]]"
  - "[[grep-acotado-no-prueba-ausencia]]"
aliases:
  - PASS declarado no es PASS verificado
  - overclaim de cierre
  - exit 0 no es evidencia
confidence: verified
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/global
  - project/agents-os
  - tech/agents-os
---

# PASS declarado no es PASS verificado

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- Un veredicto sintetizado a partir de que "nada falló visiblemente" no es una verificación. Un comando en verde, un reviewer que no reportó, un estado lógico terminal o una suite que corrió sin aserciones sobre el hecho en cuestión pueden coexistir con el resultado contrario.

## Por qué importa

- El overclaim es la falla más cara del sistema porque destruye la utilidad de todo lo que se persistió después: una decisión rotulada `PASS / CLOSED` sin prueba física entra al retrieval con la misma autoridad que una certificada, y el siguiente agente construye encima.

## Aplicabilidad

- Todo cierre, gate, certificación o review que produzca un veredicto, en cualquier dominio y superficie.

## Cómo aplicarlo

- Nombrar la capa que posee la semántica del resultado y verificar ahí, no en la capa que lo orquesta.
- Distinguir tres estados y no colapsarlos: verificado con evidencia citable, no verificado, y bloqueado. "Bloqueado" es un resultado legítimo; "PASS" sin evidencia no lo es.
- Cuando la superficie no permite ejecutar el gate, decirlo explícitamente y declarar el control compensatorio aplicado, en vez de afirmar que el gate corrió.
- Auditar el mapeo de severidades del agregador antes de creerle su veredicto: si alguna severidad del provider se proyecta a `PASS`, ese hallazgo desaparece del resumen, de los contadores y del modo estricto, y el verde que queda es literalmente cierto y materialmente falso. Un hallazgo sólo puede mapear a estados de hallazgo — `FAIL`, `WARN`, `INFO` —, nunca a `PASS`.
- Revisar si el agregador reconstruye una semántica que el provider ya posee. Dos dueños del mismo juicio no se contradicen el día que se escriben: se contradicen el día que uno de los dos se limpia, y ahí el mismo defecto se cuenta dos veces.

## Evidencia

- Instancia mecánica al 2026-09-14 en el propio agregador del Doctor unificado: una severidad `LOW` se proyectaba a `status: PASS` y quedaba fuera de contadores, resumen y `--strict`; y el agregador reconstruía un gate cuya semántica ya era del provider. Ambos defectos aparecieron en la herramienta construida para detectar verdes falsos. Ver [[2026-09-14-agents-os-p4-adversarial-verification-session-feedback]].
- Once sesiones a lo largo del período, cruzando dominios y herramientas: [[2026-07-26-echo-forge-g3-overclaim-session-feedback]], [[2026-07-26-echo-forge-g4-rejected-overclaim-and-skipped-tests-feedback]], [[2026-08-27-playmaker-fury-lock-orchestration-session-feedback]] ("el primer PASS fue una síntesis sin reviewers exitosos, potencialmente engañosa"), [[2026-09-06-echo-forge-independent-reality-review-session-feedback]], [[2026-09-08-echo-e01-s0-contract-verification-session-feedback]].
