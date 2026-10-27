---
type: feedback
schema_version: 1
scope: session
created: 2026-10-26
updated: 2026-10-26
area: "[[Echo]]"
project: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-10-26-forge-shot4-cont-close]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-10-26-zcode-glm53-forge-shot4-cont-closure]]"
session_goal: "Shot 4 continuación: brechas residuales B1–B6 del candidato 2681883"
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/echo-forge
  - agent/system1
---

# Session Feedback — 2026-10-26 — forge-shot4cont

## Context

- Agent surface: ZCode (GLM-5.3-Flash)
- Agent run: [[2026-10-26-zcode-glm53-forge-shot4-cont-closure]]
- Session goal: cerrar brechas residuales del Shot 4 de FEAT-SQX-DYNAMIC-GROUP-TARGETS
- Main entity: [[Echo Forge]]

## Observaciones

1. **El oráculo que congeló el defecto.** El candidato traía un test
   adversarial (`TestAdversarialC_DynamicProjectDispatchDoesNotResolve…`)
   cuyo nombre y aserción fijaban como CONTRACT el hecho de que el dispatch
   NO entrega la config efectiva — el defecto exacto que el mandato ordenaba
   corregir. Un oráculo escrito desde el comportamiento observado convierte
   el bug en especificación. Lección: nombrar oráculos por el CONTRATO que
   protegen, nunca por el comportamiento vigente.
2. **Fakes que tapan la brecha.** El fake de ranking del arnés ignoraba
   `LedgerRefs`, así que 24/25 "CORRECTED" del shot anterior eran verdes sin
   ejercitar la resolución real de evidencia. Regla: cuando el mecanismo bajo
   prueba es una ACTIVITY, el oráculo debe montar la activity real (como el
   test de ledger), no un doble que salte la resolución.
3. **Denominador de cobertura no declarado.** El 77.1% reportado no era
   reproducible porque nadie publicó el denominador. Con procedimiento
   versionado sobre el delta completo la cifra real es 59.84%. Regla: toda
   cifra de cobertura se entrega con el script que la produce.
4. **Entorno sin JDK 17** (sólo temurin-11 vía mise): el closure `HexFormat`
   del plugin no compila localmente — preexistente, pero bloquea un
   `build.sh` completo. Mantener registrado el requisito de JDK para
   verificar Java localmente.

## Mejoras propuestas

- Añadir al template de agente-run el campo "denominador y script de
  cobertura" cuando el entregable declare métricas.
- En harnesses con activities dobles, exigir al menos un test por contrato
  que use la activity real (ya existe el patrón en group_ranking_ledger_test).
